# 2026-08-16 — Krym Phase 2 pointing glossary

## Trigger

Continue Krym architecture revision: Phase 2 — stop treating "pointing problem" as an unqualified synonym for MB2; keep the field term as a disambiguated umbrella.

## Done

- `appendices/appE-glossary.tex`: new pointing-problem headword (`gloss:pointing-problem`, `sec:pointing-problem`) with identification / realization / preservation; bearer-map nearest-field line tightened.
- `frontmatter/introduction.tex`: intro link to the three-sense glossary entry.
- `appendices/appB-bridge-crosswalk.tex`: MB2/MB3 row and notes lead with value/bundle identifiability; pointing as homograph pointer to App E.
- `appendices/appG-lean-proof-spine.tex`: MB3 field crossroad — adjacent to identification sense, not same crux as MB2.
- `metadata/bridges.yml`, `reference/field-agendas/data/bridges.yml`: MB2 summary and field-agree/differ copy; MB3 bookMove scalar value identifiability.
- `metadata/concepts.yml` + `metadata/concepts/bodies/pointing-problem.md`: new glossary card; MB2/MB3/bridge-assumptions bodies updated.
- Site sync: `sync:concepts`, `sync:bridges`, `sync:field-agendas`.
- `make check` passed.

## Decisions

- Public MB2 matrix noun stays **Value Learning**; no MB2a/b/c split.
- Realization stays open interface (no Target Realization card until Phase 5).
- Site glossary card mirrors App E; manuscript `\label{sec:pointing-problem}` anchors the card home.

## Open / next

- **Phase 3:** Lean MB2 evidence→identifiability→`BundleAligned` chain; de-opaque `BundleAligned`.
- Phases 4–6 per `drafts/krym-architecture-revision-plan.md`.

## Key paths

- `appendices/appE-glossary.tex` (`gloss:pointing-problem`)
- `metadata/concepts/bodies/mb2-bundle-identifiability.md`
- `metadata/concepts/bodies/pointing-problem.md`

## Commits

- `d3cc0622` — Disambiguate pointing problem from MB2 identifiability (Krym Phase 2).
