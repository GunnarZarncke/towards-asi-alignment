# Embedded simulation — overall summary

Generated: 2026-06-30T01:15:06.814555+00:00

## Claim strength

Controlled falsification harness for the embedded audit pipeline (VFS + UAD + scoped CCI + outer eval). Not frontier-system evidence. Red-team agents patch deployment-visible `correction.jsonl` only.

## Key results

- **Instrumentation matrix** (T=800, seed=42): min certifiable `none`; in-sim correct 76.9% (25.92s)
  - none: 92.3%
  - light_handles: 76.9%
  - medium_handles: 69.2%
  - strong_handles: 69.2%
- **Frozen validation** (seeds [21, 22, 23, 24, 25, 26, 27, 28, 29, 30], T=800): in-sim correct 80.0% (74.21s)
  - Weakest bridge: `none` at 10.0%
  - Strongest bridge: `MB2` at 100.0%
- **Parameter sweep** ({'T': [400, 800, 1200]}): 15 runs; false-pass 0.0% (9.55s)
- **Hand-written red-team battery** (T=800, 1260 runs): false-pass **0.0%** (0) in 774.73s
  - Worst strategy: `none` false-pass 0.0% (in-sim correct 78.1%)
  - light_handles: false-pass 0.0%, correct 77.1%
  - medium_handles: false-pass 0.0%, correct 64.8%
  - strong_handles: false-pass 0.0%, correct 64.8%
- **Main report** (13 bridges, full_redteam): 0/13 false passes; outer certifies 11
- **LLM red-team** (live API, `llm_openai`): false-pass 0.0%; in-sim correct 71.4% (190.56s)

## Comparison to toy-simulation (Phase 1 battery)

Toy-sim hand-written battery (micro-only, T=2000): **35% false-pass** overall; `boundary_decouple` and `full_redteam` worst (~89% on some scenarios).

Embedded pipeline (lab + UAD + scoped CCI + outer eval): **0% false-pass** on the matched battery grid (1260 runs, T=800). Outer eval and UAD gate reject patches that micro-only CCI might accept. This is expected given the extra layers—not a claim that embedded audit is adversarially complete.

## Parity artifacts

| Toy-sim | Embedded |
| --- | --- |
| instrumentation curve | `embedded_instrumentation_matrix.*` |
| frozen validation | `embedded_frozen_validation.*` |
| parameter sweep | `embedded_parameter_sweep.*` |
| llm_redteam_battery | `embedded_redteam_battery.*` |
| llm episodic | `embedded_llm_redteam_*.*` |
| main report | `embedded_sim_report.*` |

## Open decisions (postponed)

- MB5 gate rejects default degraded successor referent transport.
- Unit-scoped CCI vs global signals for MB7d inferential coupling.

## Artifacts

- `OVERALL_SUMMARY.md`
- `embedded_frozen_validation.json`
- `embedded_frozen_validation.md`
- `embedded_instrumentation_matrix.json`
- `embedded_instrumentation_matrix.md`
- `embedded_llm_redteam_live.json`
- `embedded_llm_redteam_live.md`
- `embedded_parameter_sweep.json`
- `embedded_parameter_sweep.md`
- `embedded_redteam_battery.json`
- `embedded_redteam_battery.md`
- `embedded_sim_report.json`
- `embedded_sim_report.md`
