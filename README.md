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

## How the IPA was determined

Every row of `wordlist_all.tsv` has an IPA reading in the `ipa` column, and `ipa_source` says where it came from:

| Where the IPA comes from | Forms |
|---|---:|
| The dictionary's own reading (`ipa_source` = `dictionary`) | 92,472 |
| Generated from the accented spelling by rule (`rule`) | 58,554 |
| Consonant-only abbreviations read letter by letter, such as tv, dr, gym (`spelled`) | 236 |

- **Dictionary readings** are the IPA of the Tagalog to Portuguese dictionary, collected from Wiktionary and the other sources of the project. When a word has one, it is used as it stands.
- **Rule-generated readings** come from `scripts/make_ipa.py`, which reads the accent marks of the *Ortograpiyang Pambansa* in the `form` column: an acute mark stresses that syllable, a final grave mark means penultimate stress plus a final glottal stop, a circumflex means final stress plus a final glottal stop, and no mark means penultimate stress. Syllables follow the usual Tagalog rules (maximal onsets, `ng` and `ts` as single consonants, `ny` and `sy` read as n+j and s+j, a hyphen starts a new syllable); a vowel that starts a word, follows another vowel in a different syllable or follows a hyphen gets a glottal stop.
- **Spelled abbreviations** have no vowel to read, so they are spelled out by letter names with the last letter stressed. The particle `ng` is read /ˈnaŋ/.
- The style matches the dictionary's readings: `/kuˈmaʔin/`, `/ˈbahaj/`, `/ŋaˈjon/`, with ˈ before the stressed syllable, no length marks and no syllable dots.

**Check against the dictionary.** On 83,000 words spelled with native letters that have both a dictionary reading and a generated one, the stressed vowel agrees on 93% and the sounds agree on 95%. Most of the remaining differences are conventions of the older dictionary readings (syllable dots, `r`, `y` and `g` for English words), not errors of the rule.

**Limits.** The IPA is metadata: the audio was synthesized from the accented spelling, never from the IPA, so the two cannot disagree for words that carry an accent mark. For the 25,984 forms that have no stress information (`stress_source` = `none`) the IPA assumes penultimate stress, the Tagalog default, and the audio is whatever the voice chose for the bare word.
