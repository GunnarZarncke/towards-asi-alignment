# 2026-09-28 — Edit-attribution scope

## Trigger
User asked for the edit-tracking plan, then required that authorship bars (and updates to them) be derivable more often, and that tracked changes be manuscript and site.

## Done
- Revised `drafts/plans/tsa-on-itself.md` §3.1, §3.12, §5, and the §7 tooling bullet.
- Noted the same constraint on the TSA-on-itself line in `metadata/TODO.md`.

## Decisions
- Ledger, trailers, and the unattributed-share stop count `chapters/`, `appendices/`, `frontmatter/`, and `site/src/` except manuscript sync output (`site/src/content/book/`). Snapshots stay whole-tree.
- A span's `\begin{authbar}` key is recomputed on the commit that changes its tracked lines: human only → `GZ`, agent only → `AI`, both → `GZ+AI`. Once both are present the key stays `GZ+AI`. Pre-ledger lines keep the key declared at ledger start.
- Site chapter chips follow those keys on `sync:chapters`. The bar-update log feeds §3.1; there is no three-month wait.

## Open / next
- Tooling in §7 is still unbuilt. Author still freezes the §3.1 share threshold before the first run.

## Key paths
- `drafts/plans/tsa-on-itself.md`
- `metadata/TODO.md`
