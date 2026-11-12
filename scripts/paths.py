"""Locations of data that lives outside the git repo.

STORE is the large-file store (embeddings, NLTK data, Glasgow norms). Override with the
EMB_STORE environment variable; the default is ./store relative to the working directory
(git-ignored). Layout mirrors the monorepo's external-drive store:
    $EMB_STORE/muse/            MUSE aligned vectors wiki.multi.{en,es,fr,de}.vec + dictionaries/
    $EMB_STORE/fasttext_cc/     fastText Common Crawl cc.{es,fr,de,it,pl,en}.300.vec
    $EMB_STORE/glasgow/         Glasgow Norms (not redistributable; see docs/FETCH-GLASGOW.md)
    $EMB_STORE/nltk_data/       NLTK WordNet corpus (downloaded on first use)
    $EMB_STORE/kaikki/          kaikki.org Wiktionary dumps (Spanish, French, English JSONL); only for
                                rebuilding candidate lists (wp_cues_*, wp_persons_*), not for scoring
    $EMB_STORE/person_adjectives/  person-adjective lists collected by Garg et al. 2018 (cue builder only)
"""

import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
STORE = Path(os.environ.get("EMB_STORE", "store"))
LEXICON = REPO / "data" / "lexicon"  # Wiktionary-derived {es,fr}_nouns.csv
STIMULI = REPO / "data" / "stimuli"  # phase2_final_v4.csv copied from the monorepo (see data/stimuli/README.md)


def muse_dir() -> Path:
    return STORE / "muse"


def fasttext_cc_dir() -> Path:
    return STORE / "fasttext_cc"


def glasgow_csv() -> Path:
    return STORE / "glasgow" / "glasgow_norms_scott2019.csv"


def nltk_dir() -> Path:
    return STORE / "nltk_data"


def kaikki_dir() -> Path:
    return STORE / "kaikki"


def person_adjectives_dir() -> Path:
    return STORE / "person_adjectives"
