# Field — crux divergence plan

Status: **Field lane** — follow-up to field matrix noun rename (2026-08-02). Track 1 locked reader-facing nouns in [`reference/field-agendas/data/bridges.yml`](../../reference/field-agendas/data/bridges.yml) and [`metadata/bridges.yml`](../../metadata/bridges.yml). This plan covers where **agendas share a label but not a formal object**, and what to do about it in Lean + manuscript.

## Goal

For each `MB*` column, make explicit:

1. **Field objects** — what different agendas actually certify or argue about under the same noun.
2. **Book predicates** — what the Lean bridge antecedent/consequent pair actually bets.
3. **Gap handling** — field-local Lean models + interface counterexamples where load-bearing; App B / chapter prose where claim strength must change.

**Non-goals:** renaming spine `MB*` axioms for synonymy; collapsing glossary homographs; adding `MB12` without a distinct conclusion not already represented; painting `actsOnContextOf` as coverage-matrix cells; putting the 2.0 cycle claim on the v1 six.

Embedded-system reading (bridges as cuts; capacity vs structural field construction): [`embedded-v2.md`](embedded-v2.md). Grain map: [`reference/embedded-v2-grain-map.md`](../../reference/embedded-v2-grain-map.md).

Precedent: [`drafts/attic/field-claim-formalization-and-bridge-review-plan.md`](../attic/field-claim-formalization-and-bridge-review-plan.md) (field-local first, interfaces + defeaters, no `Safe` bypass).

## Priority divergences

### P1 — MB4 / MB4a vs field “corrigibility”

| | |
|---|---|
| **Field** | MIRI/CHAI shutdown-button utility + anti-naturality; Christiano dynamical basin; RLHF obedience; CIRIS deferral/shutdown ops |
| **Book** | `MB4`: correction process self-preservation; `MB4a`: measured-path legitimacy + anti-capture (separate bridge) |
| **Lean today** | `Field/Corrigibility.lean`, `Field/Finite/OffSwitchGame.lean`, `Correction.lean` (`MB4a_measured_path_legitimacy`) |
| **Work** | Finite models separating MIRI interruptibility vs Christiano basin vs CCI trajectory; App B notes already split MB4/MB4a — extend with explicit “same word, three objects” table; CIRIS composite-path bypass as `MB4a` defeater cite |

### P1 — MB5 (Tiling) vs MB10 (Successor Gaming)

| | |
|---|---|
| **Field** | Tiling / Vingean reflection / ontology identification; deceptive alignment / alignment faking (usually under inner alignment) |
| **Book** | `MB5`: transport composes to `SuccessorSafe`; `MB10`: green audit signature not forgeable |
| **Lean today** | `Forgeability.lean` (`forgeability_gap` counterexample); `Successors.lean` |
| **Work** | App B + matrix legend already split; manuscript WWCTV in ch08/ch31/ch43 should forward-ref MB10 noun; optional `Field/Finite/SuccessorAuditForgeability.lean` toy beyond existing counterexample |

### P1 — MB9 (Grounding Drift) vs GSAI specification coverage

| | |
|---|---|
| **Field** | Open-world completeness / omitted phenomena (GSAI); conservativity / no silent gaps (book) |
| **Book** | `MB9_grounding_certificate_soundness` → `GroundingViable` (conservative abstraction) |
| **Lean today** | `Field/Finite/Nonrealizability.lean` as MB1/MB9 ambient cousin |
| **Work** | App B MB9 notes: state weakened demand explicitly; interface record from misspec model → `GroundingCertificate` (deferred in field-claim plan) |

### P2 — MB2 (Value Learning) vs ELK / PreDCA / pointing

| | |
|---|---|
| **Field** | ELK = latent-readout slice; CIRL = scalar assistance game; PreDCA/QACI = peer outer targets |
| **Book** | `MB2` bundle identifiability; `MB3` bearer import (field often folds together) |
| **Lean today** | `Field/ELK.lean`, `Field/Finite/*` value-learning toys |
| **Work** | Strengthen separation theorems (readout ⇏ correction; bundle ⇏ bearer); glossary cross-links from matrix legend |

