#!/usr/bin/env python3
"""Pick a test sample of clips for the phone-recognition check, by category.  Run from the repository root:

    python3 scripts/make_phone_sample.py [N_PER_CATEGORY_SCALE] > checks/sample.tsv
"""
import collections
import json
import random
import re
import sys

scale = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
rows = [l.split("\t") for l in open("wordlist_all.tsv", encoding="utf-8").read().split("\n")[1:] if l]
index = json.load(open("index.json", encoding="utf-8"))
ACC = "áéíóúàèìòùâêîôû"
TL_PREFIX = re.compile(r"^(mag|nag|pag|mang|nang|pang|ma|na|pa|ka|may|di|i|tig|sang)-")


def rank(r):
    return int(r[4]) if r[4] else 10 ** 9


def single(f):
    return "-" not in f and " " not in f


cats = collections.OrderedDict()
cats["dict"] = [r for r in rows if r[6] == "dictionary" and r[2] in ("ipa", "headword") and single(r[0])
                and re.search(f"[{ACC}]", r[0]) and not re.search(r"[âêîôû](?=.*[a-z])", r[0]) and rank(r) <= 30000]
cats["glottal"] = [r for r in rows if r[6] == "dictionary" and single(r[0]) and r[3].endswith("ʔ/") and r[0][-1] in "àèìòùâêîôû"]
cats["english"] = [r for r in rows if r[6] == "english" and single(r[0]) and rank(r) <= 60000]
cats["english_tagalog"] = [r for r in rows if r[6] == "english" and "-" in r[0] and (TL_PREFIX.match(r[0]) or len(set(r[0].split("-"))) == 1)]
cats["circ_bug"] = [r for r in rows if re.search(r"[âêîôû](?=.*[a-z])", r[0])]
cats["nostress"] = [r for r in rows if r[2] == "none" and single(r[0]) and r[6] == "rule" and rank(r) <= 60000]
by_plain = collections.defaultdict(list)
for r in rows:
    if single(r[0]) and r[2] != "none":
        by_plain[r[1]].append(r)
pairs = [v for v in by_plain.values() if len(v) == 2 and len({x[0] for x in v}) == 2]
size = {"dict": 80, "glottal": 50, "english": 40, "english_tagalog": 20, "circ_bug": 40, "nostress": 30}
random.seed(20261029)
print("form\tfile\tcategory\tipa\tipa_source\tstress_source")
seen = set()
for c, pool in cats.items():
    for r in random.sample(pool, min(len(pool), int(size[c] * scale))):
        if r[0] in index and r[0] not in seen:
            seen.add(r[0]); print("\t".join([r[0], index[r[0]]["file"], c, r[3], r[6], r[2]]))
for v in random.sample(pairs, min(len(pairs), int(20 * scale))):
    for r in v:
        if r[0] in index and r[0] not in seen:
            seen.add(r[0]); print("\t".join([r[0], index[r[0]]["file"], "heteronym", r[3], r[6], r[2]]))
