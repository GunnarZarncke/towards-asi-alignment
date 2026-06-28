# ch19 Split Plan — Bundle Geometry and Measurement Pressure

## Executive Decision

Split ch19 by **geometry/tradeoffs vs. measurement/Goodhart/social-choice**.

The current chapter is mathematically dense: 29 pages and 94 formulas. It combines the core geometry of value-bundle tradeoffs with later questions about measurement, cross-agent comparison, Goodhart pressure, toy models, social choice, and moral learning. Those are connected, but they ask different reader questions:

- What is bundle geometry?
- How do we measure, compare, and protect it under pressure?

Titles:

1. **Tradeoffs and Bundle Geometry**  
   The conceptual and mathematical geometry: scalar-value failure, bundle coordinates, tradeoffs, response geometry, feasible sets, lexical regions, uncertainty, ontology/substrate transfer.

2. **Measuring and Stress-Testing Bundle Geometry**  
   The operational/adversarial layer: comparing geometries, measurement, Goodhart pressure, toy model, social choice, moral learning, superintelligence relevance, falsifiers.

## Proposed Chapter Boundary

Preferred split point:

- Chapter A ends after `\section{Substrate Transfer}`.
- Chapter B begins with `\section{Comparing Geometries across Agents}`.

Rationale:

- Through `Substrate Transfer`, the chapter is still defining what it means for bundle geometry and tradeoff structure to survive changes in context, ontology, and substrate.
- `Comparing Geometries across Agents` begins the measurement/comparison problem.
- Everything after that naturally asks how to detect, compare, stress-test, or govern geometry.


## Content Allocation

### Chapter A: Tradeoffs and Bundle Geometry

Keep these sections from current ch19:

- `The Problem with Scalar Values`
  - Keep as opening motivation.
  - It explains why scalar reward/value accounts are the wrong shape for tradeoffs.

- `From Value Lists to Bundle Coordinates`
  - Keep.
  - This transitions from verbal lists to coordinate geometry.

- `Tradeoffs Are Not Defects`
  - Keep.
  - This is part of the core philosophical/mathematical framing.

- `The Value-Bundle Response Geometry`
  - Keep.
  - This is a central definitional section.

- `Examples of Bundle Interactions`
  - Keep, but consider shortening.
  - The examples help readers understand geometry before formal material.

- `Feasible Sets and Pareto Fronts`
  - Keep.
  - Core geometry.

- `Lexical Regions and Protected Directions`
  - Keep.
  - Core to the book's non-scalar account of protected values.

- `Bundle Metrics`
  - Two options:
    - Preferred: keep if it defines the basic mathematical objects used by Chapter A.
    - Alternative: move to Chapter B if it reads primarily as measurement procedure.
  - If kept, end the section with a warning that metrics become dangerous under Goodhart pressure, which Chapter B handles.

- `Contextual Weights and Their Failure Modes`
  - Keep if the point is that weights are part of the geometry.
  - Move if the section mainly discusses measurement failure.
  - Recommended: keep a short definitional version in Chapter A, move detailed failure modes to Chapter B if they can be separated cleanly.

- `Uncertainty and Reversibility`
  - Keep.
  - Core to how tradeoff geometry should be handled when uncertain.

- `Bundle Geometry and Ontology Shift`
  - Keep.
  - This is still preservation of geometry, not measurement of it.

- `Substrate Transfer`
  - Keep as Chapter A's closing stress on the definition.
  - It connects geometry to transformation and sets up why measurement/comparison is needed.

Add a new closing section:

- `What Geometry Gives Us`
  - Short bridge.
  - State:
    - bundle geometry avoids scalar collapse;
    - tradeoffs are structured, not noise;
    - ontology/substrate shift makes preservation nontrivial;
    - the next chapter asks how to measure and stress-test this geometry without Goodharting it.

### Chapter B: Measuring and Stress-Testing Bundle Geometry

Move these sections from current ch19:

- `Comparing Geometries across Agents`
  - Opening section.
  - It naturally asks what it means to compare geometries once the geometry has been defined.

- `Measuring Bundle Geometry`
  - Move.
  - This becomes the operational core.
  - Keep subsections:
    - `behavioral-perturbation`;
    - `representation-probing`;
    - `correction-channel-testing-geometry`.

- `Goodhart Pressure on Bundle Geometry`
  - Move.
  - This is one of the main reasons the split helps.
  - Keep subsections:
    - `semantic-without-geometric-geometry`;
    - `benchmark-vs-deployment-geometry`;
    - `bearer-map-shrinkage-geometry`;
    - `tradeoff-laundering`;
    - `context-manipulation-geometry`.

- `A Worked Toy Model`
  - Move.
  - It belongs with measurement/stress-testing.

- `Bundle Geometry and Social Choice`
  - Move.
  - This is not core geometry; it is what happens when multiple agents/geometries must be aggregated.

- `Moral Learning as Geometry Revision`
  - Move.
  - This is an application of the geometry to learning and revision.

- `Why This Matters for Superintelligence`
  - Move.
  - It summarizes the measurement/stress implications.

- `What Would Change This View`
  - split.
    - Chapter A gets a short WWCTV about scalar sufficiency, arbitrary values, or geometry not being stable/useful.
    - Chapter B keeps the existing WWCTV and rewrites it around measurement, Goodhart, and social-choice failure.

- `Summary`
  - Write new for both.

Add a new opening section:

- `From Geometry to Measurement`
  - One-page recap.
  - State: "The previous chapter defined the geometry. This chapter asks how one would compare, measure, and protect it under optimization pressure."

Expected result:

