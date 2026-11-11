"""Unchanged rerun of Omrani Sabbaghi & Caliskan's notebook, Spanish (writes results/repro_es/).

The 2026-11-08 run was done by hand with the same steps; this script records them so the folder
has a writer. It executes `main.ipynb` from external/GG_Disentangling (commit 725d813) exactly as
released (its default is lang = "es") in a scratch copy, so the clone's own Results/ folder keeps
the upstream originals, and saves the executed notebook with all outputs. results/repro_es/README.md
compares those outputs with the upstream saved ones.

    uv run --no-project --python 3.12 --with numpy,scipy,scikit-learn,pandas,openpyxl,statsmodels,\
matplotlib,nbconvert,ipykernel python scripts/repro_es.py
"""

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "external/GG_Disentangling"
OUT = ROOT / "results/repro_es"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    work = OUT / "work"
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(SRC, work, symlinks=True, ignore=shutil.ignore_patterns(".git", "__pycache__"))
    cells = json.loads((work / "main.ipynb").read_text())["cells"]
    assert any('lang = "es"' in "".join(c["source"]) for c in cells), "notebook default is no longer Spanish"
    subprocess.run(["jupyter", "nbconvert", "--to", "notebook", "--execute", "main.ipynb",
                    "--ExecutePreprocessor.timeout=-1", "--output", "executed.ipynb"],
                   cwd=work, check=True)  # fmt: skip
    shutil.copy(work / "executed.ipynb", OUT / "main_es_executed.ipynb")
    shutil.rmtree(work)
    print("=== REPRO es done", flush=True)


if __name__ == "__main__":
    main()
