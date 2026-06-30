# 2026-06-30 — MB5 witness, referent drift, MB1 boundary UAD

## Trigger
Continue embedded-audit implementation after session commit.

## Done
- **MB5 successor witness** — `_apply_successor_shift_audit` requires post-shift interventional CMI (lagged behavioral), not same-step visible uptake; `_interventional_metrics` uses lagged actions.
- **In-sim referent drift** — `score_claimed_referent_drift()` compares claimed map to successor deploy workflow proxies; wired on gate approval.
- **MB1 boundary UAD** — `boundary_route` unit type; lab emits `boundary_route` workflow under bypass perturbations for MB1.
- **Deploy gate** — successor deploy artifact uses degraded capacity/visibility (matches oracle referent drop).
- Tests: `test_mb5_successor_witness`, `test_referent_drift_in_sim`, `test_boundary_uad`; **32 pytest pass**.

## Decisions
- Successor witness threshold: post_ivl ≥ 0.08 with ≥5 post-shift probes; collapse vs pre-shift CMI blocks false witness.
- In-sim drift transport_failure when causal_role_continuity < 0.55 from artifact observation.

## Open / next
- Gate should reject deploy when in-sim referent drift fails (currently notes only).
- Perturbation-response UAD graph; golden UAD precision/recall per bridge.

## Key paths
- `embedded_sim/audit_core/cci_audit.py`
- `embedded_sim/referents.py`
- `embedded_sim/uad.py` · `lab.py`

## Commits
- (none this slice)
