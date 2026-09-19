# Generalized adverse selection

- **Date:** 2024-03-14
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/posts/vyAZyYh3qsqcJwwPn/towards-a-broader-conception-of-adverse-selection
- **Source read:** full
- **TSA files consulted:** `metadata/concepts/bodies/goodhart-as-selector.md`; `metadata/concepts/bodies/attractor-control.md`
- **Keywords grepped:** adverse selection; selection-conditioned; winner's curse; selection environment; Fit_E; attractor; information asymmetry; Goodhart

## Source ontology

Heicklen recasts **adverse selection** from a market-lemons phenomenon into a general observation type: an opportunity is a leftover. Conditional on getting to take a “trade” (any decision, agreement, plan, or exchange in a competitive environment), the deal is worse than a naive model that treats availability as a random sample. Availability itself is evidence that other agents passed, or took the other side. The unit is not hidden product quality or a special auction, but **selection-conditioned leftover options**.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** selection environment / \(\mathrm{Fit}_E\) (ch34, MB6); Goodhart-as-selector (ch34); goal laundering / cost of faking (ch40, ch43); false attractors (ch37)
- **Overlap:** TSA already treats deployment as non-random leftover: institutions copy, fund, and audit systems. Goodhart-as-selector uses the same inequality shape—\(\mathbb{E}[P \mid M \text{ extremely high}]\) can be worse than a moderate \(M\)—because the proxy became a selector. Goal laundering and false attractors are the case where what reaches you as “safety” survived presentation-selection.
- **Gap:** TSA’s load-bearing “selection” is forward population dynamics of *systems* (\(\mu_E\), \(\mathrm{Fit}_E\)), not an epistemic update from being offered an option. Chapters never name adverse selection, leftover availability, or “conditional on getting to trade.” Stretching \(\mathrm{Fit}_E\) to cover proposals, evals, talent, or techniques that reached *you* would be a hostile-test rename.

## Applicability to TSA

- **Score (0–5):** 2
- **Why:** Alignment-relevant as a caution about leftover safety artifacts and leftover systems, not a missing spine claim. Cite beside Goodhart-as-selector / MB6 as a related epistemic pattern; do not absorb into ch34. The glossary already splits selection homographs (\(\mathrm{Fit}_E\) vs Wentworth vs Goodhart); this is a fourth, weaker one.
- **Ontology-stickiness risk:** Medium. Pre-2024 models have Akerlof lemons and winner’s curse, not availability-as-observation. Drafting models will map “selection” onto ch34/MB6. TSA includes nearby forward-selection objects, not this leftover-observation primitive.
- **Recommended action:** cite-in-crosswalk

## One-line finding

Heicklen’s leftover-opportunity observation is adjacent to TSA’s Goodhart-as-selector and \(\mathrm{Fit}_E\) machinery but is an epistemic unit—availability as evidence of others’ rejection—that the manuscript never names and should not rename into deployment growth rates.
