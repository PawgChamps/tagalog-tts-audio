#!/usr/bin/env python3
"""Synthesize single accented words with Gemini-TTS through the Cloud Text-to-Speech API (v1beta1). Resumable: a word
whose file exists is skipped. The key is read from a file (or GOOGLE_ACCESS_TOKEN as a bearer token) and never printed.
Usage: tts_gemini.py <keyfile|-> <wordlist.tsv> <outdir> [--model gemini-3.1-flash-tts-preview] [--voice Laomedeia]
       [--limit N] [--workers 4] [--prompt "..."]      (keyfile "-" = $GOOGLE_ACCESS_TOKEN; "token:<file>" = access token in a file; "sa:<json>" = service account, needs `pip install google-auth requests`;
        header X-Goog-User-Project from $GOOGLE_QUOTA_PROJECT for the token modes)"""
import argparse
import base64
import json
import os
import sys
import threading
import time
import unicodedata
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

API = "https://texttospeech.googleapis.com/v1beta1/text:synthesize"
def letter_dir(form):
    """audio/<first letter>/<form>.mp3 (accents and case ignored for the folder; anything else goes to `_`)."""
    c = unicodedata.normalize("NFD", form)[:1].lower()
    return c if c.isalpha() and c.isascii() else "_"


DEFAULT_PROMPT = "Read aloud clearly, in a neutral tone. The text is a single Filipino word; say only that word, with the stress where the accent marks put it."


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keyfile"); ap.add_argument("wordlist"); ap.add_argument("outdir")
    ap.add_argument("--model", default="gemini-3.1-flash-tts-preview"); ap.add_argument("--voice", default="Laomedeia")
    ap.add_argument("--limit", type=int, default=0); ap.add_argument("--workers", type=int, default=4); ap.add_argument("--prompt", default=DEFAULT_PROMPT)
    ap.add_argument("--respell", default="", help="TSV form<TAB>text: send this text instead of the form (the file keeps the form's name)")
    a = ap.parse_args()
    headers = {"Content-Type": "application/json"}
    if a.keyfile == "-":
        headers["Authorization"] = "Bearer " + os.environ["GOOGLE_ACCESS_TOKEN"].strip()
    elif a.keyfile == "adc":                     # Application Default Credentials (workload identity federation in GitHub Actions)
        import google.auth
        import google.auth.transport.requests as gat
        cred, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        sa_lock = threading.Lock()
        def sa_header():
            with sa_lock:
                if not cred.valid or (cred.expiry and (cred.expiry - __import__("datetime").datetime.utcnow()).total_seconds() < 300):
                    cred.refresh(gat.Request())
                return "Bearer " + cred.token
        headers["Authorization"] = sa_header()
    elif a.keyfile.startswith("sa:"):            # sa:<service-account.json>: tokens are minted and refreshed automatically
        from google.oauth2 import service_account
        import google.auth.transport.requests as gat
        cred = service_account.Credentials.from_service_account_file(os.path.expanduser(a.keyfile[3:]), scopes=["https://www.googleapis.com/auth/cloud-platform"])
        sa_lock = threading.Lock()
        def sa_header():
            with sa_lock:
                if not cred.valid or (cred.expiry and (cred.expiry - __import__("datetime").datetime.utcnow()).total_seconds() < 300):
                    cred.refresh(gat.Request())
                return "Bearer " + cred.token
        headers["Authorization"] = sa_header()
    elif a.keyfile.startswith("token:"):        # token:<file> = OAuth access token kept in a file (gcloud auth print-access-token > file)
        headers["Authorization"] = "Bearer " + open(os.path.expanduser(a.keyfile[6:]), encoding="utf-8").read().strip()
    else:
        headers["X-Goog-Api-Key"] = open(os.path.expanduser(a.keyfile), encoding="utf-8").read().strip().splitlines()[0].strip()
    if ("Authorization" in headers or a.keyfile in ("adc",) or a.keyfile.startswith("sa:")) and os.environ.get("GOOGLE_QUOTA_PROJECT"):   # user tokens need a billing project
        headers["X-Goog-User-Project"] = os.environ["GOOGLE_QUOTA_PROJECT"]
    secret = headers.get("X-Goog-Api-Key") or headers.get("Authorization")
    os.makedirs(a.outdir, exist_ok=True)
    rows = [l.rstrip("\n").split("\t") for l in open(a.wordlist, encoding="utf-8")][1:]
    if a.limit:
        rows = rows[:a.limit]
    respell = dict(l.rstrip("\n").split("\t")[:2] for l in open(a.respell, encoding="utf-8") if "\t" in l) if a.respell else {}
    log = open(os.path.join(a.outdir, "log.tsv"), "a", encoding="utf-8"); lock = threading.Lock()
    stop = threading.Event(); n = {"ok": 0, "skip": 0, "fail": 0}

    def one(row):
        form = unicodedata.normalize("NFC", row[0])
        sub = os.path.join(a.outdir, letter_dir(form)); os.makedirs(sub, exist_ok=True)
        out = os.path.join(sub, form + ".mp3")
        if os.path.exists(out) and os.path.getsize(out) > 0:
            with lock: n["skip"] += 1
            return
        if stop.is_set():
            return
        body = {"input": {"text": respell.get(form, form), "prompt": a.prompt}, "voice": {"languageCode": "fil-PH", "name": a.voice, "modelName": a.model},
                "audioConfig": {"audioEncoding": "MP3"}}
        for attempt in range(6):
            if a.keyfile == "adc" or a.keyfile.startswith("sa:"):
                headers["Authorization"] = sa_header()
            req = urllib.request.Request(API, data=json.dumps(body).encode(), headers=dict(headers), method="POST")
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    d = json.loads(r.read().decode())
                audio = base64.b64decode(d.get("audioContent", ""))
                if not audio:
                    raise RuntimeError("empty audio")
                open(out, "wb").write(audio)
                with lock:
                    n["ok"] += 1; log.write(f"{form}\t{row[1]}\tok\t{len(audio)}\n"); log.flush()
                return
            except urllib.error.HTTPError as e:
                msg = e.read().decode(errors="replace").replace(secret, "<secret>")
                if e.code in (429, 500, 503) and attempt < 5:
                    time.sleep(2 ** attempt + 1); continue
                with lock:
                    n["fail"] += 1; log.write(f"{form}\t{row[1]}\tHTTP {e.code}\t{msg[:200].replace(chr(10), ' ')}\n"); log.flush()
                if e.code in (401, 403):
                    stop.set()
                    print("auth/permission error, stopping:", msg[:300].replace("\n", " "))
                return
            except Exception as ex:  # network hiccup
                if attempt < 5:
                    time.sleep(2 ** attempt + 1); continue
                with lock:
                    n["fail"] += 1; log.write(f"{form}\t{row[1]}\terror\t{str(ex)[:120]}\n"); log.flush()
                return

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        list(ex.map(one, rows))
    print(f"done in {time.time() - t0:.0f}s: {n} (model {a.model}, voice {a.voice}, {len(rows)} rows)")


if __name__ == "__main__":
    main()
