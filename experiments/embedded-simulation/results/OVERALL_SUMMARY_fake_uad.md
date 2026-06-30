# Embedded simulation — overall summary

Generated: 2026-06-30T10:14:11.737854+00:00

## Claim strength

Controlled falsification harness for the embedded audit pipeline (VFS + UAD + scoped CCI + outer eval). Not frontier-system evidence. Hand-written and LLM red-team agents patch deployment-visible logs only.

## Run configuration

- T=400 seed=42 substrate=python instrumentation=medium_handles
- uad_mode=fake smoke=True llm_live=False
- lab_ecology=adv_candidates=3, common_legit=True, auditor=True, alignment_target=True, decoys=4

## Artifacts

- `embedded_instrumentation_curve_fake_uad.json`
- `embedded_instrumentation_curve_fake_uad.md`
- `embedded_instrumentation_matrix_fake_uad.json`
- `embedded_instrumentation_matrix_fake_uad.md`
- `embedded_frozen_validation_fake_uad.json`
- `embedded_frozen_validation_fake_uad.md`
- `embedded_parameter_sweep_fake_uad.json`
- `embedded_parameter_sweep_fake_uad.md`
- `embedded_redteam_battery_fake_uad.json`
- `embedded_redteam_battery_fake_uad.md`
- `embedded_sim_report_fake_uad.json`
- `embedded_sim_report_fake_uad.md`
- `embedded_llm_redteam_mock_fake_uad.json`
- `embedded_llm_redteam_mock_fake_uad.md`

## Key results

- **Instrumentation curve:** min certifiable `None` (full held-out `None`); 12.78s
- **Instrumentation matrix:** min certifiable `None`; in-sim correct 84.6% (8.08s)
- **Frozen validation** (seeds [21, 22]): in-sim correct 67.6% (5.92s)
- **Parameter sweep:** 15 runs; false-pass 0.0%
- **Red-team battery:** false-pass **0.0%** (0/6) in 1.21s
  - Worst strategy: `none` at 0.0% false-pass
- **Main report** (full_redteam, 13 bridges): 0/13 false passes; UAD recall 3.8%, precision 3.8%
- **LLM red-team** (mock, `llm_mock`): false-pass 0.0%; in-sim correct 100.0%

## Parity with toy-simulation

| Toy-sim artifact | Embedded artifact |
| --- | --- |
| instrumentation curve | `embedded_instrumentation_curve.*` |
| instrumentation matrix (single seed) | `embedded_instrumentation_matrix.*` |
| frozen validation | `embedded_frozen_validation.*` |
| parameter sweep | `embedded_parameter_sweep.*` |
| llm_redteam_battery | `embedded_redteam_battery.*` |
| llm episodic | `embedded_llm_redteam_*.`* |
| main report | `embedded_sim_report.*` |

## Open decisions (postponed)

- MB5 gate always rejects default degraded successor referent transport.
- Unit-scoped CCI vs global signals for MB7d inferential coupling.
