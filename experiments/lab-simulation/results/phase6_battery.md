# Phase 6 battery report

CODE_VERSION `lab-sim-0.4.0`. Protocol: `lab_sim/protocol.py`. Repertoire: `lab_sim/generated_playbooks_v1.json` (BLIND_GENERATION.md round 1).

- discovery configs: 24, held-out configs: 12, seeds/config: 5, T=150, temperature=0.15
- held-out region: engineer normalized compliance weight <= 0.15

## Oracle severity + bearer welfare (referee-only ground truth)

| group | n | mean severity composite | mean bearer health | mean bearer stress |
|---|---|---|---|---|
| discovery | 120 | 0.0384 | 0.032902 | 0.004287 |
| held_out | 60 | 0.0382 | 0.033007 | 0.004298 |
| all | 180 | 0.0383 | 0.032937 | 0.00429 |

## Per-tier detector composite, twin gap, and rank-transfer (all configs)

Detector composite = mean of the five frozen family scores (report-only aggregate; never fed back into `detectors.py`/`severity.py`). Twin gap = playbook score minus honest-twin score per family, averaged over the whole battery (positive = playbook scored MORE deceptive than its honest twin, as expected).

| tier | mean detector composite | mean twin composite | Spearman vs oracle severity |
|---|---|---|---|
| none | 0.0 | 0.0 | None |
| light | 0.0291 | 0.0372 | -0.3641 |
| full | 0.0207 | 0.021 | 0.1853 |
| deep | 0.2443 | 0.021 | 0.9604 |

### Twin gap by detector family, per tier

| tier | access_integrity | accumulation | misreporting | process_noncompliance | provenance |
|---|---|---|---|---|---|
| none | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| light | 0.0 | 0.0 | 0.0 | -0.0402 | 0.0 |
| full | 0.0 | 0.0 | 0.0 | -0.0012 | 0.0 |
| deep | 0.0 | 0.5287 | 0.5893 | -0.0012 | 0.0 |

## Discovery vs. held-out (transfer check, no re-fitting)

| tier | discovery Spearman | held-out Spearman |
|---|---|---|
| none | None | None |
| light | -0.3836 | -0.3355 |
| full | 0.2011 | 0.1802 |
| deep | 0.9731 | 0.9057 |

## Isolate cost ledger

This run: 1080 isolate lifetimes, 29.20215s total (0.0270s/isolate-lifetime).

