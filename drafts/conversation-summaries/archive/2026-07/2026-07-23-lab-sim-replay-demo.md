# 2026-07-23 — Lab-sim plane replay demo

## Trigger

User wanted an interactive demo of the `lab-simulation` line letting them
switch between what the Agent/Admin/Audit/Oracle "planes" of the sim see
(observations, actions, internal state, files) and scroll through time.
After discussion, scope was fixed to: static, precomputed single-episode
replay (no live config), four stacked horizontal lanes sharing one
horizontal time axis, tick columns that widen on click, and an
Agent-action click that cross-highlights/expands the matching
Admin/Audit(tier)/Oracle entries with drawn connector lines. A detailed
plan was written to `/Users/GunnarZarncke/.cursor/plans/lab-sim_plane_replay_demo_067b5f48.plan.md`
(not edited this session) and then implemented in full, todo by todo.

## Done

- **Backend trace recorder** (additive, off by default):
  - `experiments/lab-simulation/lab_sim/world_visible/world.py`: `run_episode` gains an optional `trace_sink: Callable[[dict], None] | None = None` param, called once per tick after that tick's agent loop with everything already computed (`agent_records`, `host`, `engine`, `permissions`, `oracle`, `ws`, `model_id`, `last_deployed_model_id`). Zero cost / byte-identical when `None` (verified by a test).
  - New `experiments/lab-simulation/lab_sim/world_visible/trace_recorder.py`: `build_frame(...)` assembles the per-tick frame — `agents` (each actor's own observation/action/result + a display-only `event_n` join key), `admin` (unredacted this-tick log slice), `audit` (the SAME slice run through the existing `oracle_only/events.py` tier projections, one sub-view per `none`/`light`/`full`/`deep`, plus deep-only report/message/memo content fetches), `oracle` (`OracleWorld` ground truth). Placed in `world_visible/` rather than the plan's suggested `harness/` to avoid a needless cross-package import direction (no other change; noted here per AGENTS.md).
  - `config.py`: bumped `CODE_VERSION` to `lab-sim-0.12.0` with a docstring entry describing the additive hook; no referee/detector code touched.
  - New `experiments/lab-simulation/tests/harness/test_trace_recorder.py` (4 tests): read-only-tap digest equality, frame count/tier-nesting/`event_n` join correctness, deep-tier report-content surfacing on the d2-inflate scenario, and a plane-separation check (no `ORACLE_ONLY_FIELDS` leak into `admin`/`audit`, mirroring `test_planes.py`).
  - Full existing suite re-run (`pytest -k "not llm"`, ~380 tests) plus the new file: all pass.
- **Export script**: `experiments/lab-simulation/export_replay_trace.py` — runs `d2_lineage_config(inflate=True, T=40)`, seed 7, `MockIsolate`; writes `demos/ch07-lab-sim-replay/data/episode_trace.json` (frames + roster + an end-of-episode detector/severity scorecard reusing `oracle_only/detectors.py`/`severity.py` directly, no reimplementation).
- **Frontend demo**: `demos/ch07-lab-sim-replay/` (`index.html`, `app.ts`, `app.test.ts`, `README.md`, `data/episode_trace.json`), following the `ch17-lhv-learnability/` static-TS pattern:
  - Horizontal timeline of 40 tick-columns; collapsed state shows a thin 4-glyph strip per tick (Agent per-actor ok/denied dot, Admin activity dot, Audit dot colored by current tier's visibility incl. a distinct color for deep-only extras, Oracle hazard bar) — these glyph rows read as four continuous horizontal lanes across the whole timeline even when collapsed.
  - Click a tick → widens; shows one row per lane (Agent per-actor / Admin log / Audit(selected tier) log / Oracle models).
  - Click an Agent row → highlights + expands the matching Admin/Audit/Oracle entries via the trace's `event_n` join key, draws dashed SVG connector lines between them (agent → admin → audit → oracle, verified working in-browser).
  - Segmented `none`/`light`/`full`/`deep` toggle governs only the Audit lane.
  - End-of-episode scorecard table (5 detectors × 4 tiers + severity composite).
  - 16 unit tests (`app.test.ts`) for the pure join/glyph/label helpers; strict-mode `tsc --noEmit` clean; `esbuild` build clean (20.7kb); manually verified in a real browser via `cursor-ide-browser` (screenshots) that expand/highlight/connectors/deep-tier report reveal all work, and that the chosen scenario really does hide the misreport below `deep` (reported hazard 0.168 vs. oracle truth ~0.39-0.44 at various ticks) and only `deep` yields `misreporting_score`/`accumulation_score` = 1.0.
  - Registered in `demos/index.html` and `demos/README.md`'s "Current demos" table (Chapter 7 — *Finding the Boundary*).
- **Site integration** (`site/`, follow-up in the same session, "integrate the demo into the site — another agent was concurrently adding `demos/ch35-kappa-percolation/`"):
  - Confirmed via a subagent investigation that `demos/chNN-*` folders are auto-discovered by `site/scripts/sync-demos.mjs` (writes `src/data/demos.json`, backs `/demos/` and `demoFor()`) and copied to `public/chapter-demos/<id>/` by `site/scripts/lib/publish-chapter-demos.mjs` — no site code is required just to list a static demo.
  - **Bug found and fixed**: `publish-chapter-demos.mjs`'s `copyStaticDemo` only copied top-level files and explicitly skipped descending into subdirectories, so `demos/ch07-lab-sim-replay/data/episode_trace.json` (this demo's only subfolder, needed at runtime) never reached `public/chapter-demos/ch07-lab-sim-replay/data/` — the site-served demo would have 404'd on load. Fixed by making the copy recursive (skipping `tests/`, `__pycache__/`, `node_modules/`, `.pytest_cache/`, `.venv/`, and any dot-directory); verified no other existing demo needed this (none has a data subfolder) and that `ch01-scaffold-misuse`'s hybrid-backend copy path still behaves the same.
  - Added a `demos:` entry pointing at `ch07-lab-sim-replay` to the **body-file source of truth** for the `adversarial-boundary-discovery` concept card — `metadata/concepts/bodies/adversarial-boundary-discovery.md` — after discovering `site/src/content/cards/*.md` are themselves generated by `sync-concepts.mjs` from `metadata/concepts.yml` + `metadata/concepts/bodies/*.md` and get silently overwritten by any `npm run sync`/`npm run build`; an initial attempt to hand-edit the generated card file was clobbered by the very build that validated it, then corrected at the real source.
  - Improved the demo's `README.md` opening line to avoid embedding a raw `[text](url)` markdown link in the auto-extracted site summary (the sync script does not strip markdown syntax).
  - Verified end-to-end with a real `npm run build` + a local static server + `cursor-ide-browser`: `/chapter-demos/ch07-lab-sim-replay/` mounts and fetches its data (200 on `data/episode_trace.json`), `/cards/adversarial-boundary-discovery/`'s "Interactive demos" section links to it with the correct href, `/demos/` inventory lists all 6 demos including the concurrently-added `ch35-kappa-percolation`.
  - Confirmed minimal, non-conflicting footprint against the concurrent agent: only `site/scripts/lib/publish-chapter-demos.mjs` and `metadata/concepts/bodies/adversarial-boundary-discovery.md` ended up as tracked-file diffs from this integration; `demos/ch07-lab-sim-replay/`'s co-presence with the other agent's already-landed `demos/index.html`/`README.md` edits for `ch35-kappa-percolation` merged cleanly (both entries present, neither clobbered the other).

## Decisions

- `trace_recorder.py` lives in `world_visible/` (not `harness/` as the plan sketched) — purely to avoid `world_visible.world` importing from `harness` (which itself sometimes imports `world_visible.world`); no functional difference, `harness/__init__.py` is a docstring-only module so the risk was low either way, but the safer direction was free to take.
- Audit-tier per-tick views are computed on **this tick's log slice only** (not cumulative history) — matches the demo's "same event, four ways, one tick at a time" framing and keeps the JSON from duplicating history at every frame.
- `event_n` is explicitly documented (module docstring, README, code comments) as a demo-only join key, not a new real-sim field, per the plan's honesty requirement.
- Collapsed-tick glyphs double as the "tight summary lets you anticipate content" requirement: even before any click, the four glyph rows already read as four persistent horizontal lanes.

## Open / next

- Nothing outstanding from the plan; all 9 todos completed, plus the follow-up site-integration request.
- Possible future polish (not requested): trimming `episode_trace.json`'s ~667KB size (mostly per-tick observation-dict duplication) if the demo is ever bundled more aggressively; a `results/`-style note if this replay is ever cited from the manuscript (currently demo-only, not wired into `book.tex` per repo convention).
- Site build was validated locally (`npm run build`, `dist/` served + browser-checked) but not committed/deployed; `site/dist/`, `site/src/data/*.json`, and `site/public/search-index.json`/`chapter-demos/` are generated/gitignored and were left as regenerated by the local run.

## Key paths

- `experiments/lab-simulation/lab_sim/world_visible/{world.py,trace_recorder.py,config.py}`
- `experiments/lab-simulation/tests/harness/test_trace_recorder.py`
- `experiments/lab-simulation/export_replay_trace.py`
- `demos/ch07-lab-sim-replay/`
- `site/scripts/lib/publish-chapter-demos.mjs` (recursive static-demo copy fix)
- `metadata/concepts/bodies/adversarial-boundary-discovery.md` (added `demos:` entry — the actual source; `site/src/content/cards/adversarial-boundary-discovery.md` is generated from it)
- Plan: `/Users/GunnarZarncke/.cursor/plans/lab-sim_plane_replay_demo_067b5f48.plan.md`

## Commits

- None made this session (not requested).
