"""Person-noun word-pair test as counts (exploratory, paper B, 2026-11-26): the counts companion of
wordpair_persons.py / wordpair_persons_extra.py, as wordpair_counts.py is for the occupation cue study.

Same frozen nouns (data/wp_persons_{es,fr}_frozen_v1.csv; groups person / occupation / identity), cues
(frozen v1 primary), original space and scoring (wordpair_mechanism.rr_table). For each group and cue type
(masculine, invariant, feminine), shares of queries in which the masculine / feminine form is the first
word retrieved (after the cue word), is in the top ten, or ranks above the other form (a form outside the
top 999 counts as last), and in which neither form is retrieved. No intervals (descriptive).
Added 2026-11-26 (second run): plain translation (query = the English noun alone, as
wordpair_persons_extra.plain) and every condition again without flagged nouns (subset "no_flags").

    uv run --no-project --python 3.12 --with numpy,pandas,scikit-learn python scripts/wordpair_persons_counts.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
from wordpair_mechanism import rr_table
from wordpair_persons_extra import plain
from zhou_shift import Z, load_vec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/wordpair_persons_counts"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cues = pd.read_csv(ROOT / "data/wp_cues_frozen_v1.csv", keep_default_na=False, dtype=str)
    en, en_w2i = load_vec(Z / "data/wiki.multi.en.vec.txt", nmax=200000)
    rows = []
    for lang in ("es", "fr"):
        nouns = pd.read_csv(ROOT / f"data/wp_persons_{lang}_frozen_v1.csv", keep_default_na=False, dtype=str)
        T, w2i = load_vec(Z / f"data/wiki.multi.{lang}.vec.txt")
        i2w = {i: w for w, i in w2i.items()}
        nouns = nouns[nouns.en.isin(en_w2i) & nouns.masc.isin(w2i) & nouns.fem.isin(w2i)].reset_index(drop=True)
        occ = [(f, m, e) for f, m, e in zip(nouns.fem, nouns.masc, nouns.en)]
        cs = cues[(cues.lang == lang) & (cues.subset == "primary")]
        G, I = cs[cs.type == "gendered"], cs[cs.type == "invariant"]
        qs = {"masculine": [(e, x, "m") for e, x in zip(G.en, G.masc)],
              "feminine": [(e, x, "f") for e, x in zip(G.en, G.fem)],
              "invariant": [(e, x, "inv") for e, x in zip(I.en, I.masc)]}  # fmt: skip
        flags = ["fem_also_noun", "masc_also_noun", "language_name", "masc_identical_en", "place_name"]
        clean = ~nouns[[f for f in flags if f in nouns]].eq("True").any(axis=1).to_numpy()
        tables = {t: rr_table(en, T, en_w2i, w2i, i2w, q, occ) for t, q in qs.items()}  # [cue, noun, 2]
        tables["plain"] = plain(en, T, en_w2i, w2i, i2w, occ)
        for t, R in tables.items():
            for g, sub in [(g, sub) for g in ("person", "occupation", "identity") for sub in ("all", "no_flags")]:
                ix = np.flatnonzero((nouns.group.to_numpy() == g) & (clean if sub == "no_flags" else True))
                rm, rf = R[:, ix, 0].ravel(), R[:, ix, 1].ravel()
                n = len(rm)
                c = {"masc_top1": (rm == 1).sum(), "fem_top1": (rf == 1).sum(),
                     "masc_top10": (rm >= 0.1).sum(), "fem_top10": (rf >= 0.1).sum(),
                     "masc_wins": (rm > rf).sum(), "fem_wins": (rf > rm).sum(), "neither": ((rm == 0) & (rf == 0)).sum()}  # fmt: skip
                rows.append({"lang": lang, "group": g, "subset": sub, "n_nouns": len(ix), "cue_type": t, "n_queries": n,
                             **{k: int(v) for k, v in c.items()}, **{f"{k}_share": v / n for k, v in c.items()}})  # fmt: skip
        print("done", lang, flush=True)
    d = pd.DataFrame(rows)
    d.to_csv(OUT / "counts.csv", index=False)
    print(d[["lang", "group", "subset", "cue_type", "n_queries"] + [c for c in d.columns if c.endswith("_share")]].round(3).to_string(index=False))
    print("=== WPPCOUNTS done")


if __name__ == "__main__":
    main()
