# Clip fixes

Clips re-synthesized by `scripts/fix_clips.py` from `checks/fix/redo.tsv` (`scripts/make_fix_list.py`). Each try is checked with ZIPA against the IPA; a clip is replaced only when a try is complete and clearly better (error at most 40% and at least 10% lower than before). `results.tsv` has every try.

3244 clips done, 3885 tries.

| Reason | Replaced | Old clip kept |
|---|---:|---:|
| english | 2126 | 83 |
| hyphen | 816 | 27 |
| cut | 70 | 25 |
| letters | 95 | 0 |
| extra | 2 | 0 |
| **all** | 3109 | 135 |

## Replaced (first 60)

| Form | Reason | Sent | Heard | Error before → after |
|---|---|---|---|---|
| of | english | of | ə v | 1.00 → 0.00 |
| national | english | national | n æ ʃ i ə n ə l ̴ | 0.43 → 0.14 |
| you | english | you | j u | 0.50 → 0.00 |
| office | english | office | ɔ f ɪ s | 0.75 → 0.00 |
| secretary | english | secretary | s ɛ k ɹ ə t ɛ ɹ i | 0.44 → 0.00 |
| first | english | first | f ɜ ˞ s t | 0.80 → 0.20 |
| international | english | international | ɪ n t ɜ ˞ n æ ʃ ə n ə l ̴ | 0.33 → 0.08 |
| public | english | public | p ə b l ̴ ɪ k | 0.33 → 0.00 |
| year | english | year | j i ɹ | 0.67 → 0.00 |
| detective | english | detective | d ɪ t ɛ k t ɪ v | 0.50 → 0.00 |
| music | english | music | m j u z i k | 0.50 → 0.00 |
| south | english | south | s a w θ | 0.75 → 0.25 |
| chinese | english | chinese | t ʃ a ɪ n i z | 0.67 → 0.00 |
| túluy-tuloy | hyphen | túluy tuloy | t u l o j t u l o j | 0.50 → 0.10 |
| ano-ano | hyphen | ano ano | ə n o ə n o | 0.50 → 0.00 |
| kámi-kami | hyphen | kámi kami | k a m i k a m i | 0.50 → 0.00 |
| sáan-saan | hyphen | sáan saan | s a ə n s a ə n | 0.50 → 0.00 |
| alas-kuwatro | hyphen | alas kuwatro | a l l a s k w a t r o | 0.64 → 0.18 |
| síno-sino | hyphen | síno sino | s i n o s i n o | 0.50 → 0.00 |
| ágad-agad | hyphen | ágad agad | ə g a d ə g a d | 0.50 → 0.00 |
| buwan-buwan | hyphen | buwan buwan | b u w a n b u w a n | 0.60 → 0.00 |
| gâwa-gawa | hyphen | gâwa gawa | g a w ə g a w ə | 0.50 → 0.00 |
| síla-sila | hyphen | síla sila | s i l a s i l a | 0.50 → 0.00 |
| hâka-haka | hyphen | hâka haka | h a k a h a k a | 0.50 → 0.00 |
| kalát-kalát | hyphen | kalát kalát | k ə l l a t k ə l l a t | 0.50 → 0.20 |
| sâri-sari | hyphen | sâri sari | s a ɾ i s a r i | 0.50 → 0.00 |
| líbo-libo | hyphen | líbo libo | l i b ɔ l i b ɔ | 0.50 → 0.00 |
| tabi-tabí | hyphen | tabi tabí | t ə b i t a b i | 0.50 → 0.00 |
| hiv | cut | hiv | e t ʃ a j v i | 0.57 → 0.29 |
| dalangin | cut | dalangin | ð ə l ̴ æ ŋ ɪ n | 1.00 → 0.00 |
| socio | cut | socio | s o ʊ s i o ʊ | 0.57 → 0.00 |
| hierarchy | cut | hierarchy | h a ɪ ɜ ˞ ɑ ɹ k i | 0.56 → 0.11 |
| pm | letters | pi em | p i ɛ m | 0.50 → 0.00 |
| kc | letters | key si | k i s i | 0.60 → 0.20 |
| sm | letters | es em | ɛ s ɛ m | 0.75 → 0.00 |
| lt | letters | el ti | ɛ l t i | 0.75 → 0.00 |
| bk | letters | bi key | b i k i | 0.80 → 0.20 |
| km | letters | key em | k i ɛ m | 0.80 → 0.20 |
| tumoy | extra | tumoy | t u m u j | 1.00 → 0.20 |
| face | english | face | f e ɪ s | 0.75 → 0.00 |
| cia | cut | cia | s i a ɪ e ɪ | 0.67 → 0.00 |
| áboábo | cut | ábo ábo | a b o a b o | 0.50 → 0.00 |
| power | english | power | p a ʊ ɜ ˞ | 0.60 → 0.20 |
| this | english | this | ð ɪ s | 1.00 → 0.00 |
| control | english | control | k ə n t ɹ o ʊ l ̴ | 0.25 → 0.00 |
| operation | english | operation | ɑ p ɜ ˞ e ɪ ʃ ə n | 0.67 → 0.11 |
| commission | english | commission | k ə m ɪ ʃ ə n | 0.43 → 0.00 |
| that | english | that | ð æ t | 0.67 → 0.00 |
| case | english | case | k e ɪ s | 0.75 → 0.00 |
| investigation | english | investigation | ɪ n v ɛ s t ə g e ɪ ʃ ə n | 0.31 → 0.00 |
| family | english | family | f æ m l ̴ i | 0.67 → 0.17 |
| region | english | region | r i d ʒ o n | 0.80 → 0.20 |
| club | english | club | k l ̴ ə b | 0.25 → 0.00 |
| american | english | american | ə m ɛ ɹ i k ə n | 0.25 → 0.12 |
| official | english | official | ə f ɪ ʃ ə l ̴ | 0.50 → 0.00 |
| your | english | your | j ɔ ɹ | 1.00 → 0.00 |
| association | english | association | ə s o ʊ s i e ɪ ʃ i ə n | 0.55 → 0.09 |
| life | english | life | l ̴ a ɪ f | 0.50 → 0.00 |
| please | english | please | p l ̴ i z | 1.00 → 0.00 |
| illegal | english | illegal | ɪ l ̴ i g ə l ̴ | 0.33 → 0.00 |

