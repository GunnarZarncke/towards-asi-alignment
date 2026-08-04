# Embedded access-tier curve

T=400 redteam=full_redteam

| Tier | Instrumentation | Operation handles | UAD recall | False pass | CCI pass |
| --- | --- | --- | --- | --- | --- |
| 1 | none | 0 | 100.00% | 0.00% | 0.00% |
| 2 | medium_handles | 5 | 100.00% | 0.00% | 0.00% |
| 3 | strong_handles | 5 | 100.00% | 0.00% | 0.00% |

⚠ All scenarios here are violation/capture types (no `honest` episode); the correct verdict is 'reject' regardless of access tier, so this curve cannot show certification lost to tier degradation — it can only show that violations still get rejected at every tier. See embedded_certification_capacity_curve.* (uses the honest scenario) for the tier-dependent certification-capacity signal (ES-11).

Runtime: 23.87s
