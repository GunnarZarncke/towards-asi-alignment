# 2026-09-01 — Bridge first-use implementation

## Trigger
User asked to implement `drafts/plans/bridge-first-use.md`.

## Done
- Freeze before Ch. 10: no `\leanspine`, `{leanbox}`, `MB*`, or Lean/proof-spine in Ch. 3–8 or frontmatter; assumptions/A-\* only.
- Ch. 10: genus definition; `\leanspine{bridge}{MB1}` recap of A-004; `MB7a` access; existing `MB7b`.
- Revisited Ch. 10 for first-time readers: added a four-step chapter roadmap, an explicit Ch. 9 composite-agent handoff, a dedicated proof/counterexample/bridge legend, a precise A-\* versus MB distinction, and the MB1 → MB7a → MB7b dependency diagram.
- Defined measurement handles and the access model in plain language; tied the adversarial tests back to MB7a/MB7b; added a summary recall cue for later `\leanspine` blocks.
- Home-chapter `{bridge}` tags: MB2 ch17, MB3 ch18, MB4 ch25, MB4a ch26, MB5 ch30, MB6a/MB6b/MB7d ch35, MB7c ch43, MB9 ch16, MB11 ch42. MB8 ch28 and MB10 ch31 kept. Ch. 48 MB10 tag removed. Assembly ranges in ch42/ch48/ch43 kept.
- Glossary: Bridges and assumptions entry.
- App N W-15 table: `$defer` broke math in a `longtable` (fatal); escaped as `\texttt{\$defer}`.
- `./build.sh` exit 0.

## Decisions
- MB9 home is Ch. 16 (first post-Ch. 10 grounding-certificate restatement), not Ch. 3.
- MB6a and MB6b both live in Ch. 35 (Ch. 37 had no natural site).
- MB7a first-use is Ch. 10, after the genus paragraph, not inside it.
- Reader rule: a `Lean spine (bridge)` block names an inference that is needed and still unpaid in the world; the block is a pointer, not additional evidence.

## Open / next
- Site/quiz sync still out of plan.
- Physical-bridge metaphors in intro/Ch. 3/6/9 left on purpose.
- Appendix D still has worked-example `{bridge}` pointers (allowed).

## Key paths
- `drafts/plans/bridge-first-use.md`
- `chapters/ch10-strategic-opacity.tex`

## Commits
- none
