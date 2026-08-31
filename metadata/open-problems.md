# Open Problems

Research directions and unresolved questions for the book project.

## Measurement

- **The Certification-Under-Manipulation Problem** (flagship, ELK-style): for a load-bearing certification measurand $M$ and adversary capability $\kappa$, does a threshold $\kappa^{*}$ exist below which $M$ is adversarially verifiable (cost of faking grows faster than affordable surplus) and above which it provably is not? Named and stated formally in Chapter~43 (`ch:verifiability-ontology`, \S`sec:certification-under-manipulation-ch43`); restates A-009 / MB7b–d (`metadata/assumptions-ledger.md`, `appendices/appB-bridge-crosswalk.tex`) as one citable target rather than a per-chapter WWCTV caveat. Unresolved for every concrete measurand in the book (boundary residual, CCI, conserved-property score, GLI).
- Operational detection of composite agent boundaries in deployment systems
- **TODO — foundation-model agent discovery:** [TimesFM-3](https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/) (Google Research, Aug 2026) pre-trains on multivariate time series with alternating causal temporal attention and full cross-variate attention, plus zero-shot horizon fill from masked patches. May be relevant as a backbone for a general **agent discovery model** (infer boundary/coupling structure from raw deployment telemetry without per-task fitting). Not yet mapped to UAD benchmarks, intervention handles, or MB1 soundness criteria.
- Grounding-viability tests: whether value-relevant world changes move checked abstractions, correction signals, or uncertainty states under optimization pressure
- Adversarial-robust correction-channel integrity metrics
- Goal laundering detection under strategic opacity

## Theory

- Sufficient conditions for alignment basin stability
- Pivotal process: conditions for $\mathbb{B}_{\mathrm{race}} \to \mathbb{B}_{\mathrm{certified}}$ without unilateral decisive action — **ch38** (`eq:race-certified-basins-ch37`) currently uses loose set descriptions only; `% TODO[formalize]` there calls for percolation ($\tilde{\kappa}$), selection envelope ($\mu_E$), and basin-stability predicates (track: `metadata/TODO.md` Formalization tracks, notation C12)
- Inferential coupling indices and detection of effective AI coalitions
- Conservative abstraction criteria for value-bundle and correction maps
- Bearer-map transport across radical ontology shift
- **Bearer admission under unfamiliar substrates** (ch18 §`sec:recognizing-new-bearers`, MB3 sub-obligation): given candidate bounded process $z$ (from boundary discovery) and uncertain competing theories of consciousness, sentience, valence, or personhood, what observations suffice to include a process in, or conservatively exclude it from, a bundle-specific bearer class? Decompose rather than collapse into one ``consciousness probability'':
  - **Boundary:** what is $z$? (MB1 / ch07)
  - **Property/theory:** what internal organization supports the morally relevant property? (candidate $T$'s as evidence providers, not framework axioms)
  - **Normative relevance:** which property makes $\Phi_k(z)$ high for bundle $k$?
- Legitimate vs. pathological value-bundle change

## Practice

- Safety-case templates that scale to frontier systems
- Successor certification without full construction understanding
- Institutional designs that preserve correction-channel capacity
- **Inert writes and iterated copies as successor events:** operational closure over \(C=0\) stores (checkpoints, firmware, constructor files) and over export/load; measurement, not renaming
- **Envelope recertification:** \(\mathcal{E}\) (channels, inventory, human lab access) and \(\mathcal{T}\) (writes, tools, fine-tunes) as named hypotheses; connecting a previously isolated process to the internet is a new envelope
- **Residuals that need extra work:** constructors exported outside the envelope; nested constructors that emit new types; unlisted guards; physical/capability drift below eval grain (distinct from ch46 value-geometry drift); published science as a pre-existing constructor field; \(\tau_h < \tau_c\) after a physical threshold; certificates on weights while operators and tools are the optimizer

See also `metadata/uncertainty-ledger.md`.
