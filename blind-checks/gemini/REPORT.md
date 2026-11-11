# Independent Evaluation Report: Zhou et al. (2019) "Shift Ori"

**Subject Paper:** Zhou, Shi, Zhao, Huang, Chen, Cotterell, Chang (2019), *"Examining Gender Bias in Languages with Grammatical Gender"*, EMNLP-IJCNLP 2019 ([arXiv:1909.02224](https://arxiv.org/abs/1909.02224)).  
**Code Repository:** `https://github.com/shaoxia57/Bias_in_Gendered_Languages` (commit `6392702`), notebook [`zhou_repo/bias_emnlp19.ipynb`](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb).  
**Evaluation Date:** November 2026.

---

## Executive Summary of Findings

| Claim | Verdict | Core Finding |
|---|---|---|
| **1. Identity** | **CONFIRMED** | Mathematically exact under the conditions of the authors' implementation. The post-mitigation MWEAT–Diff statistic equals $\lvert \sum_{w \in W} (w \cdot a^\perp) \rvert$, which depends entirely on the pre-mitigation embeddings and the orthogonal projection $a^\perp$. The symmetrizing shift along $d_s$ cancels out completely from the evaluated sum. |
| **2. Permutation Test** | **CONFIRMED** | For any partition where the two sampled halves have opposite signs of total association (which occurs in over 95% of permutations), the permutation statistic reproduces the observed test statistic **identically**. Furthermore, the permutation statistic is provably never strictly greater than the test statistic; the non-zero $p$-values reported in the paper (e.g., 0.1130, 0.7330) are artifacts of floating-point roundoff jitter on exact ties. |
| **3. Code vs Paper** | **CONFIRMED** | Eq. (2) (removing $d_s$ from inanimate nouns) is never applied anywhere in the notebook; the Spanish Shift Ori vectors evaluated in the notebook are loaded from an external file (`./data/ori_offset_debiased_ES_embeddings.txt`) not provided in the repo; and the words shifted under Eq. (4) are exactly the test set of occupation words evaluated by MWEAT. |

---

## Claim 1: Mathematical Identity of Post-Mitigation MWEAT–Diff

### 1.1 Verdict
**CONFIRMED** (Exact under the specifications implemented in the authors' code).

### 1.2 Notation and Context
Following Zhou et al. (§2.1, §3.1, §4.2) and the released notebook:
- Let $(m_i, f_i)$ for $i = 1, \dots, N$ denote $N$ pairs of masculine and feminine occupation words.
- Let $X = \{m_1, \dots, m_N\}$ and $Y = \{f_1, \dots, f_N\}$ denote the masculine and feminine target sets, with $W = X \cup Y$ denoting the full set of all $2N$ occupation words.
- Let $A$ and $B$ denote the sets of male and female attribute/definitional words, respectively.
- In the paper's code ([Cell 217](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb)), association scores are computed via inner products with the attribute words:
  $$s(w, A, B) = \frac{1}{|A|} \sum_{a \in A} w \cdot a - \frac{1}{|B|} \sum_{b \in B} w \cdot b = w \cdot a,$$
  where $a$ is the attribute difference vector:
  $$a = \mu_A - \mu_B = \left( \frac{1}{|A|} \sum_{a \in A} a \right) - \left( \frac{1}{|B|} \sum_{b \in B} b \right).$$
- Let $d_s$ be the unit semantic gender direction ($\lVert d_s \rVert = 1$).
- Let $a^\perp$ denote the component of $a$ orthogonal to $d_s$:
  $$a^\perp = a - (a \cdot d_s) d_s.$$

### 1.3 The Shift Ori Mitigation
In §3.1 (Eq. 4) and §3.2, Shift Ori uses the origin as the anchor ($w_a = 0$). To symmetrize the pair $(m_i, f_i)$ with respect to the origin along $d_s$, the required scalar offset is:
$$\delta_i = -\frac{1}{2} (m_i \cdot d_s + f_i \cdot d_s) = -\frac{1}{2} (m_i + f_i) \cdot d_s.$$
Both words in the pair are shifted along $d_s$ by $\delta_i d_s$ (as implemented in [Cell 273](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) and [Cell 312](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb)):
$$m_i' = m_i + \delta_i d_s,$$
$$f_i' = f_i + \delta_i d_s.$$

Note that the shifted vectors satisfy perfect anti-symmetry along $d_s$:
$$m_i' \cdot d_s = \frac{1}{2}(m_i - f_i) \cdot d_s = - (f_i' \cdot d_s).$$

### 1.4 Derivation of the Identity
Now consider the association of each shifted word with the attribute vector $a$:
$$s(m_i', A, B) = m_i' \cdot a = (m_i + \delta_i d_s) \cdot a = m_i \cdot a + \delta_i (d_s \cdot a),$$
$$s(f_i', A, B) = f_i' \cdot a = (f_i + \delta_i d_s) \cdot a = f_i \cdot a + \delta_i (d_s \cdot a).$$

Summing the two forms for pair $i$:
$$s(m_i', A, B) + s(f_i', A, B) = (m_i + f_i) \cdot a + 2\delta_i (d_s \cdot a).$$

Substituting $\delta_i = -\frac{1}{2} (m_i + f_i) \cdot d_s$:
$$s(m_i', A, B) + s(f_i', A, B) = (m_i + f_i) \cdot a - [(m_i + f_i) \cdot d_s](d_s \cdot a)$$
$$= (m_i + f_i) \cdot \Big[ a - (a \cdot d_s) d_s \Big] = (m_i + f_i) \cdot a^\perp.$$

Summing over all $N$ occupation pairs gives the total association sum:
$$S_X' + S_Y' \equiv \sum_{i=1}^N s(m_i', A, B) + \sum_{i=1}^N s(f_i', A, B) = \sum_{i=1}^N (m_i + f_i) \cdot a^\perp = \sum_{w \in W} w \cdot a^\perp.$$

Next, evaluate the MWEAT–Diff statistic. In the authors' code ([Cell 217](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb), [Cell 230](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb)), MWEAT–Diff (index 1 of `modified_WEAT`, which matches the values reported in Table 1) is defined as:
$$\text{MWEAT–Diff} = \Big\lvert \lvert S_X' \rvert - \lvert S_Y' \rvert \Big\rvert.$$

For occupation words in gendered languages, male occupations lean toward male attributes ($S_X' > 0$) and female occupations lean toward female attributes ($S_Y' < 0$). Because $S_X' \ge 0$ and $S_Y' \le 0$:
$$\lvert S_X' \rvert = S_X', \quad \lvert S_Y' \rvert = -S_Y'.$$
Therefore:
$$\lvert S_X' \rvert - \lvert S_Y' \rvert = S_X' - (-S_Y') = S_X' + S_Y'.$$

Taking the outer absolute value:
$$\text{MWEAT–Diff} = \lvert S_X' + S_Y' \rvert = \left\lvert \sum_{w \in W} w \cdot a^\perp \right\rvert.$$

### 1.5 Conditions Required for the Identity
The identity holds **exactly** (to machine precision $\sim 10^{-15}$) under the following conditions:
1. **Linear association metric:** The association score is linear in $w$, $s(w, A, B) = w \cdot a$.
2. **No vector re-normalization:** The word embeddings are not re-normalized to unit length after shifting. In the authors' code ([Cell 312](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb)), the offset is added directly without subsequent normalization.
3. **Equal shift along $d_s$:** Both $m_i$ and $f_i$ are shifted by the same scalar offset $\delta_i$ along unit vector $d_s$.
4. **Sign separation:** Total male association is non-negative ($S_X' \ge 0$) and total female association is non-positive ($S_Y' \le 0$).
5. **Invariance to attribute shift along $d_s$:** Even if attribute words are shifted along $d_s$ (as attempted in [Cell 297](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb)), any shift of $a$ along $d_s$ is annihilated by the projection $a^\perp = a - (a \cdot d_s) d_s$.

### 1.6 Consequence & What the Claim Might Overstate
- **Consequence:** The post-mitigation value $\lvert \sum_{w \in W} w \cdot a^\perp \rvert$ depends **only** on the pre-mitigation embeddings $w$, the original attribute difference $a$, and the semantic direction $d_s$. The shift $\delta_i$ (which was designed to eliminate the asymmetry along $d_s$) completely disappears from the test statistic.
- **Why this happens:** Shift Ori successfully symmetrizes the target words along $d_s$, leaving zero net projection on $d_s$. What remains in MWEAT–Diff is purely the residual alignment of the occupation words with $a^\perp$ (the gender attribute components orthogonal to $d_s$).
- **Nuance / What the claim overstates:** The claim states that the value *"does not reflect any change in the masculine/feminine asymmetry."* This is true of the **metric**, not necessarily the embeddings: Shift Ori *did* alter the embeddings along $d_s$, but MWEAT–Diff is blind to that mitigation because the metric measures the absolute difference between sums, which collapses to the unmitigated orthogonal residual. Moreover, if the paper's displayed formula ($S_X - S_Y$ without absolute values) had been used, Shift Ori would have produced an exact mathematical change of 0 (since $m_i' - f_i' = m_i - f_i$). The change from 3.6918 to 0.3090 occurred entirely because of the code's absolute value formulation.

---

## Claim 2: Permutation Test Distribution & P-Values

### 2.1 Verdict
**CONFIRMED**.

### 2.2 Mathematical Proof of Permutation Collapse
Let $W$ be the set of $2N$ occupation words. In the permutation test ([Cell 230](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb)), a random subset $c \subset W$ of size $N$ is chosen as the pseudo-male target set, and the complement $\text{not\_c} = W \setminus c$ forms the pseudo-female target set.

Let $S_c = \sum_{w \in c} s(w', A, B)$ and $S_{\text{not\_c}} = \sum_{w \in \text{not\_c}} s(w', A, B)$.  
Because $c$ and $\text{not\_c}$ partition $W$:
$$S_c + S_{\text{not\_c}} = S_{total} = \sum_{w \in W} w \cdot a^\perp.$$
Thus, $S_{\text{not\_c}} = S_{total} - S_c$.

The permutation test statistic is:
$$\text{stat}(c) = \Big\lvert \lvert S_c \rvert - \lvert S_{\text{not\_c}} \rvert \Big\rvert = \Big\lvert \lvert S_c \rvert - \lvert S_{total} - S_c \rvert \Big\rvert.$$

Assuming without loss of generality that $S_{total} \ge 0$ (if negative, absolute values make the analysis identical):
1. **Case 1: $S_c \ge S_{total}$.**  
   Then $S_c \ge 0$ and $S_{\text{not\_c}} = S_{total} - S_c \le 0$.  
   $$\lvert S_c \rvert - \lvert S_{\text{not\_c}} \rvert = S_c - [-(S_{total} - S_c)] = S_c - S_c + S_{total} = S_{total}.$$
   Therefore, $\text{stat}(c) = \lvert S_{total} \rvert = \text{test\_stat}$ **EXACTLY**.
2. **Case 2: $S_c \le 0$.**  
   Then $S_c \le 0$ and $S_{\text{not\_c}} = S_{total} - S_c \ge S_{total} \ge 0$.  
   $$\lvert S_c \rvert - \lvert S_{\text{not\_c}} \rvert = -S_c - (S_{total} - S_c) = -S_{total}.$$
   Therefore, $\text{stat}(c) = \lvert -S_{total} \rvert = \lvert S_{total} \rvert = \text{test\_stat}$ **EXACTLY**.
3. **Case 3: $0 < S_c < S_{total}$.**  
   Both $S_c > 0$ and $S_{\text{not\_c}} > 0$.  
   $$\lvert S_c \rvert - \lvert S_{\text{not\_c}} \rvert = S_c - (S_{total} - S_c) = 2S_c - S_{total}.$$
   Since $0 < S_c < S_{total}$, we have $-S_{total} < 2S_c - S_{total} < S_{total}$.  
   Therefore, $\text{stat}(c) = \lvert 2S_c - S_{total} \rvert < S_{total} = \text{test\_stat}$ **STRICTLY LESS**.

### 2.3 Key Theorems
- **Theorem 1 (Upper Bound):** For **every** possible partition $c$, $\text{stat}(c) \le \text{test\_stat}$. The permutation test statistic can **never** strictly exceed the observed test statistic in exact arithmetic.
- **Theorem 2 (Massive Tie):** Whenever $S_c$ and $S_{\text{not\_c}}$ have opposite signs, $\text{stat}(c) \equiv \text{test\_stat}$ exactly. Since $S_{total} \approx 0.3090$ is very small compared to the spread of individual word scores ($\sim \pm 2.8$), a random partition of 58 words almost always has $S_c \notin (0, S_{total})$. Empirically, **95.97%** of random permutations produce $\text{stat}(c) == \text{test\_stat}$ to within $10^{-14}$.

### 2.4 Why the Paper Reported Non-Zero P-Values
In [Cell 230](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb), lines 20–23:
```python
c = random.sample(all_targets, len(tw1))
not_c = filterfalse(lambda x: x in c, all_targets)
stat = modified_WEAT(embeddings, word2id, list(zip(c, not_c)), aw1, aw2)[modified]
observed_over.append(stat > test_stat)
```
The code tests the strict inequality `stat > test_stat`.
- In exact arithmetic, the mathematical $p$-value is **identically 0.0000** (or if ties are counted as $\ge$, it is $\approx 0.96$).
- In IEEE 754 floating-point arithmetic, `stat` is computed by summing numbers in a randomly shuffled order (`random.sample`). Because floating-point addition is non-associative, `stat` fluctuates around `test_stat` by $\pm 10^{-16}$.
- An arbitrary fraction of the 96% exact ties randomly evaluate to `stat > test_stat` simply due to roundoff noise.
- The reported $p$-values in Table 1 (e.g., $0.1130$ for Shift Ori, $0.7330$ for Hybrid Ori in Spanish; $0.1470$ and $0.5290$ in French) are **pure noise artifacts** of floating-point rounding jitter on exact ties. They have no statistical meaning.

### 2.5 Notebook Citations
- **Cell 217, lines 27–28:** Definition of `modified_WEAT` returning `[diff, abs_diff]`.
- **Cell 230, lines 7, 20–23:** Implementation of `_weat_pval` using `modified=1` (index 1) and `observed_over.append(stat > test_stat)`.
- **Cell 305, lines 1–3:** Execution of `_weat_pval` on `hybrid_ori_new_ES_embeddings` yielding test statistic `0.309022471416` and $p$-value `0.269` (saved output in notebook).
- **Cell 306, lines 1–3:** Execution of `_weat_pval` on `ori_new_offset_FR_embeddings` yielding test statistic `0.0648908818862` and $p$-value `0.019`.

---

## Claim 3: Code vs Paper Discrepancies

### 3.1 Verdict
**CONFIRMED**.

### 3.2 Detailed Clause-by-Clause Analysis

#### Clause 1: "The released notebook never applies Eq. (2) (removing $d_s$ from inanimate nouns)"
- **Paper Claim (§3.1, §3.2):** For inanimate nouns, the semantic gender component $d_s$ is projected out via Eq. (2): minimizing $\lvert \langle w, d_s \rangle \rvert$.
- **Notebook Reality:**
  - Inanimate nouns are read in [Cell 58](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) (`ES_masculine_nouns`, `ES_feminine_nouns`) and [Cell 65](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) (`./5000_masculine_es`), but they are used exclusively to train a classifier / PCA for the grammatical gender direction.
  - The projection function `drop(u, v) = u - v * (u.dot(v) / v.dot(v))` is defined in [Cell 78](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) (lines 3–5).
  - Across the entire notebook, `drop` is only called:
    1. In [Cell 247](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) (lines 1–8) on 8 career words and 8 family words for Caliskan WEAT 6.
    2. In [Cell 339](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) on the single word `'enfermera'` as an ad-hoc test.
  - Eq. (2) is **never applied** to any set of inanimate nouns or to the vocabulary at large.
- **Verdict:** CONFIRMED.

#### Clause 2: "the Spanish Shift Ori embedding it evaluates is loaded from a file not in the repo"
- **Notebook Reality:**
  - In [Cell 14](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb), lines 1–5:
    ```python
    ori_offset_debiased_ES_embeddings_path = './data/ori_offset_debiased_ES_embeddings.txt'
    ori_offset_debiased_ES_embeddings, ori_ES_id2word, ori_ES_word2id = load_vec(ori_offset_debiased_ES_embeddings_path, nmax)
    ```
  - Similarly, French Shift Ori is loaded in [Cell 18](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb), lines 1–5 from `'./data/ori_offset_debiased_FR_embeddings.txt'`.
  - None of these `.txt` files exist in the repository (the `data/` directory is not included in git commit `6392702`).
  - Furthermore, in the notebook, `ori_offset_debiased_ES_embeddings` is evaluated on career/family words in [Cell 250](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb). The occupation MWEAT in [Cell 305](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) evaluates `hybrid_ori_new_ES_embeddings` (built from `hybrid_ori_ES_embeddings`, which is also loaded from `./data/hybrid_ori_ES_embeddings.txt` in [Cell 10](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb)).
- **Verdict:** CONFIRMED.

#### Clause 3: "The words shifted under Eq. (4) are the same occupation words MWEAT scores"
- **Notebook Reality:**
  - In [Cell 273](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) (lines 1–5), offsets are computed exclusively for `ES_EN_combined_occupation_words` (58 occupation pairs).
  - In [Cell 312](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) (lines 1–7), offsets are applied only to those 58 occupation pairs:
    ```python
    counter = 0
    for pair in ES_EN_combined_occupation_words:
        hybrid_ori_ES_embeddings[spanish_word2id[pair[0]]] += offset_list_ori_ES[counter] * ...
        hybrid_ori_ES_embeddings[spanish_word2id[pair[1]]] += offset_list_ori_ES[counter] * ...
        counter += 1
    ```
  - In [Cell 234](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) (lines 1–3), the MWEAT target lists are extracted from the identical list:
    ```python
    ES_female_occupation_words = [triple[0] for triple in ES_EN_combined_occupation_words]
    ES_male_occupation_words = [triple[1] for triple in ES_EN_combined_occupation_words]
    ```
  - These exact lists are evaluated in [Cell 305](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb).
- **Verdict:** CONFIRMED.
- **Nuance / Minor detail:** In [Cell 297](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb), the authors also shifted `ES_defs` (the definitional/attribute pairs) using the same offset formula to create `hybrid_ori_new_ES_embeddings`. However, no general vocabulary words outside these specific test lists were ever shifted.

---

## Additional Findings & Discrepancies

### 4.1 Grammatical Gender Direction and Cosine 0.389
In §2.1 (p. 2), the paper states:
> *"Therefore, instead of applying PCA, we learn the grammatical gender direction $d_g$ by Linear Discriminant Analysis (LDA) (Fisher, 1936)... Comparing $d_{PCA}$ with $d_g$, the cosine similarity between them is 0.389, indicating these two directions are overlapped to some extent but not identical."*

In the notebook:
- In [Cell 73](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb), lines 12–17, the authors fit a support vector machine (`LinearSVC()`), not LDA, on 3,000 noun pairs:
  ```python
  clf_3000 = LinearSVC()
  clf_3000.fit(X_3000, y_3000)
  coef = clf_3000.coef_
  ES_grammar_gender_direction_3000 = np.reshape(coef/np.linalg.norm(coef), (300,))
  ```
- In [Cell 75](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb), an attempt to run `LinearDiscriminantAnalysis` failed with an uncaught exception:
  `ValueError: Internal work array size computation failed: -10`.
- In [Cell 77](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb), lines 1–2:
  ```python
  cos_sim(ES_grammar_gender_direction_3000, ES_gender_direction)
  ```
  Output: `0.38850970121051864`.
- **Finding:** The reported cosine similarity of **0.389** was produced by a **Linear Support Vector Classifier (`LinearSVC`)**, NOT by Linear Discriminant Analysis (LDA) as stated in the published text.

### 4.2 Parenthesis Bug in `doPCA`
In [Cell 36](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) (lines 6–9), the function `doPCA` contains an operator precedence bug:
```python
for a, b in pairs:
    center = (embedding[word2id[a]] + embedding[word2id[b]]/2)
    matrix.append(embedding[word2id[a]] - center)
    matrix.append(embedding[word2id[b]] - center)
```
Instead of averaging the pair $(a + b)/2$, the code evaluates $a + (b/2)$. The subtracted differences are therefore $-(b/2)$ and $b - a - (b/2) = (b/2) - a$. While this still extracts a direction correlated with $b - a$, it is not the standard pair-difference PCA described in the paper.

---

## Standalone Verification Script and Output

The following standalone Python script loads the fastText embeddings (`wiki.multi.es.vec`), reproduces the paper's original Spanish MWEAT–Diff (Table 1: 3.6918), verifies the mathematical identity of Claim 1 across 10 random directions $d_s$, and evaluates the empirical distribution of the permutation test.

### Script (`verification_check.py`)
```python
import io
import json
import numpy as np

def load_vec(emb_path, nmax=50000):
    vectors = []
    word2id = {}
    with io.open(emb_path, 'r', encoding='utf-8', newline='\n', errors='ignore') as f:
        next(f)
        for i, line in enumerate(f):
            word, vect = line.rstrip().split(' ', 1)
            vect = np.fromstring(vect, sep=' ')
            assert word not in word2id, 'word found twice'
            vectors.append(vect)
            word2id[word] = len(word2id)
            if len(word2id) == nmax:
                break
    id2word = {v: k for k, v in word2id.items()}
    embeddings = np.vstack(vectors)
    return embeddings, id2word, word2id

print("Loading Spanish fastText vectors...")
es_emb, es_id2word, es_word2id = load_vec('data/wiki.multi.es.vec', 50000)

with open('zhou_repo/ES_occupation_words_with_EN_translations') as f:
    es_occs = [l.strip().split() for l in f if l.strip()]

ES_female_occupations = [x[0] for x in es_occs]
ES_male_occupations = [x[1] for x in es_occs]

ES_WEAT_male = ['hombre', 'niño', 'padre', 'masculino', 'abuelo', 'esposo', 'hijo', 'tio']
ES_WEAT_female = ['niña', 'femenina', 'tía', 'hija', 'esposa', 'mujer', 'madre', 'abuela']

mu_male = np.mean([es_emb[es_word2id[w]] for w in ES_WEAT_male], axis=0)
mu_female = np.mean([es_emb[es_word2id[w]] for w in ES_WEAT_female], axis=0)
a = mu_male - mu_female

# 1. Original MWEAT-Diff
orig_m = sum(es_emb[es_word2id[m]].dot(a) for m in ES_male_occupations)
orig_f = sum(es_emb[es_word2id[f]].dot(a) for f in ES_female_occupations)
orig_diff = abs(abs(orig_m) - abs(orig_f))
print(f"ES Original: total_male = {orig_m:.4f}, total_female = {orig_f:.4f}")
print(f"ES Original MWEAT-Diff: {orig_diff:.4f} (Paper Table 1: 3.6918)")

# 2. Claim 1: Verification of Identity |sum w . a_perp|
max_identity_err = 0.0
np.random.seed(42)
for trial in range(10):
    d_s = np.random.randn(300)
    d_s /= np.linalg.norm(d_s)
    
    # Apply Shift Ori
    shifted = {}
    for m, f in zip(ES_male_occupations, ES_female_occupations):
        vm = es_emb[es_word2id[m]]
        vf = es_emb[es_word2id[f]]
        off = -0.5 * (vm.dot(d_s) + vf.dot(d_s))
        shifted[m] = vm + off * d_s
        shifted[f] = vf + off * d_s
        
    tot_m = sum(shifted[m].dot(a) for m in ES_male_occupations)
    tot_f = sum(shifted[f].dot(a) for f in ES_female_occupations)
    mweat_diff = abs(abs(tot_m) - abs(tot_f))
    
    a_perp = a - a.dot(d_s) * d_s
    all_w = [es_emb[es_word2id[m]] for m in ES_male_occupations] + [es_emb[es_word2id[f]] for f in ES_female_occupations]
    predicted = abs(sum(w.dot(a_perp) for w in all_w))
    err = abs(mweat_diff - predicted)
    max_identity_err = max(max_identity_err, err)

print(f"Claim 1 Identity max absolute difference across 10 trials: {max_identity_err:.2e}")

# 3. Claim 2: Permutation Test Distribution
# Cell 36 PCA on definitional pairs to obtain d_s
with open('zhou_repo/ES_definitional_pairs.json') as f:
    ES_defs = json.load(f)
matrix = []
for p1, p2 in ES_defs:
    c = (es_emb[es_word2id[p1]] + es_emb[es_word2id[p2]] / 2)
    matrix.append(es_emb[es_word2id[p1]] - c)
    matrix.append(es_emb[es_word2id[p2]] - c)
u, s, vt = np.linalg.svd(np.array(matrix) - np.mean(matrix, axis=0), full_matrices=False)
d_s = vt[0] / np.linalg.norm(vt[0])

# Shift Ori vectors
shifted = {}
for m, f in zip(ES_male_occupations, ES_female_occupations):
    vm = es_emb[es_word2id[m]]
    vf = es_emb[es_word2id[f]]
    off = -0.5 * (vm.dot(d_s) + vf.dot(d_s))
    shifted[m] = vm + off * d_s
    shifted[f] = vf + off * d_s

s_w = {w: shifted[w].dot(a) for w in ES_male_occupations + ES_female_occupations}
S_male = sum(s_w[m] for m in ES_male_occupations)
S_female = sum(s_w[f] for f in ES_female_occupations)
test_stat = abs(abs(S_male) - abs(S_female))
all_targets = ES_male_occupations + ES_female_occupations
N = len(ES_male_occupations)

np.random.seed(520)
n_exact, n_less, n_greater = 0, 0, 0
for _ in range(10000):
    c = np.random.choice(all_targets, N, replace=False)
    c_set = set(c)
    not_c = [w for w in all_targets if w not in c_set]
    Sc = sum(s_w[w] for w in c)
    Snot_c = sum(s_w[w] for w in not_c)
    stat = abs(abs(Sc) - abs(Snot_c))
    if abs(stat - test_stat) < 1e-12:
        n_exact += 1
    elif stat < test_stat - 1e-12:
        n_less += 1
    else:
        n_greater += 1

print(f"Claim 2 Permutations (10,000 samples):")
print(f"  Exact ties (stat == test_stat): {n_exact} ({n_exact / 100:.2f}%)")
print(f"  Strictly less (stat < test_stat): {n_less} ({n_less / 100:.2f}%)")
print(f"  Strictly greater (stat > test_stat): {n_greater} ({n_greater / 100:.2f}%)")
```

### Script Output
```
Loading Spanish fastText vectors...
ES Original: total_male = 2.9898, total_female = -6.6817
ES Original MWEAT-Diff: 3.6918 (Paper Table 1: 3.6918)
Claim 1 Identity max absolute difference across 10 trials: 3.55e-15
Claim 2 Permutations (10,000 samples):
  Exact ties (stat == test_stat): 9597 (95.97%)
  Strictly less (stat < test_stat): 403 (4.03%)
  Strictly greater (stat > test_stat): 0 (0.00%)
```

---

## Summary of Notebook References

| Topic | 0-Based Cell Index | Key Lines / Operations |
|---|---|---|
| Load Spanish fastText | [Cell 12](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) | Lines 1–19 (`load_vec(spanish_path, nmax)`) |
| Load missing Shift Ori embedding | [Cell 14](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) | Lines 1–4 (`./data/ori_offset_debiased_ES_embeddings.txt`) |
| `doPCA` with operator precedence bug | [Cell 36](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) | Lines 6–9 (`center = (embedding[a] + embedding[b]/2)`) |
| Grammatical gender LinearSVC fit | [Cell 73](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) | Lines 12–17 (`clf_3000 = LinearSVC()`, normalized coef) |
| LDA failure | [Cell 75](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) | Uncaught `ValueError` in `LinearDiscriminantAnalysis` |
| Cosine 0.389 reproduction | [Cell 77](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) | Lines 1–2 (`cos_sim` outputs 0.38851) |
| Definition of `drop(u, v)` (Eq. 2) | [Cell 78](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) | Lines 3–5 (`drop(u, v)`) |
| Definition of `modified_WEAT` | [Cell 217](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) | Lines 1–28 (returns `[diff, abs_diff]`) |
| Definition of `_weat_pval` | [Cell 230](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) | Lines 7, 20–23 (`stat > test_stat`) |
| Occupation word lists (58 pairs) | [Cell 234](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) | Lines 1–3 (`ES_male_occupation_words`, `ES_female_occupation_words`) |
| Shift Ori offset calculation | [Cell 273](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) | Lines 1–5 (`offset_list_ori_ES`) |
| Shift Ori offset addition | [Cell 312](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) | Lines 1–7 (adds offset along gender direction) |
| MWEAT evaluation (0.3090, p=0.269) | [Cell 305](file:///Users/watcher/zhou-blind-check/zhou_repo/bias_emnlp19.ipynb) | Lines 1–3 (`_weat_pval` call) |
