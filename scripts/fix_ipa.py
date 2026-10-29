#!/usr/bin/env python3
"""Clean the `ipa` / `ipa_source` columns of wordlist_all.tsv.  Run from the repository root:

    python3 scripts/fix_ipa.py            # dry run: prints counts and samples, writes nothing
    python3 scripts/fix_ipa.py --write    # rewrites wordlist_all.tsv (then run scripts/build_index.py)

Needs `pip install cmudict` (English pronunciations for English loanwords).  What it does, in order:

 dictionary readings (ipa_source = dictionary)
   1. drop notes after the closing slash ("/ˈbas/ (Taglish)");
   2. readings that hold several words ("/ˈɡeŋ ɡeŋ/", garbled reduplications) are rebuilt: by rule for Tagalog spellings,
      from CMUdict for English ones, letter by letter for consonant-only abbreviations;
   3. notation brought to the documented style: no syllable dots, no length marks, no tie bars, glide y -> j, ʎ -> lj;
   4. the stress mark is moved to the start of its syllable when the dictionary's dot had left it after a consonant
      (ʔib.ˈaŋ -> ʔiˈbaŋ); after a hyphen the glottal stop is written (paɡ.ˈaral -> paɡˈʔaɾal);
   4b. two vowels in a row get their glottal stop (kahalataan -> kahalataʔan); readings that lost vowels or read
      consonant+y as consonant+i (akyat -> ki-at) are replaced by the rule reading;
   5. if the stress still is not on the vowel the accent mark of the spelling names, the rule reading replaces it;
   6. readings that still contain spelling leftovers (th, sh, ea, ou ...) for words CMUdict knows are replaced by it.
 generated readings (rule / spelled)
   7. English loanwords (no accent mark, not a name, found in CMUdict, and a foreign letter or digraph, or six letters or more, or a doubled consonant) get their English reading
      (ipa_source = english); consonant-only words with y (gym, sky) too.
"""
import re
import sys
import unicodedata

sys.path.insert(0, __import__("os").path.dirname(__file__))
import make_ipa as M

try:
    import cmudict
    CMU = cmudict.dict()
except ImportError:
    CMU = {}

VOW = set("aeiouəɛɔɪʊæʌɑɝɚ")
FORM_V = set("aeiou")
ACCENTED = dict(zip("áéíóúàèìòùâêîôû", "aeiouaeiouaeiou"))
FOREIGN_LETTERS = re.compile(r"[cfjqvxz]|ch|sh|th|ph|ck|wh|gh|oo|ee|ou|ea|ow|ie")
LEFTOVER = re.compile(r"th|sh|ch|ck|ph|ea|ou|oo|ee|ie|ui|qu|wh|ow|gh")
CL = {a + b for a in "bkdɡpstfv" for b in "lɾr"}


def plain(s):
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()


def has_accent(form):
    return any(c in ACCENTED for c in form.lower())


def tagalog_like(form):
    p = plain(form)
    return not re.search(r"[cfjqvxz]|ch|sh|th|ph|ck|wh|gh", re.sub(r"c(?=[eiy])", "", p)) or has_accent(form)


def form_vowels(form):
    return [(c if c in FORM_V else ACCENTED[c]) for c in form.lower() if c in FORM_V or c in ACCENTED]


def accent_marks(form):
    """indexes (among the spelling's vowels) of vowels that carry an accent mark"""
    return [k for k, c in enumerate(c for c in form.lower() if c in FORM_V or c in ACCENTED) if c in ACCENTED]


def stress_index(body):
    return sum(1 for c in body[:body.index("ˈ")] if c in VOW) if "ˈ" in body else None


def nvow(body):
    return sum(1 for c in body if c in VOW)


# ---------------------------------------------------------------- English from CMUdict
ARPA = {"AA": "ɑ", "AE": "æ", "AH": "ʌ", "AO": "ɔ", "AW": "aʊ", "AY": "aɪ", "EH": "ɛ", "ER": "ɝ", "EY": "eɪ", "IH": "ɪ", "IY": "i",
        "OW": "oʊ", "OY": "ɔɪ", "UH": "ʊ", "UW": "u", "B": "b", "CH": "tʃ", "D": "d", "DH": "ð", "F": "f", "G": "ɡ", "HH": "h",
        "JH": "dʒ", "K": "k", "L": "l", "M": "m", "N": "n", "NG": "ŋ", "P": "p", "R": "ɹ", "S": "s", "SH": "ʃ", "T": "t",
        "TH": "θ", "V": "v", "W": "w", "Y": "j", "Z": "z", "ZH": "ʒ"}
STOPS = set("pbtdkɡf")


def legal_onset(on):
    if len(on) == 1:
        return on[0] != "ŋ"
    if len(on) == 2:
        return (on[0] in STOPS | {"θ", "ʃ"} and on[1] in "lɹwj") or (on[0] == "s" and on[1] in "ptkmnflwj")
    if len(on) == 3:
        return on[0] == "s" and on[1] in "ptk" and on[2] in "lɹwj"
    return False


