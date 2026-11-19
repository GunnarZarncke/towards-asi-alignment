# 2026-11-10 — Compendium vs TSA and chapter cites

kind: new-work
uptake: local

## Trigger
How [Griffin Hilly's AI Safety Compendium](https://aisafetycompendium.com/compendium/) relates to TSA; whether to add it to the spec sheet; which compendium-sourced items deserve manuscript references; apply cites via chapter rereads; clarify Ch. 9 composite-agency prose; commit; what Griffin is trying to achieve with the map.
Prompts: (none recorded)

## Done
- notes: Compared compendium to TSA — meta-survey of 154 approaches / 24 overviews vs bridge×agenda field map; no mutual citation. Spec sheet: **no** (columns are programs that ship, not lookup census). Useful compendium references for gaps, not the compendium itself.
- content: Ch. 27 — Roger et al. 2023 measurement tampering; Belrose et al. 2024 MAD update (after detected-tampering training point).
- content: Ch. 28 — O'Keefe et al. 2025 law-following AI as obedience, after local examples.
- content: Ch. 9 — nesting paragraph (company made of agents; hierarchical/group/scale-free cited; chapter asks where the composite agent is); tests sentence names composite agent.
- bookkeeping: Six bib keys + `\bibsummary`; `.venv/bin/python scripts/check_bibliography_summaries.py` — 580/580 passed.
- housekeeping: Commit `2ecb256ee4` (not pushed). Hook added `edit-attribution/span-ledger.json` to commit.
- notes: Griffin's stated aim — map ideas to avoid rederiving, find comparative advantage; site = lookup + neglect scoring + open Tailwind-style opportunities; his research = human agency taxonomy, voluntary disempowerment pilot, Alignment by Onion (closest to TSA ch27/ch29, not the field hub).

## Decisions
- Do not add compendium to `product-comparison.yml` or a Surveys column.
- Optional later: one bullet on [field-map starting points](https://towards-alignment.com/cards/concept/field-map-starting-points/) card only.
- Gabriel & Keeling 2025 (`fair treatment of claims`) deferred to `papers/alignment-criteria/`.

## Open / next
- Push `2ecb256ee4` when ready.
- Gabriel & Keeling in alignment-criteria paper if desired.
- Outreach to Griffin only if Gunnar wants dialogue on agency/disempowerment vs correction-channel framing (no draft prepared).

## Key paths
- `chapters/ch09-composite-agent.tex`, `ch27-correction-channels-adversarial-pressure.tex`, `ch28-extrapolative-correction.tex`
- `metadata/concepts/bodies/field-map-starting-points.md`
- https://aisafetycompendium.com/compendium/ · https://griffinhilly.com/

## Commits
- `2ecb256ee4` Cite measurement tampering, law-following AI, and group agency in Ch. 9, 27, 28.
