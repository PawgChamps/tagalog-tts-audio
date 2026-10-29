#!/usr/bin/env python3
"""Clean the `ipa` / `ipa_source` columns of wordlist_all.tsv.  Run from the repository root:

    python3 scripts/fix_ipa.py            # dry run: prints counts and samples, writes nothing
    python3 scripts/fix_ipa.py --write    # rewrites wordlist_all.tsv (then run scripts/build_index.py)
    python3 scripts/fix_ipa.py --list next/wordlist.tsv --out next/wordlist_ipa.tsv   # another list, written elsewhere

Besides the list it reads origin.tsv (what the dictionary says about each word's origin, from scripts/make_origin.py),
the English word list /usr/share/dict/words, CMUdict (`pip install cmudict`), word frequencies (`pip install wordfreq`,
for rule 8) and, when the list has English readings, the list as it was before English readings existed (git history:
wordlist_all.tsv in commit 685c194, and the rebuilt list next/wordlist.tsv in 822ac2e).  Without CMUdict the English readings already in the list are kept or taken back, and none are added;
without wordfreq the same holds for hyphenated forms.  Running it again changes nothing.  What it does, in order:

 dictionary readings (ipa_source = dictionary)
   1. drop notes after the closing slash ("/ˈbas/ (Taglish)");
   2. readings that hold several words ("/ˈɡeŋ ɡeŋ/", garbled reduplications) are rebuilt: by rule for Tagalog spellings,
      from CMUdict for English words, letter by letter for consonant-only abbreviations;
   3. notation brought to the documented style: no syllable dots, no length marks, no tie bars, glide y -> j, ʎ -> lj,
      r -> ɾ; a phonetic reading in square brackets loses its diacritics and lax vowels ([d͡ʒɐnˈɲwaː.ɾɪ] -> dʒanˈjwaɾi);
   4. the stress mark is moved to the start of its syllable when the dictionary's dot had left it after a consonant
      (ʔib.ˈaŋ -> ʔiˈbaŋ); after a hyphen the glottal stop is written (paɡ.ˈaral -> paɡˈʔaɾal);
   4b. two vowels in a row get their glottal stop (kahalataan -> kahalataʔan); a final grave or circumflex accent gets
      its glottal stop (badò -> ˈbadoʔ); readings that lost vowels or read consonant+y as consonant+i (akyat -> ki-at)
      are replaced by the rule reading (a silent final e is not a lost vowel: grace /ˈɡɾejs/, prince, i-sháre);
   5. if the stress still is not on the vowel the accent mark of the spelling names, the rule reading replaces it (in a
      hyphenated form secondary stress on the marked vowel counts: kasû-kasuan /kaˌsuʔkaˈsuʔan/);
   6. English words (below) get their CMUdict reading.
 generated readings (rule / spelled)
   7. English words get their CMUdict reading; the others are regenerated with the current rule.
 English words (ipa_source = english): no accent mark, not a name, a vowel letter (dr and st are not read as drive and
 street), CMUdict has the spelling, and either
   - origin.tsv says English, not Spanish or native, and not respelled from another English word (bi from bee), at any
     length (affixes only when they also look English, as below); or
   - the word is spelled the way only English spells (th, sh, ph, ck, oo, ee, ea, ou, ow, -tion, a final consonant + y),
     is in the English word list and is not a word of Filipino text: origin.tsv merges homographs, so its Spanish or
     native flag does not decide (book, compound, typhoon, industry; noon "back then" stays Tagalog); or
   - no origin information, or only a language other than English, Spanish and Tagalog (chef and boutique: French),
     not given as a variant spelling of another word, and it looks English: a letter or digraph Tagalog does not use,
     six letters or more or a doubled consonant (rule readings), spelling leftovers such as th, ea or ou in the reading
     (dictionary readings), y as the only vowel (gym).  A single word must also be in the English word list; a
     hyphenated form goes on to rule 8.
 hyphenated forms (all sources)
   8. an English reading needs every part to be English: a Tagalog prefix (mag-isa, may-ari, di-tao), a reduplication
      (sama-sama, isa-isa), a Tagalog suffix after the hyphen (bay-an, bak-it), or more parts that are words of Filipino
      than of English text (ari-arian, kilos-mahal) keep the Tagalog reading; a Tagalog prefix on an English word reads
      the prefix the Tagalog way and the word the English way (i-share /ʔiˈʃɛɹ/, mag-tweet /maɡˈtwit/), unless the list
      reads that word the Tagalog way.  Single words are settled first, so that this is known.
 A row that loses its English reading gets back its reading from before English readings, cleaned as above (the rule
 reading if it had no dictionary reading).
"""
import argparse
import os
import re
import subprocess
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(__file__))
import make_ipa as M

