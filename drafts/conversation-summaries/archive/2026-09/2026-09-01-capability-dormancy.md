# 2026-09-01 — Capability dormancy (plan §7)

## Trigger
Implement plan §7 Dormancy (Lane A: capability/transfer-breakers; one Lane B pointer).

## Done
- ch05 new section `sec:capability-dormancy-ch05`: quiet failure is not a certificate; transfer-breaker table; explicit “low capability is not therefore not deceptive”; one sentence to ch33 successor/envelope (no spores table).
- ch14 after A-012: eval-at-present-capability does not license the jump; pointer back to ch05.
- App F conjunctive-spine one-liner (not the §8 OR paragraph).
- Site: `what-not-claiming.md`, `scope-and-correction-capacity.md`; `sync:concepts`; search index rebuilt.
- `make check` passed. No Lean change; no new `MB*`; no `CapabilityBelow → Safe`. Chapter-reading DAG not regenerated (paragraph/section add, no new chapter prerequisite).

## Decisions
- Lane B stays a pointer to ch33; Construct 2.0 / adverse-process-generator not named in the PDF.
- Table uses chapter refs rather than an MB wall, for early-chapter accessibility.

## Open / next
- Plan §8 App F problem-side OR vs case-side AND; App B takeaway pointer.
- Optional: `npm run sync:chapters` for live book pages.
- User sign-off if the table still reads as a below-K safety certificate (intended not to).

## Key paths
- `chapters/ch05-assumptions-scope-failure-coverage.tex`
- `chapters/ch14-intelligence-deepens-misalignment.tex`
- `appendices/appF-research-program.tex`

## Commits
- none (not requested)
