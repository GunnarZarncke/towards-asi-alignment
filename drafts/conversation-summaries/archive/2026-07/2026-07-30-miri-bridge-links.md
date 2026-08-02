# 2026-07-30 — MIRI writeup links on bridges

## Trigger
User asked that bridge discussions link to prior MIRI writeups of the corresponding cruxes.

## Done
- App. B: short “MIRI writeups” paragraph pointing to Embedded Agency + Technical Agenda; surgical cites for value learning (MB2), Vingean reflection (MB5/MB10), subsystem alignment via Embedded Agency (MB7).
- New bib keys + summaries: `fallenstein2015vingean`, `soares2015technicalagenda`, `soares2015valuelearning`.
- Bridge concept cards: MIRI/AF external links on MB1, MB2, MB4, MB5, MB7, MB8, MB10 (not MB3/MB6/MB9 — no clean MIRI prior writeup).
- Synced concepts + bridges; bibliography-summary check passed (433 keys).
- Clarified shared-cite overlap: App. B notes MIRI writeups do not draw the book’s cuts; MB8/MB10 cards each name the sibling split (MB4↔MB8, MB5↔MB10).

## Decisions
- Link MIRI sources where they own or named the crux; do not invent MIRI coverage for book-only bridges (bearer maps, selection basins, GSAI-style grounding).
- Prefer intelligence.org PDFs / Embedded Agency hub for public-facing card links; keep manuscript `\autocite`s on bib keys.
- Explicitly mark MB5/MB10 and MB4/MB8 as this book’s typed handoffs of shared AF walls, not MIRI paper distinctions.

## Open / next
- Commit when requested (also pending: earlier App. C MIRI hard-pause + AI 2040 news link).

## Key paths
- `appendices/appB-bridge-crosswalk.tex`
- `metadata/concepts/bodies/mb{1,2,4,5,7,8,10}-*.md`
- `references/external-alignment.bib`

## Commits
- `2d0cddad` Link MIRI agent-foundations writeups into the bridge crosswalk and Plan A context.
