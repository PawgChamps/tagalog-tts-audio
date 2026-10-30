# Tagalog word audio

One MP3 per reading of every single-word headword of a Tagalog → Portuguese dictionary, each with an IPA reading.
The clips were made with Google Cloud Text-to-Speech, model **Gemini 3.1 Flash TTS**, voice **Laomedeia**.

**[Listen and search online](https://pawgchamps.github.io/tagalog-tts-audio/)**

<!-- counts -->
147,533 clips for 147,533 forms of 141,604 spellings.

| Stress from (`stress_source`) | Forms |
|---|---:|
| KWF (Diksiyonaryo ng Wikang Filipino and its Filipino-English dictionary) (`kwf`) | 44,171 |
| UP Diksiyonaryong Filipino (diksiyonaryo.ph, else the 2001 print) (`up`) | 40,921 |
| Wiktionary's IPA (`wiktionary`) | 11,981 |
| other dictionaries (Vicassan, Leo English, Leo James, Tuttle, Ramos...) (`book`) | 25,853 |
| older word lists (Calderón 1915, Nigg 1904, Freelang) (`legacy`) | 2,596 |
| the dictionary's stress class (malumay, malumi, mabilis, maragsa) (`class`) | 99 |
| English loanword, read the English way (`english`) | 353 |
| a word the dictionary respells (names, foreign words), left as spelt (`respelled`) | 9 |
| no source marks the stress: the voice's own reading (`none`) | 21,550 |

| IPA from (`ipa_source`) | Forms |
|---|---:|
| the dictionary's own reading, cleaned (`dictionary`) | 28,058 |
| generated from the accented form (`rule`) | 107,620 |
| English reading from CMUdict, for English loanwords (`english`) | 11,630 |
| abbreviation read letter by letter (`spelled`) | 210 |
| corrected by hand after listening to the clip (`ipa_fixes.tsv`) (`checked`) | 15 |
<!-- /counts -->

## Files

| Path | Contents |
|---|---|
| `audio/<first letter>/<form>.mp3` | the clips, named after the accented form: `audio/b/bakâ.mp3` (`audio/_/` for forms that start with another character) |
| `wordlist_all.tsv` | every form: `form`, `plain` (the spelling without marks), `stress_source`, `ipa`, `rank` (frequency rank of the spelling, empty if unranked), `sense` (a Portuguese gloss of the spelling), `ipa_source` |
| `index.json` | form → `file`, `plain`, `ipa`, `rank` for every form that has a clip; the dictionary and the search page read it |
| `respell.tsv` | text sent to the voice instead of the form (`lrt` → `el ar ti`) |
| `origin.tsv` | where the dictionary says each spelling comes from (English, Spanish, a Tagalog root…), for the English readings |
| `docs/index.html` | the search page, published with GitHub Pages |
| `checks/` | the phone check of the clips (`checks/phones/`), the re-synthesis of the clips it found wrong (`checks/fix/`) and the accent-mark changes of the rebuild (`checks/forms_fix/`) |
| `scripts/` | everything that makes the above |

## How a form gets its accent marks

Tagalog spelling leaves stress unwritten, so each form is sent to the voice with the marks of the *Ortograpiyang
Pambansa*:

- no mark: stress on the next-to-last syllable (`baka` cow)
- acute: stress where the mark is (`bakít`)
- final grave: next-to-last stress and a final glottal stop (`punò` tree)
- final circumflex: last-syllable stress and a final glottal stop (`bakâ` maybe, `punô` full)

A spelling with several readings gets one form, and one clip, per reading.

`scripts/make_wordlist.py` takes the marks from these sources, in this order (`stress_source`):

1. **KWF**: the Komisyon sa Wikang Filipino's *Diksiyonaryo ng Wikang Filipino* (app and website) and its
   *Diksiyonaryong Filipino-English*, with the derived forms they print.
2. **UP**: the *UP Diksiyonaryong Filipino*, from diksiyonaryo.ph, or from the 2001 print for words the site lacks.
3. **Wiktionary**: the stress of its IPA.
4. **Books**: the project's other dictionaries (Vicassan, Leo English, Leo James, Tuttle, Ramos…), then old word lists
   (Calderón 1915, Nigg 1904, Freelang: `legacy`), and last the dictionary's stress class (`class`).

When sources mark the same word differently, the higher one wins. A homograph that only a lower source lists keeps that
source's reading: UP's `dagá` and `dagà` stand beside the KWF's `daga` and `dagâ`, and Wiktionary's `lalakí` (future of
*lumaki*) beside `lalaki` "man". Two entries are taken as the same word when their definitions share content words;
without definitions, the part of speech decides.

- Names take the stress of the respelling the dictionary prints: `Cebu (se•bú)` → `Cebú`, `Jose (ho•sé)` → `José`.
- English loanwords stay as spelt, so that the voice reads them the English way.
- A form that no source marks keeps its bare spelling (`none`), and the voice reads it its own way.
- Known limit: two paraphrased definitions of one word can give two readings (`parábula` from the KWF, `parabula` from UP).

The rules in detail are in the docstring of `scripts/make_wordlist.py`.

## IPA

Every form has an IPA reading in the style `/kuˈmaʔin/`, `/ˈbahaj/`, `/ŋaˈjon/`: ˈ before the stressed syllable, no
length marks or syllable dots, `j` for the glide. `ipa_source` says where it comes from:

- `dictionary`: the dictionary's own reading (Wiktionary's, or another source's), cleaned.
- `rule`: made from the accented form by `scripts/make_ipa.py`. It reads the marks as above, takes the longest possible
  onsets, treats `ng`, `ts`, `ch` and `sh` as single consonants and `ny`, `sy` as n+j, s+j, and puts a glottal stop
  before a vowel that starts the word, follows a vowel of another syllable or follows a hyphen.
- `english`: CMUdict, for English loanwords. A word counts as one when the dictionary derives it from an English word
  spelled the same way, and not also from Spanish or a Tagalog root (`origin.tsv`, written by `scripts/make_origin.py`).
  With no origin given, a single word of the English word list counts when it looks English: a letter or digraph
  Tagalog does not use, six letters or more, or a doubled consonant. Names and accented forms never count. A
  hyphenated form counts only when every part is English: a Tagalog prefix, a reduplication or a Tagalog suffix keeps
  the Tagalog reading (*mag-isa*, *sama-sama*, *bay-an*), and a Tagalog prefix on an English word reads each part its own
  way (*i-share* /ʔiˈʃɛɹ/).
- `spelled`: abbreviations with no vowel, read by letter names with the last one stressed (`tv`, `dr`); `ng` is /ˈnaŋ/.

`scripts/fix_ipa.py` brings every reading to that style. It drops syllable dots, length marks and tie bars, puts the
stress mark at the start of its syllable, adds the glottal stop between two vowels, writes the tap as ɾ and *ly* as
`lj`, and ends a final grave or circumflex in ʔ. A reading whose stress or vowels contradict the accent marks is
replaced by the rule reading, and the English loanwords get their CMUdict reading. Running it again changes nothing.

The IPA is metadata: the audio is synthesized from the accented form, never from the IPA. Forms with no stress
information get next-to-last stress in the IPA, while the voice reads the bare word its own way. English words that the
dictionary does not derive from English (it calls *chef* French), English compounds CMUdict lacks (*worktext*) and
Spanish words are read by the Tagalog rules.

## Phone check

A phone-recognition model listens to each clip and writes the phones it hears, and `scripts/score_phones.py` compares
them with the IPA (`checks/phones/README.md`).

| | Old list, 151,262 clips (29/10) | Rebuilt list, 147,533 clips (30/10) |
|---|---:|---:|
| phones wrong, without the glottal stop | 9.6 % | 8.5 % |
| `dictionary` / `rule` readings | 7.6 % / 9.6 % | 8.6 % / 8.0 % |
| hyphenated forms | 10.7 % | 7.2 % |
| `english` readings | 24.7 % | 16.0 % |
| `spelled` abbreviations | 50.3 % | 20.3 % |

The first check found 1,013 hyphenated clips cut at the hyphen, 2,992 English loanwords spoken the Tagalog way (some
translated: *blood* → "dugo") and 5 clips with extra speech. `scripts/fix_clips.py` re-synthesized the clips the check
found wrong, up to three tries each, and replaced a clip only when ZIPA confirmed the new one: 3,414 of 3,526 on the old
list, then 439 of 471 on the rebuilt one, mostly words the rebuilt list reads the English way (`checks/fix/`). The
30,083 new clips of the rebuild were asked the way those runs proved (the hyphen as a space with prompt `parts`,
English words with prompt `english`, `respell.tsv`): none of the 197 hyphenated clips of its pilot was cut short.

## Workflows

| Workflow | What it does |
|---|---|
| *Synthesize audio* (`synthesize.yml`) | with `fix=<fix list>` (`checks/fix/redo_rebuild.tsv`), re-synthesizes and checks the clips of a fix list (`scripts/fix_clips.py`); otherwise runs a list through the voice in batches of 2,000, commits each batch to the branch it runs on, and starts a new run of itself at the 5-hour limit; `list=next` and `list=next-pilot` run the lists of the rebuild |
| *Phone recognition* (`phones.yml`) | the phone check of a list, one job per model and shard; commits `checks/phones/<list>/` |
| *Fix IPA* (`fix_ipa.yml`) | `scripts/fix_ipa.py` with CMUdict on `wordlist_all.tsv`, then `index.json` |
| *Prepare the rebuild* (`prepare.yml`) | IPA for `next/wordlist.tsv` and the plan of the switch (`scripts/plan_next.py`) |
| *Switch to the rebuilt list* (`switch.yml`) | `scripts/apply_next.py`: renames, retires and replaces clips, then installs the new list |
| *Request* (`request.yml`) | starts the workflows listed in `next/request.txt` when a push changes it, for agents that can push but cannot start workflows (`scripts/request.py`) |

The workflows reach Google through workload identity federation (repository secrets `GCP_WIF_PROVIDER`,
`GCP_SERVICE_ACCOUNT`, `GCP_PROJECT_NUMBER`), so no key is stored in the repository. Google bills the voice per token,
about 25 audio tokens per second of speech.

## Making the list again

The word list comes from the dictionary project: its published JSON, its KWF and UP source files, and two of its
modules (`tagalog_orthography`, `tagalog_phonetics_baybayin`).

```bash
export TGL_ROOT=/path/to/Tagalog                       # the dictionary project
export PYTHONPATH="$TGL_ROOT/Project TGL to PRT-BR/Scripts"
DICT="$TGL_ROOT/Project TGL to PRT-BR/tagalog_ptbr_dictionary.json"
python3 scripts/make_wordlist.py "$DICT" --top 0 --out next/wordlist.tsv
python3 scripts/make_origin.py "$DICT" --list wordlist_all.tsv next/wordlist.tsv --out origin.tsv
python3 checks/forms_fix/compare_forms.py wordlist_all.tsv index.json next/wordlist.tsv checks/forms_fix/changes.tsv
```

Then the *Prepare*, *Synthesize* and *Switch* workflows do the rest (`next/RUNBOOK.md`). Outside Actions,
`scripts/tts_gemini.py <key> <list.tsv> audio` synthesizes a list. It is resumable, because existing files are
skipped, and `<key>` is a key file, `-` for `$GOOGLE_ACCESS_TOKEN`, or `adc`. `scripts/build_index.py` then rebuilds
`index.json`. `run_batches.sh` does both in batches and pushes each one.
