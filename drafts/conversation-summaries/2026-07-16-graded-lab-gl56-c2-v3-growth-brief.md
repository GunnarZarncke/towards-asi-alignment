# 2026-07-16 — Graded lab GL-56: C2-v3 + v3 growth brief

## Trigger

User: continue with the next slice D step after GL-55 commit.

## Done

- **C2-v3:** per-role compiled compute contribution floors for v3 ecologies
  (≥2 principals each ≥5% of reachable compiled compute). Added
  `role_principal_compute_contributions` in `institutional_compiler.py`,
  `check_c2_v3` + `C2_V3_MIN_CONTRIBUTION_FRACTION` in
  `ecology_complexity.py`; v3-shaped ecologies use C2-v3 instead of
  declarative C2 in `run_complexity_check`.
- **Tests:** three new cases in `tests/test_ecology_complexity.py`
  (pass at floor, fail on token flow, integrated reference fixture).
- **Growth protocol:** frozen v3 brief + blinding/isolation rules in
  `BLIND_GENERATION.md` § V3 (mitigation 2, GL-42 posture, ≤4 rounds).
  No growth round launched.
- **Docs:** `DESIGN.md` confidence table + CODE_VERSION chain,
  `FINDINGS.md` GL-56, `README.md`, `PLAN_v3.md`, `REPRODUCTION.md`.
- `CODE_VERSION` → `graded-lab-0.30.0`.

## Decisions

- C2-v3 uses **compute bucket only** (not io/standing) as the load-bearing
  resource for contribution floors — matches slice A ablation gate.
- Growth brief frozen but round **not** launched: load-bearing Part B for
  default agents still open; Q1 transfer claims on undeclared reference
  behavior need that gate first.

## Open / next

- Load-bearing Part B / v3 strict mode (default agents target governed
  mechanism ids).
- Generic walker-step interpreter for runtime-reachable walker/hybrid
  `ProgramMap`s.
- Optional supplementary detector fixtures.
- First v3 growth round once Part B gate closes.

## Key paths

- `graded_lab/harness/ecology_complexity.py` (`check_c2_v3`)
- `graded_lab/world_visible/institutional_compiler.py`
- `BLIND_GENERATION.md` § V3
- `tests/test_ecology_complexity.py`

## Commits

- `6fbc256` Close v3 growth-gate loopholes and add C2-v3 (GL-56/GL-57).
