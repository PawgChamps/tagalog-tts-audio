# Plan for the switch to the rebuilt word list

Made by `scripts/plan_next.py` from `next/wordlist_ipa.tsv`.

| | Forms or clips |
|---|---:|
| current list: forms / clips | 151,262 / 181,627 |
| rebuilt list: forms | 147,533 |
| clips kept as they are | 146,128 |
| clips renamed (the same reading spelled differently) | 1,390 |
| re-synthesized over a kept or renamed clip (`redo.tsv` / `redo_english.tsv`) | 0 / 0 |
| new readings to synthesize (`synthesize.tsv` / `synthesize_english.tsv`) | 15 / 0 |
| clips retired (the reading leaves the list) | 34,109 |
| pilot (`pilot.tsv`: hyphenated / `pilot_english.tsv`) | 15 (4) / 0 |

Why clips are re-synthesized: none (the clips the phone check found wrong are left to scripts/fix_clips.py, checks/fix/).

Hyphenated forms are sent with the hyphen read as a space and told the word is written in parts (prompt `parts`); abbreviations as letter names (`letters`): 4 new lines in `next/respell.tsv` (15 in all;
by prompt: parts 4).
