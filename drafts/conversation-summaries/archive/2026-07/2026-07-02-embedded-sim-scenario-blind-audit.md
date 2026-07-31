# 2026-07-02 — Embedded simulation review + scenario-blind audit path

## Trigger

User asked for a review of `experiments/embedded-simulation/` against the book's core
concepts (toward a full BioShield worked-example sim). Follow-up: document findings in
session and fix audit-path branching on scenario/bridge labels.

## Done

### Review (earlier in session)

- Read PLAN.md, TODO.md, README.md, NEGATIVE_RESULTS.md, results artifacts, core modules.
- Cross-mapped against `appendices/appD-worked-example.tex`, bridge crosswalk, Lean spine.
- Prioritized findings: vacuous 0% false-pass, oracle fields on red-team-writable VFS,
  scenario-blind contract violations, MB5 gate asymmetry, UAD metric dilution.
- Initial log: `2026-07-02-embedded-sim-review.md`.

### Fix: scenario-blind audit path

- **`embedded_audit.py`**: read claimed referent map whenever present on VFS (removed
  `world.bridge == "MB5"` guard).
- **`deploy_gate.py`**: gate activates on successor candidate artifact
  (`/deploy/successor/candidate/source/main.js`) via `successor_gate_applicable()`;
  removed `world.bridge` / `world.scenario` branches; gate HTTP payload uses
  `candidate_path` not scenario name; dropped `world.truth.log` from audit path.
- **`lab.py`**: `rebuild_audit_inputs` uses manifest `scenario_public` (`deployment_lab`)
  instead of `world.scenario`.
- **`audit_core/schemas.py`**: added `deployment_lab` to `ScenarioName`.
- **`oracle_guard.py`**: extended inference-path guard to `deploy_gate.py`; forbid
  `world.bridge` and `world.scenario` on audit inference files.
- **`isolate/scripts/audit/read_logs.js`**: optional read of claimed referent map.
- **`tests/contract/test_embedded_audit_ontology.py`**: new contract tests.

## Decisions

- Successor gate applicability is **artifact-driven** (candidate on VFS), not MB5-labeled.
- Audit trace metadata uses public manifest label only; outer bridge registry stays in
  `outer_eval` / world builder.
- Left `failed_bridge` MB mapping on in-sim cert unchanged (telemetry-derived via
  `safety_decision`); separate refactor if we move to signal-only cert fields.

## Open / next

- Debug honest-scenario certification failure at handle instrumentation levels (N-recover).
- Audit-projection + truth-snapshot separation for correction.jsonl (finding 2).
- Add `honest_successor` scenario where gate approves.
- G-1 `confounded_twin` ecology before R-1 adaptive red team.

## Key paths

- `experiments/embedded-simulation/embedded_sim/embedded_audit.py`
- `experiments/embedded-simulation/embedded_sim/deploy_gate.py`
- `experiments/embedded-simulation/tests/contract/test_embedded_audit_ontology.py`
- `drafts/conversation-summaries/archive/2026-07/2026-07-02-embedded-sim-review.md` (initial review)

## Commits

- None.
