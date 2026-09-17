# 2026-09-05 — v1.6.0 release notes and tag

## Trigger
User asked for the next minor release notes, then when authorship bars entered the PDF, then to create the release, then end of session.

## Done
- **`RELEASE_NOTES.md`:** **v1.6.0 — 2026-09-05** — Witness W-1–W-17, problem-axis / four questions / bridge first-use, manuscript (Bergemann, harm-path, voice), Lean `AlignmentRegime`, companion-site product (essays, quiz, spec sheet, funding, Field hub v2). User trimmed housekeeping / “not in manuscript” blocks before tag.
- **`README.md` / `docs/MANUSCRIPT.md`:** release **v1.6.0**; milestone **Sixth**; W-1–W-17 in experiments row.
- **`site/.gitignore`:** `release-v1-6-0.md`.
- **`site/src/lib/field-matrix-cell.test.ts`:** matrix evidence links → `/field/#ev-*` (stale `/field/v2/` expectation).
- **Release cut:** `make check` passed; commits `c6713029` + `486cd926`; annotated tag **`v1.6.0`** on `486cd926`. `sync-releases.mjs` run locally (generated cards gitignored).
- **Q&A (no repo change):** `\authbar` PDF bars — frontmatter **2026-08-21** (`f728c696`); full book **2026-08-22** (`c866af5f`); shipped in **v1.5.0**.

## Decisions
- **v1.6.0 = MINOR** (Witness class, problem-axis objects, site product layers).
- Commit line = notes commit `c6713029`; tag on hash-fill `486cd926` (same pattern as v1.5.0).
- Release commits only — no unrelated tree staged.

## Open / next
- **Push:** `git push origin main && git push origin v1.6.0` (not done this session).
- **Deploy / sync:** `cd site && npm run sync` (or CI) so `/updates/` serves v1.6.0.
- **Field lane:** adjacent-work markdown render in `FieldAdjacentWork.astro` still open (`field.md`).

## Key paths
- `RELEASE_NOTES.md`
- `README.md`, `docs/MANUSCRIPT.md`
- `site/scripts/sync-releases.mjs`

## Commits
- `c6713029` Add v1.6.0 release notes.
- `486cd926` Set v1.6.0 release commit hash in release notes.
