# Representational drift

- **Date:** 2022
- **Field:** Neuroscience
- **Source:** https://www.sciencedirect.com/science/article/am/pii/S0959438822001039
- **Source read:** full
- **TSA files consulted:** `chapters/ch18-bearer-maps.tex`, `metadata/concepts/bodies/value-bundle-transport.md`
- **Keywords grepped:** representational drift, population code, neural representation, ontology shift, transport, grounding, representational, drift

## Source ontology

Driscoll, Duncker & Harvey (2022) take a neural “representation” off the list of stable tunings stored in particular cells. Over days to weeks, the pool of neurons correlated with a stimulus, place, or action largely turns over—even while the animal keeps performing the same task and population-level statistics (fraction of task-related cells, overall activity) stay roughly constant. The new object is a temporally evolving relation among population activity, computation, and the environment, with stability that can hold at one grain (behavior, manifold geometry, downstream readout) while identity-level codes drift at another. The authors argue this is unlikely to be only recording damage or cell-tracking error; they treat drift as possibly both a biological nuisance (synaptic turnover) *and* a computational resource for continual learning: allocating new memories to an “excitable” pool so they do not overwrite old ones, and, when memories are revisited, rewriting them into a shared reference frame so temporally separated associations can be related. They also warn that the words “representation” and “drift” smuggle a map-of-the-world picture; some activity is better described as interacting with the world than as encoding it.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** preservative transport / ontology shift (ch18); value-bundle transport (label preservation ≠ meaning); grounding / MB9 silent-gap dual; MB5 successor/ontology-shift (app B).
- **Overlap:** TSA already has a safe mode in which “the representation changes but value relevance is conserved” (ch18 preservative transport) and a failure mode in which labels persist while referents drift (value-bundle transport). Representational drift is empirical existence proof of the first: computation and behavior can survive complete turnover of the implementing units.
- **Gap:** TSA’s ontology shift is a discrete transformation of *categories* (`Ω_t → Ω_{t+1}`), usually a stressor to audit. The source’s primitive is continuous *unit-identity* turnover as the normal dynamics of a living code, with an explicit level split (cell vs population vs readout) and a functional role (separate vs relate memories over time; forget unused associations). TSA cannot currently type “stability is level-relative” or “the code should turn over,” except by stretching preservative transport.

## Applicability to TSA

- **Score (0–5):** 2
- **Why:** This does not add a new alignment cut. It does give a biological operationalization of what *not* to conserve under transport: neuron identity, parameter identity, or a frozen feature-to-variable map. Successor and grounding audits that treat “same units / same features still light up” as evidence of preservation would misread the source. The continual-learning role (drift as anti-interference, not just corruption) is a real underspecification, but it does not rival TSA’s value/bearer/CCI decomposition. Worth a crosswalk cite under MB5/MB9 as the dual of covert transport, not a new bridge.
- **Ontology-stickiness risk:** High for the dual, not the slogan. Pre-2022 (and much current) training treats a representation as a stable code in particular units, or flattens nonstationarity into “concept drift” / catastrophic forgetting. A model will map this onto TSA’s *value* drift (labels stay, meaning moves)—the opposite failure. TSA already *names* preservative transport but frames it as a rare ontology event; the source makes identity-level turnover the default of a code. LLMs will also miss the authors’ own refusal of “representation” as the right object.
- **Recommended action:** cite-in-crosswalk

## One-line finding

Representational drift is the dual of TSA’s covert-transport failure: computation can stay put while implementing units turn over; TSA already has this as preservative transport but not as level-relative, default, possibly useful dynamics of a code.
