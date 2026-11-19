# Orientation: start here (updated 2026-11-19)

This repository reproduces and re-analyses Zhou et al. (2019), "Examining Gender Bias in Languages
with Grammatical Gender", and extends it to inanimate nouns. Paths are relative to the repository
root. For who's who and the vocabulary used in these documents, see "Reading these documents" in the
README.

## Where things stand

**The project.** Two papers grow out of one question (does Zhou et al.'s bias mitigation keep the
grammatical gender of inanimate nouns?): (1) a reanalysis of Zhou et al. 2019, (2) the inanimate-noun
findings.

**State in one paragraph.** Zhou's cross-lingual bias holds and is stronger than their test showed; it
is specific to occupations (ordinary person nouns show a weaker masculine default that a feminine cue
cancels). Most of their quantitative support doesn't hold: Table 1 p-values are guaranteed or tie
artefacts, Shift's drop is algebraic and its reported size depends on a centring bug, Hybrid = Shift
on Table 1, Table 2 has no feminine cues, the French numbers come from an unreleased list, and the
attribute lists have errors. With a fair zero point their monolingual asymmetry is inconclusive in
Spanish and borderline in French. Grammatical gender of inanimates survives the mitigations; human
gender ratings of objects show up in the vectors. Claim-by-claim table: `docs/zhou-summary.md`;
inanimates: `docs/inanimates-summary.md`; every upstream issue (Z1–Z35): `docs/upstream-issues.md`.

**Authors.** Zhou et al. were contacted on 2026-11-11, before any write-up, and are preparing a
correction.

**Open.** French person-noun follow-ups; checking the mitigated results against the authors' files if
they are released.

## Conventions

- **Pre-register, commit the scoring script, then score.** Every study in `docs/*-prereg.md` has an
  adoption record; deviations are dated sections at the end of the prereg with both versions shown.
  Preregs keep their drafting history (open questions at drafting, later results and deviations), so
  read them top to bottom as a dated record.
- **Exploratory vs pre-registered:** anything not pre-registered says so in its script docstring and
  result README (`results/attrfix_sensitivity/`, `list_audit/`, `hub_csls_check/`,
  `common_gender_check/`, `z23_check/`, `word_similarity_es/`, `wordpair_cues_midpoint/`,
  `wordpair_share_check/`).
- **Attribute words:** Zhou et al.'s lists contain errors (Z19). The corrected lists (Spanish *tío*;
  French de-duplicated, names dropped) are primary and the scripts' **default**
  (`scripts/zhou_shift.py`, `attributes()`). `ZHOU_ATTR=published` reproduces Zhou's lists and the
  result folders frozen before 2026-11-11; the corrected outputs are in
  `results/attrfix_sensitivity/`. Rerunning a study with the default overwrites its frozen folder
  (git shows the change).
- **PCA centring:** the notebook centres definitional pairs at `a + b/2` (Z3). Our rebuilds keep it to
  match the paper; `ZHOU_CENTRE=midpoint` uses the correct midpoint (Z33).
- **Issue IDs:** Z (Zhou et al.) and O (Omrani Sabbaghi & Caliskan) in `docs/upstream-issues.md`;
  checks of our own pipeline in `docs/internal-checks.md`. Every decision is a row in
  `docs/decisions.md`.
- **Labels:** gold labels never come from a model. Word lists were built by rule; where an AI
  assistant suggested a label it is marked `claude_suggest_unverified`, and the author reviewed the
  lists (review copies are the `*_edited.csv` files).

## Studies

