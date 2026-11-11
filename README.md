# gender-embeddings: grammatical and social gender in static word embeddings

Standalone copy of the `embeddings/` study from the monorepo `gender` (research on whether
LLM and word-embedding representations of grammatical gender overlap with social gender).
This repo carries the static-embedding part only.

**Two papers** in preparation (drafts and plans are kept locally in a git-ignored `drafts/`):

1. **Zhou et al. (2019) re-analysis.** Zhou et al. separate grammatical-gender from semantic-gender
   components of Spanish/French MUSE embeddings and test animate nouns only. We re-run their
   pipeline, check their claims (see `docs/zhou-summary.md`,
   `docs/upstream-issues.md`), and test mitigation and reference-set choices.
2. **Inanimate nouns.** Does an inanimate noun still carry a social-gender association once its
   grammatical gender is removed? Gender ValNorm on inanimate nouns (`docs/gvalnorm-prereg.md`),
   C1 test-noun list (`docs/c1-prereg.md`), zero-point and reference sets
   (`docs/zhou-zero-point-prereg.md`), word-pair mechanism (`docs/wordpair-mechanism-prereg.md`),
   crime nouns (`docs/crime-noun-probe-prereg.md`), generic masculine (`docs/generic-masculine-prereg.md`).

Start with `docs/orientation.md`, then `docs/embeddings-handoff.md` and
`docs/embeddings-lit-verification.md`. Decisions are in `docs/decisions.md`.

## Layout

- `scripts/`: all analysis code (run from the repo root; see the `uv run` line in each docstring).
- `results/<name>/`: outputs of the scripts below; each folder may have its own `README.md`.
- `data/`: frozen, versioned stimulus and reference lists (`*_v1.csv`); `data/lexicon/` holds the
  Wiktionary-derived noun lexicons (see Licences).
- `docs/`: preregistrations, summaries, upstream-issue log; `docs/PROVENANCE.md` lists copied files.
- `blind-checks/`: task and report files of the blind checks of Zhou et al. (Gemini, Claude).
- `docs/HISTORY-MAP.md`: maps every monorepo commit hash to its hash here (the history was split
  with `git subtree`; the monorepo hashes quoted in the preregs are listed there).

## Fetching the external material

Nothing large is in the repo. Two inputs are needed.

**1. Upstream code (git-ignored, cloned by hand; no licence files upstream, so not redistributed):**

```sh
mkdir -p external && cd external
git clone https://github.com/shaoxia57/Bias_in_Gendered_Languages && git -C Bias_in_Gendered_Languages checkout 6392702   # Zhou et al. 2019
git clone https://github.com/shivaomrani/GG_Disentangling && git -C GG_Disentangling checkout 725d813                      # Omrani Sabbaghi & Caliskan 2022
cd ..
```

`external/debiaswe` (Bolukbasi et al. 2016 code) is also used by `zhou_hybrid.py` and
`create_stress_test_notebook.py` (only its `data/` word lists are read):

```sh
git -C external clone https://github.com/tolga-b/debiaswe && git -C external/debiaswe checkout 6bb03ee   # Bolukbasi et al. 2016
```

