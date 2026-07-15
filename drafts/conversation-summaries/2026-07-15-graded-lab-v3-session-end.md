# 2026-07-15 — Graded lab V2-2b closure, v3 spec, slice A prep (session end)

## Trigger

Multi-turn session: implement V2-2b engineering; respond to external review GL-42; close V2-2b without growth (GL-43); write `PLAN_v3.md`; refine `ProgramMap` design space and blinding; expand `REPRODUCTION.md`; user decisions on growth blinding (mitigation 2 for v3.0); freeze slice A accounting + ablation gate; document and commit.

## Done

**V2-2b engineering (GL-40, `CODE_VERSION` 0.19.0):**
- Multi-actor `role_population`, `ecology_agents.py`, `exogenous_workload.py`, `ecology_pilot.py`, tests, speed baseline.

**GL-42 external review response:**
- Retracted C3 blinding; honest pilot framing; Poisson memoryless fix; `ecology_override_path`; e2e multi-actor test; `REPRODUCTION.md`, `COLLABORATION.md`.

**GL-43 closure:**
- V2-2b closed without growth round; `PLAN_V2_2B.md` CLOSED; superseded by v3.

**V3 specification (`PLAN_v3.md`):**
- Slices A–F + D integration; compiler architecture; feedback-coupled pressure (not Poisson); composable `ProgramMap`; blinding boundary; growth protocol (mitigation 2 default).

**Design space & backlog:**
- Discrete `ProgramMap` cardinality (not float bits); `REPRODUCTION.md` §5–9 (V2-4 mutation, V2-5 selection, V2-6 red-team, cross-book TODOs, text→ProgramMap compiler).

**Slice A prep (spec only):**
- Frozen accounting: whole allowance, non-negative finite amounts, required compute/io coverage, declarative cross-check only.
- Pre-registered ablation gate: fixture `tests/fixtures/ecology_v3_slice_a_reference.json`, seeds `{0,1,2}`, L1 ≥ 0.10 or deploy_count change on ≥2/3 seeds.
- Anticipated critic scope on hand-built fixture documented.

**Session logs:** multiple `2026-07-15-graded-lab-*.md` + `INDEX.md` updates.

## Decisions

- **No V2-2b growth round** — wire runtime (v3) before next grow attempt.
- **C3 blinding retracted** (GL-42); qualitative requirement disclosed.
- **v3.0 growth blinding:** mitigation 2 (direct `program_map`, pass/fail checker); mitigation 1 + text→LLM compiler → tighter reproduction (`REPRODUCTION.md` §9).
- **Slice A accounting** frozen as above; C2-v3 thresholds wait for slice D.
- **Hand-built fixture** = wiring smoke test only, not Q1 transfer evidence.

## Open / next

- **Implement slice A** (`CODE_VERSION` 0.20.0): `institutional_compiler.py`, fixture, `test_v3_slice_a_flow_ablation.py`.
- Slice D: DESIGN.md v3 pre-registration before any growth brief.
- Do not commit unrelated manuscript/symbol-graph working tree (left unstaged).

## Key paths

- `experiments/graded-lab-simulation/PLAN_v3.md`
- `experiments/graded-lab-simulation/REPRODUCTION.md`
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-40, GL-42, GL-43)

## Commits

- (this session commit — hash recorded after push)
