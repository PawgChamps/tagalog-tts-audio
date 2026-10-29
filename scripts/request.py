#!/usr/bin/env python3
"""Start the workflows named in a request file (the Request workflow runs it when a push changes next/request.txt), for
agents that can push to the repository but cannot start workflows themselves.
Usage: python3 scripts/request.py next/request.txt [--dry-run]   (needs GH_TOKEN and GITHUB_REF_NAME, as in Actions)

One request per line, `<workflow> key=value ...`; empty lines and lines starting with # are skipped:
    synthesize list=next-pilot
    phones list=next/pilot.tsv models=zipa audio=fetch
    prepare hyphen=join
    switch
Only the workflows and inputs below are accepted, and values may only hold letters, digits and _ . , / -"""
import os
import re
import subprocess
import sys

ALLOWED = {
    "synthesize": {"list", "outdir", "respell", "prompt", "batch", "workers", "hours", "max_words"},
    "phones": {"list", "models", "shards", "audio"},
    "prepare": {"hyphen", "pilot", "pilot_english", "redo"},
    "switch": set(),
    "fix_ipa": set(),
}
VALUE = re.compile(r"^[A-Za-z0-9_.,/-]+$")


def parse(text):
    out = []
    for n, ln in enumerate(text.splitlines(), 1):
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        name, *pairs = ln.split()
        if name not in ALLOWED:
            sys.exit(f"line {n}: unknown workflow {name!r} (allowed: {', '.join(ALLOWED)})")
        inputs = []
        for p in pairs:
            k, sep, v = p.partition("=")
            if not sep or k not in ALLOWED[name] or not VALUE.match(v) or ".." in v:
                sys.exit(f"line {n}: bad input {p!r} for {name} (allowed: {', '.join(sorted(ALLOWED[name])) or 'none'})")
            inputs.append((k, v))
        out.append((name, inputs))
    return out


def main():
    reqs = parse(open(sys.argv[1], encoding="utf-8").read())
    ref = os.environ.get("GITHUB_REF_NAME", "main")
    for name, inputs in reqs:
        cmd = ["gh", "workflow", "run", f"{name}.yml", "--ref", ref] + [x for k, v in inputs for x in ("-f", f"{k}={v}")]
        print(" ".join(cmd))
        if "--dry-run" not in sys.argv:
            subprocess.run(cmd, check=True)
    if not reqs:
        print("no requests")


if __name__ == "__main__":
    main()
