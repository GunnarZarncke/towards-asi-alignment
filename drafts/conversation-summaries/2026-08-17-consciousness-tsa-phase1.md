# 2026-08-17 — Consciousness TSA Phase 1

## Trigger
Implement Phase 1: bibliography + ch18 bearer-inference section + surgical cross-chapter pointers (no Rainbow; short model-welfare cites).

## Done
- New section `sec:recognizing-new-bearers` in `chapters/ch18-bearer-maps.tex` (after sufficient-statistics, before FN/FP): property-specific inference, $E(z)\to T\to P\to \Phi_k$, conservative exclusion / nonperson predicate, phenomenality vs subjecthood, counterexamples, MB9/MB11 pointers, short model-welfare cite list.
- FN/FP opening links to conservative exclusion; digital-mind example extended.
- Surgical pointers: ch07 (boundary before bearer tests), ch32 (self-model quantities not bearer tests), ch47 (current inference vs transformation).
- Bib keys + summaries: `yudkowsky2008nonperson`, `butlin2023consciousnessai`, `butlin2025responsibleconsciousness`, `long2024aiwelfare`, `anthropic2025modelwelfare`, `anthropic2025endsubset`.
- PDF build passes (`latexmk`).

## Decisions
- No Rainbow Theory cites; phenomenality/subjecthood split stated in prose only.
- Used `\not\Rightarrow` (book convention) instead of `\centernot`.
- ch42 left unchanged (already lists bearer-map checks).

## Open / next
- **Phase 2:** add `ch07 → ch18` to `chapter-informal-edges.yml`; regenerate concept graphs + site reading graph.
- **Phase 3:** ledgers/open problem.
- **Phase 4:** field v2 adjacent-work YAML.
- **Phase 5 (late):** MB3 card, Lean.

## Key paths
- `chapters/ch18-bearer-maps.tex` (`sec:recognizing-new-bearers`)
- `references/external-alignment.bib`, `references/philosophy.bib`

## Commits
- none
