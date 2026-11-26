# Does a common-gender noun's stereotype predict its lean? (pre-registration, paper B)

*Status: **ADOPTED 2026-11-26** (adoption record at the end). Nothing scored at adoption. Complements the crime probe
(`crime-noun-probe-prereg.md`), which can only fail in one direction.*

## Question

Common-gender person nouns (*el/la periodista*, *le/la secrétaire*) have one form for both sexes, so
their vector carries no fixed grammatical gender. **Does a noun lean further toward the female attribute
words the more its role is stereotyped as female?** The prediction can fail in either direction: a
noun rated mostly male should lean male, one rated mostly female should lean female, relative to a
sex-neutral zero point.

## Why this design

A Glasgow-stratified version (female / neutral / male) was not feasible: only one Spanish and one
French held-out common-gender noun has a female-rated (GEND ≤ 3) English gloss. Two causes: Glasgow
lacks most role nouns (*receptionist*, *cosmetician*), and female-stereotyped roles mostly have their
own feminine form (*enfermera*, *infirmière*), so few remain common-gender (itself a descriptive
finding). Misersky et al. (2014) rate role nouns directly (estimated share of women, 0–1, 1,663 raters,
gendered nouns shown in both masculine and feminine plural forms), which covers far more of them; the
female side is still thin (ES 6, FR 9 rated ≥ .60), so the test is a slope over all matched nouns, not
a comparison of strata.

## Materials

- Space, attribute words and zero point exactly as the zero-point study: MUSE `wiki.multi.{es,fr}`
  (first 200k words for the test nouns), raw dot products, corrected native attribute lists (primary)
  and English attributes in the aligned space (secondary), zero point c = strict-epicene anchor
  (inanimate anchor as check). Original space only.
- **Nouns** (`scripts/stereo_misersky_build.py` → `data/stereo_misersky_{es,fr}_candidates_v0.csv`):
  common-gender person nouns by the frozen "common" rule (Zipf ≥ 2), matched to a Misersky role noun by
  the English gloss's plural. Candidates: ES 76, FR 62. The PI marks `pi_keep`; Claude's suggestions
  (`claude_suggest_unverified`) drop English loans (*runner, cheerleader, bartender, teenager,
  celebrity, fan, courier, drummer, boss, people*), slang and fan-of-a-club words (*beibi, transa,
  xeneize, sevillista*), clipped forms (*inge*) and a non-person sense (*estafeta*).
- **Rating:** Spanish nouns use the English rating of their gloss; French nouns the French rating.
  The other language's rating is kept for a check.
- Norms: `/Volumes/Lexar/gbleed/shared/misersky2014/norms.csv`, extracted from the article's Table 3
  by `scripts/misersky_extract.py` (PI's licensed copy; not redistributed).

## Measures

- Lean L(w) = s(w) − c (s as in the zero-point study; positive = toward the male attribute words).
- **Primary:** slope β of L on the rating (standardised), over all kept nouns. Prediction β < 0 (more
  women estimated → leans more female).
- 95% joint bootstrap (10,000, seed 0): nouns, epicene reference words (within gender), attribute words.
- Descriptive: mean L by stratum (rating ≥ .60 / .40–.60 / < .40) with intervals; a figure of L
  against rating.

## Reading (fixed before data)

1. **Stereotype tracked** if β's 95% CI is below 0; **reversed** if above 0; else **not shown**.
2. Floor: at least 25 kept nouns per language, else "too few" (French descriptive if below).
3. Sensitivity (reported, not used for verdicts):
   (a) **held-out only**: nouns not in the exploratory common-gender check (`in_exploratory` False;
   ES 46, FR 25 before review), the same tiering as the flagged-occupation checks;
   (b) without nouns spelled as their English gloss (`identical_en`);
   (c) the other language's rating (Spanish with French ratings, French with English);
   (d) inanimate anchor; (e) English attribute words.

## Predictions (Claude, before scoring)

Spanish stereotype tracked (the exploratory Glasgow check gave r 0.69 with English attributes, though
with native attributes the interval touched 0); French tracked but weaker. Held-out-only intervals
wide, same sign.

## Open for the PI

1. Review the candidate lists (`pi_keep`).
2. Slope as primary, strata descriptive?
3. Floor of 25 nouns per language?

## Adoption record (2026-11-26)

- PI: prereg adopted as drafted; slope primary, strata descriptive; floor 25; Spanish uses English
  ratings (no Romance-language substitution); English loans dropped; held-out-only check tiered like the
  flagged-occupation checks.
- PI review of both candidate lists (Numbers files, exported as `*_candidates_v0_edited.csv`), plus in
  conversation: drop *courier* (loan) and *guarda* (sense mismatch: 'keeper, warden', matched to
  Misersky's "Guards" by gloss only; *guardia* is not in the pool because its gloss is sex-marked).
- **Added rule (PI, before scoring): nouns with a separate gendered singular form** (Wiktionary, plus the
  PI's RAE findings *bedel/bedela*, *modista/modisto*) leave the primary set: where *jueza* or *poétesse*
  exists the shared form drifts toward one sex, and such forms arise mainly for historically male roles,
  so they would inflate the slope. Kept as sensitivity check (d') "including separate-form nouns".
- Test nouns restricted to the first 200k words (stated above; the candidate builder had not applied it).
- Frozen by `scripts/stereo_misersky_freeze.py`: `data/stereo_misersky_es_frozen_v1.csv` (sha256
  8000855bdb079c0d…): primary 46 (rated ≥ .60: 4, .40–.60: 19, < .40: 23; held out 24), separate-form 10;
  `data/stereo_misersky_fr_frozen_v1.csv` (42cf10aaa67cf77b…): primary 52 (8 / 27 / 17; held out 20, so
  the held-out French check is reported as "few nouns"), separate-form 3.
- Note: the zero point c shifts every lean equally, so it does not change β; it enters only the stratum
  means. Scoring script `scripts/stereo_probe.py`, committed with this record before any score.

## Results (2026-11-26, `results/stereo_probe/`)

- **Spanish: stereotype tracked.** β −0.022 [−0.037, −0.008] (r −0.66, 46 nouns); English attributes
  −0.026 [−0.038, −0.013].
- **French: stereotype tracked.** β −0.021 [−0.034, −0.009] (r −0.60, 52 nouns); English attributes
  −0.021 [−0.035, −0.009].
- Sensitivity: no-English-spelling, other-language rating and including separate-form nouns all
  tracked in both languages. Held-out only: Spanish not shown (−0.014 [−0.033, 0.006], 24 nouns, same
  sign); French tracked (−0.026, 20 nouns, below the floor).
- Descriptive strata (epicene zero, native attributes): male-rated roles lean male (ES +0.029
  [0.001, 0.058]); female-rated lean female but with few nouns the interval crosses 0 (ES −0.046, 4
  nouns; FR −0.023, 8 nouns); neutral ≈ 0.
- Predictions: Spanish tracked (right); French tracked but weaker (wrong: about the same); held-out
  same sign with wide intervals (right).
