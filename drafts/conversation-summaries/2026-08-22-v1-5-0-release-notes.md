# 2026-08-22 — v1.5.0 release notes and tag

## Trigger
User asked to prepare release notes, reviewed the draft, then asked to perform the release steps.

## Done
- **`RELEASE_NOTES.md`:** **v1.5.0 — 2026-08-22** covering work since tagged v1.4.0 (user-edited body kept; one summary paragraph restored for the `/updates/` card parser).
- **`site/.gitignore`:** generated `release-v1-5-0.md`.
- **README / `docs/MANUSCRIPT.md`:** Release row → v1.5.0; manuscript milestone Fifth.
- **Release cut:** `make check`; notes commit + hash-fill commit; annotated tag **`v1.5.0`**; push `main` and tag; GitHub Release.

## Decisions
- **v1.5.0 = MINOR** (new framework objects and site layers; no chapter/appendix renumber).
- Hash line follows v1.4.0: notes commit SHA in `Commit:`; tag on the hash-fill commit.
- Did not stage unrelated `site/src/data/chapter-reading-graph.json`.

## Open / next
- CI / site deploy so `/updates/` serves the v1.5.0 card (`npm run sync` on deploy).

## Key paths
- `RELEASE_NOTES.md`
- `README.md`
- `docs/MANUSCRIPT.md`
- `site/.gitignore`
