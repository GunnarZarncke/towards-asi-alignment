# 2026-07-19 — Mechanism comparison, umbrella framing, chapter refs

## Trigger
External advice to prefer mechanism comparisons over agenda branding; audit manuscript for disagreements with field agendas, umbrella/UAD framing, and branding; then reduce umbrella instances and fix plain `ch<n>` references.

## Done
- Wrote audit report: [`review/mechanism-comparison-umbrella-audit-2026-07-18.md`](../../review/mechanism-comparison-umbrella-audit-2026-07-18.md) (four parallel subagent searches + synthesis).
- Softened umbrella/branding language across appB, appF, appG caption, ch48, executive overview, and ~20 chapters (`serious alignment must` → scoped preservation/certification path; shared antecedent vs single-problem/master crux; necessary-not-sufficient for debate/ELK in ch27; funding line in ch12).
- User follow-ups: ch48 empirical claim → bridge-by-bridge establishment before safety case binds; ch35 UAD as one operational approach to multipolar agent identification (removed footnote disambiguation).
- Linked all plain-text `ch<n>` reader references in appB table/notes, appG, appN, ch31/ch43/ch44 `\leanspine` lines ( `\ref{ch:...}` / `Chapter~\ref{...}` ); fixed appG `Ch24` → ch25 for \(U_S\).

## Decisions
- Lean identifiers, projection URL slugs, and `\label{...-chNN}` equation/section anchors left unchanged (per prior 2026-07-08 crosswalk reframe policy).
- UAD disambiguation via prose in ch35 (multipolar identification problem), not a defensive footnote.

## Open / next
- Optional: name RLHF explicitly in ch25–28 block where critique is RLHF-shaped but implicit (audit §6).
- Optional: finish `metadata/projections.yml` display copy if site cards still read as subsumption.
- Unrelated working-tree items not staged: graded-lab v4 R-MB6a, foresight slides, context PDFs, `hostile-review.md`, salon drafts.

## Key paths
- Audit: `review/mechanism-comparison-umbrella-audit-2026-07-18.md`
- Crosswalk: `appendices/appB-bridge-crosswalk.tex`
- ch48 synthesis: `chapters/ch48-towards-alignment.tex`
- ch35 UAD: `chapters/ch35-multi-agent-strategic-coupling.tex`

## Commits
- Single amended commit on `main` (2026-07-19): umbrella/branding soften, chapter `\ref` links, audit report; includes appF/ch18 follow-up wording.
