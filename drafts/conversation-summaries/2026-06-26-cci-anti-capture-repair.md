# 2026-06-26 — CCI anti-capture repair

## Trigger

User provided reviewer feedback that CCI could read high at the catastrophic fixed point: a superintelligent system captures human interpretation, endorsement, and world-improvement criteria, so manipulation and ontology mismatch terms collapse even though correction has been domesticated. User asked to implement improvements.

## Reviewer feedback addressed

- CCI had no independent anchor: \(M\), ontology mismatch, coercion/dependency, endorsement, and human interpretation all referenced signals the threat model says a capable system can capture.
- Directional transparency overstated separability between assistance-models and manipulation-models; a model that helps a person can also predict how to move them.
- No-Bypass risked regress: "prior valid correction process" needed a base case or it would assume the validity it tries to protect.
- Scalar CCI with hand-set \(\lambda\)-weights invited false precision and could hide a failed dimension behind a positive sum.

## Done

- Updated `chapters/ch25-correction-channel-integrity.tex` so CCI is a conditional anti-capture certificate, not an Archimedean source of legitimacy.
- Added `ValidRef(A,G_t,\mathcal H_t)`: CCI is evaluated only when the correcting agent/institution is an independently identified control process with handles not captured by the target system.
- Added explicit captured/invalid status: if the reference process is captured, CCI is invalid rather than high.
- Added a footnote that scalar CCI is an expository projection; the certification form should be a vector certificate with per-coordinate thresholds and invalidation rules. Noted the same caveat for scalarized BIQ when used for certification.
- Tightened manipulation and ontology-mismatch terms: agreement with captured `W^{relevant}` or a captured human interpretation map is not safety evidence.
- Revised directional transparency: it is an access/governance mitigation, not a clean information-theoretic separation between help and manipulation.
- Added vector-quality framing for the \(Q(U)\) update-quality guardrail.
- Updated stop/continue criteria to require `ValidRef` and vector CCI thresholds.
- Updated `chapters/ch27-manipulation-false-consent.tex` so No-Bypass uses a fallible local seed: less-captured correction sources such as protected persons, independent auditors, courts, rival institutions, holdout groups, adversarial reviewers, and pre-system records.
- Clarified No-Bypass is a normative rule and audit target, not a detector; verification requires external handles and cannot be established by later endorsement.
- Added convergence caveat: convergence helps only under protected independent conditions, not after system-mediated dependency or narrowed alternatives.
- Updated `metadata/claims-ledger.md`, `metadata/assumptions-ledger.md`, and `metadata/uncertainty-ledger.md` so C-005/A-002/U-03 carry the anti-capture validity condition.

## Decisions

- Did not modify Lean: `formal/AlignmentProofSpine/Correction.lean` already includes `CorrectionPath.notCaptured`; the manuscript now points at that condition.
- Treated CCI as undefined/invalid under captured reference processes rather than merely lower-scored.
- Grounded "human judgment" in discovered correcting agents and institutions with controlled handles, not raw approval or endorsement.

## Open / next

- `make check` still fails on the existing structure issue: `Expected 10 appendix files, found 9`.
- Consider a later consistency pass for BIQ / capability scalarization if vector-bounds need to be stated beyond the CCI footnote.
- If this repair becomes load-bearing in the safety case, consider adding a named `ValidRef` / anti-capture certificate to Appendix G and Appendix I prose.

## Verification

```bash
./build.sh   # success
make check   # fails: Expected 10 appendix files, found 9
```

`ReadLints` reported no diagnostics for the edited files.

## Key paths

- `chapters/ch25-correction-channel-integrity.tex`
- `chapters/ch27-manipulation-false-consent.tex`
- `metadata/claims-ledger.md`
- `metadata/assumptions-ledger.md`
- `metadata/uncertainty-ledger.md`
- `formal/AlignmentProofSpine/Correction.lean`

## Commits

- `c3d1ff3` Add CCI anti-capture validity condition.
