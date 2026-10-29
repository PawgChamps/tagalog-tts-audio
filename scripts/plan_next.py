#!/usr/bin/env python3
"""Plan the switch to the rebuilt word list: which clips to synthesize, rename, re-synthesize and retire.
Run from the repository root (the Prepare workflow runs it after scripts/fix_ipa.py has given the list its IPA):

    python3 scripts/plan_next.py [--list next/wordlist_ipa.tsv] [--pilot 300] [--pilot-english 60] [--hyphen space]
                                 [--redo auto|yes|no]

Reads the current list wordlist_all.tsv and its clips (the audio/ files of HEAD), respell.tsv, the rebuilt list, and the
phone check of the current clips in checks/phones/wordlist_all/: truncated.tsv and extra_speech.tsv (clips cut short or
with extra speech) and english_vs_tagalog.tsv (whether an English-tagged clip sounds English or Tagalog).
Writes, in next/ (every list has the 7 columns of the word list plus `file`, the clip it makes):
  synthesize.tsv          readings with no clip yet (Tagalog prompt), into audio/
  synthesize_english.tsv  the same for English loanwords (ipa_source english: English prompt)
  redo.tsv                readings whose clip stays (or is renamed) but is wrong: cut short, extra speech, or spoken the
                          English way while the reading is Tagalog; synthesized into next/redo_audio/ and moved over the
                          old clip by the switch. Empty once scripts/fix_clips.py has re-synthesized the wrong clips
                          with its phone check (checks/fix/results.tsv; --redo yes plans them anyway)
  redo_english.tsv        the same for English loanwords, mostly clips spoken the Tagalog way (English prompt)
  pilot.tsv               a sample of synthesize.tsv, two thirds hyphenated forms (where the cuts were)
  pilot_english.tsv       a sample of redo_english.tsv (into next/redo_audio/), to test the English prompt
  rename.tsv              old file -> new file: the same reading spelled differently (letter case, or an acute the voice
                          reads as the default: súkal = sukal)
  retire.tsv              clips whose reading leaves the list
  respell.tsv             form -> text sent to the voice [-> prompt name of scripts/tts_gemini.py]: respell.tsv, plus
                          each reading to synthesize or redo that is asked differently: with --hyphen space (the
                          default) the first try of scripts/fix_clips.py (hyphen as a space with prompt `parts`,
                          abbreviations as letter names with `letters`); join: the halves joined; keep: as spelt
  plan.md                 the counts
Two forms are the same clip when they differ only in letter case or in an acute that adds nothing (checks/forms_fix)."""
import argparse
import collections
import os
import random
import subprocess
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fix_clips import tries                     # noqa: E402
from tts_gemini import read_respell             # noqa: E402

ACU = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}
HEADER = "form\tplain\tstress_source\tipa\trank\tsense\tipa_source"
PHONES = "checks/phones/wordlist_all"
REDO_DIR = "next/redo_audio"


def nfc(s):
    return unicodedata.normalize("NFC", s)


