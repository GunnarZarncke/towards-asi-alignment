# 2026-10-16 — Ch. 1 claim extract and analysis

kind: new-work
uptake: status

## Trigger
Perform the claim extract and analysis for Chapter 1 (first in the combined queue).
Prompts: paraphrase-only (no resolvable prompt id)

## Done
- content: `metadata/claim-extracts/ch01.jsonl` — full-chapter extract (thesis box through Summary), informal-warrant lens with Lean names where they exist; notes cite record ids.
- content: Analysis in `drafts/plans/claim-extract/claim-extract.md` § Ch. 1: surgical prose items, author decisions, spine gaps, Lean support worth citing.
- bookkeeping: `scripts/check_claim_extract.py` resolves `chNN.jsonl` to the unique `chapters/chNN-*.tex` (replaces the hand-kept `CHAPTER_FILES` map).
- bookkeeping: `ch42.jsonl` line spans relocated. Every quote still existed; only `lines` had drifted after later Ch. 42 edits (checker had reported 82 errors). `ch42.054` matched two lines; kept the risk-gap leaf equation.
- bookkeeping: Claim-extract row added to the `metadata/TODO.md` work map; Ch. 1 Lean candidates added to the 2.0 bullet in `drafts/plans/spine/spine.md`; README shipped list.
- Verification (extract): `.venv/bin/python scripts/check_claim_extract.py` → `ch01.jsonl: 0 error(s)`, `ch42.jsonl: 0 error(s)`.
- content: Ch. 1 surgical phrase-level items applied (`chapters/ch01-wrong-object.tex`); affected extract records shifted and re-checked → `ch01.jsonl: 0 error(s)`.
- Verification: `make check` → `## Check — pass`. `./build.sh` exit 0.
- content: Author pass on the surgical text. Membrane contrast moved to a footnote on physical containment; candidate boundaries restored as a scale hierarchy with a DAG footnote; the three discovery conditions restated in prose, formulas left to Ch. 7 and Ch. 22. Ch. 7 no longer says those variable roles were introduced in Ch. 1. Extract re-checked → `ch01.jsonl: 0 error(s)`.

## Decisions
- Extract pass listed repairs; author then asked for the surgical list. Author-decision items (unique vs several risk systems; typology axes; equivalence class; key-claim ordering vs selection; empirical falsifier) left open.
- Infant claim hedged, not cited. Pairwise formula now uses Ch. 7 \(\mathcal{P}\) and \(\Omega\).
- New flags introduced where the informal lens needed them (e.g. `HIDDEN-PREMISE`, `INTERNAL-TENSION`, `TYPOLOGY-MIXED-AXES`, `FALSIFIER-ASYMMETRIC`, `UNCITED-EMPIRICAL`). Histogram: checker output after surgical pass.
- Main remaining finding: the selection criterion still appears in several forms that disagree. Strongest spine finding: object selection happens outside Lean (`System` argument), so a valid case can certify the wrong object.

## Open / next
- Author-decision items in plan § Ch. 1.
- Line-drift handling for extracts (plan § Infrastructure).
- Next chapter in the queue: Ch. 5.

## Key paths
- `metadata/claim-extracts/ch01.jsonl`
- `drafts/plans/claim-extract/claim-extract.md` § Ch. 1
- `chapters/ch01-wrong-object.tex`

## Commits
- none
