# `lab_sim/oracle_only/` — tier 3 (full incl. oracle)

The highest non-harness grade: tier 1 + tier 2 + everything here — true
state and referee/detection logic. See
[`../../ACCESS_TIERS.md`](../../ACCESS_TIERS.md) for the full four-tier
scheme and rationale.

| File | What it is |
| --- | --- |
| `oracle.py` | Models (true capability/hazard), bearer harm, provenance ledger |
| `severity.py` | Referee: continuous severity components + never-events (full oracle access) |
| `detectors.py` | 5 tier-gated detector families over `AuditView` |
| `twins.py` | Full-surface honest-twin transform |
| `escalation.py` | Screen -> bounded query -> artifact-grounded contradiction ladder |
| `events.py` | Generic hash-chained `EventLog` + tier projection (none/light/full/deep) |
| `handles.py` | Handle registry (owner/operation/anchor/evasion story) + `HandleService` + invocation ledger |
| `bearer.py` | Welfare bundle: health (deployed-model bearer) + stress (lab-staff bearer), referee-neutral |
| `uad.py` | Undetected-adversarial-drift / coalition discovery signal |
| `collusion.py` | Collusion signal score over detected coalitions |
| `playbook_claim.py` | Playbook-claim gap score (facade detection) |

This is the referee's own view: ground truth, detection logic, and the
handle/bearer internals whose leakage would let a grantee directly read
off what the detectors check for or what a handle's real evasion story is.
`handles.py`/`bearer.py` in particular mix host-called mechanism with
referee-only secrets (see `ACCESS_TIERS.md`'s "judgment calls" section) —
both ship here whole, as the safe default.
