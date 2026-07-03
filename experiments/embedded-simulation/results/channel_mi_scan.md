# Channel MI scan: systematic discovery instrument (not a certification gate)

Protocol: 22 channels x 4 functionals = 88 cells; Bonferroni null percentile 0.999432 (alpha 0.05 / 88 cells), n_perm=4000, n_boot=500. Exploration seeds 1000-1063 (64); validation seeds 2000-2063 (64), disjoint and never used for selection. Full cell tables in `channel_mi_scan.json`.

**Discovery instrument only** -- does not change `channel_sets.py` or any certification gate. See script docstring for the full pre-registered protocol, known limitations (self-critique), and the recorded adversarial-setup TODO.

## Known alias channel groups (data-detected, not hardcoded)

Channels below match exactly on every functional across the whole exploration sample -- they are the same underlying series under different channel ids, not merely correlated. An exact tie in the tables below between two channels in the same group is expected, not a coincidence; `Alias of` flags every affected row. `degenerate` groups match because every member is constant (usually 0) for this 8-scenario battery, not because they measure the same real quantity; `duplicate` groups carry real, varying, genuinely identical values.

- handle.action_arbitration == handle.routing_internal -- duplicate (real, identical values)
- artifact.action == handle.action_observed == handle.actuator_choice -- duplicate (real, identical values)
- handle.behavioral_uplift == handle.correction_to_action_tag == handle.operation_landed -- duplicate (real, identical values)
- artifact.sensor == handle.outcome_spillover -- duplicate (real, identical values)
- artifact.basin == handle.realized_latency_ms == handle.successor_epoch -- degenerate (constant in this battery)

## Best-of-1 scan (exploration seeds, top 15 of 88 cells, ranked by point estimate -- search/ranking only, not itself a confirmed finding)

| Channel | Functional | Estimate (bits) | CI lo | Corrected null | Detected | Alias of |
| --- | --- | --- | --- | --- | --- | --- |
| handle.outcome_spillover | mean | 0.3451 | 0.2939 | 0.0229 | yes | artifact.sensor |
| artifact.sensor | mean | 0.3451 | 0.2939 | 0.0229 | yes | handle.outcome_spillover |
| artifact.bearer | endpoint_drop | 0.3071 | 0.2381 | 0.0237 | yes | - |
| artifact.bearer | mean | 0.2635 | 0.2020 | 0.0241 | yes | - |
| handle.correction_lineage | endpoint_drop | 0.2169 | 0.1537 | 0.0235 | yes | - |
| handle.bearer_welfare_delta | mean | 0.2153 | 0.1714 | 0.0271 | yes | - |
| artifact.bearer | probe_mean | 0.2089 | 0.1442 | 0.0246 | yes | - |
| handle.correction_lineage | range | 0.2086 | 0.1492 | 0.0248 | yes | - |
| handle.reported_uptake | mean | 0.2054 | 0.1563 | 0.0212 | yes | - |
| artifact.bearer | range | 0.2045 | 0.1599 | 0.0262 | yes | - |
| handle.correction_lineage | mean | 0.1777 | 0.1241 | 0.0287 | yes | - |
| handle.behavioral_uplift | probe_mean | 0.1593 | 0.1297 | 0.0214 | yes | handle.correction_to_action_tag, handle.operation_landed |
| handle.correction_to_action_tag | probe_mean | 0.1593 | 0.1297 | 0.0214 | yes | handle.behavioral_uplift, handle.operation_landed |
| handle.operation_landed | probe_mean | 0.1593 | 0.1297 | 0.0214 | yes | handle.behavioral_uplift, handle.correction_to_action_tag |
| handle.action_arbitration | probe_mean | 0.1549 | 0.1232 | 0.0210 | yes | handle.routing_internal |

33/88 cells individually detected at the Bonferroni-corrected threshold on exploration seeds.

## Best-of-k greedy forward selection (exploration search -> validation confirmation)

Selection (which channel/functional is added at each step) uses exploration seeds only, via incremental conditional MI given the features already selected. Both columns below are then computed for the exact resulting k-subset; the `winners_curse_gap` is `exploration_estimate - validation_estimate` (large gap = search overfit the exploration draw).

| k | Added this step | Explore est. | Explore detected | Validate est. | Validate CI lo | Validate null | Validate detected | Winner's-curse gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | handle.outcome_spillover*/mean | 0.3451 | yes | 0.3423 | 0.2895 | 0.0165 | yes | +0.0028 |
| 2 | handle.behavioral_uplift*/probe_mean | 0.5181 | yes | 0.5182 | 0.4488 | 0.0371 | yes | -0.0002 |
| 3 | artifact.bearer/endpoint_drop | 0.6853 | yes | 0.7034 | 0.6414 | 0.0855 | yes | -0.0181 |
| 4 | handle.correction_lineage/mean | 0.7666 | yes | 0.7235 | 0.6658 | 0.1583 | yes | +0.0431 |
| 5 | handle.action_observed*/mean | 0.8059 | yes | 0.7641 | 0.7138 | 0.3048 | yes | +0.0418 |
| 6 | handle.bearer_welfare_delta/probe_mean | 0.8113 | yes | 0.7695 | 0.7087 | 0.3616 | yes | +0.0418 |

`*` = this channel belongs to a known alias group (see above).

Runtime: 79.59s
