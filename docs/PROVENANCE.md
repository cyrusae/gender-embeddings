# Provenance of copied files

Files copied from the monorepo `/Users/watcher/GitHere/gender` (HEAD 39ef36a at copy time, 2026-11-10)
into this repo. Each line: new path, source, monorepo commit that last changed the source, notes.

- `docs/embeddings-handoff.md`: from monorepo `docs/design/embeddings-handoff.md`, last changed in
  monorepo commit 7f3f886 (2026-11-08, "PI: embeddings study handoff from planning chat").
- `docs/embeddings-lit-verification.md`: from monorepo `docs/design/embeddings-lit-verification.md`,
  last changed in monorepo commit feedfed (2026-11-08, verification of the handoff and Zhou
  inanimate review claims).
- `data/lexicon/es_nouns.csv`: built by the monorepo's `gbleed lexicon` from the Wiktionary (kaikki.org)
  Spanish dump, dump file mtime 2026-10-03 10:55:01 UTC, dump sha256
  7b23a5dc004a47b63edc2e79a34b246bbf59d1a3067a1843a5c554c0e252b97c; built 2026-10-06; 54,508 lemmas.
  Monorepo commit that last changed the lexicon code/metadata: 8f2a70e (2026-11-08). Copy sha256
  f2e3d1855fb7e6a534287fb8c11236c87d16c674d5d36483b824b1eca5a36b41. Derived from Wiktionary, CC BY-SA 4.0.
  The monorepo git-ignores `*_nouns.csv`; the copy here is an unversioned snapshot, so the regeneration
  path is the monorepo's `gbleed lexicon` (not included here).
- `data/lexicon/fr_nouns.csv`: built by `gbleed lexicon` from the kaikki.org French dump, dump file mtime
  2026-11-08 23:29:46 UTC, dump sha256 9053b1845fb3e045fa1fbe3f749122fa43e21b49bfa741cadd50255ae6ca0126;
  built 2026-11-09; 38,583 lemmas. Monorepo commit 8f2a70e (2026-11-08, "French Wiktionary lexicon").
  Copy sha256 74d827a66ccb2ad5b2a69df21c17c55e5ccc2b7a8bd4075d6e32e2c9f7d1615e. Derived from Wiktionary,
  CC BY-SA 4.0.
- `blind-checks/gemini/TASK.md`, `blind-checks/gemini/REPORT.md`: from `~/zhou-blind-check/` (the
  Gemini blind check of Zhou et al. claims). Only these two files copied (no vectors, no zhou_repo).
  Source commit: not in the monorepo (home-directory working files); copied as they were on 2026-11-10.
- `blind-checks/claude/TASK.md`, `blind-checks/claude/REPORT.md`: from `~/zhou-blind-check-claude/`,
  same rules and caveats as above.
- `scripts/_wordnet.py`: vendored from monorepo `src/gbleed/lexicon.py` (function `_wordnet`, lines
  222-233, monorepo commit 8f2a70e). See the file header.
