# Independent check: a claim about Zhou et al. (2019), "Shift Ori"

You are checking a claim made by someone else. Be sceptical: your job is to confirm it, refute it,
or narrow it, with your own reasoning and your own code. Don't look for, or ask for, the claimant's
derivation or code; there is none in this folder on purpose.

## Materials (all in this folder)

- `zhou2019_arxiv1909.02224.pdf`: Zhou, Shi, Zhao, Huang, Chen, Cotterell, Chang (2019),
  "Examining Gender Bias in Languages with Grammatical Gender", EMNLP-IJCNLP.
- `zhou_repo/`: the authors' released code and word lists (https://github.com/shaoxia57/Bias_in_Gendered_Languages,
  commit 6392702). Main file `bias_emnlp19.ipynb` (saved outputs included).
- `data/wiki.multi.es.vec`, `data/wiki.multi.fr.vec`: MUSE aligned fastText vectors (the paper uses
  the first 50,000 words). The notebook's other intermediate files (`./data/…debiased…`) are not
  available.

## The claims to check

1. **Identity.** For the paper's MWEAT–Diff statistic (§4.2, Table 1) computed on the occupation
   pairs after the Shift Ori mitigation (§3.1 Eq. 4 with the origin as anchor, §3.2), the value
   equals |Σ over all occupation words w of (w · a⊥)|, where a = (mean of the male attribute word
   vectors) − (mean of the female attribute word vectors) and a⊥ is a with its component along the
   semantic gender direction d_s removed. Consequently the post-mitigation value is fixed by the
   original embeddings and does not reflect any change in the masculine/feminine asymmetry.
   (Under what conditions, if any, does this hold? Is it exact?)
2. **Permutation test.** The MWEAT permutation p-values reported after Shift Ori / Hybrid Ori
   (Table 1) are not meaningful because a large share of permutations reproduce the observed
   statistic exactly.
3. **Code vs paper.** The released notebook never applies Eq. (2) (removing d_s from inanimate
   nouns), and the Spanish Shift Ori embedding it evaluates is loaded from a file not in the repo.
   The words shifted under Eq. (4) are the same occupation words MWEAT scores.

## What to deliver (write to `REPORT.md` in this folder)

- For each claim: CONFIRMED / REFUTED / PARTLY, with your reasoning. For claim 1, a derivation in
  your own words that a reader can check without running code, and the conditions it needs.
- For claims 2–3: the exact notebook cell indices (0-based) and line numbers you rely on.
- If you compute numbers, give the script you wrote and its output; note anything you couldn't
  reproduce (e.g. which gender-direction estimator matches the paper's reported cos 0.389).
- Anything the claim gets wrong or overstates.

Rules: don't contact anyone; don't use material outside this folder except to install standard
Python packages; say plainly when something can't be determined from the release.
