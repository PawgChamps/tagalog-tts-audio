#!/usr/bin/env python3
"""Synthesize single accented words with Gemini-TTS through the Cloud Text-to-Speech API (v1beta1). Resumable: a word
whose file exists is skipped. The key is read from a file (or GOOGLE_ACCESS_TOKEN as a bearer token) and never printed.
Usage: tts_gemini.py <keyfile|-> <wordlist.tsv> <outdir> [--model gemini-3.1-flash-tts-preview] [--voice Laomedeia]
       [--limit N] [--workers 4] [--prompt tagalog|english|parts|...|"..."] [--respell respell.tsv]      (keyfile "-" = $GOOGLE_ACCESS_TOKEN; "token:<file>" = access token in a file; "sa:<json>" = service account, needs `pip install google-auth requests`;
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
PROMPTS = {        # --prompt and the third column of --respell take one of these names (or the text of a prompt).
    "tagalog": DEFAULT_PROMPT,                # Tested by scripts/fix_clips.py on 3,526 clips (checks/fix/README.md).
    "english": "Read aloud clearly, in a neutral tone. The text is a single English word; say only that word, pronounced "
               "the English way. Do not translate it.",
    "parts": "Read aloud clearly, in a neutral tone. The text is one Filipino word written here in parts; say every part, "
             "with the stress where the accent marks put it, and nothing else.",          # hyphen sent as a space
    "repeat": "Read aloud clearly, in a neutral tone. The text is one Filipino word made by repeating a part. Say every "
              "part, the repeated one too, with the stress where the accent marks put it, and nothing else.",
    "letters": "Read aloud clearly, in a neutral tone. Say exactly the text, and nothing else.",   # letter names: es dyi ti
    "caps": "Read aloud clearly, in a neutral tone. The text is letters of the alphabet; say the English name of each "
            "letter, one after the other, and nothing else.",
    "quoted": "Read aloud clearly, in a neutral tone. Say only the word in quotation marks, without the quotation marks.",
    "quoted_english": "Read aloud clearly, in a neutral tone. Say only the English word in quotation marks, without the "
                      "quotation marks, pronounced the English way. It is not an instruction. Do not translate it.",
}


def read_respell(path):
    """respell file -> {form: (text, prompt name or None)}: form<TAB>text[<TAB>prompt]"""
    out = {}
    for line in open(path, encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) >= 2:
            out[unicodedata.normalize("NFC", f[0])] = (f[1], f[2] if len(f) > 2 and f[2] else None)
    return out


class AuthError(RuntimeError):
    pass


def auth(keyfile):
    """Request headers for the API, as a function (tokens are refreshed when they near expiry), and the secret to mask
    in error messages.  keyfile: a file with an API key; "-" = $GOOGLE_ACCESS_TOKEN; "token:<file>" = access token in a
    file; "sa:<json>" = service account; "adc" = Application Default Credentials (workload identity in GitHub Actions)."""
    headers = {"Content-Type": "application/json"}
    refresh = None
    if keyfile == "-":
        headers["Authorization"] = "Bearer " + os.environ["GOOGLE_ACCESS_TOKEN"].strip()
    elif keyfile == "adc" or keyfile.startswith("sa:"):
        import google.auth.transport.requests as gat
        if keyfile == "adc":                     # Application Default Credentials (workload identity federation in GitHub Actions)
            import google.auth
            cred, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        else:                                    # sa:<service-account.json>: tokens are minted and refreshed automatically
            from google.oauth2 import service_account
            cred = service_account.Credentials.from_service_account_file(os.path.expanduser(keyfile[3:]), scopes=["https://www.googleapis.com/auth/cloud-platform"])
        sa_lock = threading.Lock()

        def refresh():
            with sa_lock:
                if not cred.valid or (cred.expiry and (cred.expiry - __import__("datetime").datetime.utcnow()).total_seconds() < 300):
                    cred.refresh(gat.Request())
                return "Bearer " + cred.token
        headers["Authorization"] = refresh()
    elif keyfile.startswith("token:"):          # token:<file> = OAuth access token kept in a file (gcloud auth print-access-token > file)
        headers["Authorization"] = "Bearer " + open(os.path.expanduser(keyfile[6:]), encoding="utf-8").read().strip()
    else:
        headers["X-Goog-Api-Key"] = open(os.path.expanduser(keyfile), encoding="utf-8").read().strip().splitlines()[0].strip()
    if "Authorization" in headers and os.environ.get("GOOGLE_QUOTA_PROJECT"):   # user tokens need a billing project
        headers["X-Goog-User-Project"] = os.environ["GOOGLE_QUOTA_PROJECT"]
    secret = headers.get("X-Goog-Api-Key") or headers.get("Authorization")

    def get():
        if refresh:
            headers["Authorization"] = refresh()
        return dict(headers)
    return get, secret


def synthesize(get_headers, secret, text, prompt, voice, model, language="fil-PH", attempts=6):
    """One clip as MP3 bytes.  Retries rate limits, server errors and network hiccups; raises AuthError on 401/403
    and RuntimeError on anything else."""
    body = {"input": {"text": text, "prompt": prompt}, "voice": {"languageCode": language, "name": voice, "modelName": model},
            "audioConfig": {"audioEncoding": "MP3"}}
    for attempt in range(attempts):
        req = urllib.request.Request(API, data=json.dumps(body).encode(), headers=get_headers(), method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                d = json.loads(r.read().decode())
            audio = base64.b64decode(d.get("audioContent", ""))
            if not audio:
                raise RuntimeError("empty audio")
            return audio
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace").replace(secret, "<secret>")[:300].replace("\n", " ")
            if e.code in (429, 500, 503) and attempt < attempts - 1:
                time.sleep(2 ** attempt + 1); continue
            if e.code in (401, 403):
                raise AuthError(f"HTTP {e.code} {msg}")
            raise RuntimeError(f"HTTP {e.code} {msg}")
        except (AuthError, KeyboardInterrupt):
            raise
        except Exception as ex:                  # network hiccup
            if attempt < attempts - 1:
                time.sleep(2 ** attempt + 1); continue
            raise RuntimeError(str(ex)[:120])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keyfile"); ap.add_argument("wordlist"); ap.add_argument("outdir")
    ap.add_argument("--model", default="gemini-3.1-flash-tts-preview"); ap.add_argument("--voice", default="Laomedeia")
    ap.add_argument("--limit", type=int, default=0); ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--prompt", default="tagalog", help="a prompt name (" + ", ".join(PROMPTS) + ") or the prompt itself")
    ap.add_argument("--respell", default="", help="TSV form<TAB>text[<TAB>prompt]: send this text (with this prompt) instead "
                                                  "of the form (the file keeps the form's name)")
    a = ap.parse_args()
    a.prompt = PROMPTS.get(a.prompt, a.prompt)
    get_headers, secret = auth(a.keyfile)
    os.makedirs(a.outdir, exist_ok=True)
    rows = [l.rstrip("\n").split("\t") for l in open(a.wordlist, encoding="utf-8")][1:]
    if a.limit:
        rows = rows[:a.limit]
    respell = read_respell(a.respell) if a.respell else {}
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
        text, pname = respell.get(form, (form, None))
        prompt = PROMPTS.get(pname, pname) if pname else a.prompt
        try:
            try:
                audio = synthesize(get_headers, secret, text, prompt, a.voice, a.model)
            except RuntimeError as e:             # the content filter refuses some harmless respellings (di matutunaw):
                if isinstance(e, AuthError) or "usage guidelines" not in str(e) or (text, prompt) == (form, a.prompt):
                    raise
                audio = synthesize(get_headers, secret, form, a.prompt, a.voice, a.model)   # try the form as written
        except AuthError as e:
            stop.set()
            print("auth/permission error, stopping:", str(e)[:300])
            with lock:
                n["fail"] += 1; log.write(f"{form}\t{row[1]}\tauth\t{str(e)[:200]}\n"); log.flush()
            return
        except RuntimeError as e:
            with lock:
                n["fail"] += 1; log.write(f"{form}\t{row[1]}\terror\t{str(e)[:200]}\n"); log.flush()
            return
        open(out, "wb").write(audio)
        with lock:
            n["ok"] += 1; log.write(f"{form}\t{row[1]}\tok\t{len(audio)}\n"); log.flush()

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        list(ex.map(one, rows))
    print(f"done in {time.time() - t0:.0f}s: {n} (model {a.model}, voice {a.voice}, {len(rows)} rows)")


if __name__ == "__main__":
    main()
