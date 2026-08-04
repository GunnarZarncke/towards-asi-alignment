# Changelog

Milestones for embedded-simulation. Package version: `embedded_sim.__version__`
(currently `0.1.0` in `embedded_sim/__init__.py`). No separate `CODE_VERSION`
cache key — scenario batteries pin digests in tests instead.

Finding / negative ledger: [`results/NEGATIVE_RESULTS.md`](results/NEGATIVE_RESULTS.md).

| Doc | Role |
|-----|------|
| [`embedded_sim/__init__.py`](embedded_sim/__init__.py) | Self-contained architecture overview |
| [`MILESTONE-v5-goal-agents.md`](MILESTONE-v5-goal-agents.md) | Spawn plan for goal-agent line (separate repo folder) |

Entries are **newest first**.

---

## 2026-07 (ongoing maintenance)

- Handle registry expansion, eligibility batteries, channel MI scans (ES-3–12+ in negative ledger).
- AppD handle kernels, certification artifacts, safety-case scaffolding.

## 2026-06-30 — line launch

- Embedded auditor on VFS artifacts via Python/Node **isolate bridge**.
- Three-plane separation: micro-sim truth → projected VFS → embedded audit → outer eval.
- UAD unit discovery, scoped CCI, MB5 deploy gate, referent drift scenarios.
- 13 MB bridge scenarios + red-team strategies; default-ecology 0% false-pass at T=400.
- **ES-1:** Default ecology UAD equals loudest-actor heuristic (recorded negative).

## Prior

- Methodological precursor patterns ported from toy/agency-detect (MI/CMI boundary detection, handle tiers).
