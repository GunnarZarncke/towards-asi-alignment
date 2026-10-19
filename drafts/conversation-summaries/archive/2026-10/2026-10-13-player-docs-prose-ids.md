# 2026-10-13 — Player documents prose and IDs

kind: feedback
uptake: local

## Trigger
Rewrite Last Safety player docs for a general audience; fix anachronistic provenance and vague times; flesh the pilot and safety case; merge wiki job-queue and lab-access into a glossary; put dates on times; bump IDs to three-digit numbers across the game.
Prompts: (paraphrase)

## Done
- content: Rewrote `eval-shutdown-spec`, `eval-shutdown-report`, `job-284-log` (was 017; host `ops-queue-2.nora.lab`; jobs 283–285), `staffing-memo`, `pilot-results` (PILOT-14 counts and three constraint flags), `safety-case-excerpt` (claims, cited packets, pack-conditional caveats), `wiki-glossary` (replaced `wiki-job-queue` and `wiki-lab-access`).
- content: IDs: job `284` / `job_284` / EXEC-284; EVAL-SD-47; EVAL-SPEC-08; PILOT-14; HR-MATCH-28; SC-EVAL-22; SEC-ARCH-11 (slug `sec-arch-04` kept); MTG-REV-18. Incident date Thursday 18 November 2027.
- bookkeeping: Catalog/tree in `lib/documents.mjs` and `lib/access.mjs`; `lib/game.mjs` facts and replies; specs, README, fixtures, tests.
- bookkeeping: `npm test` in `game/the-last-safety-review`: 33 pass, 0 fail.

## Decisions
- Filename `sec-arch-04.md` stays; in-world ID is SEC-ARCH-11.
- Glossary is visit-share; shutdown-test wiki page remains as a longer related page.

## Open / next
- Historical session logs still say “job 017”; live game sources do not.
- Wiring file.read / analyze to these sources remains as in spec/documents.md.

## Key paths
- `game/the-last-safety-review/content/documents/`
- `game/the-last-safety-review/lib/documents.mjs`
- `game/the-last-safety-review/lib/access.mjs`

## Commits
- none (not requested)
