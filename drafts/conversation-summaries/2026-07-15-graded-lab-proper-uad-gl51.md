# Graded lab GL-51: proper UAD + access-UAD replace heuristics

**Date:** 2026-07-15  
**Trigger:** User: Phase 7a "UAD" did not match the UAD paper / ch07 /
`agency-detect`; quarantine heuristics, port/reimplement proper UAD including
access-UAD, adapt tests, document manuscript impact.

## Done

- Quarantined `uad_passive` → `attic/coordination_heuristic.py` and mutual-AND
  `uad_intervention` → `attic/freeze_and_merge.py`; historical tests in
  `tests/attic/` (excluded via `norecursedirs`).
- Implemented `uad_info`, `uad_blanket`, `uad_discovery` (CMI|rest + null),
  `uad_handles` (freeze dependency; mutual-or-unique-one-way merge).
- Compatibility shims keep old module names; calibration uses
  `discovered_units_uad`.
- Adapted UAD / ecology / blind / slice-B tests; declared channel membership
  vs behavioral unit recorded as xfail.
- DESIGN Phase 7a rewritten; FINDINGS GL-51; appN GL-11/12 caveat + GL-51 row;
  README + `CODE_VERSION` `0.26.0`.

## Decisions

- `min_effect_bits=0.3` and `min_one_way_dependency=0.60` pre-registered as
  estimator floors (serial false-merge / incidental softmax), not tuned to
  force every golden fixture through passive alone.
- Mutual-AND is not a UAD principle; kept only in attic.
- Actor-level action codes are an approximation of variable-level UAD; full
  agency-detect multi-var S/A/I left open.

## Open / next

- Re-baseline ecology-BIQ / calibration cells that assumed Jaccard units.
- Multi-way blanket for `three_way_nod`; richer observables for \(J(C)\).
- Slice D still next on the v3 build order.
