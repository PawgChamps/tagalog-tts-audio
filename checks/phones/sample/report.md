# Phone recognition check

300 clips. Error rate = phone edit distance / reference length, after reducing both sides to a broad Tagalog phone set (stress, length and diacritics dropped; ɾ/ɹ → r; lax vowels → a e i o u). The reference is the IPA column of the word list, so a high rate can mean the model, the audio or the IPA is wrong.

| Model | Clips | Error rate | Error rate without ʔ | Exact (without ʔ) | Final ʔ found | Final ʔ invented | Much longer than the word | s per clip |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| powsm | 0 | – | – | – | – | – | – | – |
| w2v2 | 300 | 17.7% | 13.4% | 49% | 0/73 | 0/227 | 1 | 0.54 |
| xeus | 300 | 16.2% | 12.5% | 49% | 7/73 | 1/227 | 1 | 1.04 |
| zipa | 300 | 16.3% | 11.7% | 55% | 0/73 | 0/227 | 1 | 0.17 |

## Error rate without ʔ, by category

| Category | powsm | w2v2 | xeus | zipa |
|---|---:|---:|---:|---:|
| circ_bug | – | 11.9% | 13.0% | 13.0% |
| dict | – | 8.6% | 8.6% | 7.0% |
| english | – | 23.2% | 23.6% | 27.2% |
| english_tagalog | – | 28.0% | 26.7% | 27.3% |
| glottal | – | 6.3% | 6.0% | 3.3% |
| heteronym | – | 16.5% | 11.3% | 10.1% |
| nostress | – | 14.4% | 10.5% | 8.7% |

## Clips where two or more models hear much more than the word

Usually the TTS read extra text (for example the instruction) into the clip: listen and re-synthesize.

- input: w2v2 `ɹ iː d ɐ l aʊ d k l iː l i ɪ n ɐ n uː t ɹ əl t oʊ n d ð ə t ɛ k s t ɪ z ɐ s ɪ ŋ ɡ əl f ɪ l ɪ p iː n oʊ w ɜː d s eɪ oʊ n `, xeus `ɹ ɛ d ə l a ʊ d kʰ l ɪ ɹ l i ɪ̃ n ə n u t ɹ ə l tʰ o ʊ̃ n ð ə tʰ ɛ k s t ɪ z ə s ɪ̃ ŋ ɡ ə l f ɪ l ə p ĩ n o ʊ w ə˞ d s `, zipa `▁ ɹ ɛ d ə l a ʊ d k l ɪ ɹ l i ɪ n ə n u t ɹ ə l t o ʊ n ð ə t ɛ k s t ɪ z ə s ɪ ŋ g ə l f ɪ l ə p i n o ʊ w ə ˞ d s e ɪ `

## Clips every model disagrees with (40 % or more of the phones, without ʔ)

The word list IPA, the audio, or both are likely wrong here.

