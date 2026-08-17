# Uncertainty Ledger

Open problems and unresolved uncertainties tracked across the manuscript.

**Last cross-check:** 2026-08-17 — U-17 added for bearer admission (ch18 §`sec:recognizing-new-bearers`; three-layer uncertainty). Prior cross-check 2026-06-29 — U-05 gloss extended for blanket well-definedness vs recovery hardness (ch06–07).

| # | Open question | Treated in | Bears on |
|---|----------------|-----------|----------|
| U-01 | Are human values sufficiently low-dimensional, and are their bundle representations recoverable enough to be learned and transported? | ch15–17 | A-001, C-004 |
| U-02 | Can bearer maps survive radical ontology shift? | ch18, ch47 | A-001, C-004, C-011 |
| U-03 | Can correction-channel integrity be measured under adversarial conditions without the reference process or the independence test itself being captured by the target system? | ch46, ch48, ch46, ch47 | A-002, C-005 |
| U-04 | Can successor constraints be enforced before recursive capability growth, and can import-preserving transport be verified rather than only syntactic continuity? Sharpened by the forgeability worry (ch08, ch31): a successor can pass every conserved-property check while defecting on the unmeasured remainder, formalized as a finite counterexample (`AlignmentProofSpine.Forgeability.forgeability_gap`) and named as bridge `MB10` (appendices/appG-lean-proof-spine.tex §appi:sec:forgeability). | ch08, ch31, ch46, ch48, ch48 | A-007, C-006 |
| U-05 | Is the agent--world cut well-defined and observer-independent enough to estimate, and can composite-agent boundaries then be recovered from finite, high-dimensional, adversarial deployment data without learned detectors inheriting the criterion/labeling gap? | ch06–07, ch09, ch45 | A-004, C-001, C-003 |
| U-06 | How much capability growth is safe without proportional transparency/correction growth? | ch12, ch14, ch46 | C-008 |
| U-07 | What counts as legitimate (vs. pathological) value-bundle change? | ch46, ch48, ch45–42 | C-005, C-011 |
| U-08 | Where does technical alignment end and civilizational self-governance begin? | ch45, ch47 | C-002, C-011 |
| U-09 | Is the compression test for intention robust against semantic camouflage and decomposition attacks? | ch46, ch48 | A-006, C-009 |
| U-10 | What are sufficient conditions for alignment-basin stability under competitive selection? | ch46, ch48 | C-007 |
| U-11 | Pivotal process: can the transition checklist (ch45 `sec:pivotal-process-ch48`) close in the available time budget? Slow path conditional; fast path = pivotal-act limit. | ch45, ch48 | C-007 |
| U-12 | Can effective AI coalitions / inferential coupling be detected and indexed adversarially, including audit-side \(P_{\text{meta}}\) certificates, self-modeling evidence, probe coverage, and calibrated open-edge thresholds for shared-history, non-message, self-similar, and full-acausal-trade cases? | ch48, ch47, ch48 | A-013, C-001, C-007 |
| U-13 | Can successors be certified without full construction understanding? | ch48 | A-007, C-006 |
| U-14 | Do safety-case templates scale to frontier systems under adversarial optimization? | ch46, ch47, appG | C-002, C-044 |
| U-15 | Can institutional designs reliably preserve correction-channel capacity over time? | ch46, ch46 | A-003, A-005, C-007 |
| U-16 | Can grounding viability be measured or certified under adversarial optimization, especially when value-relevant variables are not yet nameable in the current ontology? | ch03, ch16, ch46, ch46, ch46, ch47 | A-014, C-004a, C-004, C-005 |
| U-17 | **Bearer admission under unfamiliar substrates:** given candidate process $z$ and uncertain theories of consciousness, sentience, valence, or personhood, what observations suffice to include $z$ in, or conservatively exclude it from, a bundle-specific bearer class? Separately: (1) boundary — what is $z$? (ch07); (2) property/theory — what organization supports the target property? (3) normative — which property makes $\Phi_k$ high? Do not collapse into one scalar consciousness weight. Lean: `ConservativeExclusion` (one-sided shape); signal `BearerAdmissionMisclassified` — not part of `MB3Crux`. | ch07, ch18 (`sec:recognizing-new-bearers`), ch47 | MB3 (sub-obligation), C-004, C-004a, C-011 |

## Notes

- U-12, U-14, and U-16 now have manuscript homes, but remain open as adversarial/empirical questions. appG safety-case template is still pending.
- U-08 and U-11 are partly philosophical / governance questions and are acknowledged as limits (see C-011, status `limit`).
- U-17 is distinct from U-02 (bearer-map *transport* across ontology shift): admission/inference for unfamiliar computational processes is the upstream step before transport and persistence (ch47).

See also `metadata/open-problems.md` (research-direction framing) and `metadata/claims-ledger.md` / `metadata/assumptions-ledger.md` for the claims and assumptions each uncertainty threatens.
