# Witness annex

Not a simulation line. Frozen **deployment-witness** protocols, fixtures, and findings for the Witness lane ([`drafts/plans/witness.md`](../../drafts/plans/witness.md)).

**Claim strength:** methodology-building. A layer **fail** or **refuse** is the paid outcome. H0 sims remain backing only.

| Phase | Protocol | Findings |
|-------|----------|----------|
| 0 | [`drafts/plans/witness-phase0.md`](../../drafts/plans/witness-phase0.md) | (scope only) |
| 1 | [`drafts/plans/witness-phase1.md`](../../drafts/plans/witness-phase1.md) | W-1 H1 C2 mock; W-2 H4 MASK refuse |
| 2 | [`drafts/plans/witness-phase2.md`](../../drafts/plans/witness-phase2.md) | W-3 Linux; W-4 Wikipedia |
| 3 | [`drafts/plans/witness-phase3.md`](../../drafts/plans/witness-phase3.md) | W-5 Moral Machine bundle; W-6 Arena×MASK selector |
| 4 | [`drafts/plans/witness-phase4.md`](../../drafts/plans/witness-phase4.md) | W-7 C-004 leftovers; W-8 Lean C2 pin; W-9–W-11 H5 trees |
| C-004 raw | [`drafts/plans/witness-c004-raw.md`](../../drafts/plans/witness-c004-raw.md) | W-12 Moral Machine raw same-unit geometry |

```bash
python3 experiments/witness/check_c2_mock.py
python3 experiments/witness/check_h2.py
python3 experiments/witness/check_h3.py
python3 experiments/witness/check_h4_bundle.py
python3 experiments/witness/check_h4_selector.py
python3 experiments/witness/check_h5_trees.py
python3 experiments/witness/check_h4_mm_raw.py
```

Lean pin: `lake build` in `formal/` (module `WitnessC2Instance`).

Ledger: [`results/FINDINGS.md`](results/FINDINGS.md). Prefix **`W-`**.
