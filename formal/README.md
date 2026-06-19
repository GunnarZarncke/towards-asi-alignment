# `formal/` — Lean proof spine

A compact, **self-contained Lean 4 formalization** of the *logical skeleton* of
the alignment argument in *Towards Superintelligence Alignment*. It implements
the spec in [`../LeanProofSpineImplementationBrief.md`](../LeanProofSpineImplementationBrief.md)
(conjectured dependency structure in
[`../context/lean_proof_dependency_graph.dot`](../context/lean_proof_dependency_graph.dot)).

## What this is and is not

The goal is **not** to formalize the empirical content of UAD, value bundles,
B-IQ, attractor basins, or CEV. It formalizes the chain

```
boundary discovery → capability/control/correction quantities
  → value-bundle and bearer-map transport → correction-channel integrity
  → successor stability → adversarial measurement → certified-class safety
```

and makes one distinction explicit and machine-checked:

* **Proved in Lean** — *if* these predicates and inequalities hold, *then* the
  certification conclusion follows.
* **Assumed bridge** (`axiom`) — real systems satisfy these predicates under
  these measurement procedures. These are the eight `MB1`–`MB8` bridges plus the
  model-selection convention `S07`. They are **never hidden** inside definitions.

**Toy vs. target strength.** The current spine is deliberately compact. Many
counterexamples are finite `Bool` separations (one predicate defined as `True`,
another as equality); several “theorems” are definitional; abstract quantities
use integer proxies. The strengthening roadmap lives in `metadata/TODO.md`
(§ Lean proof spine — **chapter ↔ Lean mapping gaps**). Bridges `MB1`–`MB8` are
**out of scope** for Lean completion (empirical / philosophical imports); in-scope
work is aligning **drafted chapter formalism** to spine structure.

Priority: derive certification conclusions from spine inputs (capacity slack,
correction channel, successor invariance) rather than assuming them as bare
hypotheses.

> The book must not say "Lean proves ASI alignment." It may say "Lean proves
> that, *if* these boundary, bundle, correction, successor, and adversarial
> conditions hold, *then* the certification argument has the advertised logical
> shape. The hard work is showing real systems satisfy the bridge conditions."

## Build

