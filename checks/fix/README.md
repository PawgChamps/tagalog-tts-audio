# Clip fixes: re-synthesize the clips the phone check found wrong

`redo.tsv` lists the clips to redo, built by `scripts/make_fix_list.py` from the ZIPA check of all 151,262 clips
(`checks/phones/wordlist_all/`), with the IPA of `wordlist_all.tsv` as the reference:

| Reason | Clips | What went wrong | How it is asked again |
|---|---:|---|---|
| `english` | 2,270 | English word said the Tagalog or Spanish way (*solution* → "soluson"), or translated (*blood* → "dugo", *eighth* → "ikawalo") | told it is an English word, not to translate; then with the English (US) voice setting |
| `hyphen` | 1,049 | the TTS stopped at the hyphen (*bûtu-butu* → "bûtu") | hyphen as a space; as written; without the hyphen |
| `cut` | 107 | other clips heard at under 60 % of their phones (*buwanbuwan* → "buwan") | as written; two equal halves as two words |
| `letters` | 98 | abbreviation not read as its letters (*sgt* → "si") | the letter names (*es dyi ti*); the capital letters |
| `extra` | 2 | extra speech: *input* reads the instruction aloud, *tumoy* | as written; in quotation marks; as an English word |

Left alone on purpose: abbreviations people say as words (*dr* "doktor", *jr*, *gng*); English-tagged words ending
in -a or -o, words common in Filipino text (*noon* "back then", *cellphone*) and a few Spanish or Tagalog words
(*corregidor*, *luz*), where the Tagalog reading can be the right one.

`scripts/fix_clips.py` sends up to three tries per clip and lets ZIPA listen to each. A try replaces the clip only
when it is complete (at least 75 % of the phones, not much longer than the word) and clearly better than the old
clip (error at most 40 % and at least 10 points lower). Otherwise the old clip stays. Every try is in `results.tsv`,
the totals in `report.md`.

## Result (29/10/2026)

**3,414 of the 3,526 clips replaced**, 112 kept, in 4,252 tries (a trial of 48 clips, the full list, then
`repeat.tsv`):

| Reason | Replaced | Kept | Notes |
|---|---:|---:|---|
| `english` | 2,183 | 87 | 2,094 on the first try; the kept ones are mostly fine already (*director*, *jump*, error 0.25) |
| `hyphen` | 1,019 | 11 | 954 on the first try (hyphen as a space) |
| `letters` | 98 | 0 | 27 needed the capital letters (*mg*: "em dyi" was read as more letters) |
| `cut` | 79 | 14 | the kept ones are not cut words but odd spellings (*reseaux*, *sleíght*, *worktext*) |
| `repeat` | 33 | 0 | reduplications said once whatever the spelling (*asa-asa*, *tánggal-tanggal*); fixed by saying the word repeats a part and every part must be said, the parts separated by a comma |
| `extra` | 2 | 0 | *input* in quotation marks |

The kept clips are listed at the end of `report.md`, each with its best try.

**For new clips**: send a hyphenated word with the hyphen as a space (*túluy tuloy*), a reduplication with a comma
between the parts and the "repeats a part" instruction, an English word with "say it the English way, do not
translate", and an abbreviation as letter names; `tries()` in `scripts/fix_clips.py` has the exact texts and
instructions.

## Run it

GitHub: Actions → **Synthesize audio** → *Run workflow*, branch of your choice, `fix` = `checks/fix/redo.tsv`
(`max_words` = 50 for a trial). It commits the replaced clips and `checks/fix/` every 200 clips and resumes where it
stopped; a run cut off by the time limit starts the next one itself.

Locally: `python3 scripts/fix_clips.py KEY checks/fix/redo.tsv` (KEY as in `tts_gemini.py`; needs `onnxruntime lhotse
huggingface_hub imageio-ffmpeg` and a clone of github.com/lingjzhu/zipa in `$ZIPA_SRC`).

Rebuild the list after a new phone check: `python3 scripts/make_fix_list.py` (needs `wordfreq`); after a fix run,
`python3 scripts/make_fix_list.py --repeat` lists the reduplications it could not fix for one more pass.
