#!/usr/bin/env python3
"""Switch the repository to the rebuilt word list once every clip of the plan exists (the Switch workflow runs it).
Run from the repository root:

    python3 scripts/apply_next.py --check            # clips of each next/ list committed / missing; exit 1 if any missing
    python3 scripts/apply_next.py --drop next/pilot.tsv   # git rm the clips of a list (a pilot that failed its check)
    python3 scripts/apply_next.py                    # the switch; refuses while clips are missing

The switch stages everything with git: renames the clips of next/rename.tsv, removes those of next/retire.tsv, moves
the re-synthesized clips of next/redo_audio/ over the old ones, installs next/wordlist_ipa.tsv as wordlist_all.tsv and
next/respell.tsv as respell.tsv, rebuilds index.json, rewrites the counts in README.md (and drops its
<!-- rebuild --> notes) and removes next/."""
import os
import re
import shutil
import subprocess
import sys
import unicodedata

LISTS = ("synthesize.tsv", "synthesize_english.tsv", "redo.tsv", "redo_english.tsv")


def nfc(s):
    return unicodedata.normalize("NFC", s)


def git(*args, stdin=None):
    subprocess.run(["git", "--literal-pathspecs", *args], check=True, input=stdin)     # forms are file names, not globs


def committed():
    out = subprocess.run(["git", "ls-tree", "-r", "-z", "--name-only", "HEAD", "--", "audio", "next/redo_audio"],
                         capture_output=True, check=True).stdout.decode("utf-8")
    return {nfc(x) for x in out.split("\0") if x}


def rows_of(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    head = lines[0].split("\t")
    return [dict(zip(head, ln.split("\t"))) for ln in lines[1:] if ln]


def check():
    have, missing = committed(), 0
    for name in LISTS:
        p = f"next/{name}"
        if not os.path.exists(p):
            print(f"{p}: missing (run the Prepare workflow)")
            missing += 1
            continue
        rows = rows_of(p)
        lack = [r["file"] for r in rows if nfc(r["file"]) not in have]
        missing += len(lack)
        print(f"{p}: {len(rows) - len(lack):,} of {len(rows):,} clips committed" + (f", e.g. {lack[0]}" if lack else ""))
    return missing


def drop(path):
    have = committed()
    files = [r["file"] for r in rows_of(path) if nfc(r["file"]) in have]
    if files:
        git("rm", "-q", "--pathspec-from-file=-", "--pathspec-file-nul", stdin="\0".join(files).encode("utf-8"))
    print(f"{len(files):,} clips of {path} removed (staged; commit and push them)")


def switch():
    for old, new in ((r["old_file"], r["new_file"]) for r in rows_of("next/rename.tsv")):
        if old != new:
            os.makedirs(os.path.dirname(new), exist_ok=True)
            git("mv", "--", old, new)
    retire = [r["file"] for r in rows_of("next/retire.tsv")]
    if retire:
        git("rm", "-q", "--pathspec-from-file=-", "--pathspec-file-nul", stdin="\0".join(retire).encode("utf-8"))
    moved = []
    for name in ("redo.tsv", "redo_english.tsv"):
        for r in rows_of(f"next/{name}"):
            dst = "audio/" + r["file"].split("/", 2)[2]          # next/redo_audio/b/báka.mp3 -> audio/b/báka.mp3
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            os.replace(r["file"], dst)
            moved.append(dst)
    shutil.copyfile("next/wordlist_ipa.tsv", "wordlist_all.tsv")
    shutil.copyfile("next/respell.tsv", "respell.tsv")
    readme = open("README.md", encoding="utf-8").read()          # the "rebuild in progress" notes go
    open("README.md", "w", encoding="utf-8").write(re.sub(r"<!-- rebuild -->.*?<!-- /rebuild -->\n+", "", readme, flags=re.S))
    subprocess.run([sys.executable, "scripts/build_index.py"], check=True)
    subprocess.run([sys.executable, "scripts/readme_counts.py"], check=True)
    git("rm", "-r", "-q", "--cached", "--ignore-unmatch", "next")
    shutil.rmtree("next", ignore_errors=True)
    git("add", "-A", "audio", "wordlist_all.tsv", "respell.tsv", "index.json", "README.md")
    print(f"switched: {len(moved):,} clips re-synthesized, {len(retire):,} retired; now commit and push")


def main():
    if "--check" in sys.argv:
        sys.exit(1 if check() else 0)
    if "--drop" in sys.argv:
        drop(sys.argv[sys.argv.index("--drop") + 1])
        return
    if check():
        sys.exit("clips are missing: synthesize them first (see next/RUNBOOK.md)")
    switch()


if __name__ == "__main__":
    main()