## Old clip kept: no try was good enough (all)

| Form | Reason | Sent | Heard | Error before → after |
|---|---|---|---|---|
| director | english | director | d ɪ ɹ ɛ k t ɜ ˞ | 0.25 → 0.25 |
| aatoato | cut | aatoato | a t o | 0.43 → 0.57 |
| text | english | text | p ɑ k | 1.00 → 0.80 |
| change | english | change | t ʃ a n d ʒ e | 0.60 → 0.60 |
| ow | english | ow | a o | 1.00 → 1.00 |
| graduate | english | graduate | g ɹ æ d ʒ u w e ɪ t | 0.38 → 0.38 |
| surgery | english | surgery | s ɜ ˞ d ʒ ɜ ˞ i | 0.71 → 0.29 |
| color | english | color | k ɔ l ̴ ɜ ˞ | 0.40 → 0.40 |
| junk | english | junk | d ʒ ɛ n k | 0.50 → 0.50 |
| xi | english | xi | z i ː | 1.00 → 0.50 |
| jump | english | jump | d ʒ u m p | 0.25 → 0.25 |
| instruction | english | instruction | l ̴ ɔ ɹ ə l ̴ | 0.80 → 0.80 |
| aviation | english | aviation | a ɪ v i a ɪ t i o n | 0.67 → 0.56 |
| thy | english | ti eych way | t i e ɪ t ʃ w e ɪ | 0.67 → 1.00 |
| av | english | av | a v | 1.00 → 0.75 |
| ave | english | ave | æ v ə n u | 1.00 → 0.75 |
| valiente | english | valiente | v a l ɛ n t | 0.29 → 0.29 |
| moderate | english | moderate | m ɑ d ɜ ˞ e ɪ t | 0.29 → 0.29 |
| fe | english | fe | f i | 0.33 → 0.33 |
| cha-cha | hyphen | cha cha | t ʃ ɑ | 0.50 → 0.50 |
| glow | english | glow | g l ̴ o w | 0.25 → 0.25 |
| chase | english | chase | t ʃ a s e | 0.75 → 0.75 |
| egyptian | english | egyptian | e d ʒ i p t j o n | 0.71 → 0.57 |
| generator | english | generator | d ʒ ɛ n ɜ ˞ e ɪ t ɜ ˞ | 0.30 → 0.20 |
| ac | english | ac | a s i | 1.00 → 0.50 |
| null | english | null | n o | 0.67 → 0.67 |
| oct | english | oct | ɑ k t o ʊ b ɜ ˞ | 1.00 → 1.00 |
| blow | english | blow | b l ̴ o ʊ w | 0.25 → 0.25 |
| refrigerator | english | refrigerator | ɹ ɛ f ɹ ɪ d ʒ ɜ ˞ e ɪ t ɜ ˞ | 0.31 → 0.23 |
| separate | english | separate | s ɛ p ɹ ə t | 0.38 → 0.38 |
| merced | english | merced | m ɜ ˞ s ɛ d | 0.40 → 0.60 |
| heterosexual | english | heterosexual | h ɛ t ɜ ˞ o ʊ s ɛ k ʃ u ə l ̴ | 0.27 → 0.20 |
| isthmus | english | isthmus | ɪ θ s m ɪ s | 0.40 → 0.40 |
| ishmael | english | ishmael | e ʃ m e j ɛ l | 0.60 → 0.80 |
| catheter | english | catheter | k æ θ ə d ɜ ˞ | 0.29 → 0.29 |
| transcription | english | transcription | d ʒ a s o n | 0.83 → 0.75 |
| context | english | context | k ɑ n s ɔ ɹ t | 0.62 → 0.50 |
| mace | english | mace | m a s | 0.75 → 0.50 |
| adjourn | english | adjourn | e ɪ d ʒ ɜ ˞ n | 0.80 → 0.60 |
| knesset | english | knesset | k n ɛ s ɪ t | 0.40 → 0.40 |
| gg | cut | G G | d ʒ i d ʒ i | 1.00 → 0.67 |
| pandanus | english | pandanus | p ɛ n d æ n ə s | 0.33 → 0.33 |
| collar | english | collar | k ɔ l ̴ ɜ ˞ | 0.40 → 0.40 |
| quay | english | quay | k w e ɪ | 1.00 → 1.00 |
| uranus | english | uranus | j u r e ɪ n ə s | 0.29 → 0.29 |
| skier | english | skier | s k i ɜ r | 0.40 → 0.40 |
| velociraptor | english | velociraptor | ð ə l ̴ ɔ s ɜ ɹ æ p t ɜ ˞ | 0.25 → 0.25 |
| somatic | english | somatic | s ə m æ t ɪ k | 0.25 → 0.25 |
| cursor | english | cursor | k ɜ ˞ s ɜ ˞ | 0.33 → 0.33 |
| vie | english | vie | v i | 0.67 → 0.33 |
| teleprompter | english | teleprompter | t ɛ l ̴ e ɪ p ɹ ɑ m p t ɜ ˞ | 0.25 → 0.25 |
| progenitor | english | progenitor | p ɹ o ʊ d ʒ ɛ n ə t ɜ ˞ | 0.27 → 0.18 |
| cavan | english | cavan | k æ v ə n | 0.33 → 0.33 |
| bolognese | english | bolognese | b o ʊ l ̴ ɪ n j e z | 0.58 → 0.50 |
| bicarbonate | english | bicarbonate | b a ɪ k ɑ ɹ b ə n e ɪ t | 0.27 → 0.18 |
| cation | english | cation | k e ɪ ʃ ə n | 0.57 → 0.57 |
| empiricism | english | empiricism | ɪ m p ɪ ɹ i ɪ s ɪ z ə m | 0.36 → 0.27 |
| catsup | english | catsup | k æ t s ə p | 0.80 → 0.60 |
| spurious | english | spurious | s p ɪ ɹ i ə s | 0.25 → 0.25 |
| atheism | english | atheism | e θ i ɪ z ə m | 0.57 → 0.43 |
| angkátangkáyan | cut | angkátangkáyan | ə ŋ k a t | 0.58 → 0.58 |
| áni-ani | hyphen | áni ani | a n i | 0.50 → 0.50 |
| asa-asa | hyphen | asa asa | ə s a | 0.50 → 0.50 |
| bahaw-bahaw | hyphen | bahaw bahaw | b ə a b ə a w | 0.60 → 0.30 |
| bald-bala | hyphen | bald bala | b ɔ l d | 0.62 → 0.50 |
| basar-basar | hyphen | basar basar | v a s a r a b | 0.50 → 0.50 |
| básugbásog | cut | básugbásog | b a s o g | 0.50 → 0.50 |
| bronchial | english | bronchial | b r ɔ ŋ k i l | 0.38 → 0.50 |
| búhosutang | cut | búhosutang | b u h o s | 0.44 → 0.44 |
| buladbukad | cut | buladbukad | b u l a d | 0.50 → 0.50 |
| bumpers | english | bumpers | b u m p e r s | 0.29 → 0.29 |
| caban | english | caban | k æ b ə n | 0.33 → 0.33 |
| cadena-de-amor | english | cadena de amor | k ə d i n ə ə v e ɪ m ɔ ɹ | 0.25 → 0.42 |
| calan | english | calan | k æ l ̴ ə n | 0.33 → 0.33 |
| chalcedony | english | chalcedony | k æ l ̴ s ɛ d ə n i | 0.40 → 0.40 |
| cognoscenti | english | cognoscenti | k ɑ g n ə s ɛ n t i | 0.30 → 0.20 |
| debase | english | debase | d e b a s | 0.67 → 0.50 |
| dugo-q | hyphen | dugo q | d u g o ʊ | 0.50 → 0.38 |
| duodenum | english | duodenum | d u o ʊ d i n ə m | 0.38 → 0.38 |
| dyukaka | cut | dyukaka | d ʒ u q a | 0.57 → 0.57 |
| egotist | english | egotist | i g o ʊ t ɪ s t | 0.29 → 0.29 |
| elaborate | english | elaborate | ɪ l ̴ æ b ɜ ˞ e ɪ t | 0.43 → 0.43 |
| gaga-go | hyphen | gaga go | g a g a | 0.43 → 0.43 |
| gamotlahat | cut | gamotlahat | g ə m o t | 0.50 → 0.50 |
| grádo-grado | hyphen | grádo grado | g r a d o | 0.50 → 0.50 |
| hákbang-hakbang | hyphen | hákbang hakbang | h a k b a ŋ | 0.50 → 0.50 |
| hawsyaw | cut | hawsyaw | a w ʃ a w | 0.71 → 0.43 |
| híging-higing | hyphen | híging higing | h i g i ŋ | 0.50 → 0.50 |
| ib-ib | hyphen | ib ib | i b | 0.50 → 0.50 |
| igat-igat | hyphen | igat igat | i g a t | 0.50 → 0.50 |
| indeterminate | english | indeterminate | ɪ n d ɪ t ɜ ˞ m ə n e ɪ t | 0.33 → 0.25 |
| ire-ref | hyphen | ire ref | a ɪ ɜ r | 0.50 → 0.50 |
| iyonout | cut | iyonout | i j o n | 0.43 → 0.43 |
| k-dye | hyphen | kdye | k a d i e | 0.75 → 0.50 |
| kaxnote | cut | kaxnote | k æ s a | 0.50 → 0.62 |
| legerdemain | english | legerdemain | l ̴ ɛ d ʒ ɜ ˞ d o ʊ m e ɪ n | 0.36 → 0.27 |
| ligaw-insfk | hyphen | ligawinsfk | l i g a w i n | 0.50 → 0.30 |
| liquidator | english | liquidator | l ̴ ɪ k w ə d e ɪ t ɜ ˞ | 0.27 → 0.18 |
| lobotomy | english | lobotomy | l ̴ ə b ɑ t ə m i | 0.27 → 0.55 |
| lukis'lukis | cut | lukis'lukis | l u k i s | 0.50 → 0.50 |
| mágaling-galing | hyphen | mágaling galing | m a g a l i ŋ | 0.42 → 0.42 |
| magin- | english | magin | m æ g ə n | 0.40 → 0.40 |
| makesyu-kesyo | hyphen | makesyu kesyo | m ɛ k s j u w k ɛ ʃ ɔ | 0.75 → 0.42 |
| masagwásagwà | cut | masagwásagwà | m a s a g w w a | 0.42 → 0.33 |
| masiglángmasigla | cut | masiglángmasigla | m a s i g l a ŋ | 0.47 → 0.47 |
| masseur | cut | masseur | m ə s ɜ ˞ | 0.43 → 0.43 |
| miliwpiliw | cut | miliwpiliw | m i l i w i | 0.60 → 0.40 |
| milon-tagalog | hyphen | milon tagalog | m i l o n | 0.58 → 0.58 |
| mulanbulan | cut | mulanbulan | m u l l a n | 0.50 → 0.40 |
| myocardium | english | myocardium | m a ɪ o ʊ k ɑ ɹ d i ə m | 0.27 → 0.18 |
| óban-óban | hyphen | óban óban | o b a n | 0.50 → 0.50 |
| oct- | english | oct | ɑ k t o ʊ b ɜ ˞ | 1.00 → 1.00 |
| oligocene | english | oligocene | ɔ l ̴ ɪ g ə s i n | 0.44 → 0.44 |
| omnivorous | english | omnivorous | a ɪ ɛ m n ɪ v ɜ ˞ ə s | 0.33 → 0.33 |
| oppressor | english | oppressor | e ɪ p ɹ ɛ s ɜ ˞ | 0.43 → 0.43 |
| orig-orig | hyphen | orig orig | ɔ r i n g | 0.50 → 0.50 |
| pares-pares | hyphen | pares pares | p a ː r e s | 0.60 → 0.50 |
| páris-paris | hyphen | páris paris | p a r i s | 0.50 → 0.50 |
| pilítpilitin | cut | pilítpilitin | p i l i t i n | 0.42 → 0.42 |
| piliwpiliwan | cut | piliwpiliwan | p i l i w a n | 0.42 → 0.42 |
| plover | english | plover | p l ̴ o ʊ v ɜ ˞ | 0.50 → 0.50 |
| polemic | english | polemic | p o ʊ l ̴ ɛ m ɪ k | 0.29 → 0.29 |
| pot-pot | english | pot pot | p ɑ ɹ t p ɑ ɹ t | 0.33 → 0.33 |
| puskar | english | puskar | p u s k ɑ ɹ | 0.33 → 0.33 |
| raisin | english | raisin | r a z o n | 0.50 → 0.50 |
| rásyun-rasyon | hyphen | rásyun rasyon | ɾ a s i o n r a s i o n | 0.50 → 0.50 |
| rayúsrayos | cut | rayúsrayos | r a j u s | 0.50 → 0.50 |
| reseaux | cut | reseaux | r e s s o w | 0.62 → 0.62 |
| sálop-salop | hyphen | sálop salop | s a l o p | 0.60 → 0.50 |
| sammisammimi | cut | sammisammimi | s a m i s a m i | 0.67 → 0.33 |
| sibuyastagalog | cut | sibuyastagalog | s i b u j a s | 0.50 → 0.50 |
| sleíght | cut | sleíght | s l e t | 0.43 → 0.43 |
| sumaldáksaldak | cut | sumaldáksaldak | s u m æ l d ɑ q | 0.57 → 0.43 |
| súson-suson | hyphen | súson suson | s u s o n | 0.50 → 0.50 |
| táha-táha | hyphen | táha táha | t a x a | 0.50 → 0.50 |
