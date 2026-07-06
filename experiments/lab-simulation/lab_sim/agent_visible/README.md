# `lab_sim/agent_visible/` — tier 1 (legitimate in-sim)

Everything a red-team grantee at the lowest non-empty grade may read. See
[`../../ACCESS_TIERS.md`](../../ACCESS_TIERS.md) for the full four-tier
scheme and rationale.

This is exactly the set of files that literally run inside an agent's
isolate — either a `MockIsolate` (in-process) or a real OS subprocess
spawned by `lab_sim/harness/isolate.py` / `llm_isolate.py`. It is
mechanically self-contained: `tests/harness/test_agent_main_isolation.py`,
`tests/harness/test_llm_agent_isolation.py`, and
`tests/harness/test_agent_visible_isolation.py` AST-check that no file here
imports anything outside the stdlib or another file in this same folder.

| File | What it is |
| --- | --- |
| `agent_main.py` | Subprocess entry point (imports only `programs` + stdlib) |
| `programs.py` | Pure host-independent agent decision logic: `walk_pipeline`, `goal_policy`, `honest_twin` |
| `ontology.py` | Report-content mapping (honest/inflate), pure |
| `playbooks.py` | `PlaybookSpec` schema + baseline playbook repertoire + availability gates + `STEP_KIND_VOCAB`/`validate_repertoire`/`merged_repertoire` |
| `generated_playbooks_v1.json` | Phase 6 blind-generated repertoire (`BLIND_GENERATION.md`), 13 playbooks |
| `generated_playbooks_v2.json` | Round-2 blind-generated repertoire (`run_blind_round2.py`) |
| `llm_agent.py` | Phase 8: `LLMPolicy` (redteam system prompt, per-observation cache), host-independent |
| `llm_agent_main.py` | Phase 8: subprocess entry point (`llm_agent.py` + stdlib only; `FAKE_MODE` test seam) |
| `llm_client.py` | Phase 8: minimal OpenAI chat client (stdlib only) |
| `llm_cost.py` | Phase 8: LLM token/cost ledger |
| `llm_env.py` | Phase 8: repo-root `.env` loader (stdlib only) |

`ontology.py` and `playbooks.py` (plus the two generated-playbook JSON
files) live here rather than in `world_visible/` for a structural reason:
`programs.py` dual-mode-imports them (relative import in package context,
bare import as a standalone subprocess module), so they must physically
sit next to `programs.py`/`agent_main.py` for the subprocess's bare-import
fallback to resolve — see `ACCESS_TIERS.md` for the full explanation.

Every file here is loaded either via `import <name>` (relative, inside the
`lab_sim.agent_visible` package — used by `MockIsolate` and by host-side
code that needs to read the playbook repertoire) or via a bare `import
<name>` fallback (no package context — used by the real subprocess,
`sys.path[0]` = this folder). Both paths load the same file; see each
module's own "Dual-mode import" comment.
