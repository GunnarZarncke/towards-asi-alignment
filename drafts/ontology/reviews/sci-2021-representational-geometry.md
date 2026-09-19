# Neural population / representational geometry

- **Date:** 2021
- **Field:** Neuroscience
- **Source:** https://www.nature.com/articles/s41583-021-00502-3
- **Source read:** full
- **TSA files consulted:** `chapters/ch03-dynamical-guarantee.tex`, `chapters/ch15-values-compressed-control.tex`
- **Keywords grepped:** representational geometry, population geometry, neural manifold, tuning curve, manifold, geometry, decoder, population

## Source ontology

Kriegeskorte & Wei recarve the explanatory unit of a neural code. Classically it is neuron *i*'s tuning curve (how one cell's firing depends on a stimulus variable, often scored by Fisher information). The complementary object is *representational geometry*: the pairwise distances among population response patterns in multivariate response space — equivalently the manifold traced as the population state moves with the stimulus. Tuning induces geometry, but many tunings (including rotations and neuron permutations) induce the same geometry; the geometry, not the named cells, is the sufficient statistic for what linear (and many nonlinear) decoders can extract, and it determines Fisher information (local), mutual information, and ideal-observer psychophysics. A representational dissimilarity matrix abstracts away from individual neurons. Chung & Abbott (2021) treat the same population-geometry object as a shared descriptor for brains and ANNs (dimensionality, radius, untangling, classification capacity). The recarving is B→A-ish: RSA and population coding predate 2021; the 2021 cut is the dual-perspective claim that geometry, not the unit list, is what the code *is* for downstream readout.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** value-bundle response geometry \(G_B\) (ch03, ch15); control manifold \(\mathcal{M}_B\) (ch15); transport (words surviving ≠ meaning surviving). App B maps mechanistic interpretability to instruments under adversarial verifiability, not to a geometry layer.
- **Overlap:** Both refuse to reify the named unit (neuron; value-word) and conserve a relational geometry of how distinctions change what can be read out or how policy moves. Ch03's conserved object is explicitly "the response geometry," not the policy or the labels.
- **Gap:** TSA's geometry is \(\partial\pi/\partial B\) — how policy changes when bundle coordinates become salient. It is not the pairwise distance structure of population or activation states. TSA cannot currently say that two internal codes are the same representation if the RDM/manifold matches after a rotation that remaps every unit. That is the internal analog of transport, and it is only a homograph of bundle geometry.

## Applicability to TSA

- **Score (0–5):** 2
- **Why:** The recarving is real, and the word-collision is load-bearing for LLM-drafted TSA prose, but the source does not supply a missing alignment primitive. Absorbing population geometry as a special case of \(G_B\) would hide that TSA has no account of internal representational distances, linear-decoder information, or "same geometry, different units." A reverse-gap (score 3) would overclaim: TSA is not a theory of neural codes, and App B already declines to treat mechinterp as a solution layer. The right use is a crosswalk note: circuits/tuning are the unit-side analog; RSA/manifolds are the geometry-side analog; neither is bundle response geometry.
- **Ontology-stickiness risk:** High for the homograph, not for the slogan. Pre-2021 training already has RSA (Kriegeskorte 2008/2013) and population coding; models will treat "geometry" as one object and flatten TSA's \(G_B\) into activation-space RDMs (or vice versa). TSA already *includes a different object under the same word*, so a model can miss the exclusion even when it "knows" representational geometry.
- **Recommended action:** cite-in-crosswalk

## One-line finding

TSA already conserves a "response geometry," but that object is how policy changes with value-bundle salience; Kriegeskorte–Wei’s primitive is the pairwise geometry of population states — a homograph to cite, not a special case of the bundle.