### P2 — MB6 (Goodhart Selection) vs Demski selection

| | |
|---|---|
| **Field** | Goodhart-as-selector / gradual disempowerment vs Demski search-vs-control inside one optimizer |
| **Book** | `MB6a`/`MB6b` basin + correction; deployment leverage / `Fit_E` typed form. **Accepted (2026-09-18):** unsigned `BasinStable` is the wrong object; retype around \(g_{\mathrm{CCI}}\) / correction-supporting basin before tests. [`bridge-prediction-markets.md`](bridge-prediction-markets.md), [`spine.md`](spine.md) P2 |
| **Lean today** | Selection env predicates in spine; no Demski finite model; live objects `MB6a_gradient_estimator_soundness` / `MB6b_correction_supporting_basin` (`CorrectionSupportingBasin`, signed \(g_{\mathrm{CCI}}\`); unsigned `BasinShockRobust` is not the consequent) |
| **Work** | One paragraph homograph guard in ch34 + App B; optional finite Demski vs deployment-selection contrast module (catalog only unless it interfaces to the *new* MB6 object, not unsigned `BasinStableSys`) |

### P2 — MB7 vs MB10 naming history

| | |
|---|---|
| **Field** | “Deceptive alignment” / scheming / alignment faking → usually MB7 column empirics |
| **Book** | MB7 = access/filter/cost-of-faking; MB10 = successor checklist forgeability |
| **Work** | Field hub legend (done Track 1); evidence catalog tags review so Redwood ev-13 etc. stay on correct columns; App B MB10 row fieldCrux sync when manuscript pass runs |

### P3 — MB11 (Deployment Safety) vs regret / GSAI closure

| | |
|---|---|
| **Field** | Safety-case adequacy; GSAI proof closure; Kosoy regret bounds |
| **Book** | `MB11_safety_case_adequacy` only arrow to `Safe`; regret = side channel (`RegretSafety.lean`) |
| **Lean today** | `Field/Finite/RegretSafety.lean`, `Certification.lean` |
| **Work** | App B MB11 notes + field-index do-not-infer (done); optional `DeploymentHarmBounded` leaf if book adopts expected-harm language (deferred — [`spine.md`](spine.md) P4) |

### P3 — MB7d (Acausal Coordination)

| | |
|---|---|
| **Field** | FDT, ECL, program equilibrium — sparse matrix evidence |
| **Book** | Inferential-coupling detector validity |
| **Work** | Manuscript ch48 already homes acausal load; field-local detector toy if eval line expands |

### P3 — MB8 (Extrapolated Volition)

| | |
|---|---|
| **Field** | CEV process philosophy vs CBV/QACI/PreDCA peer endpoints |
| **Book** | Legacy `MB8_cev_process_convergence`; live path MB4/MB4a |
| **Work** | Keep secondary labeling in App B; no merge with MB2/MB3 outer targets |

## Bridge cuts and field construction (2.0 reading)

The coverage matrix remains **evidential**. Institutional variables are often *inside* the causal subgraph a bridge compresses, not a second DAG.

**Cut method** (analysis only; no new `MB*`): for each live bridge, name what the unary form silently holds fixed. First inventory: memo §4 / [`embedded-v2.md`](embedded-v2.md). Families: MB1/2/7/9 epistemic; MB4/4a authority and correction; MB3/5/10 temporal/inheritance; MB6 ecological; MB11 deployment.

**Capacity vs structural field construction.** Explicit on [`roster.yml`](../../reference/field-agendas/data/roster.yml) as `fieldConstruction`: `none` | `capacity` | `structural` | `mixed`. Capacity stays upstream of the matrix. Structural acts on context of MB4a/MB6/MB7/MB10/MB11 and does not discharge those bridges. Coverage matrix stays evidential — no `actsOnContextOf` cells. Construction/convergence is presented on the lifecycle cycle, not as matrix paint.

**Lifecycle.** Cycle `specify → construct → identify → certify → act/refuse`. **Preserve** is a property of repeating that cycle (stability or convergence), not a fifth equal stage. Bridges tagged `preserve` are cycle-property constraints. Source: [`lifecycle.yml`](../../reference/field-agendas/data/lifecycle.yml).

## Execution order (suggested)

1. **Inventory pass** — export `bridges.yml` `fieldAgree`/`fieldDiffer` into a checklist; mark which have glossary headwords vs need new entries.
2. **App B notes pass** — P1 divergences first (MB4/MB4a, MB5/MB10, MB9); align `fieldCrux` strings with `cruxWording` (partially done via site cards).
3. **Lean field-local pass** — only where a finite model or interface record is missing (P1 MB4 homograph, P1 MB9 grounding interface, P2 ELK separation already partial).
4. **Manuscript WWCTV** — forward refs for MB10 noun, MB6 Demski homograph, MB9 conservativity vs GSAI completeness.
5. **Evidence catalog audit** — verify bridge tags on ev rows match noun intent (especially MB7 vs MB10).

## Checklist

- [ ] Field crux divergence — inventory → App B notes → field-local Lean (no new `MB*`)
- [x] Ngo reverse column — site card [What this map misses](../../site/src/content/cards/what-tsa-fails-to-represent.md) (2026-09-08): grant-then-residual, two paragraphs per agenda. YAML-per-agenda field and App B disclaimer still optional; not the 2026-08-25 ontology-homograph section.
- [ ] MB7a–c optional field-standard noun aliases (keep MB7 split)
- [ ] App B vs merged field-agenda row names (secondary prose)
- [ ] International AI Safety Report → Field when read
- [x] Lifecycle cycle on field hub; Preserve as cycle property ([`lifecycle.yml`](../../reference/field-agendas/data/lifecycle.yml), 2026-09-18)
- [x] Capacity vs structural on roster (`fieldConstruction`); no matrix paint
- [ ] Bridge-cut inventory: one paragraph or table per live MB (silently fixed context); start MB6 and MB11

## Verification

- Matrix legend + [`bridges.yml`](../../reference/field-agendas/data/bridges.yml) stay in sync.
- App B crosswalk `fieldCrux` matches bridge card `fieldCrux` for MB1–MB10.
- No prose claims “field X solves MBY” without naming which object X certifies.
- Lean: new field modules do not add axioms reaching `Safe` without `MB11`.

## Related artifacts

- [`embedded-v2.md`](embedded-v2.md) — coupled-system reading; `evidenceFor` ≠ `actsOnContextOf`
- [`bridge-prediction-markets.md`](bridge-prediction-markets.md) — 2027 binary contracts on live `MB*`; YES ≠ discharge; not a second green-cell layer
- [`alignment-crux-map.md`](alignment-crux-map.md) — funder-facing job map + outsider tests (Field lane grant)
- [`cousin-product-comparison.md`](cousin-product-comparison.md) — spec sheet for what programs *ship* (Start Here, not Field hub)
- [`iliad-communal-canon.md`](iliad-communal-canon.md) — Iliad lessons (concept)
- [`lw-wiki-tags.md`](lw-wiki-tags.md) — offer TSA object-splits to the LW wiki (Arbital fold-in)

- [`reference/field-agendas/data/bridges.yml`](../../reference/field-agendas/data/bridges.yml) — nouns + crux wording
- [`reference/field-agendas/inter-agenda-term-glossary.md`](../../reference/field-agendas/inter-agenda-term-glossary.md) — homograph headwords
- [`drafts/attic/field-claim-formalization-and-bridge-review-plan.md`](attic/field-claim-formalization-and-bridge-review-plan.md)
