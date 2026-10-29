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

## Run it

GitHub: Actions → **Synthesize audio** → *Run workflow*, branch of your choice, `fix` = `checks/fix/redo.tsv`
(`max_words` = 50 for a trial). It commits the replaced clips and `checks/fix/` every 200 clips and resumes where it
stopped; a run cut off by the time limit starts the next one itself.

Locally: `python3 scripts/fix_clips.py KEY checks/fix/redo.tsv` (KEY as in `tts_gemini.py`; needs `onnxruntime lhotse
huggingface_hub imageio-ffmpeg` and a clone of github.com/lingjzhu/zipa in `$ZIPA_SRC`).

Rebuild the list after a new phone check: `python3 scripts/make_fix_list.py` (needs `wordfreq`).
