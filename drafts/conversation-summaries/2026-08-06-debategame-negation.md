# 2026-08-06 — DebateGame negation / role-swap

## Trigger
Hostile feedback: `Claim` had only `atom`/`conj`/`disj` (monotone), so `debate_tracks_truth` was a trivial Boolean-evaluator identity and invited readers to dismiss the game as non-adversarial. Request: add negation with defender/challenger swap.

## Done
- Extended `Claim` with `neg`; `Claim.eval`, `debateValue`, and `debateOutcome` handle negation (`debateOutcome` swaps strategies and flips the outcome).
- Unified `honestStrategy` for both roles so role-swap stays honest; proved `honest_optimal` by induction generalizing over strategies; kept `honestDefender`/`honestChallenger` as aliases.
- Added `negation_role_swap_tracks_truth` witness.
- Updated App G debate paragraph, `Field/Debate.lean` module blurb, and LW MB4/debate draft snippet.
- `lake build` of `DebateGame` + `Field.Debate` succeeds.

## Decisions
- Role-swap semantics: `debateOutcome judge σ τ (.neg c) = !(debateOutcome judge τ σ c)` (Irving-style), not a polarity bit threaded through every constructor.
- Scope note in the module header: finite claim-tree *fragment* of Irving et al. (deterministic judge, no compute limits) — negation closes the monotone gap without claiming the full protocol.

## Open / next
- Optional: sync site field-projection / concept-card prose if any still say "conjunction/disjunction" only (App G updated; check regenerated site JSON on next sync).
- No commit requested.

## Key paths
- `formal/AlignmentProofSpine/Field/Finite/DebateGame.lean`
- `formal/AlignmentProofSpine/Field/Debate.lean`
- `appendices/appG-lean-proof-spine.tex`

## Commits
- `1e82c95f` Add negation with role-swap to the finite debate game.