| Study | Prereg | Result (short) |
|---|---|---|
| C1: inanimates keep grammatical gender after mitigation | `c1-prereg.md` | survives, 16/16 (ES 84%, FR 1.09–1.13×) |
| Gender ValNorm: object gender ratings in vectors | `gvalnorm-prereg.md` | yes in both languages (β 0.18–0.34) |
| Zero point for Zhou's asymmetry | `zhou-zero-point-prereg.md` | ES inconclusive; FR borderline; FR with English words: asymmetry |
| Crime-noun probe | `crime-noun-probe-prereg.md` | ES male-leaning; FR borderline |
| Generic masculine (occupations) | `generic-masculine-prereg.md` | ES supported; FR inconclusive |
| Word-pair mechanism | `wordpair-mechanism-prereg.md` | not the dictionary; stereotype β 0.30 |
| Expanded feminine cues (87 ES / 86 FR) | `wordpair-cues-prereg.md` | intrusion ES 0.29, FR 0.19; mitigations cut ~⅓ (robust to the centring fix) |
| Person-noun baseline | `wordpair-persons-prereg.md` | persons none, occupations 0.29; masculine default 0.28 vs 0.51; CSLS 0.19 |
| Person-noun zero point (ES) | `persons-zero-point-prereg.md` | inconclusive, groups not distinguishable |
| Person-noun generic masculine (ES) | `persons-genmasc-prereg.md` | occupations supported, persons inconclusive (unstable with vocabulary) |

Reproductions without a prereg: `scripts/zhou_shift.py`, `zhou_hybrid.py`, `zhou_figures.py`,
`zhou_sec43_44.py`, `zhou_wordpair.py`, `repro_es.py`, `word_similarity_es.py`; the Shift identity is
written up in `docs/zhou-shift-identity.md`.

## Blind checks

Independent AI agents (Claude and Gemini) were given only the paper, the released code and the
vectors, first with a claim list, then open-ended; later rounds used autonomous replication runs.
What each found independently is noted in `docs/upstream-issues.md`. Their task files and reports
are in `blind-checks/` (the non-blind Gemini walkthrough `blind-checks/stress_test_zhou2019.ipynb`
reached a wrong conclusion in its §4; see `docs/wordpair-persons-prereg.md`).

## History

This repository was split out of the author's research monorepo (`cyrusae/gender`, directory
`embeddings/`) with `git subtree split`; `docs/HISTORY-MAP.md` maps monorepo commit hashes quoted in
the preregs to hashes here. Later work was copied over in batches.

---

# Original orientation: the two upstream repos (2026-11-08)

*Kept as written on 2026-11-08 except where marked; later findings supersede parts of it (see above
and `docs/upstream-issues.md`).*

Read from the cloned code and the notebooks' saved outputs (`external/`), not from
the papers. Paper claims still need checking against the PDFs.

## Embeddings (downloaded to the store, linked into each repo)

`scripts/fetch_embeddings.sh` puts everything in
`$EMB_STORE` (default `./store`; checksums in `SHA256SUMS`) and symlinks it where
each notebook looks.

| repo | vectors | other files |
|---|---|---|
| Zhou et al. 2019 | MUSE aligned fastText Wikipedia `wiki.multi.{en,es,fr,de}.vec` (300d, 200k words; notebook loads the first 50k) | MUSE dictionaries `en-es`, `es-en`, `es-fr` (+ `en-fr`, `fr-en`) |
| Omrani Sabbaghi & Caliskan 2022 | fastText Common Crawl `cc.{es,fr,de,it,pl,en}.300.vec` (2M words; notebook loads the first 1M) | none |

Not obtainable from the repos: Zhou's *derived* files (`debiased_aligned_*`, `hybrid_*`,
`*_offset_debiased_*`, the hard-debiased English `.bin`), `WEFAT_occupations.txt`,
`ES_gender_neutral_words.txt` and the `genbiasmt-master` occupation lists. The notebook writes
some of the derived files itself (`save_vec`); the others would have to be rebuilt.

## Zhou et al. 2019 (`Bias_in_Gendered_Languages/bias_emnlp19.ipynb`, 395 cells)

- One exploratory notebook, run top to bottom by hand; many cells commented out or repeated
  (two definitions of `modified_WEAT`).
