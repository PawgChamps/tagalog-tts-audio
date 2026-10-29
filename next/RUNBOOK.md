# Rebuild runbook

For the agent that carries out the rebuild. `next/wordlist.tsv` is the word list rebuilt with accent marks taken in the
source order KWF > UP > Wiktionary > books (`scripts/make_wordlist.py`; the changes per spelling are in
`checks/forms_fix/changes.tsv`). The job: give the list its IPA, synthesize the readings that have no clip yet, rename
and retire clips, switch the repository to the new list and open a pull request to `main`. All the heavy work runs in
GitHub Actions; you write requests, read the results and decide.

## Rules

- Work on your own branch, made from `main`. Never push to `main`, never merge into it, never force-push.
- Never print, write or ask for secrets. The workflows reach Google through workload identity federation; you need no key.
- Don't edit `wordlist_all.tsv`, `index.json`, `respell.tsv`, `audio/` or the plan files in `next/` by hand, except
  where a step below says so.
- `git pull --rebase` before every push: the workflows commit to your branch while they run.
- One request at a time for `prepare`, `synthesize` and `switch`. They share a queue that holds one running and one
  waiting run, and a newer waiting run cancels the older one. `phones` runs beside them.
- If a run fails twice in a row, or what you see does not match this file, stop and report the run's address, the
  failing step and what you saw.

## Starting a workflow

You can push but not start workflows, so the *Request* workflow starts them for you on your branch. Write one request
per line in `next/request.txt`, with a comment line so that the file always changes, then push:

```bash
printf '# %s\nsynthesize list=next-pilot\n' "$(date -u +%FT%TZ)" > next/request.txt
git add next/request.txt && git commit -qm "request: pilot" && git pull -q --rebase && git push -q
```

Accepted (`scripts/request.py`): `prepare` (inputs `hyphen`, `pilot`, `pilot_english`, `redo`), `synthesize` (`list`,
`prompt`, `batch`, `workers`, `hours`, `max_words`, `outdir`, `respell`), `phones` (`list`, `models`, `shards`, `audio`)
and `switch`. Values may only hold letters, digits and `_ . , / -`.

## Watching

- `git pull -q --rebase && git log --oneline -15`. Each workflow commits as it goes: `next: IPA and plan` (Prepare),
  `audio: next/… rows …` (Synthesize), `checks: phone recognition of …` (Phone recognition), `Switch to the rebuilt word
  list …` (Switch).
- The runs on your branch (public, no token needed):
  `curl -s "https://api.github.com/repos/PawgChamps/tagalog-tts-audio/actions/runs?branch=$(git branch --show-current)&per_page=10"`
  gives `name`, `status`, `conclusion` and `html_url`; `…/actions/runs/<id>/jobs` gives the steps of one run.
- `python3 scripts/apply_next.py --check` counts the committed clips of each list.
- Look every 15 to 30 minutes, not more often.

## Steps

1. **Prepare.** Request `prepare`. When its commit arrives, read `next/plan.md`. Expect about 147,500 forms in the new
   list, about 30,000 readings to synthesize, about 1,400 clips renamed and 34,000 retired. `redo.tsv` is empty when
   `checks/fix/results.tsv` exists: the wrong clips of the current list were already re-synthesized and checked by
   `scripts/fix_clips.py`. If the counts are far off, stop and report.
2. **Pilot.** Request `synthesize list=next-pilot`: 300 new readings into `audio/`, two thirds of them hyphenated and
   sent with the hyphen read as a space, plus `next/pilot_english.tsv` when it has rows. When its clips are committed,
   request the phone check. Add the second line only if `next/pilot_english.tsv` has rows:

   ```text
   phones list=next/pilot.tsv models=zipa audio=fetch
   phones list=next/pilot_english.tsv models=zipa audio=fetch
   ```

3. **Judge the pilot.** When `checks/phones/pilot/` (and `checks/phones/pilot_english/`) are committed, run
   `python3 scripts/judge_pilot.py`.
   - **hyphen PASS**: go on.
   - **hyphen FAIL**: run `python3 scripts/apply_next.py --drop next/pilot.tsv`, commit and push, request
     `prepare hyphen=join` (the halves joined) and repeat steps 2 and 3. If `join` fails too, prepare again with
     whichever of `space` and `join` cut fewer clips, go on, and say so in the pull request.
   - **english FAIL**: run `python3 scripts/apply_next.py --drop next/pilot_english.tsv`. Append the rows of
     `next/synthesize_english.tsv` (without its header) to `next/synthesize.tsv`. Leave only the header line in
     `next/synthesize_english.tsv`, `next/redo_english.tsv` and `next/pilot_english.tsv`. Commit and push.
4. **Full run.** Request `synthesize list=next`. It works through `synthesize.tsv`, `synthesize_english.tsv`, `redo.tsv`
   and `redo_english.tsv`, commits every 2,000 clips and starts a new run of itself at the 5-hour limit. It takes hours.
   It is done when `python3 scripts/apply_next.py --check` exits 0 and no *Synthesize audio* run is queued or running.
   If the runs have stopped and clips are still missing (the voice refused a word, or the network failed), request
   `synthesize list=next` again. If the same clips are still missing after two more runs, delete their rows from the
   list that has them (that form then has no clip, and `index.json` leaves it out), commit, push, and name them in the
   pull request.
5. **Phone check of the new clips** (optional). Request `phones list=next/synthesize.tsv models=zipa shards=6 audio=checkout`
   and put its summary in the pull request. Wrong clips are fixed after the switch with `scripts/fix_clips.py`.
6. **Switch.** Copy the table of `next/plan.md` somewhere for the pull request: the switch deletes `next/`. If `main` has
   moved since you branched, run `git fetch origin main && git merge origin/main` first. On a conflict in
   `wordlist_all.tsv`, `index.json`, `respell.tsv` or `README.md`, keep main's version, because the switch rewrites
   these files. On any other conflict, stop and report. Push, then request `switch`. When its commit arrives,
   `wordlist_all.tsv` is the new list, `index.json` is rebuilt and `next/` is gone. Check that `wc -l wordlist_all.tsv`
   is the number of forms plus one and that the README counts match.
7. **Pull request** from your branch to `main`, titled "Rebuilt word list: accent marks from KWF > UP > Wiktionary >
   books". Include the plan table, the output of `judge_pilot.py`, the hyphen option used, the phone check of step 5 if
   you ran it, and anything left out. Don't merge it: the user does.
