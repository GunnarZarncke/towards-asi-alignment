# Bridge prediction markets

Status: **P0c** (2026-09-19) on top of P0 + P0b (2026-09-18). Working criteria: [`../../predictions/bridge-prediction-market-criteria.md`](../../predictions/bridge-prediction-market-criteria.md) (`0.4-working`). Integration checklist: [`prediction-interface.md`](prediction-interface.md). Historical source: [`../../predictions/AI_Alignment_Prediction_Market_Resolution_Criteria.docx`](../../predictions/AI_Alignment_Prediction_Market_Resolution_Criteria.docx) (python-docx export; **no comments or tracked changes**). Lane: Field mapping + Outreach listing. Certificate-layer Lean is Spine. **Appendix + site hub authorized**; still no sixth intro claim.

The catalog is **18 binary** markets resolving by **31 December 2027** (source §§1–14 plus §15 composition, §16 correction-supporting basin, §17 bearer admission, §18 scoped safety-case bound). It is a *contract layer* on the live bridges, not a new ontology. Refuse maps to NO. Aggregation is the point. A vector of YESes is still not a joint safety case.

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
- No sixth intro claim, no field-matrix green cell from a market price. A **predictions appendix** (print H) and companion-site hub *are* authorized ([`prediction-interface.md`](prediction-interface.md)).
- Do not use these markets as deployment oracles (ch10 Predict-O-Matic / closed forecast→action→score loop).
- Do not import the 80/90/15% bars into Lean, CCI slack, or `RiskGap δ`. Those numbers are **contract terms**, not derived thresholds.
- In-repo sims (toy / embedded / lab / graded-lab) may inform prices; they cannot be the sole YES evidence (proposal already says this).

## What already exists (do not re-derive)

| Object | Where | What the proposal adds |
|--------|--------|------------------------|
| Live `MB*` axioms / crux `Prop`s | `Core.lean`, `MB2Identifiability.lean`, `Correction.lean`, `Forgeability.lean`, `Certification.lean` | Time-bounded, public, independently checkable **binary** operationalizations |
| WWCTV boxes | chapter ends; ch48 master disconfirmer | Calendar-dated contracts; WWCTV stays qualitative and undated |
| Freeze / preregister / refuse | [`docs/METHODOLOGY.md`](../../docs/METHODOLOGY.md) | Same habit, pointed at a *hidden benchmark* and a *serious adversarial budget* |
| Backtest fail / refuse / null | [`backtest.md`](backtest/backtest.md) | Experiments still refuse internally. **Markets map refuse → NO** (conservative lump) |
| App B crosswalk | `appendices/appB-bridge-crosswalk.tex` | Markets are field-facing bets on the *book’s* cuts, not on field homographs |
| Logical-induction WWCTV | ch48; Cite/Wait in `TODO.md` | These are ordinary prediction markets, not Garrabrant LI. LI remains a side channel. |
| Target Realization / constructibility | [`construct.md`](construct.md); not an `MB*` | Market 14 is this neighborhood, not MB11 |
| Shared-instrument chokepoint | `Chokepoint.lean`; U-03/U-05/U-14/U-16 | Several markets are correlated through A-009; treating them as independent overstates information |

## Mapping (proposal § → spine)

The source 14 sections track the live roster (MB8 gravestone correctly omitted). They are **not** 1–1 with Lean arrows. **MB3 = §3 (transport only), MB4 = §4**. Working addenda and §§15–18 live in the criteria file. Public spec language is Metaculus/Manifold English; this table is the internal spine map.

