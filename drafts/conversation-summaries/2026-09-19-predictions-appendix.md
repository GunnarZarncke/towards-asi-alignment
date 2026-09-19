# 2026-09-19 — Predictions appendix (print H)

## Trigger
User asked to write the new 2027 bridge-predictions appendix, then to continue until it was finished.

## Done
- Drafted `appendices/appP-bridge-predictions.tex` (print H): 18 boxed contracts, common qualification, judgment stack, 19 Sep 2026 prior-test notes, relation-to-other-appendices closer.
- Pointers from App B, App F, and the Lean appendix opener; preface appendices list.
- `predictionbox` in `metadata/preamble.tex`; wired in `book.tex` after the research program and before Lean.
- Print-letter table: Lean is now I, experimental evidence J (`INSTRUCTIONS.md`, README, `docs/MANUSCRIPT.md`, finding-id/experiments/methodology notes).
- Site: book index order, chapter-card and chapter-sync lists, tex-convert + book-page style for boxes. Not the `/predictions/` hub.
- App B pointer; preface appendices list.
- Prior-test bibliography pass: 24 new `.bib` keys + `\bibsummary{}` lines; `\autocite{}` on all 18 market prior-test paragraphs (Markets 15 still correctly uncited). Fixed Market 13 cites (sandbagging games, sleeper agents, adaptive attacks). `make check` passed.

## Decisions
- Two registers as planned: boxes = Metaculus English; surrounding = book terms and chapter refs. No Lean ids in boxes.
- Snapshot date in the prior-test notes is an authorized time-bounded marker, not a recency badge.
- Listing still Q1/Q6; the appendix is the absorb surface either way.

## Open / next
1. Spine `Evidence.lean`.
2. Q1/Q2/Q6 listing.
3. Site hub shipped in `2026-09-19-predictions-site.md`.

## Key paths
- `appendices/appP-bridge-predictions.tex`
- `drafts/plans/predictions/prediction-interface.md`

## Commits
- `03503995` — Appendix H + prior-test bibliography + print/site plumbing.
