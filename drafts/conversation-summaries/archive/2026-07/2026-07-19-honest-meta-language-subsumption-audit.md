# 2026-07-19 — Honest meta-language pass + subsumption audit

## Trigger
User asked to remove self-congratulatory “honest/honesty” framing from the book (show sincerity by scope and limits, not by claiming it). Later: scan manuscript and site for remaining “subsumption” after an earlier crosswalk→projection reframe. End of session with commit.

## Done
- **Honest meta-language (~70 edits, two batches):** Replaced book-facing claims like “the honest claim,” “concede honestly,” “honest about limits,” “honest result,” metric “honest” → operational terms (*track the world*, *without faking*, *reliable*, *baseline twin*, etc.) across appendices B/C/D/F/G/M, chapters 09–10, 16–17, 33, 42–44, metadata concept bodies (experiment-methodology, subsumption CIRL/debate/ELK, value-change), assumptions ledger, generalist reading path.
- **Counts:** project-wide ~1,526 → ~1,442 matches for honest/honesty/honestly/dishonest/dishonesty (most remainder: experiment fixture names, value-theoretic “honesty,” Lean IDs).
- **Subsumption audit (read-only):** Display reframe largely landed (section title “Field Results Rederived and Mapped,” site card titles “Field projection — …”). Remaining: Lean `\leanid{*_subsumption_*}` in appG PDF, stable slugs `subsumption-*`, formula/leanNode summaries in metadata bodies, `sync-lean-spine.mjs` hub title “rederived and subsumed,” internal `\label{*subsumption*}`.

## Decisions
- **Edit posture:** Manuscript voice and synced metadata/site prose only; left substantive value uses (ch15–16 honesty bundle), RLHF “HHH,” experiment `honest` scenario identifiers, Lean theorem names.
- **Commit scope:** Stage only honest-pass manuscript/metadata/site files; leave unrelated graded-lab, salon slides, hostile-review, and experiments.json changes unstaged.

## Open / next
- Optional: second honest pass on experiment docs (`FINDINGS.md` “reported honestly”) if desired.
- Subsumption cleanup (if wanted): `sync-lean-spine.mjs` “subsumed” → “mapped”; leanNode summaries in `metadata/concepts/bodies/subsumption-*.md`; then `cd site && npm run sync:projections`.
- Slugs and Lean IDs can stay stable unless breaking URLs is acceptable.

## Key paths
- `appendices/appB-bridge-crosswalk.tex`, `appD-worked-example.tex`, `chapters/ch42-safety-case.tex`, `chapters/ch43-verifiability-and-ontology-adequacy.tex`, `chapters/ch44-lethality-stress-test-open-issues.tex`
- `metadata/concepts/bodies/experiment-methodology.md`, `metadata/projections.yml`
- `review/mechanism-comparison-umbrella-audit-2026-07-18.md` (subsumption audit notes)

## Commits
- (this session commit hash below)
