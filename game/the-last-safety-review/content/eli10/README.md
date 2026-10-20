# ELI10 (explain like I'm 10)

Player-facing simplifications for **The Last Safety Review**. Off by default; enable **Explain like I’m 10 (ELI10)** in Lab Access → Settings. Served by `POST /api/eli10` (`lib/eli10.mjs`) when `eli10Enabled` is true on the session.

| Source | Where it lives |
| --- | --- |
| Catalog documents | `documents/<slug>.md` (same pack conditionals as `content/documents/` via `renderDocumentSource`) |
| Engine fact sentences | `facts.mjs` (one line per fact id) |
| Room screens and notes | `eli10` field on `SCREENS` / `ROOM_NOTES` in `lib/game.mjs` |
| Model-phrased NPC replies | OpenAI at runtime (`explainLikeTen` in `lib/llm.mjs`, up to 720 output tokens) |

Edit the prepared files here; do not hand-edit served phone copies.
