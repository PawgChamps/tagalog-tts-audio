#!/usr/bin/env python3
"""origin.tsv: what the Tagalog to Portuguese dictionary says about where the words of wordlist_all.tsv come from, so that
scripts/fix_ipa.py can tell English loanwords from Tagalog and Spanish words without the 173 MB dictionary.
Usage (from the repository root):  python3 scripts/make_origin.py <tagalog_ptbr_dictionary.json> [--out origin.tsv]
[--list wordlist_all.tsv next/wordlist.tsv]   (the spellings of every list given are covered)

One line per accent-less lowercase spelling of the word list that the dictionary says something about; a spelling that
is not listed has no origin information.  The flags (1 or 0) are the union over every record with that spelling:
  en         a sense tagged emprestimo-ingles, or an etymology that derives the word from English ("Do inglês",
             "Empréstimo do inglês", "Origem: Inglês"), not one that only compares it with English, calls it a calque or
             builds it from a Tagalog affix plus an English word (mag- + inglês comment)
  es         an etymology that names Spanish
  native     an etymology that names an Austronesian ancestor (Proto-Austronesian, Proto-Malayo-Polynesian,
             Proto-Philippine ...), Old Tagalog, or a Tagalog derivation (Derivação morfológica)
  other      an etymology that names another language (Chinese, Hokkien, Malay, Sanskrit, Arabic, Latin, French, Greek,
             Japanese, Kapampangan, Cebuano, Ilocano ...)
  respelled  the dictionary names the English source word and the headword spells it differently (bi from bee, nars from
             nurse, rises from recess): CMUdict's entry for these letters is another word
English evidence is read from the etymology text only: the dictionary's kwf / up / diksiyonaryo_ph fields also list the
English homographs of Tagalog words (at, day, raw), so they only add the other flags."""
import argparse
import json
import re
import unicodedata

EN_FROM = re.compile(r"\b(?:do|da)\s+ingl[eê]s\b((?:\s+(?:médio|antigo|moderno|filipino|americano|norte-americano|britânico|"
                     r"australiano|arcaico|coloquial))*)\s*[“\"']?([A-Za-z][A-Za-z'-]*)?", re.I)
EN_LIST = re.compile(r"origem(?:\s+regional)?\s*:\s*(.*)", re.I)
NOT_SOURCE = re.compile(r"decalque|semântic[oa]s?|influência|influenciad[oa]|possivelmente|provavelmente|talvez|parcial|"
                        r"reduplicação|amálgama|invertid[oa]|sentido|reforçad[oa]|análise|alusão|trocadilho|compar|cf\.|via|"
                        r"letra|substituíd", re.I)
TAGALOG_PART = re.compile(r"\+\s*tagalo|\btagalo\s+[+-]|\b(?:do|de|e)\s+tagalo\b(?!\s+antigo)"          # tagalo + inglês
                          r"|(?<![\w-])(?:i|ini|ika|ipa|ipag|ipang|ma|mag|nag|na|pa|pag|ka|ni|maka|naka|nakaka|paki|mang|nang|"
                          r"pang|pinag|ipina|um)-\s*\+|\+\s*-(?:an|han|in|hin|in-|um-)(?![\w-])", re.I)   # mag- + comment, reply + -an
ES = re.compile(r"espanhol|castelhano", re.I)
NATIVE = re.compile(r"proto-(?:austron|malai|malay|filip|grande filip|greater central|central[- ]philip|northern philip|luzon)"
                    r"|tagalo antigo|herdado d[oa] (?:proto-|grande filipino|tagalo)|derivação morfológica", re.I)
REGIONAL = (r"kapampangan|cebuano|bikol|hiligaynon|waray|ilocano|ilokano|iloko|pangasinense|pangasinan|maranao|maguindanao|"
            r"tausug|ibanag|ivatan|aklanon|ifugao|bontoc|igorrote|palawano|tiruray|kalinga|manobo|tboli|bagobo|subanon|"
            r"kankanaey|bukidnon|romblomanon|ibaloi|higaonon|binukid")
