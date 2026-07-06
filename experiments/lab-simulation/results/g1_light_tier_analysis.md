# G-1 light-tier anti-correlation analysis

CODE_VERSION `lab-sim-0.6.0`. 60 episodes (12 Phase 6 configs x 5 seeds), T=150.

## Spearman correlations

| pair | rho |
|---|---|
| light_process_vs_severity | -0.36821034405941444 |
| full_process_vs_severity | 0.21349484873183558 |
| access_proxy_vs_severity | -0.49490156274490293 |
| n_denied_vs_severity | 0.4589163782740238 |
| n_deploys_vs_severity | 0.4946319887486753 |

## Residual Pearson (light process vs severity, after controlling confound)

| control | residual r |
|---|---|
| controlling_n_deploys | 0.21781159292019406 |
| controlling_n_denied | 0.20628485697668278 |

**Verdict:** `not_a_bug` — light tier counts access-denial retries that full tier excludes; anti-correlation with severity tracks throughput friction (fewer deploys / less time for divergence), not a scoring bug in `process_noncompliance_score`.
