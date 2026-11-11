# embeddings/ — embeddings study (static word embeddings; scoped rules, DRAFT)

A separate, small study: a partial replication and extension of Zhou et al. (2019), "Examining
Gender Bias in Languages with Grammatical Gender" (EMNLP-IJCNLP 2019; arXiv 1909.02224). The root
`CLAUDE.md` applies here except where this file overrides it. **Status: idea stage, nothing
adopted.** The overrides below are placeholders for the PI to confirm when a design is written.

## The question (PI, 2026-11-08)

Zhou et al. separate the grammatical-gender component from the semantic-gender component of
Spanish/French word embeddings and report bias-association tests (a WEAT derivative, after
Caliskan et al. 2017) for **animate** nouns only. Do **inanimate** nouns still carry a
social-gender association once grammatical gender is removed? Related: Omrani Sabbaghi & Caliskan
(2022) on disentangling grammatical gender signals; Bolukbasi et al. (2016).

## Where things are

- `external/Bias_in_Gendered_Languages/`: Zhou et al.'s code and seed lists, cloned from
  https://github.com/shaoxia57/Bias_in_Gendered_Languages (commit 6392702, 2019-09-05). Read-only
  reference; git-ignored. It has no licence file, so don't copy its lists into tracked files
  without checking with the PI; cite it instead.
- `external/GG_Disentangling/`: Omrani Sabbaghi & Caliskan (2022) code, cloned from
  https://github.com/shivaomrani/GG_Disentangling (commit 725d813, 2023-05-08). Notebook
  `main.ipynb` + `ValNorm.py`/`calcValNorm.py`/`utils.py`; noun lists and eval sets in `data/`;
  per-language results (es, fr, de, it, pl) in `Results/`. Needs FastText crawl vectors in
  `data/embeddings/` (not downloaded). Git-ignored; no licence file, same caution as above.
- Design docs, code and results for this study go in this folder (`docs/`, `results/`), not in
  the root `docs/design/` or `results/`.

## Logging what we find

Every problem found in the upstream code, data or papers goes into `docs/upstream-issues.md`
the moment it's found (numbered, with status and evidence), and every reproduction gets a
README in its `results/` folder.

## Rule notes (draft, for the PI)

- **Base-models-only rule:** not applicable as written (static embeddings, not LLMs). The point
  of the rule (no tuning-dependent model variants) carries over: use published embeddings,
  record exact versions and sources.
- **Gold labels:** noun genders still come from Wiktionary (`gbleed lexicon`), never from a model;
  animacy labels need a rule-based source too, decided in the design.
- **Pre-register before outcomes**, as everywhere else in the repo.

## Monorepo rules that still apply (copied 2026-11-10 from `gender/CLAUDE.md`)

This repo was split from the monorepo `/Users/watcher/GitHere/gender`; the rules below are the
ones that still apply here. Paths and commands from the monorepo (e.g. `gbleed lexicon`) refer to
the monorepo, which holds the Wiktionary-dump build code.

- **Gold linguistic labels never come from a language model**, including Claude. Genders come from
  Wiktionary (kaikki.org dumps). Hand-written labels must be marked unverified (`source = claude-unverified`).
- **Pre-register before outcomes.** Fix measurement choices on linguistic or grammatical grounds,
  not on a model's scores; if a check reveals a flaw, fix it on principle and say so.
- **Stimulus lists are versioned** (`data/*_vN.csv`). Do not edit a list that has results; sample a
  new version and rerun.
- **Held-out test sets are frozen before training and never trained on.** Training code must assert
  that no test item appears in its training data.
- **Drop anything that would need a manual check** rather than keep it and ask for review. Small,
  clean, automatically filtered sets beat large ones needing review. Hand-picked items are the exception
  and still get automatic checks.
- **Set changes need PI sign-off**: show counts and trade-offs before dropping items from any word set.
- **Stage by name**: never `git add -A` or `git commit -a` (the PI keeps uncommitted edits in this tree).
- **Explain each new method** in `docs/` as it is reached, and log choices that shape results
  (date, decision, why, alternatives; flag tentative ones).
- **Report findings that cut against what was built** (e.g. a noisy measure).
