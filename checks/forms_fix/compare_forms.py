"""Compare the forms of the current word list (the clips) with a rebuilt one, per plain spelling.
Two forms are the same clip when they differ only in letter case or in an acute the voice reads as the default: on the
penult of a part with no other mark (súkal = sukal), or on a one-syllable word (ká = ka).
Usage: python3 checks/forms_fix/compare_forms.py <current wordlist_all.tsv> <index.json> <new wordlist.tsv> <changes.tsv out>"""
import sys, re, json, collections, unicodedata

cur_p, index_p, new_p, out_p = sys.argv[1:5]
ACU = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}


def nfc(s):
    return unicodedata.normalize("NFC", s)


def bare(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def marks(p):
    out = []
    for ch in p:
        if ch in "áéíóú": out.append("a")
        elif ch in "àèìòù": out.append("g")
        elif ch in "âêîôû": out.append("c")
        elif bare(ch) in "aeiou": out.append(None)
    return out


def ck(f):
    parts = nfc(f).lower().split("-")
    voiced = sum(1 for p in parts if marks(p))
    out = []
    for p in parts:
        mk = marks(p); vi = [i for i, ch in enumerate(p) if bare(ch) in "aeiou"]
        if sum(1 for m in mk if m) == 1:
            if len(vi) >= 2 and mk[-2] == "a":
                p = p[:vi[-2]] + ACU[p[vi[-2]]] + p[vi[-2] + 1:]
            elif len(vi) == 1 and mk[0] == "a" and voiced == 1:
                p = p[:vi[0]] + ACU[p[vi[0]]] + p[vi[0] + 1:]
        out.append(p)
    return "-".join(out)


MARKED = lambda f: any(marks(ck(f)))


def circ_misplaced(f):
    m = marks(nfc(f).lower())
    return any(k == "c" for k in m[:-1]) and not any(m[-1:])   # the one-syllable bug: circumflex on the first vowel, last vowel bare


def load(p):
    rows = [l.split("\t") for l in open(p, encoding="utf-8").read().split("\n")[1:] if l]
    by = collections.defaultdict(list)
    for r in rows:
        by[r[1]].append(r)
    return rows, by


cur_rows, cur = load(cur_p)
new_rows, new = load(new_p)
idx = json.load(open(index_p, encoding="utf-8"))
print("current rows", len(cur_rows), "| index.json clips", len(idx), "| forms with a clip:", len({nfc(r[0]) for r in cur_rows} & {nfc(k) for k in idx}))
print("new rows", len(new_rows), "| same plain spellings:", set(cur) == set(new))
cats = collections.Counter(); top = collections.Counter(); out = []
T = collections.defaultdict(lambda: [0, 0, 0, 0, 0])    # per category: to synthesize, retired, of them replaced, renamed, duplicates deleted
for w in list(dict.fromkeys([r[1] for r in cur_rows] + [r[1] for r in new_rows])):
    a = [nfc(r[0]) for r in cur.get(w, [])]; b = [nfc(r[0]) for r in new.get(w, [])]
    if a == b:
        continue
    srcs = {nfc(r[0]): r[2] for r in new.get(w, [])}
    ka = {}; kb = {}
    for f in a: ka.setdefault(ck(f), f)
    for f in b: kb.setdefault(ck(f), f)
    gone = [ka[k] for k in ka if k not in kb]; came = [kb[k] for k in kb if k not in ka]
    olds = collections.defaultdict(list)
    for f in dict.fromkeys(a): olds[ck(f)].append(f)
    renamed = [olds[k][0] for k in olds if k in kb and kb[k] not in olds[k]]          # same reading, new spelling
    dups = sum(len(olds[k]) - 1 for k in olds if k in kb)                              # a second clip of a reading kept
    if not gone and not came:
        if set(a) == set(b):
            continue                                        # only the order changed
        cat = "duplicate reading dropped (another letter case or a redundant acute)" if len(set(b)) < len(set(a)) else \
            "same reading, spelled differently (letter case or a redundant acute): the clip can be renamed"
    elif came and all(srcs[f] in ("english", "respelled") for f in came) and any(MARKED(f) for f in gone):
        cat = "English or respelled foreign word: marks removed"
    elif any(circ_misplaced(f) for f in gone):
        cat = "glottal mark moved from the first vowel to the last syllable (one-syllable bug)"
    elif gone and came and not any(MARKED(f) for f in gone) and all(MARKED(f) for f in came):
        cat = "stress mark added where the old form had none"
    elif gone and not came:
        cat = "a form dropped (duplicate reading or weaker evidence)"
    elif came and not gone:
        cat = "a reading added"
    elif "-" in w and any(any(marks(ck(f).split("-")[0])) for f in gone if "-" in f) and not any(any(marks(ck(f).split("-")[0])) for f in came if "-" in f):
        cat = "hyphenated word: mark taken off the first part"
    elif gone and came and all(MARKED(f) for f in gone) and not any(MARKED(f) for f in came):
        cat = "mark removed (penult stress)"
    else:
        cat = "stress moved to another syllable"
    cats[cat] += 1
    rank = next((r[4] for r in cur.get(w, []) + new.get(w, []) if r[4]), "")
    if rank and rank.isdigit() and int(rank) <= 20000:
        top[cat] += 1
    t = T[cat]; t[0] += len(came); t[1] += len(gone); t[2] += len(gone) if came else 0; t[3] += len(renamed); t[4] += dups
    out.append([w, ", ".join(a), ", ".join(b), rank, cat, ", ".join(sorted({srcs[f] for f in came})) or "-",
                str(len(came)), str(len(gone)), str(len(renamed)), str(dups)])
with open(out_p, "w", encoding="utf-8") as fh:
    fh.write("plain\told_forms\tnew_forms\trank\tcategory\tnew_stress_source\tforms_to_synthesize\tclips_retired\tclips_renamed\tduplicate_clips_deleted\n")
    for r in out:
        fh.write("\t".join(r) + "\n")
print("plain spellings whose forms change:", len(out), "| of them in the 20k most frequent:", sum(top.values()))
print("spellings | in 20k | forms to synthesize | clips retired | of them replaced by a new form | clips renamed | duplicate clips deleted   category")
S = [0, 0, 0, 0, 0]
for k, v in cats.most_common():
    t = T[k]; S = [x + y for x, y in zip(S, t)]
    print(f"  {v:6} | {top[k]:5} | {t[0]:6} | {t[1]:6} | {t[2]:6} | {t[3]:6} | {t[4]:6}   {k}")
print(f"  {sum(cats.values()):6} | {sum(top.values()):5} | {S[0]:6} | {S[1]:6} | {S[2]:6} | {S[3]:6} | {S[4]:6}   total")
