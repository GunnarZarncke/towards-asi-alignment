# 2026-06-26 — Appendix count check fix

## Trigger

User asked to set the number of appendices correctly after `make check` repeatedly failed with `Expected 10 appendix files, found 9`.

## Done

- Updated `scripts/check_structure.py` so `APPENDIX_COUNT = 9`, matching `book.tex` appendices A--I.
- Updated `scripts/init_scaffold.py` so its scaffold appendix list includes `appI-lean-proof-spine`.

## Decisions

- Treated the current manuscript structure as authoritative: `book.tex` inputs nine appendices, and `appendices/` contains those nine files.

## Open / next

- `ReadLints` still reports pre-existing Pylint warnings in `scripts/init_scaffold.py` for unused arguments `filename` and `part_name`; not changed in this pass.

## Verification

```bash
make check  # success
```

## Key paths

- `scripts/check_structure.py`
- `scripts/init_scaffold.py`
- `book.tex`
- `appendices/`

## Commits

- `95aa559` Fix appendix count checks.