| Form | Category | IPA | w2v2 | xeus | zipa |
|---|---|---|---|---|---|
| input | heteronym | /ˈʔinput/ | ɹ iː d ɐ l aʊ d k l iː l i ɪ n ɐ n uː t ɹ əl t oʊ n d ð ə t  | ɹ ɛ d ə l a ʊ d kʰ l ɪ ɹ l i ɪ̃ n ə n u t ɹ ə l tʰ o ʊ̃ n ð  | ▁ ɹ ɛ d ə l a ʊ d k l ɪ ɹ l i ɪ n ə n u t ɹ ə l t o ʊ n ð ə  |
| whale | english | /ˈweɪl/ | w aː l i | w a l i | ▁ w a l e |
| dungan-dungan | english_tagalog | /ˈdʌŋɡənˌdʌŋɡən/ | d u a n | d̪ u ŋ ʌ n | ▁ d u ŋ a n |
| two | nostress | /ˈtwo/ | t u5 | t u | ▁ t u |
| bûtu-butu | circ_bug | /ˈbutubutu/ | b u t o | b u t u | ▁ b o t o |
| bain-bain | english_tagalog | /ˈbeɪnˌbeɪn/ | b a ʔ i n | b a ʔ i n | ▁ b a i n |
| pîg-yi | circ_bug | /ˈpiɡji/ | b i ŋ ɡ | p i ɡ | ▁ p i n g |
| newton | english | /ˈnutən/ | n i d o n | n i w t o n | ▁ n ɛ u w t o n |
| tao-tao | english_tagalog | /ˈtaʊˌtaʊ/ | t ɑ5 u5 | t a u | ▁ t a o |
| solitary | english | /ˈsɑləˌtɛɹi/ | s o l i t a r o | s o l i t a r i o | ▁ s o l i t a r j o |
| coverage | english | /ˈkʌvɚədʒ/ | ɡ ɔ v ɛ ɹ ɨ dʒ | ɡ ɔ v ɜ˞ ɹ i ʒ | ▁ g ɔ l v e r i d ʒ |
| upóng | heteronym | /ʔuˈpoŋ/ | u p ɑ̃ | o p õ | ▁ o p o w |
| sâga-saga | circ_bug | /ˈsaɡasaɡa/ | s a ɡ a | s a ɡ a | ▁ s a g a |
| nâwo-nawo | circ_bug | /ˈnawonawo/ | n aː w o | n a w ɔ | ▁ n a w ɔ |
| mura-mura | english_tagalog | /ˈmʊɹəˌmʊɹə/ | m u r a | m u r a | ▁ m u r a |
| lîngang-sina | circ_bug | /ˈliŋaŋsina/ | l i ŋ ʌ n | l i ŋ a n | ▁ l i ŋ g a n |
| radiation | english | /ˌɹeɪdiˈeɪʃən/ | r a d i eː ʃ o n | r a d i e ʃ o n | ▁ r a d i a ʃ j o n |
| technology | english | /tɛkˈnɑlədʒi/ | t e k n o l o h i a | t ɛ k n o l o x i a | ▁ t ɛ k n o l o x i a |

## w2v2: the 15 clips it disagrees with most

| Form | Category | IPA | Heard |
|---|---|---|---|
| input | heteronym | /ˈʔinput/ | ɹ iː d ɐ l aʊ d k l iː l i ɪ n ɐ n uː t ɹ əl t oʊ n d ð ə t ɛ k s t ɪ z ɐ s ɪ ŋ ɡ əl f ɪ l ɪ p iː n oʊ w ɜː d s eɪ oʊ n l i ð æ t w ɚ d w ɪ ð ð ə s t ɹ ɛ s w ɜː ð i æ k s ɛ n t m ɑːɹ k s p ʊ ɾ ɪ t |
| ngitngít | dict | /ŋitˈŋit/ | ɲ i t ɲ iː |
| pîg-yi | circ_bug | /ˈpiɡji/ | b i ŋ ɡ |
| whale | english | /ˈweɪl/ | w aː l i |
| dungan-dungan | english_tagalog | /ˈdʌŋɡənˌdʌŋɡən/ | d u a n |
| two | nostress | /ˈtwo/ | t u5 |
| bûtu-butu | circ_bug | /ˈbutubutu/ | b u t o |
| bain-bain | english_tagalog | /ˈbeɪnˌbeɪn/ | b a ʔ i n |
| síngit | heteronym | /ˈsiŋit/ | s iː ɲ e |
| newton | english | /ˈnutən/ | n i d o n |
| silicate | english | /ˈsɪləkət/ | s ɪ l i ɡ eɪ t |
| upóng | heteronym | /ʔuˈpoŋ/ | u p ɑ̃ |
| upong | heteronym | /ˈʔupoŋ/ | u p ʉ n |
| treatment | english | /ˈtɹitmənt/ | d r iː d m ɛ n d |
| toyò | dict | /ˈtojoʔ/ | t uo5 j u5 |

## xeus: the 15 clips it disagrees with most

