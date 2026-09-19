# Teleosemantic reference

- **Date:** 2023-02-23
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/posts/WGEPBmErv8ufrq8Fc/teleosemantics
- **Source read:** full
- **TSA files consulted:** `chapters/ch03-dynamical-guarantee.tex`, `metadata/concepts/bodies/grounding-viability.md`
- **Keywords grepped:** teleosemantic, aboutness, symbol grounding, semantic reference, representation, grounding, optimization history, accurately track

## Source ontology

Abram Demski’s update: a symbolic construct is *about* whatever optimization shaped it to accurately reflect. That replaces map/territory correspondence and mutual-information “fit” as the account of reference. Mutual information is symmetric and admits accidental correspondence plus global-fit puzzles about false belief; optimization history is directed (the map is selected, not the territory) and more local (a symbol’s meaning depends on what *that* symbol was optimized to track). Secondary cuts: denotation vs connotation as optimized-correspondence vs probabilistic implication; honesty as optimizing statements for accuracy rather than for the audience’s belief; a linguistic community as a super-agent that pools accuracy and polices the intended map. ELK/transparency is recast as whether AIs can join that community.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** grounding viability (ch03, MB9); transport (words surviving ≠ meaning surviving); CCI / ValidRef; ELK as latent readout, not full correction.
- **Overlap:** TSA already rejects “same symbols ⇒ same meaning.” Grounding viability (ch03) is the alignment-specific symbol-grounding cut: value-relevant change must move the checked abstraction, correction signal, or uncertainty. Successor stability asks whether later systems preserve the grounding relation, not the vocabulary. Abstraction-gap exploitation is the failure when the checked map stays green.
- **Gap:** TSA’s grounding relation is a present-tense conservative-coupling test, not a generator of aboutness. It cannot say what a representation is about when current covariance is accidental, nor define honesty as “optimized for accuracy vs optimized for audience belief,” nor treat the linguistic community as the unit that polices intended correspondence. Ch03 explicitly declines a theory of intrinsic meaning.

## Applicability to TSA

- **Score (0–5):** 3
- **Why:** The source does not replace grounding viability’s operational cut (that would be a rival semantics TSA already refused). It does add a missing *historical* relation: reference as a product of optimization history. Without that, TSA can detect silent gaps in current maps but cannot distinguish “this monitor was shaped to track X” from “this monitor presently covaries with X.” That distinction matters for ELK, lying, and transport under ontology shift. App B currently maps MB9 to GSAI coverage, not to a theory of aboutness.
- **Ontology-stickiness risk:** High for the split, not the slogan. Pre-2023 training has Millikan-style teleosemantics and Harnad/Searle symbol grounding; it will flatten Demski’s update and TSA’s conservative-abstraction test into “correspondence” or “solve symbol grounding.” Models will miss that TSA *refuses* a full semantics, and that Demski’s primitive is optimization *history*, not current fit.
- **Recommended action:** add-reverse-gap

## One-line finding

TSA can test whether maps still track, but not what they were optimized to be about; teleosemantic reference is the historical generator that grounding viability leaves implicit.