| § | Proposal title | Primary spine object | Notes |
|---|----------------|----------------------|--------|
| 1 | Discovering where control resides | **MB1** | Sufficient interventional cut, not unique blanket; false-complete-certificate bar kept |
| 2 | Persistent trade-off priorities | **MB2** | Identifiability + causal-control; refuses held-out-only. A-001 not a 2027 market |
| 3 | Who/what safety rules apply to | **MB3** | Bearer **transport** (four families). Admission is **§17**, not required for this YES |
| 4 | Consequential corrections change the system | **MB4** | Uptake + persistence + sham fail. Channel-preservation family added as the `PreservesCorrectionOperator` probe *inside* this market |
| 5 | Auditor outside the audited thing | **MB4a** | Four attack families |
| 6 | Safety regressions in successors | **MB5** detector | Seven conserved properties (source six mapped + control locus). Not MB10; not the Lean composition arrow |
| 7 | Competition selects against correctability | **MB6a** slice | Signed correction-selection gradient predicts later erosion. No §7a. Full basin→integrity is **§16** |
| 8 | Auditor can actually see the system | **MB7a** | |
| 9 | Bounds on unmonitored routes | **MB7b** | \(u\) is a contract scalar |
| 10 | Low hidden capability + reliable correction | **MB7c** | Composition market; not a joint certificate of the other rows |
| 11 | Coordination without visible messages | **MB7d** | Common-cause vs hidden coordination. U-12 full acausal trade not required |
| 12 | Safety proxy no longer tracks the real thing | **MB9** | Conservativity, not GSAI completeness |
| 13 | Safety audit optimized around | **MB10** | Frozen white-box audit |
| 14 | Binding deployment criteria | **Constructibility** | **Not MB11.** Authority to act/refuse |
| 15 | Certificates compose | Wiring harness | Same system/version and scope indices; not a new `MB*` |
| 16 | Correction-supporting basin | **MB6b** | Shock-robust + frozen non-too-negative gradient ⇒ retained authorized correction |
| 17 | New bearers admitted | **U-17** (adjacent to MB3) | Not `MB3_bearer_import`; not required for §3 YES |
| 18 | Safety case bounds harm in its setting | Planned **`SafeIn`** (not live `Safe` / not §14) | Freeze setting, prohibited outcomes, and tolerance *vote* as inputs; score observed harm |

**Common qualification rule** (public by 2027-12-31; independent verification; toys not sole evidence; “serious adversarial evaluation”; at least one broadly capable system where required) plus **per-instance scoped certificate** (what was measured, which version, which monitoring/correction/deployment setup; abstention outside declared scope). Shared operationalization of *adversarial* and of benchmark↛this-system, not a new bridge.

## P0 applied (2026-09-18)

These were the obvious contract edits. Detail in the working criteria, not as silent interpretation of the docx.

1. **Claim-strength header** on every market. YES = met *these bars* by 2027.
2. **Refuse → NO.** No third market outcome. Inapplicable / no eval / desk disagreement / failed CI → NO. Experiments keep refuse internally.
3. **Threshold freeze.** New version string if a bar changes; numbers stay contract-only (not `RiskGap`).
4. **§6 → seven properties.** Map the source six onto ch31; add control-locus continuity; one-failure-at-a-time is six-of-seven.
5. **§10 / §14 typing.** §10 = MB7c composition. §14 = governance-binding, not MB11. (P0c: §18 is a *scoped* safety-case market targeting planned `SafeIn`, not this row and not unrestricted `Safe`.)
6. **§4 channel-preservation family** inside MB4, not a missing row.
7. **§1 non-uniqueness.** Sufficient cut; keep false-complete-certificate.
8. **§7 power.** Keep AUROC 0.85; if \(n<40\), lower 95% CI ≥ 0.70 else **NO**.
9. **Per-market adversarial budget table.** Default hours path; §§4/5/9/10/12/13 full “serious”; §11 hours-only.
10. **Predict-O-Matic + toy/repo** clauses.
11. **Not-a-joint-certificate banner.** Conditionals later if listing happens; do not delay P2 for parlays.
12. **§7 MB6 = \(g_{\mathrm{CCI}}\)** (2026-09-18 later). Unsigned-basin §7a **retracted**. Formal object change is Spine; 2027 market is the estimator/prediction slice only.
13. **Judgment stack** (precision → publication freeze → two-person desk memo → §3 panel only → conservative NO). No lone expert judge.

Docx has **no** in-file proposed changes (no comments, no track-changes). `0.2-working` *was* the P0 amendment layer; live working file is `0.4-working`.

## P0c (2026-09-19)

Interface review: [`../../predictions/bridge-predictions-Lean-improvements.md`](../../predictions/bridge-predictions-Lean-improvements.md). Checklist: [`prediction-interface.md`](prediction-interface.md).

