"""Extract Misersky et al. (2014) role-noun norms (Behav Res 46:841-871, Appendix B Table 3) from the PI's
licensed PDF copy (not redistributed; only the derived table is kept, on the data drive).

Per role noun (English plural name, as in the table) and language: mean estimated proportion of women
(0 = all men, 1 = all women), N, SD. Participants saw grammatically gendered role nouns in both masculine
and feminine plural forms, and unmarked ones with "women and men" added (paper, Method), so the ratings
are not of generic-masculine forms. Wrapped names are rejoined; the table ends at 'Zoologists'. Words are placed in columns by their x position under the language
headers (pdfplumber); a row whose redirect cells ('"Bookkeepers"' = see that row) sit on the line above
is merged with it; redirects are resolved to the named row.
Output: /Volumes/Lexar/gbleed/shared/misersky2014/norms.csv (english + m/n/sd/see per language).

    uv run --no-project --python 3.12 --with pdfplumber,pandas python scripts/misersky_extract.py
"""

import collections
import re
from pathlib import Path

import pandas as pd
import pdfplumber

PDF = Path("/Volumes/Lexar/gbleed/shared/Misersky et al.pdf")
OUT = Path("/Volumes/Lexar/gbleed/shared/misersky2014")
LANGS = ["Czech", "English", "French", "German", "Italian", "Norwegian", "Slovak"]
NUM = re.compile(r"^(\.?\d*\.?\d+)\s+(\d+)\s+\(\s*(\.?\d*\.?\d*)\s*\)$")


def lines():
    pdf = pdfplumber.open(PDF)
    for pn, p in enumerate(pdf.pages):
        if not re.search(r"Table ?3", (p.extract_text() or "")[:400]):
            continue
        W = p.extract_words(x_tolerance=1.5)
        t0 = min(w["top"] for w in W if w["text"] == "Czech")  # header line (the page may also hold references)
        H = [w for w in W if w["text"] in LANGS and abs(w["top"] - t0) < 3]
        xs = [next(w["x0"] for w in H if w["text"] == lang) for lang in LANGS]
        htop = t0
        L = collections.defaultdict(list)
        for w in W:
            if w["top"] > htop + 12 and "Behav" not in w["text"]:
                L[round(w["top"] / 3)].append(w)
        for k in sorted(L):
            ws = sorted(L[k], key=lambda w: w["x0"])
            name = " ".join(w["text"] for w in ws if w["x1"] < xs[0] - 2)
            cols = {lang: [] for lang in LANGS}
            for w in ws:
                if w["x1"] >= xs[0] - 2:
                    j = max([i for i in range(7) if w["x0"] >= xs[i] - 14] or [0])
                    cols[LANGS[j]].append(w["text"])
            yield pn, name, {lang: " ".join(v) for lang, v in cols.items()}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows, pend = [], None
    for _, name, c in lines():
        if not name:
            if all(v in ("M N (SD)", "") for v in c.values()):
                continue
            pend = c  # redirect cells printed on the line above their row
            continue
        if not any(c.values()):
            if rows:  # wrapped role-noun name ("Members of the armed" / "forces")
                rows[-1] = (rows[-1][0] + " " + name, rows[-1][1])
            continue
        if pend:
            c = {k: c[k] or pend[k] for k in c}
            pend = None
        rows.append((name, c))
        if name == "Zoologists":  # last row; references follow on the same page
            break
    recs = []
    for name, c in rows:
        r = {"english": name}
        for lang in LANGS:
            k = lang[:2].lower()
            v = c[lang].strip()
            m = NUM.match(v)
            r[f"{k}_m"], r[f"{k}_n"], r[f"{k}_sd"], r[f"{k}_see"] = (float(m.group(1)), int(m.group(2)), float(m.group(3)) if m.group(3).strip(".") else None, "") if m else (None, None, None, v.strip("“”\"") if v not in ("N/A", "") else v)  # fmt: skip
        recs.append(r)
    D = pd.DataFrame(recs)
    by = D.drop_duplicates("english").set_index("english")
    for lang in LANGS:
        k = lang[:2].lower()
        for j, s in D[f"{k}_see"].items():
            if s and s != "N/A" and s in by.index:
                for c in ("m", "n", "sd"):
                    D.loc[j, f"{k}_{c}"] = by.loc[s, f"{k}_{c}"]
    D.to_csv(OUT / "norms.csv", index=False)
    print("rows", len(D), "| English rated", D.en_m.notna().sum(), "| French rated", D.fr_m.notna().sum())


if __name__ == "__main__":
    main()
