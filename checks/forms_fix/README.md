# Accent-mark changes of the rebuild

`next/wordlist.tsv` is the word list rebuilt by `scripts/make_wordlist.py` with accent marks taken from the sources in
the order KWF > UP > Wiktionary > books (see the README and the script's docstring). `changes.tsv` compares it with the
current list (`wordlist_all.tsv` and its clips): one row per plain spelling whose forms differ.

| Column | Contents |
|---|---|
| `plain` | the spelling without marks |
| `old_forms`, `new_forms` | its forms in the current and the rebuilt list |
| `rank` | frequency rank of the spelling (empty if unranked) |
| `category` | what changed (table below) |
| `new_stress_source` | where the rebuilt list takes its marks from |
| `forms_to_synthesize`, `clips_retired`, `clips_renamed`, `duplicate_clips_deleted` | what happens to the clips |

Two forms count as the same clip when they differ only in letter case, or in an acute that only says what the voice
reads anyway: one on the next-to-last syllable of a part with no other mark (`súkal` = `sukal`) or on a one-syllable
word (`ká` = `ka`). Such a clip is renamed, not synthesized again.

37,497 spellings change, 2,482 of them among the 20,000 most frequent. That gives 30,380 forms to synthesize, 29,382
clips retired, 1,390 clips renamed and 4,653 duplicate clips deleted.

| Category | Spellings |
|---|---:|
| stress mark added where the old form had none | 13,585 |
| stress moved to another syllable | 6,438 |
| mark removed (penult stress) | 4,888 |
| duplicate reading dropped (another letter case or a redundant acute) | 4,390 |
| a reading added | 3,215 |
| a form dropped (duplicate reading or weaker evidence) | 2,010 |
| glottal mark moved from the first vowel to the last syllable | 1,402 |
| same reading, spelled differently: the clip can be renamed | 940 |
| hyphenated word: mark taken off the first part | 580 |
| English or respelled foreign word: marks removed | 49 |

The glottal-mark row fixes a bug of the earlier list: a word whose syllables could not be read was taken as one
syllable, so its final grave or circumflex landed on the first vowel (`hîwi` for `hiwî`).

Make the table again after a new `next/wordlist.tsv`:

```bash
python3 checks/forms_fix/compare_forms.py wordlist_all.tsv index.json next/wordlist.tsv checks/forms_fix/changes.tsv
```

The plan that the switch carries out (`scripts/plan_next.py`, `next/plan.md`) uses the same rule for renaming clips.
Its counts differ slightly, because it compares the rebuilt list after the IPA step and counts clips rather than
spellings.