def cmu_word(word):
    """one English word -> IPA body (no slashes) with ˈ / ˌ before the stressed syllables, or None"""
    prons = CMU.get(word.lower())
    if not prons:
        return None
    segs = []                                        # (symbol, is_vowel, stress)
    for ph in prons[0]:
        m = re.fullmatch(r"([A-Z]+)([012])?", ph)
        base, st = m.group(1), m.group(2)
        if base in ARPA:
            sym = ARPA[base]
            if st is not None:
                if base == "AH" and st == "0":
                    sym = "ə"
                if base == "ER" and st == "0":
                    sym = "ɚ"
            segs.append((sym, st is not None, st))
    out, marks = [s[0] for s in segs], {}
    for i, (sym, isv, st) in enumerate(segs):
        if isv and st in ("1", "2"):
            j = i
            while j > 0 and not segs[j - 1][1]:
                j -= 1
            run = i - j
            if j == 0:
                k = run                              # word-initial cluster all belongs to the first syllable
            else:
                k = min(run, 3)
                while k > 1 and not legal_onset([s[0] for s in segs[i - k:i]]):
                    k -= 1
            marks[i - k] = "ˈ" if st == "1" else "ˌ"
    return "".join(marks.get(i, "") + out[i] for i in range(len(out)))


def cmu_ipa(form):
    parts = [p for p in re.split(r"[-\s]+", form.lower()) if p]
    bodies = [cmu_word(p) for p in parts]
    if not parts or any(b is None for b in bodies):
        return None
    res = bodies[0] + "".join(b.replace("ˈ", "ˌ") for b in bodies[1:])
    if "ˈ" not in res and "ˌ" in res:
        res = res.replace("ˌ", "ˈ", 1)
    if res.count("ˈ") > 1:                               # compounds list several primaries: keep the last one
        head, _, tail = res.rpartition("ˈ")
        res = head.replace("ˈ", "ˌ") + "ˈ" + tail
    return "/" + res + "/"


# ---------------------------------------------------------------- dictionary notation
def move_stress(body, form):
    """stress mark left after a consonant by the dictionary's syllable dot -> start of the syllable (or ˈʔ after a hyphen)"""
    i = body.find("ˈ")
    if i <= 0 or i + 1 >= len(body) or body[i + 1] not in VOW:
        return body
    j = i
    while j > 0 and body[j - 1] not in VOW:
        j -= 1
    if j == 0 or j == i:
        return body
    if "-" in form:
        return body[:i] + "ˈʔ" + body[i + 1:]
    units = re.findall(r"tʃ|dʒ|.", body[j:i])
    k = 2 if len(units) >= 2 and units[-2] + units[-1] in CL else 1
    return body[:j] + "".join(units[:-k]) + "ˈ" + "".join(units[-k:]) + body[i + 1:]


def normalise(body):
    body = body.replace("͡", "").replace("ː", "").replace("·", "").replace("ʎ", "lj")
    out = []
    for i, c in enumerate(body):                       # IPA y is a vowel: a glide next to a vowel is j, otherwise it stands for i
        if c == "y":
            near = (i > 0 and body[i - 1] in VOW) or (i + 1 < len(body) and body[i + 1] in VOW)
            c = "j" if near else "i"
        out.append(c)
    return "".join(out)


def hiatus(body):
    """two vowels in a row are separate syllables in Tagalog: write the glottal stop the style asks for (kahalataan -> kahalataʔan)"""
    body = re.sub(r"([aeiou])(?=[aeiou])", r"\1ʔ", body)
    return re.sub(r"([aeiou])([ˈˌ])(?=[aeiou])", r"\1\2ʔ", body)


def broken(form, body):
    """a reading that cannot be right for a Tagalog spelling: fewer vowels than the spelling has vowel groups (lost vowels),
    or more vowels than letters because a consonant + y was read as consonant + i (akyat -> ki-at)"""
    n = nvow(body.replace("ʔ", ""))
    if n < len(re.findall(r"[aeiouáéíóúàèìòùâêîôû]+", form.lower())):
        return True
    return n > len(form_vowels(form)) and bool(re.search(r"[bdfghklmnprstvwz]y[aeiouáéíóúàèìòùâêîôû]", form.lower()))


def stress_ok(form, body):
    """True when the reading stresses a vowel that the accent marks of the spelling allow: an acute or circumflex marks the
    stressed vowel itself, a final grave means penultimate stress, a non-final grave marks the vowel.  Words with several
    marks (présidént) allow any of them; loanwords whose vowel structure differs are not compared."""
    chars = [c for c in form.lower() if c in FORM_V or c in ACCENTED]
    if not any(c in ACCENTED for c in chars) or "ˈ" not in body:
        return True
    if nvow(body.replace("ʔ", "")) != len(chars):
        return True
    n, ok = len(chars), set()
    for k, c in enumerate(chars):
        if c in ACCENTED:
            ok.add(max(0, n - 2) if (c in "àèìòù" and k == n - 1) else k)
    return stress_index(body) in ok


