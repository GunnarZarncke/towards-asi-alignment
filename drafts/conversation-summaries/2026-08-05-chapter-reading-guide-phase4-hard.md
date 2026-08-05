# 2026-08-05 — Chapter reading guide Phase 4 (high-fan-in and synthesis audit)

## Trigger
Audit the high-fan-in or synthesis chapters after Phase 3: ch16, ch22, ch26, ch33, ch42, and ch44.

## Verdict
**No new `readingguide` blocks.**

- **ch16:** ch15 hands off the compressed-control frame; ch18/ch19 are later chapters, and ch13's symbol is not a chapter-door prerequisite.
- **ch22:** self-starts with the intentional-compression test; bundle, bearer, and geometry machinery enters later.
- **ch26:** ch25 hands off and ch26 reintroduces the correction chain; ch29/ch36 are later.
- **ch33:** the certification envelope is self-starting; CCI and self-control formalism enter later; ch38/ch41/ch43 are later.
- **ch42:** begins as an artifact synthesis; `RiskGap` first appears in the later formal model.
- **ch44:** ch43's closing supplies adversarial-verifiability context; CCI, conserved properties, and `SuccessorSafe` are later detail rather than entry requirements.

## Rollout result
The full four-phase audit leaves two blocks:

1. **ch07** — ch05's correction-capacity scope condition.
2. **ch38** — ch02's artificial-civilizational control-loop object.

All other DAG edges were bridged in local prose, forward in book order, or introduced after the chapter opening. The graph is therefore an effective audit surface but not a generator of reader-facing blocks.

## Verification
- `make check`, `make pdf`, and `site/npm run build` passed.
- PDF build exposed that pre-existing `\symboldef` / `\symbolref` names collided with a loaded command and that two `\symbolref` sites wrapped their math argument in `$...$`. `metadata/preamble.tex` now owns the project marker macros explicitly and renders their arguments with `\ensuremath`; ch26 and ch28 now pass `C_t` without nested delimiters.

## Open
- Re-audit a chapter only when its opening, prior closing, or dependency edge changes.