def bare(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def marks(p):
    out = []
    for ch in p:
        if ch in "áéíóú":
            out.append("a")
        elif ch in "àèìòù":
            out.append("g")
        elif ch in "âêîôû":
            out.append("c")
        elif bare(ch) in "aeiou":
            out.append(None)
    return out


def clip_key(f):
    """What the voice is told: lower case, and an acute on the penult of a part with no other mark (or on a one-syllable
    word) taken off, as it only says the default (the same rule as checks/forms_fix/compare_forms.py)."""
    parts = nfc(f).lower().split("-")
    voiced = sum(1 for p in parts if marks(p))
    out = []
    for p in parts:
        mk = marks(p)
        vi = [i for i, ch in enumerate(p) if bare(ch) in "aeiou"]
        if sum(1 for m in mk if m) == 1:
            if len(vi) >= 2 and mk[-2] == "a":
                p = p[:vi[-2]] + ACU[p[vi[-2]]] + p[vi[-2] + 1:]
            elif len(vi) == 1 and mk[0] == "a" and voiced == 1:
                p = p[:vi[0]] + ACU[p[vi[0]]] + p[vi[0] + 1:]
        out.append(p)
    return "-".join(out)


def clip_file(form, top="audio"):
    """<top>/<first letter>/<form>.mp3, as scripts/tts_gemini.py names it."""
    form = nfc(form)
    c = unicodedata.normalize("NFD", form)[:1].lower()
    return f"{top}/{c if c.isalpha() and c.isascii() else '_'}/{form}.mp3"


def read_rows(p):
    lines = open(p, encoding="utf-8").read().split("\n")
    assert lines[0].split("\t")[:7] == HEADER.split("\t"), f"{p}: unexpected header"
    return [ln.split("\t")[:7] for ln in lines[1:] if ln]


def read_col(p, col, where=None):
    """the NFC values of column `col` of a TSV (rows where column where[0] equals where[1]); empty if the file is missing"""
    if not os.path.exists(p):
        return set()
    lines = open(p, encoding="utf-8").read().split("\n")
    head = lines[0].split("\t")
    i = head.index(col)
    j = head.index(where[0]) if where else None
    return {nfc(r[i]) for r in (ln.split("\t") for ln in lines[1:] if ln) if j is None or r[j] == where[1]}


def spoken(form, how):
    """The text sent for a hyphenated form: the hyphen as a space (pag-aari -> pag aari) or the halves joined; an
    affix's own hyphen goes (pag- -> pag). None: the form is sent as it is."""
    if how == "keep" or "-" not in form:
        return None
    return form.strip("-").replace("-", " " if how == "space" else "")


def hyphenated(r):
    return "-" in r[0].strip("-")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", default="next/wordlist_ipa.tsv", help="the rebuilt list, with its IPA fixed")
    ap.add_argument("--pilot", type=int, default=300)
    ap.add_argument("--pilot-english", type=int, default=60)
    ap.add_argument("--hyphen", choices=("space", "join", "keep"), default="space")
    ap.add_argument("--redo", choices=("auto", "yes", "no"), default="auto",
                    help="re-synthesize the clips the phone check found wrong; auto: only if scripts/fix_clips.py has not "
                         "handled them already (no checks/fix/results.tsv)")
    ap.add_argument("--seed", type=int, default=20261029)
    a = ap.parse_args()
    redo_on = a.redo == "yes" or (a.redo == "auto" and not os.path.exists("checks/fix/results.tsv"))
    if not os.path.exists(a.list):
        sys.exit(f"{a.list} is missing: run scripts/fix_ipa.py --list next/wordlist.tsv --out {a.list} first")
    old = read_rows("wordlist_all.tsv")
    new = read_rows(a.list)
    tree = subprocess.run(["git", "ls-tree", "-r", "-z", "--name-only", "HEAD", "--", "audio"], capture_output=True, check=True)
    files = {nfc(x) for x in tree.stdout.decode("utf-8").split("\0") if x.endswith(".mp3")}
    bad = read_col(f"{PHONES}/truncated.tsv", "form") | read_col(f"{PHONES}/extra_speech.tsv", "form")
    sounds_tl = read_col(f"{PHONES}/english_vs_tagalog.tsv", "form", ("verdict", "closer to the Tagalog reading"))
    sounds_en = read_col(f"{PHONES}/english_vs_tagalog.tsv", "form", ("verdict", "closer to the English reading"))

    olds = collections.defaultdict(list)                # plain -> current forms that have a clip
    for r in old:
        f = nfc(r[0])
        if clip_file(f) in files and f not in olds[r[1]]:
            olds[r[1]].append(f)
    keep = {nfc(r[0]) for r in new if clip_file(r[0]) in files}
    claimed = set(keep)
    synth, redo, rename, why = [], [], [], collections.Counter()
    for r in new:
        f = nfc(r[0])
        src = f if f in keep else None
        if src is None:
            src = next((o for o in olds.get(r[1], []) if o not in claimed and clip_key(o) == clip_key(f)), None)
            if src is None:
                synth.append(r)
                continue
            claimed.add(src)
            rename.append((clip_file(src), clip_file(f)))
        english = r[6] == "english"
        reason = ("cut short or extra speech" if src in bad else
                  "English reading, clip sounds Tagalog" if english and src in sounds_tl else
                  "Tagalog reading, clip sounds English" if not english and src in sounds_en else None)
        if reason and redo_on:
            redo.append(r)
            why[reason] += 1
    rename_from = {x for x, _ in rename}
    retire = sorted({clip_file(o) for v in olds.values() for o in v if o not in claimed} - rename_from)

    os.makedirs("next", exist_ok=True)

    def write(name, rows, top):
        with open(f"next/{name}", "w", encoding="utf-8") as fh:
            fh.write(HEADER + "\tfile\n")
            fh.write("".join("\t".join(r + [clip_file(r[0], top)]) + "\n" for r in rows))
        return rows

    en = lambda rows: [r for r in rows if r[6] == "english"]
    tl = lambda rows: [r for r in rows if r[6] != "english"]
    write("synthesize.tsv", tl(synth), "audio")
    write("synthesize_english.tsv", en(synth), "audio")
    write("redo.tsv", tl(redo), REDO_DIR)
    write("redo_english.tsv", en(redo), REDO_DIR)
    rng = random.Random(a.seed)
    order = {id(r): i for i, r in enumerate(new)}
    hy = [r for r in tl(synth) if hyphenated(r)]
    other = [r for r in tl(synth) if not hyphenated(r)]
    n_hy = min(len(hy), a.pilot * 2 // 3)
    pilot = sorted(rng.sample(hy, n_hy) + rng.sample(other, min(len(other), a.pilot - n_hy)), key=lambda r: order[id(r)])
    write("pilot.tsv", pilot, "audio")
    pool = en(redo)
    pilot_en = sorted(rng.sample(pool, min(len(pool), a.pilot_english)), key=lambda r: order[id(r)])
    write("pilot_english.tsv", pilot_en, REDO_DIR)
    with open("next/rename.tsv", "w", encoding="utf-8") as fh:
        fh.write("old_file\tnew_file\n" + "".join(f"{x}\t{y}\n" for x, y in rename))
    with open("next/retire.tsv", "w", encoding="utf-8") as fh:
        fh.write("file\n" + "".join(x + "\n" for x in retire))
    resp = {}                                           # form -> (text, prompt name or "": the list's prompt)
    if os.path.exists("respell.tsv"):
        resp = {k: (t, p or "") for k, (t, p) in read_respell("respell.tsv").items()}
    n_resp = collections.Counter()
    for r in synth + redo:
        f = nfc(r[0])
        if f in resp:
            continue
        if a.hyphen == "space":                         # the first try of scripts/fix_clips.py, tested on 3,526 clips
            text, pname, _ = tries(f, "hyphen" if hyphenated(r) else "new", r[6])[0]
            default = "english" if r[6] == "english" else "tagalog"
            if text == f and pname == default:
                continue
            resp[f] = (text, "" if pname == default else pname)
        else:
            t = spoken(f, a.hyphen)
            if not t:
                continue
            resp[f] = (t, "")
        n_resp[resp[f][1] or "the list's prompt"] += 1
    with open("next/respell.tsv", "w", encoding="utf-8") as fh:
        fh.write("".join(f"{k}\t{t}\t{p}\n" if p else f"{k}\t{t}\n" for k, (t, p) in resp.items()))
    how = {"space": "the hyphen read as a space and told the word is written in parts (prompt `parts`); "
                    "abbreviations as letter names (`letters`)",
           "join": "the halves joined", "keep": "the hyphen kept"}[a.hyphen]
    plan = f"""# Plan for the switch to the rebuilt word list

Made by `scripts/plan_next.py` from `{a.list}`.

| | Forms or clips |
|---|---:|
| current list: forms / clips | {len(old):,} / {len(files):,} |
| rebuilt list: forms | {len(new):,} |
| clips kept as they are | {len(keep) - sum(1 for r in redo if nfc(r[0]) in keep):,} |
| clips renamed (the same reading spelled differently) | {len(rename):,} |
| re-synthesized over a kept or renamed clip (`redo.tsv` / `redo_english.tsv`) | {len(tl(redo)):,} / {len(en(redo)):,} |
| new readings to synthesize (`synthesize.tsv` / `synthesize_english.tsv`) | {len(tl(synth)):,} / {len(en(synth)):,} |
| clips retired (the reading leaves the list) | {len(retire):,} |
| pilot (`pilot.tsv`: hyphenated / `pilot_english.tsv`) | {len(pilot):,} ({n_hy:,}) / {len(pilot_en):,} |

Why clips are re-synthesized: {", ".join(f"{k} {v:,}" for k, v in why.most_common()) or "none"}{"" if redo_on else
" (the clips the phone check found wrong are left to scripts/fix_clips.py, checks/fix/)"}.

Hyphenated forms are sent with {how}: {sum(n_resp.values()):,} new lines in `next/respell.tsv` ({len(resp):,} in all;
by prompt: {", ".join(f"{k} {v:,}" for k, v in n_resp.most_common()) or "none"}).
"""
    open("next/plan.md", "w", encoding="utf-8").write(plan)
    print(plan)


if __name__ == "__main__":
    main()
