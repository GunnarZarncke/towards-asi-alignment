# 2026-06-19 — Lean proof spine implementation

## Trigger
Implement the Lean proof spine described in `LeanProofSpineImplementationBrief.md`:
compact Lean proofs for the logical skeleton, with empirical/philosophical bridge
claims kept explicit as axioms (`MB1`–`MB8`). Prioritize the non-bridge proofs
(invariant/basin, successor chain, B-IQ bounds, correction-channel lemmas, finite
counterexamples, host-capacity aliasing), then expose `MB1`–`MB8` in the top-level
certification theorem. Create suitable folders and update folder docs.

## Done
- Created `formal/` — a self-contained Lean 4 lake project (`lean-toolchain`
  pinned to `leanprover/lean4:v4.28.0`, `lakefile.toml`, `.gitignore`), **no
  Mathlib** dependency (builds in seconds, offline).
- Wrote the spine as a root module `formal/AlignmentProofSpine.lean` re-exporting
  nine layer modules under `formal/AlignmentProofSpine/`:
  - `Core.lean` — abstract carriers (`axiom`), concrete `Boundary`, MDL/graph
    scaffolding, a **from-scratch finite pigeonhole** (`finSkip`/`finPigeonhole`),
    bridges `MB1`–`MB8`, and a `BridgeAssumptions` record + `standardBridges`.
  - `Boundaries` (P05–P09, P36), `Capability` (P10–P13, P32, P43),
    `Bundles` (P14, P19–P22a proofs; P15/P17/P18/P22b counterexamples),
    `Correction` (P23–P26), `Successors` (P27–P29),
    `Adversarial` (P31, P33, P34, P37), `Philosophy` (P41, P42, P44, P45),
    `Certification` (P01, P02, P30, P35, P39, P40 + top-level theorems).
- `lake build` succeeds with **no errors, no warnings, no `sorry`/`admit`**.
- Verified separation via `#print axioms`: `P34` and other non-bridge results
  rest only on `propext`/`Quot.sound` (or abstract carriers);
  `certified_class_safety_from_bridges` additionally lists `MB6`/`MB7`.
- Docs: added `formal/README.md` (build, module map, proof/counterexample/bridge
  taxonomy, deviations); updated root `README.md` repository map.

## Decisions
- **No Mathlib.** Chose a core-only project for speed, offline builds, and the
  AGENTS "simplicity first / keep the theory small" guidance. Cost: the finite
  pigeonhole for `P34` is proved by hand (`finSkip` deletes the image of `0`)
  instead of `Fintype.card_le_of_injective`.
- **`axiom` not `constant`.** Lean 4 removed `constant`; abstract carriers use
  `axiom`, concrete structure uses `structure`/`def`.
- **Counterexamples use finite toy models** (`Bool`/`Fin`), per brief §8, rather
  than abstract `System` — they are genuine separations (`decide`).
- **`P44` uses the brief's §6 amendment** (two disagreeing legitimacy orderings),
  avoiding the inconsistent `L c ∧ ¬ L c` form.
- **Bridges kept visible.** `MB1`–`MB8` are `axiom`s aggregated in
  `BridgeAssumptions`/`standardBridges`, and the top-level
  `certified_class_safety_from_bridges` consumes `MB6`/`MB7` so the dependence is
  machine-checkable.
- Numbering follows the **brief** (§4/§5); the `.dot` graph's different numbering
  is treated as conjectural.

## Open / next
- Optional: derive `hrisk` in the top-level theorem from P01/P10/P13/P23/P27/P34
  rather than taking it as a hypothesis (brief §10 "stronger version").
- Optional: probabilistic `MB1` (`Pr[BoundaryCondition | certificate] ≥ 1 − δ`).
- Optional: wire selected theorem statements into the manuscript (e.g. a Ch. 39
  safety-case appendix), citing each as proof / counterexample / bridge.
- Not committed (per AGENTS git policy — user did not request a commit).

## Key paths
- `formal/` (project), `formal/README.md`, `formal/AlignmentProofSpine.lean`,
  `formal/AlignmentProofSpine/*.lean`
- `LeanProofSpineImplementationBrief.md`, `context/lean_proof_dependency_graph.dot`

## Commits
- none (no commit requested)
