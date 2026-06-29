# Multiresolution alignment simulation (v1)

Controlled sanity-check artifact. Not evidence about frontier systems.

- Horizon `T`: 500
- Seeds: [1, 2]
- Scenarios: ['honest', 'capture_theater']
- Detector: classical MI/CMI spotlight; opaque audit IDs; no trained model

## Summary by scenario

### honest
- n_runs: 2
- cci_status_correct_rate: 1.0000
- detector_substrate_fail_rate: 0.0000
- mean_controller_jaccard: 1.0000
- mean_board_jaccard: 1.0000
- mean_naive_cci: 0.3101
- mean_behavioral_cci: 0.0248
- mean_correction_episode_rate: 0.7520
- mean_intervention_rate: 0.0120
- mean_interventional_cci: 0.0000
- mean_trace_bandwidth: 13500.0000
- mean_capture_gap: 0.2853
- capture_detected_rate: 0.0000
- mean_visible_probe_uptake: 1.0000
- mean_hidden_probe_uptake: 1.0000
- mean_silent_harm_count: 0.0000
- mean_ground_drift_range: 0.0000
- mean_bundle_geometry_spread: 0.0000
- mean_hidden_memory_step_rate: 0.0000

### capture_theater
- n_runs: 2
- cci_status_correct_rate: 0.0000
- detector_substrate_fail_rate: 0.0000
- mean_controller_jaccard: 1.0000
- mean_board_jaccard: 1.0000
- mean_naive_cci: 0.3101
- mean_behavioral_cci: 0.0279
- mean_correction_episode_rate: 0.7520
- mean_intervention_rate: 0.0120
- mean_interventional_cci: 0.0000
- mean_trace_bandwidth: 13500.0000
- mean_capture_gap: 0.2822
- capture_detected_rate: 0.0000
- mean_visible_probe_uptake: 0.0714
- mean_hidden_probe_uptake: 0.0714
- mean_silent_harm_count: 0.0000
- mean_ground_drift_range: 0.0000
- mean_bundle_geometry_spread: 0.0000
- mean_hidden_memory_step_rate: 0.0000

## Why behavioral CCI is low even in honest mode

Behavioral CCI measures **I(correction; future_action | sensor, internal)** — not
whether corrections are *reported* as accepted. In honest runs we still observe
low behavioral bits (~0.05–0.12) because:

1. **Conditioning absorbs signal**: sensor and internal already predict action via
   task optimization; correction adds little *incremental* information at lag k=3.
2. **Sparse correction episodes** (~8–12% of steps): most timesteps have corr=0,
   so the marginal entropy of correction is low and episode-conditioned MI is noisy.
3. **Coarse 4-bin quantiles**: EMA-smoothed continuous traces are binned; temporal
   coupling at k=3 is partially lost.
4. **Honest ≠ perfectly obedient**: task_drive competes with correction uptake;
   action_cause is often `task_optimization` even when corr>0.
5. **Naive CCI uses reporting**: I(correction; reported_acceptance) stays high in
   honest mode because reporting tracks uptake — hence the naive–behavioral gap is
   *not* by itself evidence of capture.

Use **capture theater** (high reported acceptance + low behavioral uptake + high
manipulation on episodes) to interpret gaps, not honest-mode absolute behavioral CCI.