ALT_SENSE = re.compile(r"variante de|forma alternativa|grafia alternativa|sinônimo de", re.I)      # Tagalog variants, not English
NAME_SENSE = re.compile(r"sobrenome|prenome|nome pr[óo]prio|nome de (?:homem|mulher|pessoa)|nome masculino|nome feminino|apelido", re.I)


def fix(r):
    form, src, ipa = r[0], r[6], r[3]
    is_name = bool(NAME_SENSE.search(r[5])) or form[:1].isupper()      # names keep their dictionary / rule reading
    new, nsrc, why = ipa, src, None
    if src == "english":
        return new, nsrc, why
    if src == "dictionary":
        m = re.match(r"(/[^/]*/)", ipa)
        body = m.group(1).strip("/") if m else ipa.strip("/")
        if m and m.group(1) != ipa:
            why = "note removed"
        multi = " " in body
        dots = "." in body
        if multi or "ʎ" in body:
            e = cmu_ipa(form) if not has_accent(form) and not is_name else None
            if e:
                new, nsrc, why = e, "english", "multi-word/ly reading rebuilt from CMUdict"
            elif re.search(r"[aeiou]", plain(form)):
                new, nsrc, why = M.ipa(form), "rule", "multi-word/ly reading rebuilt by rule"
            else:
                new, nsrc, why = M.spelled(form), "spelled", "multi-word reading spelled by letters"
        else:
            body = normalise(body)
            if "." in body:
                body = body.replace(".", "")
            nb = move_stress(body, form)
            raw = nb                                       # before the glottal stops: spelling leftovers show here
            tl = tagalog_like(form)
            if tl:
                nb = hiatus(nb)
            new = "/" + nb + "/"
            if new != ipa:
                why = why or ("notation" if dots else "cleaned")
            e = None
            if not has_accent(form) and not is_name and (LEFTOVER.search(raw) or (not tl and re.search(r"[aeiou][aeiou]", raw))):
                e = cmu_ipa(form)
            if e:
                new, nsrc, why = e, "english", "spelling leftovers in reading"
            elif tl and broken(form, nb) and re.search(r"[aeiou]", plain(form)):
                rule = M.ipa(form)
                if nvow(rule.replace("ʔ", "")) == len(form_vowels(form)):
                    new, nsrc, why = rule, "rule", "reading lost vowels or read consonant+y as consonant+i"
            elif tl and not stress_ok(form, nb):
                rule = M.ipa(form)
                if nvow(rule.replace("ʔ", "")) == len(form_vowels(form)):
                    new, nsrc, why = rule, "rule", "stress did not match the accent mark"
    else:                                                # rule / spelled
        p = plain(form)
        looks_english = FOREIGN_LETTERS.search(p) or (src == "spelled" and "y" in p) or (
            src == "rule" and (len(p) >= 6 or re.search(r"([^aeiou])\1", p)) and not ALT_SENSE.search(r[5]))   # long / doubled consonant
        english = not has_accent(form) and not is_name and re.search(r"[aeiouy]", p) and looks_english
        if english:
            e = cmu_ipa(form)
            if e:
                new, nsrc, why = e, "english", "English loanword"
        if nsrc == src:                                  # regenerate with the corrected rule
            vowelless = not re.search(r"[aeiou]", plain(form))
            g = M.spelled(form) if vowelless else M.ipa(form)
            nsrc = "spelled" if vowelless else "rule"
            if g and (g != ipa or nsrc != src):
                new, why = g, "rule updated" if g != ipa else "label corrected (spelled -> rule)"
    return new, nsrc, why


def main():
    write = "--write" in sys.argv
    lines = open("wordlist_all.tsv", encoding="utf-8").read().split("\n")
    header, body = lines[0], lines[1:]
    if body and body[-1] == "":
        body.pop()
    out, stats, samples = [header], {}, {}
    for ln in body:
        r = ln.split("\t")
        assert len(r) == 7, ln[:80]
        first = r[3]
        why = None
        for _ in range(4):                               # repeat until stable (a rule reading can still be an English word)
            new, nsrc, w = fix(r)
            if new == r[3] and nsrc == r[6]:
                break
            r[3], r[6], why = new, nsrc, w
        if why:
            stats[why] = stats.get(why, 0) + 1
            samples.setdefault(why, []).append((r[0], first, r[3]))
        out.append("\t".join(r))
    for k, v in sorted(stats.items(), key=lambda kv: -kv[1]):
        print(f"{v:7}  {k}")
        for s in samples[k][:4]:
            print(f"           {s[0]}   {s[1]}  ->  {s[2]}")
    if write:
        open("wordlist_all.tsv", "w", encoding="utf-8").write("\n".join(out) + "\n")
        print("wordlist_all.tsv rewritten; now run scripts/build_index.py")


if __name__ == "__main__":
    main()