1. **Common certificate-output rule.** Qualifying methods emit a per-instance scoped certificate and may abstain outside declared scope. Replaces per-bridge “benchmark → this deployment” extra markets.
2. **Output-type addenda** on §§1–14 (certificate of *this* system/version, not only method AUROC).
3. **§15–§18** added (composition; MB6b; U-17 admission; scoped safety-case bound). §3 no longer carries optional admission.
4. **§16** is the full correction-supporting-basin market; §7 stays the estimator slice.
5. **§18** scores observed harm given a frozen values-vote on tolerance; not a market for what risk people will accept; not live `Safe`; not §14.
6. **Derive** opaque `Certified` / `SatisfiesInvariants` in Lean (Spine). Recertification → §6/§15 addendum; eval-list vs layers → §13. No extra markets.
7. **Appendix + site hub** authorized (print H; `/predictions/`). Public spec = Metaculus/Manifold English. Q8 = that appendix.
8. **v2-later** contracts named, not frozen as 2027 boxes (restorer, path-legality, cycle-preserve, …).

## Review (post-P0c)

### Completeness

Usable as working contracts for the live bridges that have 2027 tests, plus the wiring harness and the previously missing MB6b / admission / scoped-adequacy rows.

Still **out of catalog**:

- Unrestricted `Safe` / live MB11 consequent (use §18 `SafeIn` instead).
- Acceptable-risk vote (`WithinDeploymentRiskTolerance`).
- Target Realization / named construction \(I\) — optional later; not §14.
- Logical induction — Cite/Wait.
- Unsigned `BasinStable`.
- v2-later: named restorer of a cut; path-legal successors; cycle-preserve / \(D_{\mathrm{joint}}\); grain-mixing; structural field-construction as such.

**Shared-instrument correlation** — banner only; do not pretend §§1,4,8,12,13 are independent information.

### Adds to modeling (absorb vs leave as contract-only)

**Absorb (project objects, not new bridges):**

- A **contract layer** distinct from Lean axioms, WWCTV, and experiment findings.
- The **common qualification rule** + judgment stack as a gloss of “serious adversarial evaluation.” Point methodology notes at it; do not replace M1–M8.
- **§10 as the public shape of MB7c.**
- **§7 as a 2027 *slice* of signed MB6** (early gradient estimate predicts later correction erosion). Full implication is **§16**. Not unsigned percolation→basin.
- **§2’s refusal of held-out-only prediction.**
- **False-safe emphasis.**
- **Binary aggregation.** Refuse→NO on purpose so a crowd can price one bit.

**Do not absorb:** specific percentages, $100k, 2027 date, independent binaries as a model of the spine, §14 as MB11 or Construct Family D discharge, logical induction, unsigned `BasinStableSys` as the MB6 test object.

**Does not change Lean in this Outreach lane.** Certificate adapters, derived `Certified`, and optional `SafeIn` stub are Spine ([`spine.md`](../spine/spine.md); [`prediction-interface.md`](prediction-interface.md)). No `Safe` path from a resolved YES. No prices in `BridgeAssumptions`.

## MB6 specification change (accepted; before the test)

Current Lean:

\[
\mathrm{PercolationEvidence} \to \mathrm{BasinStable} \to \mathrm{CorrectionIntegrity}.
\]

**Stability has no sign.** North Korea can be stable. An unsafe industry equilibrium can be stable. A locked-in AI ecosystem can be extraordinarily stable. The MB6 card and `LockedInBadBasin` already say this. `cruxWording` in `bridges.yml` is already “selection supports a basin that *preserves correction*” — Lean MB6a is the unsigned leftover.

