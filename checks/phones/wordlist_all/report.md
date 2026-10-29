# Phone recognition check

151262 clips. Error rate = phone edit distance / reference length, after reducing both sides to a broad Tagalog phone set (stress, length and diacritics dropped; ɾ/ɹ → r; lax vowels → a e i o u). The reference is the IPA column of the word list, so a high rate can mean the model, the audio or the IPA is wrong.

| Model | Clips | Error rate | Error rate without ʔ | Exact (without ʔ) | Final ʔ found | Final ʔ invented | Much longer than the word | s per clip |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| zipa | 151262 | 12.8% | 9.6% | 54% | 8/8865 | 4/142397 | 5 | 0.16 |

## Error rate without ʔ, by category

| Category | zipa |
|---|---:|
| dictionary | 7.6% |
| english | 24.7% |
| hyphenated | 10.7% |
| rule | 9.6% |
| spelled | 50.3% |

## Clips where 1 or more models hear much more than the word (5, all in extra_speech.tsv)

Usually the TTS read extra text (for example the instruction) into the clip: listen and re-synthesize.

- ofw: zipa `▁ o ʊ ɛ f d ə b ə l ̴ j u`
- input: zipa `▁ ɹ ɛ d ə l a ʊ d k l ɪ ɹ l i ɪ n ə n u t ɹ ə l t o ʊ n ð ə t ɛ k s t ɪ z ə s ɪ ŋ g ə l f ɪ l ə p i n o ʊ w ə ˞ d s e ɪ `
- ocw: zipa `▁ o ʊ s i d ə b ə l ̴ j u`
- tumoy: zipa `▁ t u u n ʲ ɛ k ɭ a ɔ d v ɑ j ɛ m o j`
- ywca: zipa `▁ w a ɪ d ə b ə l ̴ j u s i e ɪ`

## Clips every model disagrees with (40 % or more of the phones, without ʔ): 8380, all in disagree.tsv

The word list IPA, the audio, or both are likely wrong here.

