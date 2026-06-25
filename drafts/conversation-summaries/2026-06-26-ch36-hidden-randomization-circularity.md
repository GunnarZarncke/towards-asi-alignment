# 2026-06-26 — Ch36 hidden-randomization circularity

## Trigger

User asked to address feedback item (a) directly in Chapter 36: the hidden-randomization subsection appeared to assume away the \(K_{\text{evasion}}\) regress it had just named.

## Done

- Updated `chapters/ch36-passive-observation-not-enough.tex` in Section `Hidden Randomization`.
- Added explicit caveat that hidden randomization is not a free escape from the adequacy condition \(A+Q>K_{\text{evasion}}\).
- Added the narrower non-circular form: pre-randomization commitment \(C\), fresh entropy relative to the system's pre-commitment view \(V^{-}\), and a min-entropy condition \(H_\infty(R \mid V^{-},C)\ge h\).
- Added the required probe-family coverage condition \(\Pr_R[D_R(C)=1]\ge q\) for unsafe commitments.

## Decisions

- Claim strength is conditional, not proof-like: hidden randomization can raise faking cost only if freshness, nonadaptivity, and coverage are established.
- No Lean changes were made. The existing proof spine already treats adversarial measurement through bridge assumptions rather than a proved capability-independent floor.

## Open / next

- `make check` was attempted but stopped on an existing structure issue: `scripts/check_structure.py` expected 10 appendix files and found 9. The check did not reach the Chapter 36 text.
- If strengthening item (b) is pursued, likely homes are Chapter 36 plus the verifiability chapter, with possible Appendix I / Lean-spine bridge-note updates.

## Key paths

- `chapters/ch36-passive-observation-not-enough.tex`
- `chapters/ch39b-verifiability-and-ontology-adequacy.tex`
- `formal/AlignmentProofSpine/Adversarial.lean`
- `formal/AlignmentProofSpine/Core.lean`

## Commits

- None.
