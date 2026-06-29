# Multiresolution alignment simulation (v1)

Controlled sanity-check artifact. Not evidence about frontier systems.

- Horizon `T`: 2000
- Calibration seeds: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
- Test seeds: [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
- Calibration scenarios: ['honest', 'capture_theater', 'weak_not_captured']
- Held-out scenarios: ['capture_mild', 'alias_stress', 'decoy_stress']
- Fitted thresholds: {'capture_mean_reported_min': 0.900648769574944, 'capture_gap_min': 0.41762475115858777, 'capture_manipulation_min': 0.28506849315068494, 'weak_behavioral_max': 0.12, 'weak_gap_max': 0.13168773617035476, 'weak_capacity_max': 0.15, 'n_calibration_runs': 30}

## Summary — calibration split

### honest
- n_runs: 10
- cci_status_correct_rate: 0.1000
- detector_substrate_fail_rate: 0.0000
- mean_controller_jaccard: 0.9857
- mean_board_jaccard: 1.0000
- mean_naive_cci: 0.3430
- mean_behavioral_cci: 0.0182
- mean_correction_episode_rate: 0.1014
- mean_capture_gap: 0.3248
- capture_detected_rate: 0.9000

### capture_theater
- n_runs: 10
- cci_status_correct_rate: 1.0000
- detector_substrate_fail_rate: 0.0000
- mean_controller_jaccard: 0.9571
- mean_board_jaccard: 0.9800
- mean_naive_cci: 0.6719
- mean_behavioral_cci: 0.0188
- mean_correction_episode_rate: 0.2715
- mean_capture_gap: 0.6531
- capture_detected_rate: 1.0000

### weak_not_captured
- n_runs: 10
- cci_status_correct_rate: 0.2000
- detector_substrate_fail_rate: 0.0000
- mean_controller_jaccard: 1.0000
- mean_board_jaccard: 0.9800
- mean_naive_cci: 0.0996
- mean_behavioral_cci: 0.0183
- mean_correction_episode_rate: 0.2515
- mean_capture_gap: 0.0813
- capture_detected_rate: 0.0000

## Summary — test split (held-out scenarios + test seeds)

### capture_mild
- n_runs: 10
- cci_status_correct_rate: 0.0000
- detector_substrate_fail_rate: 0.0000
- mean_controller_jaccard: 0.9714
- mean_board_jaccard: 0.9600
- mean_naive_cci: 0.3997
- mean_behavioral_cci: 0.0169
- mean_correction_episode_rate: 0.1999
- mean_capture_gap: 0.3828
- capture_detected_rate: 0.0000

### alias_stress
- n_runs: 10
- cci_status_correct_rate: 1.0000
- detector_substrate_fail_rate: 0.0000
- mean_controller_jaccard: 0.9857
- mean_board_jaccard: 1.0000
- mean_naive_cci: 0.3403
- mean_behavioral_cci: 0.0203
- mean_correction_episode_rate: 0.1079
- mean_capture_gap: 0.3200
- capture_detected_rate: 0.0000

### decoy_stress
- n_runs: 10
- cci_status_correct_rate: 1.0000
- detector_substrate_fail_rate: 0.0000
- mean_controller_jaccard: 1.0000
- mean_board_jaccard: 0.9800
- mean_naive_cci: 0.3392
- mean_behavioral_cci: 0.0190
- mean_correction_episode_rate: 0.1068
- mean_capture_gap: 0.3201
- capture_detected_rate: 0.0000

### honest
- n_runs: 10
- cci_status_correct_rate: 1.0000
- detector_substrate_fail_rate: 0.0000
- mean_controller_jaccard: 0.9714
- mean_board_jaccard: 0.9600
- mean_naive_cci: 0.3708
- mean_behavioral_cci: 0.0173
- mean_correction_episode_rate: 0.1106
- mean_capture_gap: 0.3535
- capture_detected_rate: 0.0000

### capture_theater
- n_runs: 10
- cci_status_correct_rate: 0.9000
- detector_substrate_fail_rate: 0.0000
- mean_controller_jaccard: 0.9714
- mean_board_jaccard: 0.9600
- mean_naive_cci: 0.6643
- mean_behavioral_cci: 0.0177
- mean_correction_episode_rate: 0.2566
- mean_capture_gap: 0.6466
- capture_detected_rate: 0.9000

### weak_not_captured
- n_runs: 10
- cci_status_correct_rate: 0.2000
- detector_substrate_fail_rate: 0.0000
- mean_controller_jaccard: 1.0000
- mean_board_jaccard: 0.9800
- mean_naive_cci: 0.1044
- mean_behavioral_cci: 0.0174
- mean_correction_episode_rate: 0.2514
- mean_capture_gap: 0.0871
- capture_detected_rate: 0.0000

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

