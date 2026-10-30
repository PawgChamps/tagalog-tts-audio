# Phone recognition check

147533 clips. Error rate = phone edit distance / reference length, after reducing both sides to a broad Tagalog phone set (stress, length and diacritics dropped; ɾ/ɹ → r; lax vowels → a e i o u). The reference is the IPA column of the word list, so a high rate can mean the model, the audio or the IPA is wrong.

| Model | Clips | Error rate | Error rate without ʔ | Exact (without ʔ) | Final ʔ found | Final ʔ invented | Much longer than the word | s per clip |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| zipa | 147533 | 12.0% | 8.5% | 55% | 12/9961 | 4/137572 | 5 | 0.15 |

## Error rate without ʔ, by category

| Category | zipa |
|---|---:|
| dictionary | 8.6% |
| english | 16.0% |
| hyphenated | 7.2% |
| rule | 8.0% |
| spelled | 20.3% |

## Clips where 1 or more models hear much more than the word (5, all in extra_speech.tsv)

Usually the TTS read extra text (for example the instruction) into the clip: listen and re-synthesize.

- ofw: zipa `▁ o ʊ ɛ f d ə b ə l ̴ j u`
- ocw: zipa `▁ o ʊ s i d ə b ə l ̴ j u`
- kalí-kalibumbón: zipa `▁ k a l i k a l i b o m b o n k a l i k a l i b u m b o n k a l i k a l i b u m b o n`
- swswsw: zipa `▁ ɛ s d ə b ə l ̴ j u ɛ s d ə b ə l ̴ j u ɛ s d ə b ə l ̴ j u`
- ywca: zipa `▁ w a ɪ d ə b ə l ̴ j u s i e ɪ`

## Clips heard much shorter than the word (under 60 % of its phones, words of 6+ phones): 55, all in truncated.tsv

| Kind | Cut short | Clips | Share |
|---|---:|---:|---:|
| hyphenated | 19 | 13881 | 0.1% |
| plain | 36 | 133652 | 0.0% |

## Clips every model disagrees with (40 % or more of the phones, without ʔ): 5383, all in disagree.tsv

The word list IPA, the audio, or both are likely wrong here.

