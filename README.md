# Tagalog word audio

One MP3 per reading of single-word headwords for a Tagalog dictionary:
151,262 clips, synthesized with Google Cloud Text-to-Speech, model **Gemini 3.1 Flash TTS**, voice **Laomedeia**.

**[Listen and search online](https://pawgchamps.github.io/tagalog-tts-audio/)**

Tagalog does not write stress, so each word is sent with the accent marks of the *Ortograpiyang Pambansa*
(`báka` cow, `bakâ` maybe; `punò` tree, `punô` full), derived from the word's IPA, from the printed headword or
from the stress class. Heteronyms get one clip per reading. `wordlist_all.tsv` lists every form with its IPA and
frequency rank; `index.json` maps each form to its file.

Layout: `audio/<first letter>/<accented form>.mp3`, e.g. `audio/b/báka.mp3`. The search page is `docs/index.html`, published with GitHub Pages.

## Regenerate
`scripts/make_wordlist.py` builds the list from the dictionary JSON; `scripts/tts_gemini.py` synthesizes
(resumable, skips existing files); `run_batches.sh` runs the list in batches and pushes each one.
Cost: billed per token by Google (about 25 audio tokens per second of speech).
