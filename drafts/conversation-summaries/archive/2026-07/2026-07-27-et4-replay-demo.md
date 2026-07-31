# 2026-07-27 — ET-4 replay demo and trace export

## Trigger
User asked to implement ET-4 trace export and case-brief extensions to the
lab-sim replay UI, then end session and commit (excluding the ~8 MB trace
JSON).

## Done
- Added `experiments/lab-simulation/export_et4_replay_traces.py` — exports
  organism, content-matched control, and remediation variants (seed 201) plus
  evidence anchors and confirmatory aggregate metadata.
- Extended `demos/ch07-lab-sim-replay/app.ts` with ET-4 case brief mode:
  variant tabs, evidence anchor cards, aggregate strip, ET-4 scorecard, and
  demo hub (classic D2 + ET-4 tabs).
- Updated demo README, `demos/index.html`, and hackathon report demo URL.
- Ignored generated `data/et4_case_brief.json` in `demos/.gitignore`.
- Built `app.js`; all 36 demo vitest tests pass.

## Decisions
- Do **not** commit `et4_case_brief.json` (~8 MB); regenerate locally via
  `export_et4_replay_traces.py`. Demo falls back to classic replay if the
  file is missing.
- Did not stage `experiments/lab-simulation/ET4-context/` (user-added hackathon
  reference material, outside this task).

## Open / next
- Run `python3 export_et4_replay_traces.py` before serving ET-4 demo locally.
- Optional: gzip or tick-window trim if reviewers need a committed smaller bundle.
- `ET4-context/` remains untracked if the user wants it in-repo separately.

## Key paths
- `experiments/lab-simulation/export_et4_replay_traces.py`
- `demos/ch07-lab-sim-replay/app.ts` — `mountEt4CaseBriefDemo`, `mountDemoHub`
- `demos/ch07-lab-sim-replay/README.md` — serve URLs and regen commands
- `experiments/lab-simulation/results/et4_hackathon_report.md`

## Commits
- `ac79283a` Add ET-4 case-brief replay demo and trace export
