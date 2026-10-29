#!/usr/bin/env bash
# Synthesize the whole list in resumable batches and push each batch. Needs the Google key in $TTS_KEYFILE (a file) or
# $GOOGLE_ACCESS_TOKEN (a bearer token); the Vertex AI API must be enabled on the project for the Gemini-TTS models.
# Usage: ./run_batches.sh [batch size=2000] [workers=4]
set -euo pipefail
cd "$(dirname "$0")"
N="${1:-2000}"; W="${2:-4}"; KEY="${TTS_KEYFILE:--}"
total=$(($(wc -l < wordlist_all.tsv) - 1))
for ((start = 0; start < total; start += N)); do
  { head -1 wordlist_all.tsv; tail -n +2 wordlist_all.tsv | sed -n "$((start + 1)),$((start + N))p"; } > /tmp/batch.tsv
  python3 scripts/tts_gemini.py "$KEY" /tmp/batch.tsv audio --workers "$W" --model "${TTS_MODEL:-gemini-3.1-flash-tts-preview}" --voice "${TTS_VOICE:-Laomedeia}"
  python3 scripts/build_index.py
  git add audio index.json && git commit -qm "audio: rows $((start + 1))-$((start + N))" && git push -q || true
done
