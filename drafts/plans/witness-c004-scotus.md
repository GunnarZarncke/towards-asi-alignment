# Witness — C-004 later host: SCDB justice votes (held-out policy direction)

**Frozen:** 2026-08-29. Reopen only by amending this file. Parent: [`witness.md`](witness.md). After [`witness-c004-cpc.md`](witness-c004-cpc.md). Not Phase 5. Do **not** retune W-12. Do **not** retune this file after seeing held-out scores.

**Claim strength:** methodology-building. Pays a **same-unit detection-pipeline** check on institutional vote direction (justice-centered, not correction-channel CCI). Observational; doctrine and coalition confound. Does **not** discharge MB2. Does **not** transfer W-12 or W-14.

**Finding ID:** **W-16**. Ledger: `experiments/witness/results/FINDINGS.md`.

---

## Why this

[`witness-c004-raw.md`](witness-c004-raw.md) lists the Supreme Court Database as the next v1 C-004 later host: stable justice IDs, repeated votes, public case codings. v2 institutional correction (handle→act) is a **different** claim — see [`witness-v2.md`](witness-v2.md).

---

## Protocol version

`h4-scotus-v1.0.0`

**Host:** H4 public institutional surface (SCDB modern release).

**Source (frozen):** Supreme Court Database **2025 Release 01**, justice-centered CSV organized by Supreme Court citation — [download zip](https://scdb.la.psu.edu/?jet_download=d9fd858d0211fe70abbe33bf7cd7ec832f3a2313), file `SCDB_2025_01_justiceCentered_Citation.csv` inside. If that file is missing, **refuse**. Do **not** switch to case-centered, docket-organized, or legacy (pre-1946) releases after seeing scores. Cite: Spaeth et al., Supreme Court Database (2025 Release 01).

**Unit:** `justiceName`.

**Inclusion:** justice has **≥ 40** rows with a valid binary label (below) and finite frozen case features. **Refuse** if fewer than **9** included justices (fewer than a full bench worth of eligible units).

**Split:** within each included justice, sort by (`term`, `caseId`) lexicographic (numeric coerce on `term` and `caseId` when possible); first \(\lfloor 0.7 n\rfloor\) train, remainder test; require **≥ 8** test rows (else drop). Seed **7** unused except later bootstrap.

**Choice label \(y\) (frozen):** `direction` in \(\{1,2\}\) only — \(y=1\) if `direction`=1 (liberal), \(y=0\) if `direction`=2 (conservative). Other or missing `direction` ⇒ drop row. Do **not** use `vote` (affirm/reverse) as \(y\).

**1-D (frozen):** `issueArea` as numeric (policy-domain axis).

**Geometry features (frozen; all from the same row):** `issueArea`, `lawType`, `caseOrigin`, `caseSource`, `lcDisagreement`, `jurisdiction`, `decisionDirection`. If a listed column is absent, drop it from **all** models before fitting (do not add replacements). Rows with missing or non-numeric values in any retained column ⇒ drop.

**Term filter:** none — use all rows in the frozen CSV (modern terms 1946–2024 as shipped).

---

## Frozen models

Shared slope, justice intercept \(\alpha_i\); train rows only. L2-regularized logistic, \(\lambda=1.0\) (fixed).

1. **Intercept-only:** \(\mathrm{logit}\,P(y=1)=\alpha_i\).
2. **1-D:** \(\alpha_i + \beta \,\mathrm{issueArea}\).
3. **Geometry:** \(\alpha_i + \beta^\top x\) (frozen feature list).

**Primary metric:** mean held-out **accuracy** over included justices (equal weight). Secondary: mean held-out log-loss.

**Margins:** geometry beats 1-D by **≥ 0.05** accuracy **and** beats intercept by **≥ 0.05**. Both must hold.

Do not downsample justices (≤ 40 in modern release).

---

## Outcomes

| Outcome | When |
|---------|------|
| **Fail (issue-area-only / non-implication)** | Geometry meets both margins. Single issue-area axis is not the whole reusable direction. |
| **Pass (detection pipeline)** | Same event — multi-feature direction predicts held-out liberal vote. Record both labels. **Not** a C-004 values claim. |
| **Ambig.** | Beats one margin only. |
| **Refuse** | Missing CSV; no `justiceName`/`direction`/feature columns; `<9` included justices. |
| **Null** | Geometry misses both margins. Stop: pipeline did not beat issue-area+intercept here. |

**Not claimed:** correction-channel integrity; coalition-free causal doctrine; LHCV; MB2; transport to Moral Machine or CPC.

---

## Predictions (registered before run)

Written 2026-08-29. Do not edit to match scores.

1. Geometry beats **intercept** by ≥ 0.05 (case codings add signal beyond justice baseline).
2. Geometry beating **1-D issueArea** by ≥ 0.05 is **uncertain** — issue area is already a strong policy-domain compression; ambig. or null is an allowed hit.
3. 1-D issueArea beats intercept (domain predicts vote direction).
4. Scope: modern SCDB justice votes only; observational institutional class.

---

## Checker

`python3 experiments/witness/check_h4_scotus.py`. Cache gitignored under `experiments/witness/data/scotus/`.
