"""Word-pair plurals study as counts (exploratory, paper B, 2026-11-26): the counts companion of
wordpair_plurals.py (docs/wordpair-plurals-prereg.md). Same occupations, cues, queries, 200k vocabulary
and scoring (wordpair_plurals.rr: reciprocal rank among the top 999, cue form removed). For each arm
(singular / plural cues) and cue type, shares of queries in which each of the four occupation forms
(m_sg, m_pl, f_sg, f_pl) is (a) the first word retrieved and (b) the highest-ranked of the four; and in
which none of the four is retrieved. No intervals (descriptive).

    uv run --no-project --python 3.12 --with numpy,pandas python scripts/wordpair_plurals_counts.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
import wordpair_plurals as wp
from zhou_shift import Z, load_vec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/wordpair_plurals_counts"
FORMS = ("m_sg", "m_pl", "f_sg", "f_pl")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    en, en_w2i = load_vec(Z / "data/wiki.multi.en.vec.txt", nmax=200000)
    cues = pd.read_csv(ROOT / "data/wp_cues_frozen_v1.csv", keep_default_na=False, dtype=str)
    pcues = pd.read_csv(ROOT / "data/wp_plural_cues_v0.csv", keep_default_na=False, dtype=str)
    gm = pd.read_csv(ROOT / "data/gm_pairs_frozen_v1.csv", keep_default_na=False, dtype=str)
    mp = pd.read_csv(ROOT / "data/occupation_mapping_v1.csv")
    enp = pd.read_csv(ROOT / "data/wp_plural_occ_en_v0.csv", keep_default_na=False, dtype=str)
    rows = []
    for lang in ("es", "fr"):
        T, w2i = load_vec(Z / f"data/wiki.multi.{lang}.vec.txt", nmax=200000)
        wp.Tn_raw = T
        Tn = T / np.linalg.norm(T, axis=1, keepdims=True)
        m = mp[(mp.lang == lang) & mp.clean_keep].merge(gm[gm.lang == lang][["masc", "fem", "masc_pl", "fem_pl"]], on=["masc", "fem"], how="left")
        m = m.merge(enp[enp.lang == lang][["masc", "en_pl"]], on="masc", how="left")
        m = m[m.en.isin(en_w2i)]
        occ = m[m[["masc", "fem", "masc_pl", "fem_pl"]].isin(list(w2i)).all(axis=1)].reset_index(drop=True)
        fidx = np.array([[w2i[r[c]] for c in ("masc", "masc_pl", "fem", "fem_pl")] for _, r in occ.iterrows()])
        cs = cues[(cues.lang == lang) & (cues.subset == "primary")]
        G = cs[cs.type == "gendered"].reset_index(drop=True)
        I = cs[cs.type == "invariant"].reset_index(drop=True)
        pc = pcues[pcues.lang == lang]
        Gp = G.merge(pc[pc.type == "gendered"][["masc", "masc_pl", "fem_pl"]], on="masc", how="left")
        Ip = I.merge(pc[pc.type == "invariant"][["masc", "masc_pl"]], on="masc", how="left")
        Gq = Gp[Gp.masc_pl.isin(w2i) & Gp.fem_pl.isin(w2i)].reset_index(drop=True)
        Iq = Ip[Ip.masc_pl.isin(w2i)].reset_index(drop=True)

        def table(cue_rows, form_col, occ_col):
            q, fi = [], []
            for _, c in cue_rows.iterrows():
                for oi, o in occ.iterrows():
                    q.append((o[occ_col], c.en, c[form_col]))
                    fi.append(fidx[oi])
            return wp.rr(en, en_w2i, Tn, w2i, q, np.array(fi))

        R = {("singular", "masculine"): table(G, "masc", "en"), ("singular", "feminine"): table(G, "fem", "en"),
             ("singular", "invariant"): table(I, "masc", "en"),
             ("plural", "masculine"): table(Gq, "masc_pl", "en_pl"), ("plural", "feminine"): table(Gq, "fem_pl", "en_pl"),
             ("plural", "invariant"): table(Iq, "masc_pl", "en_pl")}  # fmt: skip
        for (arm, t), X in R.items():
            n = len(X)
            best = np.where(X.max(1) > 0, X.argmax(1), -1)
            r = {"lang": lang, "arm": arm, "cue_type": t, "n_occupations": len(occ), "n_queries": n,
                 "none_of_four": float((best == -1).mean())}  # fmt: skip
            for k, f in enumerate(FORMS):
                r[f"{f}_first"] = float((X[:, k] == 1).mean())
                r[f"{f}_best_of_four"] = float((best == k).mean())
            rows.append(r)
        print("done", lang, flush=True)
    d = pd.DataFrame(rows)
    d.to_csv(OUT / "counts.csv", index=False)
    print(d.round(3).to_string(index=False))
    print("=== WPPLCOUNTS done")


if __name__ == "__main__":
    main()
