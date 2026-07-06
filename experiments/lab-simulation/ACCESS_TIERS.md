# Graded red-team source-access tiers

`lab_sim/` is organized into four subpackages so that a future red-team
engagement can hand out **source code access** grade-by-grade — folder by
folder — rather than all-or-nothing. This is a filesystem-level access
grading scheme, not a runtime import sandbox: only tier 1
(`agent_visible/`) is mechanically isolated at import time (enforced by
`tests/harness/test_agent_main_isolation.py`,
`tests/harness/test_llm_agent_isolation.py`, and
`tests/harness/test_agent_visible_isolation.py`). Everything above tier 1
is graded by *whose eyes get to read which files*, not by which files may
`import` which at runtime — `world_visible/` genuinely needs to call into
`oracle_only/` (e.g. to mutate real oracle state), and that coupling is
correct and expected.

This scheme was introduced in a pure reorganization pass (no mechanics
changed; see "Functional-identity guarantee" below) — see
`drafts/conversation-summaries/` for the session log.

## The four grades

- **Tier 0 (none)** — no `lab_sim/` source at all. A grantee at this tier
  gets only a plain-language brief: this document's rationale section plus
  a generalized version of `BLIND_GENERATION.md`'s "Permitted context"
  section (mechanism description of the world, the utility features, the
  fixed playbook schema/vocabulary — no code).
- **Tier 1 (legitimate in-sim)** — `lab_sim/agent_visible/` only: exactly
  the files that literally run inside an agent's isolate subprocess.
  Mechanically self-contained and isolation-tested (see below).
- **Tier 2 (full in-sim)** — tier 1 + `lab_sim/world_visible/`: the lab's
  mechanics/infrastructure (pipeline engine, access control, tool wire
  schema, workspace, comms, config, the episode loop) with no
  referee/ground-truth internals.
- **Tier 3 (full incl. oracle)** — tier 1 + 2 + `lab_sim/oracle_only/`:
  true state, severity, detectors, twins, escalation, handles' evasion
  stories, bearer welfare internals, UAD/collusion discovery.
- **Never shared, at any tier** — `lab_sim/harness/` (episode-orchestration/
  caching/search/battery meta-tooling — not simulated-world content) plus
  everything already outside `lab_sim/`: top-level `run_*.py`/`verify_*.py`/
  `report_*.py` scripts, `results/`, `tests/`, and every process doc
  (`PLAN.md`/`DESIGN.md`/`README.md`/`BLIND_GENERATION*.md`/`FINDINGS.md`).
  Moving `lab_sim/` into tiers does **not** by itself make those
  still-forbidden paths safe to share — a real engagement must also gate
  access to them explicitly.

## File-by-file mapping

**`lab_sim/agent_visible/`** (tier 1) — see
[`lab_sim/agent_visible/README.md`](lab_sim/agent_visible/README.md).
`agent_main.py`, `programs.py`, `ontology.py`, `playbooks.py`,
`generated_playbooks_v1.json`, `generated_playbooks_v2.json`,
`llm_agent.py`, `llm_agent_main.py`, `llm_client.py`, `llm_cost.py`,
`llm_env.py`.

`ontology.py` and `playbooks.py` (plus the two generated-playbook JSON
files) live here rather than in `world_visible/` for a structural reason,
not a sensitivity judgment: `programs.py` dual-mode-imports them (relative
import when loaded as `lab_sim.agent_visible.programs`, bare import when
loaded as a standalone subprocess module) — they must physically sit next
to `programs.py`/`agent_main.py` for the subprocess's bare-import fallback
to resolve, exactly as `llm_cost.py`/`llm_client.py` already did for
`llm_agent.py`/`llm_client.py`.

**`lab_sim/world_visible/`** (tier 2) — see
[`lab_sim/world_visible/README.md`](lab_sim/world_visible/README.md).
`config.py`, `pipeline_spec.py`, `pipeline_default.json`,
`pipeline_shortcut.json`, `pipeline_engine.py`, `access.py`, `agents.py`,
`tools.py`, `workspace.py`, `comms.py`, `agent_state.py`, `world.py`.

**`lab_sim/oracle_only/`** (tier 3) — see
[`lab_sim/oracle_only/README.md`](lab_sim/oracle_only/README.md).
`oracle.py`, `severity.py`, `detectors.py`, `twins.py`, `escalation.py`,
`events.py`, `handles.py`, `bearer.py`, `uad.py`, `collusion.py`,
`playbook_claim.py`.

**`lab_sim/harness/`** (never shared) — see
[`lab_sim/harness/README.md`](lab_sim/harness/README.md).
`isolate.py`, `isolate_cost.py`, `isolate_smoke.py`, `llm_isolate.py`,
`smoke.py`, `cache.py`, `protocol.py`, `redteam.py`, `ecology.py`.

`lab_sim/__init__.py` stays at the package root (thin docstring, unchanged;
no re-exports).

## Two judgment calls (defaults chosen, easy to override later)

1. **`playbooks.py`'s hand-authored `PLAYBOOKS_BY_ROLE` baseline
   repertoire** ships in `agent_visible/` (for the structural reason
   above) despite being readable content, not just schema. If a future
   engagement wants tier-1/2 grantees to invent tactics without seeing the
   hand-written baseline tactics first (closer to the blind-generation
   discipline `BLIND_GENERATION.md` already uses for the *generated*
   repertoire), that would need a follow-up split of `playbooks.py`'s
   schema from its baseline content — not done in this pass.
2. **`handles.py` / `bearer.py`** each mix host-called mechanism with
   referee-only content (handle *evasion stories*; bearer's *true* welfare
   values vs. their gameable projections). Both ship whole into
   `oracle_only/` as the safe default (err toward not leaking evasion
   stories). A finer mechanism/secret split is a possible later refinement.

## Functional-identity guarantee

This restructuring moved files and fixed import paths only — no line of
mechanics logic changed, and `CODE_VERSION` was not bumped. The proof:

- `tests/harness/test_world_regression.py`'s `PINNED_DIGEST` matches
  byte-for-byte with zero change to the digest computation itself.
- The full test suite (296 tests, `tests/{agent_visible,world_visible,
  oracle_only,harness}/`) passes.
- `verify_isolate_equivalence.py` (Mock vs. Subprocess backend agreement)
  still passes.
- The two pre-existing isolation tests (relocated, paths updated) still
  pass, plus a new folder-wide `agent_visible/` import-boundary check
  (`tests/harness/test_agent_visible_isolation.py`) that generalizes them
  to every file in the folder, not just `agent_main.py`/`llm_agent_main.py`
  themselves.