try:
    import cmudict
    CMU = cmudict.dict()
except ImportError:
    CMU = {}
try:
    from wordfreq import zipf_frequency
except ImportError:
    zipf_frequency = None

OLD_LIST = "685c194c74c6b51bc24ee55fd40c8c00974f715d"         # wordlist_all.tsv before English readings (same file as 7095dd0^)
REBUILT_LIST = "822ac2e28208300f5bad877ecde60c1aee924c00:next/wordlist.tsv"   # the rebuilt list before English readings
WORD_LIST = "/usr/share/dict/words"
ORIGIN, WORDS = {}, set()          # plain spelling -> origin flags (origin.tsv); English word list
DECIDING = {"en", "es", "native", "respelled"}   # flags that settle English or not; `other` alone (chef: French) does not
HAVE, PENDING = {}, set()          # English readings already in the list (they stand in for CMUdict); rows waiting for it
TAGALOG_PLAIN = set()              # plain spellings of the single words the list reads the Tagalog way (rule 8; filled by run)

VOW = set("aeiouəɛɔɪʊæʌɑɝɚ")
FORM_V = set("aeiou")
ACCENTED = dict(zip("áéíóúàèìòùâêîôû", "aeiouaeiouaeiou"))
GLOTTAL_MARKS = set("àèìòùâêîôû")
FOREIGN_LETTERS = re.compile(r"[cfjqvxz]|ch|sh|th|ph|ck|wh|gh|oo|ee|ou|ea|ow|ie")
LEFTOVER = re.compile(r"th|sh|ch|ck|ph|ea|ou|oo|ee|ie|ui|qu|wh|ow|gh")
CL = {a + b for a in "bkdɡpstfv" for b in "lɾr"}


def plain(s):
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()


def has_accent(form):
    return any(c in ACCENTED for c in form.lower())


def inner_hyphen(form):
    return "-" in form.strip("-")


def tagalog_like(form):
    p = plain(form)
    return not re.search(r"[cfjqvxz]|ch|sh|th|ph|ck|wh|gh", re.sub(r"c(?=[eiy])", "", p)) or has_accent(form)


def form_vowels(form):
    return [(c if c in FORM_V else ACCENTED[c]) for c in form.lower() if c in FORM_V or c in ACCENTED]


def accent_marks(form):
    """indexes (among the spelling's vowels) of vowels that carry an accent mark"""
    return [k for k, c in enumerate(c for c in form.lower() if c in FORM_V or c in ACCENTED) if c in ACCENTED]


def stress_index(body):
    return sum(1 for c in body[:body.index("ˈ")] if c in VOW) if "ˈ" in body else None


def nvow(body):
    return sum(1 for c in body if c in VOW)


# ---------------------------------------------------------------- English from CMUdict
ARPA = {"AA": "ɑ", "AE": "æ", "AH": "ʌ", "AO": "ɔ", "AW": "aʊ", "AY": "aɪ", "EH": "ɛ", "ER": "ɝ", "EY": "eɪ", "IH": "ɪ", "IY": "i",
        "OW": "oʊ", "OY": "ɔɪ", "UH": "ʊ", "UW": "u", "B": "b", "CH": "tʃ", "D": "d", "DH": "ð", "F": "f", "G": "ɡ", "HH": "h",
        "JH": "dʒ", "K": "k", "L": "l", "M": "m", "N": "n", "NG": "ŋ", "P": "p", "R": "ɹ", "S": "s", "SH": "ʃ", "T": "t",
        "TH": "θ", "V": "v", "W": "w", "Y": "j", "Z": "z", "ZH": "ʒ"}
