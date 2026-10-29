#!/usr/bin/env python3
"""Rewrite the counts in README.md (between <!-- counts --> and <!-- /counts -->) from wordlist_all.tsv and index.json.
Usage: python3 scripts/readme_counts.py   (from the repository root; scripts/apply_next.py runs it at the switch)"""
import collections
import json
import re

rows = [ln.split("\t") for ln in open("wordlist_all.tsv", encoding="utf-8").read().split("\n")[1:] if ln]
clips = len(json.load(open("index.json", encoding="utf-8")))
ipa = collections.Counter(r[6] for r in rows)
stress = collections.Counter(r[2] for r in rows)
IPA = [("dictionary", "the dictionary's own reading, cleaned"), ("rule", "generated from the accented form"),
       ("english", "English reading from CMUdict, for English loanwords"), ("spelled", "abbreviation read letter by letter")]
STRESS = [("kwf", "KWF (Diksiyonaryo ng Wikang Filipino and its Filipino-English dictionary)"),
          ("up", "UP Diksiyonaryong Filipino (diksiyonaryo.ph, else the 2001 print)"),
          ("wiktionary", "Wiktionary's IPA"), ("canon", "the accented headword of the dictionary"),
          ("book", "other dictionaries (Vicassan, Leo English, Leo James, Tuttle, Ramos...)"),
          ("legacy", "older word lists (Calderón 1915, Nigg 1904, Freelang)"),
          ("class", "the dictionary's stress class (malumay, malumi, mabilis, maragsa)"),
          ("english", "English loanword, read the English way"),
          ("respelled", "a word the dictionary respells (names, foreign words), left as spelt"),
          ("ipa", "the dictionary's IPA (earlier list)"), ("headword", "the accented headword (earlier list)"),
          ("none", "no source marks the stress: the voice's own reading")]
lines = [f"{clips:,} clips for {len(rows):,} forms of {len({r[1] for r in rows}):,} spellings.", "",
         "| Stress from (`stress_source`) | Forms |", "|---|---:|"]
lines += [f"| {d} (`{k}`) | {stress[k]:,} |" for k, d in STRESS if stress[k]]
lines += [f"| other (`{k}`) | {v:,} |" for k, v in sorted(stress.items()) if k not in dict(STRESS)]
lines += ["", "| IPA from (`ipa_source`) | Forms |", "|---|---:|"]
lines += [f"| {d} (`{k}`) | {ipa[k]:,} |" for k, d in IPA if ipa[k]]
block = "<!-- counts -->\n" + "\n".join(lines) + "\n<!-- /counts -->"
text = open("README.md", encoding="utf-8").read()
new, n = re.subn(r"<!-- counts -->.*?<!-- /counts -->", lambda m: block, text, flags=re.S)
if not n:
    raise SystemExit("README.md has no <!-- counts --> block")
open("README.md", "w", encoding="utf-8").write(new)
print(f"README.md counts: {clips:,} clips, {len(rows):,} forms")
