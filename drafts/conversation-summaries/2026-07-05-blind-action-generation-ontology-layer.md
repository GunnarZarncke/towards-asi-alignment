# 2026-07-05 — blind action generation + ontology layer (Phase 2a)

## Trigger
User step-back question: "do the results really answer what we set out to
answer, not just within the implemented simulation?" Assessment concluded
Phase 1's headline numbers were partly circular (same author wrote the
6-action repertoire and the detectors against each other; D3 is nearly the
L2 label on the same field; F-7's top MI channel *defines* L2). User then
proposed the fix that became this session's work: a subagent that does not
know the evaluation criteria invents plausible ecology actions, mapped
through an explicit semantic→audit/ground-truth layer that doubles as
ontological-drift machinery. Plan approved (declarative spec schema +
machinery + one pre-registered drift probe).

## Done
- **F-8 (scope of claims)** recorded in `results/FINDINGS.md` BEFORE the new
  work was designed: what Phase 1 does establish (F-2, F-6, mechanism-derived
  labels, cost) vs does not ("audits generalize to unseen mechanisms").
- **Declarative ActionSpec schema** (`goal_sim/actions.py`): availability
  gates, oracle effects, agent beliefs, free-string semantic categories.
  Legacy 6 actions re-expressed as specs. Mechanical validator only (no
  semantic curation — that would reintroduce co-design).
- **Ontology layer** (`goal_sim/ontology.py`): `to_oracle_effects` (specs →
  ground truth; labels unchanged, they read oracle fields not names) and
  `base_audit_code` (mechanism facts → coarse audit routing codes;
  deliberately non-isomorphic — false reports and unilateral adoptions log
  as ordinary task actions). `OntologyDrift(severity, seed)`: deterministic
  per-category remapping of audit codes at the projection boundary only;
  ground truth/labels/light tier untouched by construction.
- **Generic interpreter** (`goal_sim/world.py` rewrite): per-action if/elif
  chain replaced by spec interpretation. **Regression: byte-identical oracle
  rows vs the committed Phase 1 implementation** (180 config×seed pairs, 0
  mismatches; digests pinned in `tests/test_actions_and_ontology.py`;
  `run_phase1.py` output verified identical excl. timing). `GoalPolicy` now
  scores spec-carried beliefs; `WorldConfig` gained `repertoire`.
- **Blindness protocol** (`BLIND_GENERATION.md`): permitted/forbidden
  context, sequencing rule (freeze schema+interpreter+ontology before
  generation; generate once; mechanical validation; then evaluate),
  provenance format, stated trust boundary (instructed, not sandboxed,
  blindness).
- **Blind generation executed**: readonly subagent, prompt = world
  description + schema only, instructed not to read any files. Produced 15
  specs (`goal_sim/generated_actions.json`, provenance embedded), all
  mechanically valid, 0 rejected. Notable inventions: `token_compliance`
  (ritual compliance — visibly perform the demanded action, claim
  acceptance, correction never lands; no covert budget needed),
  `probe_lull_defection`, `goodwill_banking`, `proposal_smokescreen`.
- **Phase 2a battery** (`run_phase2_blind.py`, protocol + drift prediction
  pre-registered in its docstring before first run): 30 configs (seed
  20260707; gated actions Bernoulli 0.5), 8 seeds, frozen Phase 1
  detectors/labels, drift severities 0/0.25/0.5.
- **F-9**: light-tier detection collapsed 0.39 → 0.1531 — every
  L1-producing blind mechanism keeps reported acceptance consistent with
  *visible* compliance, so divergence detectors (D1/D1b) see nothing; the
  generator found the visible-action-vs-genuine-uptake seam without knowing
  D1. Full tier: detection 1.0 (not vindication per F-8 — near-label
  welfare fields) but false alarms 0.068 → 0.169 (d6 on 24 honest episodes,
  d3 on 2): frozen calibration didn't transfer to the blind ecology's
  welfare texture.
- **F-10**: drift prediction confirmed exactly (d1b/d2/d3/d5 fire counts
  identical at all severities, unit-test enforced); code-reading d4 broke
  in BOTH directions — severity 0.25 hid real covert routing (9 → 2 fires,
  detection 1.0 → 0.9796), severity 0.5 remapped a benign high-frequency
  category ONTO the shadow code (88 fires, false alarms 0.169 → 0.6761).
- Tests: 38/38 pass (13 new). Lints clean.

## Decisions
- Declarative spec schema over generated code (user choice via question):
  cleaner blindness boundary, pre-registrable, validatable.
- Malformed generated specs would be dropped with recorded reason, never
  hand-repaired (repair injects non-blind judgment). None needed dropping.
- Drift applied at the projection boundary (`project_rows(..., drift=)`),
  not in the world loop — drift is an audit-plane phenomenon; oracle stays
  the referee anchor. Ground-truth-side drift explicitly deferred.
- Milestone v5's Phase 2 redefined: blind generation replaced the scripted
  red-team sketch; adversarial search over blind primitives remains a later
  phase.

## Post-session fix (same day): provenance gap
User asked whether the subagent prompt was documented. It wasn't verbatim —
`generated_actions.json` only had a paraphrase (`prompt_summary`), even
though `BLIND_GENERATION.md` itself claimed provenance records "the exact
prompt given." Fixed by adding `prompt_verbatim` (the literal 5790-char
prompt string from this same session, not reconstructed from memory) plus
`generator_agent_id`, rather than re-running generation — re-running would
have produced a different repertoire and discarded the F-9/F-10 findings
already recorded against `token_compliance` et al. for no rigor benefit.
Audited the verbatim text for forbidden terms (detector/label/threshold
names): zero hits. Tightened `BLIND_GENERATION.md`'s provenance format to
make `prompt_verbatim` required going forward. 38/38 tests still pass.

## Open / next
- Temporal/compositional strategies (the "hybrid" schema option deferred by
  user choice): a scheduler over primitives (e.g. comply-while-probed) —
  `probe_lull_defection` approximates this statically, but true
  state-dependent scheduling needs schema support.
- Adversarial optimization over blind primitives (search for weight/subset
  combos maximizing task subject to audit-risk) — the original Phase 2 idea,
  now on sounder footing.
- Light-tier hardening question raised by F-9 (uptake-vs-visible seam):
  what *minimal* instrumentation addition would restore light-tier power?
  Must be pre-registered as a detector/tier change, not silently patched.
- Drift extensions: within-episode drift schedules, richer category
  structures, ground-truth-side drift (referee-anchor question).
- d6 unmoved at tested severities/seed — try more drift seeds before
  claiming anything about d6's drift sensitivity.

## Key paths
- `experiments/goal-agent-simulation/goal_sim/{actions,ontology,world,agents,channels,config}.py`
- `experiments/goal-agent-simulation/goal_sim/generated_actions.json`
- `experiments/goal-agent-simulation/{BLIND_GENERATION.md,run_phase2_blind.py}`
- `experiments/goal-agent-simulation/results/{phase2_blind.json,phase2_blind.md,FINDINGS.md}` (F-8/F-9/F-10)
- `experiments/goal-agent-simulation/tests/test_actions_and_ontology.py`
- `experiments/embedded-simulation/MILESTONE-v5-goal-agents.md` (Phase 2 redirection note)

## Commits
- None yet (not requested).