OTHER = re.compile(r"chin[eê]s|hokkien|mandarim|canton[eê]s|hakka|malaio(?!-poli)|javan[eê]s|indon[eé]sio|s[aâ]nscrito|"
                   r"sanskrit|h[ií]ndi|urdu|bengali|t[aâ]mil|persa|[aá]rabe|hebraico|aramaico|turco|n[aá]uatle|qu[ií]chua|tupi|"
                   r"japon[eê]s|coreano|korean|tailand[eê]s|vietnamita|latim|grego|franc[eê]s|italiano|alem[aã]o|holand[eê]s|"
                   r"neerland[eê]s|sueco|noruegu[eê]s|dinamarqu[eê]s|russo|polon[eê]s|ucraniano|basco|catal[aã]o|galego|"
                   r"\b(?:" + REGIONAL + r")\b", re.I)
FLAGS = ("en", "es", "native", "other", "respelled")


def plain(s):
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()


def letters(s):
    return re.sub(r"[^a-z]", "", plain(s))


def english_evidence(text):
    """-> (the text derives the word from English, the English source words it names)"""
    english, sources = False, set()
    for clause in re.split(r"[;|\n]|\.\s", text):
        m = EN_LIST.search(clause)
        if m and re.search(r"(?:^|[\s,(])ingl[eê]s\b", m.group(1), re.I):
            english = True
            continue
        if TAGALOG_PART.search(clause):
            continue
        for f in EN_FROM.finditer(clause):
            if NOT_SOURCE.search(clause[:f.start()]):
                continue
            english = True
            if f.group(2) and letters(f.group(2)):
                sources.add(letters(f.group(2)))
    return english, sources


def respelled(key, sources):
    """the record names English source words and the headword is none of them, an inflection or a clipping of one
    (drugs from drug and disco from discotheque are English spellings; bos from boss and bi from bee are not)"""
    k = letters(key)
    return bool(sources) and all(s != k and not k.startswith(s) and not (s.startswith(k) and len(s) - len(k) >= 3) for s in sources)


def etymology_texts(et):
    """-> (etymology text, the other etymology fields joined)"""
    if isinstance(et, str):
        return et, ""
    if not isinstance(et, dict):
        return (json.dumps(et, ensure_ascii=False) if et else ""), ""
    text = et.get("texto") or ""
    rest = []
    for k in ("cadeia", "kwf", "diksiyonaryo_ph", "up"):
        v = et.get(k)
        rest += [v] if isinstance(v, str) else [str(x) for x in v] if isinstance(v, list) else []
    return (text if isinstance(text, str) else json.dumps(text, ensure_ascii=False)), " | ".join(rest)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("--out", default="origin.tsv")
    ap.add_argument("--list", nargs="+", default=["wordlist_all.tsv"],
                    help="word lists whose spellings to cover (first column: the form); default wordlist_all.tsv")
    a = ap.parse_args()
    need = set()
    for p in a.list:
        need |= {plain(ln.split("\t")[0]) for ln in open(p, encoding="utf-8").read().split("\n")[1:] if ln}
    flags = {}
    for rec in json.load(open(a.json, encoding="utf-8")):
        k = plain(rec.get("termo") or "")
        if k not in need:
            continue
        text, rest = etymology_texts(rec.get("etimologia"))
        f = flags.setdefault(k, set())
        english, src = english_evidence(text)
        if english or any("emprestimo-ingles" in (s.get("etiquetas") or []) for s in rec.get("sentidos") or []):
            f.add("en")
        if respelled(k, src):
            f.add("respelled")
        both = text + " | " + rest
        f.update(name for name, rx in (("es", ES), ("native", NATIVE), ("other", OTHER)) if rx.search(both))
    n = 0
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write("plain\t" + "\t".join(FLAGS) + "\n")
        for k in sorted(flags):
            f = flags[k]
            if f:
                fh.write(k + "\t" + "\t".join("1" if x in f else "0" for x in FLAGS) + "\n")
                n += 1
    print(f"{n:,} of {len(need):,} spellings have origin information -> {a.out}")


if __name__ == "__main__":
    main()
