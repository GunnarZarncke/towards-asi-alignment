# 2026-08-28 — Witness site documentation and session end

## Trigger
User asked to document Witness results on the companion site, end the session, and commit.

## Done
- `metadata/experiments.yml`: witness kind blurb, role, and howToRead updated with W-1–W-15 sprint synthesis (bounded outcome, W-12 strongest quantitative, W-15 null interpretation).
- `docs/EXPERIMENTS.md`: sprint synthesis paragraph after the W-1–W-15 table.
- Ran `site/scripts/sync-experiments.mjs` → `site/src/data/experiments.json` + experiment cards.
- Prior session work included in commit: W-13 PDG refuse, W-14 CPC2015 null, W-15 CIRIS stack C2 null; collectors/checkers/fixtures; plans; FINDINGS; App I; HANDOFF/INDEX.

## Decisions
- Site synthesis matches critical-review posture: process demonstration yes, bridge discharge / deployable alignment no.
- W-15 described as “no live bypass demonstrated,” not “defer stopped composite.”
- Later hosts (SCOTUS, BBQ, HH/PKU) and Lens cohort left unpaid; sprint declared bounded.

## Open / next
- Optional: CIRIS positive-control arm + rerun under new freeze.
- Independent reproduction of W-12 model spec.
- Construct concrete chapters still gated on a real stop (not H5 analogue).

## Key paths
- `metadata/experiments.yml`, `site/src/data/experiments.json`
- `/experiments/#witness`, `/experiments/findings/witness/`
- `experiments/witness/results/FINDINGS.md`

## Commits
- (this session)