STOPS = set("pbtdkɡf")


def legal_onset(on):
    if len(on) == 1:
        return on[0] != "ŋ"
    if len(on) == 2:
        return (on[0] in STOPS | {"θ", "ʃ"} and on[1] in "lɹwj") or (on[0] == "s" and on[1] in "ptkmnflwj")
    if len(on) == 3:
        return on[0] == "s" and on[1] in "ptk" and on[2] in "lɹwj"
    return False


def cmu_word(word):
    """one English word -> IPA body (no slashes) with ˈ / ˌ before the stressed syllables, or None"""
    prons = CMU.get(word.lower())
    if not prons:
        return None
    segs = []                                        # (symbol, is_vowel, stress)
    for ph in prons[0]:
        m = re.fullmatch(r"([A-Z]+)([012])?", ph)
        base, st = m.group(1), m.group(2)
        if base in ARPA:
            sym = ARPA[base]
            if st is not None:
                if base == "AH" and st == "0":
                    sym = "ə"
                if base == "ER" and st == "0":
                    sym = "ɚ"
            segs.append((sym, st is not None, st))
    out, marks = [s[0] for s in segs], {}
    for i, (sym, isv, st) in enumerate(segs):
        if isv and st in ("1", "2"):
            j = i
            while j > 0 and not segs[j - 1][1]:
                j -= 1
            run = i - j
            if j == 0:
                k = run                              # word-initial cluster all belongs to the first syllable
            else:
                k = min(run, 3)
                while k > 1 and not legal_onset([s[0] for s in segs[i - k:i]]):
                    k -= 1
            marks[i - k] = "ˈ" if st == "1" else "ˌ"
    return "".join(marks.get(i, "") + out[i] for i in range(len(out)))


def cmu_ipa(form):
    parts = [p for p in re.split(r"[-\s]+", form.lower()) if p]
    bodies = [cmu_word(p) for p in parts]
    if not parts or any(b is None for b in bodies):
        return None
    res = bodies[0] + "".join(b.replace("ˈ", "ˌ") for b in bodies[1:])
    if "ˈ" not in res and "ˌ" in res:
        res = res.replace("ˌ", "ˈ", 1)
    if res.count("ˈ") > 1:                               # compounds list several primaries: keep the last one
        head, _, tail = res.rpartition("ˈ")
        res = head.replace("ˈ", "ˌ") + "ˈ" + tail
    return "/" + res + "/"


# ---------------------------------------------------------------- which words get an English reading
ALT_SENSE = re.compile(r"variante de|forma alternativa|grafia alternativa|sinônimo de|"
                       r"(?:grafia|forma) (?:datada|obsoleta|antiga|arcaica) de", re.I)     # Tagalog variants, not English
NAME_SENSE = re.compile(r"sobrenome|prenome|nome pr[óo]prio|nome de (?:homem|mulher|pessoa)|nome masculino|nome feminino|apelido", re.I)


ACRONYM = re.compile(r"^(?:sigla|acr[ôo]nimo)\b", re.I)


def is_name(r):
    return bool(NAME_SENSE.search(r[5])) or r[0][:1].isupper()      # names keep their dictionary / rule reading


def origin_of(r):
    """origin flags of the row: those of its own reading (same sense) when origin.tsv has a line for it, even an empty
    one (its records give no origin), else the spelling's union line"""
    p = plain(r[0])
    return ORIGIN[(p, r[5])] if (p, r[5]) in ORIGIN else ORIGIN.get(p)


EN_ONLY_SPELLING = re.compile(r"th|sh|ph|ck|wh|gh|oo|ee|ea|ou|ow|tions?$|[^aeiouy]y$")   # spellings Tagalog and Spanish don't use


def english_spelled(p):
    """a single word spelled the way only English spells (book, typhoon, industry, satisfaction) that is in the English
    word list and not a word of Filipino text (noon "back then"): English whatever the dictionary's homographs say"""
    return (bool(EN_ONLY_SPELLING.search(p)) and "-" not in p and p in WORDS
            and not (zipf_frequency and zipf_frequency(p, "fil") >= 3.0 and zipf_frequency(p, "fil") >= zipf_frequency(p, "en") + 0.5))


