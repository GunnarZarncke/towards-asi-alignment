# 2026-07-27 — Lab-sim cleanup, ET-4 docs, hackathon context

## Trigger

End-of-session commit: reorganize lab-simulation layout (runners tree, blind
protocol co-location), add ET-4 README, move hackathon context to `context/`,
and land demo/doc updates from the ET-4 hackathon workstream.

## Done

- Moved 47 root `run_*.py` scripts into `experiments/lab-simulation/runners/`
  with subfolders (`et4_secret_loyalties/`, `phases/`, `batteries/`, `uad/`,
  `llm_detectors/`, `llm_discovery/`, `prototypes/`, `et3/`) and shared
  `runners/_paths.py` bootstrap.
- Kept gitignored `runs/` for ephemeral episode workspaces only (not runners).
- Co-located `BLIND_GENERATION_ROUND2.md` → `lab_sim/agent_visible/`,
  `BLIND_DETECTOR_GENERATION.md` → `lab_sim/oracle_only/`; updated pointers.
- Added `README_ET4_secret_loyalties.md`; lightened main `README.md`.
- Moved `ET4-context/` → `context/ET4-context/` with index README and filled
  `et4-hackathon-submission.md`.
- Added `external/README.md` (vendor annex policy); moved
  `et3_reverse_smoke.json` to `results/`.
- ET-4 replay demo legibility pass (BB label, tier tooltip, condensed glyphs).
- Updated tests/imports for runner and blind-protocol paths.

## Decisions

- **Main repo + pinned commit** for hackathon source (no dedicated extract repo).
- **`runners/` not `runs/`** — `runs/` already gitignored for episode temp dirs.
- **Blind protocol filenames unchanged** — provenance strings in JSON/tests stay valid.
- **Early `approve_review` attempts** — intentional pipeline behavior; document only.

## Open / next

- Polish hackathon submission prose (user-edited draft has placeholders).
- Pin release tag for hackathon submitters if desired (`et4-hackathon-2026`).
- Regenerate local `et4_case_brief.json` before demo serve (gitignored).

## Key paths

- `experiments/lab-simulation/runners/et4_secret_loyalties/`
- `experiments/lab-simulation/README_ET4_secret_loyalties.md`
- `context/ET4-context/et4-hackathon-submission.md`
- `experiments/lab-simulation/PLAN_ET4.md`
- `demos/ch07-lab-sim-replay/`

## Commits

- (this session)
