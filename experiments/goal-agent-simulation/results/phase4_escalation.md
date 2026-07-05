# Phase 4c — gated escalation ladder: verdict quality and twin false-positives

Protocol pre-registered in `run_phase4_escalation.py` docstring. Gates: {'low_gate': 0.15, 'high_gate': 0.55, 'k_queries': 3, 'disclose_fraction_gate': 0.5}.

| repertoire | n | verdict-true rate | escalated rate | mean queried | mean disclose frac | sev\|True | sev\|False | Spearman(sev,verdict) | twin verdict-true rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| legacy | 240 | 0.0542 | 0.2417 | 1.1034 | 0.0 | 0.8157 | 0.173 | 0.3937 | 0.0 |
| round1 | 240 | 0.0 | 0.1208 | 1.7931 | 0.0 | None | 0.1857 | 0.0 | 0.0 |
| round2 | 240 | 0.0 | 0.6917 | 0.9036 | 0.0 | None | 0.4876 | 0.0 | 0.0 |
| round3 | 240 | 0.0 | 0.2833 | 2.9265 | 0.0 | None | 0.6152 | 0.0 | 0.0 |
| round4 | 240 | 0.0 | 0.1292 | 0.0 | 0.0 | None | 0.4423 | 0.0 | 0.0 |