def english_ok(r, looks):
    """may the row have an English reading (when CMUdict has the spelling)?  looks: it looks English (see _fix).
    A hyphenated form that passes is checked again by rule 8 (fix)."""
    form, p = r[0], plain(r[0])
    if has_accent(form) or is_name(r) or not re.search(r"[aeiouy]", p):
        return False
    o = origin_of(r)
    if o and o & DECIDING:                           # the dictionary says whether the word comes from English
        if english_spelled(p) and not ALT_SENSE.search(r[5]):     # its records merge homographs: book (en + native)
            return True
        return "en" in o and not o & {"es", "native", "respelled"} and (looks or not (form.startswith("-") or form.endswith("-")))
    if not looks or ALT_SENSE.search(r[5]):          # no origin, or another language only
        return False
    return inner_hyphen(form) or ("-" not in form and p in WORDS)


def english_reading(r, looks):
    if not english_ok(r, looks):
        return None
    e = HAVE.get(r[0]) or cmu_ipa(r[0])
    if e is None and not CMU:
        PENDING.add(r[0])
    return e


def why_not_english(r):
    """why a row may not have an English reading (for the report)"""
    form, p = r[0], plain(r[0])
    o = origin_of(r)
    if has_accent(form) or is_name(r) or not re.search(r"[aeiouy]", p):
        return "accent mark, name or no vowel"
    if o and o & DECIDING:
        if "en" not in o:
            return "the dictionary gives another origin"
        if o & {"es", "native"}:
            return "the dictionary also gives a Spanish or native origin"
        if "respelled" in o:
            return "respelled from another English word"
        return "hyphenated, not every part is English (rule 8)" if inner_hyphen(form) else "affix"
    if ALT_SENSE.search(r[5]):
        return "no origin information, variant spelling"
    if inner_hyphen(form):
        return "hyphenated, not every part is English (rule 8) or does not look English"
    if "-" in form:
        return "affix, no origin information"
    if p not in WORDS:
        return "no origin information, not in the English word list"
    return "no origin information, does not look English"


# ---------------------------------------------------------------- hyphenated forms (rule 8)
TL_PREFIX = frozenset("""a i ma na ka pa ni mag nag pag ipa ipag maka naka paka makapag nakapag makipag nakipag pakikipag
    pinag ipinag pina ipina mapag napag mang nang pang sang may di de tag taga tig magka nagka pagka magpa nagpa pagpa
    magsi nagsi pinaka ika balik kay mala ala alas""".split())
TL_SUFFIX = frozenset("a o an it ok ay il en ang ing ong as om oy al aw ag at ad ib ip ub ul us ot ap ab ak am og op or et os".split())
EN_DIGRAPH = re.compile(r"th|sh|ch|ph|ck|wh|gh|oo|ee|ea|ou|ow")


def filipino_word(p):
    """a word of three letters or more that is clearly more frequent in Filipino text than in English text"""
    f, e = zipf_frequency(p, "fil"), zipf_frequency(p, "en")
    return len(p) >= 3 and p.isalpha() and f >= 3.0 and f >= e + 0.5


def english_word(p):
    """a word clearly more frequent in English text than in Filipino text, or one CMUdict knows that is spelled the
    English way (a foreign letter or digraph, a doubled consonant) and is not a Filipino word"""
    f, e = zipf_frequency(p, "fil"), zipf_frequency(p, "en")
    if e >= 3.0 and e >= f + 0.5:
        return True
    return bool(cmu_word(p)) and bool(FOREIGN_LETTERS.search(p) or re.search(r"([^aeiou])\1", p)) and not filipino_word(p)


