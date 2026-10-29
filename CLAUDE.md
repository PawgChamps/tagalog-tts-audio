# Notes for agents

- One MP3 per reading of each single-word headword of a Tagalog → Portuguese dictionary (`audio/<letter>/<form>.mp3`),
  listed in `wordlist_all.tsv` and `index.json`. The dictionary project reads those two files from `main` and links the
  clips, so on `main` the list, the index and `audio/` must always match. Change them only through a pull request, and
  never by hand: `scripts/build_index.py`, `scripts/fix_ipa.py` and the workflows write them.
- The work runs in GitHub Actions (README, "Workflows"). If you can push but not start workflows, write the request in
  `next/request.txt` (`scripts/request.py`).
- If `next/` exists, a switch to a rebuilt word list is in progress: follow `next/RUNBOOK.md`.
- The phone check (`checks/phones/`) is how clips are judged. Re-synthesize a clip only when a check of the new clip
  confirms it is better.
- Never print, write or commit keys or tokens. Google access in Actions is through workload identity federation
  (repository secrets `GCP_*`).
- Don't push to `main` or merge into it unless the user says so.
