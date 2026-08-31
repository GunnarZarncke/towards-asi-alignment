# Witness annex

Not a simulation line. Frozen **deployment-witness** protocols, fixtures, and findings for the Witness lane ([`drafts/plans/witness.md`](../../drafts/plans/witness.md)).

**Companion site:** one card per test under `/cards/experiment/w-1/` … `/w-16/`, listed from [Witness](https://towards-alignment.com/cards/experiment/witness-tests/). Combined ledger: [`results/FINDINGS.md`](results/FINDINGS.md).

**Layout.** Code, fixtures, and large host dumps currently share [`experiments/witness/`](.). Splitting into `experiments/witness-<name>/` per test is deferred: the kernel clone, OSF dumps, and shared `check_h5_trees.py` fixtures are not worth duplicating until a test needs its own pin.

**Claim strength:** methodology-building. A layer **fail** or **refuse** is the paid outcome. H0 sims remain backing only.

**Methodology:** [`docs/METHODOLOGY.md`](../../docs/METHODOLOGY.md) § Witness tests.

| Phase | Protocol | Findings |
|-------|----------|----------|
| 0 | [`drafts/plans/witness-phase0.md`](../../drafts/plans/witness-phase0.md) | (scope only) |
| 1 | [`drafts/plans/witness-phase1.md`](../../drafts/plans/witness-phase1.md) | W-1 H1 C2 mock; W-2 H4 MASK refuse |
| 2 | [`drafts/plans/witness-phase2.md`](../../drafts/plans/witness-phase2.md) | W-3 Linux; W-4 Wikipedia |
| 3 | [`drafts/plans/witness-phase3.md`](../../drafts/plans/witness-phase3.md) | W-5 Moral Machine bundle; W-6 Arena×MASK selector |
| 4 | [`drafts/plans/witness-phase4.md`](../../drafts/plans/witness-phase4.md) | W-7 C-004 leftovers; W-8 Lean C2 pin; W-9–W-11 H5 trees |
| C-004 raw | [`drafts/plans/witness-c004-raw.md`](../../drafts/plans/witness-c004-raw.md) | W-12 Moral Machine raw same-unit geometry |
| C-004 PDG | [`drafts/plans/witness-c004-pdg.md`](../../drafts/plans/witness-c004-pdg.md) | W-13 PDG refuse |
| C-004 CPC | [`drafts/plans/witness-c004-cpc.md`](../../drafts/plans/witness-c004-cpc.md) | W-14 CPC2015 Exp. 1 null |
| C-004 SCOTUS | [`drafts/plans/witness-c004-scotus.md`](../../drafts/plans/witness-c004-scotus.md) | W-16 SCDB justice geometry pass |
| H7 Moltbook MB7a | [`drafts/plans/witness-v2-moltbook-mb7a.md`](../../drafts/plans/witness-v2-moltbook-mb7a.md) | W-17 reserved; frozen, pending collect |
| Phase 5 | [`drafts/plans/witness-phase5.md`](../../drafts/plans/witness-phase5.md) | W-15 CIRIS stack C2 null P3 |

```bash
python3 experiments/witness/check_c2_mock.py
python3 experiments/witness/check_h2.py
python3 experiments/witness/check_h3.py
python3 experiments/witness/check_h4_bundle.py
python3 experiments/witness/check_h4_selector.py
python3 experiments/witness/check_h5_trees.py
python3 experiments/witness/check_h4_mm_raw.py
python3 experiments/witness/check_h4_pdg.py
python3 experiments/witness/check_h4_cpc2015.py
python3 experiments/witness/collect_h4_scotus.py
python3 experiments/witness/check_h4_scotus.py
python3 experiments/witness/collect_c2_stack.py
python3 experiments/witness/check_c2_stack.py
```

Lean pin: `lake build` in `formal/` (module `WitnessC2Instance`).

Ledger: [`results/FINDINGS.md`](results/FINDINGS.md). Prefix **`W-`**.
