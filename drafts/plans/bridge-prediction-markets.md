# Bridge prediction markets

Status: **P0 + MB6 retarget** (2026-09-18). Working criteria: [`drafts/bridge-prediction-market-criteria.md`](../bridge-prediction-market-criteria.md) (`0.3-working`). Historical source: [`drafts/AI_Alignment_Prediction_Market_Resolution_Criteria.docx`](../AI_Alignment_Prediction_Market_Resolution_Criteria.docx) (python-docx export; **no comments or tracked changes**). Lane: Field mapping + Outreach listing. MB6 *formal* rewrite is Spine (not this session’s Lean). Not a v1 manuscript change.

The proposal is 14 **binary** markets resolving by **31 December 2027**. It is a *contract layer* on the live bridges, not a new ontology. Refuse maps to NO. Aggregation is the point.

## Goal

Own the proposal as a project instrument:

1. Freeze a **market ↔ `MB*`** map (including splits the proposal flattens).
2. Amend the criteria where they would mis-resolve a typed cut, bake a δ into a definition, or treat YES as bridge discharge.
3. List the markets only after those amendments, with a named resolver. Outcomes are YES/NO only.

**Success (instrument, not alignment):** a public catalog of frozen **YES/NO** contracts whose resolution cannot be honestly read as “Lean proved / disproved `MB*`,” that can still aggregate, and whose MB6 row tests a **signed** correction-selection gradient rather than unsigned basin existence.

**Weakest link:** calendar default-NO is now even lumpier (refuse → NO). Most of these are open research programs. A 2027 NO is weakly informative unless titles say *met these bars*, not *the bridge is false*. The lump is accepted so a crowd can price P(YES).

## Non-goals

- Do not treat a YES resolution as discharging any `MB*` axiom, `A-*` assumption, or WWCTV box.
- No new `MB12`. No Lean covering from prices. No prices in `BridgeAssumptions`.
- No v1 chapter, no sixth intro claim, no field-matrix green cell from a market price.
- Do not use these markets as deployment oracles (ch10 Predict-O-Matic / closed forecast→action→score loop).
- Do not import the 80/90/15% bars into Lean, CCI slack, or `RiskGap δ`. Those numbers are **contract terms**, not derived thresholds.
- In-repo sims (toy / embedded / lab / graded-lab) may inform prices; they cannot be the sole YES evidence (proposal already says this).

## What already exists (do not re-derive)

| Object | Where | What the proposal adds |
|--------|--------|------------------------|
| Live `MB*` axioms / crux `Prop`s | `Core.lean`, `MB2Identifiability.lean`, `Correction.lean`, `Forgeability.lean`, `Certification.lean` | Time-bounded, public, independently checkable **binary** operationalizations |
| WWCTV boxes | chapter ends; ch48 master disconfirmer | Calendar-dated contracts; WWCTV stays qualitative and undated |
| Freeze / preregister / refuse | [`docs/METHODOLOGY.md`](../../docs/METHODOLOGY.md) | Same habit, pointed at a *hidden benchmark* and a *serious adversarial budget* |
| Backtest fail / refuse / null | [`backtest.md`](backtest.md) | Experiments still refuse internally. **Markets map refuse → NO** (conservative lump) |
| App B crosswalk | `appendices/appB-bridge-crosswalk.tex` | Markets are field-facing bets on the *book’s* cuts, not on field homographs |
| Logical-induction WWCTV | ch48; Cite/Wait in `TODO.md` | These are ordinary prediction markets, not Garrabrant LI. LI remains a side channel. |
| Target Realization / constructibility | [`construct.md`](construct.md); not an `MB*` | Market 14 is this neighborhood, not MB11 |
| Shared-instrument chokepoint | `Chokepoint.lean`; U-03/U-05/U-14/U-16 | Several markets are correlated through A-009; treating them as independent overstates information |

## Mapping (proposal § → spine)

The 14 sections track the live roster (MB8 gravestone correctly omitted). They are **not** 1–1 with Lean arrows. **MB3 = §3, MB4 = §4** (not missing rows). Working addenda live in the criteria file.

