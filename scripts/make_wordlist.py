#!/usr/bin/env python3
"""Accented spellings for text-to-speech, most frequent words first. One line per reading of a single-word headword:
the accent marks of the Ortograpiyang Pambansa (acute = stress off the penult, grave = penult stress + final glottal,
circumflex = final stress + final glottal, no mark = penult stress). Usage: make_wordlist.py <published json> --top 20000
--out audio/wordlist_top20k.tsv (--top 0 = every spelling). Needs tagalog_orthography and tagalog_phonetics_baybayin from
"Project TGL to PRT-BR/Scripts" (on the path, or this file in Scripts/audio), and the KWF and UP source files (--kwf,
--dfe, --dph, --up-scan; by default under the project folder, or $TGL_ROOT).
Columns: form (accented), plain, stress_source, ipa, rank, sense, ipa_source. The sense is the first sense of the first
record (dictionary order) that gives the reading; the IPA is Wiktionary's own when its reading is the same (ipa_source
dictionary), else the reading make_ipa.py derives from the form (rule; spelled for a spelling with no vowel letter).

Source order (stress_source): KWF, then UP, then Wiktionary, then the other books. When two sources mark the same word
differently, the first one's reading is the word's; a homograph only a later source lists keeps that source's reading. A
proper noun and a common word of the same spelling are looked up apart (the city Iríga beside the KWF's irigá, "to give
an enema"; a capitalized interjection such as Anó! is not a name):
  kwf        the KWF's dictionaries: Diksiyonaryo ng Wikang Filipino (app and website) and Diksiyonaryong
             Filipino-English, their headwords (ma•ta•ób, hin•dî) and the affixed and derived forms they print
             (nakamamatáy, pagkaabâ). Homographs are separate entries (wa•là "open sea", wa•lâ "none"): one reading each.
  up         UP Diksiyonaryong Filipino: diksiyonaryo.ph (pa•la•rô), else the 2001 scan (pang-wa-kás). For a spelling the
             KWF has, a UP reading the KWF lacks is added only for another word (bungá "mouth" beside bunga, husáy "comb"
             beside husay, ulì "a tree" beside uli "again"): its definitions share no content word with those of the KWF
             entries (nor with the UP articles that give a KWF reading; a class word such as isda or halaman alone does
             not count) and it is not a cross-reference to the spelling itself (saksi: saksí). Without any definition to
             compare, the part of speech decides. Of the UP's own articles of a spelling the KWF lacks, one that repeats
             another's definitions (metal beside metál) or only points to it is dropped. A UP form says the stress of a
             word the KWF prints without marks (Isneg, langawen), unless the spelling is English (multiple, barometer).
  wiktionary Wiktionary's own IPA (the dictionary's other IPA readings are machine-made, see real_ipas). For a spelling
             KWF or UP have, a Wiktionary reading they lack is kept only for another word: a form of a word their
             definitions do not name (lalakí, future of lumaki, beside laláki "man"; dáting, linker form of dati, beside
             datíng "arrival"; ginawâ, completive of gawin), an obsolete spelling excepted; a part of speech none of
             their entries has (habáng "asymmetric" beside the conjunction habang); or another of Wiktionary's own
             homographs when every KWF and UP reading of the spelling is one of Wiktionary's readings too (atê "dirt"
             beside ate "older sister", tapayán "bakery" beside tapáyan "jar"). A word the KWF and UP print without
             any mark takes Wiktionary's reading (Ibà, Cebú, reberénsiya), unless it is a common word spelt the
             English way. Otherwise the KWF's or UP's reading is the word's, and Wiktionary only fills the ipa column
             where its reading is the same.
  For a spelling neither KWF nor UP has, the dictionary's records (each gives its own readings):
  english    an English loan written the English way (sense tag emprestimo-ingles, or an etymology that derives the word
             from English, and an English spelling): left unmarked, so the voice reads it as English
  wiktionary Wiktionary's own IPA, as above.
  and, when none of these gives a reading, the other books as read from the records:
  book       an accented form printed by another dictionary (Vicassan, Leo English, Leo James, Tuttle, Ramos...): the
             record's accented headword, its first accented printed form (forma_canonica; the first word of a printed
             phrase counts: ma-la-kíng tí-tik), its accented syllabification, or an accented twin headword that the
             dictionary build folded into the record (formas_alternativas: lamúray)
  legacy     accents printed only by the old lists (Calderón 1915, Panganiban, Guzmán, Freelang...)
  respelled  a foreign spelling that the dictionary follows with a respelled pronunciation (masquerade (más-ke-réyd),
             pausa (páw-sa)): left unmarked, as its stress class describes the respelling, not the spelling
  class      the stress class alone (tonicidade: malumay, malumi, mabilis, maragsa)
  none       nothing known: the bare spelling
KWF and UP mark every stressed syllable, so their forms are read by the rules measured for the UP forms (part_reading,
mákiná -> mákina); when a form has several marks and Wiktionary's own IPA stresses one of the marked syllables, that
syllable is the main stress (á•ni•yá -> aniyá, dá•ra•tíng -> daratíng). A word they print without any mark (video, riot)
or with a respelling (chef (syef)) is a foreign spelling and stays unmarked, except that a name takes the respelling's
stress when its vowels match the spelling's one to one (Cebu (se•bú) -> Cebú, Jose (ho•sé) -> José).
In the books a record gives one reading (plus those of the twins folded into it; the class may give several); when a
homograph of another sense is printed with that reading (tanagà beside tanaga), the record takes the next reading its
own forms print. Per spelling, a class form is dropped when a stronger source gives a reading, a bare `respelled` or
`none` form when any other reading exists, and a form that differs from an earlier one only in letter case or in an
acute on the penult (súkal beside sukal) is not a new reading.
Printed forms with several marks are read by the rules measured against Wiktionary's IPA (part_reading): a mark is a
secondary stress when the UP rules or Tagalog morphology say so (bá-ya-ni-han, sumásama, mátira, makipágbárilan). A
glottal stop cannot follow a consonant: the root's grave or circumflex that the UP keeps in a linker form (ma-da-lîng,
dilàng-aso) is read as the stress alone (madalíng, dilang-aso).
In a hyphenated word each part keeps the marks its source prints on it; the main stress from the IPA or the class goes
on the last part (the root after a prefix, the second half of a doubling), and the IPA's secondary stresses mark the
earlier parts (sabáy-sabáy, humigít-kumulang); a prefix gets no stress mark, only its glottal stop (may-halò, not
máy-halò; dî-kapaní-paniwalà)."""
import argparse
import collections
import difflib
import json
import re
import sys
import unicodedata
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tagalog_orthography import syllabify  # noqa: E402
try:
    from tagalog_phonetics_baybayin import generate_tagalog_ipa  # the dictionary build's own IPA generator
except ImportError:                                                     # pragma: no cover
    generate_tagalog_ipa = None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_ipa import ipa as gen_ipa  # noqa: E402

