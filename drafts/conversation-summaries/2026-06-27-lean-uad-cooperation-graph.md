# 2026-06-27 — Lean UAD cooperation graph

## Trigger
Review whether Lean connects percolation to UAD; implement cooperation-graph derivation from UAD-discovered agents; extend with acausal modeling per the acausal-trade UAD paper.

## Done
- Added/extended `formal/AlignmentProofSpine/CooperationGraph.lean`:
  - UAD audit → causal graph (`DerivedCoopGraph`) via P32 κ threshold;
  - acausal layer: `AcausalAgentProfile` (`D_i`), `AcausalPairProps` (`ε_ij`), `inferentialCouplingScore` (paper eq. 8), `DerivedAcausalGraph` (IC > τ_ac);
  - `\tilde{κ}` assembly: `auditMutualModelWithAcausal` with proved `(1-p)·IC` boost;
  - key theorems: `uad_audit_yields_acausal_graph`, `severed_causal_reach_positive_effective_reach`, `acausal_open_on_severed_edge_yields_reach`, `P33` (coop + acausal graphs);
- Strengthened acausal Lean model: added `UnitScore`, `MetaPriorEvidence`, derived `metaPriorMismatch = 1 - P_meta(π_i = π_j)`, and `AcausalDetectionCertificate` for shared-meta-prior, self-readout, and probe-coverage assumptions.
- Updated `formal/README.md`, `metadata/TODO.md`, ch33 `\leanspine{P33}` and new `\leanspine{acausal-ici}`.
- Expanded ch33's `P_{\text{meta}}` treatment from a light mention into a full acausal-UAD subsection: UAD-derived `(f_i,g_i)`, permutation-invariant meta-prior, diagonal mass / `\epsilon_{ij}`, introspective posterior `\beta_i^{\mathrm{int}}`, acausal equilibrium equation, detector factors, attack-surface assumptions, and a mapping table.
- Reframed `P_{\text{meta}}` as an audit-side/expositional certificate rather than a claim of literal symbolic agent self-modeling; noted that acausal cooperation may be implemented implicitly in weights, scaffolds, or behavior, and that UAD detects it at a chosen resolution.
- Added TODO for calibrating \(\tau_{\mathrm{ac}}\) / acausal open-edge thresholds in ch39b/ch40 rather than treating the illustrative 0.9 threshold as universal.
- Updated ch33 WWCTV after the P_meta/acausal work: acausal cooperation is degree-valued; benign high coupling is handled by composite-agent audit rather than special exemption; detector evasion points forward to ch39b/ch40; calibration is framed defensively.
- Added ch33 subsection `Acausal Coalitions as Composite Agents`: detected causal/acausal cooperation changes the unit of audit, collapsing the component into a candidate composite \(C_S\) and rerunning boundary, capability, opacity, correction, value, and successor tests.
- Refined ch33 WWCTV for the acausal/coalition critique: added reliable negative evidence as a later adversarial-setup requirement, strengthened composite correction through handle-controlled correction, referenced first-coalition seed effects to ch12 boundary expansion, and added a strong probe-local TODO for one-shot/short-episode inferential coupling.
- Retitled ch33 to `Multi-Agent Superintelligence and Inferential Coupling`; made inferential coupling the umbrella term and added the taxonomy distinguishing shared-history/common-cause coupling, non-message inferential coupling, self-similarity/self-model coupling, and full decision-theoretic acausal trade.
- Made ch33/acausal assumptions bridge-visible: `UADDiscoveredAgent` now carries an `EpsilonBoundary` certificate consumed through MB1; Core now splits MB6 into MB6a (percolation evidence → basin stability) and MB6b (basin stability → correction integrity); Core adds MB7d (acausal-UAD detector validity); Certification consumes `PercolationEvidenceSys`; Appendix I/H, ch39/ch39b, ledgers, and generated assumptions index were updated.
- Updated Lean proof dependency DOT sources and rendered graph PNGs: full dependency graph plus Appendix I overview, boundary/measurement, and selection/limits diagrams now show MB6a/MB6b, MB7d, and the UAD/acausal graph certificate path.
- `lake build` succeeds.
- `make check` succeeds after the ch33 prose expansion.

## Decisions
- **Three opaque axioms:** `causalMutualModelOf`, `acausalProfileOf`, `acausalPairOf`; `acausalPairOf` now emits a `P_meta` evidence certificate rather than `ε_ij` directly. Mismatch, IC score, and inferential boost are derived.
- Integer scale 100 for unit-interval proxies; `defaultAcausalThreshold = 90` (τ_ac ≈ 0.9).
- Acausal equilibrium (paper eq. 6) not formalized; detection + percolation composition only.
- Giant-component / MB6a remains external; MB6b bridges basin stability to correction integrity.
- Manuscript claim strength: `P_{\text{meta}}` definition and detector structure are source-derived definitions; equilibrium and large-scale percolation dynamics remain conjectural/open.
- `P_{\text{meta}}` is now treated as an opaque audit certificate in Lean/prose; the detector's key claim is behavioral detectability of acausal cooperation, not symbolic introspection by the agents.
- Coupling is not intrinsically bad; the bad case is a composite whose correction channels lag capability/control or whose boundary/opacity prevents audit.
- Bridge mapping: A-013 covers acausal detector certificates and maps to MB7d; S09-style percolation theory enters via MB6a, not the unsplit MB6.
- Appendix graph decision: MB7d is shown as access-robust input from Spine I plus acausal detector validity in Spine IV; MB6a/MB6b separates graph/percolation evidence from the basin-to-correction claim.
- Acausal threshold calibration TODO now suggests prediction markets / Logical-Induction-style forecasting for future causally severed coordination, probe failures, and detector-evasion events.
- Terminology decision: book-facing prose should say inferential coupling for the broad mechanism; full acausal trade is a limiting decision-theoretic case. Lean/source identifiers may still say `acausal` where they refer to the source formalism.
- Renamed Lean referents to match: `InferentialAgentProfile`, `InferentialPairProps`, `inferentialProfileOf`, `inferentialPairOf`, `InferentialDetectionCertificate`, `DerivedInferentialGraph`, `auditMutualModelWithInferential`, `InferentialDetectorAdequate`, `InferentialCouplingMeasurementValid`, `MB7d_inferential_uad_detector_soundness`; manuscript `\leanspine{inferential-ici}`.
- WWCTV scope decision: do not add separate objections for nonseparation, opaque non-agentic paths, or resolution/time-scale regress in ch33 now; UAD discovery, handles, and later adversarial-verifiability chapters own those issues.

## Open / next
- Optional: wire `MB6a` to a percolation-above-threshold predicate on `DerivedCoopGraph` (needs `S09`-style external axiom).
- Optional: finite toy instances of the three opaque estimators for Appendix I.
- Resolve `TODO[probe-local-inferential]`: can one-shot or short-episode inferential coupling evade graph-level coalition detection, and what adversarial setup would reveal it?
- Canary TeX comments from prior session may still be uncommitted.

## Key paths
- `formal/AlignmentProofSpine/CooperationGraph.lean`
- `chapters/ch33-multi-agent-strategic-coupling.tex` (UAD grounding prose + P33 gloss)
- `context/lean_proof_dependency_graph.dot`, `context/lean_proof_graphs/*.dot`, `figures/lean_proof/*.png`
- `context/extracts/attractor-basins.md`, `context/extracts/acausal-trade-uad-formalization.md`

## Commits
- (none this session)
