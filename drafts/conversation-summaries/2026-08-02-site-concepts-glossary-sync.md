# 2026-08-02 — Site concepts glossary sync

## Trigger
User asked to sync site `metadata/concepts.yml` with App E / inter-agenda glossary (deferred from App E session); then end-of-session commit.

## Done
- Updated `metadata/concepts.yml` glossaryTerms: deployment leverage/growth rate, preservation conditions, selection environment; CCI Christiano vs MIRI homograph; boundary Friston note; value bundle/transport; strategic opacity + hidden B-IQ; ICI; adversarial verifiability + certification-under-manipulation; conserved properties.
- Fixed stale **ch46** equation refs → ch25/ch26/ch34.
- Bodies: `correction-channel-integrity`, `attractor-control`, `strategic-opacity`, `mb7-hidden-capability-and-access`.
- Ran `npm run sync:concepts` (51 cards + `site/src/data/glossary.json` — build artifacts, not git-tracked).
- Updated `drafts/glossary-term-audit.md` and `HANDOFF.md` — terminology demotion track complete.

## Decisions
- Source of truth remains `metadata/concepts.yml` + bodies; generated site cards rebuilt at sync time.

## Open / next
- Residual appendices grep for demotion drift (`drafts/glossary-term-audit.md`).
- Thin glossary leftovers (`drafts/glossary-prose-pass/THIN.md`).

## Key paths
- `metadata/concepts.yml`
- `appendices/appE-glossary.tex`
- `drafts/glossary-term-audit.md`

## Commits
- (this session)
