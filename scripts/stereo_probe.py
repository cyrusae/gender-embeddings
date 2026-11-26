"""Stereotype probe on common-gender person nouns (docs/stereotype-probe-prereg.md, ADOPTED 2026-11-26).
Committed before any score.

s(w) = mean_{x in male attr} w·x − mean_{y in female attr} w·y (raw dot products, as the zero-point study
and crime_probe.py; same attribute lists, same 50k-restricted epicene / inanimate anchors). Lean
L(w) = s(w) − c. Nouns: data/stereo_misersky_{lang}_frozen_v1.csv, set "primary" (in the first 200k words).
Primary: slope β of L on the standardised Misersky rating (estimated share of women; Spanish English
rating, French French rating). Because c shifts every lean equally it does not change β; it matters only
for the descriptive stratum means. Also reported: Pearson r.
Joint bootstrap (10,000, seed 0): nouns, attribute words, epicene words (within gender).
Reading: β CI below 0 = stereotype tracked; above 0 = reversed; else not shown. Floor 25 nouns.
Sensitivity (2,000 draws): held-out only (not in the exploratory common-gender check); without nouns
spelled as their English gloss; the other language's rating; including the separate-form nouns
(set alt_form). English attribute words are run as a second yardstick throughout; the inanimate anchor
changes only the stratum means and is reported there.

    uv run --no-project --python 3.12 --with numpy,pandas python scripts/stereo_probe.py
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from c1_run import EN_F, EN_M
from crime_probe import load
from zhou_shift import Z, attributes

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/stereo_probe"
FLOOR, N_BOOT, SEED = 25, 10_000, 0
STRATA = (("female (>= .60)", 0.6, 1.01), ("neutral (.40-.60)", 0.4, 0.6), ("male (< .40)", 0.0, 0.4))


def truthy(x):
    return x.astype(str).str.lower().eq("true")


def stats(Pm, Pf, rating, Em, Ef, eg, Im, If, ig, am, af, ni, ei, ii):
    s = Pm[ni][:, am].mean(1) - Pf[ni][:, af].mean(1)
    r = rating[ni]
    z = (r - r.mean()) / r.std()
    beta = (z * (s - s.mean())).sum() / (z * z).sum()
    out = {"beta": beta, "r": np.corrcoef(r, s)[0, 1] if s.std() > 0 else np.nan}
    for anc, (Am, Af, g, ix) in {"epicene": (Em, Ef, eg, ei), "inanimate": (Im, If, ig, ii)}.items():
        se = Am[ix][:, am].mean(1) - Af[ix][:, af].mean(1)
        gg = g[ix]
        c = 0.5 * (se[gg == "m"].mean() + se[gg == "f"].mean())
        for lab, lo, hi in STRATA:
            k = (r >= lo) & (r < hi)
            out[f"L_{anc}|{lab}"] = (s[k] - c).mean() if k.any() else np.nan
    return out


def run(E, w2i, AM, AF, nouns, rating, epi, ina, n, rng):
    AM, AF = np.array(AM), np.array(AF)
    V = lambda ws: np.array([E[w2i[w]] for w in ws])  # noqa: E731
    X, Ex, Ix = V(nouns), V(epi.lemma), V(ina.lemma)
    P = (X @ AM.T, X @ AF.T)
    EP, IP = (Ex @ AM.T, Ex @ AF.T), (Ix @ AM.T, Ix @ AF.T)
    eg, ig = epi.gender.to_numpy(), ina.gender.to_numpy()
    rating = np.asarray(rating, float)
    nm, nf, nn = AM.shape[0], AF.shape[0], len(nouns)
    full = (slice(None), slice(None), np.arange(nn), np.arange(len(eg)), np.arange(len(ig)))
    pt = stats(*P, rating, *EP, eg, *IP, ig, *full)
    B = []
    for _ in range(n):
        ei = np.concatenate([rng.choice(np.flatnonzero(eg == x), (eg == x).sum()) for x in "mf"])
        ii = np.concatenate([rng.choice(np.flatnonzero(ig == x), (ig == x).sum()) for x in "mf"])
        B.append(stats(*P, rating, *EP, eg, *IP, ig, rng.integers(0, nm, nm), rng.integers(0, nf, nf),
                       rng.integers(0, nn, nn), ei, ii))  # fmt: skip
    return pt, pd.DataFrame(B)


def verdict(lo, hi):
    return "stereotype tracked" if hi < 0 else "reversed" if lo > 0 else "not shown"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    en, en_w2i = load(Z / "data/wiki.multi.en.vec.txt", 200_000)
    rows, info = [], {}
    rng = np.random.default_rng(SEED)
    for lang in ("es", "fr"):
        E, w2i = load(Z / f"data/wiki.multi.{lang}.vec.txt", 200_000)
        defs = json.load(open(Z / f"{lang.upper()}_definitional_pairs.json"))
        am, af = attributes(lang, defs)
        occ = {w for line in open(Z / f"{lang.upper()}_occupation_words_with_EN_translations")
               for w in line.rstrip("\n").split("\t")[:2]}  # fmt: skip
        ref = pd.read_csv(ROOT / f"data/zero_ref_{lang}_frozen_v1.csv")
        ref = ref[ref.lemma.map(lambda w: w2i.get(w, 10**9) < 50_000) & ~ref.lemma.isin(occ | set(am) | set(af))]
        epi = ref[(ref.set == "epicene") & (ref.tier == "strict")]
        ina = ref[ref.set == "inanimate"]
        F = pd.read_csv(ROOT / f"data/stereo_misersky_{lang}_frozen_v1.csv", keep_default_na=False)
        F = F[F.lemma.isin(w2i)]
        F["rating"] = F.rating.astype(float)
        other = "fr_rating" if lang == "es" else "en_rating"
        prim = F[F.set == "primary"]
        checks = {"main": prim,
                  "held_out_only": prim[~truthy(prim.in_exploratory)],
                  "no_identical_en": prim[~truthy(prim.identical_en)],
                  "other_language_rating": prim[pd.to_numeric(prim[other], errors="coerce").notna()].assign(rating=lambda x: pd.to_numeric(x[other])),
                  "incl_separate_form": F}  # fmt: skip
        info[lang] = {k: len(v) for k, v in checks.items()} | {"epicene_by_gender": epi.gender.value_counts().to_dict()}
        yard = {"native": ([E[w2i[w]] for w in am], [E[w2i[w]] for w in af]),
                "english": ([en[en_w2i[w]] for w in EN_M], [en[en_w2i[w]] for w in EN_F])}  # fmt: skip
        for y, (AM, AF) in yard.items():
            for chk, sub in checks.items():
                if len(sub) < FLOOR and chk == "main":
                    rows.append({"lang": lang, "yardstick": y, "check": chk, "measure": "beta", "verdict": f"too few ({len(sub)})"})
                    continue
                pt, B = run(E, w2i, AM, AF, sub.lemma.tolist(), sub.rating, epi, ina, N_BOOT if chk == "main" else 2000, rng)
                for k, v in pt.items():
                    lo, hi = np.nanpercentile(B[k], [2.5, 97.5])
                    v_ = verdict(lo, hi) if k == "beta" else ""
                    if k == "beta" and len(sub) < FLOOR:
                        v_ += f" (few nouns: {len(sub)})"
                    rows.append({"lang": lang, "yardstick": y, "check": chk, "n": len(sub), "measure": k, "value": v, "lo": lo, "hi": hi, "verdict": v_})
        print("done", lang, flush=True)
    R = pd.DataFrame(rows)
    R.to_csv(OUT / "results.csv", index=False)
    json.dump(info, open(OUT / "info.json", "w"), indent=1, ensure_ascii=False)
    with pd.option_context("display.width", 220, "display.max_columns", 20, "display.max_rows", 200):
        print(json.dumps(info))
        print(R[R.measure.isin(["beta", "r"]) | (R.check == "main")].round(4).to_string(index=False))
    print("=== STEREO done")


if __name__ == "__main__":
    main()
