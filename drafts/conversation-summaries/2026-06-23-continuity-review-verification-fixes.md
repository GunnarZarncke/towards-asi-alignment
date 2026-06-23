# 2026-06-23 — Continuity review verification fixes

## Trigger
User asked which continuity-review items were still open; review file was stale vs chapters. Requested fixes: ch08 conserved properties, WWCTV ch36/41 + ch40 suggestion, Critch bib split, pivotal notation, ch24/ch23 re-derivation, bundle-catalogue TODO, update review.

## Done
- **ch08:** Identity vector + seven conserved-property subsections aligned to ch29 (names, order, forward ref); control locus `K_t` → `L_t`; WWCTV/summary lists updated.
- **WWCTV:** ch36/ch41 retitled; ch40 new section with four falsifiers (structure absent, rename-only, safety-case pass + catastrophe, pivotal blocked).
- **Critch bib:** ch28/ch38 formalism cites → `critch2022boundaries3a`; ch01 keeps `critch2022boundaries` for Part-1 primitive argument.
- **ch35:** New `sec:pivotal-process-ch35` — `\mathcal{B}_{\text{race}} \to \mathcal{B}_{\text{certified deployment}}`; ch40 checklist + comment updated.
- **ch24:** Opening correction chain → pointer to ch23; canonical `eq:correction-chain-ch24` in `sec:minimal-causal-model`.
- **metadata/TODO.md:** Bundle catalogue terminology drift item; C12 pivotal marked done in manuscript.
- **review/full-book-continuity-review-2026-06-22.md:** Rewritten with 2026-06-23 verification pass (WWCTV 44/44, ch33 partial, closed items).
- **review/fix-plans-2026-06-22.md:** §C items 3, 12, 13, 14 marks updated.
- `./build.sh` clean (971 pp).

## Decisions
- Critch split is **semantic**, not single-key: Part 1 (`critch2022boundaries`) for utility-theory primitive in ch01; Part 3a (`critch2022boundaries3a`) for directed Markov-blanket formalism elsewhere.
- ch40 WWCTV framed around stress-test falsifiers (conditional structure, adversarial verifiability, safety-case sufficiency, pivotal-process rename).

## Open / next
- §A formula deduplication still not started.
- Bundle catalogue audit (TODO item).
- appA + INSTRUCTIONS §18 sync.
- `make check` fails on 45 vs 44 chapter files (ch39b).
- ch36 incident taxonomy wording vs ch37 layers (minor).

## Key paths
- `chapters/ch08-grow-split-merge.tex`, `ch24-correction-causal-channel.tex`, `ch35-alignment-attractor.tex`, `ch40-lethality-stress-test-open-issues.tex`
- `review/full-book-continuity-review-2026-06-22.md`
- `metadata/TODO.md` (bundle catalogue item)

## Commits
- (none — user did not request commit)
