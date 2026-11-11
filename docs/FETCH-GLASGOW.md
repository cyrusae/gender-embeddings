# Glasgow Norms (not redistributed here)

`scripts/gvalnorm_en.py` and `scripts/wordpair_mechanism.py` read the Glasgow Norms
(Scott, Keitel, Becirspahic, Yao & Sereno 2019, Behavior Research Methods), file
`glasgow_norms_scott2019.csv`. This repo does not ship it (it fetches from the publisher instead; see below).

Put the file at `$EMB_STORE/glasgow/glasgow_norms_scott2019.csv` (default `store/glasgow/`; see
`scripts/paths.py`, `glasgow_csv()`).

Expected file: 814,379 bytes, sha256
`30d7776eed9219767f8a6aabdf95d7120cd050ddeab431acef13d435807bbc39`
(checksum of the copy the monorepo used, taken 2026-11-10 from
`/Users/watcher/GitHere/gender/data/raw/glasgow/glasgow_norms_scott2019.csv`).

Source: Electronic Supplementary Material 2 of the article (doi 10.3758/s13428-018-1099-3), CC BY 4.0
(as recorded in the monorepo's `docs/decisions.md`, 2026-10-08):

```sh
mkdir -p store/glasgow
curl -L -o store/glasgow/glasgow_norms_scott2019.csv \
  "https://static-content.springer.com/esm/art%3A10.3758%2Fs13428-018-1099-3/MediaObjects/13428_2018_1099_MOESM2_ESM.csv"
shasum -a 256 store/glasgow/glasgow_norms_scott2019.csv
```

Verified 2026-11-11: that URL returns a file whose sha256 matches the one above exactly. Being
CC BY 4.0, the file could also be shipped in this repo with attribution; it currently isn't.
