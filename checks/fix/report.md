# Clip fixes

Clips re-synthesized by `scripts/fix_clips.py` from `checks/fix/redo.tsv` (`scripts/make_fix_list.py`). Each try is checked with ZIPA against the IPA; a clip is replaced only when a try is complete and clearly better (error at most 40% and at least 10% lower than before). `results.tsv` has every try.

3995 clips done, 5089 tries.

| Reason | Replaced | Old clip kept |
|---|---:|---:|
| english | 2582 | 38 |
| hyphen | 1033 | 5 |
| letters | 107 | 0 |
| cut | 94 | 7 |
| again | 63 | 29 |
| repeat | 33 | 0 |
| extra | 3 | 1 |
| **all** | 3915 | 80 |

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
| aatoato | repeat | aatoato | a t o a t o | 0.43 → 0.14 |
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

## Old clip kept: no try was good enough (all)

| Form | Reason | Sent | Heard | Error before → after |
|---|---|---|---|---|
| director | english | director | d ɪ ɹ ɛ k t ɜ ˞ | 0.25 → 0.25 |
| ow | again | "ow" | a ʊ | 1.00 → 0.50 |
| color | english | color | k ɔ l ̴ ɜ ˞ | 0.40 → 0.40 |
| junk | again | junk | d ʒ ɛ n k | 0.50 → 0.50 |
| jump | english | jump | d ʒ u m p | 0.25 → 0.25 |
| ave | again | ave | æ v ə n u | 1.00 → 0.75 |
| valiente | english | valiente | v a l ɛ n t | 0.29 → 0.29 |
| moderate | again | moderate | m ɑ d ɜ ˞ e ɪ t | 0.29 → 0.29 |
| fe | english | fe | f i | 0.33 → 0.33 |
| glow | english | glow | g l ̴ o w | 0.25 → 0.25 |
| chase | again | chase | t ʃ a s e | 0.75 → 0.75 |
| oct | english | oct | ɑ k t o ʊ b ɜ ˞ | 1.00 → 1.00 |
| blow | english | blow | b l ̴ o ʊ w | 0.25 → 0.25 |
| separate | again | separate | s ɛ p ɹ ə t | 0.38 → 0.38 |
| merced | english | merced | m ɜ ˞ s ɛ d | 0.40 → 0.60 |
| heterosexual | english | heterosexual | h ɛ t ɜ ˞ o ʊ s ɛ k ʃ u ə l ̴ | 0.27 → 0.20 |
| ishmael | english | ishmael | e ʃ m e j ɛ l | 0.60 → 0.80 |
| knesset | english | knesset | k n ɛ s ɪ t | 0.40 → 0.40 |
| collar | english | collar | k ɔ l ̴ ɜ ˞ | 0.40 → 0.40 |
| quay | again | quay | k w e ɪ | 1.00 → 1.00 |
| uranus | again | uranus | j u r e ɪ n ə s | 0.29 → 0.29 |
| skier | again | skier | s k i ɜ r | 0.40 → 0.40 |
| velociraptor | english | velociraptor | ð ə l ̴ ɔ s ɜ ɹ æ p t ɜ ˞ | 0.25 → 0.25 |
| somatic | english | somatic | s ə m æ t ɪ k | 0.25 → 0.25 |
| vie | again | vie | v i | 0.67 → 0.33 |
| teleprompter | english | teleprompter | t ɛ l ̴ e ɪ p ɹ ɑ m p t ɜ ˞ | 0.25 → 0.25 |
| cavan | english | cavan | k æ v ə n | 0.33 → 0.33 |
| bolognese | english | bolognese | b o ʊ l ̴ ɪ n j e z | 0.58 → 0.50 |
| bicarbonate | again | bicarbonate | b a ɪ k ɑ ɹ b ə n e ɪ t | 0.27 → 0.18 |
| cation | again | cation | k e ɪ ʃ ə n | 0.57 → 0.57 |
| catsup | again | catsup | k æ t s ə p | 0.80 → 0.60 |
| spurious | english | spurious | s p ɪ ɹ i ə s | 0.25 → 0.25 |
| atheism | again | atheism | e θ i ɪ z ə m | 0.57 → 0.43 |
| bronchial | again | "bronchial" | b r ɔ n k i l | 0.38 → 0.38 |
| búhosutang | cut | búhosutang | b u h o s | 0.44 → 0.44 |
| buladbukad | cut | buladbukad | b u l a d | 0.50 → 0.50 |
| caban | english | caban | k æ b ə n | 0.33 → 0.33 |
| cadena-de-amor | english | cadena de amor | k ə d i n ə ə v e ɪ m ɔ ɹ | 0.25 → 0.42 |
| calan | english | calan | k æ l ̴ ə n | 0.33 → 0.33 |
| chalcedony | again | chalcedony | k æ l ̴ s ɛ d ə n i | 0.40 → 0.40 |
| cognoscenti | english | cognoscenti | k ɑ g n ə s ɛ n t i | 0.30 → 0.20 |
| dyukaka | again | dyukaka | d ʒ u q a | 0.57 → 0.57 |
| elaborate | again | elaborate | ɪ l ̴ æ b ɜ ˞ e ɪ t | 0.43 → 0.43 |
| hawsyaw | again | hawsyaw | a w ʃ a w | 0.71 → 0.43 |
| ib-ib | hyphen | ib ib | i b | 0.50 → 0.50 |
| ire-ref | hyphen | ire ref | a ɪ ɜ r | 0.50 → 0.50 |
| iyonout | cut | iyonout | i j o n | 0.43 → 0.43 |
| k-dye | again | K J | k e d ʒ e | 0.83 → 0.33 |
| ligaw-insfk | hyphen | ligawinsfk | l i g a w i n | 0.50 → 0.30 |
| lobotomy | again | lobotomy | l ̴ ə b ɑ t ə m i | 0.27 → 0.55 |
| magin- | english | magin | m æ g ə n | 0.40 → 0.40 |
| masseur | cut | masseur | m ə s ɜ ˞ | 0.43 → 0.43 |
| milon-tagalog | hyphen | milon tagalog | m i l o n | 0.58 → 0.58 |
| myocardium | again | myocardium | m a ɪ o ʊ k ɑ ɹ d i ə m | 0.27 → 0.18 |
| plover | again | "plover" | p l ̴ o ʊ v ɜ ˞ | 0.33 → 0.33 |
| pot-pot | english | pot pot | p ɑ ɹ t p ɑ ɹ t | 0.33 → 0.33 |
| swswsw | extra | es dobolyu es dobolyu es dobolyu | e s d o v ə l v e e s d o b ə l v e e s d o v ə l  | 1.00 → 1.00 |
| puskar | english | puskar | p u s k ɑ ɹ | 0.33 → 0.33 |
| raisin | again | raisin | r a z o n | 0.50 → 0.50 |
| reseaux | cut | reseaux | r e s s o w | 0.62 → 0.62 |
| sleíght | cut | sleíght | s l e t | 0.43 → 0.43 |
| touche | english | touche | t u ʃ e ɪ | 0.67 → 0.67 |
| triage | again | triage | t ɹ i ɑ ʒ | 0.67 → 0.50 |
| wálang-mana | hyphen | wálang mana | w a l a ŋ | 0.44 → 0.44 |
| xero- | english | xero | ɛ k s r o ʊ | 0.40 → 0.60 |
| boy | again | boy | b o j | 0.33 → 0.33 |
| work | english | work | w ɔ r k | 0.25 → 0.25 |
| bank | english | bank | b ɛ ŋ k | 0.25 → 0.25 |
| golf | english | golf | g o l f | 0.25 → 0.25 |
| re | english | re | ɹ i | 0.33 → 0.33 |
| pulp | english | pulp | p o l p | 0.25 → 0.25 |
| grey | english | grey | g r a | 0.25 → 0.50 |
| karol | english | karol | k æ ɹ ə l ̴ | 0.40 → 0.40 |
| holen | english | holen | h o l ̴ ə n d | 0.33 → 0.33 |
| wart | english | wart | v ɔ r t | 0.25 → 0.25 |
| anemone | again | "anemone" | ə n ɛ m ə n i | 0.57 → 0.57 |
| Iyonout | again | Iyonout | i j o n | 0.43 → 0.43 |
| oeuvre | cut | oeuvre | ø v r ɛ | 0.67 → 0.33 |
| osmosis | english | osmosis | æ z m o ʊ s ə s | 0.25 → 0.25 |
| turbot | again | "turbot" | t ɜ ˞ b ɛ t | 0.33 → 0.33 |
