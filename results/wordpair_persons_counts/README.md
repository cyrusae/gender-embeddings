# Person-noun word-pair test as counts (exploratory, paper B, 2026-11-26)

`scripts/wordpair_persons_counts.py` (committed before running, 2905020). Frozen person-noun lists
(ES 107 person / 115 occupation / 102 identity; FR 40 / 41 / 7), frozen v1 cues, original space,
scoring as the pre-registered person-noun study, reported as shares of queries (cue × noun): the
masculine / feminine form retrieved first (after the cue word), in the top ten, or ranked above the
other form; neither form in the top 999. No intervals (descriptive).

Feminine cues, masculine form ranks above feminine / feminine above masculine:
- Spanish: persons 40% / 52%; occupations 74% / 24%.
- French: persons 57% / 40%; occupations 74% / 25%.
Masculine form retrieved first under feminine cues: ES persons 24%, occupations 53%; FR 33%, 55%.

**Second run (2026-11-26, 46c2a96):** adds plain translation (English noun alone, no cue) and every
condition without flagged nouns (`subset = no_flags`). Plain translation, masculine form ranks above
feminine: ES persons 75%, occupations 94%; FR 90%, 90%. Feminine cues without flagged nouns: ES persons
masculine wins 37% (feminine 54%), occupations 76% (23%); FR 52% (44%), 75% (24%).
