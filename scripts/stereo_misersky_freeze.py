"""Freeze the stereotype-probe noun lists (docs/stereotype-probe-prereg.md; PI review 2026-11-26).

Input: the PI's reviewed candidates (data/stereo_misersky_{es,fr}_candidates_v0.numbers, pi_keep column;
exported here to data/stereo_misersky_{lang}_candidates_v0_edited.csv). Rules, in order:
  1. PI drops: pi_keep starting "drop" (incl. "drop?" rows, which the separate-form rule covers anyway),
     plus PI decisions in conversation: courier (English loan), guarda (sense mismatch: 'keeper, warden',
     not 'guard').
  2. Separate gendered form (alt_form): Wiktionary lists a separate feminine (or masculine) singular form
     (juez/jueza, poète/poétesse), plus the PI's RAE findings bedel/bedela, modista/modisto. Out of the
     primary set; kept as the "including separate-form nouns" sensitivity set.
  3. In the first 200k MUSE words of the language.
Output data/stereo_misersky_{lang}_frozen_v1.csv with columns set (primary | alt_form) and in_exploratory,
identical_en for the sensitivity checks.

    uv run --no-project --python 3.12 --with numbers-parser,pandas python scripts/stereo_misersky_freeze.py
"""

import json
from pathlib import Path

import pandas as pd
from numbers_parser import Document
from zhou_shift import Z

ROOT = Path(__file__).resolve().parents[1]
KK = Path("/Volumes/Lexar/gbleed/shared/kaikki")
DUMP = {"es": "Spanish", "fr": "French"}
PI_DROP = {"es": {"courier", "guarda"}, "fr": set()}
PI_ALT = {"es": {"bedel", "modista"}, "fr": set()}


def reviewed(lang):
    t = Document(ROOT / f"data/stereo_misersky_{lang}_candidates_v0.numbers").sheets[0].tables[0]
    rows = t.rows(values_only=True)
    cols = [c if c else f"pi_note{i}" for i, c in enumerate(rows[0])]
    d = pd.DataFrame(rows[1:], columns=cols)
    note = [c for c in cols if c.startswith("pi_note")]
    d = d.rename(columns={note[0]: "pi_note"}) if note else d.assign(pi_note=None)
    d.to_csv(ROOT / f"data/stereo_misersky_{lang}_candidates_v0_edited.csv", index=False)
    return d


def alt_forms(lang, words):
    out = {}
    with open(KK / f"kaikki.org-dictionary-{DUMP[lang]}.jsonl", encoding="utf-8") as f:
        for line in f:
            if '"pos": "noun"' not in line:
                continue
            j = json.loads(line)
            w = j.get("word")
            if w not in words:
                continue
            for x in j.get("forms", []):
                t = x.get("tags", [])
                if ("feminine" in t or "masculine" in t) and "plural" not in t and x.get("form") not in (w, None):
                    out.setdefault(w, set()).add(x["form"])
    return out


def vocab(lang, n=200_000):
    out = set()
    with open(Z / f"data/wiki.multi.{lang}.vec.txt", encoding="utf-8", errors="ignore") as f:
        next(f)
        for i, line in enumerate(f):
            if i >= n:
                break
            out.add(line.split(" ", 1)[0])
    return out


def main():
    for lang in ("es", "fr"):
        d = reviewed(lang)
        pk = d.pi_keep.fillna("").astype(str).str.strip().str.lower()
        drop = pk.str.startswith("drop") | d.lemma.isin(PI_DROP[lang])
        alt = alt_forms(lang, set(d.lemma))
        d["alt_form_of"] = d.lemma.map(lambda w: ", ".join(sorted(alt.get(w, ""))))
        d.loc[d.lemma == "bedel", "alt_form_of"] = "bedela (RAE, PI)"
        d.loc[d.lemma == "modista", "alt_form_of"] = "modisto (RAE, PI)"
        is_alt = (d.alt_form_of != "") | d.lemma.isin(PI_ALT[lang])
        V = vocab(lang)
        d["in_200k"] = d.lemma.isin(V)
        # PI drops that are separate-form nouns (maire "drop?", juez "drop?") stay as alt_form, not dropped
        keep = d.in_200k & (~drop | (is_alt & pk.str.startswith("drop?")))
        d["set"] = ["alt_form" if a else "primary" for a in is_alt]
        F = d[keep & ~((d.set == "alt_form") & drop & ~pk.str.startswith("drop?"))].copy()
        F = F[["lemma", "concept_en", "role", "rating", "en_rating", "fr_rating", "set", "alt_form_of",
               "in_exploratory", "identical_en", "pi_note"]]  # fmt: skip
        F.to_csv(ROOT / f"data/stereo_misersky_{lang}_frozen_v1.csv", index=False)
        P = F[F.set == "primary"]
        print(lang, "primary", len(P), "| alt_form", (F.set == "alt_form").sum(),
              "| primary by rating: f", (P.rating >= .6).sum(), "n", ((P.rating >= .4) & (P.rating < .6)).sum(), "m", (P.rating < .4).sum(),
              "| held out (primary)", (~P.in_exploratory.astype(str).str.lower().eq("true")).sum())  # fmt: skip
        print("   alt_form:", ", ".join(f"{a}/{b}" for a, b in zip(F[F.set == 'alt_form'].lemma, F[F.set == 'alt_form'].alt_form_of)))


if __name__ == "__main__":
    main()