| Form | Category | IPA | zipa |
|---|---|---|---|
| ywca | rule | /ˈʔiwka/ | ▁ w a ɪ d ə b ə l ̴ j u s i e ɪ |
| ymca | rule | /ˈʔimka/ | ▁ w a ɛ m s i e j |
| yehey | dictionary | /ˈjehej/ | ▁ ɪ æ ɪ h æ ɪ |
| xi | english | /ˈʃi/ | ▁ ʃ a m |
| word | english | /ˈwɝd/ | ▁ s i n a b i |
| wong | dictionary | /ˈwoŋ/ | ▁ v ɛ n |
| wi-fi | hyphenated | /ˈwifi/ | ▁ w a j f a j |
| wed | english | /ˈwɛd/ | ▁ w ɛ n s d a j |
| we | english | /ˈwi/ | ▁ u w ɛ |
| waláng-konsiderasyón | hyphenated | /walaŋkonsideɾasˈjon/ | ▁ w a l a ŋ k o n s i d e ɾ a s o n w a l a ŋ k o n s i d e  |
| waláng-kakanin | hyphenated | /waˈlaŋkakanin/ | ▁ w a ː l a ŋ k ʰ a k ʰ a n i n w a l a ŋ k ʰ a ː k ʰ a ː n  |
| wa | dictionary | /wa/ | ▁ h u w a |
| vs | spelled | /viˈʔes/ | ▁ v ɜ r s ə s |
| vol | rule | /ˈvol/ | ▁ v ɔ l j u m |
| vip | rule | /ˈvip/ | ▁ v i a ɪ p i |
| viol | rule | /ˈviʔol/ | ▁ v a j u l i |
| verst | rule | /ˈveɾst/ | ▁ v ɜ ˞ s t ɑ p ɪ ŋ |
| uô | dictionary | /ʔuˈʔoʔ/ | ▁ u w o w |
| uád | dictionary | /ʔuˈʔad/ | ▁ u w ɑ d d e |
| utopianism | rule | /ʔutopiˈʔanism/ | ▁ j i t u n ɛ s k w ɔ ɑ j p ɪ n i s m u |
| uteg | rule | /ˈʔuteɡ/ | ▁ ə w t ɛ ŋ k |
| user | english | /ˈjuzɚ/ | ▁ b a k a n t e |
| us | english | /ˈʌs/ | ▁ u s a |
| upò | dictionary | /ˈʔupoʔ/ | ▁ o p p u |
| unq | rule | /ˈʔunk/ | ▁ u ɣ o j |
| unhcr | rule | /ˈʔunhkɾ/ | ▁ u ə n d e ɪ t ʃ s i ɑ ɹ |
| uncstd | rule | /ˈʔunkstd/ | ▁ u e n s i i e s t i i |
| ug | rule | /ˈʔuɡ/ | ▁ u g o d |
| tuy | dictionary | /ˈtwi/ | ▁ t u j u |
| tsô | rule | /ˈtʃoʔ/ | ▁ s o w |
| tsu-tsu | hyphenated | /ˈtʃutʃu/ | ▁ t s u ː t s u ː |
| tsu | rule | /ˈtʃu/ | ▁ t s u ː |
| tsitsa | dictionary | /ˈtʃitʃa/ | ▁ t s i t s a |
| tsetse | rule | /ˈtʃetʃe/ | ▁ s ɛ t t s e |
| tongue | english | /ˈtʌŋ/ | ▁ t a ŋ ŋ o k |
| thurs | rule | /ˈthuɾs/ | ▁ θ ɜ ˞ z d e ɪ |
| text | english | /ˈtɛkst/ | ▁ p a s ə t u g a |
| tatsó | rule | /taˈtʃo/ | ▁ t æ t s s o ʊ |
| taguyod | rule | /taˈɡujod/ | ▁ t ɑ g u u n ʲ ɛ s k a d v ɑ j ɛ ʲ ɔ d |
| t- | hyphenated | /ˈti/ | ▁ t ə t a |
| system | english | /ˈsɪstəm/ | ▁ k a b a b a j a n |
| swswsw | dictionary | /swswsws/ | ▁ ɛ s d ə b ə l ̴ j u ɛ s d ə b ə l ̴ j u ɛ s d ə b ə l ̴ j  |
| start | english | /ˈstɑɹt/ | ▁ t a ŋ k a j |
| sro | rule | /ˈsɾo/ | ▁ ɛ s ɑ ɹ o ʊ |
| sr | spelled | /ʔesˈʔaɾ/ | ▁ s i n j o r |
| siy | dictionary | /si/ | ▁ s j a |
| sitsâ | rule | /siˈtʃaʔ/ | ▁ s e ɛ t s a |
| seq | rule | /ˈsek/ | ▁ s ɯ k j ɑ p |
| sept | english | /ˈsɛpt/ | ▁ s e p t i e m b ɾ ə |
| sea | english | /ˈsi/ | ▁ s ɛ j ə |
| say | english | /ˈseɪ/ | ▁ a l a j |
| sandá-sandalî | hyphenated | /sandasandaˈliʔ/ | ▁ s a n d ə s a n d ə l ̴ i s æ n d a s a n d ə l ̴ i |
| salí-salimuót | hyphenated | /salisalimuˈʔot/ | ▁ s a l i s a l i m u ɔ t s a l i s a l i m u o t |
| ref | english | /ˈɹɛf/ | ▁ r ə f ɾ e n |
| quay | english | /ˈki/ | ▁ k w ɛ j |
| pyre | rule | /ˈpiɾe/ | ▁ b a ɪ ɜ ˞ i |
| pta | rule | /ˈpta/ | ▁ p i t i e |
| prof | rule | /ˈpɾof/ | ▁ p r o f ɛ s o r |
| plo | rule | /ˈplo/ | ▁ b e l ̴ o l ̴ |
| pew | english | /ˈpju/ | ▁ v i w |
| paying | rule | /ˈpajiŋ/ | ▁ b a i n ə m |
| paundá-undá | hyphenated | /paʔundaʔunˈda/ | ▁ p a u n d a u n d a p ə ɾ u n d ə u n d a |
| pasiwaláng-bahalà | hyphenated | /pasiwaˈlaŋbahalaʔ/ | ▁ p a ː s i w a ː l a ŋ b a ː h a ː l a p a s i w a l a ŋ b  |
| papag-anyuín | hyphenated | /papaɡʔanjuˈʔin/ | ▁ p a p a g a n j u ɪ n p a p ə g a ɲ u ɪ n |
| pantíng-pansabaló | hyphenated | /pantiŋpansabaˈlo/ | ▁ p ə n t i ŋ p a n s a b a l o p ə n t i ŋ p ə n s a b ə l  |
| paiwà | dictionary | /paˈʔiwaʔ/ | ▁ b a ɪ j u w ɔ t |
| pagpirá-pirasuhín | hyphenated | /paɡpiɾapiɾasuˈhin/ | ▁ p a g p i r a p i r a s u h i n p a g p i r a p i r a s u  |
| pagpapamalí-mali | hyphenated | /paɡpapamaˈlimali/ | ▁ p a p a m a m a l i m a l i p a g p a p a m a m a l i m a  |
| page | dictionary | /ˈpaɡe/ | ▁ p a ː h i n a |
| pagbagú-baguhin | hyphenated | /paɡbaˈɡubaɡuhin/ | ▁ p a k b a g u b a g u h i n p a k b a g u b a g u h i n |
| pag-aksayahán | hyphenated | /paɡʔaksajaˈhan/ | ▁ p a g a k s a j a h h a n p a g a k s a j a h a n |
| oò | dictionary | /ˈʔoʔoʔ/ | ▁ u u |
| oá | rule | /ʔoˈʔa/ | ▁ ə w a |
| ow | english | /ˈoʊ/ | ▁ ə w i ʃ |
| op | english | /ˈɑp/ | ▁ t o p |
| ooo | dictionary | /ʔoˈʔoʔo/ | ▁ i ŋ |
| oo- | hyphenated | /ˈʔoʔo/ | ▁ u u |
| oo | dictionary | /ˈʔoʔo/ | ▁ ɛ e |
| onion | english | /ˈʌnjən/ | ▁ s i b u j a s |
| om | english | /ˈɔm/ | ▁ o m k o d |
| ol | rule | /ˈʔol/ | ▁ u l l æ t |
| ofw | rule | /ˈʔofw/ | ▁ o ʊ ɛ f d ə b ə l ̴ j u |
| oe | rule | /ˈʔoʔe/ | ▁ ɔ w i |
| ocw | rule | /ˈʔokw/ | ▁ o ʊ s i d ə b ə l ̴ j u |
| oct- | hyphenated | /ˈɔkt/ | ▁ o q t u b r e |
| oct | english | /ˈɔkt/ | ▁ o q t u b r e |
| ob-gyn | hyphenated | /ˈʔobɡin/ | ▁ o b i d ʒ i w a ɛ n |
| oar | english | /ˈɔɹ/ | ▁ u a ɾ |
| ngóy-ngoy | hyphenated | /ˈŋojŋoj/ | ▁ ŋ ɔ ɪ ɛ n d ʒ i o ʊ w a ɪ |
| ngohód | rule | /ŋoˈhod/ | ▁ n u ɔ ʎ |
| ngo | dictionary | /ˈŋo/ | ▁ e n ʒ i ɔ |
| ngets | rule | /ˈŋetʃ/ | ▁ ɲ ɛ t s |
| new | english | /ˈnu/ | ▁ n u n ɛ w |
| neutral | rule | /neˈʔutɾal/ | ▁ r i d ə l ̴ a ʊ d |
| napakadi-makatarungan | hyphenated | /napakadimakataˈɾuŋan/ | ▁ n a p a k a d i m a k a t a ɾ u ŋ a n n a p a k a d i m a  |
| mug | english | /ˈmʌɡ/ | ▁ m u b g a |
| mt | spelled | /ʔemˈti/ | ▁ m ɔ w n t |
| mr | spelled | /ʔemˈʔaɾ/ | ▁ m i s t r |
| mfa | rule | /ˈmfa/ | ▁ ɛ m ɛ f e |
| meil | rule | /ˈmeʔil/ | ▁ m a j l i n |
| mdma | rule | /ˈmdma/ | ▁ ɛ m d i e m e |
| mba | rule | /ˈmba/ | ▁ ɛ m b ɛ e |
| matamís-tamís | hyphenated | /matamistaˈmis/ | ▁ m a t a m i s t a m i s m a t ə m i s t a m i s |
| manun | rule | /ˈmanun/ | ▁ m a n o n u l l a t |
| male | english | /ˈmeɪl/ | ▁ r i l a b |
| makipag-unawaán | hyphenated | /makipaɡʔunawaˈʔan/ | ▁ m a k i p a g u n a w a a n m a k i p a g u n a w a a n |
| maghalu-halò | hyphenated | /maɡhaluˈhaloʔ/ | ▁ m a g h a l u h a l o m a g h a l o h a l o |
| mag-alinlangan | hyphenated | /maɡʔalinˈlaŋan/ | ▁ m a g a l i n l a m a n m a g a l i n l a ŋ a n |
| maasím-asím | hyphenated | /maʔasimʔaˈsim/ | ▁ m a ə s i m ə s i m m ə ə s i m ə s i m |
| lû | rule | /ˈluʔ/ | ▁ ɛ l o |
| liklík | rule | /liˈklik/ | ▁ l e a g e l e a g e |
| like | english | /ˈlaɪk/ | ▁ b a q a j |
| lgi | rule | /ˈlɡi/ | ▁ e l ʒ i a |
| letter | english | /ˈlɛtɚ/ | ▁ s ɑ b ɑ q |
| lb | spelled | /ʔelˈbi/ | ▁ p a ʊ n d |
| kutí-kutiltilín | hyphenated | /kutikutiltiˈlin/ | ▁ k u t i k u t i l t i l i n k u t i k u t i l t i l i n |
| kmi | rule | /ˈkmi/ | ▁ k i ɛ m a j |
| kawaláng-katarungan | hyphenated | /kawaˈlaŋkataɾuŋan/ | ▁ k a w a ː l a ŋ k a t a r u ŋ a n k a w a l a ŋ k a t a r  |
| kaul | english | /ˈkɔl/ | ▁ k a u l o g |
| karaniwang-karaniwan | hyphenated | /kaɾaniwaŋkaɾaˈniwan/ | ▁ k a r a n i w a ŋ k a r a n i w a ŋ k a r a n i w a ŋ k a  |
| kalí-kalibumbón | hyphenated | /kalikalibumˈbon/ | ▁ k a l i k a l i b o m b o n k a l i k a l i b u m b o n k  |
| kalá | rule | /kaˈla/ | ▁ k a l a a j o n |
| june | dictionary | /ˈdʒun/ | ▁ x u ɲ j o |
| ir | rule | /ˈʔiɾ/ | ▁ i r a w |
| ip | dictionary | /ˈʔip/ | ▁ i p o p |
| ino | rule | /ˈʔino/ | ▁ i n u p u |
| imf | rule | /ˈʔimf/ | ▁ a j ɛ m ɛ f |
| ikul | rule | /ˈʔikul/ | ▁ i l l u k o l |
| idipá | rule | /ʔidiˈpa/ | ▁ i l ɛ n ɛ s t p a |
| icbm | rule | /ˈʔikbm/ | ▁ a ɪ s i b i ɛ m |
| ibp | rule | /ˈʔibp/ | ▁ a ɪ b i p i |
| hî | rule | /ˈhiʔ/ | ▁ ɕ i n |
| huhu | dictionary | /ˈhuhu/ | ▁ h i f i t |
| hi- | hyphenated | /hi/ | ▁ h a j |
| here | english | /ˈhiɹ/ | ▁ s a b i |
| gut | english | /ˈɡʌt/ | ▁ g u t u m |
| gpu | rule | /ˈɡpu/ | ▁ d ʒ i p i j u |
| gnu | english | /ˈnu/ | ▁ d ʒ i ɛ n d j u |
| giyc | rule | /ˈɡijk/ | ▁ g i a ɪ w a ɪ s i |
| gg | spelled | /dʒiˈdʒi/ | ▁ g a |
| ge | dictionary | /ˈɡe/ | ▁ d ʒ ɛ j |
| eyyy | dictionary | /ˈʔej/ | ▁ e j a j j a j |
| ewer | english | /ˈjuɚ/ | ▁ ɛ w a |
| ewe | english | /ˈju/ | ▁ ɛ w e |
| ets | dictionary | /ˈʔetʃ/ | ▁ ɛ t s |
| esp | rule | /ˈʔesp/ | ▁ ɛ s p e ʃ a l i |
| esau | english | /ˈiˌsɔ/ | ▁ e s s a w |
| er | english | /ɚ/ | ▁ ɯ ð |
| eon | english | /ˈiən/ | ▁ e j ɔ n |
| egg | english | /ˈɛɡ/ | ▁ ɪ t l ̴ o g |
| ef | dictionary | /ʔef/ | ▁ e s s ɛ k |
| ecg | rule | /ˈʔekɡ/ | ▁ i s i ʒ i |
| dyi | dictionary | /dji/ | ▁ d i w a ɪ a ɪ |
| dy | dictionary | /ˈdi/ | ▁ d ɾ a j |
| dues | english | /ˈduz/ | ▁ d u w e s |
| due | english | /ˈdu/ | ▁ d u p u |
| dr | spelled | /diˈʔaɾ/ | ▁ d o q t o r |
| diyuditso | rule | /dijuˈditʃo/ | ▁ d ʒ u d ʒ i t t s u |
| dipag-iintindí | hyphenated | /dipaɡʔiʔintinˈdi/ | ▁ d i p a g i i n t i n d i d i p ə g i i n t i n d ̪ i |
| di-mapagtitiwalaan | hyphenated | /dimapaɡtitiwaˈlaʔan/ | ▁ d i m ə p a g t i t i w a l a a n d i m a p ə ŋ t i t i w  |
| di-malulusután | hyphenated | /dimalulusuˈtan/ | ▁ d i m a l u l u s u t a n d i m a l u l u s u t a n |
| di-karamihan | hyphenated | /dikaɾaˈmihan/ | ▁ d i k a r a m i h a n d i k a r a m i h a n |
| dew | english | /ˈdu/ | ▁ d e w a |
| daub | english | /ˈdɔb/ | ▁ d a u b a |
| cpa | rule | /ˈkpa/ | ▁ s i p i e |
| cno | rule | /ˈkno/ | ▁ s i ɛ n o ʊ |
| chiu | dictionary | /ˈtʃu/ | ▁ t ʃ i j u |
| ch | dictionary | /ˈtʃe/ | ▁ s i |
| c- | hyphenated | /ˈsi/ | ▁ k a t i b |
| bô | rule | /ˈboʔ/ | ▁ b u u |
| bâ | dictionary | /ˈbaʔ/ | ▁ v a u n |
| buyuboy | rule | /buˈjuboj/ | ▁ b u u u n ʲ ɛ s k ɭ d v ɑ j ɛ b o j |
| buoy | english | /ˈbui/ | ▁ b o ɔ j |
| buk | rule | /ˈbuk/ | ▁ v u k o d |
| be | dictionary | /ˈbe/ | ▁ v i |
| bb | spelled | /biˈbi/ | ▁ v a |
| balungkalíng | rule | /baluŋkaˈliŋ/ | ▁ b a l u ŋ k a l i ŋ b a l u ŋ k a l i ŋ |
| ave | rule | /ˈʔave/ | ▁ a v e n ɲ u u |
| av | english | /ˌeɪˈvi/ | ▁ a v n u |
| audio | english | /ˈɑdiˌoʊ/ | ▁ i s u g a t |
| aliwíw | rule | /ʔaliˈwiw/ | ▁ ɑ ɭ ɛ u n ʲ ɛ k ɭ a d ɔ v j ɛ |
| ahá | dictionary | /ʔaˈha/ | ▁ æ ʃ ʃ ɑ r |
| aging | rule | /ˈʔaɡiŋ/ | ▁ e j d ʒ i n |
| age | english | /ˈeɪdʒ/ | ▁ a ː h e |
| ae | rule | /ˈʔaʔe/ | ▁ e j |
| ado | rule | /ˈʔado/ | ▁ ɑ d o b u w |
| adieu | english | /əˈdu/ | ▁ e ɪ d j u |
| add | spelled | /ʔeidiˈdi/ | ▁ a n |
| ac | english | /ˌeɪˈsi/ | ▁ a s i n g |
| Puig | dictionary | /ˈputʃ/ | ▁ p ɔ j g |
| Cebú | dictionary | /seˈbu/ | ▁ s e ɛ s t b o |
| -y | hyphenated | /ˈwaɪ/ | ▁ j ɔ |
| -s | hyphenated | /ˈʔes/ | ▁ s a |
| -o | hyphenated | /ˈʔo/ | ▁ t o |
| -ng- | hyphenated | /ŋ/ | ▁ n a ŋ |
| -n- | hyphenated | /n/ | ▁ n a |
| -m- | hyphenated | /m/ | ▁ m i |
| -id | hyphenated | /ˈʔid/ | ▁ i b i |
| -ic | hyphenated | /ˈʔik/ | ▁ p i s i |
| -g- | hyphenated | /ˈdʒi/ | ▁ g a |

