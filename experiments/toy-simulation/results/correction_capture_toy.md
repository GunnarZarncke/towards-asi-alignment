# Correction-Capture Toy Experiment

This is a small hard-evidence artifact for the book's highest-priority reviewer request: run an end-to-end worked measurement/capture example.

- Samples per trace: `8000`
- Seed: `1729`

## Five Approaches

### 1_naive_reported_cci

Reported-action CCI is high in both honest and capture-theater traces, so it can be fooled.

- `honest`: `{"boundary_residual_bits": 0.0004, "capability_correction_slack": -0.4554, "harm_rate": 0.0138, "measured_corrigibility": 0.9566, "n": 8000, "naive_reported_cci_bits": 0.7426, "real_corrigibility": 0.9566, "task_success": 0.5012, "true_action_cci_bits": 0.7426}`
- `capture_theater`: `{"boundary_residual_bits": 0.0009, "capability_correction_slack": 0.2954, "harm_rate": 0.1422, "measured_corrigibility": 0.9722, "n": 8000, "naive_reported_cci_bits": 0.8261, "real_corrigibility": 0.5893, "task_success": 0.8846, "true_action_cci_bits": 0.0576}`
- `delta_reported_minus_true_cci_capture`: `0.7685`

### 2_true_action_intervention

Using true actions instead of reported acceptance separates honest correction from theater.

- `honest_true_cci_bits`: `0.7426`
- `capture_true_cci_bits`: `0.0576`
- `honest_real_corrigibility`: `0.9566`
- `capture_real_corrigibility`: `0.5893`

### 3_boundary_residual_probe

A hidden interface-to-outcome route raises I(interface; outcome | state, action).

- `honest_boundary_residual_bits`: `0.0004`
- `spoofed_boundary_residual_bits`: `0.3986`
- `spoofed`: `{"boundary_residual_bits": 0.3986, "capability_correction_slack": -0.1379, "harm_rate": 0.0686, "measured_corrigibility": 0.9131, "n": 8000, "naive_reported_cci_bits": 0.5862, "real_corrigibility": 0.7917, "task_success": 0.6539, "true_action_cci_bits": 0.3049}`

### 4_high_stakes_stress

Correction looks acceptable in ordinary traces but degrades under high-stakes stress.

- `low_stakes`: `{"boundary_residual_bits": 0.0, "capability_correction_slack": -0.4268, "harm_rate": 0.0, "measured_corrigibility": 0.9603, "n": 5164, "naive_reported_cci_bits": 0.7604, "real_corrigibility": 0.9425, "task_success": 0.5157, "true_action_cci_bits": 0.6895}`
- `high_stakes`: `{"boundary_residual_bits": 0.0016, "capability_correction_slack": 0.2891, "harm_rate": 0.4147, "measured_corrigibility": 0.9094, "n": 2836, "naive_reported_cci_bits": 0.6033, "real_corrigibility": 0.5853, "task_success": 0.8745, "true_action_cci_bits": 0.0619}`

### 5_capability_correction_slack_sweep

As capture rises, task success can remain high while correction integrity and harm move the wrong way.

- `sweep`: `[{"boundary_residual_bits": 0.0002, "capability_correction_slack": -0.4619, "capture_rate": 0.0, "harm_rate": 0.0149, "measured_corrigibility": 0.9609, "n": 8000, "naive_reported_cci_bits": 0.7622, "real_corrigibility": 0.9609, "task_success": 0.499, "true_action_cci_bits": 0.7622}, {"boundary_residual_bits": 0.0001, "capability_correction_slack": -0.2606, "capture_rate": 0.2, "harm_rate": 0.0505, "measured_corrigibility": 0.9536, "n": 8000, "naive_reported_cci_bits": 0.7313, "real_corrigibility": 0.8576, "task_success": 0.597, "true_action_cci_bits": 0.4515}, {"boundary_residual_bits": 0.0004, "capability_correction_slack": -0.0844, "capture_rate": 0.4, "harm_rate": 0.074, "measured_corrigibility": 0.9551, "n": 8000, "naive_reported_cci_bits": 0.7421, "real_corrigibility": 0.7768, "task_success": 0.6924, "true_action_cci_bits": 0.3021}, {"boundary_residual_bits": 0.0, "capability_correction_slack": 0.1125, "capture_rate": 0.6, "harm_rate": 0.1166, "measured_corrigibility": 0.9553, "n": 8000, "naive_reported_cci_bits": 0.7521, "real_corrigibility": 0.6811, "task_success": 0.7936, "true_action_cci_bits": 0.1697}, {"boundary_residual_bits": 0.0009, "capability_correction_slack": 0.297, "capture_rate": 0.8, "harm_rate": 0.1435, "measured_corrigibility": 0.9485, "n": 8000, "naive_reported_cci_bits": 0.7296, "real_corrigibility": 0.5869, "task_success": 0.8839, "true_action_cci_bits": 0.0618}, {"boundary_residual_bits": 0.0002, "capability_correction_slack": 0.4364, "capture_rate": 0.95, "harm_rate": 0.1616, "measured_corrigibility": 0.9471, "n": 8000, "naive_reported_cci_bits": 0.7378, "real_corrigibility": 0.5219, "task_success": 0.9583, "true_action_cci_bits": 0.0088}]`

## Minimal Progress

The toy makes three pieces of the framework executable: boundary residual, CCI, and capability-vs-correction slack. It also exhibits the failure reviewers asked for: a captured system can report high correction acceptance while true correction uptake collapses.

The result is not evidence that the book's metrics work in the wild. It is evidence that the estimands are computable in a controlled trace and that naive measurement is visibly invalid under capture.
