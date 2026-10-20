# 2026-10-20 — Ch. 1 claim-extract author decisions

kind: feedback
uptake: status

## Trigger
Author answers on open Ch. 1 claim-extract decisions (risk system uniqueness, typology axes, moving object, thesis vs key claim, empirical falsifier); end of session and commit.
Prompts: paraphrase-only (no resolvable prompt id)

## Done
- content: `chapters/ch01-wrong-object.tex` — boundary-error definition allows several processes; extent vs resolution typology framing + misplaced → Ch. 7; chain of admissible transitions; thesis vs operational key claim; empirical WWCTV bullet; Summary aligned.
- bookkeeping: `drafts/plans/claim-extract/claim-extract.md` § Ch. 1 author decisions closed with recorded readings.
- bookkeeping: `metadata/claim-extracts/ch01.jsonl` — quotes/lines repaired; `ch01.094` empirical falsifier; `ch01.087` updated after display formula replaced by prose key claim (line 688).
- Verification: `.venv/bin/python scripts/check_claim_extract.py metadata/claim-extracts/ch01.jsonl` → `ch01.jsonl: 0 error(s)`.

## Decisions
- Ch. 1 need not posit a unique risk system; examples use one boundary; per-risk / per-case specificity deferred to later chapters.
- Typology is a family of failure modes (extent vs resolution), not a complete partition; misplaced named via Ch. 7.
- Moving object = chain of admissible transitions, not an equivalence class.
- Thesis (`ch01.003`) = locate before align; key claim (`ch01.087`) = operational selection rule for a given risk.
- WWCTV: empirical post-hoc / non-localization pattern added alongside proof bar on non-localizability.

## Open / next
- Claim-extract queue: **Ch. 5** when author asks.
- Line-drift tooling (`--relocate`) still open in plan § Infrastructure.

## Key paths
- `chapters/ch01-wrong-object.tex`
- `metadata/claim-extracts/ch01.jsonl`
- `drafts/plans/claim-extract/claim-extract.md` § Ch. 1

## Commits
- (this session)
