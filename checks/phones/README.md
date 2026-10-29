# Phone check: what the clips actually say

Phone-recognition models listen to each clip and write the phones they hear (audio → IPA). Comparing that with the
IPA column of the word list finds clips where the TTS said something else, and IPA that does not match the audio.

## Run it on GitHub

Actions → **Phone recognition (audio to IPA)** → *Run workflow*:

| Input | Meaning | Sample check | All clips |
|---|---|---|---|
| `list` | TSV with `form` and `ipa` (and `file`, or the paths come from `index.json`) | `checks/sample.tsv` | `wordlist_all.tsv` |
| `models` | `zipa`, `xeus`, `powsm`, `w2v2`, comma-separated | all four | `zipa` |
| `shards` | jobs per model; the list is split between them | `1` | `10` |
| `audio` | `fetch` downloads each clip; `checkout` checks out `audio/` | `fetch` | `checkout` |

Each model runs in its own job on a free 2-core runner (public repository: no cost). A last job scores everything
and commits `checks/phones/<list name>/`: `raw/` (what each model heard), `compare.tsv` (one row per clip, one column
per model), `report.md`, `extra_speech.tsv` (clips where the model hears much more than the word) and
`disagree.tsv` (clips every model run disagrees with). Outputs of earlier runs on the same list stay, so models can be
added one at a time.

From a shell, with a token that may run workflows:

```bash
curl -X POST -H "Authorization: Bearer $GITHUB_TOKEN" https://api.github.com/repos/PawgChamps/tagalog-tts-audio/actions/workflows/phones.yml/dispatches -d '{"ref":"main","inputs":{"list":"wordlist_all.tsv","models":"zipa","shards":"10","audio":"checkout"}}'
```

Locally: `python3 scripts/phones.py zipa LIST.tsv out/zipa.tsv` (needs `onnxruntime lhotse huggingface_hub` and a
clone of github.com/lingjzhu/zipa in `$ZIPA_SRC`), then `python3 scripts/score_phones.py LIST.tsv out checks/x`.

## The models (300-clip sample, 29/10/2026)

Both sides are reduced to a broad phone set before comparing (stress, length and diacritics dropped, ɾ/ɹ → r, lax
vowels → a e i o u); a clip counts at most 100 % wrong. Full numbers in `sample/report.md`.

| Model | Phone error (without ʔ) | Exact | Seconds per clip | Notes |
|---|---:|---:|---:|---|
| **ZIPA** large CR-CTC NS (`anyspeech/zipa-large-crctc-ns-800k`, ONNX) | **11.7 %** | **55 %** | **0.17** | best and fastest: the one to run on all clips |
| PhoneticXEUS (`changelinglab/PhoneticXeus`) | 12.5 % | 49 % | 1.04 | the only one that writes some glottal stops (7 of 73 final ʔ) |
| wav2vec2 espeak (`facebook/wav2vec2-lv-60-espeak-cv-ft`) | 13.4 % | 49 % | 0.54 | espeak phone set with tone digits |
| POWSM (`espnet/powsm`) | see `sample/report.md` | | | no Tagalog language token; run with `<unk>` |

None of them hears stress, and final glottal stops almost never, so the check says nothing about accent marks or
final ʔ.

## What the sample found

- **The TTS read its instruction aloud**: the `input` clip is the whole prompt ("read aloud clearly in a neutral
  tone…"), not the word. `extra_speech.tsv` lists every such clip.
- **Hyphenated words cut in half**: `bûtu-butu`, `sâga-saga`, `nâwo-nawo`, `lîngang-sina`, `tao-tao`, `mura-mura`,
  `bain-bain`, `dungan-dungan` and `pîg-yi` contain only the part before the hyphen (all three models agree), while
  `pâsang-awa` and `shao-shao` are complete. The full run gives the count (category `hyphenated`).
- **English loanwords spoken the Tagalog or Spanish way**: `technology` → *teknolohia*, `radiation` → *radiashon*,
  `solitary` → *solitario*, `newton` → *niwton*. Where the IPA column has an English reading, it does not match the
  clip.
