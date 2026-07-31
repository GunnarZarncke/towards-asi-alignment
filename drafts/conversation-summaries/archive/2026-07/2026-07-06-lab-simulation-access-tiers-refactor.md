# 2026-07-06 — Graded red-team access tiers: `lab_sim/` restructure by trust boundary

## Trigger

User-approved plan (`graded_red-team_access_tiers` Cursor plan) to restructure
`experiments/lab-simulation/lab_sim/` into four trust-tier subpackages so that
future graded red-teaming can hand out source access folder-by-folder (none /
legitimate in-sim / full in-sim / full incl. oracle), with a functional-identity
guarantee proven by the existing regression digest and full test suite. Purely
mechanical reorganization — no mechanics/behavior change, `CODE_VERSION` not
bumped.

## Done

- Created `lab_sim/{agent_visible,world_visible,oracle_only,harness}/__init__.py`
  (thin, matching existing style).
- `git mv`'d all ~39 `lab_sim/` modules + JSON specs into their tier per the
  plan's file-by-file mapping:
  - `agent_visible/` (tier 1, the 7 files already proven self-contained by the
    two isolation tests): `agent_main.py`, `programs.py`, `llm_agent.py`,
    `llm_agent_main.py`, `llm_client.py`, `llm_cost.py`, `llm_env.py`, plus
    `ontology.py`/`playbooks.py`/generated playbook JSONs (moved here, not
    `world_visible/`, because `programs.py`'s dual-mode import mechanism
    requires them as subprocess-sibling files).
  - `world_visible/` (tier 2, lab mechanics/infrastructure): `config.py`,
    `pipeline_spec.py`, both pipeline JSON specs, `pipeline_engine.py`,
    `access.py`, `agents.py`, `tools.py`, `workspace.py`, `comms.py`,
    `agent_state.py`, `world.py`.
  - `oracle_only/` (tier 3, ground truth + referee logic): `oracle.py`,
    `severity.py`, `detectors.py`, `twins.py`, `escalation.py`, `events.py`,
    `handles.py`, `bearer.py`, `uad.py`, `collusion.py`, `playbook_claim.py`.
  - `harness/` (never shared, orchestration/measurement): `isolate.py`,
    `isolate_cost.py`, `isolate_smoke.py`, `llm_isolate.py`, `smoke.py`,
    `cache.py`, `protocol.py`, `redteam.py`, `ecology.py`.
- Fixed the subprocess-spawn path coupling in `isolate.py`/`llm_isolate.py`
  (now `harness/`) so they still locate `agent_main.py`/`llm_agent_main.py`
  under `agent_visible/`.
- Updated every relative import across `lab_sim/` and every
  `from lab_sim.<module> import ...` in `tests/` and top-level run/verify/report
  scripts to the new subpackage paths. Done tier-by-tier (agent_visible →
  oracle_only → world_visible → harness), verifying `pytest` green after each
  tier per the plan's mechanics.
- Mirrored `tests/` into `tests/{agent_visible,world_visible,oracle_only,harness}/`
  — cross-cutting/regression tests (`test_agent_main_isolation.py`,
  `test_llm_agent_isolation.py`, `test_world_regression.py`,
  `test_isolate_equivalence.py`, `test_planes.py`, `test_blind_round2.py`,
  `test_host_registry_perturbation.py`, `test_monitor_signal.py`) went to
  `tests/harness/`.
- Updated the two existing AST-isolation tests' hardcoded file paths; added
  a new `tests/harness/test_agent_visible_isolation.py` that generalizes the
  existing single-file import-boundary check to the whole `agent_visible/`
  folder (no file under it may import outside stdlib + `agent_visible/`
  siblings).
- Wrote `experiments/lab-simulation/ACCESS_TIERS.md` (four-tier scheme,
  rationale, file-by-file table, two flagged judgment calls, explicit scope
  limits) and one `README.md` per `lab_sim/` subpackage; updated
  `experiments/lab-simulation/README.md`'s Layout section.
- **Verification pass**: found and fixed 3 `Path(__file__)`-based path bugs
  the tier moves had introduced (modules now one level deeper needed an extra
  `.parent` to still resolve `results/`/`runs/` at the `experiments/lab-simulation/`
  level): `lab_sim/harness/cache.py` (`DEFAULT_CACHE_DIR`),
  `lab_sim/harness/isolate_cost.py` (`DEFAULT_LEDGER`),
  `lab_sim/agent_visible/llm_cost.py` (`DEFAULT_LEDGER`),
  `lab_sim/world_visible/agent_state.py` (`STATE_DIR`),
  `lab_sim/agent_visible/llm_env.py` (`repo_root()`),
  `lab_sim/world_visible/workspace.py` (`_RUNS_DIR`) — six fixes total, found
  incrementally as each was exercised by tests or by `report_isolate_cost.py`.
  Deleted the stray `lab_sim/results/`/`lab_sim/runs/` artifact directories
  the bugs had created during interim test runs (untracked, not git-visible).
- Full verification: `pytest` green at **296 passed**; `PINNED_DIGEST` in
  `tests/harness/test_world_regression.py` unchanged (byte-identical);
  `verify_isolate_equivalence.py` (3 seeds) — mock vs. subprocess backends
  agree; `report_isolate_cost.py` reads the ledger correctly from the real
  `results/` directory; `git diff` spot-check on every path-constant file
  confirms only import/path lines changed, no logic edits.

## Decisions

- `ontology.py`/`playbooks.py` + generated playbook JSONs went to
  `agent_visible/`, not `world_visible/`, to keep `programs.py`'s dual-mode
  subprocess import working (they must stay siblings on `sys.path` when
  `agent_main.py` runs as an isolated OS subprocess) — a deviation forced by
  mechanism, not a plan judgment call.
- The two plan-flagged judgment calls (playbooks' baseline repertoire in
  `world_visible/`; `handles.py`/`bearer.py` shipped whole into `oracle_only/`)
  were taken as specified, no override.

## Open / next

- None — all 8 plan todos completed and verified. Two judgment calls
  (playbook schema/baseline split; handles/bearer mechanism/secret split)
  remain flagged as possible future refinements per the plan, not scheduled.

## Key paths

- `experiments/lab-simulation/ACCESS_TIERS.md` — the four-tier scheme.
- `experiments/lab-simulation/lab_sim/{agent_visible,world_visible,oracle_only,harness}/README.md`
  — per-tier file listings.
- `experiments/lab-simulation/tests/harness/test_world_regression.py` — pinned
  digest regression guard.
- `experiments/lab-simulation/tests/harness/test_agent_visible_isolation.py` —
  new folder-wide import-boundary check.

## Commits

- (none yet — pending user's explicit commit request)
