# 2026-08-02 — Glossary demotion pass (manuscript + deployment leverage)

## Trigger
User asked to implement edits from `drafts/glossary-term-audit.md`; then retire **deployment mass** entirely in favor of **deployment leverage** everywhere.

## Done
- Plain-first demotion: `selection environment` → `deployment environment` outside ch34 home; `selection handle` → `point of control over deployment` outside ch34/appE; ch10 anthropic capture cite/disambiguation.
- Retired coined term **deployment mass** → **deployment leverage** across manuscript, appendices, experiments, metadata, site, inter-agenda glossary, Lean comments.
- ch34/appE definitions simplified (no “for short” alias for μ_E).
- Updated `drafts/glossary-term-audit.md` (shipped vs open queue).

## Decisions
- Keep equation labels `eq:deployment-mass-*` and Lean `DeploymentMass` axiom name (cross-ref stability).
- `metadata/notation-index.tex` and `site/public/search-index.json` are gitignored; regen from `metadata/notation.md` / site build as needed.

## Open / next
- Site concepts.yml MB6/CCI card parity spot-check.
- Optional: rename eq labels / Lean axiom in a dedicated pass (high churn).

## Key paths
- `drafts/glossary-term-audit.md`
- `chapters/ch34-selection-environment.tex`, `appendices/appE-glossary.tex`

## Commits
- (pending this session)
