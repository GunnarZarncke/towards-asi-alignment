# 2026-06-30 — Narrative voice policy + chapterthesis pass

## Trigger
User asked to commit open changes (gitignore `experiments/toy-simulation/results/`), then apply the narrative-voice audit plan from TODO.

## Done
- **Gitignore:** `experiments/toy-simulation/results/`; removed tracked result files from index.
- **Pre-voice commit:** `book.tex` appendix stub cleanup, ch09 CCI forward-ref, dedication trim, `source-canon.md` Lean build note.
- **Policy:** two-register voice in `INSTRUCTIONS.md` §2 and `context/writing-style-gunnar.md` (body = inclusive **we**; meta/`chapterthesis`/appendices = impersonal; WWCTV = **This chapter argues**; **I** paratext only).
- **chapterthesis:** normalized 15 outliers (removed `we`, `This chapter`, `this chapter` from thesis boxes) across ch01, ch07, ch19–ch21, ch25/25b, ch27, ch29, ch31, ch35b, ch38, ch39b, ch40.
- **Lint:** `scripts/check_voice.py` (chapter bodies + chapterthesis + WWCTV).
- **TODO:** narrative voice item marked `[~]`.

## Decisions
- Did **not** rewrite ~480 body `we need/must` instances; Register A stays inclusive procedural **we**.
- ch44 closing `chapterthesis` keeps **this book** (meta closing chapter).

## Open / next
- Optional: add `check_voice.py` to `make check`.
- Optional body pass for redundant `this book` in mid-chapter prose.

## Key paths
- `INSTRUCTIONS.md`, `context/writing-style-gunnar.md`, `scripts/check_voice.py`
- Normalized `chapterthesis` in ch01, ch07, ch19–ch21, ch25/25b, ch27, ch29, ch31, ch35b, ch38, ch39b, ch40

## Commits
- (this session)