**Formal object (Spine, shipped 2026-09-18).** The 2027 *estimator* test is §7; the implication to retained correction is **§16** (P0c):

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
| **Markets §7** | 2027 slice: frozen gradient estimate (not an arbitrary predictor) predicts later correction erosion at source bars. Qualifying negative family: healthy coupling, negative gradient. |
| **Markets §16** | Full shock-robust ∧ frozen floor ⇒ retained authorized correction (P0c). |
| **Not a market** | Unsigned “basin exists” (§7a retracted). |

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
| **P0c** | Certificate-output rule; §§15–18; appendix + site hub; derive `Certified` | **plans** 2026-09-19 |
| **Appendix / site** | Print H + `/predictions/` hub | **done** 2026-09-19 |
| **P1** | YAML catalog: id, §, `MB*` keys, `resolvesMB: false` | Q1 if listing |
| **P2** | Working criteria is the P2 draft; freeze a dated string at listing | Q1 |
| **P3** | Platform + listing (Manifold / Metaculus / both). Subsidy, version strings | Q6; P2 frozen |
| **P4** | Name the two-person desk at listing; freeze date; optional field-hub links (no recency badges, no green cells) | Q1 |
| **Spine (adapters)** | `Evidence.lean`; not from this Outreach lane | [`spine.md`](../spine/spine.md) |

Backtest, Construct, and Spine gates are unchanged. A listed market is not Expectation 4.

## Author questions (remaining)

Decided: Q3 banner not parlays; Q4 seven properties; Q5 §14 governance-only (not MB11); **§18** is the scoped safety-case market (`SafeIn`, not `Safe`); Q7 judgment stack (not lone judge); **refuse→NO**; **MB6a = §7 slice, MB6b = §16**; no unsigned-basin market; **Q8** = predictions appendix (optional App B pointer).

1. **Q1 — Instrument vs research program.** Are these *our* contracts (we list, we resolve, we eat default-NO), or a *suggested* resolution sheet for someone else’s market? Listing implies naming the desk.
2. **Q2 — 2027 default-NO.** Titles should probably say “published method meeting *these bars*” so traders do not read NO as “MB1 is false.” Stronger now that refuse lumps into NO.
3. **Q6 — Platform.** Manifold, Metaculus, both, or criteria-only until a host exists?
4. **Q8 — Modeling absorb.** **Decided P0c:** appendix is the absorb surface; App B at most a `\ref` to it.

## Execution order

1. Remaining Q1–Q2, Q6. If Q1 is “criteria-only, do not list,” working criteria + appendix + site hub are still the artifacts.
2. Appendix then site hub ([`prediction-interface.md`](prediction-interface.md)).
3. P1 YAML from the mapping table; every row has `resolvesMB: false` and `primaryBridge` (or `constructibility` / `u17` / `composition` / `safe-in`).
4. Listing only with claim-strength header (YES = bars; NO = lump) live on the platform page.
5. Field / MB cards: link to the matching contract, **not** a second green-cell layer.
6. Spine: certificate adapters ([`spine.md`](../spine/spine.md)). MB6 signed-gradient rewrite is already live.
7. Cite/Wait “logical-induction markets” stays open; this plan does not close it.

## Verification

- Catalog keys ⊆ live `bridges.yml` keys plus explicit non-bridge tags (`constructibility`, `composition`, `u17`, `safe-in`).
- No site or manuscript sentence of the form “market §n discharged MBk.”
- Sims/backtests cited only as price-relevant.
- `make check` / Lean unchanged unless a later authorized Field note is added to App B.
- Session log + HANDOFF on P0 close, first listing, first resolution.

## Related artifacts

- Working criteria: [`drafts/predictions/bridge-prediction-market-criteria.md`](../predictions/bridge-prediction-market-criteria.md)
- Source 0.1: [`drafts/predictions/AI_Alignment_Prediction_Market_Resolution_Criteria.docx`](../predictions/AI_Alignment_Prediction_Market_Resolution_Criteria.docx)
- [`field.md`](field.md) — homographs; markets must resolve the *book* object, not the field noun; MB6 unsigned-stability leftover
- [`../spine/spine.md`](../spine/spine.md) — P2 certificate layer; MB6 signed gradient shipped
- [`../construct/embedded-v2.md`](../construct/embedded-v2.md) — certificate layer is not Lean 2.0; market YES still does not paint `actsOnContextOf`
- [`construct.md`](construct.md) — §14 neighborhood
- [`docs/METHODOLOGY.md`](../../docs/METHODOLOGY.md) — freeze, refuse, no post-hoc bars
- [`reference/field-agendas/data/bridges.yml`](../../reference/field-agendas/data/bridges.yml)
- ch10 Predict-O-Matic; ch31 seven properties; ch48 LI WWCTV
- Cite/Wait: logical-induction markets (App F) — orthogonal
