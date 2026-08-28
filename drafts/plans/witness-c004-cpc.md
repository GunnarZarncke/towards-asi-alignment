# Witness — C-004 later host: CPC2015 raw (held-out latent direction)

**Frozen:** 2026-08-28. Reopen only by amending this file. Parent: [`witness.md`](witness.md). After [`witness-c004-pdg.md`](witness-c004-pdg.md). Not Phase 5. Do **not** retune W-12. Do **not** retune this file after seeing held-out scores.

**Claim strength:** methodology-building. Pays a **same-unit detection-pipeline** check on repeated risky choice (not a moral bundle). Does **not** discharge MB2. Does **not** transfer W-12.

**Finding ID:** **W-14**. Ledger: `experiments/witness/results/FINDINGS.md`.

---

## Why this

[`witness-c004-raw.md`](witness-c004-raw.md) lists CPC2015/CPC18 as the method check after dictator games: `SubjID`, repeated gambles, held-out latent direction. Public CSV on Zenodo.

---

## Protocol version

`h4-cpc2015-v1.0.0`

**Host:** H4 public lab surface.

**Source (frozen):** Erev, Ert, Plonsky et al. CPC2015 raw Experiment **1** only — Zenodo [10.5281/zenodo.321652](https://doi.org/10.5281/zenodo.321652) file `RawDataExperiment1sorted.csv` (or the same Experiment 1 CSV under [10.5281/zenodo.776226](https://doi.org/10.5281/zenodo.776226)). If that file is missing, **refuse**. Do **not** switch to Experiment 2/3 after seeing scores. Cite: Erev, Ert, Plonsky, Cohen & Cohen (2017) *Psychological Review*.

**Unit:** `SubjID`.

**Inclusion:** subject has **≥ 40** rows with a binary choice label (below) and finite \(\Delta\mathrm{EV}\). **Refuse** if fewer than **40** included subjects.

**Split:** within each included subject, sort by (`GameID`, `Trial`) lexicographic as strings then numeric if needed; first \(\lfloor 0.7 n\rfloor\) train, remainder test; require **≥ 8** test rows (else drop). Seed **7** unused except later bootstrap.

**Choice label \(y\) (frozen):** if column `Risk` exists and is in \(\{0,1\}\) (or 0/1 after numeric coerce), use it. Else **refuse** (do not reverse-engineer Button×Order after seeing accuracy).

**\(\Delta\mathrm{EV}\) (1-D):** \(\mathrm{EV}_A = p_{Ha} H_a + (1-p_{Ha}) L_a\), \(\mathrm{EV}_B = p_{Hb} H_b + (1-p_{Hb}) L_b\), \(\Delta\mathrm{EV} = \mathrm{EV}_B - \mathrm{EV}_A\). Column names frozen: `Ha`, `pHa`, `La`, `Hb`, `pHb`, `Lb`. Missing column ⇒ refuse.

**Geometry features (frozen; all from the same row):** \(\Delta\mathrm{EV}\), `Amb`, `LotNum`, `Corr`, `pHa`, `pHb`. If a listed column is absent, drop it from **all** models before fitting (do not add replacements).

---

## Frozen models

Shared slope, subject intercept \(\alpha_i\); train rows only. L2-regularized logistic, \(\lambda=1.0\) (fixed).

1. **Intercept-only:** \(\mathrm{logit}\,P(y=1)=\alpha_i\).
2. **1-D:** \(\alpha_i + \beta \Delta\mathrm{EV}\).
3. **Geometry:** \(\alpha_i + \beta^\top x\) (frozen feature list).

**Primary metric:** mean held-out **accuracy** over included subjects (equal weight). Secondary: mean held-out log-loss.

**Margins:** geometry beats 1-D by **≥ 0.05** accuracy **and** beats intercept by **≥ 0.05**. Both must hold.

If the dump is large, do not downsample subjects unless \(n>20\,000\); then seed **7** cap **20 000** after inclusion.

---

## Outcomes

| Outcome | When |
|---------|------|
| **Fail (EV-only / non-implication)** | Geometry meets both margins. Scalar EV is not the whole reusable direction. |
| **Pass (detection pipeline)** | Same event — multi-feature direction predicts held-out risky choice. Record both labels. **Not** a C-004 values claim. |
| **Ambig.** | Beats one margin only. |
| **Refuse** | Missing Exp 1 file; no `SubjID`/`Risk`/\(\Delta\mathrm{EV}\) columns; \(<40\) included subjects. |
| **Null** | Geometry misses both margins. Stop: pipeline did not beat EV+intercept here. |

**Not claimed:** moral bundles; LHCV; MB2; transfer to PDG or Moral Machine.

---

## Predictions (registered before run)

Written 2026-08-28. Do not edit to match scores.

1. Geometry beats **intercept** by ≥ 0.05 (problem features plus \(\Delta\mathrm{EV}\) are not noise).
2. Geometry beating **1-D \(\Delta\mathrm{EV}\)** by ≥ 0.05 is **uncertain** — EV is already a strong compression on this task; ambig. or null is an allowed hit for this host.
3. 1-D still beats intercept (EV is real).
4. Scope: risk/ambiguity lab class only.

---

## Checker

`python3 experiments/witness/check_h4_cpc2015.py`. Cache gitignored under `experiments/witness/data/cpc2015/`.
