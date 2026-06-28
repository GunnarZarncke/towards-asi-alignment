# Chapter Split Preferences

Recorded 2026-06-28 after reviewing chapter size, pages, formulas, section/subsection counts, and material complexity.

## Quantitative Signals

The heaviest chapters by composite size / complexity were:

- ch25 — `Correction-Channel Integrity`: 35 pages, 84 formulas, 27 sections.
- ch24 — `Correction Is a Causal Channel`: 31 pages, 94 formulas, 26 sections.
- ch19 — `Tradeoffs and Bundle Geometry`: 29 pages, 94 formulas.
- ch20 — `From Rewards to Values`: 28 pages, 91 formulas.
- ch18 — `What Values Apply To`: 27 pages, 74 formulas, 26 sections.
- ch35 — `The Alignment Attractor`: 32 pages, 26 sections, 39 subsections.
- ch07 — `Finding the Boundary`: 32 pages, 53 formulas.
- ch34 — `Parasites in the Correction System`: 24 pages, 67 formulas, 24 sections.
- ch27 — `Manipulation, Domestication, and False Consent`: 31 pages, 62 formulas, 29 subsections.
- ch36 — `Passive Observation Is Not Enough`: 29 pages, 64 formulas, 38 subsections.

These are signals for editorial pressure, not automatic split decisions.

## Author Preferences

Detailed plans:

- ch19: see `review/ch19-split-plan-2026-06-28.md`.
- ch25: see `review/ch25-split-plan-2026-06-28.md`.
- ch35: see `review/ch35-split-plan-2026-06-28.md`.

### Preferred Splits

- **ch19** — split into:
  - `geometry / tradeoffs`;
  - `measurement / Goodhart / social-choice`.
  - Detailed plan: `review/ch19-split-plan-2026-06-28.md`.
  - Implemented 2026-06-28 as `ch19` + `ch19b`.

- **ch35** — split into:
  - `alignment-attractor theory`;
  - `artifact / conductivity / pivotal-process governance`.
  - Detailed plan: `review/ch35-split-plan-2026-06-28.md`.
  - Implemented 2026-06-28 as `ch35` + `ch35b`.

### Possible But Not Critical

- **ch36** — split into:
  - `observation limits`;
  - `active / adversarial measurement`.

This may work, but is not currently critical.

### Keep Together Unless Convinced

- **ch25** — suggested split was `CCI definition / calibration` versus `applications / separations / safety-case use`.

Author preference: keep theory and application together if possible. A split should require a stronger argument, because the point of the chapter is partly that CCI definition, calibration, failure modes, and use cases constrain each other.

### Keep Together

Do not split these on size alone:

- **ch24** — keep correction-channel theory, examples, and subsumptions together for now.
- **ch20** — keep reward-to-bundle inference together for now.
- **ch18** — restructure if needed, but do not split by default.
- **ch16** — consolidate heading granularity if needed, but do not split by default.
- **ch34** — keep as one memorable parasite chapter; trim or consolidate sections if needed.
- **ch11** — structure pass rather than split.
- **ch27** — only split if reviewer fatigue specifically appears.
- **ch07** — keep as one foundational boundary chapter; consider moving worked examples/procedures to appendix before splitting.

## Next Step

If doing a split pass, start with ch19 and ch35 only. Draft a chapter-map proposal before moving text, because splitting these affects part summaries, cross-references, generated tables, labels, and possibly chapter numbering.