## zipa: the 15 clips it disagrees with most

| Form | Category | IPA | Heard |
|---|---|---|---|
| ywca | rule | /ˈʔiwka/ | ▁ w a ɪ d ə b ə l ̴ j u s i e ɪ |
| ymca | rule | /ˈʔimka/ | ▁ w a ɛ m s i e j |
| yehey | dictionary | /ˈjehej/ | ▁ ɪ æ ɪ h æ ɪ |
| xi | english | /ˈʃi/ | ▁ ʃ a m |
| word | english | /ˈwɝd/ | ▁ s i n a b i |
| wong | dictionary | /ˈwoŋ/ | ▁ v ɛ n |
| wi-fi | hyphenated | /ˈwifi/ | ▁ w a j f a j |
| wed | english | /ˈwɛd/ | ▁ w ɛ n s d a j |
| we | english | /ˈwi/ | ▁ u w ɛ |
| waláng-konsiderasyón | hyphenated | /walaŋkonsideɾasˈjon/ | ▁ w a l a ŋ k o n s i d e ɾ a s o n w a l a ŋ k o n s i d e ɾ a s i o n |
| waláng-kakanin | hyphenated | /waˈlaŋkakanin/ | ▁ w a ː l a ŋ k ʰ a k ʰ a n i n w a l a ŋ k ʰ a ː k ʰ a ː n i n |
| wa | dictionary | /wa/ | ▁ h u w a |
| vs | spelled | /viˈʔes/ | ▁ v ɜ r s ə s |
| vol | rule | /ˈvol/ | ▁ v ɔ l j u m |
| vip | rule | /ˈvip/ | ▁ v i a ɪ p i |
