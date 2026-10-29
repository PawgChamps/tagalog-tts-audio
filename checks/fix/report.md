# Clip fixes

Clips re-synthesized by `scripts/fix_clips.py` from `checks/fix/redo.tsv` (`scripts/make_fix_list.py`). Each try is checked with ZIPA against the IPA; a clip is replaced only when a try is complete and clearly better (error at most 40% and at least 10% lower than before). `results.tsv` has every try.

48 clips done, 65 tries.

| Reason | Replaced | Old clip kept |
|---|---:|---:|
| english | 14 | 1 |
| hyphen | 15 | 0 |
| cut | 6 | 2 |
| letters | 6 | 2 |
| extra | 1 | 1 |
| **all** | 42 | 6 |

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

## Old clip kept: no try was good enough (all)

| Form | Reason | Sent | Heard | Error before → after |
|---|---|---|---|---|
| director | english | director | d ɪ ɹ ɛ k t ɜ ˞ | 0.25 → 0.25 |
| gg | cut | gg | g i | 1.00 → 0.83 |
| aatoato | cut | aatoato | a t o | 0.43 → 0.57 |
| sc | letters | es si | e s | 0.75 → 0.50 |
| mg | letters | em dyi | ɛ m d i w a ɪ a ɪ | 0.50 → 1.00 |
| input | extra | input | m a n a g a s | 1.00 → 1.00 |
