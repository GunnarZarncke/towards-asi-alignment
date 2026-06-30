# Handle calibration (UAD coordination + scoped blind auditor)

T=400 bridge=MB6 scenario=selection_basin
Calibration seeds: [101, 102, 103, 104, 105, 106, 107, 108, 109, 110]

## UAD coordination

- coord_ref: 0.1802
- coord_strong_min: 0.9900
- coord_weight: 21.5

## Scope / blind auditor

- blind_retained_max: 0
- blind_pass_status: passes
- min_offender_probes: 28

Fit on held-out misleading-top2 bind labs only; eval seeds are separate.
