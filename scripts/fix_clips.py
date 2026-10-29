#!/usr/bin/env python3
"""Re-synthesize the clips of a fix list and keep a new clip only when the phone check says it is right.

    python3 scripts/fix_clips.py KEY [LIST] [--out checks/fix] [--workers 6] [--batch 200] [--limit N] [--commit]
                                 [--model gemini-3.1-flash-tts-preview] [--voice Laomedeia]

KEY as in tts_gemini.py ("adc" in GitHub Actions).  LIST (default checks/fix/redo.tsv, from make_fix_list.py) has the
columns form, reason, ipa_source, error.  Each clip gets up to three tries, each a different way of asking:

  hyphen    the hyphen as a space (bûtu butu), then as written, then without the hyphen
  letters   the letter names (sgt -> "es dyi ti"); the capital letters, "say each letter's name"; the names again
  english   told it is an English word, not to translate it; then the same with the English (US) voice setting, twice
  extra     as written; in quotation marks, "say only the word in quotes"; as an English word
  cut       as written; a word made of two equal halves is then sent as two words (buwan buwan)

(English rows, abbreviations and forms without a vowel are asked the English or letter-name way whatever the reason.)  ZIPA listens to each
try (as in scripts/phones.py; needs onnxruntime lhotse huggingface_hub imageio-ffmpeg and $ZIPA_SRC) and the error is
the share of the IPA's phones it gets wrong, as in score_phones.py.  A try replaces audio/<letter>/<form>.mp3 when it
is complete (at least 75 % of the phones, not much longer than the word) and clearly better than the old clip: at
least 0.10 less error, and 0.4 or less.  Otherwise the old clip stays.

Writes OUT/results.tsv (one row per try; resumable: a form with a final row is not tried again) and OUT/report.md.
--commit commits audio/ and OUT after each batch and pushes (for GitHub Actions).
"""
import argparse
import csv
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(__file__))
import tts_gemini as T                          # noqa: E402
from score_phones import dist, phones           # noqa: E402

PROMPT = T.DEFAULT_PROMPT
PROMPT_PARTS = ("Read aloud clearly, in a neutral tone. The text is one Filipino word written here in parts; say every "
                "part, with the stress where the accent marks put it, and nothing else.")
PROMPT_EN = ("Read aloud clearly, in a neutral tone. The text is a single English word; say only that word, pronounced "
             "the English way. Do not translate it.")
PROMPT_LETTERS = "Read aloud clearly, in a neutral tone. Say exactly the text, and nothing else."
PROMPT_CAPS = ("Read aloud clearly, in a neutral tone. The text is letters of the alphabet; say the English name of each "
               "letter, one after the other, and nothing else.")
PROMPT_QUOTED = "Read aloud clearly, in a neutral tone. Say only the word in quotation marks, without the quotation marks."
LETTER = dict(zip("abcdefghijklmnopqrstuvwxyz", "ey bi si di i ef dyi eych ay jey key el em en o pi kyu ar es ti yu vi "
                                              "dobolyu eks way zi".split()))
ACCEPT_MAX, ACCEPT_GAIN, COMPLETE = 0.4, 0.10, 0.75


def plain(s):
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()


def clip_path(form):
    return os.path.join("audio", T.letter_dir(form), form + ".mp3")


def tries(form, reason, src):
    """(text, prompt, language) for each try"""
    f = form.strip("-")
    if plain(f).isalpha() and (src == "spelled" or not any(c in "aeiou" for c in plain(f))):
        names = (" ".join(LETTER[c] for c in plain(f)), PROMPT_LETTERS, "fil-PH")
        return [names, (" ".join(plain(f).upper()), PROMPT_CAPS, "fil-PH"), names]
    if src == "english":
        text = f.replace("-", " ")
        return [(text, PROMPT_EN, "fil-PH"), (text, PROMPT_EN, "en-US"), (text, PROMPT_EN, "en-US")]
    if reason == "hyphen" or "-" in f:
        return [(f.replace("-", " "), PROMPT_PARTS, "fil-PH"), (form, PROMPT, "fil-PH"), (f.replace("-", ""), PROMPT, "fil-PH")]
    if reason == "cut":
        p, h = plain(f), len(f) // 2
        if len(f) % 2 == 0 and p[:h] == p[h:]:
            return [(form, PROMPT, "fil-PH"), (f[:h] + " " + f[h:], PROMPT_PARTS, "fil-PH")]
        return [(form, PROMPT, "fil-PH"), (form, PROMPT, "fil-PH")]
    return [(form, PROMPT, "fil-PH"), (f'"{form}"', PROMPT_QUOTED, "fil-PH"), (form, PROMPT_EN, "fil-PH")]


