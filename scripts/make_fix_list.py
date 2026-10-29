#!/usr/bin/env python3
"""List the clips to re-synthesize, from the phone check of all clips (checks/phones/wordlist_all/compare.tsv, ZIPA).

    python3 scripts/make_fix_list.py [CHECKSDIR] [OUT]     (defaults: checks/phones/wordlist_all checks/fix/redo.tsv)
    python3 scripts/make_fix_list.py --repeat              (after a fix run: checks/fix/repeat.tsv, see below)

Needs `pip install wordfreq`.  The reference is the IPA column of wordlist_all.tsv as it is now; phones are compared
the way scripts/score_phones.py does (broad phone set, glottal stops dropped).  One reason per clip, first match wins:

  extra      the clip holds much more speech than the word (the TTS read its instruction aloud, "input")
  hyphen     a hyphenated form heard at under 60 % of its phones: the TTS stopped at the hyphen (bûtu-butu -> bûtu)
  letters    an abbreviation read letter by letter whose clip is not the letters (sgt -> "si"); abbreviations people
             say as a word (dr, mr, jr, gng ...) are left alone
  english    an English word the clip says the Tagalog or Spanish way (solution -> "soluson"), or translates into
             Tagalog (blood -> "dugo"); words that end in -a or -o, words far more frequent in Filipino than in English
             text with no English spelling (cristo, mactan), and words common in Filipino text (noon "back then",
             cellphone) are left alone: the Tagalog reading can be right
  cut        any other clip of 6+ phones heard at under 60 % of them (buwanbuwan -> buwan)

Columns: form, reason, ipa_source, ipa, heard (ZIPA), error (share of the IPA's phones wrong, at most 1).

--repeat lists the reduplications among the hyphen and cut clips of redo.tsv (not English, not abbreviations) that the
fix run kept because no try was good enough, with reason `repeat`: the TTS says them only once (asa-asa -> "asa").
"""
import csv
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(__file__))
from score_phones import dist, phones          # noqa: E402

EXPANDS = {"dr", "dra", "mr", "mrs", "ms", "jr", "sr", "sra", "st", "sta", "sto", "lb", "lbs", "vs", "mt", "ft", "gng",
           "bb", "kgg", "atty", "engr", "hon", "rev", "pres", "gen", "col", "capt", "oz"}     # read as the word
NOT_ENGLISH = {"corregidor", "nogales", "luz", "lanete", "ee", "day-eng", "sows"}     # tagged English, read the Tagalog way
EN_SPELLING = re.compile(r"th|sh|ph|ck|wh|gh|oo|ee|ea|ou|ow|aw|ew|([^aeiou])\1")


def plain(s):
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()


def err(ref, heard):
    r0, h0 = [x for x in phones(ref) if x != "ʔ"], [x for x in phones(heard) if x != "ʔ"]
    return min(dist(r0, h0), len(r0)) / max(1, len(r0)), len(r0), len(h0)


def repeat(redo="checks/fix/redo.tsv", results="checks/fix/results.tsv", out="checks/fix/repeat.tsv"):
    final = {}
    for r in csv.DictReader(open(results, encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE):
        if r["outcome"] in ("replaced", "kept"):
            final[r["form"]] = r["outcome"]
    def repeats(form):                            # some three letters occur twice: a (partial) reduplication
        p = re.sub(r"[^a-z]", "", plain(form))
        return any(p.count(p[i:i + 3]) > 1 for i in range(len(p) - 2))
    rows = [r for r in csv.DictReader(open(redo, encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE)
            if r["reason"] in ("hyphen", "cut") and r["ipa_source"] not in ("english", "spelled") and final.get(r["form"]) == "kept"
            and repeats(r["form"])]
    cols = ["form", "reason", "ipa_source", "ipa", "heard", "error"]
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\t".join(cols) + "\n")
        fh.writelines("\t".join(dict(r, reason="repeat")[c] for c in cols) + "\n" for r in rows)
    print(f"{len(rows)} clips -> {out}")


def main():
    if "--repeat" in sys.argv:
        return repeat()
    checks = sys.argv[1] if len(sys.argv) > 1 else "checks/phones/wordlist_all"
    out = sys.argv[2] if len(sys.argv) > 2 else "checks/fix/redo.tsv"
    from wordfreq import zipf_frequency as z
    words = {r["form"]: r for r in csv.DictReader(open("wordlist_all.tsv", encoding="utf-8"), delimiter="\t",
                                                   quoting=csv.QUOTE_NONE)}
    heard = {r["form"]: r["zipa"] for r in csv.DictReader(open(os.path.join(checks, "compare.tsv"), encoding="utf-8"),
                                                           delimiter="\t", quoting=csv.QUOTE_NONE) if r.get("zipa")}
    tagalog_ipa = {}                                # English words: the Tagalog reading they had before the English pass
    p = os.path.join(checks, "english_vs_tagalog.tsv")
    if os.path.exists(p):
        tagalog_ipa = {r["form"]: r["tagalog_ipa"] for r in csv.DictReader(open(p, encoding="utf-8"), delimiter="\t",
                                                                          quoting=csv.QUOTE_NONE)}
    rows, counts = [], {}
    for form, w in words.items():
        h = heard.get(form)
        if not h or h.startswith("ERROR"):
            continue
        e, nr, nh = err(w["ipa"], h)
        src, pf = w["ipa_source"], plain(form)
        reason = None
        if pf in EXPANDS:
            continue
        if nh > 2 * nr + 4 and len(pf) >= 5:
            reason = "extra"
        elif "-" in form.strip("-") and nr >= 4 and nh < 0.6 * nr:
            reason = "hyphen"
        elif src == "spelled" and e >= 0.5 and pf.isalpha():
            reason = "letters"
        elif src == "english" and form in tagalog_ipa and not re.search(r"[ao]$", pf) and pf not in NOT_ENGLISH:
            et = err(tagalog_ipa[form], h)[0]
            fil, en = z(pf, "fil"), z(pf, "en")
            tagalog_like = (fil >= en + 1.0 and not EN_SPELLING.search(pf)) or (fil >= 4.0 and fil >= en)
            if not tagalog_like and ((et < e - 0.1 and e >= 0.25) or (e >= 0.6 and et >= 0.6)):
                reason = "english"
        if not reason and nr >= 6 and nh < 0.6 * nr:
            reason = "cut"
        if reason:
            rows.append((form, reason, src, w["ipa"], h.replace("▁", "").strip(), f"{e:.2f}"))
            counts[reason] = counts.get(reason, 0) + 1
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("form\treason\tipa_source\tipa\theard\terror\n")
        fh.writelines("\t".join(r) + "\n" for r in rows)
    print(f"{len(rows)} clips -> {out}:", ", ".join(f"{k} {v}" for k, v in sorted(counts.items(), key=lambda kv: -kv[1])))


if __name__ == "__main__":
    main()
