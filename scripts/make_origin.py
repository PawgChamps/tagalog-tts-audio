#!/usr/bin/env python3
"""origin.tsv: what the Tagalog to Portuguese dictionary says about where the words of the word lists come from, so that
scripts/fix_ipa.py can tell English loanwords from Tagalog and Spanish words without the 173 MB dictionary.
Usage (from the repository root):  python3 scripts/make_origin.py <tagalog_ptbr_dictionary.json> [--out origin.tsv]
[--list wordlist_all.tsv next/wordlist.tsv]   (the spellings of every list given are covered)

Columns: plain, sense, en, es, native, other, respelled.
  plain  the accent-less lowercase spelling
  sense  the first 50 characters of a dictionary record's first sense, exactly as the sense column of the word lists
         gives it for the readings taken from that record; empty on the spelling's union line (every record of it)
Look a reading up by (plain, sense) first and by (plain, "") second.  A (plain, sense) line is written only where the
records with that first sense say something other than the union; a line of zeros there means that those records give
no origin, so the reading is like a spelling with no line at all: no origin information.

Flags (1 or 0):
  en         a sense tagged emprestimo-ingles, or an etymology that derives the word from English ("Do inglês",
             "Empréstimo do inglês", "Origem: Inglês"), not one that only compares it with English, calls it a calque or
             builds it from a Tagalog affix plus an English word (mag- + inglês comment)
  es         an etymology that names Spanish
  native     an etymology that names an Austronesian ancestor (Proto-Austronesian, Proto-Malayo-Polynesian,
             Proto-Philippine ...), a Tagalog derivation (Derivação morfológica: pang + tama), or Old Tagalog when the
             spelling uses only Tagalog letters: no c, f, j, q, v, x, z and no doubled consonant but rr (diksiyonaryo.ph
             tags mess, off-white, Messiah, Mexico and optical [ST])
  other      an etymology that names another language (Chinese, Hokkien, Malay, Sanskrit, Arabic, Latin, French, Greek,
             Japanese, Kapampangan, Cebuano, Ilocano ...)
  respelled  the dictionary names the English source word and the headword spells it differently (bi from bee, nars from
             nurse, rises from recess): CMUdict's entry for these letters is another word

Which statements count:
  - English evidence is read from the etymology text only: the dictionary's kwf / up / diksiyonaryo_ph fields also list
    the English homographs of Tagalog words (at, day, raw), so they only add the other flags.
  - The languages named after an English source word are its ancestors ("Empréstimo do inglês apartment, do francês
    appartement, do italiano appartamento, do espanhol apartamiento"), and so is the Wiktionary etymology tree (cadeia)
    of a word whose text derives it from English: neither counts.
  - Within one record's text the sources keep the word list's order: a KWF statement ("Do inglês") silences the UP ones
    ("Origem: Espanhol"), and the book notes ("Do espanhol ábaco (Vicassan)") count only when neither gives one
    (compound: KWF English, UP [Esp]).
  - A UP tag with several languages ("Cognato / Origem regional: Espanhol, Inglês", printed [Esp Ing]) counts only when
    no other statement about the same records names a language (job, impromptu); the emprestimo-ingles tag is not
    one, because the dictionary gives it for [Esp Ing] words too (banana, honor, color stay Spanish).
"""
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
                    r"|herdado d[oa] (?:proto-|grande filipino|tagalo)|derivação morfológica", re.I)
OLD_TAGALOG = re.compile(r"tagalo antigo", re.I)
REGIONAL = (r"kapampangan|cebuano|bikol|hiligaynon|waray|ilocano|ilokano|iloko|pangasinense|pangasinan|maranao|maguindanao|"
            r"tausug|ibanag|ivatan|aklanon|ifugao|bontoc|igorrote|palawano|tiruray|kalinga|manobo|tboli|bagobo|subanon|"
            r"kankanaey|bukidnon|romblomanon|ibaloi|higaonon|binukid")