| Form | Category | IPA | zipa |
|---|---|---|---|
| ywca | rule | /ˈjwka/ | ▁ w a ɪ d ə b ə l ̴ j u s i e ɪ |
| your | english | /ˈjɔɹ/ | ▁ p u n i o |
| yoah | dictionary | /ˈida/ | ▁ j o w a |
| ymca | rule | /ˈjmka/ | ▁ w a ɛ m s i e j |
| yehey | dictionary | /ˈjehej/ | ▁ ɪ æ ɪ h æ ɪ |
| yatits | dictionary | /ˈidtitʃ/ | ▁ j a t e t s |
| xi | english | /ˈʃi/ | ▁ ʃ a m |
| word | dictionary | /ˈword/ | ▁ s i n a b i |
| wong | dictionary | /ˈwoŋ/ | ▁ v ɛ n |
| wise | dictionary | /ˈwise/ | ▁ v a j s |
| wi-fi | hyphenated | /ˈwifi/ | ▁ w a j f a j |
| wed | dictionary | /ˈwed/ | ▁ w ɛ n s d a j |
| walk | dictionary | /ˈwalk/ | ▁ g ɔ |
| wa | rule | /ˈwa/ | ▁ h u w a |
| vs | spelled | /viˈʔes/ | ▁ v ɜ r s ə s |
| vol | rule | /ˈvol/ | ▁ v ɔ l j u m |
| voice | english | /ˈvɔɪs/ | ▁ t a d a |
| vocal | english | /ˈvoʊkəl/ | ▁ s i n i p u p |
| viol | rule | /ˈviʔol/ | ▁ v a j u l i |
| verst | rule | /ˈveɾst/ | ▁ v ɜ ˞ s t ɑ p ɪ ŋ |
| uô | dictionary | /ʔuˈʔoʔ/ | ▁ u w o w |
| uád | dictionary | /ʔuˈʔad/ | ▁ u w ɑ d d e |
| utopianism | rule | /ʔutopiˈʔanism/ | ▁ j i t u n ɛ s k w ɔ ɑ j p ɪ n i s m u |
| uteg | dictionary | /ˈʔuteɡ/ | ▁ ə w t ɛ ŋ k |
| ust | rule | /ˈʔust/ | ▁ u ɛ s d i |
| user | rule | /ˈʔuseɾ/ | ▁ b a k a n t e |
| useless | english | /ˈjusləs/ | ▁ w o l a n k w ɛ n t a |
| upò | dictionary | /ˈʔupoʔ/ | ▁ o p p u |
| unq | rule | /ˈʔunk/ | ▁ u ɣ o j |
| unhcr | rule | /ˈʔunhkɾ/ | ▁ u ə n d e ɪ t ʃ s i ɑ ɹ |
| ungod | rule | /ˈʔuŋod/ | ▁ ə n g ɔ t |
| under | dictionary | /ˈʔunder/ | ▁ a ŋ |
| uncstd | rule | /ˈʔunkstd/ | ▁ u e n s i i e s t i i |
| ug | dictionary | /ˈʔuɡ/ | ▁ u g o d |
| tumoy | rule | /ˈtumoj/ | ▁ t u u n ʲ ɛ k ɭ a ɔ d v ɑ j ɛ m o j |
| tsu-tsu | hyphenated | /ˈtʃutʃu/ | ▁ t s u ː t s u ː |
| tsu | rule | /ˈtʃu/ | ▁ t s u ː |
| tsitsa | dictionary | /ˈtʃitʃa/ | ▁ t s i t s a |
| tsetse | dictionary | /ˈtʃetʃe/ | ▁ s ɛ t t s e |
| tidy | rule | /ˈtidj/ | ▁ t a j d i ɾ |
| thurs | dictionary | /ˈthurs/ | ▁ θ ɜ ˞ z d e ɪ |
| this | english | /ˈðɪs/ | ▁ g u b a s |
| theseus | english | /ˈθiˌziəs/ | ▁ f e s i ʎ o s |
| text | english | /ˈtɛkst/ | ▁ p a s ə t u g a |
| system | dictionary | /ˈʃstem/ | ▁ k a b a b a j a n |
| stress | english | /ˈstɹɛs/ | ▁ r i a m |
| start | rule | /ˈstaɾt/ | ▁ t a ŋ k a j |
| sro | rule | /ˈsɾo/ | ▁ ɛ s ɑ ɹ o ʊ |
| sr | spelled | /ʔesˈʔaɾ/ | ▁ s i n j o r |
| sq | spelled | /ʔesˈkju/ | ▁ s k w a r ɛ |
| speak | english | /ˈspik/ | ▁ s i b a g |
| shuzey | dictionary | /ˈshusi/ | ▁ ʃ u z e j |
| seq | rule | /ˈsek/ | ▁ s ɯ k j ɑ p |
| sept | dictionary | /ˈsept/ | ▁ s e p t i e m b ɾ ə |
| sea | english | /ˈsi/ | ▁ s ɛ j ə |
| scythe | english | /ˈsɪθ/ | ▁ s a j t |
| rna | dictionary | /ˈrna/ | ▁ ɑ ɹ ɛ n d e ɪ |
| repeat | english | /ɹɪˈpit/ | ▁ m ə t ə t a ə p o s |
| ref | dictionary | /ˈɾef/ | ▁ r ə f ɾ e n |
| reader | english | /ˈɹidɚ/ | ▁ h a ː p a ŋ |
| raid | rule | /ˈɾaʔid/ | ▁ r e j n t |
| quay | english | /ˈki/ | ▁ k w ɛ j |
| páawà | dictionary | /ˈpaʔawaʔ/ | ▁ p a a w a p a a w a |
| pyre | rule | /ˈpjɾe/ | ▁ b a ɪ ɜ ˞ i |
| puon | dictionary | /ˈpuʔon/ | ▁ b o o ɲ i |
| pta | dictionary | /ˈpta/ | ▁ p i t i e |
| proof | english | /ˈpɹuf/ | ▁ p r o ɛ b a |
| prof | rule | /ˈpɾof/ | ▁ p r o f ɛ s o r |
| procedure | english | /pɹəˈsidʒɚ/ | ▁ p r o s ɛ d i m i ɛ n t o |
| preserve | english | /pɹəˈzɝv/ | ▁ b ə t h i s ɜ ˞ v |
| plo | dictionary | /ˈplo/ | ▁ b e l ̴ o l ̴ |
| please | english | /ˈpliz/ | ▁ p a l a b a n |
| pl | spelled | /piˈʔel/ | ▁ p l a s ə |
| pier | english | /ˈpɪɹ/ | ▁ p i ɛ r r e |
| pgma | rule | /ˈpɡma/ | ▁ p i ʒ i e m e |
| pez | english | /ˈpɛz/ | ▁ v ɛ g s |
| pegpeg | rule | /ˈpeɡpeɡ/ | ▁ b ɛ ŋ b i ŋ k |
| paying | dictionary | /ˈpajiŋ/ | ▁ b a i n ə m |
| parish | english | /ˈpæɹɪʃ/ | ▁ p o r o q j æ |
| pants | dictionary | /ˈpantʃ/ | ▁ p ə n t a ʎ |
| paiwà | dictionary | /paˈʔiwaʔ/ | ▁ b a ɪ j u w ɔ t |
| pair | rule | /ˈpaʔiɾ/ | ▁ t e |
| page | dictionary | /ˈpaɡe/ | ▁ p a ː h i n a |
| oô | dictionary | /ʔoˈʔoʔ/ | ▁ t o t o |
| oò | dictionary | /ˈʔoʔoʔ/ | ▁ u u |
| owe | english | /ˈoʊ/ | ▁ u w e |
| ow | english | /ˈoʊ/ | ▁ ə w i ʃ |
| output | english | /ˈaʊtˌpʊt/ | ▁ s a w a |
| ooo | dictionary | /ʔoˈʔoʔo/ | ▁ i ŋ |
| oo- | hyphenated | /ˈʔoʔo/ | ▁ u u |
| oo | dictionary | /ˈʔoʔo/ | ▁ ɛ e |
| onion | rule | /ʔoˈniʔon/ | ▁ s i b u j a s |
| one | rule | /ˈʔone/ | ▁ w ə n |
| om | dictionary | /ˈʔom/ | ▁ o m k o d |
| olup | rule | /ˈʔolup/ | ▁ u l l u p i d |
| ol | rule | /ˈʔol/ | ▁ u l l æ t |
| ok-ok | hyphenated | /ˈʔokʔok/ | ▁ o k ɛ j o k ɛ j |
| ok | rule | /ˈʔok/ | ▁ o ʊ k e ɪ |
| oily | rule | /ˈʔoʔilj/ | ▁ p ɔ j i m i |
| ofw | rule | /ˈʔofw/ | ▁ o ʊ ɛ f d ə b ə l ̴ j u |
| of | english | /ˈʌv/ | ▁ ɔ f |
| oe | dictionary | /ˈʔoʔe/ | ▁ ɔ w i |
| ocw | rule | /ˈʔokw/ | ▁ o ʊ s i d ə b ə l ̴ j u |
| oct- | hyphenated | /ˈɔkt/ | ▁ o q t u b r e |
| oct | english | /ˈɔkt/ | ▁ o q t u b r e |
| ob-gyn | hyphenated | /ˈʔobɡin/ | ▁ o b i d ʒ i w a ɛ n |
| oats | rule | /ˈʔoʔatʃ/ | ▁ o l t s |
| npa | rule | /ˈnpa/ | ▁ e n p i e j |
| noisy | rule | /ˈnoʔisj/ | ▁ m a i ŋ a i |
| ngo | dictionary | /ˈŋo/ | ▁ e n ʒ i ɔ |
| ngets | dictionary | /ˈŋetʃ/ | ▁ ɲ ɛ t s |
| neve | english | /ˈniv/ | ▁ n e b e |
| ncca | rule | /ˈnkka/ | ▁ e n s i s i e |
| mápapagbalikan | dictionary | /ˈmapapaɡbalikan/ | ▁ m a p a p a g b a l i k a n m a p ə p a k b ə l i k a n |
| máisaulì | dictionary | /ˈmaʔisaʔuliʔ/ | ▁ m a i s a u l i m a i s a u l i |
| mt | spelled | /ʔemˈti/ | ▁ m ɔ w n t |
| mr | spelled | /ʔemˈʔaɾ/ | ▁ m i s t r |
| mme | dictionary | /ˈmme/ | ▁ e ɪ i n æ |
| mm | spelled | /ʔemˈʔem/ | ▁ b a |
| miunu | dictionary | /ˈmumo/ | ▁ m i j u n u |
| mfa | rule | /ˈmfa/ | ▁ ɛ m ɛ f e |
| meil | rule | /ˈmeʔil/ | ▁ m a j l i n |
| mdma | rule | /ˈmdma/ | ▁ ɛ m d i e m e |
| mba | dictionary | /ˈmba/ | ▁ ɛ m b ɛ e |
| mb | spelled | /ʔemˈbi/ | ▁ m ə b a h i |
| manun | dictionary | /ˈmanun/ | ▁ m a n o n u l l a t |
| male | dictionary | /ˈmale/ | ▁ r i l a b |
| ltd | spelled | /ʔeltiˈdi/ | ▁ l i m i t a d o |
| loud | english | /ˈlaʊd/ | ▁ i n a p |
| look | english | /ˈlʊk/ | ▁ l u g a r |
| liklík | dictionary | /likˈlik/ | ▁ l e a g e l e a g e |
| like | dictionary | /ˈlike/ | ▁ b a q a j |
| lgi | dictionary | /ˈlɡi/ | ▁ e l ʒ i a |
| letter | dictionary | /ˈletter/ | ▁ s ɑ b ɑ q |
| leal | english | /ˈlil/ | ▁ l e j a l |
| leah | english | /ˈliə/ | ▁ ɛ l ɛ j ə |
| lb | spelled | /ʔelˈbi/ | ▁ p a ʊ n d |
| lath | english | /ˈlæθ/ | ▁ l a f i n g |
| krill | english | /ˈkɹɪl/ | ▁ k ɯ r i j i l l e |
| know | english | /ˈnoʊ/ | ▁ k i l æ |
| kneecap | english | /ˈniˌkæp/ | ▁ t u ɔ d |
| kmu | rule | /ˈkmu/ | ▁ k e ɛ m j u |
| kmi | dictionary | /ˈkmi/ | ▁ k i ɛ m a j |
| kalá | dictionary | /kaˈla/ | ▁ k a l a a j o n |
| june | dictionary | /ˈdʒun/ | ▁ x u ɲ j o |
| jueteng | english | /ˈdʒuˌtɛŋ/ | ▁ ʒ ɔ w ə t ɛ ŋ k |
| jcl | spelled | /dʒeisiˈʔel/ | ▁ h o t a |
| isin | rule | /ˈʔisin/ | ▁ i s i n a b a t |
| isbn | dictionary | /ˈʔisbn/ | ▁ a ɪ ɛ s b i ɛ n |
| ir | rule | /ˈʔiɾ/ | ▁ i r a w |
| ip | dictionary | /ˈʔip/ | ▁ i p o p |
| input | dictionary | /ˈʔinput/ | ▁ ɹ ɛ d ə l a ʊ d k l ɪ ɹ l i ɪ n ə n u t ɹ ə l t o ʊ n ð ə  |
| imf | rule | /ˈʔimf/ | ▁ a j ɛ m ɛ f |
| ikul | dictionary | /ˈʔikul/ | ▁ i l l u k o l |
| iit | rule | /ˈʔiʔit/ | ▁ i g a i |
| ies | dictionary | /ˈʔes/ | ▁ i i e s |
| idipá | dictionary | /ʔidiˈpa/ | ▁ i l ɛ n ɛ s t p a |
| icbm | rule | /ˈʔikbm/ | ▁ a ɪ s i b i ɛ m |
| ibp | dictionary | /ˈʔibp/ | ▁ a ɪ b i p i |
| ibm | dictionary | /ˈʔibm/ | ▁ a j b i ɛ m |
| hî | rule | /ˈhiʔ/ | ▁ ɕ i n |
| huhu | dictionary | /ˈhuhu/ | ▁ h i f i t |
| hi- | hyphenated | /ˈhi/ | ▁ h a j |
| hg | spelled | /ʔeitʃˈdʒi/ | ▁ e ɪ t ʃ d i w a ɪ a ɪ |
| hf | spelled | /ʔeitʃˈʔef/ | ▁ h u |
| here | dictionary | /ˈhere/ | ▁ s a b i |
| heaven | english | /ˈhɛvən/ | ▁ k ə l ə ŋ i t a n |
| hb | spelled | /ʔeitʃˈbi/ | ▁ h a |
| guts | dictionary | /ˈɡutʃ/ | ▁ g a t s |
| gpu | rule | /ˈɡpu/ | ▁ d ʒ i p i j u |
| gnu | rule | /ˈɡnu/ | ▁ d ʒ i ɛ n d j u |
| gma | rule | /ˈɡma/ | ▁ d ʒ i ɛ m e |
| giyc | rule | /ˈɡijk/ | ▁ g i a ɪ w a ɪ s i |
| gg | dictionary | /ˈdjidji/ | ▁ g a |
| ge | dictionary | /ˈɡe/ | ▁ d ʒ ɛ j |
| gd | spelled | /dʒiˈdi/ | ▁ g r a n d |
| forward | english | /ˈfɔɹwɚd/ | ▁ p a l a w a k |
| father | english | /ˈfɑðɚ/ | ▁ p a l a b r a |
| fast | english | /ˈfæst/ | ▁ p a k i t a j o |
| false | english | /ˈfɔls/ | ▁ p i n a |
| eyyy | dictionary | /ˈʔej/ | ▁ e j a j j a j |
| expensive | english | /ɪkˈspɛnsɪv/ | ▁ m a x a l |
| eve | english | /ˈiv/ | ▁ ɛ v ɛ |
| ets | dictionary | /ˈʔetʃ/ | ▁ ɛ t s |
| esp | dictionary | /ˈʔesp/ | ▁ ɛ s p e ʃ a l i |
| er | rule | /ˈʔeɾ/ | ▁ ɯ ð |
| eocene | english | /ˈiəˌsin/ | ▁ ɛ ʎ o s ɛ n ɛ |
| envy | english | /ˈɛnvi/ | ▁ ə ŋ g i t |
| eighth | english | /ˈeɪtθ/ | ▁ i g w ə l o |
| egg | dictionary | /ˈʔeɡɡ/ | ▁ ɪ t l ̴ o g |
| ef | rule | /ˈʔef/ | ▁ e s s ɛ k |
| ee | english | /ˈi/ | ▁ e |
| ecg | rule | /ˈʔekɡ/ | ▁ i s i ʒ i |
| ease | english | /ˈiz/ | ▁ i i s |
| e-vat | hyphenated | /ˈiˌvæt/ | ▁ t e |
| dyi | rule | /ˈdji/ | ▁ d i w a ɪ a ɪ |
| dya | dictionary | /ˈdʒa/ | ▁ d i a |
| dy | dictionary | /ˈdi/ | ▁ d ɾ a j |
| dr | spelled | /diˈʔaɾ/ | ▁ d o q t o r |
| dna | rule | /ˈdna/ | ▁ d i e n e |

