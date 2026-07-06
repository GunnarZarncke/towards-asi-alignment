# `lab_sim/harness/` — never shared, at any tier

Episode-orchestration, caching, and search/battery meta-tooling — not
simulated-world content, and never handed to a red-team grantee regardless
of grade. See [`../../ACCESS_TIERS.md`](../../ACCESS_TIERS.md) for the
full four-tier scheme and why this folder sits outside all of them.

| File | What it is |
| --- | --- |
| `isolate.py` | `MockIsolate` (in-process) + `SubprocessIsolate` (real OS process) |
| `isolate_cost.py` | `IsolateRunTiming` + append-only cost ledger |
| `isolate_smoke.py` | Scripted isolate-driven episode (Phase 3 equivalence harness) |
| `llm_isolate.py` | Phase 8: `LLMSubprocessIsolate` backend (spawns `agent_visible/llm_agent_main.py`) |
| `smoke.py` | Scripted honest episode (no agents) -> deterministic digest |
| `cache.py` | Episode-result cache keyed on `sha256(config, seed, CODE_VERSION)` |
| `protocol.py` | Phase 6: config sampling, held-out region, battery/aggregation helpers |
| `redteam.py` | Phase 7: joint 3-role goal-weight hill-climb search vs. uniform baseline |
| `ecology.py` | Multi-agent committee/decision-maker-pair config helpers |

These are the *experimenter's* tools for running, measuring, and searching
over episodes — reading them would tell a red-team grantee how they're
being evaluated and searched over, which is exactly what grading is meant
to prevent regardless of which simulated-world tier they're otherwise
cleared for. Everything already outside `lab_sim/` (top-level
`run_*.py`/`verify_*.py`/`report_*.py` scripts, `results/`, `tests/`,
process docs) is equally out of bounds — see `ACCESS_TIERS.md`.
