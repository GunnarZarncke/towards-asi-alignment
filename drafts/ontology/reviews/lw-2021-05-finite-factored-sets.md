# Finite Factored Sets

- **Date:** 2021-05-23 (talk; sequence 2021-05; near-miss before Aug 2021 cutoff)
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/s/kxs3eeEti9ouwWFzr (intro talk: https://www.lesswrong.com/posts/N5Jm6Nj4HkNKySA5Z/finite-factored-sets)
- **Source read:** full (sequence hub, intro talk, Introduction and Factorizations)
- **TSA files consulted:** `chapters/ch07-finding-boundary.tex`; `appendices/appB-bridge-crosswalk.tex`
- **Keywords grepped:** finite factored; factored set; factorization; Cartesian frames; structural time; orthogonality; Garrabrant; temporal inference

## Source ontology

Garrabrant replaces Pearl’s given collection of variables plus DAG with a **finite factored set**: a set understood as a Cartesian product (factorization dual to partition). From the factorization one reads **history** of a partition (smallest set of factors that determine it), then **structural time** (X before Y iff \(h(X)\subseteq h(Y)\)) and **orthogonality** (disjoint histories; conditional orthogonality as *d*-separation analog). The fundamental theorem equates conditional orthogonality with conditional independence in all distributions on the factored set. Pearl’s “collection of variables” is treated as smuggled factorization data; FFS infers temporal structure from statistical data without that gift, and is meant to handle abstraction, determinism, and later embedded agency.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** ε-boundary discovery / MB1 (ch07); ontology trap (ch11, not opened this pass); App. B “Cartesian frames / FFS; CCD” as co-equal routes to MB1.
- **Overlap:** Ch07 and App. B already name finite factored sets as a factorization-based alternative to interventional boundary recovery: they “factorize influence rather than perturb it,” and WWCTV lists them as a way intervention handles might prove needless. That is a real neighboring instrument for Claim 1 (where is the optimizer?).
- **Gap:** TSA cites FFS under `garrabrant2021cartesian` (Cartesian Frames, arXiv 2109.10996), not the May 2021 sequence or “Temporal Inference with Finite Factored Sets.” The source’s load-bearing primitives are structural time and orthogonality on partitions, not an agent–environment influence cut. TSA cannot currently say “X is structurally before Y” or “X ⊥ Y via disjoint factor histories,” nor use FFS’s promised purchase on abstraction/determinism and conceptual inference. Lumping FFS with Cartesian frames is a hostile-test rename of the ontology.

## Applicability to TSA

- **Score (0–5):** 3
- **Why:** Alignment-relevant as a rival causal/temporal substrate (embedded agency, which abstractions are “before” others) but not a missing spine claim: TSA already chose measurable ε-boundaries plus handles over combinatorial factorization. Absorbing FFS into MB1 as “another boundary instrument” would leave the time/orthogonality primitive unexpressed. Remaining work is a reverse gap: App. B already lists FFS, so later drafting will treat the primitive as absorbed when only the sibling Cartesian-frames object was.
- **Ontology-stickiness risk:** High. Pre-2021 models have partitions and Pearl DAGs, not factorization-as-product with history-defined time. Because TSA already writes the name, LLM-drafted prose will map FFS onto ch07/MB1 and miss structural time. TSA includes the label, excludes the primitive.
- **Recommended action:** add-reverse-gap

## One-line finding

FFS is a new temporal/independence ontology that TSA already name-drops as a Cartesian-frames-style boundary tool, so the manuscript looks covered while still lacking structural time and orthogonality as objects.
