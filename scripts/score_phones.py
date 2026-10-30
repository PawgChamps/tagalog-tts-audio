#!/usr/bin/env python3
"""Compare what the phone-recognition models heard with the IPA of the word list.

    python3 scripts/score_phones.py LIST.tsv OUTDIR CHECKSDIR

Reads OUTDIR/*.tsv (from scripts/phones.py), writes CHECKSDIR/compare.tsv (one row per clip, one column per
model) and CHECKSDIR/report.md.  Both sides are reduced to a broad Tagalog phone set before comparing:
stress, length and diacritics dropped, ɾ/ɹ/r -> r, ɡ -> g, lax and central vowels -> the five Tagalog vowels.
"""
import collections
import csv
import glob
import os
import re
import sys
import unicodedata

VMAP = {"ɪ": "i", "ʊ": "u", "ɛ": "e", "ɔ": "o", "ɐ": "a", "ə": "a", "ʌ": "a", "ɑ": "a", "æ": "a", "ɒ": "o", "ɨ": "i",
        "ɯ": "u", "ø": "e", "œ": "e", "ɤ": "o", "ɵ": "o", "ɜ": "e", "ɝ": "er", "ɚ": "er", "y": "i"}
CMAP = {"ɾ": "r", "ɹ": "r", "ʁ": "r", "ɻ": "r", "ɡ": "g", "ɣ": "g", "ɫ": "l", "ɬ": "l", "β": "b", "ð": "d", "ɸ": "f",
        "ç": "h", "x": "h", "ʃ": "ʃ", "ɕ": "ʃ", "ʒ": "ʒ", "ʑ": "ʒ", "ɲ": "nj", "ŋ": "ŋ", "ʎ": "lj", "ɟ": "dʒ", "c": "k",
        "q": "k", "ʂ": "ʃ", "d̪": "d"}
DROP = set("ˈˌːˑ./[] ʰʲʷˀ̃-▁˞0123456789")      # ▁ = ZIPA word boundary; digits = tones in the espeak set
VOWELS = set("aeiou")
DIPHTHONGS = [("aɪ", "aj"), ("ɑɪ", "aj"), ("äɪ", "aj"), ("eɪ", "ej"), ("ɛɪ", "ej"), ("ɔɪ", "oj"), ("oɪ", "oj"),
              ("aʊ", "aw"), ("ɑʊ", "aw"), ("oʊ", "o"), ("əʊ", "o"), ("ow", "o")]


def phones(s):
    s = unicodedata.normalize("NFD", s or "")
    s = re.sub(r"[ɜə]\s*˞", "ɝ", s)                    # ZIPA writes an r-coloured vowel as two symbols (ɜ ˞): = ɝ, ɚ
    s = re.sub(r"\s*˞", "r", s)                         # any other vowel + ˞ (o ˞): the vowel and r
    s = "".join(c for c in s if unicodedata.category(c) != "Mn" and c not in DROP)
    for a, b in DIPHTHONGS:                             # aɪ = aj, ɔɪ = oj, aʊ = aw, oʊ = o: one sound, two notations
        s = s.replace(a, b)
    s = s.replace("ts", "ts").replace("tʃ", "C").replace("dʒ", "J").replace("tɕ", "C").replace("dʑ", "J")
    out = []
    for c in s:
        c = VMAP.get(c, CMAP.get(c, c))
        out.extend(["tʃ"] if c == "C" else ["dʒ"] if c == "J" else list(c) if c in ("nj", "lj", "er") else [c])
    return out


