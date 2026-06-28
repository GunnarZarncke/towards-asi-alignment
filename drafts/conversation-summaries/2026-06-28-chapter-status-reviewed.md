# 2026-06-28 — Chapter status reviewed

## Trigger

The user asked to update chapter statuses so chapters that received feedback in the logs count as reviewed, and to mark the split chapters as reviewed too.

## Done

- Updated every chapter entry in `metadata/book.yml` from `draft` to `reviewed`.
  - This includes the split chapters `ch19b`, `ch25b`, and `ch35b`.
- Updated visible status language:
  - `README.md` now says there are `0 draft`, `48 reviewed`, `0 stub` chapter entries.
  - `frontmatter/current-status.tex` now clarifies that `reviewed` means feedback has been received and incorporated or logged, not final/polished/publication-ready.
- Regenerated:
  - `tables/chapter-map.tex`
  - `tables/part-roadmap.tex`
  - `metadata/book-stats.md`
- Updated the split-plan files so their proposed status lines use the same convention:
  - `review/ch19-split-plan-2026-06-28.md`
  - `review/ch25-split-plan-2026-06-28.md`
  - `review/ch35-split-plan-2026-06-28.md`

## Decisions

- Interpreted `reviewed` as an internal workflow status meaning "has received at least one review/feedback pass."
- Did not treat `reviewed` as final, polished, or publication-ready; this distinction is now explicit in the frontmatter and README.

## Open / next

- If a stricter status taxonomy is desired later, consider adding separate fields such as `feedback_received`, `revision_state`, or `publication_ready` instead of overloading `status`.
- Chapter-numbering cleanup remains open for temporary `b` chapters.

## Key paths

- `metadata/book.yml`
- `README.md`
- `frontmatter/current-status.tex`
- `tables/chapter-map.tex`
- `metadata/book-stats.md`
- `review/ch19-split-plan-2026-06-28.md`
- `review/ch25-split-plan-2026-06-28.md`
- `review/ch35-split-plan-2026-06-28.md`

## Commits

- None.

## Verification

- `make check` passed.
- `./build.sh` passed.
- `python3 scripts/book_stats.py` regenerated `metadata/book-stats.md`.
- `book.log` scan found no undefined references or citations.
- Read lints reported no diagnostics for edited files.