def score(ipa, heard):
    """error (share of the IPA's phones wrong, at most 1), IPA phones, heard phones; glottal stops left out"""
    r0 = [x for x in phones(ipa) if x != "ʔ"]
    h0 = [x for x in phones(heard) if x != "ʔ"]
    return min(dist(r0, h0), len(r0)) / max(1, len(r0)), len(r0), len(h0)


def good(e, nr, nh, e_old):
    return nh >= COMPLETE * nr and nh <= 2 * nr + 4 and e <= ACCEPT_MAX and e <= e_old - ACCEPT_GAIN


def load_listener():
    import phones as P
    P.FFMPEG = P.find_ffmpeg()
    run = P.load_zipa()
    return lambda path: run(P.decode(path))


COLS = ["form", "reason", "try", "text", "language", "heard", "error_before", "error", "outcome"]


def git(*args, check=True):
    return subprocess.run(["git", *args], check=check, capture_output=True, text=True)


def commit(out, message):
    git("add", "-A", "audio", out)
    if git("diff", "--cached", "--quiet", check=False).returncode == 0:
        return
    git("commit", "-qm", message)
    branch = os.environ.get("GITHUB_REF_NAME") or git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    for attempt in range(5):                      # another run may have pushed in the meantime
        if (git("pull", "-q", "--rebase", "origin", branch, check=False).returncode == 0
                and git("push", "-q", "origin", f"HEAD:refs/heads/{branch}", check=False).returncode == 0):
            return
        time.sleep(5 * (attempt + 1))
    sys.exit("could not push")


