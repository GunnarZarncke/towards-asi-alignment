# Writer-compromise scenario prototype (2026-07-09)

CODE_VERSION `lab-sim-0.11.0`. Exploratory, `MockIsolate`, 10 seeds x 2 engineer-weight regimes (honest / deceptive) -- not a battery.

## Predictions

- P1_naive_tamper_always_detected: **True**
- P2_self_consistent_tamper_caught_one_entry_later: **True**
- P3_forward_recompute_tamper_undetectable_by_chain_alone: **True**
- P4_engine_log_has_no_partial_detection: **True**
- P5_oracle_severity_unaffected_by_log_tamper: **True**

## What this means

- `access_log`/`events` (both `EventLog`-backed, per-entry hash-chained): a tamper is caught immediately UNLESS the writer also recomputes every downstream entry's hash -- a full log-rewrite capability, not a one-field edit, is undetectable by `verify_chain()` alone.
- `engine_log` (flat whole-list digest, no per-entry chain): strictly weaker -- ANY single-entry edit is invisible the moment the writer republishes a consistent digest; there is no 'caught one entry later' middle ground at all.
- Oracle-computed severity (`severity.score_episode`) never reads any of the three logs, so it is immune to all of this by construction -- only an AUDIT-TIER detector that trusts log content as evidence can be fooled by a compromised writer.