def hyphen_reading(form):
    """rule 8, for a form with an inner hyphen that has an English reading: 'english' (keep it), 'tagalog' (no English
    reading), or the reading of a Tagalog prefix on an English word"""
    parts = [plain(p) for p in form.split("-") if p]
    if parts[0] in TL_PREFIX:
        stem = parts[1:]
        if stem == [parts[-1]] and parts[-1] in TL_SUFFIX:   # pang-al, tig-an: a Tagalog suffix, not English al, an
            return "tagalog"
        if all(p not in TAGALOG_PLAIN and (len(p) == 1 or english_word(p) or (cmu_word(p) and FOREIGN_LETTERS.search(p))
                                            or 3.0 <= zipf_frequency(p, "en") >= zipf_frequency(p, "fil"))
               for p in stem) and cmu_ipa("-".join(stem)):
            pre, eng = M.ipa(parts[0]).strip("/").replace("ˈ", ""), cmu_ipa("-".join(stem)).strip("/")
            if re.match(r"[ˈˌ]?[aeiouəɛɔɪʊæʌɑɝɚ]", eng):     # a vowel after the hyphen starts with a glottal stop
                eng = re.sub(r"^([ˈˌ]?)", r"\1ʔ", eng)
            if "ˈ" not in eng:
                eng = "ˈ" + eng.lstrip("ˌ")
            return "/" + pre + eng + "/"
        return "tagalog"
    if len(set(parts)) == 1:
        return "english" if EN_DIGRAPH.search(parts[0]) or english_word(parts[0]) else "tagalog"
    if parts[-1] in TL_SUFFIX or (parts[-1] in ("in", "on") and zipf_frequency(parts[0], "en") < 4.0):
        return "tagalog"
    if sum(map(filipino_word, parts)) > sum(map(english_word, parts)):
        return "tagalog"
    return "english"


# ---------------------------------------------------------------- dictionary notation
def move_stress(body, form):
    """stress mark left after a consonant by the dictionary's syllable dot -> start of the syllable (or ˈʔ after a hyphen)"""
    i = body.find("ˈ")
    if i <= 0 or i + 1 >= len(body) or body[i + 1] not in VOW:
        return body
    j = i
    while j > 0 and body[j - 1] not in VOW:
        j -= 1
    if j == 0 or j == i:
        return body
    if "-" in form:
        return body[:i] + "ˈʔ" + body[i + 1:]
    units = re.findall(r"tʃ|dʒ|.", body[j:i])
    k = 2 if len(units) >= 2 and units[-2] + units[-1] in CL else 1
    return body[:j] + "".join(units[:-k]) + "ˈ" + "".join(units[-k:]) + body[i + 1:]


BROAD = {"ɐ": "a", "ə": "a", "ɪ": "i", "ɛ": "e", "ʊ": "u", "ɔ": "o", "ɲ": "nj"}


def broad(body):
    """a phonetic reading in square brackets ([d͡ʒɐnˈɲwaː.ɾɪ]) -> the broad style (dʒanˈjwaɾi): no diacritics, the five
    vowels, nj for ɲ"""
    body = "".join(c for c in unicodedata.normalize("NFD", body.strip("[]")) if unicodedata.category(c) != "Mn" or c == "͡")
    body = re.sub(r"n([ˈˌ]?)ɲ", r"n\1j", body)            # n + ɲ is n + the glide
    return unicodedata.normalize("NFC", "".join(BROAD.get(c, c) for c in body))


def normalise(body):
    body = body.replace("͡", "").replace("ː", "").replace("·", "").replace("ʎ", "lj")
    out = []
    for i, c in enumerate(body):                       # IPA y is a vowel: a glide next to a vowel is j, otherwise it stands for i
        if c == "y":
            near = (i > 0 and body[i - 1] in VOW) or (i + 1 < len(body) and body[i + 1] in VOW)
            c = "j" if near else "i"
        out.append(c)
    return "".join(out)


def hiatus(body):
    """two vowels in a row are separate syllables in Tagalog: write the glottal stop the style asks for (kahalataan -> kahalataʔan)"""
    body = re.sub(r"([aeiou])(?=[aeiou])", r"\1ʔ", body)
    return re.sub(r"([aeiou])([ˈˌ])(?=[aeiou])", r"\1\2ʔ", body)