def report(out, results):
    final = {}
    for r in results:
        if r["outcome"] in ("replaced", "kept"):
            final[r["form"]] = r
    by = {}
    for r in final.values():
        by.setdefault(r["reason"], {"replaced": 0, "kept": 0})[r["outcome"]] += 1
    tries_n = sum(1 for r in results if r["outcome"] != "failed")
    lines = ["# Clip fixes", "",
             "Clips re-synthesized by `scripts/fix_clips.py` from `checks/fix/redo.tsv` (`scripts/make_fix_list.py`). Each try "
             "is checked with ZIPA against the IPA; a clip is replaced only when a try is complete and clearly better "
             f"(error at most {ACCEPT_MAX:.0%} and at least {ACCEPT_GAIN:.0%} lower than before). `results.tsv` has every try.", "",
             f"{len(final)} clips done, {tries_n} tries.", "",
             "| Reason | Replaced | Old clip kept |", "|---|---:|---:|"]
    for k, v in sorted(by.items(), key=lambda kv: -sum(kv[1].values())):
        lines.append(f"| {k} | {v['replaced']} | {v['kept']} |")
    lines.append(f"| **all** | {sum(v['replaced'] for v in by.values())} | {sum(v['kept'] for v in by.values())} |")
    for outcome, title in (("replaced", "Replaced (first 60)"), ("kept", "Old clip kept: no try was good enough (all)")):
        rows = [r for r in final.values() if r["outcome"] == outcome]
        rows = rows[:60] if outcome == "replaced" else rows
        lines += ["", f"## {title}", "", "| Form | Reason | Sent | Heard | Error before → after |", "|---|---|---|---|---|"]
        lines += [f"| {r['form']} | {r['reason']} | {r['text']} | {r['heard'][:50]} | {float(r['error_before']):.2f} → "
                  f"{float(r['error']) if r['error'] else 1:.2f} |" for r in rows]
    open(os.path.join(out, "report.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return by


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keyfile"); ap.add_argument("list", nargs="?", default="checks/fix/redo.tsv")
    ap.add_argument("--out", default="checks/fix"); ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--batch", type=int, default=200); ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--model", default="gemini-3.1-flash-tts-preview"); ap.add_argument("--voice", default="Laomedeia")
    ap.add_argument("--commit", action="store_true")
    ap.add_argument("--fake", help=argparse.SUPPRESS)          # tests: a script that writes the clip instead of the API
    a = ap.parse_args()
    ipa = {r["form"]: r for r in csv.DictReader(open("wordlist_all.tsv", encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE)}
    todo = list(csv.DictReader(open(a.list, encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE))
    os.makedirs(a.out, exist_ok=True)
    res_path = os.path.join(a.out, "results.tsv")
    results = list(csv.DictReader(open(res_path, encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE)) if os.path.exists(res_path) else []
    done = {r["form"] for r in results if r["outcome"] in ("replaced", "kept")}
    todo = [r for r in todo if r["form"] not in done and r["form"] in ipa and os.path.exists(clip_path(r["form"]))]
    if a.limit:
        todo = todo[:a.limit]
    print(f"{len(todo)} clips to fix ({len(done)} done before)", flush=True)
    if not todo:
        report(a.out, results)
        return
    if a.fake:
        def synth(text, prompt, language, path):
            subprocess.run([a.fake, text, language, path], check=True)
    else:
        get_headers, secret = T.auth(a.keyfile)

        def synth(text, prompt, language, path):
            open(path, "wb").write(T.synthesize(get_headers, secret, text, prompt, a.voice, a.model, language))
    listen = load_listener()
    new = not os.path.exists(res_path)
    log = open(res_path, "a", encoding="utf-8")
    if new:
        log.write("\t".join(COLS) + "\n")
    tmp = tempfile.mkdtemp(prefix="fix_clips_")
    stop = threading.Event()
    t0 = time.time()

    def attempt(job):
        k, row, (text, prompt, language) = job
        if stop.is_set():
            return job, None, "stopped"
        path = os.path.join(tmp, f"{k}.mp3")
        try:
            synth(text, prompt, language, path)
            return job, path, None
        except T.AuthError as e:
            stop.set()
            return job, None, str(e)
        except Exception as e:                    # noqa: BLE001 - recorded, the clip is tried again next round
            return job, None, f"{type(e).__name__} {str(e)[:150]}"

    for b in range(0, len(todo), a.batch):
        batch = todo[b:b + a.batch]
        state = {}
        for r in batch:
            w = ipa[r["form"]]
            state[r["form"]] = {"row": r, "plan": tries(r["form"], r["reason"], w["ipa_source"]), "best": None,
                                "e_old": float(r["error"]), "ipa": w["ipa"]}
        for rnd in range(3):
            jobs = [(f"{rnd}_{i}", s["row"], s["plan"][rnd]) for i, s in enumerate(state.values())
                    if rnd < len(s["plan"]) and not s.get("final")]
            if not jobs:
                break
            with ThreadPoolExecutor(max_workers=a.workers) as ex:
                for (k, row, (text, prompt, language)), path, error in ex.map(attempt, jobs):
                    s = state[row["form"]]
                    rec = {"form": row["form"], "reason": row["reason"], "try": str(rnd + 1), "text": text,
                           "language": language, "heard": "", "error_before": f"{s['e_old']:.2f}", "error": "", "outcome": "failed"}
                    if path:
                        heard = listen(path).replace("▁", "").strip()
                        e, nr, nh = score(s["ipa"], heard)
                        rec.update(heard=heard, error=f"{e:.2f}", outcome="rejected")
                        if good(e, nr, nh, s["e_old"]):
                            shutil.move(path, clip_path(row["form"]))
                            rec["outcome"] = "replaced"
                            s["final"] = True
                    else:
                        rec["heard"] = error or ""
                    results.append(rec)
                    log.write("\t".join(rec[c].replace("\t", " ").replace("\n", " ") for c in COLS) + "\n")
            log.flush()
            if stop.is_set():
                sys.exit("auth/permission error, stopping: " + next((r["heard"] for r in reversed(results) if r["outcome"] == "failed"), ""))
        for f, s in state.items():                # no good try: the old clip stays
            if not s.get("final") and any(r["form"] == f and r["outcome"] == "rejected" for r in results):
                rec = {"form": f, "reason": s["row"]["reason"], "try": "-", "text": "", "language": "", "heard": "",
                       "error_before": f"{s['e_old']:.2f}", "error": "", "outcome": "kept"}
                best = min((r for r in results if r["form"] == f and r["outcome"] == "rejected"), key=lambda r: float(r["error"]))
                rec.update(text=best["text"], language=best["language"], heard=best["heard"], error=best["error"])
                results.append(rec)
                log.write("\t".join(rec[c].replace("\t", " ") for c in COLS) + "\n")
        log.flush()
        by = report(a.out, results)
        n_done = min(b + a.batch, len(todo))
        print(f"  {n_done}/{len(todo)} clips, {time.time() - t0:.0f} s: " +
              ", ".join(f"{k} {v['replaced']} replaced / {v['kept']} kept" for k, v in by.items()), flush=True)
        if a.commit:
            commit(a.out, f"Fix clips: {n_done} of {len(todo)} from {a.list} re-synthesized and checked")
    print(f"done in {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
