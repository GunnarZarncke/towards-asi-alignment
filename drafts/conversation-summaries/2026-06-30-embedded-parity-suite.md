# 2026-06-30 — Embedded parity suite + reports

## Trigger
Bring embedded-simulation on par with toy-sim: LLM redteam, sweeps, reports, overall summary.

## Done
- `embedded_sim/batch.py` — instrumentation matrix, frozen validation, parameter sweep, red-team battery, main report helpers.
- `run_suite.py` — batch CLI (`--all`, `--battery`, `--llm-live`, etc.).
- `embedded_llm/` — LLM episodic red-team (patches `correction.jsonl`; reuses toy `llm_client`).
- `write_overall_summary.py` — aggregates all `results/*.json` into `OVERALL_SUMMARY.md`.
- **Full suite run** (T=800): matrix, frozen (seeds 21–30), sweep, battery (1260 runs), main report, live LLM (21 episodes).

## Key numbers
- Hand-written battery: **0% false-pass** (1260 runs, 775s) vs toy-sim **35%** at T=2000.
- Live LLM red-team: **0% false-pass** (21 runs, gpt-4o-mini, ~$0.017).
- Main report (full_redteam): **0/13 false passes**; outer certifies 11/13.
- Frozen validation: **80%** in-sim correct across bridges/seeds.

## Open
- ~~`minimum_certifiable_level` counts `none`~~ — fixed in methodology pass (handles-only, 0.95 threshold).
- Postponed product decisions unchanged (MB5 gate, unit-scope vs global CCI).

## Commits
- `13454bb` — embedded parity suite + toy methodology alignment (see [2026-06-30-embedded-methodology-ontology.md](2026-06-30-embedded-methodology-ontology.md))

## Paths
- `results/OVERALL_SUMMARY.md`
- `run_suite.py`, `embedded_sim/batch.py`, `embedded_llm/`
