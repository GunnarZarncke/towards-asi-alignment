# Field — crux divergence plan

Status: **Field lane** — follow-up to field matrix noun rename (2026-08-02). Track 1 locked reader-facing nouns in [`reference/field-agendas/data/bridges.yml`](../../reference/field-agendas/data/bridges.yml) and [`metadata/bridges.yml`](../../metadata/bridges.yml). This plan covers where **agendas share a label but not a formal object**, and what to do about it in Lean + manuscript.

## Goal

For each `MB*` column, make explicit:

1. **Field objects** — what different agendas actually certify or argue about under the same noun.
2. **Book predicates** — what the Lean bridge antecedent/consequent pair actually bets.
3. **Gap handling** — field-local Lean models + interface counterexamples where load-bearing; App B / chapter prose where claim strength must change.

**Non-goals:** renaming spine `MB*` axioms for synonymy; collapsing glossary homographs; adding `MB12` without a distinct conclusion not already represented.

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
| **Book** | `MB6a`/`MB6b` basin + correction; deployment leverage / `Fit_E` typed form |
| **Lean today** | Selection env predicates in spine; no Demski finite model |
| **Work** | One paragraph homograph guard in ch34 + App B; optional finite Demski vs deployment-selection contrast module (catalog only unless it interfaces to `BasinStableSys`) |

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

## Execution order (suggested)

1. **Inventory pass** — export `bridges.yml` `fieldAgree`/`fieldDiffer` into a checklist; mark which have glossary headwords vs need new entries.
2. **App B notes pass** — P1 divergences first (MB4/MB4a, MB5/MB10, MB9); align `fieldCrux` strings with `cruxWording` (partially done via site cards).
3. **Lean field-local pass** — only where a finite model or interface record is missing (P1 MB4 homograph, P1 MB9 grounding interface, P2 ELK separation already partial).
4. **Manuscript WWCTV** — forward refs for MB10 noun, MB6 Demski homograph, MB9 conservativity vs GSAI completeness.
5. **Evidence catalog audit** — verify bridge tags on ev rows match noun intent (especially MB7 vs MB10).

## Checklist

- [ ] Field crux divergence — inventory → App B notes → field-local Lean (no new `MB*`)
- [ ] Ngo reverse column (parked): one “what TSA fails to represent of *their* crux” line per agenda YAML; App B disclaimer that the crosswalk is translation, not completeness. Not the 2026-08-25 ontology-homograph section.
- [ ] MB7a–c optional field-standard noun aliases (keep MB7 split)
- [ ] App B vs merged field-agenda row names (secondary prose)
- [ ] International AI Safety Report → Field when read

## Verification

- Matrix legend + [`bridges.yml`](../../reference/field-agendas/data/bridges.yml) stay in sync.
- App B crosswalk `fieldCrux` matches bridge card `fieldCrux` for MB1–MB10.
- No prose claims “field X solves MBY” without naming which object X certifies.
- Lean: new field modules do not add axioms reaching `Safe` without `MB11`.

## Related artifacts

- [`reference/field-agendas/data/bridges.yml`](../../reference/field-agendas/data/bridges.yml) — nouns + crux wording
- [`reference/field-agendas/inter-agenda-term-glossary.md`](../../reference/field-agendas/inter-agenda-term-glossary.md) — homograph headwords
- [`drafts/attic/field-claim-formalization-and-bridge-review-plan.md`](attic/field-claim-formalization-and-bridge-review-plan.md)
