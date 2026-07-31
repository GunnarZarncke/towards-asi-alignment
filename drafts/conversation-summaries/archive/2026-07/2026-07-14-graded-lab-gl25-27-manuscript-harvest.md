# 2026-07-14 — Graded lab GL-25/26/27 manuscript harvest

## Trigger

User: "incorporate into manuscript" (follow-up to Phase 8a/8b/8c session).

## Done

- **`ch34-selection-environment.tex`** §`sec:minimal-model-selection-ch34`:
  revised the GL-23 anchor paragraph (removed stale "open calibration work"
  language); added a second paragraph on the three same-day follow-up
  phases with finding labels `gl-24`--`gl-27` (selection-mechanism-noise
  read from 8a, proxy insensitivity from 8b, carryover causal but small
  from 8c).
- **`appendices/appN-experimental-evidence.tex`**: ledger range GL-0--27;
  section intro updated; added `finding:gl-24`--`finding:gl-27` table rows;
  MB6 crosswalk cell updated.
- **`metadata/claims-ledger.md`** C-007 support bullet updated to reflect
  follow-up findings and weakened causal read.
- **`experiments/graded-lab-simulation/PLAN.md`** manuscript-integration
  backlog note for ch34 updated.
- `make check` clean (structure, citations, bibliography summaries).

## Decisions

- Split ch34 into two paragraphs rather than one overstuffed block: first
  retains GL-23 anchor + review pointer; second carries GL-25/26/27 detail.
- Added `finding:gl-24` as its own appendix row (not only inline in GL-23)
  because ch34 cites `\ref{finding:gl-24}--\ref{finding:gl-27}`.
- Did not touch ch36/ch40 (still no parasite/laundering evidence).
- Did not re-run site sync (ch34 card text is generated from `.tex`; site
  `experiments.json` already had GL-25--27 headline from prior session).

## Open / next

- Full `./build.sh` failed on a **pre-existing** `appN` longtable preamble
  error (`Illegal pream-token (\appnbridgecols)` at line 192), unrelated to
  this edit; `make check` passed. May need `./clean.sh && make biber` fix
  or appN bridge-table repair from an earlier session.
- No commit (not requested).

## Key paths

- `chapters/ch34-selection-environment.tex` (lines ~84--86)
- `appendices/appN-experimental-evidence.tex` (graded-lab table + MB6 row)
- `metadata/claims-ledger.md` (C-007)

## Commits

- None
