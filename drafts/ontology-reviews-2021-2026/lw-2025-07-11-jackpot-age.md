# Jackpot Age / Jackpot Paradox

- **Date:** 2025-07-11
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/posts/3xjgM7hcNznACRzBi/the-jackpot-age
- **Source read:** full
- **TSA files consulted:** `chapters/ch34-selection-environment.tex`; `appendices/appB-bridge-crosswalk.tex`
- **Keywords grepped:** jackpot; geometric mean; ergodicity; arithmetic; power law; winner-take-all; median; selection environment

## Source ontology

A multiplicative gamble can have **positive arithmetic expectation** (wealth concentrated in rare jackpot paths) while the **geometric mean / typical trajectory goes to zero**. The post names that split the **Jackpot Paradox** (economists: ergodicity problem; traders: volatility drag) and treats **wealth preference** as an institutional type: log (shrinking risk appetite), linear (constant risk, SBF-style EV), exponential (rising appetite for jackpots). **Jackpot Age** is the regime in which VC, founder mythos, retail speculation, and post-AGI winner-take-all culture select for arithmetic EV even as median mobility, dignity, and compounded civilizational growth deteriorate. “Positive EV growth” stops being one success metric.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** selection environment / \(\mathrm{Fit}_E = d/dt\log\mu_E\) (ch34, Claim 6); alignment-supporting vs alignment-destroying \(E\) (ch34 Selection Alignment Condition); Goodhart selection of proxies (ch34); MB6a/b socio-technical selection and basin stability (App. B); value lock-in as a stably bad basin (App. B); gradual disempowerment / bearers (ch47, App. B MB6).
- **Overlap:** Both refuse to score a lab artifact in isolation. Ch34 already asks which traits reproduce under institutional handles, and App. B already says a stable basin can be stably bad. Multiplicative spread (\(p_{t+1}\propto p_t\exp(\mathrm{Fit}_E)\)) and the alignment externality (locally costly preservation vs selected throughput) are nearby.
- **Gap:** No TSA file grepped uses jackpot, geometric mean, or ergodicity. \(\mathrm{Fit}_E\) is a log *rate of one system’s deployment leverage*, not arithmetic-vs-geometric aggregation over an outcome *distribution*. \(\mu_E\) is a sum of handle capacities. The Selection Alignment Condition compares preservation frequency among growing vs non-growing systems; it does not ask whether aggregate “success” is a 0.0001% tail while typical preservation paths bleed to zero. Linear/exponential wealth preference is not an institutional type. Mapping the Paradox onto \(\mathrm{Fit}_E\)’s log would be a hostile-test rename.

## Applicability to TSA

- **Score (0–5):** 2
- **Why:** Alignment-relevant as a *shape* of Claim 6 failure: an environment can look like growth (arithmetic EV, a few power-law winners) while typical correction-preserving trajectories die. That is already inside alignment-destroying \(E\) plus MB6b’s stably-bad basin; the source does not force a new spine cut. It is worth a short App. B note under the Selection cluster: jackpot-shaped selection (mean up, median/geometric down) is not what \(\mathrm{Fit}_E\) measures, and gradual-disempowerment / bearer loss is the civilizational analogue, not a Kelly theorem.
- **Ontology-stickiness risk:** High for the math (Kelly, ergodicity, volatility drag predate 2021). Medium for the 2025 packaging: institutions as types that maximize arithmetic EV from rare wins. Pre-2025 models will flatten this into expected utility or power laws. Post-TSA drafting will absorb it into \(\mathrm{Fit}_E\) because of the log, or into “selection” because of the homograph. TSA includes a nearby object, not this aggregator split.
- **Recommended action:** cite-in-crosswalk

## One-line finding

The Jackpot Paradox’s arithmetic-vs-geometric split is a named regime of alignment-destroying selection that TSA’s \(\mathrm{Fit}_E\)/basin vocabulary almost covers and will be misread as already covering, but it is not a missing spine primitive.
