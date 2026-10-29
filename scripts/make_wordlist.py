#!/usr/bin/env python3
"""Accented spellings for text-to-speech, most frequent words first. One line per reading of a single-word headword:
the accent marks of the Ortograpiyang Pambansa (acute = stress off the penult, grave = penult stress + final glottal,
circumflex = final stress + final glottal), derived from the IPA, from a printed accented headword or from the stress
class. Usage: make_wordlist.py <published json> --top 20000 --out audio/wordlist_top20k.tsv
Columns: form (accented), plain, stress_source (ipa|headword|class|none), ipa, rank, senses (first sense of each record)."""
import argparse
import collections
import json
import re
import sys
import unicodedata
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tagalog_orthography import syllabify  # noqa: E402

ACUTE = {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú"}
GRAVE = {"a": "à", "e": "è", "i": "ì", "o": "ò", "u": "ù"}
CIRC = {"a": "â", "e": "ê", "i": "î", "o": "ô", "u": "û"}
VOW = "aeiou"
LEGACY = {"Freelang", "Calderón 1915", "Nigg 1904", "Tgl-Spa", "Tesauro Filipino", "Thesaurus", "Panganiban", "Guzmán", "Forvo Audio", "Tatoeba", "Wikimedia / Lingua Libre Audio"}


def strip(s):
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn").lower()


def mark_syllable(syl, table):
    for i, ch in enumerate(syl):
        if ch.lower() in VOW:
            m = table[ch.lower()]
            return syl[:i] + (m.upper() if ch.isupper() else m) + syl[i + 1:]
    return syl


def accent(word, syls, stressed, glottal):
    """syls: list of syllables of `word`; stressed: index of the stressed syllable; glottal: final glottal stop."""
    n = len(syls)
    s = list(syls)
    if n == 1:
        if glottal:
            s[0] = mark_syllable(s[0], CIRC)
        return "".join(s)
    if stressed == n - 2:
        if glottal:
            s[-1] = mark_syllable(s[-1], GRAVE)
    elif stressed == n - 1:
        s[-1] = mark_syllable(s[-1], CIRC if glottal else ACUTE)
    else:
        s[stressed] = mark_syllable(s[stressed], ACUTE)
        if glottal:
            s[-1] = mark_syllable(s[-1], GRAVE)
    return "".join(s)


def unaccent(s):
    """Accents off, case kept (the UP syllabification carries stress marks: bú‧kás)."""
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def syllables_of(rec, plain):
    cands = []
    for sy in rec.get("silabacao") or []:
        cands.append([unaccent(p) for p in re.split(r"[‧·.]", sy) if p])
    try:
        cands.append([unaccent(p) for p in syllabify(plain) if p])
    except Exception:
        pass
    for parts in cands:
        if len(parts) > 1 and "".join(parts).lower() == plain and all(re.search(r"[aeiou]", p, re.I) for p in parts):
            return parts
    return [plain]


def stress_from_ipa(ipa):
    """-> (index of the stressed syllable counted by vowel nuclei, final glottal) or None."""
    t = ipa.strip("/[] ")
    if "ˈ" not in t:
        return None
    core = re.sub(r"[ˌ.\s]", "", t)
    before = core.split("ˈ")[0]
    idx = len(re.findall(r"[aeiouɛɔɪʊəɐ]", before))
    return idx, core.rstrip().endswith("ʔ")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("json"); ap.add_argument("--top", type=int, default=20000); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    D = json.load(open(a.json, encoding="utf-8"))
    freq = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tl_frequency.json"), encoding="utf-8"))
    by = collections.defaultdict(list)
    for r in D:
        t = r["termo"]
        if " " in t or len(t) < 2 or not re.fullmatch(r"[A-Za-zÀ-ÿñÑ'\-]+", t):
            continue
        by[strip(t)].append(r)
    ranked = [w for w, v in sorted(freq.items(), key=lambda kv: kv[1]["rank"]) if w in by]
    if a.top > 0:
        ranked = ranked[:a.top]
    else:                                   # --top 0: every spelling, the frequency-ranked ones first, the rest alphabetically
        seen = set(ranked)
        ranked += sorted(w for w in by if w not in seen)
    rows, stats = [], collections.Counter()
    for w in ranked:
        forms = {}
        for r in by[w]:
            t = r["termo"]; sense = r["sentidos"][0]["definicao"][:50] if r["sentidos"] else ""
            ipas = (r.get("pronuncia") or {}).get("ipa") or []
            ton = r.get("tonicidade") or []
            done = False
            legacy_only = all(f in LEGACY for f in (r.get("fontes") or []))
            if t != strip(t) and re.search(r"[áéíóúàèìòùâêîôû]", t) and not legacy_only:   # printed with accents by a real dictionary
                forms.setdefault(t.lower() if not t[0].isupper() or t == t.capitalize() else t, ["headword", ipas[0] if ipas else "", sense]); done = True
            if not done and ipas:
                st = stress_from_ipa(ipas[0])
                if st:
                    syls = syllables_of(r, w)
                    if st[0] < len(syls):
                        forms.setdefault(accent(w, syls, st[0], st[1]), ["ipa", ipas[0], sense]); done = True
            if not done and ton:
                syls = syllables_of(r, w); n = len(syls)
                for c in ton:
                    if c == "malumay": f = accent(w, syls, max(0, n - 2), False)
                    elif c == "mabilis": f = accent(w, syls, n - 1, False)
                    elif c == "malumi": f = accent(w, syls, max(0, n - 2), True)
                    elif c == "maragsa": f = accent(w, syls, n - 1, True)
                    else: continue
                    forms.setdefault(f, ["class", "", sense]); done = True
            if not done:
                forms.setdefault(w, ["none", "", sense])
        has_ipa = any(v[0] == "ipa" for v in forms.values())
        for f, (src, ipa, sense) in forms.items():
            if has_ipa and src == "class":          # the stress class is weaker evidence and usually repeats an IPA reading
                continue
            rows.append([f, w, src, ipa, str(freq[w]["rank"]) if w in freq else "", sense]); stats[src] += 1
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write("form\tplain\tstress_source\tipa\trank\tsense\n")
        for r in rows:
            fh.write("\t".join(x.replace("\t", " ") for x in r) + "\n")
    print(f"{len(ranked):,} spellings -> {len(rows):,} forms; by stress source: {dict(stats)}; -> {a.out}")


if __name__ == "__main__":
    main()
