# 2026-08-16 — Move three alignment questions to the introduction

## Trigger
Chapter 1 after Phase 1 felt overloaded. Author chose Option A: put the determine / construct / certify orientation in the introduction; leave ch01 with a short handoff. Use glossary-level language, not later technical labels, for forward references.

## Done
- `frontmatter/introduction.tex`: new §Three Alignment Questions (`sec:three-alignment-questions`) in plain terms (values, bearers, grounding, correction channel, successors, selection); certification ≠ construction; book scope; pointing as glossary umbrella; first chapter locates the process.
- `chapters/ch01-wrong-object.tex`: removed the full three-questions section; Standard Picture / Which Alignment? no longer forward-cite ch25–26, Part V, or composite-agent by name; short intro handoff then “Where is the optimizer?”
- `chapters/ch33-certification-without-construction.tex`: back-ref now points at the introduction, not ch01.
- Tracker: `drafts/krym-architecture-revision-plan.md`.

## Decisions
- Introduction carries book-level scope; ch01 stays the wrong-object argument.
- Forward refs in the new intro section and ch01 opening use glossary nouns, not chapter-technical labels (CCI, bundle inference, Part V).

## Open / next
- Phase 2: App E pointing-problem headword (intro already points at the glossary umbrella).
- Optional later: ch01↔ch07 boundary-material overlap (not this pass).

## Key paths
- `frontmatter/introduction.tex`
- `chapters/ch01-wrong-object.tex`

## Commits
- `893d08b8` — Move three alignment questions to the introduction; trim ch01 handoff.
