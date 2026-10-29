# Phone recognition check

300 clips. Error rate = phone edit distance / reference length, after reducing both sides to a broad Tagalog phone set (stress, length and diacritics dropped; ɾ/ɹ → r; lax vowels → a e i o u). The reference is the IPA column of the word list, so a high rate can mean the model, the audio or the IPA is wrong.

| Model | Clips | Error rate | Error rate without ʔ | Exact (without ʔ) | Final ʔ found | Final ʔ invented | s per clip |
|---|---:|---:|---:|---:|---:|---:|---:|
| powsm | 0 | – | – | – | – | – | – |
| w2v2 | 300 | 23.1% | 19.2% | 45% | 0/73 | 0/227 | 0.54 |
| xeus | 300 | 21.1% | 17.7% | 47% | 7/73 | 1/227 | 1.04 |
| zipa | 300 | 32.6% | 30.1% | 0% | 0/73 | 0/227 | 0.17 |

## Error rate without ʔ, by category

| Category | powsm | w2v2 | xeus | zipa |
|---|---:|---:|---:|---:|
| circ_bug | – | 14.4% | 13.7% | 26.7% |
| dict | – | 10.6% | 10.4% | 20.9% |
| english | – | 23.2% | 23.9% | 41.7% |
| english_tagalog | – | 29.8% | 28.0% | 38.5% |
| glottal | – | 8.7% | 6.8% | 17.2% |
| heteronym | – | 54.0% | 48.8% | 64.9% |
| nostress | – | 15.3% | 11.4% | 22.3% |

## w2v2: the 15 clips it disagrees with most

| Form | Category | IPA | Heard |
|---|---|---|---|
| input | heteronym | /ˈʔinput/ | ɹ iː d ɐ l aʊ d k l iː l i ɪ n ɐ n uː t ɹ əl t oʊ n d ð ə t ɛ k s t ɪ z ɐ s ɪ ŋ ɡ əl f ɪ l ɪ p iː n oʊ w ɜː d s eɪ oʊ n l i ð æ t w ɚ d w ɪ ð ð ə s t ɹ ɛ s w ɜː ð i æ k s ɛ n t m ɑːɹ k s p ʊ ɾ ɪ t |
| toyò | dict | /ˈtojoʔ/ | t uo5 j u5 |
| ngitngít | dict | /ŋitˈŋit/ | ɲ i t ɲ iː |
| pîg-yi | circ_bug | /ˈpiɡji/ | b i ŋ ɡ |
| whale | english | /ˈweɪl/ | w aː l i |
| hiyá | heteronym | /hiˈja/ | ɕ i5 j ɑ5 |
| dungan-dungan | english_tagalog | /ˈdʌŋɡənˌdʌŋɡən/ | d u a n |
| two | nostress | /ˈtwo/ | t u5 |
| tao-tao | english_tagalog | /ˈtaʊˌtaʊ/ | t ɑ5 u5 |
| shao-shao | english_tagalog | /ˈʃaʊˌʃaʊ/ | s. ɑu5 s. ɑu5 |
| pinawà | glottal | /piˈnawaʔ/ | b i5 n ɑ5 w ɑ5 |
| pinaka | nostress | /piˈnaka/ | b i j i n a q a |
| pâsang-awa | circ_bug | /ˈpasaŋʔawa/ | p ə1 s a5 ŋ ɑu5 w ɑ5 |
| bûtu-butu | circ_bug | /ˈbutubutu/ | b u t o |
| bain-bain | english_tagalog | /ˈbeɪnˌbeɪn/ | b a ʔ i n |

## xeus: the 15 clips it disagrees with most

| Form | Category | IPA | Heard |
|---|---|---|---|
| input | heteronym | /ˈʔinput/ | ɹ ɛ d ə l a ʊ d kʰ l ɪ ɹ l i ɪ̃ n ə n u t ɹ ə l tʰ o ʊ̃ n ð ə tʰ ɛ k s t ɪ z ə s ɪ̃ ŋ ɡ ə l f ɪ l ə p ĩ n o ʊ w ə˞ d s e ɪ o ʊ̃ n l i ð æ t w ə˞ d w ɪ ð ð ə s t ɹ ɛ s w ɛ ɹ ð ə æ k s ɛ̃ n t m ɑ ɹ k s pʰ ʊ t ɪ t |
| whale | english | /ˈweɪl/ | w a l i |
| mike | nostress | /ˈmike/ | m a j k |
| Sulú | dict | /suˈlu/ | s u n l o p |
| coverage | english | /ˈkʌvɚədʒ/ | ɡ ɔ v ɜ˞ ɹ i ʒ |
| two | nostress | /ˈtwo/ | t u |
| shao-shao | english_tagalog | /ˈʃaʊˌʃaʊ/ | ʂ a w ʂ a w |
| dungan-dungan | english_tagalog | /ˈdʌŋɡənˌdʌŋɡən/ | d̪ u ŋ ʌ n |
| bain-bain | english_tagalog | /ˈbeɪnˌbeɪn/ | b a ʔ i n |
| newton | english | /ˈnutən/ | n i w t o n |
| upóng | heteronym | /ʔuˈpoŋ/ | o p õ |
| tao-tao | english_tagalog | /ˈtaʊˌtaʊ/ | t a u |
| sâga-saga | circ_bug | /ˈsaɡasaɡa/ | s a ɡ a |
| solitary | english | /ˈsɑləˌtɛɹi/ | s o l i t a r i o |
| nâwo-nawo | circ_bug | /ˈnawonawo/ | n a w ɔ |

## zipa: the 15 clips it disagrees with most

| Form | Category | IPA | Heard |
|---|---|---|---|
| input | heteronym | /ˈʔinput/ | ▁ ɹ ɛ d ə l a ʊ d k l ɪ ɹ l i ɪ n ə n u t ɹ ə l t o ʊ n ð ə t ɛ k s t ɪ z ə s ɪ ŋ g ə l f ɪ l ə p i n o ʊ w ə ˞ d s e ɪ o ʊ n l i ð æ t w ə ˞ d w ɪ ð ð ə s t ɹ ɛ s w ɛ ɹ ð ə æ k s ɛ n t m ɑ ɹ k s p ʊ t ɪ t |
| whale | english | /ˈweɪl/ | ▁ w a l e |
| two | nostress | /ˈtwo/ | ▁ t u |
| shao-shao | english_tagalog | /ˈʃaʊˌʃaʊ/ | ▁ ʂ a w ʂ a w |
| pîg-yi | circ_bug | /ˈpiɡji/ | ▁ p i n g |
| newton | english | /ˈnutən/ | ▁ n ɛ u w t o n |
| upóng | heteronym | /ʔuˈpoŋ/ | ▁ o p o w |
| upong | heteronym | /ˈʔupoŋ/ | ▁ o p u ŋ |
| solitary | english | /ˈsɑləˌtɛɹi/ | ▁ s o l i t a r j o |
| bûtu-butu | circ_bug | /ˈbutubutu/ | ▁ b o t o |
| Sulú | dict | /suˈlu/ | ▁ s u l l o |
| coverage | english | /ˈkʌvɚədʒ/ | ▁ g ɔ l v e r i d ʒ |
| radiation | english | /ˌɹeɪdiˈeɪʃən/ | ▁ r a d i a ʃ j o n |
| tao-tao | english_tagalog | /ˈtaʊˌtaʊ/ | ▁ t a o |
| pinaka | nostress | /piˈnaka/ | ▁ b i j n ɑ q ɑ |
