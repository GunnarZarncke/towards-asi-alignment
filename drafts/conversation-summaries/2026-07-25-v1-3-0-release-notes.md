# 2026-07-25 — v1.3.0 release notes and tag

## Trigger
User asked to prepare the next release notes, then revise framing (split Manuscript/Lean, strengthen findings and graded-lab v4 sections, drop "harvest" language), then cut the release and commit at session end.

## Done
- **`RELEASE_NOTES.md`:** added **v1.3.0 — 2026-07-25** covering field news, ch01–ch16 illustrations, graded-lab v4 architecture, experimental findings (ET-1/ET-2 + Appendix N synthesis), companion site, manuscript, and Lean P1–P4 evidence ladder; revised per user feedback (separate Manuscript / Lean sections; findings substance not UX-first; v4 features not GL ledger list).
- **`site/.gitignore`:** added generated `release-v1-3-0.md`; ran `sync-releases.mjs`.
- **Release cut:** `make check` passed; commits `ee5e83ff` + `6cd34dcf`; tag **`v1.3.0`** on `6cd34dcf`; pushed `main` and tag to `origin`.
- **Post-release hash line:** aligned Commit line to tagged commit `6cd34dcf` (this session commit).

## Decisions
- **v1.3.0 = MINOR** (new layers and evidence integration; no renumbering).
- **Graded-lab v4 section** describes rig architecture (portfolio, precondition/SKIP, substrate classes, fixture layer, `channel_severance`) not per-GL inventory.
- **Findings section** leads with Appendix N chapter synthesis and ET/v4 substance; site UX bullets last.
- **Lean section** framed as P1–P4 evidence ladder, not "credibility artifacts."

## Open / next
- Run `cd site && npm run sync && npm run build` (or CI) so `/updates/` serves v1.3.0 card on deploy.
- Optional: create GitHub Release from tag in UI (`gh` unavailable in agent shell).
- Branch was ahead of origin by additional commits after v1.3.0 push (RSS, field-news plain language, updates-page fixes) — push when ready.

## Key paths
- `RELEASE_NOTES.md`
- `site/scripts/sync-releases.mjs`
- `site/src/content/cards/release-v1-3-0.md` (generated, gitignored)

## Commits
- `ee5e83ff` Add v1.3.0 release notes.
- `6cd34dcf` Set v1.3.0 release commit hash in release notes.
- `bd266441` Align v1.3.0 release commit hash and record session logs.
