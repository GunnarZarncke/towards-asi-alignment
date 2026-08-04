# 2026-08-02 — App E glossary sync with inter-agenda glossary

## Trigger
User asked to review `appendices/appE-glossary.tex` against `reference/field-agendas/inter-agenda-term-glossary.md` for clarifications, additions, and disambiguations; then to implement agreed changes (steps 1–4), leaving site `concepts.yml` parity for later.

## Done
- Expanded `appendices/appE-glossary.tex` (~170→212 lines):
  - **Homographs:** CCI (Christiano vs MIRI/CHAI); selection environment + Demski/Wentworth on `Fit_E`; experimental BIQ vs hidden productive B-IQ.
  - **New section** *Strategic coupling and verifiability:* strategic opacity, hidden productive B-IQ bound, ICI, adversarial verifiability, certification-under-manipulation.
  - **Selection:** restored `selection environment` headword with deployment-environment plain alias; nearest-field on deployment leverage.
  - **Nearest-field deltas:** boundary (Friston), goal, transport, value bundle (shard/CIRL), alignment basin (Christiano), conserved properties (tiling/MB10).
  - Preservation conditions list: `hidden productive B-IQ bounds` (was `hidden productive-control bounds`).
- Updated `drafts/glossary-term-audit.md` — App E sync marked shipped; site still open.
- Updated `drafts/conversation-summaries/HANDOFF.md` — terminology demotion open work trimmed.

## Decisions
- Did not rename `\label{appf-glossary}` — many manuscript refs depend on it.
- Did not add substitution hazards to App E — App F Meta vs object-level split stays in research-program appendix.
- Site `metadata/concepts.yml` parity deferred per user.

## Open / next
- Site `concepts.yml` / concept cards parity with App E (MB6, CCI, new headwords).
- Residual appendices grep for demotion drift (`drafts/glossary-term-audit.md`).

## Key paths
- `appendices/appE-glossary.tex`
- `reference/field-agendas/inter-agenda-term-glossary.md`
- `drafts/glossary-term-audit.md`

## Commits
- (this session)

## Not staged (other working tree)
- Field agenda index / site field-agenda layer, conversation-summary archive moves, unrelated drafts — left out of this commit.
