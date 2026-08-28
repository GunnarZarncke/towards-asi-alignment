# Witness — C-004 same-unit bundle effect (Moral Machine raw)

**Frozen:** 2026-08-28. Reopen only by amending this file. Parent: [`witness.md`](witness.md). Not Phase 5 (that remains CIRIS live). Not a sixth sim. Do **not** retune features, split, seed, or margins after seeing held-out scores.

**Claim strength:** methodology-building. Pays a **policy-effect / reusable-direction** witness on one decision-making unit class (ch16 activation + policy effect; tradeoff geometry as held-out non-implication vs 1-D). Does **not** test LHCV \(L\to H\to C\). Does **not** discharge MB2.

**Finding ID (reserve):** **W-12**. Ledger: `experiments/witness/results/FINDINGS.md`.

---

## Why this, not W-5 again

**W-5** used country AMCE (wrong unit: place). **W-7** refused WVS/ESS/LHCV-as-host. Chapter 16 identifies a bundle by **counterfactual variation of policy** in the **same** agent, not by country means.

Raw Moral Machine sessions (OSF [osf.io/3hvt2](https://osf.io/3hvt2); feature notes [osf.io/wt6mc](https://osf.io/wt6mc)) are the cheapest public host with: stable respondent/session IDs, randomized paired outcomes, shared scene ontology, repeated dilemmas.

---

## Protocol version

`h4-mm-raw-v1.0.0`

**Host:** H4 public survey surface (raw rows, not `CountriesChangePr.csv`).

**Source (frozen):** Awad et al., *The Moral Machine experiment*, Nature 2018; OSF Moral Machine project. Prefer the published individual-response table (commonly `SharedResponses` / Moral Machine Data dump). If that file is missing, **refuse** — do not substitute country AMCE.

**Unit (frozen, first available):** `UserID` if present and non-null on ≥ half of paired scenarios; else `ExtendedSessionID`; else `ResponseID` prefix only if the readme defines a session key. Document which key was used. **Refuse** if no stable unit column exists.

**Scenario pair:** two rows sharing `ResponseID` (stay vs swerve / Intervention). Incomplete pairs dropped.

**Inclusion:** unit has **≥ 8** complete paired scenarios after dropping missing `Saved`. Predicted typical session length is ~13; 8 is the floor so a train/test split is possible. **Refuse** if fewer than **500** included units (too thin for a mean held-out comparison).

**Split (frozen before scores):** within each included unit, sort pairs by `ResponseID` (lexicographic); first \(\lfloor 0.7 n\rfloor\) train, remainder test; require **≥ 2** test pairs (if not, drop the unit). Seed **7** is unused for this deterministic split; keep it for any later bootstrap CIs only.

---

## Frozen columns (do not add after seeing scores)

| Field | Role |
|-------|------|
| unit key | same decision-maker |
| `ResponseID` | pair |
| `Saved` | policy (1 = this outcome chosen) |
| `Intervention`, `PedPed`, `Barrier`, `CrossingSignal` | structural features |
| `NumberOfCharacters` (or paper equivalent) | 1-D / Number axis |
| Twenty character-type counts (Man, Woman, Pregnant, Stroller, OldMan, OldWoman, Boy, Girl, Homeless, LargeWoman, LargeMan, Criminal, MaleExecutive, FemaleExecutive, FemaleAthlete, MaleAthlete, FemaleDoctor, MaleDoctor, Dog, Cat) | bearer / type geometry |

**Difference vector \(\Delta x\):** chosen-outcome features minus unchosen-outcome features on the frozen fields above (structural + Number + 20 types). If a listed type column is absent, **refuse** that column and drop it from **all** models before fitting — do not replace with a new type.

**1-D (same as W-5 scalar, now at the right unit):** \(\Delta\) Number only.

---

## Frozen models

All fit **only on train pairs**. Shared slope, respondent intercept \(\alpha_i\):

1. **Intercept-only:** \(\mathrm{logit}\,P(\text{Saved}=1)=\alpha_i\).
2. **1-D:** \(\alpha_i + \beta_N \Delta\mathrm{Number}\).
3. **Geometry:** \(\alpha_i + \beta^\top \Delta x\) (full frozen \(\Delta x\)).

Estimator: L2-regularized logistic, \(\lambda=1.0\) (fixed; not CV-tuned). If the dump is too large, downsample **units** uniformly at random with seed **7** to **20 000** included units **after** the ≥8 filter; do not downsample pairs inside a unit.

**Primary metric:** mean **held-out accuracy** over included units (each unit equally weighted). Secondary (report, not retuned): mean held-out log-loss.

**Margins (fixed first):** geometry beats 1-D by **≥ 0.05** accuracy **and** beats intercept-only by **≥ 0.05**. Both must hold.

---

## Outcomes (do not rename after seeing signs)

| Outcome | When |
|---------|------|
| **Fail (scalar sufficiency / C-004 non-implication at unit)** | Geometry meets both margins. 1-D is not the policy. |
| **Pass (bundle-effect detection)** | Same numerical event as the row above — a reusable multi-feature direction predicts held-out policy. Record **both** labels in FINDINGS (fail of 1-D leaf; pass of detection). |
| **Ambig.** | Geometry beats intercept but **not** 1-D by 0.05, or beats 1-D but not intercept. |
| **Refuse** | Missing unit key; cannot pair `ResponseID`; median \(n<8\); \(<500\) included units; only country table available. |
| **Null (fail to detect)** | Geometry misses both margins. **Not** “values are scalar.” Stop: this host did not show a reusable direction under this freeze. |

**Stop (if fail/pass row):** stop treating country AMCE or a Number-only score as the value bundle for *these respondents in this dilemma class*.

**Not claimed:** LHCV hubs/loops; general human values; MB2; Moral Machine as ethics; cross-domain transport.

---

## Predictions (registered before run)

Written 2026-08-28. Compare to FINDINGS after the checker runs; do not edit this list to match.

1. **Primary:** geometry meets both +0.05 margins vs 1-D and intercept. Aggregate AMCE already showed multiple attributes; the prediction is that this **survives within respondent** on held-out dilemmas.
2. **1-D still above intercept:** Number-only beats intercept-only (utilitarian compression is real) but loses to geometry — same non-implication as W-5, correct unit.
3. **Pooled \(\hat\beta\):** Number coefficient and Species (Dog+Cat vs human-type sum) coefficient are both nonzero in sign on the train fit (two-sided, no p-hacking: report signs and magnitudes only; no extra attributes).
4. **Scope:** effect is **traffic-dilemma-class only**. Do not predict transfer to dictator games or courts.

If (1) fails and (2) holds: ambig. or null as the table says. If pairing/IDs fail: refuse (prediction: OSF dump **does** have session/user keys; refuse would surprise).

---

## Later / alternative hosts (not this freeze)

Do not fetch these until W-12 is recorded (or this protocol refuses).

| Host | Why later | What it could pay |
|------|-----------|-------------------|
| Pandemic Dictator Game (longitudinal, multiple targets) | Bearer substitution + stability; little tradeoff diversity | Care/giving direction + \(\Phi\) sketch |
| CPC2015/CPC18 raw (`SubjID`, repeated gambles) | Method check (held-out latent direction); not moral bundles | Detection pipeline, not C-004 values |
| Supreme Court Database (justice-centered) | Observational; doctrine/coalition confound | Institutional reusable policy directions |
| BBQ published per-example logits | Bearer/identity policy effect in a **model**; bias more than bundles | Artificial-system \(\Phi\)-like test |
| HH-RLHF / PKU-SafeRLHF dual labels | Still optional; need same judge/policy across varied contexts | Same-unit 1-D vs harm axis |
| Wikipedia admin/RfA repeated acts | Heavy feature reconstruction | Institutional C-004 analogue |
| KernelCI / lore NAK / CIRIS live | Other layers | Not C-004 |

**Still unpaid after W-12 even if it hits:** LHCV \(\epsilon_i(t),s_h(t),c_h(t)\); hub compression; selectable Goodhart on a real selector (GL-85); cross-domain bundle transport.

---

## Checker (when implemented)

`python3 experiments/witness/check_h4_mm_raw.py` — print inclusion \(n\), which unit key, three held-out accuracies, both margins, refuse-or-outcome. Raw cache gitignored under `experiments/witness/data/`.
