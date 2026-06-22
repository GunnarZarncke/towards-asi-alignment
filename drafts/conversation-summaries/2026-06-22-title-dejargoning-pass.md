# Title de-jargoning pass (Parts IV/V/IX and several chapters)

**Date:** 2026-06-22
**Trigger:** Reader feedback on Parts IV–IX: jargon density in TOC titles ("Bundle Geometry," "Bearer Maps," "Goal Laundering," "Multi-Scale Decomposition," "Extrapolative Correction"); near-duplicate "Bearers" chapters (18 vs 43) with no signposted difference; ch23 ("Semantic, Bundle, Bearer, and Correction Transport") flagged as the most opaque title in the book; "cruxes" friction for funders/generalists. Plus a separate note about over-segmented chapters (1, 6, 16) and a Part V skim-energy drop.

## What was done

Applied **title renames only** (user authorized "all title swaps", mix style, keep "goal laundering"). No prose or section-structure changes yet.

Renames (old → new):

- Part IV: Human Values as Bundle Geometry → **What Human Values Actually Are**
- Part V: Goal Inference → **Reading a System's Goals**
- Part IX: Safety Cases, Adversaries, and Open Cruxes → **Safety Cases, Adversaries, and Open Questions**
- Ch18: Bearers: What Values Apply To → **What Values Apply To** (technical bearer concept)
- Ch43: The Bearers of Value → **Who Still Counts After Transformation** (philosophical bearer question; differentiated from ch18)
- Ch23: Semantic, Bundle, Bearer, and Correction Transport → **When the Words Survive but the Meaning Doesn't** (from chapter thesis; "transport stack" kept as internal section structure)
- Ch38: Multi-Scale Decomposition → **Checking a System at Every Level**
- Ch26: From Obedience to Extrapolative Correction → **Beyond Literal Obedience**
- Ch20: From Reward Inference to Bundle Inference → **From Rewards to Values**
- Ch22: Inferring Goal Transport → **Has the Goal Really Survived?**

Kept deliberately: Ch37 "Detecting Goal Laundering" (vivid, self-explaining metaphor — earns its keep); Ch21 "The Compression Test for Intention" (already concrete); "bundle geometry"/"goal inference" as in-text section/concept terms.

## Files touched

- `parts/part04-value-bundles.tex`, `parts/part05-goal-inference.tex`, `parts/part09-safety-cases.tex` (`\part{}` lines)
- `chapters/ch18,ch20,ch22,ch23,ch26,ch38,ch43` (`\chapter{}` lines only)
- `metadata/book.yml` (title fields)
- `tables/chapter-map.tex` (maintainer table rows)
- `INSTRUCTIONS.md` (§4 part list + detailed chapter list)
- `README.md` (part overview table)

## Non-obvious decisions

- Left `context/lw-references.md` and dated conversation-summaries untouched per AGENTS.md (context/ is source canon; logs are historical records). They still show old titles; minor staleness, mentioned here.
- `\label`s, filenames, and `\ref`/`\autoref` cross-refs unchanged, so no internal-reference breakage. Internal section headers using "bundle geometry"/"goal inference" as concepts were intentionally not renamed.

## Verification

- `make check` → structure check passed; citation check passed (107 cited / 301 in bib). No full PDF rebuild run this session.

## Open / next steps (NOT done, proposed and waiting)

- Section over-segmentation: Ch1 (17→~6), Ch6 (17→~6), Ch16 (**24**→~9). Proposed merge groupings exist in chat; these need heading-level changes + light connective prose.
- Part V "drag": chapter hooks improved via titles, but the four-chapter inference run may still warrant a concrete opening hook.
- Consider updating `context/lw-references.md` titles if desired (skipped per rules).