ACUTE = {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú"}
GRAVE = {"a": "à", "e": "è", "i": "ì", "o": "ò", "u": "ù"}
CIRC = {"a": "â", "e": "ê", "i": "î", "o": "ô", "u": "û"}
MARK_OF = {**{v: "a" for v in ACUTE.values()}, **{v: "g" for v in GRAVE.values()}, **{v: "c" for v in CIRC.values()}}
VOW = "aeiou"
ACCENTED = re.compile(r"[áéíóúàèìòùâêîôûÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛ]")
LEGACY = {"Freelang", "Calderón 1915", "Nigg 1904", "Tgl-Spa", "Tesauro Filipino", "Thesaurus", "Panganiban", "Guzmán", "Forvo Audio", "Tatoeba", "Wikimedia / Lingua Libre Audio"}
CLASS = {"malumay": (2, False), "malumi": (2, True), "mabilis": (1, False), "maragsa": (1, True)}   # (syllable from the end, glottal)
STRONG = {"kwf", "up", "wiktionary", "english", "respelled", "book", "legacy"}   # a form from these makes a class-only form of the same spelling redundant
BOOK_SOURCE = {"ipa": "wiktionary", "headword": "book", "canon": "book", "syllables": "book"}   # reading_of's names -> the list's


def strip(s):
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn").lower()


def mark_syllable(syl, table):
    for i, ch in enumerate(syl):
        if ch.lower() in VOW:
            m = table[ch.lower()]
            return syl[:i] + (m.upper() if ch.isupper() else m) + syl[i + 1:]
    return syl


def accent(word, syls, stressed, glottal):
    """syls: syllables of `word` that join back to it, a hyphen kept at the end of the syllable before it (pag-, a, sa);
    stressed: index of the stressed syllable; glottal: final glottal stop. A hyphenated word is marked on its last part
    only (the root after a prefix, the second half of a doubling), by the rules for a word of its own: a stress that
    falls on an earlier part is left unmarked, as the dictionaries' own readings never put the main stress there, and a
    final glottal stop then gives the last part its grave (circumflex on a one-syllable part). earlier_parts adds the
    secondary stresses that Wiktionary's IPA gives the earlier parts."""
    s = list(syls)
    glottal = glottal and unaccent(s[-1]).rstrip("'’-")[-1:].lower() in VOW    # no glottal stop after a consonant
    start = 0                                   # first syllable of the last part
    for i, x in enumerate(s[:-1]):
        if x.endswith("-"):
            start = i + 1
    n, k, several = len(s) - start, stressed - start, start > 0
    if n == 1:
        if glottal:
            s[start] = mark_syllable(s[start], CIRC)
        elif several and k == 0:
            s[start] = mark_syllable(s[start], ACUTE)
    elif k == n - 2 or k < 0:
        if glottal:
            s[-1] = mark_syllable(s[-1], GRAVE)
    elif k == n - 1:
        s[-1] = mark_syllable(s[-1], CIRC if glottal else ACUTE)
    else:
        s[start + k] = mark_syllable(s[start + k], ACUTE)
        if glottal:
            s[-1] = mark_syllable(s[-1], GRAVE)
    return "".join(s)


def unaccent(s):
    """Accents off, case kept (the UP syllabification carries stress marks: bú‧kás)."""
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def letters(s):
    return re.sub(r"[^a-z]", "", unaccent(s).lower())


def split_syllables(word, syllabified):
    """Syllables of `word` cut where `syllabified` breaks it: ‧ · • . and - all count as breaks, because the UP
    dictionary writes `hi-wî`, `a-rà` and the KWF rules give `a‧ra` (accents and case of `syllabified` are ignored).
    A hyphen of `word` always ends a syllable and stays at its end (pag-, a, sa), so the syllables join back to `word`.
    None when the letters differ (another word, OCR damage, a respelled pronunciation)."""
    cuts, n = set(), 0
    for ch in unaccent(syllabified).lower():
        if ch in "‧·•.-":
            cuts.add(n)
        elif "a" <= ch <= "z":
            n += 1
        elif ch not in "'’":
            return None
    out, cur, n, total = [], "", 0, len(letters(word))
    for ch in word:
        if "a" <= unaccent(ch).lower() <= "z":
            if n in cuts and re.search(r"[a-z]", unaccent(cur), re.I):
                out.append(cur); cur = ""
            n += 1
        cur += ch
        if ch == "-" and n < total and re.search(r"[a-z]", unaccent(cur), re.I):
            out.append(cur); cur = ""
    out.append(cur)
    return out if letters("".join(out)) == letters(syllabified) and "".join(out) == word else None


def recase(plain, model):
    """`plain` in the letter case of `model`, a spelling or syllabification of the same letters (Ma‧ri‧a -> Maria)."""
    ups = [unaccent(c).isupper() for c in model if "a" <= unaccent(c).lower() <= "z"]
    if len(ups) != len(letters(plain)):
        return plain
    out, i = [], 0
    for ch in plain:
        if "a" <= unaccent(ch).lower() <= "z":
            out.append(ch.upper() if ups[i] else ch.lower()); i += 1
        else:
            out.append(ch)
    return "".join(out)


def syllables_of(rec, plain):
    """Syllables of `plain` that join back to it, hyphens kept: from the record's own syllabification (Wiktionary, UP and
    KWF with ‧ or -), else by the KWF rules (tagalog_orthography.syllabify, which returns a string: a‧ra). [plain] when
    neither fits. The syllables take the letter case of the syllabification they come from (I‧sang, BA‧YAN), as the
    earlier word list did."""
    cands = list(rec.get("silabacao") or [])
    try:
        cands.append(syllabify(plain))
    except Exception:
        pass
    for sy in cands:
        parts = split_syllables(recase(plain, sy), sy) if isinstance(sy, str) else None
        if parts and len(parts) > 1 and all(re.search(r"[aeiou]", unaccent(p), re.I) for p in parts):
            return parts
    return [plain]


IPA_VOWEL = r"[aeiouɛɔɪʊəɐæɑʌɒɚɝɜøœɤɯ]"


def stress_from_ipa(ipa):
    """-> (index of the stressed syllable counted by vowel nuclei, number of nuclei, final glottal) or None. Wiktionary
    writes no stress mark on one syllable (/ba/ the question particle, /naŋ/, /ˈbaʔ/ beside it)."""
    m = re.match(r"\s*[/\[]([^/\]]*)[/\]]", ipa)          # the transcription itself, without a note such as "(Batangas)"
    t = m.group(1) if m else ipa.strip("/[] ")
    core = re.sub(r"[ˌ.\s‿ː]", "", unicodedata.normalize("NFD", t))
    if "ˈ" not in t:
        nuc = re.findall(IPA_VOWEL, re.sub(IPA_VOWEL + "̯", "", core))
        return (0, 1, core.endswith("ʔ")) if len(nuc) == 1 else None    # one syllable needs no stress mark (/naŋ/)
    core = re.sub(IPA_VOWEL + "̯", "", core)       # non-syllabic vowels (aɪ̯) are glides
    before = core.split("ˈ")[0]
    return len(re.findall(IPA_VOWEL, before)), len(re.findall(IPA_VOWEL, core)), core.endswith("ʔ")


def earlier_parts(f, syls, ipa):
    """`f` (a hyphenated form read from Wiktionary's IPA, marked on its last part) with the secondary stresses (ˌ) the
    IPA puts on its earlier parts, where tl-pr's respelling marks them: /saˌbaj saˈbaj/ sabáy-sabáy, /humiˌɡit kuˈmulaŋ/
    humigít-kumulang, /ʔaˌlas kuˈwatɾo/ alás-kuwatro; with the glottal stop that ends the part (/maˌjaʔ maˈjaʔ/ mayâ-mayâ,
    /siˌɾaʔ ˈʔulo/ sirâ-ulo; the glottal stop before a part that begins with a vowel is that part's onset: unti-untî).
    A secondary stress on the part's penult needs no mark, and a prefix keeps only its glottal stop (dî-kapaní-paniwalà,
    pag-: see PREFIXES)."""
    m = re.match(r"\s*[/\[]([^/\]]*)[/\]]", ipa)
    t = m.group(1) if m else ipa.strip("/[] ")
    core = re.sub(IPA_VOWEL + "̯", "", re.sub(r"[.\s‿ː]", "", unicodedata.normalize("NFD", t)))
    nuc = [x.start() for x in re.finditer(IPA_VOWEL, core)]
    if "ˌ" not in core or len(nuc) != len(syls):
        return f
    sec = [sum(1 for q in nuc if q < i) for i, ch in enumerate(core) if ch == "ˌ"]     # nucleus index of each ˌ
    ranges, a = [], 0
    for i, sy in enumerate(syls):
        if sy.endswith("-") or i == len(syls) - 1:
            ranges.append((a, i + 1)); a = i + 1
    parts = f.split("-")
    if len(parts) != len(ranges):
        return f
    for pi, (a, b) in enumerate(ranges[:-1]):
        p = parts[pi]
        ks = [k for k in sec if a <= k < b]
        vi = [i for i, ch in enumerate(p) if ch.lower() in VOW]
        if not ks or len(vi) != b - a or ACCENTED.search(p):
            continue
        seg = core[nuc[b - 1] + 1:nuc[b]]                 # from the part's last vowel to the next part's first
        glot = (seg.count("ʔ") >= 2 or ("ʔ" in seg and unaccent(parts[pi + 1][:1]).lower() not in VOW)) and \
            unaccent(p)[-1:].lower() in VOW
        n, pos, ch = len(vi), b - max(ks), list(p)
        if unaccent(p).lower() in PREFIXES:
            if not glot:
                continue
            pos = min(pos, 2)

        def put(j, table):
            c = ch[vi[j]]; mm = table[c.lower()]; ch[vi[j]] = mm.upper() if c.isupper() else mm
        if n == 1 or pos == 1:
            put(n - 1, CIRC if glot else ACUTE)
        else:
            if pos > 2:
                put(n - pos, ACUTE)
            if glot:
                put(n - 1, GRAVE)
        parts[pi] = "".join(ch)
    return "-".join(parts)


def real_ipas(rec):
    """The record's IPA readings that are Wiktionary's own. Every other IPA in the dictionary was made by its build
    (build_yomitan_ptbr.py -> tagalog_phonetics_baybayin.generate_tagalog_ipa) from the record's first accented form or
    syllabification, or from the bare headword: all 83,000 readings of the entries that are not from Wiktionary, and
    the 564 Wiktionary entries that have no recorded pronunciation. Such a reading says nothing its source spelling
    does not, and it reads that spelling wrongly in three ways: it stresses the first marked syllable although the UP
    dictionary marks secondary stresses too (hús-ti-pi-kas-yón gave /ˈhus.ti.pi.kas.yon/), it takes a hyphen for a
    syllable break (may-halò gave /ˈmay.haloʔ/), and with no mark it assumes the penult."""
    ipas = (rec.get("pronuncia") or {}).get("ipa") or []
    if not ipas or "Wiktionary" not in (rec.get("fontes") or []):
        return []
    if any(i.lstrip().startswith("[") for i in ipas):           # Wiktionary's phonetic form: the generator never writes one
        return ipas
    if generate_tagalog_ipa is None:
        return [i for i in ipas if "." not in i and "ː" not in i]   # the generator's style: syllable dots, length marks
    t, can, syl = rec["termo"], rec.get("forma_canonica") or [], rec.get("silabacao") or []
    ref = can[0] if can else (syl[0].replace("‧", "-") if syl else t)
    machine = generate_tagalog_ipa(t, ref)
    return [i for i in ipas if i != machine]


def marks_of(s):
    """Accent marks of a spelling, one item per vowel letter: None, 'a' acute, 'g' grave, 'c' circumflex."""
    out = []
    for ch in unicodedata.normalize("NFC", s).lower():
        if ch in MARK_OF:
            out.append(MARK_OF[ch])
        elif unaccent(ch) in VOW:
            out.append(None)
    return out


GREEK_IYA = re.compile(r"(?:[aeiou][^aeiou]*[aeiou]lohiya|[aeiou](?:grapiya|metriya|patiya|sopiya))$")   # not si-lohiya
KNOWN = set()     # the dictionary's plain spellings (filled by build): the roots and words of the tests below


def _prefix_chain(s, depth=3):
    """Can s be written as up to `depth` prefixes of PREFIXES (pinag + ka, maka, napaka)?"""
    return s in PREFIXES or depth > 1 and any(s[:i] in PREFIXES and _prefix_chain(s[i:], depth - 1) for i in range(1, len(s)))


def _root_known(rest):
    """rest is a word of the dictionary, maybe after a CV reduplication (sasalita) or before -an/-in (kilalanin)."""
    if len(re.findall(r"[aeiou]", rest)) < 2:
        return False
    if rest in KNOWN:
        return True
    if len(rest) > 3 and rest[:2] == rest[2:4] and rest[2:] in KNOWN:
        return True
    return any(rest.endswith(x) and rest[:-len(x)] in KNOWN for x in ("han", "hin", "an", "in"))


def secondary_mark(part, k, loan=False):
    """Does Tagalog morphology explain an acute on vowel k (0-based) of a part printed without syllable breaks as a
    secondary stress? Vicassan and Leo English mark the stress of a prefix (mátira, makápito, pagkálayas), of a
    reduplicated syllable (sumásama, tinátaya, nakabúbuti), of the root before -an/-in (kílusan, pálitan) and of the
    first word of a compound (walámpera, hulíngsabi); the main stress is then the penult. A Spanish loan printed with its
    own accent (mákina, kódigo, péndulo, simétriko) has none of these and keeps its antepenult stress; for a record
    whose etymology names Spanish, Latin, Greek or French (loan=True) only the suffix and reduplication tests count,
    as ma-kina or pa-lido would pass the prefix test."""
    w = unaccent(part).lower()
    vi = [i for i, c in enumerate(w) if c in VOW]
    if not re.fullmatch(r"[a-z']+", w) or k >= len(vi):
        return False
    at = vi[k]
    if w.endswith(("an", "in")):                                          # root + suffix
        return True
    try:
        sy = syllabify(w)
    except Exception:
        sy = None
    S = sy.split("‧") if isinstance(sy, str) else []
    if "".join(S) == w:                                                    # reduplication: na-ka-bú-bu-ti, su-má-sa-ma
        j, n0 = 0, 0
        while j < len(S) and n0 + len(S[j]) <= at:
            n0 += len(S[j]); j += 1
        if j + 1 < len(S):
            if S[j] == S[j + 1]:
                return True
            if j and len(S[j]) == 2 and S[j][0] in "mn" and re.fullmatch(r"[^aeiou]+[aeiou]", S[j - 1]) and \
                    S[j - 1][:-1] + S[j][1] == S[j + 1]:                     # -um-/-in- inside: s-um-á-sama, t-in-á-taya
                return True
    if loan:
        return False
    m = re.match(r"(ng|n|m)(?=[^aeiou'])", w[at + 1:])                     # compound with a linker: wala-m-pera
    if m and w[:at + 1] in KNOWN and w[at + 1 + len(m.group()):] in KNOWN:
        return True
    for i in range(at + 1, len(w) - 2):                                    # prefix: ma-tira, maka-pito, pagka-layas
        if _prefix_chain(w[:i]) and _root_known(w[i:].lstrip("'")):
            return True
    return False




def part_reading(part, marks, plain=False, loan=False):
    """Stress of one part of a word (the whole word when it has no hyphen) from the marks its source prints on it:
    (syllable counted from the end, 1 = last; final glottal; a second acute kept, or None), or None with no mark.
    The UP dictionary and diksiyonaryo.ph mark every stressed syllable, so long words carry two or three marks. Which
    one is the main stress was measured on the Wiktionary entries that also have such a form (README): a final grave
    means penult stress + glottal and a final circumflex final stress + glottal, whatever comes before (95 % and 85 %);
    otherwise the last mark is the main stress (77-98 %), except that
      - antepenult + last syllable (té-le-po-nó, Lé-ba-nón) is an antepenult stress when the word ends in a vowel (83 %),
        and is kept with both marks when it ends in a consonant (Wiktionary: last 53 %, antepenult 40 %);
      - except in a doubled word (sa-lá-sa-lá, la-wí-la-wí), where the stress of the second half is the main one;
      - penult + last (tín-tá) is a penult stress (2:1);
      - a last mark on the fourth syllable from the end or earlier (bá-ya-ni-han, lóng-ga-ni-sa) is a secondary stress:
        the main stress is the unmarked penult (19 of 25 syllabified forms, 65 of 72 plain ones);
      - plain: in a form written without syllable breaks (Vicassan, Leo English, Calderón: própaganda, mátira,
        makipágbárilan) a last mark on the antepenult is a secondary stress too (penult 82 of 91, antepenult 4), while in
        the syllabified UP forms it is the main stress (nú-me-ro, 54 of 84);
      - -lohiya, -grapiya, -metriya, -patiya, -sopiya (Spanish -logía, -grafía...) stress the i (59 of 60 -lohiya
        words in Wiktionary), whatever the marks say (bul-ka-no-ló-hi-yá)."""
    n = len(marks)
    if not any(marks):
        return None
    if marks[-1] == "c":
        return (1, True, None)
    if marks[-1] == "g":
        return (2 if n > 1 else 1, True, None)
    if GREEK_IYA.search(unaccent(part).lower()):
        return (2, False, None)
    pos = [n - i for i, m in enumerate(marks) if m]    # an inner grave or circumflex (pá-ta-hì-an) marks a stress too
    if pos[-2:] == [3, 1]:
        end = unaccent(part).lower().rstrip("'’")
        h = len(end) // 2
        if len(end) % 2 == 0 and end[:h] == end[h:]:     # a doubled word (sa-lá-sa-lá): the second half's stress, 21 of 21
            return (1, False, None)
        return (3, False, None) if end and end[-1] in VOW else (1, False, 3)
    if pos[-2:] == [2, 1]:
        return (2, False, None)
    if pos[-1] >= 4 or (plain and pos[-1] == 3 and secondary_mark(part, n - 3, loan)):
        return (2, False, None)
    return (pos[-1], False, None)


# Prefixes that stand before a hyphen (makapag-aral, tagapag-ugnay, di-mapang-akit). Vicassan, Leo English and the UP
# dictionary print their secondary stress (makapág-aral, papág-aralin); OP writes none, and an acute there would make
# the voice stress the prefix instead of the root. A glottal mark on a prefix (dî-kasí) is a real sound and stays.
PREFIXES = set("""i ka ma na pa um in di mag nag pag ipag pinag ipinag papag pinapag makapag nakapag ikapag pagkapag
    makapang nakapang makipag nakipag pakikipag makikipag nakikipag ipakipag mapag napag mapang mapam mapan tagapag
    tagapang taga tag maka naka magka nagka pagka pagkaka magkaka nagkaka mang nang pang man nan pan mam nam pam ipang
    ipinang pinang maki naki paki makiki nakiki pakiki magsi nagsi magsipag nagsipag pagsi magpa nagpa pagpa ipa pina
    ipina magpapa nagpapa pagpapa magpaka nagpaka pagpapaka mapa napa kasing kasin kasim sing sin sim magkasing
    magkasin magkasim pinaka pinakama may tig sang ika labing ikalabing""".split())


def render(base, readings):
    """`base` (no accents, hyphens kept) with marks, one reading per hyphen-separated part (None = no mark)."""
    parts = base.split("-")
    voiced = sum(1 for p in parts if re.search(r"[aeiou]", p, re.I))
    out = []
    for idx, (p, rd) in enumerate(zip(parts, readings)):
        vi = [i for i, ch in enumerate(p) if ch.lower() in VOW]
        if rd is not None and rd[1] and p.rstrip("'’")[-1:].lower() not in VOW:   # no glottal stop after a consonant:
            rd = (rd[0], False, rd[2])                  # the UP keeps the root's mark in a linker form (ma-da-lîng)
        if rd is not None and p.lower() in PREFIXES and any(re.search(r"[a-z]", q, re.I) for q in parts[idx + 1:]):
            rd = (min(rd[0], 2), True, None) if rd[1] else None     # a prefix keeps only a glottal mark
        if rd is None or not vi:
            out.append(p); continue
        n, (pos, glot, extra), ch = len(vi), rd, list(p)

        def put(k, table):
            c = ch[vi[k]]; m = table[c.lower()]; ch[vi[k]] = m.upper() if c.isupper() else m
        if n == 1:
            if glot:
                put(0, CIRC)
            elif pos == 1 and voiced > 1:
                put(0, ACUTE)
        elif pos == 1:
            put(n - 1, CIRC if glot else ACUTE)
        else:
            if pos > 2:
                put(max(0, n - pos), ACUTE)
            if glot:
                put(n - 1, GRAVE)
        if extra and n > 1 and extra != pos and n - extra >= 0:
            put(n - extra, ACUTE)
        out.append("".join(ch))
    return "-".join(out)


def marked_form(base, s, plain_ok=True, loan=False):
    """`base` with the stress that `s`, an accented spelling or syllabification of the same word, prints on it: hi-wî ->
    hiwî, hús-ti-pi-kas-yón -> hustipikasyón, may-halò -> may-halò. None when s is another word or has no mark.
    plain_ok=False for headwords (diksiyonaryo.ph and UP print them unsyllabified but mark them by the UP rules)."""
    t = unicodedata.normalize("NFC", s.strip())
    if re.fullmatch(r"\S+(?:\s+\S+)+", t) and not re.search(r"[,;/()]", t) and (t[:1].islower() or base[:1].isupper()):
        t = t.split()[0]                   # a printed phrase: its first word (ma-la-kíng tí-tik); not a list of variants,
                                           # nor a name (Pa-to-là Ka-o-rá-yan) for a common word
    t = t.strip("!?¡¿.,;: ")
    if not t or re.search(r"[^A-Za-zÀ-ÿñÑ'’‧·•.\-]", t) or letters(t) != letters(base):
        return None
    mk = marks_of(t)
    if not any(mk):
        return None
    plain = plain_ok and not re.search(r"[‧·•.]", t) and t.count("-") <= base.count("-") and not base.startswith("-") \
        and not base.endswith("-")                                       # an affix entry (nápaka-) is not a derived word
    readings, i = [], 0
    for p in base.split("-"):
        n = sum(1 for c in p if c.lower() in VOW)
        readings.append(part_reading(p, mk[i:i + n], plain, loan)); i += n
    return render(base, readings)


def unmark(s):
    """Acute, grave and circumflex off; case and ñ kept."""
    return unicodedata.normalize("NFC", "".join(c for c in unicodedata.normalize("NFD", s) if c not in "\u0300\u0301\u0302"))


def reading_key(f):
    """What a form tells the voice, for telling readings apart: lower case, and its marks read by the rules above, so
    that an acute on the penult (súkal = sukal, lángka = langka), on a one-syllable word (ká = ka) or on a prefix
    (mapág-impók = mapag-impók) adds nothing; ñ is kept (masbatéño is not masbateno)."""
    return (marked_form(unmark(f), f, False) or f).lower()


def _english_words():
    for p in ("/usr/share/dict/american-english", "/usr/share/dict/words"):
        try:
            return {w.strip().lower() for w in open(p, encoding="utf-8", errors="ignore") if w.strip()}
        except OSError:
            continue
    return set()


ENGLISH_WORDS = _english_words()
EN_ETY = re.compile(r"ingl[eê]s", re.I)
EN_ETY_NOT = re.compile(r"ingl[eê]s (?:antigo|médio|arcaico)|compare com[^;.\n]*|decalque[^;.\n]*|calco[^;.\n]*|alternância de código[^;.\n]*", re.I)
# notes that say the word is not read the English way: several pronunciations of different origins (mama, Bay), a
# Spanish stress or reading (radar, ikon, desperado), an English influence on a native word or spelling (charing, ios,
# otcho), a semantic loan (base, pasta), wordplay (dakota)
EN_ETY_SKIP = re.compile(r"pron[uú]ncia|pronunciad|tonicidade|sem[aâ]ntic|pseudo-?h?ispanismo|influenciad[oa] pel[oa] (?:espanhol|ingl[eê]s|grafia)|"
                         r"sob influ[eê]ncia do ingl|grafia|wordplay|trocadilho|am[aá]lgama|espanhol", re.I)
EN_LETTERS = re.compile(r"[cfjqvxz]|sh|th|ph|ck|gh|wh|ee|oo|ea|ou|([bdfgklmnprstz])\1")


RESPELLED = re.compile(r"^\s*[^\s(]+\s*\((.+)\)\s*$")       # a foreign spelling with the dictionary's respelling
LOAN_ETY = re.compile(r"espanhol|latim|grego|franc[eê]s|\[Esp|\bEsp\b", re.I)


def ety_texts(rec):
    e = rec.get("etimologia")
    if not e:
        return []
    if isinstance(e, str):
        return [e]
    return [x for v in e.values() for x in ([v] if isinstance(v, str) else (v if isinstance(v, list) else [])) if isinstance(x, str)]


def english_loan(rec, plain):
    """An English loan written the English way: the dictionary tags a sense emprestimo-ingles or derives the word from
    English, and the spelling is English: an English word, or letters a Tagalog spelling does not use. Respelled loans
    (iskul, kompyuter, dóbol) are Tagalog spellings and keep their marks. For a Wiktionary entry only its own etymology
    text counts (the UP/KWF notes merged into it belong to all its homographs, and the chain also runs through the
    English words a native word was blended with); an etymology that also names Spanish (Empréstimo do espanhol karate
    ou inglês karate; Origem regional: Espanhol, Inglês) or speaks of the word's pronunciation is not enough."""
    w = strip(plain)
    if not re.fullmatch(r"[a-z'\-]+", w) or not re.search(r"[aeiou]", w):
        return False
    core = w.replace("'", "")
    spelled = core in ENGLISH_WORDS or core.replace("-", "") in ENGLISH_WORDS or \
        ("-" in core and all(p in ENGLISH_WORDS for p in core.split("-") if p)) or bool(EN_LETTERS.search(core))
    if not spelled:
        return False
    if any("emprestimo-ingles" in (s.get("etiquetas") or []) for s in rec.get("sentidos") or []):
        return True
    e = rec.get("etimologia")
    if not e:
        return False
    if isinstance(e, str):
        texts = [e]
    else:
        keys = ("texto",) if "Wiktionary" in (rec.get("fontes") or []) else list(e)
        texts = [x for k in keys for x in ([e.get(k)] if isinstance(e.get(k), str) else (e.get(k) or [])) if isinstance(x, str)]
    texts = [EN_ETY_NOT.sub("", t) for t in texts]
    if any(EN_ETY_SKIP.search(t) for t in texts):
        return False
    return any(EN_ETY.search(t) for t in texts)


def first_ipa(r):
    ipas = real_ipas(r)
    return next((i for i in ipas if i.lstrip().startswith("/")), ipas[0] if ipas else "")


def ipa_reading(r, w, syls=None):
    """The record's reading from Wiktionary's own IPA: (form, ipa), or None when it has none that fits the spelling."""
    syls = syls or syllables_of(r, w)
    base = "".join(syls)
    for ip in real_ipas(r):
        st = stress_from_ipa(ip)
        if st and len(syls) == st[1] and st[0] < len(syls):    # the reading has as many syllables as the spelling
            return earlier_parts(accent(base, syls, st[0], st[2]), syls, ip), ip
        if st and st[1] == 1:                                   # one syllable however it is spelled (Young /ˈjaŋ/)
            return accent(base, [base], 0, st[2]), ip
    return None


def reading_of(r, w, taken=frozenset(), loan=False):
    """-> list of (form, stress_source, ipa) for one record of the plain spelling w, from the dictionary's record alone;
    taken: the readings (lower case) of the accented headwords of the spelling's other records; loan: some record of
    the spelling derives it from Spanish, Latin, Greek or French (see secondary_mark)."""
    t = r["termo"]
    syls = syllables_of(r, w)
    base = "".join(syls)                                         # w in the case of the record's syllabification (Maria, BAYAN)
    ipa0 = first_ipa(r)
    flat = ipa0 if ipa0 and "ˈ" not in ipa0 else ""    # a reading without a stress mark (apaka- /ʔapaka/) fits a form of
    flat_glottal = bool(re.search(r"ʔ\s*[/\]]", flat))   # the word that has its final glottal stop or lacks it alike
    legacy_only = all(f in LEGACY for f in (r.get("fontes") or []))
    if english_loan(r, t):
        return [(base, "english", ipa0)]
    if t != strip(t) and ACCENTED.search(t) and not legacy_only:   # printed with accents by a real dictionary
        h = t.lower() if not t[0].isupper() or t == t.capitalize() else t
        h = marked_form(unmark(h), h, False) or h      # read by the rules of the printed forms: mákiná, págsasálin, súkal
        return [(h, "headword", ipa0)]
    x = ipa_reading(r, w, syls)
    if x:
        return [(x[0], "ipa", x[1])]
    cands = [(t, "legacy")] if legacy_only and t != strip(t) else []
    cands += [(c, "legacy" if legacy_only else "canon") for c in r.get("forma_canonica") or []]
    cands += [(c, "syllables") for c in r.get("silabacao") or []]
    loan = loan or bool(LOAN_ETY.search(" ".join(ety_texts(r))))
    marked = []
    for c, src in cands:
        f = marked_form(base, c, True, loan)
        if f and all(f.lower() != m[0].lower() for m in marked):
            marked.append((f, src, ""))
    if marked:
        # the record's reading: the first marked form, unless another record of the spelling (an accented headword the
        # build kept apart, tanagà beside tanaga) already gives it and the record's own forms print another reading
        out = [next((m for m in marked if m[0].lower() not in taken), marked[0])]
        for alt in r.get("formas_alternativas") or []:      # accented twins the build folded into this record (lamúray
            if alt != strip(alt) and ACCENTED.search(alt) and letters(alt) == letters(w):    # into lamuray): their
                f = marked_form(base, alt, False)                                             # readings are its too
                if f and all(f.lower() != o[0].lower() for o in out):
                    out.append((f, "canon", ""))
        return out
    if any(RESPELLED.match(c) for c in r.get("forma_canonica") or []):
        return [(base, "respelled", ipa0)]                  # masquerade (más-ke-réyd): the class describes the respelling
    out = []
    n = len(syls)
    for c in r.get("tonicidade") or []:
        if c in CLASS:
            pos, g = CLASS[c]
            out.append((accent(base, syls, max(0, n - pos), g), "class", flat if flat_glottal == g else ""))
    return out or [(w, "none", "" if flat_glottal else flat)]


# ---------------------------------------------------------------- the KWF and UP dictionaries
POS = {"png": "n", "pnr": "adj", "pnd": "v", "pnb": "adv", "pnh": "pron", "pdm": "intj", "pdd": "intj", "plp": "affix",
       "pnl": "affix", "ptg": "conj", "pnu": "prep", "pnt": "part", "ptk": "part", "pnk": "part", "daglat": "abbr",
       "symbol": "abbr", "akronim": "abbr",                                           # KWF and UP labels
       "noun": "n", "adjective": "adj", "verb": "v", "adverb": "adv", "pronoun": "pron", "interjection": "intj",
       "affix": "affix", "conjunction": "conj", "preposition": "prep", "article": "part", "ligature": "part",
       "participle": "adj",                                                           # Filipino-English
       "substantivo": "n", "adjetivo": "adj", "verbo": "v", "advérbio": "adv", "pronome": "pron", "interjeição": "intj",
       "afixo": "affix", "partícula": "part", "abreviação": "abbr", "acrônimo": "abbr", "conjunção": "conj",
       "preposição": "prep", "artigo": "part", "numeral": "num"}                      # the UP scan and the dictionary
STOP = frozenset("""isang mga nang para mula hindi ginagamit bilang anumang naman upang kung siya sila ito iyon kanilang
    kaniyang tulad gaya karaniwang karaniwan lalo lamang pagiging bagay nauukol hinggil kaugnay paraan sinumang ibang
    mayroong walang kaya dito doon niya nila tingnan varyant
    marami maraming mahaba mahabang maikli maikling maliit malaki malaking""".split())   # the last line: sizes, which
    # describe a fish and a fishing line alike (kitang)
STOP6 = frozenset(x[:6] for x in STOP)
LONG_PREFIX = re.compile(r"^(?:pagkaka|pagka|pakikipag|pakiki|pagpapa|pinaka|nakaka|makaka|nakiki|makiki|nagpapa|magpapa|"
                         r"ipinag|pinag|nagsisi|magsisi)(?=[a-z]{4})")    # pagkakaisa and pagkakalapat share no root


def _stem(x):
    return LONG_PREFIX.sub("", x)[:6]


CLASS_WORDS = frozenset(_stem(x) for w in """isda halaman ibon hayop insekto kulisap damo baging palumpong punongkahoy
    kahoy bahagi""".split() for x in (w, w + ("ng" if w[-1] in "aeiou" else "g" if w[-1] == "n" else "")))
    # "uri ng isda", "bahagi ng": a word in common that says nothing about which fish
Src = collections.namedtuple("Src", "word printed proper pos stems heads defs foreign respell kind")
RESPELLING = re.compile(r"^(.*?)\s*\((.+)\)\s*$")       # chef (syef), video (ví•di•ó): a foreign spelling and its respelling
SENSE_BREAK = re.compile(r"\s*\|\s*|\s+\d+\s*:\s*")      # senses joined by " | " (the sites) or numbered "2:" (the scan)
DEBUG = collections.defaultdict(list)                   # samples of the decisions below, for checking a build


def pos_set(s):
    """A part-of-speech label of a source or a record -> a set of n, v, adj, adv... (empty when unknown)."""
    return frozenset(filter(None, (POS.get(x.strip(". ").lower()) for x in re.split(r"[\s,/;]+", s or ""))))


def _content(text):
    for x in re.findall(r"[a-z]{4,}", strip(text)):
        s = _stem(x)
        if x not in STOP and len(s) >= 4 and s not in STOP6:
            yield s


def stems(text):
    """Content words of a definition (accents off, 4 letters or more, a long prefix off, first 6 letters), for telling
    homographs apart."""
    return frozenset(_content(text))


def _entry(table, word, printed, pos, defs="", foreign=False, kind="head", respell=""):
    raw = (word or "").strip()
    word = re.sub(r"\d+$", "", unicodedata.normalize("NFC", re.sub(r"[•·‧]", "", raw)).strip().strip("!?.,;: "))
    if len(word) < 2 or not re.fullmatch(r"[A-Za-zÀ-ÿñÑ'\-]+", word) or re.fullmatch(r"([A-Z])(?i:\1)", word):
        return                                          # not a single word, or a letter entry (Aa, Bb)
    printed = re.sub(r"\d+\.?$", "", unicodedata.normalize("NFC", (printed or word).strip()))
    p = pos_set(pos)
    proper = word[:1].isupper() and not raw.endswith("!") and "intj" not in p     # Anó! is an interjection, not a name
    heads = frozenset(filter(None, (next(_content(t), None) for t in SENSE_BREAK.split(defs))))   # each sense's first word
    table[strip(word)].append(Src(word, printed, proper, p, stems(defs), heads, defs, foreign, respell, kind))


def default_sources():
    """Where the KWF and UP files are: $TGL_ROOT (the Tagalog project folder), else found from tagalog_orthography."""
    root = os.environ.get("TGL_ROOT")
    if root:
        scripts = os.path.join(root, "Project TGL to PRT-BR", "Scripts")
    else:
        import tagalog_orthography
        scripts = os.path.dirname(os.path.abspath(tagalog_orthography.__file__))
        root = os.path.dirname(os.path.dirname(scripts))
    d = os.path.join(root, "Digital dictionaries")
    return {"kwf": [os.path.join(d, "KWF Diksiyonaryo", "output", "kwf_tagalog_entries.jsonl"),
                    os.path.join(d, "KWF Diksiyonaryo", "output", "kwf_website_extra.jsonl")],
            "dfe": os.path.join(d, "DFE", "dfe_dictionary.jsonl"),
            "dph": os.path.join(d, "UP Diksiyonaryo", "up_diksiyonaryo_ph.jsonl"),
            "up_scan": os.path.join(scripts, "up_enrichments.json")}


def load_sources(paths):
    """The KWF and UP dictionaries by plain spelling: kwf (the Diksiyonaryo ng Wikang Filipino and the Filipino-English
    dictionary: headwords, affixed and derived forms), dph (diksiyonaryo.ph), up_scan (the 2001 print, read by OCR)."""
    missing = [p for p in [*paths["kwf"], paths["dfe"], paths["dph"], paths["up_scan"]] if not os.path.exists(p)]
    if missing:
        sys.exit("missing source files (set --kwf, --dfe, --dph, --up-scan or $TGL_ROOT):\n  " + "\n  ".join(missing))
    S = {k: collections.defaultdict(list) for k in ("kwf", "dph", "up_scan")}
    for p in paths["kwf"]:
        for line in open(p, encoding="utf-8"):
            e = json.loads(line)
            defs = " | ".join(d.get("definition") or "" for d in e.get("definitions") or [])
            _entry(S["kwf"], e.get("word"), e.get("syllabification"), (e.get("part_of_speech") or {}).get("abbreviation"), defs)
            for a in e.get("affixations") or []:
                for f in re.split(r"\s*[,;]\s*", a.get("affixed_form") or ""):
                    _entry(S["kwf"], f, f, a.get("abbreviation"), kind="derived")
    for line in open(paths["dfe"], encoding="utf-8"):
        e = json.loads(line)                     # English definitions: they cannot be compared with UP's Filipino ones
        _entry(S["kwf"], e.get("headword_plain") or e.get("headword"), e.get("headword"), e.get("part_of_speech"))
        for d in e.get("derivatives") or []:
            for f in d.get("forms") or [d.get("form")]:
                _entry(S["kwf"], f, f, d.get("part_of_speech"), kind="derived")
    for line in open(paths["dph"], encoding="utf-8"):
        for a in json.loads(line).get("articles") or []:
            h = (a.get("headword_accented") or "").strip()
            m = RESPELLING.match(h)
            for v in (m.group(1) if m else h).split(","):     # abdomen, abdómen: variants
                _entry(S["dph"], v, v, a.get("pos"), " | ".join(a.get("senses") or []), bool(m), respell=m.group(2) if m else "")
    for key, v in json.load(open(paths["up_scan"], encoding="utf-8")).items():
        k0 = key.split(",")[0].strip()
        for u in v.get("up_entries") or []:
            h = (u.get("headword_up") or "").strip()
            m = RESPELLING.match(h)
            h = m.group(1) if m else h
            if letters(h) == letters(k0):         # the scan writes syllable breaks as hyphens: the key has the real ones
                _entry(S["up_scan"], recase(k0, h), h, u.get("pos_pt"), u.get("definition_tl") or "", bool(m),
                       respell=m.group(2) if m else "")
    return S


def respelled_form(base, resp):
    """The stress a respelling prints, put on the spelling when both have as many vowel letters (Cebu (se•bú) -> Cebú,
    Quiapo (kyá•po) has fewer: None). The respelling of a list of names is matched by its letters (Burgos, Jose
    (búr•gos, ho•sé): Jose takes ho•sé)."""
    vi = [i for i, c in enumerate(base) if unaccent(c).lower() in VOW]
    fits = []
    for t in re.split(r"\s*[,;]\s*", resp.strip()):
        mk = marks_of(t)
        if t and not re.search(r"[^A-Za-zÀ-ÿñÑ'’‧·•.\-]", t) and any(mk) and len(mk) == len(vi):
            fits.append((difflib.SequenceMatcher(None, strip(base), re.sub(r"[^a-z]", "", strip(t))).ratio(), mk))
    if not fits:
        return None
    mk = max(fits, key=lambda x: x[0])[1]
    ch = list(base)
    for i, m in zip(vi, mk):
        if m:
            c = unaccent(ch[i]); v = {"a": ACUTE, "g": GRAVE, "c": CIRC}[m][c.lower()]
            ch[i] = v.upper() if c.isupper() else v
    return marked_form(base, "".join(ch), False)


def src_form(s, base, transfer=False):
    """-> (form, unmarked): the reading a source entry prints, on `base`. A respelled foreign word (chef (syef)) or a
    word printed without any mark (video, hostage) stays as spelt; unmarked: such a word of two syllables or more.
    transfer: a respelling gives its stress to the spelling where the vowels match one to one (names: Cebu (se•bú) ->
    Cebú; in a common word the letters rarely match the respelling's syllables: polypropene (po•lí•pro•pín))."""
    if not s.foreign:
        for t in (s.printed, s.word):
            f = marked_form(base, t, False)
            if f:
                return f, False
    elif transfer and s.respell:
        f = respelled_form(base, s.respell)
        if f:
            return f, False
    return base, len(re.findall(r"[aeiou]", strip(base))) > 1


def self_xref(s, w):
    """Every sense of the article only names a form of the same spelling (saksi: saksí)."""
    senses = [x.strip(" .") for x in s.defs.split("|") if x.strip(" .")]
    clean = lambda t: strip(re.sub(r"[•·‧]|\s*\d+(?:-\d+)?$", "", re.sub(r"^(?:varyant ng|tingnan ang|ibang anyo ng)\s+", "", t, flags=re.I)))
    return bool(senses) and all(clean(t) == w for t in senses)


def related(x, s):
    """Do the definitions of the entries x and s describe the same word? Two content words in common (a class word
    such as isda or halaman counts only beside another), or one that is the whole definition of one of them when the
    other's is short too or one of its senses begins with it (mister: ginoó; ginoó, magalang na tawag sa lalaki...),
    not a word that a long definition only mentions (dagá: lupà; dagà, a Visayan rite before a boat lands). Sizes and
    quantities are not content words (kitáng, a long line with many hooks, is not kítang, a fish)."""
    a, b = x.stems, s.stems
    shared = a & b
    strong = shared - CLASS_WORDS
    if len(strong) >= 2 or (strong and len(shared) >= 2):
        return True
    if len(strong) == 1 and min(len(a), len(b)) == 1:
        return max(len(a), len(b)) <= 4 or bool(strong & (s.heads if len(a) == 1 else x.heads))
    return False


def same_text(x, s):
    """Nearly the same definition: half the content words of the two together in common (suwà, suwá: suhà)."""
    return bool(x.stems and s.stems) and len(x.stems & s.stems) * 2 >= len(x.stems | s.stems)


def same_word(x, refs, w, pos_fallback=True, ups=()):
    """The entry of `refs` (KWF entries, or UP articles already taken) that the UP article x is the same word as: its
    definitions share content words with that entry's (metal and metál, both "alinman sa mga batayang substance...");
    else, when they cannot be compared that way, the same part of speech (pos_fallback). `ups`: UP articles beside the
    KWF entries, which count only with nearly the same definition (the UP's own copy of the word). A cross-reference
    to the spelling itself (saksi: saksí) is the same word too. None: another word."""
    if self_xref(x, w):
        return x
    voters, up_voters = [s for s in refs if s.stems], [s for s in ups if s.stems]
    if (voters or up_voters) and x.stems:
        return next((s for s in voters if related(x, s)), None) or next((s for s in up_voters if same_text(x, s)), None)
    return next((s for s in list(refs) + list(ups) if x.pos & s.pos), None) if pos_fallback else None


FORM_OF = re.compile(r"^(?:aspecto|modo|forma|grafia|variante|plural|contração|abreviação|abreviatura|diminutivo)\b[^:;]*\b"
                     r"d[aeo]s?\s+(?:palavra\s+)?['‘“\"]?([^\s'’”\":;,()]+)", re.I)
OBSOLETE = re.compile(r"^(?:forma|grafia)\s+(?:obsoleta|arcaica|antiga)", re.I)


def wikt_other_word(r, w, refs):
    """Is the Wiktionary record r another word than the KWF and UP entries `refs` of spelling w? True when its sense is
    a form of another word that those entries do not name (lalakí: future of lumaki, beside laláki "man"; dáting: linker
    form of dati, beside datíng "arrival"; ginawâ: completive of gawin; uli, a form of ule "oilcloth", beside ulî
    "again"), or when its part of speech is one none of them has (habáng "asymmetric" beside the conjunction habang).
    False when it is a form of a word they name, of w itself, or an obsolete spelling. None: undecided."""
    d = (r.get("sentidos") or [{}])[0].get("definicao") or ""
    m = FORM_OF.match(d)
    if m:
        if OBSOLETE.match(d):
            return False
        x = strip(m.group(1)).strip("'-")
        named = {t for s in refs for t in re.findall(r"[a-z'-]+", strip(s.defs))}
        return x != w and x not in named
    p = pos_set(r.get("classe_gramatical"))
    if p and not p & frozenset().union(*(s.pos for s in refs)):
        return True
    return None


def wikt_choice(s, base, wk):
    """A KWF or UP form with several marks (á•ni•yá, dá•ra•tíng) is read by part_reading's rules; when Wiktionary's own
    IPA puts the stress on one of the marked syllables, its reading decides which (aniyá, daratíng)."""
    if s.foreign or "-" in base or not wk:
        return None
    t = s.printed if letters(s.printed) == letters(base) else s.word
    mk = marks_of(t)
    n = len(mk)
    if sum(1 for m in mk if m) < 2:
        return None
    glot = mk[-1] in ("g", "c")
    pos = {(2 if n > 1 else 1) if (i == n - 1 and m == "g") else n - i for i, m in enumerate(mk) if m}
    for f, ip, r in wk:
        st = stress_from_ipa(ip)
        if st and st[1] == n and st[1] - st[0] in pos and st[2] == glot and "-" not in f:
            return f
    return None


def first_sense(r):
    return r["sentidos"][0]["definicao"][:50] if r.get("sentidos") else ""


def printed_keys(r, w):
    """The readings a record prints (headword, printed forms, syllabification, folded twins, Wiktionary's IPA)."""
    base = "".join(syllables_of(r, w))
    out = set()
    for c in [r["termo"], *(r.get("forma_canonica") or []), *(r.get("silabacao") or []), *(r.get("formas_alternativas") or [])]:
        if isinstance(c, str):
            for plain_ok in (False, True):
                f = marked_form(base, c, plain_ok)
                if f:
                    out.add(reading_key(f))
    x = ipa_reading(r, w)
    if x:
        out.add(reading_key(x[0]))
    return out


def book_readings(w, recs, loan):
    """The readings of the dictionary's records alone (no KWF, UP or Wiktionary reading): see reading_of."""
    heads = [(i, marked_form(w, r["termo"], False)) for i, r in enumerate(recs) if r["termo"] != strip(r["termo"]) and
             ACCENTED.search(r["termo"]) and not all(f in LEGACY for f in (r.get("fontes") or []))]
    first = [(r["sentidos"][0]["definicao"] if r["sentidos"] else "")[:40] for r in recs]
    cands = []
    for i, r in enumerate(recs):
        taken = frozenset(h.lower() for j, h in heads if h and j != i and first[j] != first[i])   # a homograph, not a twin
        cands += [(f, BOOK_SOURCE.get(src, src), ipa, first_sense(r)) for f, src, ipa in reading_of(r, w, taken, loan)]
    srcs = {c[1] for c in cands}
    sense_ipa = {}                          # the sense and ipa columns: the first record (dictionary order) that gives the
    for f, src, ipa, sense in cands:        # reading, a dropped class or bare form included (ng: the marker /naŋ/, not the
        sense_ipa.setdefault(reading_key(f), (sense, ipa))       # letter /ˈŋa/; sa: the marker, not tsa's old form)
    out = []
    for f, src, ipa, sense in cands:
        if src == "class" and srcs & STRONG:        # the stress class is weaker evidence and usually repeats a stronger reading
            continue
        if src == "respelled" and srcs & (STRONG - {"respelled"}):   # the foreign word beside a reading of the spelling
            continue
        if src == "none" and srcs - {"none"}:       # nothing known about this record: another record of the spelling says more
            continue
        s, i = sense_ipa[reading_key(f)]
        out.append((f, src, i or ipa, s))
    return out


def group_readings(w, recs, proper, split, S, loan, stats):
    """(form, stress_source, ipa, sense) for the records of spelling w that are proper nouns (proper) or not. split: the
    spelling has records of both kinds, which are then looked up apart in the sources."""
    base = "".join(syllables_of(recs[0], w))

    def pick(table):
        ents = table.get(w, [])
        mine = [s for s in ents if s.proper == proper]
        return mine if mine or split else ents

    wk = [(x[0], x[1], r) for r in recs for x in [ipa_reading(r, w)] if x]     # Wiktionary's own IPA readings
    bare_ok = proper or (w not in ENGLISH_WORDS and not EN_LETTERS.search(w))   # an unmarked English spelling of a
    sf = lambda s: src_form(s, base, proper)                                    # common word is read as English

    def form_of(s):
        f, unm = sf(s)
        if s.foreign and not unm and len(re.findall(r"[aeiou]", strip(base))) > 1:
            stats["kwf/up: stress from a respelling"] += 1
            if len(DEBUG["respelling"]) < 3000:
                DEBUG["respelling"].append((w, s.word, s.respell, f))
        c = wikt_choice(s, base, wk) if not unm else None
        if c and c != f:
            stats["kwf/up: Wiktionary chose among the marked syllables"] += 1
            if len(DEBUG["wikt_choice"]) < 3000:
                DEBUG["wikt_choice"].append((w, s.printed, f, c))
            return c, unm
        return f, unm

    R, key_of = {}, {}                          # reading key -> (form, source, entry); entry -> its reading key
    kwf = pick(S["kwf"])
    for s in kwf:
        f, unm = form_of(s)
        k = reading_key(f)
        if unm and any(not sf(t)[1] and t.pos & s.pos for t in kwf):
            continue                             # an unmarked foreign spelling beside a marked entry of the same class
        R.setdefault(k, (f, "kwf", s)); key_of[s] = k
    up = pick(S["dph"]) or pick(S["up_scan"])
    if up:
        had_kwf = bool(R)
        up_f = sorted(((s, *form_of(s)) for s in up), key=lambda x: x[2])      # marked articles first
        refs = list(kwf) + [s for s, f, u in up_f if reading_key(f) in R]
        for s, f, unm in up_f:
            k = reading_key(f)
            if k in R:
                key_of.setdefault(s, k)
                continue
            # printed without marks or respelling beside the KWF's word of its class: that word (mustang beside mustáng);
            # a respelled foreign word may be another word (UP: book (buk) "aklát" beside boók "beheading")
            m = next((t for t in refs if s.pos & t.pos), None) if unm and had_kwf and not s.respell else None
            if m is None and had_kwf:
                # the KWF's word, or the UP's own copy of a word already taken (nearly the same definition); two UP
                # articles that only share a sense word are the UP's homographs (dagá "lupà"; dagà, a rite | ... | lupà)
                m = same_word(s, kwf, w, ups=refs[len(kwf):])
            elif m is None:                      # UP alone: its own duplicate articles (saksi: saksí)
                m = same_word(s, refs, w, pos_fallback=False) if R else None
            if m is not None:
                old = key_of.get(m)
                if had_kwf and not unm and old in R and R[old][1] == "kwf" and sf(m)[1] and bare_ok:
                    # the KWF prints no stress (Isneg, langawen): the UP's marked form of the word says it; an English
                    # spelling the KWF leaves unmarked (multiple, barometer) is read the English way, whatever the UP marks
                    del R[old]
                    R[k] = (f, "up", s); key_of[s] = k
                    stats["up: stress of an unmarked KWF word"] += 1
                    DEBUG["up_for_unmarked_kwf"].append((w, old, f))
                else:
                    stats["up: same word as KWF's, dropped" if had_kwf else "up: duplicate article, dropped"] += 1
                    if len(DEBUG["up_same"]) < 5000:
                        DEBUG["up_same"].append((w, f, "/".join(v[0] for v in R.values()), s.defs[:70], m.defs[:50], had_kwf))
                continue
            if had_kwf:
                stats["up: another word, added"] += 1
                if len(DEBUG["up_added"]) < 5000:
                    DEBUG["up_added"].append((w, f, "/".join(v[0] for v in R.values()), s.defs[:70]))
            R[k] = (f, "up", s); key_of[s] = k; refs.append(s)
    if R:
        refs = [v[2] for v in R.values()]
        wk_keys = {reading_key(f) for f, ip, r in wk}
        own = set(R) <= wk_keys                 # every KWF/UP reading is one of Wiktionary's readings too
        bare = [k for k, (f, src, s) in R.items() if not s.foreign and sf(s)[1]]    # printed without marks
        wk_ipa, extra = {}, []
        for f, ip, r in wk:
            k = reading_key(f)
            wk_ipa.setdefault(k, ip)
            if k in R or any(k == reading_key(e[0]) for e in extra):
                continue
            other = wikt_other_word(r, w, refs)
            if other is None and own:
                # Wiktionary's own homographs (ate "older sister", atê "dirt"; tapayan "jar", tapayán "bakery"): the
                # KWF and UP give one of its readings and no other, so the other belongs to a word they lack
                other = True
                stats["wiktionary: another homograph, added"] += 1
            if other:                                    # a word the KWF and UP do not list: Wiktionary's reading
                extra.append((f, "wiktionary", ip, first_sense(r)))
                stats["wiktionary: another word, added"] += 1
                if len(DEBUG["wikt_added"]) < 3000:
                    DEBUG["wikt_added"].append((w, f, "/".join(v[0] for v in R.values()), r.get("classe_gramatical") or "", first_sense(r)))
            elif other is None and bare and bare_ok:     # the same word, printed by the KWF or UP without marks (Iba,
                p = pos_set(r.get("classe_gramatical"))  # Cebu, reberensiya): Wiktionary's reading says its stress
                old = next((b for b in bare if R[b][2].pos & p), bare[0])
                bare.remove(old)
                R[k] = (f, "wiktionary", R.pop(old)[2])
                stats["wiktionary: stress of a word KWF/UP print without marks"] += 1
                if len(DEBUG["wikt_for_unmarked"]) < 3000:
                    DEBUG["wikt_for_unmarked"].append((w, old, f, r.get("classe_gramatical") or "", first_sense(r)))
            else:
                stats["wiktionary: same word as KWF's or UP's, dropped"] += 1
                if len(DEBUG["wikt_dropped"]) < 3000:
                    DEBUG["wikt_dropped"].append((w, f, "/".join(v[0] for v in R.values()), r.get("classe_gramatical") or "", first_sense(r)))
        keys = None
        out = []
        for k, (f, src, s) in R.items():
            if keys is None:
                keys = [printed_keys(r, w) for r in recs]
            r = next((r for r, ks in zip(recs, keys) if k in ks), None) or \
                next((r for r in recs if s.pos & pos_set(r.get("classe_gramatical"))), None)
            out.append((f, src, wk_ipa.get(k, ""), first_sense(r) if r else s.defs[:50]))
        return out + extra
    out = []                                    # no KWF or UP entry: English loans and Wiktionary's IPA, then the books
    for r in recs:
        if english_loan(r, r["termo"]):
            out.append(("".join(syllables_of(r, w)), "english", first_ipa(r), first_sense(r)))
    eng = {id(r) for r in recs if english_loan(r, r["termo"])}
    out += [(f, "wiktionary", ip, first_sense(r)) for f, ip, r in wk if id(r) not in eng]
    return out or book_readings(w, recs, loan)


def main():
    src = default_sources()
    ap = argparse.ArgumentParser()
    ap.add_argument("json"); ap.add_argument("--top", type=int, default=20000); ap.add_argument("--out", required=True)
    ap.add_argument("--kwf", nargs="+", default=src["kwf"], help="KWF Diksiyonaryo ng Wikang Filipino (jsonl, app + website)")
    ap.add_argument("--dfe", default=src["dfe"], help="KWF Diksiyonaryong Filipino-English (jsonl)")
    ap.add_argument("--dph", default=src["dph"], help="diksiyonaryo.ph (jsonl)")
    ap.add_argument("--up-scan", default=src["up_scan"], help="up_enrichments.json (the UP dictionary's 2001 print)")
    a = ap.parse_args()
    S = load_sources({"kwf": a.kwf, "dfe": a.dfe, "dph": a.dph, "up_scan": a.up_scan})
    D = json.load(open(a.json, encoding="utf-8"))
    freq = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tl_frequency.json"), encoding="utf-8"))
    rows, stats, agree, diffs = build(D, freq, a.top, S)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write("form\tplain\tstress_source\tipa\trank\tsense\tipa_source\n")
        for r in rows:
            fh.write("\t".join(x.replace("\t", " ") for x in r) + "\n")
    print("rule vs Wiktionary IPA:", dict(agree), "| sample of differences:", diffs[:12])
    print(f"{len({r[1] for r in rows}):,} spellings -> {len(rows):,} forms; {dict(stats)}; -> {a.out}")


def build(D, freq, top, sources=None):
    S = sources if sources is not None else load_sources(default_sources())
    by = collections.defaultdict(list)
    for r in D:
        t = r["termo"]
        if " " in t or len(t) < 2 or not re.fullmatch(r"[A-Za-zÀ-ÿñÑ'\-]+", t):
            continue
        by[strip(t)].append(r)
    KNOWN.clear(); KNOWN.update(w.replace("'", "") for w in by)
    ranked = [w for w, v in sorted(freq.items(), key=lambda kv: kv[1]["rank"]) if w in by]
    if top > 0:
        ranked = ranked[:top]
    else:                                   # --top 0: every spelling, the frequency-ranked ones first, the rest alphabetically
        seen = set(ranked)
        ranked += sorted(w for w in by if w not in seen)
    rows, stats = [], collections.Counter()
    agree, diffs = collections.Counter(), []
    norm = lambda x: re.sub(r"[\[\]/ˌː.\s]", "", x)
    for w in ranked:
        loan = any(LOAN_ETY.search(" ".join(ety_texts(r))) for r in by[w])     # homographs of a loan (mákina) are loans too
        groups = {}
        for r in by[w]:
            groups.setdefault(r["termo"][:1].isupper(), []).append(r)
        cands = []
        for proper, recs in groups.items():
            cands += group_readings(w, recs, proper, len(groups) > 1, S, loan, stats)
        forms = {}                          # one form per reading: letter case (two file names that differ only in case
        for f, src, ipa, sense in cands:    # clash on a case-blind disk) or a redundant acute is not another reading; first wins
            k = reading_key(f)
            if k not in forms:
                forms[k] = [f, src, ipa, sense]
            elif forms[k][0] == f and ipa and not forms[k][2]:     # the same form again, now with Wiktionary's IPA
                forms[k][2] = ipa
        for k, (f, src, ipa, sense) in forms.items():
            g = gen_ipa(f)
            if ipa and g and src in ("kwf", "up", "wiktionary"):    # agreement of the rule with Wiktionary's own reading
                agree["same" if norm(g) == norm(ipa) else "diff"] += 1
                if norm(g) != norm(ipa) and len(diffs) < 40:
                    diffs.append((f, ipa, g))
            final, isrc = (ipa, "dictionary") if ipa else (g, "rule" if re.search(r"[aeiou]", f.lower()) else "spelled")
            rows.append([f, w, src, final, str(freq[w]["rank"]) if w in freq else "", sense, isrc]); stats[src] += 1; stats["ipa_" + isrc] += 1
    return rows, stats, agree, diffs


if __name__ == "__main__":
    main()