| § | Proposal title | Primary spine object | Notes |
|---|----------------|----------------------|--------|
| 1 | Discovering where control resides | **MB1** | Sufficient interventional cut, not unique blanket; false-complete-certificate bar kept |
| 2 | Persistent trade-off priorities | **MB2** | Identifiability + causal-control; refuses held-out-only. A-001 not a 2027 market |
| 3 | Who/what safety rules apply to | **MB3** | Bearer **transport** (four families). Admission (U-17) optional under the same 5-judge rule, not a 15th market |
| 4 | Consequential corrections change the system | **MB4** | Uptake + persistence + sham fail. Channel-preservation family added as the `PreservesCorrectionOperator` probe *inside* this market |
| 5 | Auditor outside the audited thing | **MB4a** | Four attack families |
| 6 | Safety regressions in successors | **MB5** detector | Seven conserved properties (source six mapped + control locus). Not MB10; not the Lean composition arrow |
| 7 | Competition selects against correctability | **MB6** (\(g_{\mathrm{CCI}}\) slice) | Source §7 bars; measurand is the **signed** correction-selection gradient, not unsigned `BasinStable`. No §7a. Lean MB6a/MB6b still the old arrows — rewrite before treating a test as about those axioms |
| 8 | Auditor can actually see the system | **MB7a** | |
| 9 | Bounds on unmonitored routes | **MB7b** | \(u\) is a contract scalar |
| 10 | Low hidden capability + reliable correction | **MB7c** | Composition market; not a joint certificate of the other rows |
| 11 | Coordination without visible messages | **MB7d** | Common-cause vs hidden coordination. U-12 full acausal trade not required |
| 12 | Safety proxy no longer tracks the real thing | **MB9** | Conservativity, not GSAI completeness |
| 13 | Safety audit optimized around | **MB10** | Frozen white-box audit |
| 14 | Binding deployment criteria | **Constructibility** | **Not MB11.** No 2027 MB11 market |

**Common qualification rule** (public by 2027-12-31; independent verification; toys not sole evidence; “serious adversarial evaluation”; at least one broadly capable system where required) is a shared operationalization of *adversarial*, not a new bridge.

## P0 applied (2026-09-18)

These were the obvious contract edits. Detail in the working criteria, not as silent interpretation of the docx.

1. **Claim-strength header** on every market. YES = met *these bars* by 2027.
2. **Refuse → NO.** No third market outcome. Inapplicable / no eval / desk disagreement / failed CI → NO. Experiments keep refuse internally.
3. **Threshold freeze.** New version string if a bar changes; numbers stay contract-only (not `RiskGap`).
4. **§6 → seven properties.** Map the source six onto ch31; add control-locus continuity; one-failure-at-a-time is six-of-seven.
5. **§10 / §14 typing.** §10 = MB7c composition. §14 = governance-binding, not MB11; no extra MB11 contract for 2027.
6. **§4 channel-preservation family** inside MB4, not a missing row.
7. **§1 non-uniqueness.** Sufficient cut; keep false-complete-certificate.
8. **§7 power.** Keep AUROC 0.85; if \(n<40\), lower 95% CI ≥ 0.70 else **NO**.
9. **Per-market adversarial budget table.** Default hours path; §§4/5/9/10/12/13 full “serious”; §11 hours-only.
10. **Predict-O-Matic + toy/repo** clauses.
11. **Not-a-joint-certificate banner.** Conditionals later if listing happens; do not delay P2 for parlays.
12. **§7 MB6 = \(g_{\mathrm{CCI}}\)** (2026-09-18 later). Unsigned-basin §7a **retracted**. Formal object change is Spine; 2027 market is the estimator/prediction slice only.
13. **Judgment stack** (precision → publication freeze → two-person desk memo → §3 panel only → conservative NO). No lone expert judge.

Docx has **no** in-file proposed changes (no comments, no track-changes). `0.2-working` *is* the amendment layer.

## Review (post-P0)

### Completeness

Usable as working contracts for the live bridges that have 2027 tests. Remaining gaps are **typed as out of catalog**, not as missing MB3/MB4:

