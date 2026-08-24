# Epistemic legibility

- **Date:** 2022-02-09
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/posts/jbE85wCkRr9z7tqmD/epistemic-legibility
- **Source read:** full
- **TSA files consulted:** `chapters/ch37-alignment-attractor.tex`, `chapters/ch26-correction-channel-integrity.tex`
- **Keywords grepped:** legibility, inspectable, inferential, opaque, epistemic opacity, inspectability

## Source ontology

Elizabeth (Aceso Under Glass) isolates **epistemic legibility**: how cheap it is to identify a work’s load-bearing claims, evidence, and logical steps and to check or productively disagree with them. The unit is a *claim-system* (essay, book, public-health line, experiment writeup), not a model’s internals. The new relation is orthogonality to truth: a work can be wrong but inspectable, or possibly right but opaque (four-quadrant). It borrows Scott’s “legible” (scalable, low-context, standardized) while warning that excess demand cuts illegible value, kills butterfly ideas, and, unilaterally in adversarial settings, supplies keys for effective lies. Inferential distance is handled as error-vs-silent-fail: the reader should leave knowing they did not understand, not thinking they did.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** field \(L_t\) and “legibility to correction” (ch37); directional transparency / three Scott-derived channels (ch26); locatable bridges (appB); experiment checkability (concept body `experiment-methodology`); strategic/self-opacity (ch10, ch32)
- **Overlap:** ch37 defines \(L_t\) as how much of the work outsiders can understand without adopting the originating ontology, and treats illegibility as a priesthood risk. ch26 quotes Scott and then *bounds* legibility by direction (system→audit high; human→AI assistance adequate; human→AI manipulation small). appB’s “make unsolved-ness locatable” is the same operational move as “easy to epistemic spot-check.”
- **Gap:** TSA’s “legibility” is overloaded onto systems, fields, and power, not onto *inferential structure ⊥ truth*. TSA can say “the field is opaque to outsiders” or “the system is opaque to auditors”; it cannot, without stretching, say “this safety case is false but checkable” versus “possibly true but has no hooks.” Directional transparency is a capture constraint, not a discourse axis. Goal-laundering (cheap-to-fake signals) is nearby but tracks *cost of faking*, not *cost of arguing*.

## Applicability to TSA

- **Score (0–5):** 3
- **Why:** The split is load-bearing for TSA’s own hygiene—bridges, hostile tests, experiment negatives, safety-case artifacts—without competing with boundary, bundle, CCI, successor, or basin. A reverse-gap note would stop collapsing Elizabeth into \(L_t\) or Scott-statecraft. Score 4 would require changing a TSA cut; this does not. Score 2 would underweight that TSA already uses the *word* while missing the *axis*.
- **Ontology-stickiness risk:** High for pre-2022 training (Scott, interpretability, “transparency”). TSA already includes Scott and directional channels, so the failure mode is rename-and-exclude: treating epistemic legibility as already covered by \(L_t\) or CCI, and losing “wrong but inspectable.” LLM-drafted TSA prose is especially likely to maximize rhetorical smoothness over checkable cruxes.
- **Recommended action:** add-reverse-gap

## One-line finding

TSA already names several “legibilities”; it still lacks Elizabeth’s axis that a claim-system can be wrong-but-inspectable or possibly-right-but-opaque.
