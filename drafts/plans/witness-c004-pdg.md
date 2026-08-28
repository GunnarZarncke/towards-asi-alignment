# Witness — C-004 later host: Pandemic Dictator Game (same-unit giving)

**Frozen:** 2026-08-28. Reopen only by amending this file. Parent: [`witness.md`](witness.md). Prior freeze: [`witness-c004-raw.md`](witness-c004-raw.md) (W-12). Not Phase 5. Do **not** retune W-12. Do **not** retune this file after seeing held-out scores.

**Claim strength:** methodology-building. Pays **bearer substitution + within-person giving stability** (care/giving class; a \(\Phi\)-sketch only). Does **not** test LHCV. Does **not** discharge MB2. Does **not** transfer Moral Machine geometry.

**Finding ID:** **W-13**. Ledger: `experiments/witness/results/FINDINGS.md`.

---

## Why this, not MM again

W-12 is traffic-dilemma policy effect. The next row in [`witness-c004-raw.md`](witness-c004-raw.md) is a longitudinal dictator game with **multiple targets for the same person**: friend, unknown peer, doctor, COVID patient, poor immune system (van de Groep / Sweijen / Dubois Urban Rotterdam PDG). That is bearer substitution, not trolley Number vs types.

---

## Protocol version

`h4-pdg-v1.0.0`

**Host:** H4 public survey / lab surface (individual giving rows).

**Source (frozen preference order; first dump that yields person×wave×target amounts wins; do not mix after scoring):**

1. Sweijen / Dubois Urban Rotterdam longitudinal PDG — OSF [osf.io/h5x2a](https://osf.io/h5x2a/), prereg [osf.io/x69t7](https://osf.io/x69t7/), EUR Dataverse `10.25397/eur.14916531` / collection `10.25397/eur.c.5809043`.
2. If (1) has no individual table: van de Groep et al. 2020 PLOS ONE daily-diary PDG — Dataverse `10.25397/eur.12783161` / `10.34894/c81eja` (merged `.sav`; two Dictator waves, five targets).

If neither dump is a **public individual** table (prereg PDFs only, Anubis/login wall, author-request-only), **refuse**. Do **not** substitute country means, Moral Machine, or paper bar charts.

**Refuse scoring source 2 if it is the only table:** van de Groep et al. 2020 is a PLOS ONE **daily-diary adolescent** sample (ages 10–20). This protocol does **not** score that microdata. Metadata (file names on DataverseNL) may be listed. Adult Urban Rotterdam rows remain the intended host.

**Unit:** participant ID (any stable person key in the dump).

**Core targets (frozen):** `friend`, `unknown`, `doctor`, `covid`, `poor_immune`. Map columns by documented labels (English or Dutch). Extra targets (vaccinated/unvaccinated from later waves) are **not** in the primary geometry.

**Outcome \(y\):** coins given to that target, 0–10 (or the dump’s documented coin scale; if scale is not 0–10, keep native units and report the unit; do not rescale after seeing scores).

**Inclusion:** person has all **five** core targets on **≥ 2** distinct waves. **Refuse** if fewer than **50** included people.

**Split (frozen before scores):** within each included person, sort waves chronologically; first \(\lfloor 0.7 n_{\mathrm{waves}}\rfloor\) waves train, remainder test; require **≥ 1** test wave (if not, drop the person). Seed **7** unused except for any later bootstrap.

---

## Frozen models (train waves only)

1. **Intercept:** one global train mean \(\bar y\) as \(\hat y\) for every person×target on test.
2. **1-D:** that person’s train **grand mean** (scalar generosity) as \(\hat y\) for every target on test.
3. **Geometry:** that person’s train **per-target mean** as \(\hat y\) for the matching target on test. Missing train target ⇒ drop that test cell (do not impute from other targets).

No logistic; this is a giving amount. No new features after seeing scores.

**Primary metric:** mean **MAE** (coins) over included people (each person equally weighted; within person, mean over that person’s test cells). Secondary (report only): mean signed error.

**Margins (fixed first):** geometry MAE is **≤** 1-D MAE **minus 0.25** coins **and** **≤** intercept MAE **minus 0.25**. Lower MAE is better. Both must hold.

---

## Outcomes (do not rename after seeing signs)

| Outcome | When |
|---------|------|
| **Fail (scalar generosity / non-implication)** | Geometry meets both MAE margins. A single generosity number is not the giving policy. |
| **Pass (bearer-profile detection)** | Same numerical event — a per-target profile predicts held-out waves better than 1-D and intercept. Record **both** labels. |
| **Ambig.** | Geometry beats intercept but not 1-D by 0.25, or beats 1-D but not intercept. |
| **Refuse** | No public individual dump; cannot map five targets; median waves \(<2\); \(<50\) included people. |
| **Null (fail to detect)** | Geometry misses both margins. **Not** “giving is scalar.” Stop: this host did not show a stable bearer profile under this freeze. |

**Stop (if fail/pass row):** stop treating a person-level generosity scalar as the PDG policy for *these people in this giving class*.

**Not claimed:** LHCV; general human values; MB2; transfer from W-12; COVID-specific ethics.

---

## Predictions (registered before run)

Written 2026-08-28. Compare to FINDINGS after the checker runs; do not edit this list to match.

1. **Primary:** both MAE margins (geometry better than 1-D and intercept by ≥ 0.25 coins).
2. **1-D still beats intercept:** person grand means beat the global train mean (people differ in generosity) but lose to per-target profiles.
3. **Need/deservedness sketch (train only, signs):** mean giving to `{covid, poor_immune, doctor}` **>** mean giving to `unknown`.
4. **Scope:** giving-class only. Do not predict transfer to Moral Machine or courts.

If the dump is missing **or** only the 2020 adolescent diary SPSS is public: **refuse** (prediction: OSF is prereg-only; DataverseNL may list SPSS names without an adult longitudinal table).

---

## Checker

`python3 experiments/witness/check_h4_pdg.py` — print source used, \(n\), three MAEs, both margins, refuse-or-outcome. Raw cache gitignored under `experiments/witness/data/pdg/`.