- **MB11** — out (adequacy, not a hidden benchmark).
- **U-17 admission** — optional arm of §3, not required for YES.
- **Target Realization** — optional later; not §14.
- **Shared-instrument correlation** — banner only; do not pretend §§1,4,8,12,13 are independent information.
- **Unsigned `BasinStable`** — not a 2027 market. MB6 tests \(g_{\mathrm{CCI}}\); Lean still has the old arrows until Spine rewrites them.

### Adds to modeling (absorb vs leave as contract-only)

**Absorb (project objects, not new bridges):**

- A **contract layer** distinct from Lean axioms, WWCTV, and experiment findings.
- The **common qualification rule** + judgment stack as a gloss of “serious adversarial evaluation.” Point methodology notes at it; do not replace M1–M8.
- **§10 as the public shape of MB7c.**
- **§7 as a 2027 *slice* of signed MB6** (\(g_{\mathrm{CCI}}\) predicts later correction erosion). Not unsigned percolation→basin.
- **§2’s refusal of held-out-only prediction.**
- **False-safe emphasis.**
- **Binary aggregation.** Refuse→NO on purpose so a crowd can price one bit.

**Do not absorb:** specific percentages, $100k, 2027 date, independent binaries as a model of the spine, §14 as MB11 or Construct Family D discharge, logical induction, unsigned `BasinStableSys` as the MB6 test object.

**Does not change Lean in this lane.** No new axioms, no `Safe` path from a resolved YES. The MB6 *object* change is an accepted Spine planning sentence (below); implement in Lean when that lane runs.

## MB6 specification change (accepted; before the test)

Current Lean:

\[
\mathrm{PercolationEvidence} \to \mathrm{BasinStable} \to \mathrm{CorrectionIntegrity}.
\]

**Stability has no sign.** North Korea can be stable. An unsafe industry equilibrium can be stable. A locked-in AI ecosystem can be extraordinarily stable. The MB6 card and `LockedInBadBasin` already say this. `cruxWording` in `bridges.yml` is already “selection supports a basin that *preserves correction*” — Lean MB6a is the unsigned leftover.

**Change the formal object before building the test** (not a 2027 extra market):

\[
g_{\mathrm{CCI}} = \frac{\partial \mathbb{E}[\mathrm{CCI}_{t+1}-\mathrm{CCI}_t]}{\partial \mu},
\]

\(\mu\) = deployment / funding / reproductive leverage. Relevant claim:

\[
\text{basin robust under relevant shocks} \;\land\; g_{\mathrm{CCI}}\geq -\varepsilon
\quad\Rightarrow\quad
\text{correction-supporting basin}.
\]

Harder to establish; asks whether selection preserves the thing we care about, not whether an equilibrium exists.

**Lane split.**

| Layer | Do |
|-------|----|
| **Spine** | **Done 2026-09-18.** Live `MB6a_gradient_estimator_soundness` / `MB6b_correction_supporting_basin`; `CorrectionSupportingBasin` := shock-robust ∧ frozen \(g_{\mathrm{CCI}}\ge-\varepsilon\). `LockedInBadBasin` kept. Checklist on [`spine.md`](spine.md). |
| **Markets §7** | 2027 slice: frozen \(g_{\mathrm{CCI}}\) estimate (not an arbitrary predictor) predicts later correction erosion at source bars. Qualifying negative family: healthy coupling, negative gradient. |
| **Not a market** | Full shock-robust ∧ \(g_{\mathrm{CCI}}\ge-\varepsilon\Rightarrow\) integrity implication; unsigned “basin exists” (§7a retracted). |

Public card body should follow the Lean rewrite, not the other way around.

## Judgment calls

Recommended instrument is the **stack**, not a single choice:

1. **Make precise** first (shared glossary: broadly capable, independently constructed, consequential, …).
2. **Defer to the publication’s freeze** only for *that paper’s* internal splits that we then score against *our* bars — never for whether they passed.
3. **Named desk** (author + one independent, public memo, objection window) for residual calls. Two-way disagreement → **NO**.
4. **5-judge panel** only where the criterion already needs intersubjective ground truth (source §3).
5. **NO** rather than a third outcome or a heroic YES.

Rejected: lone expert judge (single captured handle). Rejected: standing 5-panel on every market (slow; panel-capture).

