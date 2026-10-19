# Conversation log index

**Start here:** [HANDOFF.md](HANDOFF.md) (aggregated themes and open work).

**Recent sessions** (15 newest in this folder). Older: [archive/](archive/README.md).

| Date | Topic | Log |
|------|-------|-----|
| 2026-10-19 | **Last Safety play telemetry** — Add tracking to the game using the companion site mechanism; record fuel, room id, NPC id, knowle... | [2026-10-19-last-safety-play-telemetry.md](2026-10-19-last-safety-play-telemetry.md) |
| 2026-10-19 | **Last Safety glossary and leads** — Playtest confusion on the job-queue glossary. Hide that lesson on the first pack, keep the deep d... | [2026-10-19-last-safety-glossary-leads.md](2026-10-19-last-safety-glossary-leads.md) |
| 2026-10-16 | **Last Safety O-41 concept links** — Per-fact optional TSA companion card links (O-41): phone setting, room footer line, persistence, ... | [2026-10-16-last-safety-concept-links.md](2026-10-16-last-safety-concept-links.md) |
| 2026-10-16 | **Claim-extract combined queue** — Extend the claim-extract plan with spine-name vs informal-warrant lenses and a combined chapter o... | [2026-10-16-claim-extract-queue.md](2026-10-16-claim-extract-queue.md) |
| 2026-10-16 | **Ch. 1 claim extract and analysis** — Perform the claim extract and analysis for Chapter 1 (first in the combined queue). | [2026-10-16-ch01-claim-extract.md](2026-10-16-ch01-claim-extract.md) |
| 2026-10-15 | **Last Safety Welcome until 11:00** — Welcome ended on the first sentence to Ian, so simulated play spent almost all of its fuel in Dou... | [2026-10-15-last-safety-welcome-until-eleven.md](2026-10-15-last-safety-welcome-until-eleven.md) |
| 2026-10-15 | **Last Safety transcript reveal and composer focus** — After send, the transcript should scroll smoothly and reveal NPC reply one sentence per second (n... | [2026-10-15-last-safety-transcript-reveal-focus.md](2026-10-15-last-safety-transcript-reveal-focus.md) |
| 2026-10-15 | **Last Safety /text.html browser fix** — `/text.html` showed the input line but no log output (not even initial room text or `help`). User... | [2026-10-15-last-safety-text-html-fix.md](2026-10-15-last-safety-text-html-fix.md) |
| 2026-10-15 | **Last Safety start screen** — Add a pre-game start screen that drops the player into the scenario: task, short-notice framing, ... | [2026-10-15-last-safety-start-screen.md](2026-10-15-last-safety-start-screen.md) |
| 2026-10-15 | **Last Safety room UI and mobile handset** — Room chat layout, completion latency investigation, Lab Access notification clarity, narrow-viewp... | [2026-10-15-last-safety-room-ui-mobile.md](2026-10-15-last-safety-room-ui-mobile.md) |
| 2026-10-15 | **Last Safety public-hosting hardening** — Prompts: paraphrase only (no prompt id). User asked for a safety review of the game for public ho... | [2026-10-15-last-safety-public-hosting-hardening.md](2026-10-15-last-safety-public-hosting-hardening.md) |
| 2026-10-15 | **Last Safety photo pipeline and transcript collapse** — Follow-up on handset/room UX: photos not viewable or black; transcript log should hide off-input ... | [2026-10-15-last-safety-photo-transcript-fixes.md](2026-10-15-last-safety-photo-transcript-fixes.md) |
| 2026-10-15 | **Last Safety onboarding hints** — Playtests: people wander, miss what they can do, and do not realize speaking and the phone are th... | [2026-10-15-last-safety-onboarding-hints.md](2026-10-15-last-safety-onboarding-hints.md) |
| 2026-10-15 | **Last Safety NPC dialogue and DM phrasing** — Explain the reply pipeline (parse → engine → phrasing), what is not phrased, and why dialogue fel... | [2026-10-15-last-safety-npc-dialogue-dm-phrasing.md](2026-10-15-last-safety-npc-dialogue-dm-phrasing.md) |
| 2026-10-15 | **Last Safety NPC click addressee** — In the 3D room, clicking an NPC still selected them for floor movement (leftover from testing). C... | [2026-10-15-last-safety-npc-click-addressee.md](2026-10-15-last-safety-npc-click-addressee.md) |

## Archive by month

- **2026-10** (76): [2026-10-INDEX.md](archive/2026-10-INDEX.md)
- **2026-09** (101): [2026-09-INDEX.md](archive/2026-09-INDEX.md)
- **2026-08** (194): [2026-08-INDEX.md](archive/2026-08-INDEX.md)
- **2026-07** (264): [2026-07-INDEX.md](archive/2026-07-INDEX.md)
- **2026-06** (202): [2026-06-INDEX.md](archive/2026-06-INDEX.md)

## Maintenance

- Roll older logs: `python3 scripts/archive_conversation_summaries.py` (keeps 15 in root).
- Prune superseded logs: `python3 scripts/prune_superseded_conversation_logs.py --apply`.
- Rules: [README.md](README.md).

