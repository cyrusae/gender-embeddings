"""WordNet access, vendored from the monorepo's src/gbleed/lexicon.py (function `_wordnet`,
monorepo commit 8f2a70e, lines 222-233). Only change: NLTK_DIR now comes from paths.nltk_dir()
instead of the monorepo-relative constant Path("data/raw/nltk_data"). Dependency: nltk (plus the
WordNet corpus, downloaded on first use from NLTK's server).
"""

import nltk

from paths import nltk_dir


def _wordnet():
    NLTK_DIR = nltk_dir()
    nltk.data.path.insert(0, str(NLTK_DIR))
    try:
        from nltk.corpus import wordnet as wn

        wn.synsets("test")
    except LookupError:
        nltk.download("wordnet", download_dir=str(NLTK_DIR), quiet=True)
        from nltk.corpus import wordnet as wn
    return wn
