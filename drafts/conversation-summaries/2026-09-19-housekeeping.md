# 2026-09-19 — Housekeeping / erasure + predictions catalog

## Trigger
User asked for housekeeping/erasure; then predictions `relatedBridges` cleanup and empty resolver slots.

## Done
- Reverted timestamp-only `site/src/data/chapter-reading-graph.json` drift.
- Compacted HANDOFF **Recently shipped** (merged predictions + spring-map bursts; rolled Sep 4–13 detail to archive pointers).
- Fixed stale P0c handoff bullet (“planned not drafted” removed).
- Marked `bridge-predictions-Lean-improvements.md` and `alignment-problem-alternative-decomposition.md` as reference-only (not live checklists).
- Added [`drafts/predictions/README.md`](../predictions/README.md) (live vs historical).
- Updated instrument plan P0c phasing row to **done**; Q1/Q2/Q6 partially decided in plan (Metaculus, title framing).
- Supersession note on `2026-09-19-prediction-interface-p0c.md` Open section.
- Pruned superseded log `2026-09-18-bridge-markets-mb6-binary.md` → RECOVERY.md; archived three spring-map logs.
- `.gitignore`: `.worktrees/`.
- **`metadata/predictions.yml`:** single `bridgeCardSlugs` mechanism — `primaryBridge` + optional `relatedBridges` (extra keys only); removed redundant/raw slug entries; market 17 → `[MB3]`; added `MB11` alias.
- **Proposed resolvers (ideal):** M7 Wentworth; M16 Wentworth + Shah; M18 Holtman + METR.
- **`sync-predictions.mjs`:** always resolve keys via `bridgeCardSlugs`; warn on unknown keys.

## Decisions
- Keep prediction sub-session logs; compact HANDOFF instead of deleting mid-chain logs.
- Do not attic `alignment-problem-alternative-decomposition.md` — header + problem-axis plan cross-ref suffices.
- `u17` maps to concept card `bearer-admission-adjacent`; MB3 is the only extra related link for market 17.

## Open / next
- Confirm resolver names with M7/M16/M18 before listing on Metaculus.
- **Boundary persistence:** ch01 unchanged; canonical home `\ref{par:cut-persistence-restoration}` in ch07 (Leaky Boundaries); ch06/ch08 one-line cross-refs only.

## Follow-up (same day)
- Author: keep ch01 as is; single home in ch07, not redundant footnotes across chapters.

## Key paths
- `metadata/predictions.yml`
- `drafts/conversation-summaries/HANDOFF.md`
- `drafts/predictions/README.md`
- `drafts/plans/predictions/bridge-prediction-markets.md`

## Commits
- `6f3033aa` — Housekeeping and unify predictions catalog bridge links.
- `9b1cbda3` — Centralize cut persistence vs repair in ch07 with thin cross-refs.
