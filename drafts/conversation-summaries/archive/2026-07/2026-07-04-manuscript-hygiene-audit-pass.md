# 2026-07-04 — Manuscript hygiene audit pass

## Trigger
User requested a manuscript-focused follow-up to the repository audit: fix claims-ledger chapter columns, reconcile bundle-catalogue drift, remove epistemic markers, regenerate `global-nocite.tex`, delete `src/demos/ch09-uad-coalition-board.zip`, add salon slides to Git, then end-of-session commit.

## Done
- **`metadata/claims-ledger.md`:** Re-verified all `Chapter(s)` columns against current `ch01`–`ch48` numbering and chapter content; fixed stale pointers (C-005 certified separation → ch29 not ch48; C-004a/C-044 eighth safety-case layer → ch42 not ch46); resolved renumbering caveat in header.
- **Bundle catalogue:** Canonical nine-bundle list in ch16; ch03/ch15/ch31 aligned with forward/back references; Learning→Truth and Legacy→Loyalty folding documented in ch15 and ch16.
- **Epistemic markers:** Removed 51 `[Defined]`/`[Conjectural]`/`[Open]`/`[Philosophical limit]` tags from ch35, ch43, ch44, ch47; left appD's separate `[Measured]`/`[Assumed]`/`[Lean-conditional]`/`[Open]` legend untouched (different device).
- **Prior session carry-over (same commit):** Certification-Under-Manipulation Problem in ch43; cross-refs in appB/appF and `open-problems.md`; reviewer refs (Edelman, Heitzig & Potham) in appB; deleted orphan `tables/assumptions-table.tex`; `metadata/TODO.md` audit notes updated.
- **`metadata/global-nocite.tex`:** Regenerated (adds `edelman2025fullstack`, `heitzig2025humanpower`).
- **`drafts/ai-salon-uad-demo-slides.md`:** Added to Git.
- **`src/demos/ch09-uad-coalition-board.zip`:** Deleted (was untracked; no commit entry).
- Build verified: `./build.sh` and `make check` pass.

## Decisions
- **Learning/Legacy:** Fold into Truth and Loyalty rather than add two new catalogue bundles; stated explicitly in ch15↔ch16 cross-refs. Author should confirm this is the intended resolution.
- **appD tags:** Not removed — appendix uses a self-contained evidentiary-kind legend, not the book-wide confidence markers.
- **Phase 0.5 session log:** `2026-07-04-phase-0.5-battery-rerun-progress-logging.md` has unrelated local edits; not included in this commit.

## Open / next
- Confirm Learning→Truth / Legacy→Loyalty folding with author.
- Decide whether to remove appD's inline tagging legend.
- C-044 / ch48: discharge grounding claim in opening-promise reconciliation (flagged in claims ledger).
- Ad-hoc composites still open: GLI (ch40), composite conservation score (ch31).

## Key paths
- `metadata/claims-ledger.md`, `metadata/TODO.md`
- `chapters/ch15-values-compressed-control.tex`, `chapters/ch16-value-bundle-model.tex`
- `chapters/ch43-verifiability-and-ontology-adequacy.tex`
- `appendices/appB-bridge-crosswalk.tex`

## Commits
- `27d0e42` Reconcile manuscript ledgers, bundle catalogue, and verifiability framing.
