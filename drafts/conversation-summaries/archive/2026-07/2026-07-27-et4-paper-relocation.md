# 2026-07-27 — ET-4 paper relocation

## Trigger
The user requested a top-level `papers/` folder using the structure of the
`brain-to-values` sibling repository, with the ET-4 submission in its own
paper folder and its date frozen.

## Done
- Moved the unchanged ET-4 Markdown, LaTeX, and PDF files to
  `papers/et4-secret-loyalties/`.
- Added the sibling-style `papers/README.md` index and a local `build.sh`.
- Updated the ET-4 context README link.
- Added the top-level papers index to the main repository README.

## Decisions
- Kept the existing July 2026 date and did not edit paper content.
- Kept hackathon reference materials in `context/ET4-context/`; only the
  submission artifacts moved.

## Open / next
- Rebuild the paper from `papers/et4-secret-loyalties/build.sh` if PDF
  verification is desired.

## Key paths
- `papers/README.md`
- `papers/et4-secret-loyalties/`
- `context/ET4-context/README.md`

## Commits
- None.
