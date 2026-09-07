# 2026-09-07 — Appendix stub retirement + App N readings

## Trigger
User approved plan: delete obsolete appendix stubs H–K; expand App N with methodology note and host-trace safety-case readings (not a separate appendix).

## Done
- Deleted four stub `.tex` files (`appH`–`appK`); nine wired appendices remain on disk.
- Housekeeping: `check_structure.py` (APPENDIX_COUNT=9), `sync-chapters.mjs`, `init_scaffold.py`, `INSTRUCTIONS.md` §14, `metadata/TODO.md`, `docs/MANUSCRIPT.md`, ledgers/source-canon, UAD funding card (`appI`→`appN`).
- App N: cut meta “why this appendix exists” voice; drop companion-site / repo-map paths (`docs/EXPERIMENTS.md`, GitHub URLs, `experiments/` folders, “site bullets”); safety-case readings report leaf outcomes.
- Plan: `drafts/plans/appendix-stubs.md`.

## Decisions
- Reconstructions titled **Safety-Case Readings on Host Traces** (not green-and-false); include W-11 success and both W-9/W-10; CIRIS mock last; no site URLs in App N.
- Historical `\label`s unchanged (`appj-`, `appk-`, etc.).

## Open / next
- Optional full PDF build (`./build.sh`).

## Commits
- `42525ed8` Retire unused appendix stubs and add App N host-trace readings.

## Key paths
- `appendices/appN-experimental-evidence.tex`
- `chapters/ch42-safety-case.tex`
- `INSTRUCTIONS.md` §14
