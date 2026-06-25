# 2026-06-26 — Ch36 randomization floor proof

## Trigger

User asked to include the suggested improvement for feedback item (b) in both text and proofs: strengthen hidden randomization into an information-theoretic post-commitment probe floor without assuming a \(K_{\text{evasion}}\) ceiling.

## Done

- Updated `chapters/ch36-passive-observation-not-enough.tex` to state the stronger conditional floor: post-commitment freshness, leakage budget \(\epsilon\), and probe-family coverage \(q\) imply detection at least \(q-\epsilon\).
- Updated `chapters/ch39b-verifiability-and-ontology-adequacy.tex` so "unpredictable probes" means the stricter post-commitment standard, not merely evaluator secrecy.
- Added `PostCommitmentProbeCertificate` and theorem `P36R_post_commitment_randomization_floor` to `formal/AlignmentProofSpine/Adversarial.lean`, plus a positive-detection corollary when coverage exceeds leakage.
- Updated `formal/README.md` module map to include `P36R`.
- Updated `appendices/appI-lean-proof-spine.tex` with theorem `P36R` and a proof explanation.

## Decisions

- Lean proves only the arithmetic consequence \(q-\epsilon\le d\) from an explicit certificate; it does not prove that a real audit has fresh entropy, bounded leakage, or adequate coverage.
- The manuscript preserves the regress limit: hidden randomization is a conditional floor, not a capability-independent safety proof.
- Did not update graph source or regenerate proof-spine figures in this pass; the appendix theorem list and formal README now name the new node.

## Open / next

- `make check` still fails before chapter checks on the existing structure issue: `Expected 10 appendix files, found 9`.
- Consider updating `context/lean_proof_dependency_graph.dot` and regenerated proof-spine figures if the visual graphs must include `P36R`.

## Verification

```bash
cd formal && lake build  # success
make check               # fails: Expected 10 appendix files, found 9
```

## Key paths

- `chapters/ch36-passive-observation-not-enough.tex`
- `chapters/ch39b-verifiability-and-ontology-adequacy.tex`
- `formal/AlignmentProofSpine/Adversarial.lean`
- `appendices/appI-lean-proof-spine.tex`
- `formal/README.md`

## Commits

- None.
