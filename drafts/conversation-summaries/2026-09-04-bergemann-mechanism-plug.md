# 2026-09-04 — Bergemann–Koh–Morris as field implementation

## Trigger
Read arXiv:2609.01595 and map it to TSA. User then asked to plug the paper in as a *specific implementation* of ch10/ch11/ch14 requirements (not as an alternative frame), keep listed incentive results, and note it for Construct.

## Done
- **ch10:** verification order (one-sided imitation) and honesty-and-obedience / double deviation as the field incentive form; epistemic-status sentence; summary bullet; chapter refs.
- **ch11:** RSP/eval→permission map as the mechanism; IC iff monotone caps (sandbagging otherwise); pointer from adversarial suppression; summary bullet; chapter refs.
- **ch14:** capability–misalignment covariance (elicitation works vs futile common cap) after the green-eval/dormancy paragraph; summary bullet; chapter refs.
- **ch35:** peer scoring as a possibility result; unbounded free rewards as why it is a benchmark, not a protocol. Not treated as implementing inferential coupling.
- **ch41:** left alone (cousin).
- Bib: `bergemann2026mechanism` in `external-alignment.bib` + `\bibsummary`.
- Construct note: keep-row in `construct.md`; mechanism-design table row in `construct-external-lit.md`.

## Decisions
- Where the field has a strong candidate, use it as the implementation rather than listing alternatives. This paper implements the *incentive* constraints of concealment, capability certificates, and eval screening. It does not replace the book's object (dynamical correction / bundles).
- **RSP-as-mechanism home is ch11 § capability thresholds** (a measure is useful when it changes decisions). ch10 owns the verification-order / double-deviation constraint; ch14 owns the covariance that tells when the same map can screen misalignment.
- ch35 is not an implementation chapter for this paper. The multi-agent results are a Crémer–McLean-style existence proof. Cite them as such.
- Do not import their names “interpretability” (= Var(bias)) or “alignment” (= E[bias]).

## Follow-up (same session)
- Rewrote the four insertions in chapter vocabulary: dropped “type”; ch10 summary simplified; ch11 tied to score→permission / playing dead; ch14 names capability–misalignment joint movement; ch35 tied to inferential coupling, \(\kappa^V_{ij}\), \(\varphi_C\), and coalition.

## Open / next
- Optional: `npm run sync:chapters` if live book pages should pick up the paragraphs.
- XI draft can use the paper as announced-map construction on contractible certificates; still not construction of \(D\).

## Key paths
- `chapters/ch10-strategic-opacity.tex`
- `chapters/ch11-capability-without-task-ontology.tex`
- `chapters/ch14-intelligence-deepens-misalignment.tex`
- `chapters/ch35-multi-agent-strategic-coupling.tex`
- `drafts/plans/construct.md`
- `drafts/plans/construct-external-lit.md`

## Commits
- (this session) Plug Bergemann–Koh–Morris as field incentive implementation in ch10/11/14/35.