- **Two directions.** A *semantic* gender direction from definitional pairs (`ES_definitional_pairs.json`
  etc.) and a *grammatical* one from inanimate feminine/masculine nouns (`feminine_nouns_es`,
  5,000 per gender; a classifier, then PCA/LDA variants, cells 63–125).
- **Bias test** (`modified_WEAT`, cells 215–232): occupation word *pairs* (feminine form,
  masculine form, e.g. *doctora/doctor*) scored against 8 male / 8 female definitional words
  (*hombre, niño, padre…* / *niña, mujer, madre…*); permutation p-value (`_weat_pval`; 1,000 random re-partitions, see Z10).
  Career/family WEAT in cells 243–250. **Only animate occupation words are tested**, which is
  the gap the PI noticed.

## Omrani Sabbaghi & Caliskan 2022 (`GG_Disentangling/main.ipynb`, 81 cells)

Clean, linear notebook; saved outputs are for Spanish.

1. Load 5,000 inanimate nouns per gender (`data/nouns/<lang>-{masc,fem}-v2.txt`); keep those in
   the vocabulary (Spanish: 5,381 m / 4,837 f), equalise, pair them up.
2. **Grammatical-gender direction** = coefficients of a LinearSVC trained on 3,000 + 3,000 nouns
   (train acc 0.99; next 6,000 nouns held out, 0.985).
3. **Iterative removal** (`num_iter`, set per language, e.g. French 27): project the direction out
   of **every word in the vocabulary**, refit the SVC, repeat. Tracked each round: SVC accuracy,
   WEATs (science/arts, career/family, a grammatical-gender WEAT), Gonen et al.'s same- vs
   different-gender noun similarity.
4. **Single-category GG-WEAT on inanimate nouns** (cells 46–58): for each of 1,000 masculine and
   1,000 feminine nouns, an SC-WEAT effect size against *man* words (*hombre, padre…*) vs
   *woman* words, before and after removal. Saved Spanish output:
   - masculine nouns: mean d **+0.84 → −0.24** (998/1000 move toward feminine);
   - feminine nouns: mean d **−0.90 → −0.29** (969/1000 move toward masculine).
5. ValNorm (valence norms) before/after, analogy test, plots.

## What this means for the PI's idea

- **The 2022 paper already runs a gender-association test on inanimate nouns** (step 4). So the
  gap is narrower than "nobody tested inanimate nouns": Zhou et al. didn't, Omrani Sabbaghi &
  Caliskan did, at least for Spanish in the notebook (the paper may report other languages; check).
- **The question their numbers leave open is the one closest to ours:** after removal, do
  grammatically masculine and feminine *things* still differ in social-gender association? In the
  saved Spanish run they end up close (−0.24 vs −0.29). Whether that difference is reliable,
  and whether it tracks the *human* gender ratings of the objects (Glasgow GEND), isn't tested.
- **Design issues to keep in mind (from reading the code, unverified against the paper):**
  - The 1,000 nouns scored in step 4 come from the 3,000 the direction was **trained on**; a
    held-out set (the next 3,000 exist) would be cleaner.
  - Removal is applied to **every** word, including the *man/woman* attribute words, so the
    attributes change too.
  - After removal both groups lean "feminine" (negative d). That could be a baseline shift in the
    attribute words rather than anything about the nouns; a within-pair difference (masculine
    minus feminine nouns) is more interpretable than the raw means.
  - The noun lists' gender labels and animacy filtering need checking against Wiktionary
    (our rule: gold labels never come from a model or unverified lists).
- **Natural link to the base-model study:** our Glasgow-norm adjective machinery and the
  German/Spanish lexicons would give an object-level social-gender rating to test against, and the
  2022 code already covers German.

## Not yet done (as of 2026-11-08; all since done)

- Reading both papers (the PI is doing this); checking the notebook numbers against the papers.
- Running anything. The Common Crawl vectors are ~4.2 GB each as text; loading 1M × 300 in
  float64 takes ~2.4 GB RAM per language, fine on the Mac one at a time.