OTHER = re.compile(r"chin[eê]s|hokkien|mandarim|canton[eê]s|hakka|malaio(?!-poli)|javan[eê]s|indon[eé]sio|s[aâ]nscrito|"
                   r"sanskrit|h[ií]ndi|urdu|bengali|t[aâ]mil|persa|[aá]rabe|hebraico|aramaico|turco|n[aá]uatle|qu[ií]chua|tupi|"
                   r"japon[eê]s|coreano|korean|tailand[eê]s|vietnamita|latim|grego|franc[eê]s|italiano|alem[aã]o|holand[eê]s|"
                   r"neerland[eê]s|sueco|noruegu[eê]s|dinamarqu[eê]s|russo|polon[eê]s|ucraniano|basco|catal[aã]o|galego|"
                   r"\b(?:" + REGIONAL + r")\b", re.I)
FLAGS = ("en", "es", "native", "other", "respelled")
CLAUSES = re.compile(r"[;|\n]|\.\s")
ANCESTORS = re.compile(r"(?:\s*,\s*(?:do|da|de)\s+[^,]*)+")          # ", do francês appartement, do italiano appartamento"
# kinds of statement, in the order of the sources inside one record's text
KWF, UP, TEXT, BOOK, COGNATE, FIELD, TAG = range(7)


def plain(s):
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()


def letters(s):
    return re.sub(r"[^a-z]", "", plain(s))


def old_tagalog_spelling(key):
    """Old Tagalog ([ST] in the UP dictionary) is written with the Tagalog letters: no c, f, j, q, v, x or z, and no
    doubled consonant but rr (kur•rúk•san); ng is one letter (gang•gáng, li•ngín•ngin)"""
    return not any(re.search(r"[cfjqvxz]|([bdghklmnpstwyN])\1", w.replace("ng", "N")) for w in re.findall(r"[a-z]+", plain(key)))


def kind(clause):
    s = clause.strip()
    if re.match(r"cognato\b", s, re.I):
        return COGNATE                               # UP tag with several languages: [Esp Ing]
    if re.match(r"origem\s*:", s, re.I):
        return UP                                    # UP (diksiyonaryo.ph or the 2001 print): [Esp]
    if re.search(r"\((?:Vicassan|Leo English)\)$", s):
        return BOOK                                  # "Do espanhol ábaco (Vicassan)"
    if re.fullmatch(r"Do [^,.;:()]+", s):
        return KWF                                   # DWF / DFE: "Do inglês", "Do espanhol fotografía"
    return TEXT                                      # Wiktionary's etymology and anything else


def clause_flags(clause, key, english_text=True):
    """-> (flags, English source words) of one statement"""
    f, src, scan = set(), set(), clause
    if english_text:
        m = EN_LIST.search(clause)
        if m and re.search(r"(?:^|[\s,(])ingl[eê]s\b", m.group(1), re.I):
            f.add("en")
        elif not TAGALOG_PART.search(clause):
            for e in EN_FROM.finditer(clause):
                if NOT_SOURCE.search(clause[:e.start()]):
                    continue
                if "en" not in f:                    # what follows the English source word: its ancestors
                    tail = re.sub(r"\s*\([^()]*\)", "", clause[e.end():])
                    a = ANCESTORS.match(tail)
                    scan = clause[:e.end()] + (tail[a.end():] if a else tail)
                f.add("en")
                if e.group(2) and letters(e.group(2)):
                    src.add(letters(e.group(2)))
    f.update(name for name, rx in (("es", ES), ("native", NATIVE), ("other", OTHER)) if rx.search(scan))
    if OLD_TAGALOG.search(scan) and old_tagalog_spelling(key):
        f.add("native")
    return f, src


def respelled(key, sources):
    """the record names English source words and the headword is none of them, an inflection or a clipping of one
    (drugs from drug and disco from discotheque are English spellings; bos from boss and bi from bee are not)"""
    k = letters(key)
    return bool(sources) and all(s != k and not k.startswith(s) and not (s.startswith(k) and len(s) - len(k) >= 3) for s in sources)


def etymology_texts(et):
    """-> (etymology text, Wiktionary etymology tree, [the kwf / diksiyonaryo_ph / up fields])"""
    if isinstance(et, str):
        return et, "", []
    if not isinstance(et, dict):
        return (json.dumps(et, ensure_ascii=False) if et else ""), "", []
    text = et.get("texto") or ""
    text = text if isinstance(text, str) else json.dumps(text, ensure_ascii=False)
    parts = []
    for k in ("cadeia", "kwf", "diksiyonaryo_ph", "up"):
        v = et.get(k)
        parts.append(" | ".join([v] if isinstance(v, str) else [str(x) for x in v] if isinstance(v, list) else []))
    return text, parts[0], [p for p in parts[1:] if p]


