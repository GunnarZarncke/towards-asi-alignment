# 2026-11-04 — Graded-lab PLAN v3 closure documented across repo

kind: housekeeping
uptake: status

## Trigger
User confirmed PLAN v3 is closed and asked to document that clearly across files and pages (including graded-lab v3 leftover TODO items).

Prompts: (paraphrase — no prompt id in thread)

## Done
- housekeeping: **`docs/EXPERIMENTS.md`** §5 — v3 closed GL-78; v4 active; REPRODUCTION.md reframed as post-v3 backlog.
- housekeeping: **`metadata/experiments.yml`** — role text no longer says v3 institutional runtime is active.
- housekeeping: **`metadata/TODO.md`** — graded-lab v3 leftover items renamed to post-v3 closure housekeeping with GL-78 pointer.
- housekeeping: **`experiments/graded-lab-simulation/REPRODUCTION.md`** — GL-78 update; §1–§4 marked delivered; §6–§7 descoped/deferred; status key fixed.
- housekeeping: **`DESIGN.md`**, **`README.md`**, **`COLLABORATION.md`**, **`experiments/TODO.md`** — program map / active vs closed.
- content: **`appendices/appN-experimental-evidence.tex`** — v3 closed via `finding~\ref{finding:gl-78}`; added GL-78 table row; v4 active in lede.
- housekeeping: **`npm run sync:experiments`** — site `experiments.json` + experiment cards updated.

## Open
- Post-v3 housekeeping TODOs remain in `metadata/TODO.md` (audit vocabulary drift; Q1 cascade doc pass).

## Verification
- `cd site && npm run sync:experiments` → `Wrote src/data/experiments.json from metadata/experiments.yml`
