# Safety-check backtests

A **backtest** here is a frozen safety check run on a history we did not write. Freeze the check, run it on a real stretch whose outcome is already known, and ask whether it would have stayed green. The backtest is witnessing the failure: the check stayed green while the harm continued.

**What this buys the project.** Lean and the authored simulations can show that a check-shape is sayable and that it works in a world we wrote. They cannot pay a safety-case leaf on a process we did not design. Backtests make that remainder visible as fail, refuse, or null. Construction chapters stay out of the v1 manuscript until a real stop exists on such a history.

**Why fail is the result we came for.** The usual eval lie is building the check and the toy world together. Foreign host traces break that loop. On Linux, `Reviewed-by` was present on 17,047 of 60,176 SHAs that later received a developer-labeled bug-introducing commit — a layer fail, not a broken test. That is an analogy for correction-channel check-shapes, not a measurement of an AI system.

Finding prefix **`W-`**. Lane plan: [`drafts/plans/backtest.md`](../../drafts/plans/backtest.md).

**Companion site:** one card per test under `/cards/experiment/w-1/` … `/w-17/`, listed from [Backtests](https://towards-alignment.com/cards/experiment/backtests/). Combined ledger: [`results/FINDINGS.md`](results/FINDINGS.md).

**Layout.** Code, fixtures, and large host dumps share [`experiments/backtest/`](.). Splitting into per-test folders is deferred: the kernel clone, OSF dumps, and shared `check_h5_trees.py` fixtures are not worth duplicating until a test needs its own pin.

**Methodology:** [`docs/METHODOLOGY.md`](../../docs/METHODOLOGY.md) § Backtests.

| Phase | Protocol | Findings |
|-------|----------|----------|
| 0 | [`drafts/plans/backtest-phase0.md`](../../drafts/plans/backtest-phase0.md) | (scope only) |
| 1 | [`drafts/plans/backtest-phase1.md`](../../drafts/plans/backtest-phase1.md) | W-1 H1 C2 mock; W-2 H4 MASK refuse |
| 2 | [`drafts/plans/backtest-phase2.md`](../../drafts/plans/backtest-phase2.md) | W-3 Linux; W-4 Wikipedia |
| 3 | [`drafts/plans/backtest-phase3.md`](../../drafts/plans/backtest-phase3.md) | W-5 Moral Machine bundle; W-6 Arena×MASK selector |
| 4 | [`drafts/plans/backtest-phase4.md`](../../drafts/plans/backtest-phase4.md) | W-7 C-004 leftovers; W-8 Lean C2 pin; W-9–W-11 H5 trees |
| C-004 raw | [`drafts/plans/backtest-c004-raw.md`](../../drafts/plans/backtest-c004-raw.md) | W-12 Moral Machine raw same-unit geometry |
| C-004 PDG | [`drafts/plans/backtest-c004-pdg.md`](../../drafts/plans/backtest-c004-pdg.md) | W-13 PDG refuse |
| C-004 CPC | [`drafts/plans/backtest-c004-cpc.md`](../../drafts/plans/backtest-c004-cpc.md) | W-14 CPC2015 Exp. 1 null |
| C-004 SCOTUS | [`drafts/plans/backtest-c004-scotus.md`](../../drafts/plans/backtest-c004-scotus.md) | W-16 SCDB justice geometry pass |
| H7 Moltbook MB7a | [`drafts/plans/backtest-v2-moltbook-mb7a.md`](../../drafts/plans/backtest-v2-moltbook-mb7a.md) | W-17 structure_stop (Tier A broadcast substrate) |
| Phase 5 | [`drafts/plans/backtest-phase5.md`](../../drafts/plans/backtest-phase5.md) | W-15 CIRIS stack C2 null P3 |

```bash
python3 experiments/backtest/check_c2_mock.py
python3 experiments/backtest/check_h2.py
python3 experiments/backtest/check_h3.py
python3 experiments/backtest/check_h4_bundle.py
python3 experiments/backtest/check_h4_selector.py
python3 experiments/backtest/check_h5_trees.py
python3 experiments/backtest/check_h4_mm_raw.py
python3 experiments/backtest/check_h4_pdg.py
python3 experiments/backtest/check_h4_cpc2015.py
python3 experiments/backtest/collect_h4_scotus.py
python3 experiments/backtest/check_h4_scotus.py
python3 experiments/backtest/fetch_h7_moltbook_cache.py
python3 experiments/backtest/collect_h7_moltbook_mb7a.py
python3 experiments/backtest/check_h7_moltbook_mb7a.py
python3 experiments/backtest/collect_c2_stack.py
python3 experiments/backtest/check_c2_stack.py
```

Lean pin: `lake build` in `formal/` (module `BacktestC2Instance`).

Ledger: [`results/FINDINGS.md`](results/FINDINGS.md). Prefix **`W-`**.
