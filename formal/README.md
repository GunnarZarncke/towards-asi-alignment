# `formal/` — Lean proof spine

A compact, **self-contained Lean 4 formalization** of the *logical skeleton* of
the alignment argument in *Towards Superintelligence Alignment*. It implements
the spec in [`../LeanProofSpineImplementationBrief.md`](../LeanProofSpineImplementationBrief.md)
(conjectured dependency structure in
[`../context/lean_proof_dependency_graph.dot`](../context/lean_proof_dependency_graph.dot);
 book figures in [`../context/lean_proof_graphs/`](../context/lean_proof_graphs/)).

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
derives `Risk A ≤ δ` from `Control A ≤ CCI A + δ` via `P13` (no bare `hrisk` hypothesis).
The bridge path now lists `MB6` plus split adversarial-UAD bridges `MB7a`–`MB7c`.

**Notation.** `ValueUpdateOperator` (`U_H`), `SystemUpdateOperator` (`U_S`),
`CCI` (sole exported correction measurand), handle-controlled `CorrectionPath`,
`SuccessorSafeWitness`.

Manuscript cross-refs: `\leanspine{kind}{node}{gloss}` in `metadata/preamble.tex`.

## Module map

| Module | Proof-spine nodes | Book chapters |
|--------|-------------------|---------------|
| `AlignmentProofSpine/Core.lean` | abstract carriers, access/handle/K-equivalence vocabulary, concrete `Boundary`, MDL/graph scaffolding, **`finPigeonhole`** (from-scratch finite pigeonhole), bridges `MB1`–`MB8` with split `MB7a`–`MB7c`, `BridgeAssumptions` | foundations |
| `AlignmentProofSpine/Boundaries.lean` | `P05`–`P09`, `P36`, access-equivalence and K-equivalence non-identifiability, smoothing-margin arithmetic | 6–7, 10, 36 |
| `AlignmentProofSpine/Capability.lean` | `P10`–`P13`, `P32`, `P43`, hidden-BIQ certificate, slow-plotting accumulation (B-IQ / control–correction arithmetic) | 11–14, 33, 36 |
| `AlignmentProofSpine/Bundles.lean` | `P14`, `P19`–`P22a` (proofs), `P15`/`P17`/`P18`/`P22b` (counterexamples) | 15–23 |
| `AlignmentProofSpine/Correction.lean` | `P23`, `P24`, `P25`, `P26`, **`CCI`**, handle-controlled **`CorrectionPath`** | 24–27 |
| `AlignmentProofSpine/Successors.lean` | `P27`, `P28`, `P29`, **`SuccessorSafeChain`**, risk bound propagation | 28–31 |
| `AlignmentProofSpine/Adversarial.lean` | `P31`, `P33`, `P34`, `P36R`, `P37` | 32–37 |
| `AlignmentProofSpine/Philosophy.lean` | `P41`, `P42`, `P44`, `P45` | 41–44 |
| `AlignmentProofSpine/Certification.lean` | `P01`, `P02`, `P30`, `P35`, `P40`, **`certified_class_safety_spine_derived`** (risk from capacity slack) | 1–5, 35, 39, 44 |
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
* **`Risk`** is `Control − CCI` (`RiskGap`). Certification uses `Control ≤ CCI + δ`.
  Handle-controlled path: `CorrectionPath` / `SystemCorrectionPath` over `CorrectionChainLink`,
  now grounded in a correcting agent's controlled handles. The weakest effective
  handle-capacity term lives inside `CCI` only (book: $C_{\mathrm{raw}}$; not exported in Lean).
* **`DeploymentMass`** is environment-relative deployment/control mass (book ch32,
  `eq:deployment-mass-ch32`). Selection uses `SelectionChannel` / `SelectionHandleFor`
  over the same `Handle` type as correction. Revenue and regulatory risk are not
  primitive Lean terms.
* **`SuccessorSafe`** = `Nonempty SuccessorSafeWitness` with `CCIPreserved` and
  `SystemUpdateOperatorPreserved` among the ch29 fields.
* Node IDs match `formal/AlignmentProofSpine/*.lean` theorem names (see module map above).
  Full graph: `context/lean_proof_dependency_graph.dot`.
  Book layout: four sub-spines + overview in `context/lean_proof_graphs/` → `figures/lean_proof/` via `scripts/render_lean_graphs.sh` (Appendix I, Section~\ref{sec:appi-proof-dependency}).
