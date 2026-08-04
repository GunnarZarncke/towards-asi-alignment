# 2026-06-23 — Continuity review verification fixes

## Trigger
User asked which continuity-review items were still open; review file was stale vs chapters. Requested fixes: ch08 conserved properties, WWCTV ch46/41 + ch48 suggestion, Critch bib split, pivotal notation, ch46/ch46 re-derivation, bundle-catalogue TODO, update review.

## Done
- **ch08:** Identity vector + seven conserved-property subsections aligned to ch48 (names, order, forward ref); control locus `K_t` → `L_t`; WWCTV/summary lists updated.
- **WWCTV:** ch46/ch45 retitled; ch48 new section with four falsifiers (structure absent, rename-only, safety-case pass + catastrophe, pivotal blocked).
- **Critch bib:** ch46/ch45 formalism cites → `critch4622boundaries3a`; ch01 keeps `critch4622boundaries` for Part-1 primitive argument.
- **ch48:** New `sec:pivotal-process-ch48` — `\mathcal{B}_{\text{race}} \to \mathcal{B}_{\text{certified deployment}}`; ch48 checklist + comment updated.
- **ch46:** Opening correction chain → pointer to ch46; canonical `eq:correction-chain-ch46` in `sec:minimal-causal-model`.
- **metadata/TODO.md:** Bundle catalogue terminology drift item; C12 pivotal marked done in manuscript.
- **review/full-book-continuity-review-2026-06-22.md:** Rewritten with 2026-06-23 verification pass (WWCTV 44/44, ch48 partial, closed items).
- **review/fix-plans-2026-06-22.md:** §C items 3, 12, 13, 14 marks updated.
- `./build.sh` clean (971 pp).

## Decisions
- Critch split is **semantic**, not single-key: Part 1 (`critch4622boundaries`) for utility-theory primitive in ch01; Part 3a (`critch4622boundaries3a`) for directed Markov-blanket formalism elsewhere.
- ch48 WWCTV framed around stress-test falsifiers (conditional structure, adversarial verifiability, safety-case sufficiency, pivotal-process rename).

## Open / next
- §A formula deduplication still not started.
- Bundle catalogue audit (TODO item).
- appA + INSTRUCTIONS §18 sync.
- `make check` fails on 45 vs 44 chapter files (ch47).
- ch46 incident taxonomy wording vs ch48 layers (minor).

## Key paths
- `chapters/ch08-grow-split-merge.tex`, `ch46-correction-causal-channel.tex`, `ch48-alignment-attractor.tex`, `ch48-lethality-stress-test-open-issues.tex`
- `review/full-book-continuity-review-2026-06-22.md`
- `metadata/TODO.md` (bundle catalogue item)

## Commits
- (none — user did not request commit)
