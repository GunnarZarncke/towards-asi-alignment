# Witness Phase 3 — protocol freeze

**Frozen:** 2026-08-28. Reopen only by amending this file. Parent: [`witness.md`](witness.md). Scope: [`witness-phase0.md`](witness-phase0.md).

Not a sixth simulation line. Raw caches in [`experiments/witness/data/`](../../experiments/witness/data/) (gitignored except README). Artifacts: [`experiments/witness/`](../../experiments/witness/).

**Exit (parent):** one bundle **non-implication** table (C-004); one **selector** table (C-007). Inputs frozen below *before* looking at signs. Report fail or refuse; do not retune the 1-D, geometry, proxy, or target after seeing the numbers.

---

## C-004 — value-bundle non-implication (Moral Machine country AMCE)

**Protocol version:** `h4-bundle-v1.0.0`  
**Host:** H4 public survey surface (not Wikipedia category text; that remains backup).  
**Source (frozen):** Awad et al., *The Moral Machine experiment*, Nature 2018; OSF project [osf.io/3hvt2](https://osf.io/3hvt2) (country-level AMCE used to reproduce Fig. 3 / Extended Data).

**Required columns (parent-plan fields):**

| Field | Role |
|-------|------|
| country | unit |
| nine AMCE coordinates | tradeoff **geometry** (Intervention, Relation to AV, Gender, Fitness, Social Status, Law, Age, Species, Number — paper labels) |
| sample-size filter | paper’s country inclusion rule if present in the file; else all rows in the country table |

**Frozen 1-D (chosen before geometry distances):** AMCE for **Number** (“sparing more characters”). This is the scalar “progress / utilitarianism” compression. It is **not** re-chosen after seeing pairs.

**Frozen geometry:** Euclidean distance on the **other eight** AMCE coordinates (Number excluded so the 1-D is not an axis of the distance).

**Layer fail:** among included countries, there exist pairs whose geometry distance is **≥ median pairwise geometry distance**, while \(|\Delta\) Number AMCE\(|\) is **≤ 25th percentile** of all pairwise \(|\Delta\) Number\(|\). That is non-implication: close on the frozen 1-D, far on the frozen tradeoff vector.

**Refuse:** country table missing the nine AMCE columns; \(n < 20\) countries after the inclusion filter.

**Not claimed:** a universal moral geometry; MB2 discharged; WVS/ESS/HH-RLHF (unpaid backups if this source refuses).

---

## C-007 — selector shift (Arena Elo vs MASK honesty)

**Protocol version:** `h4-selector-v1.0.0`  
**Host:** H4 public eval surface.  
**Sources (frozen):**

1. MASK Table 3 (arXiv:2503.03750v3 HTML): model, \(P(\mathrm{honest})\), Accuracy. **Not** training FLOP (that join is **W-2**).
2. Chatbot Arena Elo from Hugging Face `mathewhe/chatbot-arena-elo` revision **`20250301`** (first dated tag on or after 2025-03-01, MASK arXiv date). Score field `Arena Score`.

**Required columns:**

| Field | Role |
|-------|------|
| model (MASK name) | unit |
| \(P(\mathrm{honest})\) | **preservation target** |
| Accuracy | capability check (must not be the selector) |
| Arena Score | **exogenous proxy / selector** |

**Frozen alias table:** only exact case-insensitive substring matches after stripping dates/sizes in a **pre-registered** alias list in `experiments/witness/fixtures/h4-selector-aliases-v1.json`. No aliases added after seeing Spearman signs.

**Layer fail:** joined \(n \ge 8\); Spearman(\(Elo\), \(P(\mathrm{honest})\)) \(\le 0\); Spearman(\(Elo\), Accuracy) \(> 0\). Population occupying the public selector is ordered by the proxy, not by the honesty target.

**Refuse:** \(n < 8\) after the frozen alias list; snapshot missing `Arena Score`; treating FLOP as the selector (already W-2).

**Not claimed:** \(\kappa^*\) for honesty; leaderboard causation; MB6 discharged. H3 editor retention and H2 vendor-share remain unpaid.

---

## Finding IDs

**W-5** C-004 bundle · **W-6** C-007 selector. Ledger: `experiments/witness/results/FINDINGS.md`.

**Checkers:** `python3 experiments/witness/check_h4_bundle.py` · `python3 experiments/witness/check_h4_selector.py`