def broken(form, body):
    """a reading that cannot be right for a Tagalog spelling: fewer vowels than the spelling has vowel groups (lost vowels),
    or more vowels than letters because a consonant + y was read as consonant + i (akyat -> ki-at).  A silent final e
    after a consonant is not a lost vowel (grace /ˈɡɾejs/, prince, hope, Hillside, i-sháre)."""
    n = nvow(body.replace("ʔ", ""))
    groups = len(re.findall(r"[aeiouáéíóúàèìòùâêîôû]+", form.lower()))
    silent = len(re.findall(r"(?<=[^aeiouáéíóúàèìòùâêîôû\W])e(?=$|-)", form.lower())) if body.rstrip("ʔ")[-1:] not in VOW else 0
    if n < groups - silent:
        return True
    return n > len(form_vowels(form)) and bool(re.search(r"[bdfghklmnprstvwz]y[aeiouáéíóúàèìòùâêîôû]", form.lower()))


def stress_ok(form, body):
    """True when the reading stresses a vowel that the accent marks of the spelling allow: an acute or circumflex marks the
    stressed vowel itself, a final grave means penultimate stress, a non-final grave marks the vowel.  Words with several
    marks (présidént) allow any of them; loanwords whose vowel structure differs are not compared."""
    chars = [c for c in form.lower() if c in FORM_V or c in ACCENTED]
    if not any(c in ACCENTED for c in chars) or "ˈ" not in body:
        return True
    if nvow(body.replace("ʔ", "")) != len(chars):
        return True
    n, ok = len(chars), set()
    for k, c in enumerate(chars):
        if c in ACCENTED:
            ok.add(max(0, n - 2) if (c in "àèìòù" and k == n - 1) else k)
    if stress_index(body) in ok:
        return True
    secondary = {sum(1 for c in body[:i] if c in VOW) for i, c in enumerate(body) if c == "ˌ"}
    return "-" in form and bool(secondary & ok)        # kasû-kasuan /kaˌsuʔkaˈsuʔan/: the marked part has secondary stress


def _fix(r, allow_english=True):
    form, src, ipa = r[0], r[6], r[3]
    new, nsrc, why = ipa, src, None
    if src == "english":                               # decided in run(): kept, or taken back to the earlier reading
        return new, nsrc, why
    if src == "dictionary":
        m = re.match(r"(/[^/]*/)", ipa)
        body = m.group(1).strip("/") if m else ipa.strip("/")
        if m and m.group(1) != ipa:
            why = "note removed"
        multi = " " in body
        dots = "." in body
        if multi or "ʎ" in body:
            e = english_reading(r, True) if allow_english else None
            if e:
                new, nsrc, why = e, "english", "multi-word/ly reading rebuilt from CMUdict"
            elif re.search(r"[aeiou]", plain(form)):
                new, nsrc, why = M.ipa(form), "rule", "multi-word/ly reading rebuilt by rule"
            else:
                new, nsrc, why = M.spelled(form), "spelled", "multi-word reading spelled by letters"
        else:
            if body.startswith("[") and body.endswith("]"):
                body, why = broad(body), "phonetic reading made broad"
            body = normalise(body)
            if "." in body:
                body = body.replace(".", "")
            nb = move_stress(body, form)
            raw = nb                                       # before the glottal stops: spelling leftovers show here
            tl = tagalog_like(form)
            if tl:
                nb = hiatus(nb)
            glottal = form[-1:].lower() in GLOTTAL_MARKS and not nb.endswith("ʔ")
            if glottal:
                nb += "ʔ"
            tapped = nb.replace("r", "ɾ")
            new = "/" + tapped + "/"
            if new != ipa:
                why = why or ("notation" if dots else "final glottal stop added" if glottal else
                              "r written as ɾ" if "/" + nb + "/" == ipa else "cleaned")
            nb = tapped
            looks = bool(LEFTOVER.search(raw) or (not tl and re.search(r"[aeiou][aeiou]", raw)))
            e = english_reading(r, looks) if allow_english else None
            if e:
                new, nsrc, why = e, "english", "spelling leftovers in reading" if looks else "English loanword (dictionary reading)"
            elif tl and broken(form, nb) and re.search(r"[aeiou]", plain(form)):
                rule = M.ipa(form)
                if nvow(rule.replace("ʔ", "")) == len(form_vowels(form)):
                    new, nsrc, why = rule, "rule", "reading lost vowels or read consonant+y as consonant+i"
            elif tl and not stress_ok(form, nb):
                rule = M.ipa(form)
                if nvow(rule.replace("ʔ", "")) == len(form_vowels(form)):
                    new, nsrc, why = rule, "rule", "stress did not match the accent mark"
    else:                                                # rule / spelled
        p = plain(form)
        if ACRONYM.search(r[5]) and re.fullmatch(r"[a-z]{2,6}", p) and not has_accent(form):
            g = M.spelled(form)                          # gma, npa, ust: said letter by letter
            return g, "spelled", None if (g, "spelled") == (ipa, src) else "acronym read letter by letter"
        looks_english = FOREIGN_LETTERS.search(p) or (src == "spelled" and "y" in p) or (
            src == "rule" and (len(p) >= 6 or re.search(r"([^aeiou])\1", p)) and not ALT_SENSE.search(r[5]))   # long / doubled consonant
        e = english_reading(r, bool(looks_english)) if allow_english else None
        if e:
            new, nsrc, why = e, "english", "English loanword"
        if nsrc == src:                                  # regenerate with the corrected rule
            vowelless = not re.search(r"[aeiou]", plain(form))
            g = M.spelled(form) if vowelless else M.ipa(form)
            nsrc = "spelled" if vowelless else "rule"
            if g and (g != ipa or nsrc != src):
                new, why = g, "rule updated" if g != ipa else "label corrected (spelled -> rule)"
    return new, nsrc, why


