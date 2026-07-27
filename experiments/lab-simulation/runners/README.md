# Runners

Battery and protocol entry points live here instead of the lab-simulation root.

| Folder | Contents |
|--------|----------|
| [`et4_secret_loyalties/`](et4_secret_loyalties/) | ET-4 — see [`../README_ET4_secret_loyalties.md`](../README_ET4_secret_loyalties.md) |
| [`phases/`](phases/) | Phase 6–9 pre-registered batteries |
| [`batteries/`](batteries/) | D-line ecology batteries, handle calibration, stall diagnosis |
| [`uad/`](uad/) | S5–S7 UAD / blind detector line |
| [`llm_detectors/`](llm_detectors/) | LLM detector stress and stats validation |
| [`llm_discovery/`](llm_discovery/) | Phase 10 LLM coordination discovery |
| [`prototypes/`](prototypes/) | S1–S4 scenario prototypes and one-off probes |
| [`et3/`](et3/) | ET-3 AI 2027 reproduction (uses [`../external/`](../external/)) |

Run from `experiments/lab-simulation`:

```bash
python3 runners/et4_secret_loyalties/run_et4_secret_loyalty.py --stage confirmatory
python3 -m pytest
```

Shared paths: `runners/_paths.py` (`RESULTS_DIR`, `EXTERNAL_DIR`, `REPO_ROOT`).

Ephemeral per-episode workspace dirs live under gitignored `runs/` (separate from this tree).
