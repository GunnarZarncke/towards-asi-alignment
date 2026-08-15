# 2026-08-15 — ET external transfer concept card

## Trigger
User noted the companion-site ET card (`/cards/et-external-transfer/`) covered only ET-1 (Orbit) while ET-2 through ET-4 exist in `docs/EXPERIMENTS.md` and findings ledgers.

## Done
- Expanded `metadata/concepts/bodies/et-external-transfer.md`: status table for ET-1–ET-4, narrative sections per annex, five `evidenceNotes` (ET-1 bound; ET-2 null + handle-UAD pilot; ET-3 closed; ET-4 hackathon), external links to all PLAN files + replay demo.
- Updated `metadata/concepts.yml` roster: summary mentions four annexes; `bookChapters` extended (ch10, ch12, ch34, ch39, ch41, ch42).
- Ran `cd site && npm run sync:concepts` (generated card is gitignored; metadata is source of truth).

## Decisions
- Keep ET-2 handle-UAD pilot as a separate `bound` evidence note (GL-88), distinct from ET-2a passive null (GL-87).
- ET-4 classified as hackathon scope in card body; no claim it validates frontier secret loyalties.

## Open / next
- Deploy site so live card updates (`npm run build` / publish pipeline).
- ET-2 Leaf B (CIL selection/capture descriptive cross-check) still open per GL-87.

## Key paths
- `metadata/concepts/bodies/et-external-transfer.md`
- `docs/EXPERIMENTS.md` § External transfer
- Field-news cards: `field-news-et2-cil-uad-jul-2026`, `field-news-et3-ai2027-jul-2026`, `field-news-et4-secret-loyalties-jul-2026`

## Commits
- `4ac39bf5` Expand ET external transfer card to cover ET-1 through ET-4.