def statements(rec, key):
    """-> [(kind, flags, English source words)] of one dictionary record"""
    text, tree, fields = etymology_texts(rec.get("etimologia"))
    out = []
    for c in CLAUSES.split(text):
        if c.strip():
            out.append((kind(c),) + clause_flags(c, key))
    from_english = any("en" in f for k, f, s in out)
    for part in ([] if from_english else [tree]) + fields:
        for c in CLAUSES.split(part):
            if c.strip():
                out.append((COGNATE if kind(c) == COGNATE else FIELD, clause_flags(c, key, english_text=False)[0], set()))
    if any("emprestimo-ingles" in (s.get("etiquetas") or []) for s in rec.get("sentidos") or []):
        out.append((TAG, {"en"}, set()))
    return out


def resolve(key, recs):
    """-> the flags of some records of one spelling (each a list of statements)"""
    # the emprestimo-ingles tag does not count here: the dictionary also gives it for [Esp Ing] (banana, honor, color)
    others_name_one = any(f for st in recs for k, f, s in st if k not in (COGNATE, TAG))
    flags = set()
    for st in recs:
        named = [s for s in st if s[1]]
        texts = [s for s in named if s[0] in (KWF, UP, TEXT, BOOK)]
        best = min((s[0] for s in texts), default=None)
        keep = [s for s in texts if s[0] == best] + [s for s in named if s[0] in (FIELD, TAG)]
        if not others_name_one:
            keep += [s for s in named if s[0] == COGNATE]
        for s in keep:
            flags |= s[1]
        if respelled(key, set().union(*(s[2] for s in keep))):
            flags.add("respelled")
    return flags


def first_sense(rec):
    """the sense column of the word lists for the readings taken from this record (make_wordlist.first_sense)"""
    s = rec.get("sentidos")
    return (s[0]["definicao"][:50] if s else "").replace("\t", " ")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("--out", default="origin.tsv")
    ap.add_argument("--list", nargs="+", default=["wordlist_all.tsv"],
                    help="word lists whose spellings to cover (first column: the form, sixth: the sense); default wordlist_all.tsv")
    a = ap.parse_args()
    need, rows = set(), []
    for p in a.list:
        for ln in open(p, encoding="utf-8").read().split("\n")[1:]:
            if ln:
                c = ln.split("\t")
                need.add(plain(c[0]))
                rows.append((plain(c[0]), c[5] if len(c) > 5 else ""))
    recs = {}
    for rec in json.load(open(a.json, encoding="utf-8")):
        k = plain(rec.get("termo") or "")
        if k in need:
            recs.setdefault(k, []).append((first_sense(rec), statements(rec, k)))
    lines = []
    for k in sorted(recs):
        union = resolve(k, [st for s, st in recs[k]])
        if union:
            lines.append((k, "", union))
        by_sense = {}
        for s, st in recs[k]:
            if s:
                by_sense.setdefault(s, []).append(st)
        for s in sorted(by_sense):
            f = resolve(k, by_sense[s])
            if f != union:
                lines.append((k, s, f))
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write("plain\tsense\t" + "\t".join(FLAGS) + "\n")
        for k, s, f in lines:
            fh.write(f"{k}\t{s}\t" + "\t".join("1" if x in f else "0" for x in FLAGS) + "\n")
    have = {(k, s) for k, s, f in lines}
    n_sense = sum(1 for p, s in rows if s and (p, s) in have)
    n_union = sum(1 for p, s in rows if not (s and (p, s) in have) and (p, "") in have)
    unions = [f for k, s, f in lines if not s]
    print(f"{len(unions):,} of {len(need):,} spellings have origin information, plus "
          f"{len(lines) - len(unions):,} sense lines that differ from their union -> {a.out}")
    print("union lines per flag: " + ", ".join(f"{x} {sum(x in f for f in unions):,}" for x in FLAGS))
    print(f"rows of the lists: {n_sense:,} take a sense line, {n_union:,} a union line, {len(rows) - n_sense - n_union:,} none")


if __name__ == "__main__":
    main()
