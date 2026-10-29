# Phone recognition check

300 clips. Error rate = phone edit distance / reference length, after reducing both sides to a broad Tagalog phone set (stress, length and diacritics dropped; ɾ/ɹ → r; lax vowels → a e i o u). The reference is the IPA column of the word list, so a high rate can mean the model, the audio or the IPA is wrong.

| Model | Clips | Error rate | Error rate without ʔ | Exact (without ʔ) | Final ʔ found | Final ʔ invented | Much longer than the word | s per clip |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| zipa | 297 | 11.8% | 6.7% | 54% | 0/28 | 0/269 | 0 | 0.13 |

## Error rate without ʔ, by category

| Category | zipa |
|---|---:|
| hyphenated | 7.1% |
| rule | 5.9% |

## Clips where 1 or more models hear much more than the word (0, all in extra_speech.tsv)

Usually the TTS read extra text (for example the instruction) into the clip: listen and re-synthesize.

(none)

## Clips heard much shorter than the word (under 60 % of its phones, words of 6+ phones): 0, all in truncated.tsv

| Kind | Cut short | Clips | Share |
|---|---:|---:|---:|
| hyphenated | 0 | 197 | 0.0% |
| plain | 0 | 100 | 0.0% |

## Clips every model disagrees with (40 % or more of the phones, without ʔ): 7, all in disagree.tsv

The word list IPA, the audio, or both are likely wrong here.

| Form | Category | IPA | zipa |
|---|---|---|---|
| pag-ipod | hyphenated | /paɡˈʔipod/ | ▁ p a k i p u n t |
| pugú | rule | /puˈɡu/ | ▁ t u ŋ g u |
| pingád | rule | /piˈŋad/ | ▁ p i ɲ a d |
| may-in-may-ín | hyphenated | /majʔinmajˈʔin/ | ▁ m e ɪ n m e ɪ n |
| dagán-dagán | hyphenated | /daɡandaˈɡan/ | ▁ d a g a d a n d ə g a n ə n |
| bunút | rule | /buˈnut/ | ▁ b o n o t |
| bay-án | hyphenated | /bajˈʔan/ | ▁ v a a n |

## zipa: the 15 clips it disagrees with most

| Form | Category | IPA | Heard |
|---|---|---|---|
| pag-ipod | hyphenated | /paɡˈʔipod/ | ▁ p a k i p u n t |
| pugú | rule | /puˈɡu/ | ▁ t u ŋ g u |
| pingád | rule | /piˈŋad/ | ▁ p i ɲ a d |
| may-in-may-ín | hyphenated | /majʔinmajˈʔin/ | ▁ m e ɪ n m e ɪ n |
| dagán-dagán | hyphenated | /daɡandaˈɡan/ | ▁ d a g a d a n d ə g a n ə n |
| bunút | rule | /buˈnut/ | ▁ b o n o t |
| bay-án | hyphenated | /bajˈʔan/ | ▁ v a a n |
| mag-uungól | hyphenated | /maɡʔuʔuˈŋol/ | ▁ m a g o m o ɔ l |
| bantáy-pintô | hyphenated | /bantajpinˈtoʔ/ | ▁ v e n t a ʎ p i n t o ɾ |
| pasabáy-sabayín | hyphenated | /pasabajsabaˈjin/ | ▁ p a s a b a j i n |
| may-diperénsiya | hyphenated | /majdipeˈɾensija/ | ▁ m ɛ j d i p ɛ r i n ʃ a |
| nangágkaka- | hyphenated | /naˈŋaɡkaka/ | ▁ l a ŋ a k a ː q a a |
| mag-alulóng | hyphenated | /maɡʔaluˈloŋ/ | ▁ m a g a ɛ l o l ɔ ̃ |
| waláng-diyós | hyphenated | /walaŋdiˈjos/ | ▁ w a l a ŋ d ʒ ɔ s |
| utang-na-loób | hyphenated | /ʔutaŋnaloˈʔob/ | ▁ u t ɑ ̃ n a l ə u b |
