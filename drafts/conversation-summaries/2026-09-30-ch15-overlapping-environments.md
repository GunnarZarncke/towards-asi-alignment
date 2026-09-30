# 2026-09-30 — Ch. 15 overlapping environments

kind: new-work
uptake: local

## Trigger
Assess the site note on Ch. 15 ("people are different and live in different overlapping environments — what does that do to the model?"): does it affect other chapters and the Lean spine, does Ch. 15 need restructuring, and if the changes are limited, make them.

## Assessment
- The point is cross-cutting but already partly carried: Ch. 16 (culture translation map, hierarchical `B`), Ch. 17 (local charts over context regions), Ch. 20 (per-human geometries `G_B^h`, standing rules). Missing: Ch. 15 is written for one agent and never says so; Ch. 17/21 sample-complexity prose implicitly assumes one demonstrator or one shared geometry.
- Lean: `MB2Crux` is single-experiment on `PolicyProfile`; `P17_same_value_words_not_same_bearer_map` already carries the structural counterexample (same label, different bearer map). No Lean change needed; optional finite population toy noted.
- No restructure: a short new section in Ch. 15 plus one-to-three-sentence back-links in Ch. 16/17/20/21 make it a thread, not an isolated paragraph.

## Done
- content: Ch. 15 new section `sec:overlapping-environments-ch15` (Different People, Overlapping Environments) after Social Correction: per-person compression, environment sets `E_i` with partial overlap, shared coordinates rest on shared loops, same label ≠ same local policy map or bearer map, pooling across people is not plain variance reduction; forward pointers to Ch. 16/17/20/21. WWCTV bullet and one summary sentence added.
- content: **Follow-up.** Aligning to the pool but not to each person is a failure mode (conformance pressure): off-overlap loops lose their occasions and go quiet, and the pooled audit scores the convergence as success. Added to the Ch. 15 section, plus Ch. 20 (pooled geometry is not the aggregate), Ch. 21 (deploying the pooled model), and a Ch. 46 channel `sec:pool-conformance-ch46`. Second WWCTV bullet: the claim weakens if off-overlap loops stay behaviorally available.
- content: Ch. 17 — local charts indexed by person as well as domain; `m_total` prices one demonstrator, `\mathcal E` must include overlap structure.
- content: Ch. 21 — paragraph after the `K ≪ n ≪ D` window on pooled demonstrators; `\leanspine{counterexample}{P17...}`.
- content: Ch. 16 — hierarchical `B` layers separated by how far the training environments are shared. Ch. 20 — `G_B^h` estimated on each human's own environments.
- bookkeeping: `drafts/plans/spine/spine.md` optional P3 population/overlap toy. Fixed pre-existing broken link in `drafts/lw-bridges-section.md` (→ `outreach/`).
- bookkeeping: `make check` — Markdown link check passed; structure/citations/claim spine pass (concept-graph audit files regenerated). `npm run sync:chapter-cards` — Wrote 56 chapter cards.

## Decisions
- No named credit in the text; the point is stated as a modeling consequence.
- Kept notation minimal: `E_i` and `B^{(i)}` (the latter already in Ch. 15 Social Correction); no new formalism.

## Open / next
- Optional Lean toy (spine.md P3): two-demonstrator pooled `PolicyProfile`s identify shared salience but not per-person residual.
- Decision-block plain-language pass from the site-notes plan remains open.

## Key paths
- `chapters/ch15-values-compressed-control.tex` (`sec:overlapping-environments-ch15`)
- `chapters/ch17-low-dimensional-value-learning.tex`, `chapters/ch21-reward-to-bundle-inference.tex`
- `formal/AlignmentProofSpine/Bundles.lean` (`P17`), `MB2Identifiability.lean`

## Commits
- (filled in at session end)