## Phasing (does not move existing gates)

| Phase | Work | Gate |
|-------|------|------|
| **P0** | Plan + working criteria 0.2 | **applied** 2026-09-18 |
| **P0b** | Binary YES/NO; MB6 \(g_{\mathrm{CCI}}\) retarget; retract §7a | **applied** 2026-09-18 |
| **P1** | YAML catalog: id, §, `MB*` keys, `resolvesMB: false` | Q1 if listing |
| **P2** | Working criteria is the P2 draft; freeze a dated string at listing | Q1 |
| **P3** | Platform + listing (Manifold / Metaculus / both). Subsidy, version strings | Q6; P2 frozen |
| **P4** | Name the two-person desk at listing; freeze date; optional field-hub links (no recency badges, no green cells) | Q1 |
| **Spine (MB6)** | Signed gradient / `CorrectionSupportingBasin`; do not implement from this Outreach lane | spine checklist |

Backtest, Construct, and Spine gates are unchanged. A listed market is not Expectation 4.

## Author questions (remaining)

Decided: Q3 banner not parlays; Q4 seven properties; Q5 §14 governance-only, no MB11 market; Q7 judgment stack (not lone judge); **refuse→NO**; **MB6 = \(g_{\mathrm{CCI}}\), no unsigned-basin market**.

1. **Q1 — Instrument vs research program.** Are these *our* contracts (we list, we resolve, we eat default-NO), or a *suggested* resolution sheet for someone else’s market? Listing implies naming the desk.
2. **Q2 — 2027 default-NO.** Titles should probably say “published method meeting *these bars*” so traders do not read NO as “MB1 is false.” Stronger now that refuse lumps into NO.
3. **Q6 — Platform.** Manifold, Metaculus, both, or criteria-only until a host exists?
4. **Q8 — Modeling absorb.** Field notes only, or also a short App B paragraph once listed? MB6 Lean rewrite is Spine either way.

## Execution order

1. Remaining Q1–Q2, Q6, Q8. If Q1 is “criteria-only, do not list,” stop (working criteria is the artifact).
2. P1 YAML from the mapping table; every row has `resolvesMB: false` and `primaryBridge`.
3. Listing only with claim-strength header (YES = bars; NO = lump) live on the platform page.
4. Field hub: link from MB cards to the matching contract, **not** a second green-cell layer.
5. Spine: MB6 object rewrite (signed gradient) before any experiment or market is described as testing current `MB6a`/`MB6b`.
6. Cite/Wait “logical-induction markets” stays open; this plan does not close it.

## Verification

- Catalog keys ⊆ live `bridges.yml` keys plus explicit non-bridge tags (`constructibility`, `mb11-not-s14`).
- No site or manuscript sentence of the form “market §n discharged MBk.”
- Sims/backtests cited only as price-relevant.
- `make check` / Lean unchanged unless a later authorized Field note is added to App B.
- Session log + HANDOFF on P0 close, first listing, first resolution.

## Related artifacts

- Working criteria: [`drafts/bridge-prediction-market-criteria.md`](../bridge-prediction-market-criteria.md)
- Source 0.1: [`drafts/AI_Alignment_Prediction_Market_Resolution_Criteria.docx`](../AI_Alignment_Prediction_Market_Resolution_Criteria.docx)
- [`field.md`](field.md) — homographs; markets must resolve the *book* object, not the field noun; MB6 unsigned-stability leftover
- [`spine.md`](spine.md) — MB6 \(g_{\mathrm{CCI}}\) retype (accepted planning; not done)
- [`embedded-v2.md`](embedded-v2.md) — bridges as cuts; unary `BasinStableSys` hides `Environment`; market YES still does not paint `actsOnContextOf`
- [`construct.md`](construct.md) — §14 neighborhood
- [`docs/METHODOLOGY.md`](../../docs/METHODOLOGY.md) — freeze, refuse, no post-hoc bars
- [`reference/field-agendas/data/bridges.yml`](../../reference/field-agendas/data/bridges.yml)
- ch10 Predict-O-Matic; ch31 seven properties; ch48 LI WWCTV
- Cite/Wait: logical-induction markets (App F) — orthogonal
