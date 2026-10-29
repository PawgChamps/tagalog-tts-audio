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
`scripts/make_wordlist.py` builds the list from the dictionary JSON, `scripts/make_ipa.py` and `scripts/fix_ipa.py` write and clean its IPA; `scripts/tts_gemini.py` synthesizes
(resumable, skips existing files); `run_batches.sh` runs the list in batches and pushes each one.
Cost: billed per token by Google (about 25 audio tokens per second of speech).

## How the IPA was determined

Every row of `wordlist_all.tsv` has an IPA reading in the `ipa` column, and `ipa_source` says where it came from:

| Where the IPA comes from | Forms |
|---|---:|
| The dictionary's own reading, cleaned (`ipa_source` = `dictionary`) | 89,519 |
| Generated from the accented spelling by rule (`rule`) | 50,903 |
| English pronunciation from CMUdict, for English loanwords (`english`) | 10,648 |
| Consonant-only abbreviations read letter by letter, such as tv, dr (`spelled`) | 192 |

- **Dictionary readings** are the IPA of the Tagalog to Portuguese dictionary, collected from Wiktionary and the other sources of the project. They are used as they stand, after the cleaning described below.
- **Rule-generated readings** come from `scripts/make_ipa.py`, which reads the accent marks of the *Ortograpiyang Pambansa* in the `form` column: an acute mark stresses that syllable, a final grave mark means penultimate stress plus a final glottal stop, a circumflex means final stress plus a final glottal stop, and no mark means penultimate stress. Syllables follow the usual Tagalog rules (maximal onsets, `ng`, `ts`, `ch` and `sh` as single consonants, `ny` and `sy` read as n+j and s+j, a hyphen starts a new syllable); a vowel that starts a word, follows another vowel in a different syllable or follows a hyphen gets a glottal stop.
- **English readings** are taken from CMUdict for English words (no accent mark, not a name, and either a letter or digraph Tagalog does not use, six letters or more, or a doubled consonant), written in the same style: `/ˈsɪti/`, `/ˈskul/`.
- **Spelled abbreviations** have no vowel to read, so they are spelled out by letter names with the last letter stressed. The particle `ng` is read /ˈnaŋ/.
- The style is `/kuˈmaʔin/`, `/ˈbahaj/`, `/ŋaˈjon/`: ˈ before the stressed syllable, no length marks, no syllable dots, `j` for the glide.

**Cleaning.** `scripts/fix_ipa.py` brought the readings to that style and corrected what an audit of all 151,262 rows found wrong (it needs `pip install cmudict`, and running it again changes nothing):
- 63,668 dictionary readings had syllable dots, length marks or tie bars, which left the stress mark after a consonant (`/ʔib.ˈaŋ/` for *ibáng*, now `/ʔiˈbaŋ/`); the dots and marks are removed, the stress mark moved to the start of its syllable, and two vowels in a row now get their glottal stop (`/kahalaˈtaan/` is now `/kahalaˈtaʔan/`).
- 1,701 readings stressed a vowel the accent mark does not allow (`/paɡ.ˈulan/` for *pag-ulán*); they now use the rule reading.
- 759 readings had lost vowels (`/ˈdopdks/` for *dopaka*) or read consonant + `y` as consonant + `i` (`/pariˈan/` for *paryán*, now `/paɾˈjan/`); they now use the rule reading.
- 32 readings held several words or a garbled reduplication (`/ma.la.ˈkiŋ tiː.tik/` for *malakíng*), 12 carried a note such as "(Rizal)", and 252 *ly* words were written with `ʎ` (now `lj`).
- 10,648 English words, which the Tagalog rules had read letter by letter (`/ˈskhoʔol/` for *school*, `/ˈhealth/` for *health*), now have English readings. Names keep their dictionary or rule reading.
- The rule now reads `ch` as tʃ, `sh` as ʃ and a soft `c` as s.

**Limits.** The IPA is metadata: the audio was synthesized from the accented spelling, never from the IPA, so the two cannot disagree for words that carry an accent mark. For the 25,984 forms that have no stress information (`stress_source` = `none`) the IPA assumes penultimate stress, the Tagalog default, and the audio is whatever the voice chose for the bare word. English words of up to five letters, English compounds that CMUdict lacks (*worktext*) and Spanish words are still read by the Tagalog rules. About 1,000 dictionary readings have fewer or more vowels than the spelling, which is right for glides (*kaimito* /kajˈmito/) and English words (*wood* /ˈwud/) but was not checked word by word, and *þig* is a headword the dictionary spells with a stray letter.
