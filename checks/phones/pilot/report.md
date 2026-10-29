# Phone recognition check

300 clips. Error rate = phone edit distance / reference length, after reducing both sides to a broad Tagalog phone set (stress, length and diacritics dropped; ɾ/ɹ → r; lax vowels → a e i o u). The reference is the IPA column of the word list, so a high rate can mean the model, the audio or the IPA is wrong.

| Model | Clips | Error rate | Error rate without ʔ | Exact (without ʔ) | Final ʔ found | Final ʔ invented | Much longer than the word | s per clip |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| zipa | 34 | 10.1% | 4.3% | 74% | 0/4 | 0/30 | 0 | 0.18 |

## Error rate without ʔ, by category

| Category | zipa |
|---|---:|
| hyphenated | 5.9% |
| rule | 3.2% |

## Clips where 1 or more models hear much more than the word (0, all in extra_speech.tsv)

Usually the TTS read extra text (for example the instruction) into the clip: listen and re-synthesize.

(none)

## Clips heard much shorter than the word (under 60 % of its phones, words of 6+ phones): 0, all in truncated.tsv

| Kind | Cut short | Clips | Share |
|---|---:|---:|---:|
| hyphenated | 0 | 12 | 0.0% |
| plain | 0 | 22 | 0.0% |

## Clips every model disagrees with (40 % or more of the phones, without ʔ): 0, all in disagree.tsv

The word list IPA, the audio, or both are likely wrong here.

| Form | Category | IPA | zipa |
|---|---|---|---|

## zipa: the 15 clips it disagrees with most

| Form | Category | IPA | Heard |
|---|---|---|---|
| utang-na-loób | hyphenated | /ʔutaŋnaloˈʔob/ | ▁ u t ɑ ̃ n a l ə u b |
| manipulasyón | rule | /manipulasˈjon/ | ▁ m ə n i p u l ə ʃ u n |
| baliw | rule | /ˈbaliw/ | ▁ v a l i w |
| lambát-lambát | hyphenated | /lambatlamˈbat/ | ▁ ɛ l ə m b a t ɛ l ə m b a t |
| isinaulì | rule | /ʔisinaˈʔuliʔ/ | ▁ i s a n a u l i |
| pagtuturô | rule | /paɡtutuˈɾoʔ/ | ▁ p a ŋ t u t u r o |
| labing-waló | hyphenated | /labiŋwaˈlo/ | ▁ l a b i ŋ w a l o k |
| alsá-balutan | hyphenated | /ʔalˈsabalutan/ | ▁ ə l s a b ə l l u t a n |
| pagkakásunud-sunod | hyphenated | /paɡkaˈkasunudsunod/ | ▁ p a g k a q a s u n u d s u n u d |
| sinâ | rule | /siˈnaʔ/ | ▁ s i n a |
| puno | rule | /ˈpuno/ | ▁ p u n o |
| pinagkakagastusán | rule | /pinaɡkakaɡastuˈsan/ | ▁ p i n a g k a q a g a s t u s a n |
| pampamahalaán | rule | /pampamahalaˈʔan/ | ▁ p a m p a m a h a l a a n |
| pagsang-ayon | hyphenated | /paɡsaŋˈʔajon/ | ▁ p a g s a ŋ a j o n |
| paghiwá-hiwalayín | hyphenated | /paɡhiwahiwalaˈjin/ | ▁ p ə g h i w a h i w a l ̴ a j ɪ n |
