# 2026-08-25 — Site glossary sync and UAD name fix

## Trigger
Follow homograph hygiene with companion-site sync; add missing App E glossary terms; user flagged “Unit-attribution discovery” as erroneous and asked to unify on Unsupervised Agent Discovery.

## Done
- `npm run sync` (full site); tracked edits: Field intro + bridge-assumptions → App B §Ontology homographs link.
- `metadata/concepts.yml`: 13 new `glossaryTerms` (subagent, goal, simulacra, legibility, selection divergence, pointing split, UAD, VFS/BIQ/EAI, \(J_t\), etc.); homograph tweaks on correction-audit evasion, preservation conditions, deployment growth rate.
- `sync:concepts` + `build:search-index` (54 glossary entries).
- PDF rebuild (`./build.sh`) verified.
- Replaced all **Unit-attribution discovery** → **Unsupervised Agent Discovery** (App E, App N ES-1, concepts.yml, inter-agenda glossary, draft audit/prose, archive log).
- App E remains PDF-only on site; `/glossary/` sourced from `concepts.yml`.

## Decisions
- Do not add App E as a synced full appendix page this session.
- Do not implement Ngo per-agenda reverse column (still on `drafts/plans/field.md`).
- Left ordinary “unit attribution” in embedded-simulation milestone (step-level wording, not formal UAD term).

## Open / next
- Field intro still says “App E is synced separately” — slightly misleading; optional one-line fix.
- ch18 organoid bearer-vs-computer homograph line still not landed.

## Key paths
- `metadata/concepts.yml`, `site/src/content/field/intro.md`
- `appendices/appE-glossary.tex`, `appendices/appN-experimental-evidence.tex`

## Commits
- (this session)