| Form | Category | IPA | Heard |
|---|---|---|---|
| input | heteronym | /ˈʔinput/ | ɹ ɛ d ə l a ʊ d kʰ l ɪ ɹ l i ɪ̃ n ə n u t ɹ ə l tʰ o ʊ̃ n ð ə tʰ ɛ k s t ɪ z ə s ɪ̃ ŋ ɡ ə l f ɪ l ə p ĩ n o ʊ w ə˞ d s e ɪ o ʊ̃ n l i ð æ t w ə˞ d w ɪ ð ð ə s t ɹ ɛ s w ɛ ɹ ð ə æ k s ɛ̃ n t m ɑ ɹ k s pʰ ʊ t ɪ t |
| whale | english | /ˈweɪl/ | w a l i |
| mike | nostress | /ˈmike/ | m a j k |
| Sulú | dict | /suˈlu/ | s u n l o p |
| two | nostress | /ˈtwo/ | t u |
| dungan-dungan | english_tagalog | /ˈdʌŋɡənˌdʌŋɡən/ | d̪ u ŋ ʌ n |
| bain-bain | english_tagalog | /ˈbeɪnˌbeɪn/ | b a ʔ i n |
| newton | english | /ˈnutən/ | n i w t o n |
| coverage | english | /ˈkʌvɚədʒ/ | ɡ ɔ v ɜ˞ ɹ i ʒ |
| upóng | heteronym | /ʔuˈpoŋ/ | o p õ |
| tao-tao | english_tagalog | /ˈtaʊˌtaʊ/ | t a u |
| sâga-saga | circ_bug | /ˈsaɡasaɡa/ | s a ɡ a |
| solitary | english | /ˈsɑləˌtɛɹi/ | s o l i t a r i o |
| nâwo-nawo | circ_bug | /ˈnawonawo/ | n a w ɔ |
| nasyón | dict | /nasˈjon/ | n a ʃ u n |

## zipa: the 15 clips it disagrees with most

| Form | Category | IPA | Heard |
|---|---|---|---|
| input | heteronym | /ˈʔinput/ | ▁ ɹ ɛ d ə l a ʊ d k l ɪ ɹ l i ɪ n ə n u t ɹ ə l t o ʊ n ð ə t ɛ k s t ɪ z ə s ɪ ŋ g ə l f ɪ l ə p i n o ʊ w ə ˞ d s e ɪ o ʊ n l i ð æ t w ə ˞ d w ɪ ð ð ə s t ɹ ɛ s w ɛ ɹ ð ə æ k s ɛ n t m ɑ ɹ k s p ʊ t ɪ t |
| whale | english | /ˈweɪl/ | ▁ w a l e |
| bûtu-butu | circ_bug | /ˈbutubutu/ | ▁ b o t o |
| two | nostress | /ˈtwo/ | ▁ t u |
| tao-tao | english_tagalog | /ˈtaʊˌtaʊ/ | ▁ t a o |
| dungan-dungan | english_tagalog | /ˈdʌŋɡənˌdʌŋɡən/ | ▁ d u ŋ a n |
| solitary | english | /ˈsɑləˌtɛɹi/ | ▁ s o l i t a r j o |
| bain-bain | english_tagalog | /ˈbeɪnˌbeɪn/ | ▁ b a i n |
| radiation | english | /ˌɹeɪdiˈeɪʃən/ | ▁ r a d i a ʃ j o n |
| pîg-yi | circ_bug | /ˈpiɡji/ | ▁ p i n g |
| newton | english | /ˈnutən/ | ▁ n ɛ u w t o n |
| coverage | english | /ˈkʌvɚədʒ/ | ▁ g ɔ l v e r i d ʒ |
| lîngang-sina | circ_bug | /ˈliŋaŋsina/ | ▁ l i ŋ g a n |
| virology | english | /vɪˈɹɑlədʒi/ | ▁ v i ɛ r o l ̴ o h i |
| upóng | heteronym | /ʔuˈpoŋ/ | ▁ o p o w |