- Chapter A gives readers the conceptual/mathematical object.
- Chapter B gives reviewers the operational and adversarial test surface.

## Connection Between The Two Chapters

### End of Chapter A

Add a bridge paragraph:

> The preceding sections define value-bundle geometry as a structured space of activations, tradeoffs, feasible sets, protected directions, uncertainty, and ontology-sensitive preservation. But a geometry that cannot be compared or measured is not yet an alignment artifact. The next chapter asks how bundle geometry can be inferred, compared, and stress-tested without collapsing into semantic labels, benchmark proxies, or social-choice artifacts.

### Start of Chapter B

Open with:

> This chapter assumes the value-bundle geometry of the previous chapter and asks the operational question: when do we have evidence that the geometry has been preserved? Measurement is necessary, but measurement is also where Goodhart pressure enters.

### Cross-References

Use stable labels:

- Keep `ch:tradeoffs-bundle-geometry` on Chapter A.
- Give Chapter B a new label, e.g. `ch:measuring-stress-testing-bundle-geometry`.
- References to tradeoffs / feasible sets / protected directions -> Chapter A.
- References to measurement, Goodhart, cross-agent comparison, social choice -> Chapter B.

Avoid renaming section labels during the split unless necessary. Current `-geometry` labels can remain stable even if moved.

## Consequences Of The Split

### File / Chapter Map

Likely file plan:

- Keep `chapters/ch19-tradeoffs-bundle-geometry.tex` as Chapter A.
- Add `chapters/ch19b-measuring-stress-testing-bundle-geometry.tex` as Chapter B if avoiding renumbering.

Alternative:

- Wait for global chapter renumbering and make Chapter B the new ch20, shifting current ch20+.

Recommendation: use temporary `ch19b` only if the project is comfortable with another `b` chapter before global numbering cleanup. Otherwise, record the split plan and execute during the chapter-numbering cleanup pass.

### Part IV

Update `parts/part04-value-bundles.tex`:

- Insert the new chapter after ch19 or after the current ch19 split point.
- Update the part intro:
  - "tradeoff geometry and bearer maps" -> "tradeoff geometry, bearer maps, and measurement under Goodhart pressure."

### `metadata/book.yml`

Add `ch19b` if using temporary numbering:

- title: `Measuring and Stress-Testing Bundle Geometry`
- status: reviewed (under the current convention: feedback received, not final)
- word_target: 6000-8000
- formal_density: high
- reviewer_needed: `[alignment, mathematics, social-choice]` or `[alignment, information-theory, mathematics]`
- note: inserted after ch19; avoid renumbering until chapter-numbering cleanup.

Regenerate tables:

- `python3 scripts/generate_tables.py`

### Labels And Cross-References

Labels likely to remain in Chapter A:

- `ch:tradeoffs-bundle-geometry`
- `sec:problem-with-scalar-values`
- `sec:value-lists-bundle-coordinates`
- `sec:tradeoffs-not-defects`
- `sec:value-bundle-response-geometry`
- `sec:examples-bundle-interactions`
- `sec:feasible-sets-pareto-fronts`
- `sec:lexical-regions`
- `sec:bundle-metrics` if kept
- `sec:contextual-weights` if kept
- `sec:uncertainty-reversibility`
- `sec:ontology-shift-geometry`
- `sec:substrate-transfer-geometry`

Labels likely to move to Chapter B:

- `sec:comparing-geometries`
- `sec:measuring-bundle-geometry`
- `sec:behavioral-perturbation`
- `sec:representation-probing`
- `sec:correction-channel-testing-geometry`
- `sec:goodhart-bundle-geometry`
- `sec:semantic-without-geometric-geometry`
- `sec:benchmark-vs-deployment-geometry`
- `sec:bearer-map-shrinkage-geometry`
- `sec:tradeoff-laundering`
- `sec:context-manipulation-geometry`
- `sec:worked-toy-model-geometry`
- `sec:social-choice`
- `sec:moral-learning-geometry-revision`
- `sec:why-matters-superintelligence-geometry`
- `sec:wwctv-tradeoffs-bundle-geometry`
- `sec:summary-tradeoffs-geometry`

### Downstream Consequences

Review and potentially update:

- `chapters/ch20-reward-to-bundle-inference.tex`
  - It likely references ch19 for geometry; point measurement-related claims to ch19b.
- `chapters/ch22-goal-transport.tex`
  - Bundle preservation references may stay ch19; measurement/Goodhart references may move ch19b.
- `chapters/ch23-transport-types.tex`
  - Transport of bundle geometry may cite both.
- `chapters/ch37-goal-laundering.tex`
  - Tradeoff laundering should probably cite ch19b.
- `appendices/appC-value-bundle-inference.tex`
  - If expanded, ch19b is a natural source.
- `metadata/notation.md`
  - `G_B` / geometry notation home likely remains ch19.
  - Measurement-specific notation may get ch19b only if needed.

## Implementation Order

1. Create new chapter shell.
2. Move measurement/stress sections.
3. Rewrite ch19 close and ch19b open.
4. Split WWCTV and summaries.
5. Update Part IV, `metadata/book.yml`, generated tables.
6. Search/review cross-references to ch19 and moved section labels.
7. Run:
   - `python3 scripts/generate_tables.py`
   - `make check`
   - `./build.sh`
   - `python3 scripts/book_stats.py`

## Open Editorial Questions

- Does `Bundle Metrics` stay with geometry or move to measurement?
- Should contextual-weight failure modes be split between chapters?
- Should social choice remain in ch19b or become part of a later civilizational/governance chapter?
- Should the worked toy model be kept in ch19b or moved to Appendix C?
