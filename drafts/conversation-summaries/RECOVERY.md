# Pruned session logs (recovery index)

One line per log removed because a **later session log** superseded it (not because the work landed in code alone). Full text: `git log -- drafts/conversation-summaries/` or `git show <commit>:<path>`.

## Prune run 2026-07-31

- `2026-07-25-tier-b-field-news-partial.md` **Tier B field news (partial)** — **Site:** three new roster entries in `metadata/field-news.yml` + bodies (`cltr-scheming-wild-mar-2026`, `meta-openclaw-feb-2026`, `claud... (superseded; see later session in git)
- `2026-07-25-tier-a-field-news.md` **Tier A field news (manuscript + site)** — **Site:** `metadata/field-news.yml` + six body files; `site/scripts/sync-field-news.mjs`; `"news"` card type; `/news/` index; chapter-car... (superseded; see later session in git)
- `2026-07-23-et2-cil-adapter-build.md` **ET-2 (CIL) adapter + scorer built; live smoke run blocked by sandbox** — Retried the `external/cil/.venv` install multiple times with (superseded; see later session in git)
- `2026-07-23-et1-colosseum-sc-claude-positive-control.md` **ET-1 Colosseum SC positive control (Claude Sonnet 4.5)** — Installed `anthropic` into `external/orbit/.venv` (missing dependency for the Anthropic provider). (superseded; see later session in git)
- `2026-07-23-et1-colosseum-attack-simple.md` **ET-1 Colosseum Attack (simple) — decisive channel-independence finding** — Rewrote ET-1 harvest sentences in `PLAN_ET1.md` and `DESIGN.md` (§"PLAN ET-1 pre-registration") to state the scored, mechanistically-expl... (superseded; see later session in git)
- `2026-07-20-et1-colosseum-sc-battery.md` **ET-1 Colosseum Control (SC) battery** — Added `scripts/run_et1_colosseum_battery.py` — DCOP path via `JiraTicketScenario().build_task(use_blackboard=True, collusion_mode=channel... (superseded; see later session in git)
- `2026-07-18-graded-lab-plan-v4-v0-v1-v2-implementation.md` **Graded lab PLAN_v4: V4-0/V4-1/V4-2 implemented for R-MB1 + R-MB4 (GL-79)** — **V4-0 (fixture layer + rig contract):** (superseded; see later session in git)
- `2026-07-06-lab-simulation-freeze-review.md` **Lab-layer simulation: pre-freeze review + monitor signal, perturbation hooks, tool registry** — **Audit-visible monitoring signal**: `OracleWorld.monitor_signal()` — (superseded; see later session in git)
- `2026-07-06-lab-simulation-d4-d1-comms-file-channel.md` **Lab-layer sim D4/D1 built: comm protocol, committee mechanics, file channel + persistent state** — **D4 comm substrate** (`comms.py`, new): TalkJS-derived (superseded; see later session in git)
- `2026-07-06-lab-simulation-d3-ecology-notes.md` **Lab-layer simulation: D3 realistic-ecology design notes recorded (no code)** — **Recorded, no code written.** New section "D3 design notes — realistic (superseded; see later session in git)
- `2026-07-05-lab-simulation-phase2-5.md` **Lab-layer simulation (4th line): Phases 2-5 (referee freeze)** — **Phase 2 (access control)**: `access.py` (`PermissionService`: (superseded; see later session in git)

