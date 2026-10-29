#!/usr/bin/env python3
"""Compare what the phone-recognition models heard with the IPA of the word list.

    python3 scripts/score_phones.py LIST.tsv OUTDIR CHECKSDIR

Reads OUTDIR/*.tsv (from scripts/phones.py), writes CHECKSDIR/phones_compare.tsv (one row per clip, one column per
model) and CHECKSDIR/phones_report.md.  Both sides are reduced to a broad Tagalog phone set before comparing:
stress, length and diacritics dropped, ɾ/ɹ/r -> r, ɡ -> g, lax and central vowels -> the five Tagalog vowels.
"""
import collections
import csv
import glob
import os
import sys
import unicodedata

VMAP = {"ɪ": "i", "ʊ": "u", "ɛ": "e", "ɔ": "o", "ɐ": "a", "ə": "a", "ʌ": "a", "ɑ": "a", "æ": "a", "ɒ": "o", "ɨ": "i",
        "ɯ": "u", "ø": "e", "œ": "e", "ɤ": "o", "ɵ": "o", "ɜ": "e", "ɝ": "er", "ɚ": "er", "y": "i"}
CMAP = {"ɾ": "r", "ɹ": "r", "ʁ": "r", "ɻ": "r", "ɡ": "g", "ɣ": "g", "ɫ": "l", "ɬ": "l", "β": "b", "ð": "d", "ɸ": "f",
        "ç": "h", "x": "h", "ʃ": "ʃ", "ɕ": "ʃ", "ʒ": "ʒ", "ʑ": "ʒ", "ɲ": "nj", "ŋ": "ŋ", "ʎ": "lj", "ɟ": "dʒ", "c": "k"}
DROP = set("ˈˌːˑ./[] ʰʲʷˀ̃-")
VOWELS = set("aeiou")


def phones(s):
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn" and c not in DROP)
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
    with open(os.path.join(checks, "phones_compare.tsv"), "w", encoding="utf-8") as fh:
        fh.write("\t".join(["form", "category", "ipa"] + models) + "\n")
        for r in rows:
            fh.write("\t".join([r["form"], r.get("category", ""), r["ipa"]] + [hyp[m].get(r["form"], "") for m in models]) + "\n")
    rep = ["# Phone recognition check", "",
           f"{len(rows)} clips. Error rate = phone edit distance / reference length, after reducing both sides to a broad "
           "Tagalog phone set (stress, length and diacritics dropped; ɾ/ɹ → r; lax vowels → a e i o u). The reference is "
           "the IPA column of the word list, so a high rate can mean the model, the audio or the IPA is wrong.", ""]
    rep += ["| Model | Clips | Error rate | Error rate without ʔ | Exact (without ʔ) | Final ʔ found | Final ʔ invented | s per clip |",
            "|---|---:|---:|---:|---:|---:|---:|---:|"]
    cats = sorted({r.get("category", "") for r in rows})
    percat, worst = {}, {}
    for m in models:
        E = N = E0 = N0 = exact = n = tp = fn = fp = tn = 0
        pc = collections.defaultdict(lambda: [0, 0])
        bad = []
        for r in rows:
            h = hyp[m].get(r["form"])
            if h is None or h.startswith("ERROR"):
                continue
            ref, hp = phones(r["ipa"]), phones(h)
            d = dist(ref, hp)
            E += d; N += len(ref); n += 1
            r0, h0 = [x for x in ref if x != "ʔ"], [x for x in hp if x != "ʔ"]
            d0 = dist(r0, h0); E0 += d0; N0 += len(r0); exact += d0 == 0
            pc[r.get("category", "")][0] += d0; pc[r.get("category", "")][1] += len(r0)
            rf, hf = ref[-1:] == ["ʔ"], hp[-1:] == ["ʔ"]
            tp += rf and hf; fn += rf and not hf; fp += hf and not rf; tn += not rf and not hf
            bad.append((d0 / max(1, len(r0)), r["form"], r.get("category", ""), r["ipa"], h))
        if not n:
            rep.append(f"| {m} | 0 | – | – | – | – | – | – |")
            continue
        s = sum(secs[m]) / len(secs[m]) if secs[m] else 0
        rep.append(f"| {m} | {n} | {E / N:.1%} | {E0 / N0:.1%} | {exact / n:.0%} | {tp}/{tp + fn} | {fp}/{fp + tn} | {s:.2f} |")
        percat[m] = pc
        worst[m] = sorted(bad, reverse=True)[:15]
    rep += ["", "## Error rate without ʔ, by category", "", "| Category | " + " | ".join(models) + " |",
            "|---|" + "---:|" * len(models)]
    for c in cats:
        rep.append(f"| {c} | " + " | ".join(f"{percat[m][c][0] / percat[m][c][1]:.1%}" if m in percat and percat[m][c][1] else "–"
                                         for m in models) + " |")
    for m in worst:
        rep += ["", f"## {m}: the 15 clips it disagrees with most", "", "| Form | Category | IPA | Heard |", "|---|---|---|---|"]
        rep += [f"| {f} | {c} | {i} | {h} |" for _, f, c, i, h in worst[m]]
    open(os.path.join(checks, "phones_report.md"), "w", encoding="utf-8").write("\n".join(rep) + "\n")
    print("\n".join(rep[:20]))


if __name__ == "__main__":
    main()
