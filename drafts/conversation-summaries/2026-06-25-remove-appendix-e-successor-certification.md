# 2026-06-25 — Remove Appendix E (successor certification)

## Trigger
User asked to remove the successor certification Appendix E.

## Done
- Removed `\input{appendices/appE-successor-certification}` from `book.tex`.
- Deleted stub `appendices/appE-successor-certification.tex`.
- Updated `metadata/TODO.md` and `scripts/init_scaffold.py` to drop appE; noted successor certification stays in ch28–31.
- `./build.sh` passed.

## Decisions
- No manuscript `\ref{appe-successor-certification}` existed; no chapter edits required.
- Appendix letters in the PDF shift by one after D (glossary is now Appendix E, etc.); file names (`appF`, `appG`, …) unchanged; label-based refs (`appf-glossary`, etc.) unaffected.

## Open / next
- Optional: update `review/fix-plans-2026-06-22.md` §E table row for appE if that doc is still used for planning.

## Key paths
- `book.tex`
- `chapters/ch28-successor-central-test.tex`–`ch31-certification-without-construction.tex`

## Commits
- (none this session)
