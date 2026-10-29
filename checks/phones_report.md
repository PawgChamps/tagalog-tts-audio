# Phone recognition check

300 clips. Error rate = phone edit distance / reference length, after reducing both sides to a broad Tagalog phone set (stress, length and diacritics dropped; ɾ/ɹ → r; lax vowels → a e i o u). The reference is the IPA column of the word list, so a high rate can mean the model, the audio or the IPA is wrong.

| Model | Clips | Error rate | Error rate without ʔ | Exact (without ʔ) | Final ʔ found | Final ʔ invented | s per clip |
|---|---:|---:|---:|---:|---:|---:|---:|
| powsm | 0 | – | – | – | – | – | – |
| w2v2 | 0 | – | – | – | – | – | – |

## Error rate without ʔ, by category

| Category | powsm | w2v2 |
|---|---:|---:|
| circ_bug | – | – |
| dict | – | – |
| english | – | – |
| english_tagalog | – | – |
| glottal | – | – |
| heteronym | – | – |
| nostress | – | – |
