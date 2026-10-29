#!/usr/bin/env python3
"""Listen to the clips and write the phones a phone-recognition model hears (audio -> IPA).

    python3 scripts/phones.py MODEL LIST.tsv OUT.tsv [--shard i/n] [--fetch-raw]

MODEL: xeus (PhoneticXEUS, changelinglab/PhoneticXeus), zipa (ZIPA CR-CTC, ONNX), powsm (espnet/powsm), w2v2
(facebook/wav2vec2-lv-60-espeak-cv-ft).  LIST needs the columns `form` and `file` (audio/<letter>/<form>.mp3).
--fetch-raw downloads clips that are not checked out from raw.githubusercontent.com.  OUT is appended to and
resumable: forms already in it are skipped.  Output columns: form, model, phones (space-separated), seconds.
"""
import csv
import glob
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

import numpy as np

SR = 16000


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def fetch(path):
    repo = os.environ.get("GITHUB_REPOSITORY", "PawgChamps/tagalog-tts-audio")
    ref = os.environ.get("AUDIO_REF", "main")
    url = f"https://raw.githubusercontent.com/{repo}/{ref}/" + urllib.parse.quote(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=30) as r, open(path, "wb") as fh:
                fh.write(r.read())
            return
        except Exception:
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"could not fetch {url}")


def load_xeus():
    import torch
    from transformers import AutoModel
    m = AutoModel.from_pretrained("changelinglab/PhoneticXeus", trust_remote_code=True).eval()

    def run(wav):
        with torch.no_grad():
            r = m.transcribe(torch.from_numpy(wav), sampling_rate=SR)[0]
        p = r.get("predicted_transcript") or ""
        return " ".join(x for x in re.split(r"[/\s]+", p) if x) or r.get("processed_transcript", "")
    return run


def load_w2v2():
    import torch
    from transformers import AutoModelForCTC, AutoProcessor
    name = "facebook/wav2vec2-lv-60-espeak-cv-ft"
    proc, model = AutoProcessor.from_pretrained(name), AutoModelForCTC.from_pretrained(name).eval()

    def run(wav):
        x = proc(wav, sampling_rate=SR, return_tensors="pt").input_values
        with torch.no_grad():
            ids = model(x).logits.argmax(-1)
        return proc.batch_decode(ids)[0]
    return run


def load_powsm():
    from espnet2.bin.s2t_inference import Speech2Text
    s2t, last = None, None
    for lang in ("<tgl>", "<fil>", "<unk>"):
        try:
            s2t = Speech2Text.from_pretrained("espnet/powsm", device="cpu", lang_sym=lang, task_sym="<pr>")
            print("powsm language token:", lang, flush=True)
            break
        except Exception as e:                      # language token not in the vocabulary
            last = e
    if s2t is None:
        raise last

    def run(wav):
        x = np.pad(wav[:20 * SR], (0, max(0, 20 * SR - len(wav))))
        out = s2t(x, text_prev="<na>")[0][0]
        out = out.split("<notimestamps>")[-1]
        return " ".join(re.findall(r"/([^/\s]+)/", out)) or out.replace("/", " ").strip()
    return run


def load_zipa():
    import onnxruntime as ort
    import torch
    from huggingface_hub import snapshot_download
    src = os.environ.get("ZIPA_SRC", "zipa")
    sys.path.insert(0, os.path.join(src, "inference"))
    from utils import ctc_greedy_decode, get_fbank_extractor, load_tokens
    repo = os.environ.get("ZIPA_REPO", "anyspeech/zipa-large-crctc-500k")
    d = snapshot_download(repo, allow_patterns=["*fp32*", "*.txt"])
    onnx = sorted(glob.glob(f"{d}/**/*.onnx", recursive=True))
    toks = sorted(glob.glob(f"{d}/**/tokens.txt", recursive=True)) or [os.path.join(src, "ipa_simplified", "tokens.txt")]
    print("zipa:", repo, [os.path.relpath(p, d) for p in onnx], os.path.relpath(toks[0], d if toks[0].startswith(d) else src), flush=True)
    sess = ort.InferenceSession(onnx[0], providers=["CPUExecutionProvider"])
    ext, vocab = get_fbank_extractor(), load_tokens(toks[0])

    def run(wav):
        f = ext.extract_batch([torch.from_numpy(wav).float().unsqueeze(0)], sampling_rate=SR)[0].unsqueeze(0)
        lp = sess.run(None, {"x": f.numpy(), "x_lens": np.array([f.shape[1]], dtype=np.int64)})[0][0]
        return " ".join(ctc_greedy_decode(lp, vocab))
    return run


def main():
    model, lst, out = sys.argv[1:4]
    shard = next((a.split("/", 1) for a in sys.argv if re.fullmatch(r"\d+/\d+", a)), ("0", "1"))
    i, n = int(shard[0]), int(shard[1])
    rows = list(csv.DictReader(open(lst, encoding="utf-8"), delimiter="\t"))[i::n]
    done = set()
    if os.path.exists(out):
        done = {l.split("\t")[0] for l in open(out, encoding="utf-8")}
    todo = [r for r in rows if r["form"] not in done]
    print(f"{model}: {len(todo)} of {len(rows)} clips to do", flush=True)
    if not todo:
        return
    run = {"xeus": load_xeus, "w2v2": load_w2v2, "powsm": load_powsm, "zipa": load_zipa}[model]()
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    t0 = time.time()
    with open(out, "a", encoding="utf-8") as fh:
        for k, r in enumerate(todo, 1):
            if not os.path.exists(r["file"]):
                if "--fetch-raw" not in sys.argv:
                    continue
                fetch(r["file"])
            t = time.time()
            try:
                ph = run(decode(r["file"]))
            except Exception as e:                  # keep going; the row records the failure
                ph = "ERROR " + type(e).__name__
            fh.write(f"{r['form']}\t{model}\t{ph}\t{time.time() - t:.2f}\n")
            if k % 50 == 0:
                fh.flush()
                print(f"  {k}/{len(todo)}  {(time.time() - t0) / k:.2f} s per clip", flush=True)
    print(f"done in {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
