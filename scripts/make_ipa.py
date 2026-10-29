#!/usr/bin/env python3
"""Phonemic IPA for a Tagalog word written with the accent marks of the Ortograpiyang Pambansa, in the style of the
dictionary's own readings (/kuˈmaʔin/, /ˈbahaj/, /ŋaˈjon/): no length marks, no syllable dots, ˈ before the stressed
syllable, ʔ for word-initial vowels, between vowels in hiatus and after a final grave or circumflex accent.
  á é í ó ú  stress on that syllable, no final glottal      à è ì ò ù  (final) penult stress + final glottal
  â ê î ô û  (final) final stress + final glottal           no mark    penult stress (malumay)
ipa(form) -> '/.../'"""
import re
import unicodedata

ACUTE = dict(zip("áéíóú", "aeiou")); GRAVE = dict(zip("àèìòù", "aeiou")); CIRC = dict(zip("âêîôû", "aeiou"))
VOWELS = set("aeiou")
UNITS = ["ng", "ts"]                            # digraphs read as one consonant (ny, sy, dy, ly are n+j, s+j... as in the dictionary)
MAP = {"ng": "ŋ", "ts": "tʃ", "sy": "ʃ", "dy": "dʒ", "ny": "ɲ", "g": "ɡ", "y": "j", "r": "ɾ", "c": "k", "q": "k", "ñ": "ɲ",
       "j": "dʒ", "x": "ks", "'": "", "’": ""}
ONSET_CLUSTERS = {a + b for a in "bkdgpstfv" for b in "lr"}


def tokens(word):
    """-> list of (kind, text, mark) with kind 'V' (vowel, mark = None|'acute'|'grave'|'circ') or 'C' or '-' (boundary)."""
    out, i, w = [], 0, word.lower()
    while i < len(w):
        ch = w[i]
        if ch in ACUTE or ch in GRAVE or ch in CIRC:
            kind = "acute" if ch in ACUTE else "grave" if ch in GRAVE else "circ"
            out.append(("V", (ACUTE | GRAVE | CIRC)[ch], kind)); i += 1
        elif ch in VOWELS:
            out.append(("V", ch, None)); i += 1
        elif ch in "-‧·":
            out.append(("-", "", None)); i += 1
        elif w[i:i + 2] in UNITS:
            out.append(("C", w[i:i + 2], None)); i += 2
        elif ch.isalpha() or ch in "'’":
            out.append(("C", unicodedata.normalize("NFD", ch)[0], None)); i += 1
        else:
            i += 1
    return out


def syllabify(toks):
    """-> list of syllables, each {'onset': [C...], 'nucleus': (v, mark), 'coda': [C...], 'glottal_onset': bool}."""
    sylls, cur = [], None
    pending = []          # consonants waiting to be assigned
    boundary = False
    for kind, text, mark in toks:
        if kind == "-":
            if cur is not None:                 # consonants before the hyphen close the syllable before it
                cur["coda"] += pending; pending = []
            boundary = True; continue
        if kind == "C":
            pending.append(text); continue
        # a vowel: close the previous syllable with part of the pending consonants
        if cur is None:
            onset = pending
            cur = {"onset": list(onset), "nucleus": (text, mark), "coda": [], "hiatus": False}
        else:
            k = len(pending)
            if boundary:
                onset = pending                 # everything after a hyphen starts the next syllable
            elif k == 0:
                onset = []
            elif k == 1:
                onset = pending
            elif k == 2:
                onset = pending if (pending[0] + pending[1]) in ONSET_CLUSTERS else pending[1:]
                cur["coda"] += pending[:len(pending) - len(onset)]
            else:
                tail = pending[-2:] if (pending[-2] + pending[-1]) in ONSET_CLUSTERS else pending[-1:]
                cur["coda"] += pending[:len(pending) - len(tail)]; onset = tail
            sylls.append(cur)
            cur = {"onset": list(onset), "nucleus": (text, mark), "coda": [], "hiatus": not onset}
        pending = []; boundary = False
    if cur is None:
        return []
    cur["coda"] += pending
    sylls.append(cur)
    return sylls


LETTER_NAMES = {"a": "ʔei", "b": "bi", "c": "si", "d": "di", "e": "ʔi", "f": "ʔef", "g": "dʒi", "h": "ʔeitʃ", "i": "ʔai", "j": "dʒei",
                "k": "kei", "l": "ʔel", "m": "ʔem", "n": "ʔen", "o": "ʔo", "p": "pi", "q": "kju", "r": "ʔaɾ", "s": "ʔes", "t": "ti",
                "u": "ju", "v": "vi", "w": "dabəlju", "x": "ʔeks", "y": "wai", "z": "zi"}


def spelled(form):
    """Consonant-only forms (tv, dr, gym): read letter by letter, the last letter stressed; 'ng' is the particle (nang)."""
    f = re.sub(r"[^a-z]", "", unicodedata.normalize("NFD", form.lower()))
    if f == "ng":
        return "/ˈnaŋ/"
    names = [LETTER_NAMES[c] for c in f if c in LETTER_NAMES]
    return "/" + "".join(names[:-1]) + "ˈ" + names[-1] + "/" if names else ""


EXCEPTIONS = {"mga": "/maˈŋa/", "mgá": "/maˈŋa/", "ng": "/ˈnaŋ/", "ngá": "/ˈŋa/", "ang": "/ˈʔaŋ/", "ñga": "/ˈŋa/"}


def ipa(form):
    if form.lower() in EXCEPTIONS:
        return EXCEPTIONS[form.lower()]
    toks = tokens(form)
    sylls = syllabify(toks)
    if not sylls:
        return spelled(form)
    n = len(sylls)
    stress, glottal, explicit = max(0, n - 2), False, False
    for i, s in enumerate(sylls):
        m = s["nucleus"][1]
        if m == "acute":
            stress, explicit = i, True
        elif m == "circ":
            stress, explicit = i, True
            if i == n - 1:
                glottal = True
        elif m == "grave":
            if i == n - 1:
                glottal = True                  # final grave: glottal stop; stress stays penult unless an earlier acute set it
                if not explicit:
                    stress = max(0, n - 2)
            elif not explicit:
                stress, explicit = i, True
    parts = []
    for i, s in enumerate(sylls):
        seg = ""
        if not s["onset"] and (i == 0 or s["hiatus"]):
            seg += "ʔ"
        seg += "".join(MAP.get(c, c) for c in s["onset"]) + s["nucleus"][0] + "".join(MAP.get(c, c) for c in s["coda"])
        parts.append(("ˈ" if i == stress else "") + seg)
    res = "".join(parts)
    if glottal and not res.endswith("ʔ"):
        res += "ʔ"
    return "/" + res + "/"


if __name__ == "__main__":
    import sys
    for w in sys.argv[1:]:
        print(w, ipa(w))