def dist(a, b):
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def main():
    lst, outdir, checks = sys.argv[1:4]
    rows = list(csv.DictReader(open(lst, encoding="utf-8"), delimiter="\t"))
    for r in rows:                                 # lists without a category (wordlist_all.tsv): hyphen or IPA source
        if not r.get("category"):
            r["category"] = "hyphenated" if "-" in r["form"] else (r.get("ipa_source") or "")
    hyp = collections.defaultdict(dict)                           # model -> form -> phones
    secs = collections.defaultdict(list)
    for p in glob.glob(os.path.join(outdir, "*.tsv")):
        for line in open(p, encoding="utf-8"):
            f = line.rstrip("\n").split("\t")
            if len(f) >= 3:
                hyp[f[1]][f[0]] = f[2]
                if len(f) > 3:
                    secs[f[1]].append(float(f[3]))
    models = sorted(hyp)
    os.makedirs(checks, exist_ok=True)
    with open(os.path.join(checks, "compare.tsv"), "w", encoding="utf-8") as fh:
        fh.write("\t".join(["form", "category", "ipa"] + models) + "\n")
        for r in rows:
            fh.write("\t".join([r["form"], r.get("category", ""), r["ipa"]] + [hyp[m].get(r["form"], "") for m in models]) + "\n")
    rep = ["# Phone recognition check", "",
           f"{len(rows)} clips. Error rate = phone edit distance / reference length, after reducing both sides to a broad "
           "Tagalog phone set (stress, length and diacritics dropped; ɾ/ɹ → r; lax vowels → a e i o u). The reference is "
           "the IPA column of the word list, so a high rate can mean the model, the audio or the IPA is wrong.", ""]
    rep += ["| Model | Clips | Error rate | Error rate without ʔ | Exact (without ʔ) | Final ʔ found | Final ʔ invented | Much longer than the word | s per clip |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    cats = sorted({r.get("category", "") for r in rows})
    percat, worst = {}, {}
    perclip, extra, short = collections.defaultdict(dict), collections.defaultdict(list), collections.defaultdict(list)
    for m in models:
        E = N = E0 = N0 = exact = n = tp = fn = fp = tn = runaway = 0
        pc = collections.defaultdict(lambda: [0, 0])
        bad = []
        for r in rows:
            h = hyp[m].get(r["form"])
            if h is None or h.startswith("ERROR"):
                continue
            ref, hp = phones(r["ipa"]), phones(h)
            d = min(dist(ref, hp), len(ref))          # a clip counts at most 100 % wrong
            E += d; N += len(ref); n += 1
            r0, h0 = [x for x in ref if x != "ʔ"], [x for x in hp if x != "ʔ"]
            d0 = min(dist(r0, h0), len(r0)); E0 += d0; N0 += len(r0); exact += d0 == 0
            pc[r.get("category", "")][0] += d0; pc[r.get("category", "")][1] += len(r0)
            perclip[r["form"]][m] = d0 / max(1, len(r0))
            if len(h0) > 2 * len(r0) + 4:             # the model heard much more than the word
                runaway += 1; extra[r["form"]].append(m)
            if len(r0) >= 6 and len(h0) < 0.6 * len(r0):   # much less: the clip stops early (often at a hyphen)
                short[r["form"]].append(m)
            rf, hf = ref[-1:] == ["ʔ"], hp[-1:] == ["ʔ"]
            tp += rf and hf; fn += rf and not hf; fp += hf and not rf; tn += not rf and not hf
            bad.append((d0 / max(1, len(r0)), r["form"], r.get("category", ""), r["ipa"], h))
        if not n:
            rep.append(f"| {m} | 0 | – | – | – | – | – | – | – |")
            continue
        s = sum(secs[m]) / len(secs[m]) if secs[m] else 0
        rep.append(f"| {m} | {n} | {E / N:.1%} | {E0 / N0:.1%} | {exact / n:.0%} | {tp}/{tp + fn} | {fp}/{fp + tn} | {runaway} | {s:.2f} |")
        percat[m] = pc
        worst[m] = sorted(bad, reverse=True)[:15]
    rep += ["", "## Error rate without ʔ, by category", "", "| Category | " + " | ".join(models) + " |",
            "|---|" + "---:|" * len(models)]
    for c in cats:
        rep.append(f"| {c} | " + " | ".join(f"{percat[m][c][0] / percat[m][c][1]:.1%}" if m in percat and percat[m][c][1] else "–"
                                         for m in models) + " |")
    ok = [m for m in percat]
    need = min(2, len(ok))
    bad_audio = [f for f, ms in extra.items() if len(ms) >= need]
    with open(os.path.join(checks, "extra_speech.tsv"), "w", encoding="utf-8") as fh:
        fh.write("form\tmodels\n" + "".join(f"{f}\t{','.join(extra[f])}\n" for f in bad_audio))
    rep += ["", f"## Clips where {need} or more models hear much more than the word ({len(bad_audio)}, all in extra_speech.tsv)", "",
            "Usually the TTS read extra text (for example the instruction) into the clip: listen and re-synthesize.", ""]
    rep += [f"- {f}: " + ", ".join(f"{m} `{hyp[m][f][:120]}`" for m in extra[f]) for f in bad_audio[:100]] or ["(none)"]
    kind = {r["form"]: "hyphenated" if "-" in r["form"].strip("-") else "plain" for r in rows}
    ipa_of = {r["form"]: r["ipa"] for r in rows}
    cut = [f for f, ms in short.items() if len(ms) >= need]
    with open(os.path.join(checks, "truncated.tsv"), "w", encoding="utf-8") as fh:
        fh.write("kind\tform\tipa\t" + "\t".join(ok) + "\n")
        fh.write("".join(f"{kind[f]}\t{f}\t{ipa_of[f]}\t" + "\t".join(hyp[m].get(f, "") for m in ok) + "\n" for f in cut))
    heard = collections.Counter(kind[f] for f, v in perclip.items() if len(v) >= need)
    cuts = collections.Counter(kind[f] for f in cut)
    rep += ["", f"## Clips heard much shorter than the word (under 60 % of its phones, words of 6+ phones): {len(cut)}, "
            "all in truncated.tsv", "", "| Kind | Cut short | Clips | Share |", "|---|---:|---:|---:|"]
    rep += [f"| {k} | {cuts[k]} | {heard[k]} | {cuts[k] / heard[k]:.1%} |" for k in ("hyphenated", "plain") if heard[k]]
    allbad = [(sum(v.values()) / len(v), f) for f, v in perclip.items() if len(v) == len(ok) and min(v.values()) >= 0.4]
    ipa = {r["form"]: (r.get("category", ""), r["ipa"]) for r in rows}
    allbad.sort(reverse=True)
    with open(os.path.join(checks, "disagree.tsv"), "w", encoding="utf-8") as fh:
        fh.write("form\tcategory\tipa\tmean_error\t" + "\t".join(ok) + "\n")
        fh.write("".join(f"{f}\t{ipa[f][0]}\t{ipa[f][1]}\t{e:.2f}\t" + "\t".join(hyp[m].get(f, "") for m in ok) + "\n" for e, f in allbad))
    rep += ["", f"## Clips every model disagrees with (40 % or more of the phones, without ʔ): {len(allbad)}, all in disagree.tsv", "",
            "The word list IPA, the audio, or both are likely wrong here.", "",
            "| Form | Category | IPA | " + " | ".join(ok) + " |", "|---|---|---|" + "---|" * len(ok)]
    rep += [f"| {f} | {ipa[f][0]} | {ipa[f][1]} | " + " | ".join(hyp[m].get(f, "")[:60] for m in ok) + " |" for _, f in allbad[:200]]
    for m in worst:
        rep += ["", f"## {m}: the 15 clips it disagrees with most", "", "| Form | Category | IPA | Heard |", "|---|---|---|---|"]
        rep += [f"| {f} | {c} | {i} | {h} |" for _, f, c, i, h in worst[m]]
    open(os.path.join(checks, "report.md"), "w", encoding="utf-8").write("\n".join(rep) + "\n")
    print("\n".join(rep[:20]))


if __name__ == "__main__":
    main()
