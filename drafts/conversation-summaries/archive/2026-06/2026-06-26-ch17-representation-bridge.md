# 2026-06-26 — Ch17 representation bridge

## Trigger

User provided critical feedback that Chapter 17's sample-complexity math priced the easy readout problem after the low-dimensional bottleneck was supplied, while the prose claimed support for the harder representation-learning problem. User asked to make the chapter more honest, organize around the core fix, and update references.

## Reviewer feedback addressed

- The reviewer identified a load-bearing gap: Eq.~17.1 was an apprenticeship-learning / IRL bound for fitting a readout over already-known features, but Chapter 17 used it as if it also supported discovery of the low-dimensional value-bundle representation.
- The reviewer also noted that demonstration-distribution fit does not answer the chapter's own target: counterfactual transfer under punishment removal, truth/loyalty conflict, corrupt institutions, unfamiliar bearers, and other off-distribution moral cases.
- A third concern was equivocation between compact evolved motivational seeds and the rank of mature culturally elaborated values.
- The revision addresses these by splitting \(m_{\mathrm{readout}}\) from \(m_{\mathrm{repr}}\), making \(g_\psi\) discovery the explicit bridge, requiring cross-context/cross-cultural/counterfactual invariance, and downgrading the evolutionary argument to a prior rather than proof.

## Done

- Renamed Chapter 17 from "Why Low Dimensionality Makes Value Learning Possible" to "When Low Dimensionality Helps Value Learning" in `chapters/ch17-low-dimensional-value-learning.tex`, `metadata/book.yml`, and generated `tables/chapter-map.tex`.
- Rewrote the chapter thesis and opening to distinguish readout from representation discovery.
- Retitled the sample-complexity section as "The Readout Bound" and changed Eq.~17.1 to \(m_{\mathrm{readout}}\), explicitly stating that it prices \(h_\theta\) given known bundle coordinates, not discovery of \(g_\psi\).
- Added a new "The Representation Bridge" section: cross-environment / cross-cultural partial translation \(B^{(e_2)} = T_{12}(B^{(e_1)})+\eta\), proxy-breaking counterfactuals, and active/adversarial measurement as the bridge from low-dimensional readout to transfer.
- Tightened later sections so the old stronger claim does not reappear: evolution now supplies a prior over compact seeds, not proof of mature low rank; empirical signatures include representation/readout separation; failure modes include representation shortcuts; WWCTV and summary now state the recoverable-representation caveat.
- Updated Chapter 17 references to include maximum-entropy IRL, causal representation learning, affective systems, and adversarial limits on learned alignment signals.
- Updated `metadata/claims-ledger.md`, `metadata/assumptions-ledger.md`, and `metadata/uncertainty-ledger.md` so C-004/A-001/U-01 carry the new representation-recovery bridge.

## Decisions

- Treated low-dimensionality as a conditional empirical bridge, not a proof-like result.
- Used human universals and cultural convergence only as evidence to test via invariance and partial translation maps, not as an independent solution.
- Did not modify Lean: the formal spine already treats bundle alignment and transport as bridge/counterexample territory (`MB2`, `MB3`, `P15`, `P17`, `P18`, `P22b`), and this edit calibrates prose to that status.

## Open / next

- `make check` still fails on the existing structure issue: `Expected 10 appendix files, found 9`.
- Consider a consistency pass on Chapter 20's "Why Bundle Inference Helps with Sample Complexity" section, which still contains a related sample-complexity paragraph and should probably reference the Chapter 17 readout/representation split.

## Verification

```bash
./build.sh   # success
make check   # fails: Expected 10 appendix files, found 9
```

`ReadLints` reported no diagnostics for the edited files.

## Key paths

- `chapters/ch17-low-dimensional-value-learning.tex`
- `metadata/book.yml`
- `tables/chapter-map.tex`
- `metadata/claims-ledger.md`
- `metadata/assumptions-ledger.md`
- `metadata/uncertainty-ledger.md`

## Commits

- `8a6c0c9` Clarify Chapter 17 representation bridge.