## zipa: the 15 clips it disagrees with most

| Form | Category | IPA | Heard |
|---|---|---|---|
| ywca | rule | /ˈjwka/ | ▁ w a ɪ d ə b ə l ̴ j u s i e ɪ |
| your | english | /ˈjɔɹ/ | ▁ p u n i o |
| yoah | dictionary | /ˈida/ | ▁ j o w a |
| ymca | rule | /ˈjmka/ | ▁ w a ɛ m s i e j |
| yehey | dictionary | /ˈjehej/ | ▁ ɪ æ ɪ h æ ɪ |
| yatits | dictionary | /ˈidtitʃ/ | ▁ j a t e t s |
| xi | english | /ˈʃi/ | ▁ ʃ a m |
| word | dictionary | /ˈword/ | ▁ s i n a b i |
| wong | dictionary | /ˈwoŋ/ | ▁ v ɛ n |
| wise | dictionary | /ˈwise/ | ▁ v a j s |
| wi-fi | hyphenated | /ˈwifi/ | ▁ w a j f a j |
| wed | dictionary | /ˈwed/ | ▁ w ɛ n s d a j |
| walk | dictionary | /ˈwalk/ | ▁ g ɔ |
| wa | rule | /ˈwa/ | ▁ h u w a |
| vs | spelled | /viˈʔes/ | ▁ v ɜ r s ə s |
