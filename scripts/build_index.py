#!/usr/bin/env python3
"""index.json for the audio folder: {accented form: {"file": "audio/b/báka.mp3", "plain": "baka", "ipa": "/ˈbaka/", "rank": 222}}.
Usage: python3 scripts/build_index.py  (run from the repository root)
Without an audio/ folder (a sparse checkout, as in .github/workflows/fix_ipa.yml) the clips are the ones committed in HEAD."""
import json, os, subprocess, unicodedata
rows = [l.rstrip("\n").split("\t") for l in open("wordlist_all.tsv", encoding="utf-8")][1:]
if os.path.isdir("audio"):
    exists = os.path.exists
else:
    names = subprocess.run(["git", "ls-tree", "-r", "-z", "--name-only", "HEAD", "--", "audio"], capture_output=True, check=True).stdout
    exists = set(names.decode("utf-8", "surrogateescape").split("\0")).__contains__
idx = {}
for r in rows:
    form = unicodedata.normalize("NFC", r[0])
    c = unicodedata.normalize("NFD", form)[:1].lower(); d = c if c.isalpha() and c.isascii() else "_"
    f = f"audio/{d}/{form}.mp3"
    if exists(f):
        idx[form] = {"file": f, "plain": r[1], "ipa": r[3], "rank": int(r[4]) if r[4] else None}
json.dump(idx, open("index.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(f"{len(idx):,} clips indexed of {len(rows):,} forms -> index.json")
