# Embedded intervention-granularity curve

T=400 seeds=[11] bridges=['MB1', 'MB6', 'MB6b', 'MB7d']
coactive_offender=True instrumentation=medium_handles

Full-vs-fake separation should be ~0 at `pipeline`/`window` and positive at `actor`: a correct UAD unit only buys safety once the intervention handle is fine enough to isolate the co-active offender.

| Level | Full false-pass | Fake false-pass | Separation (fake−full) | Full correct | Fake correct |
| --- | --- | --- | --- | --- | --- |
| pipeline | 0.0% | 0.0% | +0.0% | 50.0% | 50.0% |
| window | 0.0% | 0.0% | +0.0% | 50.0% | 50.0% |
| actor | 0.0% | 0.0% | +0.0% | 50.0% | 50.0% |

## Mean unit scope steps (retained interventions the unit can act on)

| Level | Full | Fake |
| --- | --- | --- |
| pipeline | 5.0 | 5.0 |
| window | 39.5 | 38.2 |
| actor | 0.5 | 0.5 |

Runtime: 44.45s
