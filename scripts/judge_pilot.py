#!/usr/bin/env python3
"""Verdict on the two pilots of the rebuild (next/RUNBOOK.md), from their phone checks. Run from the repository root:

    python3 scripts/judge_pilot.py [--checks checks/phones]

Reads <checks>/pilot/ (the phone check of next/pilot.tsv: new readings, two thirds hyphenated, Tagalog prompt) and
<checks>/pilot_english/ (next/pilot_english.tsv: English loanwords whose current clip sounds Tagalog, English prompt) and
compares them with the phone check of the current clips (<checks>/wordlist_all/). Prints PASS or FAIL for each:
  hyphen   hyphenated clips heard much shorter than the word: at most 2 % (current clips: 6.8 %), and no clip with extra
           speech except spelled-out abbreviations (ipa_source spelled)
  english  at least two thirds of the clips closer to the English reading than to the Tagalog one (these words' current
           clips: none), and a mean error against the English reading of at most 0.20 (current clips that sound
           English: 0.13; these words' current clips: about 0.40)
Exit status 0 when both pass."""
import argparse
import csv
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score_phones import dist, phones  # noqa: E402

MAX_CUT, MIN_ENGLISH, MAX_ERR_EN = 0.02, 2 / 3, 0.20


def tsv(p):
    if not os.path.exists(p):
        return None
    return list(csv.DictReader(open(p, encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE))


def err(ref, heard):
    """phone error without ʔ, as in score_phones.py (a clip counts at most 100 % wrong)"""
    r = [x for x in phones(ref) if x != "ʔ"]
    h = [x for x in phones(heard) if x != "ʔ"]
    return min(dist(r, h), len(r)) / max(1, len(r))


def heard_of(rows):
    """-> ({form: what the model heard}, model): zipa when it ran, else the first model column"""
    models = [c for c in rows[0] if c not in ("form", "category", "ipa")] if rows else []
    m = "zipa" if "zipa" in models else (models[0] if models else None)
    return {r["form"]: r[m] for r in rows if m and r.get(m) and not r[m].startswith("ERROR")}, m


def hyphen(ck):
    comp = tsv(f"{ck}/pilot/compare.tsv")
    if not comp:
        return None, [f"no phone check of next/pilot.tsv yet ({ck}/pilot/compare.tsv)"]
    heard, m = heard_of(comp)
    row = {r["form"]: r for r in comp}
    hy = [f for f in heard if "-" in f.strip("-")]
    pl = [f for f in heard if "-" not in f.strip("-")]
    cut = [r for r in tsv(f"{ck}/pilot/truncated.tsv") or [] if r["form"] in heard]
    cut_hy = [r["form"] for r in cut if r["kind"] == "hyphenated"]
    cut_pl = [r["form"] for r in cut if r["kind"] == "plain"]
    extra = [r["form"] for r in tsv(f"{ck}/pilot/extra_speech.tsv") or []]
    bad_extra = [f for f in extra if row.get(f, {}).get("category") != "spelled"]
    share = len(cut_hy) / len(hy) if hy else 1.0
    mean = lambda fs: f"{statistics.mean(err(row[f]['ipa'], heard[f]) for f in fs):.1%}" if fs else "–"
    ok = bool(hy) and share <= MAX_CUT and not bad_extra
    return ok, [f"{len(heard)} clips heard ({m}), {len(hy)} hyphenated",
                f"cut short: hyphenated {len(cut_hy)}/{len(hy)} = {share:.1%} (limit {MAX_CUT:.0%}; current clips 6.8 %), "
                f"plain {len(cut_pl)}/{len(pl)}" + (f"; e.g. {', '.join(cut_hy[:10])}" if cut_hy else ""),
                f"extra speech: {', '.join(extra) or 'none'}" + (f" (not abbreviations: {', '.join(bad_extra)})" if bad_extra else ""),
                f"error without ʔ: hyphenated {mean(hy)} (current clips 10.7 %), plain {mean(pl)} "
                "(current clips: rule 9.6 %, dictionary 7.6 %)"]


def english(ck):
    if tsv("next/pilot_english.tsv") == []:
        return True, ["next/pilot_english.tsv is empty: no English clip is re-synthesized in this plan"]
    comp = tsv(f"{ck}/pilot_english/compare.tsv")
    if not comp:
        return None, [f"no phone check of next/pilot_english.tsv yet ({ck}/pilot_english/compare.tsv)"]
    heard, m = heard_of(comp)
    ipa = {r["form"]: r["ipa"] for r in comp}
    base = {r["form"]: r for r in tsv(f"{ck}/wordlist_all/english_vs_tagalog.tsv") or []}
    new, old, en, tl, n = [], [], 0, 0, 0
    for f, h in heard.items():
        e_en = err(ipa[f], h)
        new.append(e_en)
        b = base.get(f)
        if b:                                     # the verdict rule of english_vs_tagalog.tsv: 0.1 apart, rounded
            d = round(err(b["tagalog_ipa"], h), 2) - round(e_en, 2)
            en += d > 0.095
            tl += d < -0.095
            n += 1
            old.append(float(b["err_english"]))
    share = en / n if n else 0.0
    mean_new = statistics.mean(new) if new else 1.0
    ok = n >= 20 and share >= MIN_ENGLISH and mean_new <= MAX_ERR_EN
    return ok, [f"{len(heard)} clips heard ({m}), {n} with a Tagalog reading to compare",
                f"closer to the English reading: {en}/{n} = {share:.0%} (limit {MIN_ENGLISH:.0%}); closer to the Tagalog "
                f"reading: {tl}; no clear difference: {n - en - tl}",
                f"mean error against the English reading: {mean_new:.2f} (limit {MAX_ERR_EN:.2f}); the same words' current "
                f"clips: {statistics.mean(old) if old else float('nan'):.2f}"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checks", default="checks/phones")
    a = ap.parse_args()
    res = [("hyphen", *hyphen(a.checks)), ("english", *english(a.checks))]
    for name, ok, lines in res:
        print(f"{name}: {'PASS' if ok else 'NOT CHECKED' if ok is None else 'FAIL'}")
        print("".join(f"  {x}\n" for x in lines), end="")
    sys.exit(0 if all(ok for _, ok, _ in res) else 1)


if __name__ == "__main__":
    main()
