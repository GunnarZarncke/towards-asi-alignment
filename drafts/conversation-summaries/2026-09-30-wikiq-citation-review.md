# 2026-09-30 — Author review of LW wiki quote lead-ins

kind: feedback
uptake: local

## Trigger
User reviewed all `\wikiq` citation sites and adapted lead-in sentences; end-of-session commit.
Prompts: paraphrase-only (telemetry prompt ids not copied this turn).

## Done
- content: Gunnar trimmed redundant pre-quote lead-ins in 15 chapters (quotes often open sections with no duplicate label); ch15 Shard Theory bridge moved to `{GZ}` with shorter pointer; ch10 AI-control lead-in tightened.
- housekeeping: Fixed typo `researchprogram` → `research program` in ch15 during commit prep.

## Decisions
- Many wiki quotes now stand without a naming lead-in; attribution is the quote footer cite only.

## Open / next
- Run `cd site && npm run sync:chapters` before site deploy if chapter HTML should match.
- Optional PDF regen: `./build.sh`.

## Key paths
- `chapters/ch06-agent-without-anthropomorphism.tex` … `ch47-bearers-of-value.tex` (15 files)

## Commits
- (this session)
