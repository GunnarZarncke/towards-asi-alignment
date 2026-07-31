# 2026-06-25 — INSTRUCTIONS.md slim-down

## Trigger
User asked to remove obsolete book-structure and scaffold content from `INSTRUCTIONS.md`, keep general editorial rules, and deduplicate with `AGENTS.md`.

## Done
- Rewrote `INSTRUCTIONS.md` (~280 lines vs ~1500): mission, audience, style, source canon (pointers), consolidation rules, terminology/notation pointers, chapter requirements, citations, ledgers, conceptual spine, avoid list, process, acceptance, review passes.
- **Removed:** full chapter list, LaTeX scaffold checklist, duplicate term/symbol dictionaries (§6/§18), milestones §24–29, branch naming, README-create instructions, exhaustive source tables.
- **Canonical homes table** at top routes structure to `metadata/book.yml`, build/handoff to `AGENTS.md`, terms to `terminology.md`/appF, symbols to `notation.md`/appA, Lean to `formal/`.
- Updated cross-refs: `AGENTS.md`, `README.md`, `metadata/terminology.md`, `metadata/notation.md`, `metadata/source-canon.md`, `metadata/TODO.md`, `review/reviewer-guide.md`.

## Decisions
- Do not duplicate `AGENTS.md` (build, git, session logs, Lean spine workflow) or `README.md` (status table, repo map).
- Keep editorial consolidation rules (former §4.1) and conceptual spine as durable writing guidance.
- Historical conversation logs and `review/fix-plans-2026-06-22.md` still mention old § numbers; left unchanged (historical).

## Open / next
- Populate `appendices/appA-notation.tex` from `metadata/notation.md`.
- Optional: refresh stale README status row (chapter draft counts).

## Key paths
- `INSTRUCTIONS.md`, `AGENTS.md`, `README.md`, `metadata/notation.md`, `metadata/terminology.md`

## Commits
- none (not requested)
