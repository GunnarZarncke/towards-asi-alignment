# Continuity & Drift Study — orchestrator workspace (shareable)

Comparative study of continuity and drift in long-lived organizations.

This folder holds **deployable packets**, gate metadata, and audit logs. It does **not** contain the study's sealed theory, decoder, or directional hypotheses. Sub-agents receive one packet in their prompt; they must not be given this README as if it were their task.

## Status

- **Phase:** 1.1 union (366 names) + 1.3 precision **catalog complete** (366/366 in `phase1/precision/results.tsv`; usable 260). Protocol leftovers (gate packets, holdout, Phase 2) are separate.
- **Frozen (deployable):** see `gate/FROZEN.md` (logs 6.1a/b, 6.3a/b, lister, complaint-office staffing log)
- **Do not deploy:** `packets/bundle-*.md` (failed gate)
- **Collusion margin:** 2 packets
- **Gate:** `gate/PROTOCOL.md`

## Invariants (routing)

Deploy a packet only if it passed the gate and matches its frozen hash. Orchestrator does not list, bound, grade, or log cases. No worker holds predictors and outcomes together, or more packets than the collusion margin.
