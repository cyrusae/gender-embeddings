# Word-pair plurals study as counts (exploratory, paper B, 2026-11-26)

`scripts/wordpair_plurals_counts.py` (committed before running, 46c2a96). Same occupations (ES 43, FR 16),
cues, queries, 200k vocabulary and scoring as `wordpair_plurals.py`. For each arm and cue type: share of
queries in which each of the four forms is the first word retrieved (`*_first`) and the highest-ranked of
the four (`*_best_of_four`); `none_of_four` = none in the top 999. No intervals (descriptive).

Highest-ranked of the four forms, Spanish:
- singular feminine cues: masculine singular 68%, feminine singular 25% (plurals ≤ 4%);
- plural feminine cues: masculine plural 75%, feminine plural 19%;
- masculine cues: the matching masculine form 90% (singular) / 95% (plural).
French (16 occupations) is similar: singular feminine 57% vs 31%, plural feminine 72% vs 27%.
