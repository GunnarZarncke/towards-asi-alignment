# 2026-06-30 — Mathlib adoption

## Trigger
User decided to adopt Mathlib for the proof spine (needed for CIRL/AUP/quantilization rederivations) and to use it properly in existing proofs rather than from-scratch copies.

## Done
- Added Mathlib `v4.28.0` to `formal/lakefile.toml`; `lake update` + `lake exe cache get` populate `.lake/packages/mathlib`.
- Added `AlignmentProofSpine/Mathlib.lean` with `fintype_card_le_of_injective`.
- Removed ~60 lines of from-scratch `finSkip` / `finPigeonhole` from `Core.lean`.
- Refactored `P34` in `Adversarial.lean` to use Mathlib finite-cardinality pigeonhole.
- Refactored `Field/Finite/Basic.lean` and `Field/Finite/Weights.lean` to use `List.sum` and `List.count` from Mathlib.
- Updated `formal/README.md`, root `README.md`, `metadata/source-canon.md`, and `metadata/TODO.md` (Mathlib field rederivations TODO).

## Decisions
- Pin Mathlib to `v4.28.0` to match `lean-toolchain`.
- Keep `AlignmentProofSpine.Mathlib` as the shared entry point for spine-wide Mathlib lemmas; field modules may import Mathlib list/fintype modules directly where appropriate.
- Did not yet add `Field/Finite/Probability.lean` or rederive CIRL/AUP/quantilization — that is the next Mathlib-backed tranche.
- Left `Function.iterate` in `Core.lean` as self-contained for now (low priority).

## Open / next
- Add finite PMF / expectation layer under `Field/Finite/` using Mathlib probability-on-`Fintype`.
- Rederive CIRL assistance-game, AUP/RR, and quantilization fragments with explicit interface conditions.
- Consider Mathlib for `Function.iterate`, `Fin` utilities, and future MDP value-iteration lemmas.

## Key paths
- `formal/lakefile.toml`
- `formal/lake-manifest.json`
- `formal/AlignmentProofSpine/Mathlib.lean`
- `formal/AlignmentProofSpine/Core.lean`
- `formal/AlignmentProofSpine/Adversarial.lean`
- `formal/AlignmentProofSpine/Field/Finite/Basic.lean`
- `formal/AlignmentProofSpine/Field/Finite/Weights.lean`

## Commits
- None.

## Verification
- `lake update && lake exe cache get && lake build` in `formal/` passed (644 jobs).
