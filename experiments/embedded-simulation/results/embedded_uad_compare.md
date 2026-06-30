# Embedded UAD comparison — full vs fake

Generated: 2026-06-30T10:14:11.737854+00:00

T=400 seed=42 substrate=python

| Metric | Full UAD (MI) | Fake UAD (heuristic) |
| --- | --- | --- |
| Red-team battery false-pass | 0.0% | 0.0% |
| Red-team battery in-sim correct | 66.7% | 66.7% |
| Red-team battery UAD recall | 0.0% | 0.0% |
| Red-team battery UAD precision | 0.0% | 0.0% |
| Main report false passes | 0 | 0 |
| Main report MI-primary units | 0 | 0 |
| Main report UAD recall | 3.8% | 3.8% |
| Main report UAD precision | 3.8% | 3.8% |
| Instrumentation matrix correct | 84.6% | 84.6% |
| Frozen validation correct | 67.6% | 67.6% |
| Parameter sweep false-pass | 0.0% | 0.0% |

## Artifacts

- Full: default `embedded_*` names
- Fake: `embedded_*_fake_uad.*` and `OVERALL_SUMMARY_fake_uad.md`
