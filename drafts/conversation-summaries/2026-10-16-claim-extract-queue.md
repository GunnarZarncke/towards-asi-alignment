# 2026-10-16 — Claim-extract combined queue

kind: notes
uptake: status

## Trigger
Extend the claim-extract plan with spine-name vs informal-warrant lenses and a combined chapter order. First chapter is 1. Do not start extracts.
Prompts: paraphrase-only (no resolvable prompt id)

## Done
- bookkeeping: Replaced density-first rollout in `drafts/plans/claim-extract/claim-extract.md` with two lenses and a 1–48 combined queue (Ch. 42 already done; next Ch. 1, not started).

## Decisions
- Combined value = Lean-mismatch risk at named predicates plus informal-warrant / reader-surface payoff. YAML `formal_density` is an input, not the order.
- Ch. 48 last among main text; Ch. 2 and 47 late despite low density.
- Same JSONL schema for both lenses; `lean: none` is allowed and flagged.

## Open / next
- Start Ch. 1 extract only when the author asks. Infrastructure items in the plan (checker `CHAPTER_FILES`, optional `make check` wire-up) still open.

## Key paths
- `drafts/plans/claim-extract/claim-extract.md`
- `metadata/claim-extracts/README.md`
- `metadata/claim-extracts/ch42.jsonl`

## Commits
- none