(6bb03ee2a0d7214339e513ca71cd0a99069dc29c, the commit of the monorepo's clone, checked 2026-11-11.)

**2. Pretrained embeddings** (large; into `$EMB_STORE`, default `./store`, git-ignored):

```sh
bash scripts/fetch_embeddings.sh      # MUSE wiki.multi.*.vec + dictionaries; fastText cc.*.300.vec (~25 GB unzipped)
```

It also creates the symlinks the upstream notebooks expect inside `external/`.

**3. Glasgow Norms** (not redistributed): see `docs/FETCH-GLASGOW.md`.

**4. NLTK WordNet** is downloaded on first use into `$EMB_STORE/nltk_data`.

Python: `uv run --no-project --python 3.12 --with <packages> python scripts/<name>.py`; the
packages for each script are in its docstring. `pyproject.toml` lists the union.

## Rerunning each results folder

| Results folder | Script (arguments) | Notes |
|---|---|---|
| `c1_es`, `c1_fr` | `scripts/c1_run.py [es\|fr]` | reads frozen `data/c1_nouns_<lang>_v1.csv`; the list itself is written by `scripts/c1_nouns.py` |
| `crime_probe_es`, `crime_probe_fr` | `scripts/crime_probe.py [es\|fr]` | |
| `generic_masculine` | `scripts/generic_masculine.py` | |
| `gg_dump_es`, `gg_dump_fr` | `scripts/gg_dump.py <lang> 14 28` | executes a notebook (needs nbconvert, ipykernel) |
| `gg_heldout_es` | `scripts/gg_heldout.py 14 28` | |
| `gg_minfix_es` | `scripts/gg_heldout.py --minfix 14 28` | "bugs fixed, method unchanged" run |
| `gvalnorm_en` | `scripts/gvalnorm_en.py` | Glasgow norms + MUSE/fastText English |
| `gvalnorm_es`, `gvalnorm_fr`: `gvalnorm_fits.csv`, `gvalnorm_nouns.csv`, `gvalnorm_verdicts.csv`, `info.json` | `scripts/gvalnorm_run.py [es\|fr]` | main study; run first (the others read `gvalnorm_nouns.csv`) |
| …`gvalnorm_omrani_{fits,verdicts}.csv`, `gvalnorm_omrani_info.json` | `scripts/gvalnorm_omrani.py es 14 28`, `scripts/gvalnorm_omrani.py fr 27` | Omrani erasure arm; needs `gg_dump_<lang>` first |
| …`gvalnorm_orth_{fits,cos,verdicts}.csv` | `scripts/gvalnorm_orth.py [es\|fr]` | Addendum B |
| …`gvalnorm_fixed_en_{fits,cos,verdicts}.csv` | `scripts/gvalnorm_orth.py [es\|fr] --fixed-en` | Addendum C (Hybrid arms scored with the original English attributes) |
| `label_audit_es` | `scripts/label_audit.py` | reads `data/stimuli/phase2_final_v4.csv` (copied from the monorepo) |
| `repro_es` | `scripts/repro_es.py` | upstream notebook executed unchanged; the original run was by hand, this script records the same steps |
| `wordpair_mechanism` | `scripts/wordpair_mechanism.py` | needs Glasgow |
| `zhou_construct.json` | `scripts/zhou_construct.py` | |
| `zhou_figures` | `scripts/zhou_figures.py` | |
| `zhou_hybrid_es` | `scripts/zhou_hybrid.py` | needs `external/debiaswe` |
| `zhou_sec43_44` | `scripts/zhou_sec43_44.py` | |
| `zhou_shift_es`, `zhou_shift_fr` | `scripts/zhou_shift.py` | |
| `zhou_wordpair` | `scripts/zhou_wordpair.py` | |
| `zhou_zero_point_es`, `zhou_zero_point_fr` | `scripts/zhou_zero_point.py [es\|fr]` | |

Frozen lists are rebuilt by `scripts/zero_ref_lists.py` (candidates, v0) and
`scripts/zero_ref_freeze.py` (frozen, v1); both read `data/lexicon/`.

## Unresolved (missing from this repo)

- Lexicon regeneration needs the monorepo's `gbleed lexicon` (Wiktionary dumps), which is not in this repo.

## Licences

- **Code:** MIT (`LICENSE`).
- **Wiktionary-derived data** (`data/lexicon/*_nouns.csv`, `data/stimuli/phase2_final_v4.csv`): CC BY-SA 4.0 (Wiktionary, via kaikki.org).
- **Glasgow Norms:** CC BY 4.0 (publisher's supplementary file); fetched, not shipped (`docs/FETCH-GLASGOW.md`).
- **Upstream code and embeddings** (Zhou et al.; Omrani Sabbaghi & Caliskan; MUSE; fastText): not
  redistributed; cite their papers and use their own terms.

## Monorepo

The research is coordinated in the monorepo `/Users/watcher/GitHere/gender` (other studies: a
base-model gender-direction study, a character study). Rules that apply here are repeated in
`CLAUDE.md`. Quoted monorepo commit hashes map to this repo via `docs/HISTORY-MAP.md`.

## Cite

See `CITATION.cff` (authors and title are placeholders until the PI fills them in).