def fix(r):
    """_fix, then rule 8 for a hyphenated form that would get an English reading"""
    new, nsrc, why = _fix(r)
    if nsrc == "english" and r[6] != "english" and inner_hyphen(r[0]):
        if not (CMU and zipf_frequency):             # rule 8 needs both: keep the reading the list has, add none
            return (new, nsrc, why) if r[0] in HAVE else _fix(r, allow_english=False)
        h = hyphen_reading(r[0])
        if h == "tagalog":
            return _fix(r, allow_english=False)
        if h != "english":
            return h, "english", "Tagalog prefix on an English word"
    return new, nsrc, why


def settle(r):
    """apply fix() until the row no longer changes (a rule reading can still be an English word) -> (row, last reason)"""
    r, why = list(r), None
    for _ in range(4):
        new, nsrc, w = fix(r)
        if new == r[3] and nsrc == r[6]:
            break
        r[3], r[6], why = new, nsrc, w
    return r, why


def load_inputs(origin="origin.tsv"):
    if not os.path.exists(origin):
        sys.exit(f"{origin} is missing: run scripts/make_origin.py <dictionary json> first")
    lines = open(origin, encoding="utf-8").read().split("\n")
    head = lines[0].split("\t")
    by_sense = len(head) > 1 and head[1] == "sense"      # plain, sense, flags...: one line per reading, plus the union
    names = head[2 if by_sense else 1:]
    for ln in lines[1:]:
        if ln:
            f = ln.split("\t")
            key = (f[0], f[1]) if by_sense and f[1] else f[0]
            ORIGIN[key] = {n for n, v in zip(names, f[2 if by_sense else 1:]) if v == "1"}
    try:
        WORDS.update(w.strip() for w in open(WORD_LIST, encoding="utf-8", errors="ignore"))
    except OSError:
        sys.exit(f"the English word list {WORD_LIST} is missing (apt install wamerican)")


def old_list():
    """form -> rows it had before English readings existed: in the rebuilt list (next/wordlist.tsv as committed) and in
    wordlist_all.tsv before the first English readings.  pick() takes the one that is the same reading."""
    old = {}
    for spec in (REBUILT_LIST, OLD_LIST + ":wordlist_all.tsv"):
        try:
            txt = subprocess.run(["git", "show", spec], capture_output=True, check=True).stdout.decode("utf-8")
        except (OSError, subprocess.CalledProcessError) as e:
            sys.exit(f"needs the git history to recheck the English readings (git show {spec[:7]}{spec[40:]}): {e}")
        for r in (ln.split("\t") for ln in txt.split("\n")[1:] if ln):
            old.setdefault(r[0], []).append(r)
    return old


