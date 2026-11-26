"""Candidates for the stereotype probe on common-gender person nouns, rated with Misersky et al. (2014)
role-noun norms (paper B; docs/stereotype-probe-prereg.md, DRAFT 2026-11-26). Built before any score.

Pool: common-gender person nouns (one form for both sexes: el/la periodista) by the rule of the frozen
zero-point "common" set (zero_ref_lists.build), Zipf >= 2, gloss not sex-denoting. Matched to a Misersky
role noun by the English gloss's plural (regular plural rule; -man -> -men). Rating = estimated share of
women, 0-1 (Spanish: English rating, French: French rating; the other language's rating is kept).
Flags (for the PI's review; not dropped here):
  loan            the lemma is the English gloss itself or another English word (cheerleader, runner)
  in_exploratory  the noun was in the exploratory common-gender check (frozen zero-point "common" set)
Output data/stereo_misersky_{es,fr}_candidates_v0.csv with claude_suggest_unverified and empty pi_keep.

    uv run python scripts/stereo_misersky_build.py
"""

import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).parent))
from gbleed.lexicon import _wordnet  # noqa: E402
from zero_ref_lists import SEXED, person_share  # noqa: E402
from zhou_shift import Z  # noqa: E402

NORMS = Path("/Volumes/Lexar/gbleed/shared/misersky2014/norms.csv")
OUT = ROOT / "embeddings/data"


def plural(g):
    w = str(g).lower().split()
    if not w:
        return ""
    last = w[-1]
    if last.endswith("man"):
        p = last[:-3] + "men"
    elif re.search(r"(s|x|ch|sh)$", last):
        p = last + "es"
    elif re.search(r"[^aeiou]y$", last):
        p = last[:-1] + "ies"
    else:
        p = last + "s"
    return " ".join(w[:-1] + [p])


def en_vocab(n=50_000):
    out = set()
    with open(Z / "data/wiki.multi.en.vec.txt", encoding="utf-8", errors="ignore") as f:
        next(f)
        for i, line in enumerate(f):
            if i >= n:
                break
            out.add(line.split(" ", 1)[0])
    return out


def main():
    N = pd.read_csv(NORMS)
    idx = {n.lower(): r for n, r in zip(N.english, N.itertuples())}
    wn = _wordnet()
    EN = en_vocab()
    for lang in ("es", "fr"):
        d = pd.read_csv(ROOT / f"data/lexicon/{lang}_nouns.csv", low_memory=False)
        d["person_share"] = d.concept_en.map(lambda c: person_share(wn, c))
        personish = (d.person_share > 0.5) | (d.person_share.isna() & d.animacy_reason.astype(str).str.contains("gloss"))
        r = d.animacy_reason.astype(str)
        com = d[(d.zipf >= 2) & d.marked.isna() & d.also_pos.isna() & personish & (d.gender == "multi")
                & (d.animacy == "animate") & r.str.contains("by-personal-gender") & (d.multi_type == "free_variation")
                & ~d.gloss.astype(str).str.contains(SEXED)].drop_duplicates("lemma").copy()  # fmt: skip
        com["role"] = com.concept_en.map(lambda g: idx[plural(g)].english if plural(g) in idx else "")
        com = com[com.role != ""].copy()
        row = {x: idx[x.lower()] for x in com.role}
        com["en_rating"] = [row[x].en_m for x in com.role]
        com["fr_rating"] = [row[x].fr_m for x in com.role]
        com["rating"] = com.en_rating if lang == "es" else com.fr_rating
        frozen = set(pd.read_csv(OUT / f"zero_ref_{lang}_frozen_v1.csv", dtype=str).query("set == 'common'").lemma)
        com["in_exploratory"] = com.lemma.isin(frozen)
        loan = (com.lemma.str.lower() == com.concept_en.astype(str).str.lower()) | (com.lemma.isin(EN) & ~com.lemma.str.contains("[áéíóúñàâçèêëîïôûü]") & (com.lemma.str.len() > 3) & com.lemma.str.match(r"^[a-z]+$") & ~com.lemma.str.endswith(("ista", "iste", "ta", "te", "nte", "logue", "ogo", "ga")))  # fmt: skip
        com["loan"] = loan
        com["claude_suggest_unverified"] = ["drop: English loan" if x else "" for x in loan]
        com["pi_keep"] = ""
        cols = ["lemma", "concept_en", "gloss", "zipf", "role", "rating", "en_rating", "fr_rating", "in_exploratory", "loan", "claude_suggest_unverified", "pi_keep"]
        com = com.sort_values("rating")[cols]
        com.to_csv(OUT / f"stereo_misersky_{lang}_candidates_v0.csv", index=False)
        print(lang, len(com), "loan", int(com.loan.sum()), "in_exploratory", int(com.in_exploratory.sum()), "| loans:", ", ".join(com[com.loan].lemma))


if __name__ == "__main__":
    main()