Requires the Lean toolchain via [`elan`](https://github.com/leanprover/elan)
(pinned in `lean-toolchain` to `leanprover/lean4:v4.28.0`). **No Mathlib** — the
spine depends only on the Lean core library, so it builds in seconds and offline.

```bash
cd formal
lake build
```

Inspect what a theorem ultimately rests on (proofs vs. bridges):

```bash
cd formal
echo 'import AlignmentProofSpine
open AlignmentProofSpine
#print axioms certified_class_safety_from_bridges' > /tmp/chk.lean
LEAN_PATH=.lake/build/lib/lean lean --root=. /tmp/chk.lean
```

`P34` (host-capacity aliasing) and the other non-bridge results print only
`propext` / `Quot.sound` (or abstract carriers). `certified_class_safety_spine_derived`
derives `Risk A ≤ δ` from `Control A ≤ CorrectionCapacity A + δ` via `P13` (no
bare `hrisk` hypothesis). `certified_class_safety_from_spine_and_bridges` additionally
lists `MB6`/`MB7`.

## Module map

| Module | Proof-spine nodes | Book chapters |
|--------|-------------------|---------------|
| `AlignmentProofSpine/Core.lean` | abstract carriers, concrete `Boundary`, MDL/graph scaffolding, **`finPigeonhole`** (from-scratch finite pigeonhole), bridges `MB1`–`MB8`, `BridgeAssumptions` | foundations |
| `AlignmentProofSpine/Boundaries.lean` | `P05`–`P09`, `P36` | 6–7, 10, 36 |
| `AlignmentProofSpine/Capability.lean` | `P10`–`P13`, `P32`, `P43` (B-IQ / control–correction arithmetic) | 11–14, 33 |
| `AlignmentProofSpine/Bundles.lean` | `P14`, `P19`–`P22a` (proofs), `P15`/`P17`/`P18`/`P22b` (counterexamples) | 15–23 |
| `AlignmentProofSpine/Correction.lean` | `P23`, `P24`, `P25`, `P26` | 24–27 |
| `AlignmentProofSpine/Successors.lean` | `P27`, `P28`, `P29`, **`SuccessorSafeChain`**, risk bound propagation | 28–31 |
| `AlignmentProofSpine/Adversarial.lean` | `P31`, `P33`, `P34`, `P37` | 32–37 |
| `AlignmentProofSpine/Philosophy.lean` | `P41`, `P42`, `P44`, `P45` | 41–44 |
| `AlignmentProofSpine/Certification.lean` | `P01`, `P02`, `P30`, `P35`, `P39`, `P40`, **`certified_class_safety_spine_derived`** (risk from capacity slack) | 1–5, 35, 39, 44 |
| `AlignmentProofSpine.lean` | root module re-exporting all of the above | — |

## Three kinds of result (for the book)

* **proof** — a direct logical/arithmetic theorem (e.g. `P01`, `P10`, `P14`,
  `P27`, `P34`).
* **counterexample** — a compact finite toy model showing one notion does not
  imply another (e.g. `P15`, `P17`, `P18`, `P22b`, `P25`, `P26`, `P31`, `P37`,
  `P41`, `P42`, `P44`).
* **bridge** — an empirical or philosophical condition supplied by measurement,
  governance, or future theory (`MB1`–`MB8`, declared as `axiom`).

## Notes on deviations from the brief's scaffold

* The Lean 3 `constant` keyword (used in the brief's sketch) was removed in
  Lean 4; abstract carriers are declared with `axiom`, concrete structure with
  `structure`/`def`.
* No `sorry`/`admit` remain. Every `admit` placeholder in the brief's scaffold is
  either proved or, where it depended on empirical content, deliberately routed
  through an explicit `MB*` bridge.
* Counterexamples (brief §8) use finite `Bool`/`Fin` toy models rather than
  abstract `System`, as the brief requires ("do not leave these as abstract
  counterexamples forever").
* `P44` uses the brief's §6 amendment (two disagreeing legitimacy orderings), not
  the inconsistent single-predicate form.
* The host-capacity aliasing theorem `P34` is proved against a from-scratch
  pigeonhole (`finPigeonhole`) instead of Mathlib's `Fintype.card_le_of_injective`,
  keeping the project Mathlib-free.
* **`Risk` is defined** as `Control − CorrectionCapacity` (`RiskGap`). The primary
  certification theorems derive `Risk A ≤ δ` from capacity slack
  (`P13_risk_gap_bounded_by_capacity_slack`); legacy theorems that take `hrisk`
  explicitly remain for interface compatibility.
* **`CorrectionCapacity`** is **`ChainCapacity`** of per-system link capacities
  (`CorrectionLinkCapacities A`), i.e. weakest-link graph capacity (Ch. 24–25).
  `P24_correction_capacity_le_each_link` ties it to every edge; bridges supply
  the measured list and integrity→channel topology.
* **BIQ → control ceiling:** per-system profile (`IpredSys`, `IctrlSys`, `CactSys`, …)
  with `Control A ≤ IctrlSys A ≤ CactSys A` (`Control_le_IctrlSys`, `P10`). If
  correction covers the actuator ceiling plus slack (`BIQDerivedCapacitySlack`),
  `risk_bound_from_biq_ceiling` / `certified_class_safety_from_biq_ceiling` derive
  the risk bound without a separate control hypothesis.
* **Successor-safe chains** (`SuccessorSafeChain`) propagate risk bounds: if
  `RiskGap A ≤ δ` and each step is `SuccessorSafe` with non-increasing control
  and non-decreasing correction capacity (`SuccessorSafe_risk_monotone`, target of
  `MB5`), then `RiskGap B ≤ δ` for every `B` on the chain
  (`risk_bound_along_successor_safe_chain`).
* Numbering follows the **brief** (§4/§5), which is the implementation target; the
  `.dot` graph uses a different, conjectural numbering.