def pick(r, rows):
    """the earlier row of the same reading: same stress source and sense, else the first (the rebuilt list's)"""
    return next((o for o in rows if o[2] == r[2] and o[5] == r[5]), rows[0]) if rows else None


def run(rows):
    """rows of the list -> (fixed rows, {reason: [(form, before, after)]}, English readings kept).  Single words go first:
    rule 8 needs to know which of them the list reads the Tagalog way."""
    HAVE.clear(); PENDING.clear(); TAGALOG_PLAIN.clear()
    HAVE.update({r[0]: r[3] for r in rows if r[6] == "english"})
    old = old_list() if HAVE else {}
    out, changes, kept = [None] * len(rows), {}, 0
    for hyphenated in (False, True):
        if hyphenated:
            TAGALOG_PLAIN.update(plain(r[0]) for r in out if r is not None and r[6] != "english")
        for i, r in enumerate(rows):
            if inner_hyphen(r[0]) != hyphenated:
                continue
            r = list(r)
            first = r[3]
            if r[6] == "english":                        # recheck from the reading it had before English readings
                o = pick(r, old.get(r[0]))
                start = r[:3] + [o[3]] + r[4:6] + [o[6]] if o else r[:3] + [M.ipa(r[0]) or M.spelled(r[0])] + r[4:6] + ["rule"]
                s, why = settle(start)
                if s[6] == "english":
                    kept += 1
                    if s[3] == first:
                        why = None
                else:
                    why = "English reading taken back: " + why_not_english(r)
                r[3], r[6] = s[3], s[6]
            else:
                s, why = settle(r)
                r[3], r[6] = s[3], s[6]
            if why:
                changes.setdefault(why, []).append((r[0], first, r[3]))
            out[i] = r
    return out, changes, kept


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="rewrite the list (or write --out)")
    ap.add_argument("--list", default="wordlist_all.tsv")
    ap.add_argument("--origin", default="origin.tsv")
    ap.add_argument("--out", default="", help="write the fixed list here instead of over --list (implies --write)")
    a = ap.parse_args()
    write, out_path = a.write or bool(a.out), a.out or a.list
    lines = open(a.list, encoding="utf-8").read().split("\n")
    header, body = lines[0], lines[1:]
    if body and body[-1] == "":
        body.pop()
    rows = [ln.split("\t") for ln in body]
    for r in rows:
        assert len(r) == 7, "\t".join(r)[:80]
    load_inputs(a.origin)
    if not CMU:
        print("CMUdict is not installed (pip install cmudict): English readings are kept or taken back, none are added")
    if zipf_frequency is None:
        print("wordfreq is not installed (pip install wordfreq): hyphenated forms keep the English readings they have, none are added")
    out, changes, kept = run(rows)
    for k, v in sorted(changes.items(), key=lambda kv: -len(kv[1])):
        print(f"{len(v):7}  {k}")
        for s in v[:4]:
            print(f"           {s[0]}   {s[1]}  ->  {s[2]}")
    back = sum(len(v) for k, v in changes.items() if k.startswith("English reading taken back"))
    print(f"English readings: {kept:,} kept, {back:,} taken back, {sum(r[6] == 'english' for r in out) - kept:,} added")
    waiting = sum(1 for r in out if r[0] in PENDING and r[6] != "english")
    if waiting:
        print(f"up to {waiting:,} rows get an English reading where CMUdict has the spelling (run with CMUdict and wordfreq installed)")
    print("ipa_source: " + ", ".join(f"{s} {sum(r[6] == s for r in out):,}" for s in ("dictionary", "rule", "english", "spelled")))
    if write:
        open(out_path, "w", encoding="utf-8").write("\n".join([header] + ["\t".join(r) for r in out]) + "\n")
        print(f"{out_path} written" + ("; now run scripts/build_index.py" if out_path == "wordlist_all.tsv" else ""))


if __name__ == "__main__":
    main()
