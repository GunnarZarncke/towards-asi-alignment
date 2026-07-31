# GL-88 diffuse effect named as smooth-uad's variable-smoothing case

**Date:** 2026-07-25

## Trigger

User connected GL-88's finding (handle-UAD on CIL's `basin_stability` finds
a nonzero but diffuse cross-agent effect, via the shared common-pool
resource) to `context/smooth-uad.pdf` (`zarncke2026smoothing` in the
bibliography) — recognizing that this is a case the theory in that paper
already names and explains, and that CIL's own coarse-graining machinery is
the tool the theory prescribes for it. Asked to confirm/incorporate this
understanding rather than run new code.

## What was done

Read `context/extracts/smooth-uad.md` (the paper's text extract) to confirm
the connection: the paper's §5 "variable smoothing" case is exactly this —
a many-to-one observation channel `Y_t = M X_t + eta_t` mixes raw per-agent
state into a shared aggregate; if the off-block leakage `R` (cross-boundary
mixing) is large relative to within-boundary signal, no per-pair test can
distinguish "these two agents are a unit" from "these two agents merely
share the same aggregate channel" (Corollary 2). The paper's own prescribed
practical protocol (§11) is not a better pairwise statistic but testing a
family of coarse-grainings and picking the candidate stable under them —
which is structurally what CIL's causal-emergence / effective-information
tooling already does.

Updated three places to make this connection explicit and citable, rather
than just agreeing in chat:

1. **`chapters/ch07-finding-boundary.tex`** — extended the GL-88 paragraph
   with the theoretical naming: diffuse coupling under a shared aggregate is
   the variable-smoothing case (`\autocite{zarncke2026smoothing}`), and the
   fix is a coarse-grained candidate test via causal-emergence tooling
   (`\autocite{rosas2020emergence}`), not a better pairwise statistic. Added
   `zarncke2026smoothing` to the chapter-references citation list.
2. **`experiments/graded-lab-simulation/results/FINDINGS.md`** — added a
   "Theoretical framing (named, not merely described)" subsection to GL-88,
   and sharpened its "Open / next" to name the concrete follow-up (run CIL's
   EI coarse-graining search on the same traces, test population/coalition
   candidates) rather than a generic cross-check.
3. **`experiments/graded-lab-simulation/REPRODUCTION.md`** §14 item 2 —
   noted it is now concretely motivated by GL-88's diffuse result and the
   smoothing-theory framing, not just "a structurally different statistic
   worth trying."
4. **`references/bibliography-summaries.tex`** — replaced
   `zarncke2026smoothing`'s generic placeholder summary with one describing
   the actual recoverability-under-smoothing content and its coarse-graining
   implication.
5. **`appendices/appN-experimental-evidence.tex`** — extended the
   `finding:gl-88` row with the same framing.

## Non-obvious decisions

- Did not implement the CIL causal-emergence coarse-graining run itself in
  this pass — the user's message read as confirming/naming a theoretical
  connection, not requesting new code; the concrete follow-up is recorded
  as the next actionable step (REPRODUCTION.md §14 item 2, GL-88 "Open /
  next") rather than attempted under the same time pressure as the smoke
  pilots.

## Open / next steps

- Run CIL's causal-emergence / effective-information coarse-graining search
  on the GL-88 traces (or fresh episodes at the same small scale), testing
  whether a population- or coalition-level candidate clears a blanket
  criterion the per-pair freeze probe cannot resolve.

## Key paths

- `chapters/ch07-finding-boundary.tex`
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-88)
- `experiments/graded-lab-simulation/REPRODUCTION.md` (§14 item 2)
- `references/bibliography-summaries.tex` (`zarncke2026smoothing`)
- `appendices/appN-experimental-evidence.tex` (`finding:gl-88`)

No commit made yet this session; changes are in the working tree pending
review/commit instruction.
