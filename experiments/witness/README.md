# Witness annex

Not a simulation line. Frozen **deployment-witness** protocols, fixtures, and findings for the Witness lane ([`drafts/plans/witness.md`](../../drafts/plans/witness.md)).

**Claim strength:** methodology-building. A layer **fail** or **refuse** is the paid outcome. H0 sims remain backing only.

| Phase | Protocol | Findings |
|-------|----------|----------|
| 0 | [`drafts/plans/witness-phase0.md`](../../drafts/plans/witness-phase0.md) | (scope only) |
| 1 | [`drafts/plans/witness-phase1.md`](../../drafts/plans/witness-phase1.md) | W-1 H1 C2 mock; W-2 H4 MASK refuse |
| 2 | [`drafts/plans/witness-phase2.md`](../../drafts/plans/witness-phase2.md) | W-3 H2 Linux (v1.2.0); W-4 H3 Wikipedia (v1.1.0) |

```bash
python3 experiments/witness/check_c2_mock.py
python3 experiments/witness/check_h2.py
python3 experiments/witness/check_h3.py
```

Ledger: [`results/FINDINGS.md`](results/FINDINGS.md). Prefix **`W-`**.
