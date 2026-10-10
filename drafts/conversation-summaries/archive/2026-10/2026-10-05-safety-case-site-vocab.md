# 2026-10-05 — Safety-case site vocabulary

kind: correction
uptake: status

## Trigger
Use “safety case” as the public noun on the site; keep the agreed adjectives; use “evidence the case can use”; rename URLs, YAML keys, and code (not frozen).

Prompts: (paraphrase — this session)

## Done
- content: App P section titles and stack noun aligned (safety-case stack, false accept \(F\)); TeX labels `sec:appp-assurance` kept.
- content: Predictions hub, overview card, funding card, demo page use safety-case / false-accept / “evidence the case can use.”
- housekeeping: `metadata/safety-case-model.yml`; `/predictions/safety-case/` with redirect from `/predictions/assurance/`; `sync:safety-case-model`; `computeSafetyCaseUpdate`.
- verification: `npm run sync:predictions` → `wrote 20 cards`; `sync:safety-case-model` → `Lean identifier check passed`; `safety-case-demo.test.ts` → 4 pass.

## Decisions
- Noun = safety case; modifier = safety-case; event \(F\) = false accept. No new verbs.
- Field-agenda “formal assurance” left as other people’s term.
- Lane plan filename `assurance-risk-modelling.md` left (historical); live paths inside it now point at the new files.

## Open / next
- PRA acronym still used once in App P with expansion; site demo no longer says PRA in the title.

## Key paths
- `metadata/safety-case-model.yml`
- `site/src/pages/predictions/safety-case/index.astro`
- `appendices/appP-bridge-predictions.tex`

## Commits
- none
