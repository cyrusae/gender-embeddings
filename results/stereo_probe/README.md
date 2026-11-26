# Stereotype probe on common-gender person nouns (paper B; docs/stereotype-probe-prereg.md, adopted 2026-11-26)

`scripts/stereo_probe.py` (committed before scoring, 88af7bf). Lean of each common-gender noun on the
attribute axis regressed on its Misersky et al. (2014) role-noun rating (estimated share of women).
β = change in lean per SD of rating; negative = more women estimated → leans more female.

| | n | β native [95% CI] | r | verdict | β English attributes |
|---|---|---|---|---|---|
| Spanish | 46 | −0.022 [−0.037, −0.008] | −0.66 | stereotype tracked | −0.026 [−0.038, −0.013] |
| French | 52 | −0.021 [−0.034, −0.009] | −0.60 | stereotype tracked | −0.021 [−0.035, −0.009] |

Sensitivity: unchanged without nouns spelled as their English gloss, with the other language's ratings,
and including the separate-form nouns (ES 56, FR 55). Held-out only (nouns not in the exploratory check):
Spanish −0.014 [−0.033, 0.006], not shown (24 nouns); French −0.026 [−0.044, −0.008] (20 nouns, below the
floor, "few nouns"). Stratum means from the epicene zero point (native attributes): Spanish female-rated
−0.046 [−0.107, 0.018] (4 nouns), neutral +0.005, male-rated +0.029 [0.001, 0.058]; French −0.023, +0.001,
+0.035 [−0.001, 0.072]. Files: `results.csv`, `info.json`.
