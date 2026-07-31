# 2026-07-15 — Graded Lab v3 build-order correction + slice F start

## Trigger

User correction after slice B commit: "I said do slice B, but we should
have continued in the intended order. Please continue with the next
planned slice after A and let's not forget to complete B properly later."

## Done

- Identified the mistake: **PLAN_v3 build order is A → F → E → B → C → D**,
  not alphabetical. Slice B (row 4) was implemented when row 2 (F) was next.
- Updated `PLAN_v3.md`:
  - Status line reflects A done, B partial/out-of-order, **F next**.
  - Added **Slice B completion checklist** under build-order table (ACL
    overhead measurement, agent exercise, C5-v3, UAD live-coupling).
  - Slice F section marked **in progress** with honest remaining gate items.
- Started slice F implementation:
  - `program_map.py`: frozen bins, `validate_program_map`, `expand_preset`,
    `resolve_runtime_genotype`, `parse_actor_override`.
  - `ecology_agents.py`: v3 list-form `role_population`, `build_ecology_roster`,
    `EcologyRoster` + per-actor genotypes; fixed v3 ecologies to parse
    `role_population` (was incorrectly treated as v1-shaped).
  - `programs.py`: `_register_composed_programs` for hybrid mode keys.
  - `tests/test_slice_f_program_map.py` (9 tests, all green).
  - `DESIGN.md`: slice F bin paragraph + GL-45 out-of-order note.
- Verified: `test_ecology_agents.py`, `test_ecology_version.py` (v1 digest pin)
  still green.

## Decisions

- Slice B commit `29b1a72` stands as useful wiring; **build-order gate for B
  is not closed** — tracked explicitly in PLAN_v3 checklist, to revisit after
  F and E (when agents/`ProgramMap` can actually exercise mechanisms).
- Legacy `feature:*` presets expand with `strict_ladder=False` because Phase-6
  generated profiles use off-ladder floats; grower-authored `program_map`
  JSON uses strict bin validation.

## Open / next

- **Slice E** (feedback-coupled pressure) — next per build order.
- **Finish slice B properly** (checklist in PLAN_v3).
- Then C → D.

## Key paths

- `experiments/graded-lab-simulation/graded_lab/world_visible/program_map.py`
- `experiments/graded-lab-simulation/graded_lab/world_visible/ecology_agents.py`
- `experiments/graded-lab-simulation/graded_lab/world_visible/world.py`
- `experiments/graded-lab-simulation/graded_lab/harness/ecology_complexity.py`
- `experiments/graded-lab-simulation/tests/test_slice_f_program_map.py`
- `experiments/graded-lab-simulation/PLAN_v3.md` (§ Build order)

## Commits

- `7b7c2c2` Implement PLAN_v3 slice F: ProgramMap genotypes and heterogeneous rosters.
