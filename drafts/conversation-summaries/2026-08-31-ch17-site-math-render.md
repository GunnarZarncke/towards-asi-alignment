# 2026-08-31 — Ch17 site math render fix

## Trigger
User reported chapter 17 not rendering properly on the companion site: `$g_\psi$` literal, truncated “At $80…” sentence, and all formulas after that paragraph unexpanded.

## Done
- Diagnosed `stripComments` in `site/scripts/lib/tex-convert.mjs`: escaped `\%` was treated as a LaTeX comment start, truncating lines at `\(80\%\)` and leaving an unclosed `$` that broke KaTeX for the rest of the page.
- Fixed by counting preceding backslashes: odd count → literal `%`; even count → comment.
- Verified via `node scripts/sync-chapters.mjs`: ch17 line now `At $80%$ held-out accuracy, $p_e=0.2$…`; display math blocks after it convert to `$$` again. Same fix restores ch02 `$5%$`, ch34 `$10%$` / `$1%$`, and appendix N table cells with `\%`.
- Regenerated gitignored `site/src/content/book/` locally (picked up on deploy prebuild).

## Decisions
- Fix in the converter, not the manuscript — `\%` is correct LaTeX throughout the book.

## Open / next
- None for this bug. Refresh `/book/ch17/` after deploy or local `npm run sync:chapters`.

## Key paths
- `site/scripts/lib/tex-convert.mjs` — `stripComments`
- `chapters/ch17-low-dimensional-value-learning.tex` — line with `\(80\%\)` (unchanged)

## Commits
- (pending) Fix escaped percent in tex-convert comment stripping.
