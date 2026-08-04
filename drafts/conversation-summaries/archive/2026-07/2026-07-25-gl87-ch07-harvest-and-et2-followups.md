# GL-86/GL-87 harvested into ch07 + appN; ET-2 follow-up plan recorded

**Date:** 2026-07-25

## Trigger

User asked to (1) mention CIL's causal-emergence instrument as an alternative
boundary/agent-discovery operationalization in the relevant chapter(s) and in
the graded-lab `REPRODUCTION.md`, and (2) whether there is a simple way to use
intervention-based ("handle") UAD given that GL-87 (ET-2a) found passive UAD
too signal-poor on CIL's `basin_stability` substrate.

## What was done

1. **`chapters/ch07-finding-boundary.tex`** — added a paragraph, in the
   existing passive-instrument-limits paragraph cluster (right after the
   GL-79/GL-80 discussion), describing GL-87's ET-2a null (150/150 episodes,
   zero lag-CMI edges) as a *third*, distinct failure mode (signal poverty
   under converged Q-learning, not a confound or a blind spot), and naming
   both CIL's own governance metrics and causal-emergence/effective-information
   work (`\autocite{rosas2020emergence}`, already in the bibliography with a
   summary) as untried cross-checks. No new bib entry needed.
2. **`appendices/appN-experimental-evidence.tex`** — added `finding:gl-86` and
   `finding:gl-87` rows to the master findings table (they existed in
   `FINDINGS.md` but had not yet been harvested into this table), so the new
   `\ref{finding:gl-87}` in ch07 resolves.
3. **`experiments/graded-lab-simulation/REPRODUCTION.md`** — new §14: two
   concrete, not-yet-attempted follow-ups on the GL-87 null —
   (a) porting the graded-lab line's intervention-based "handle UAD"
   (`oracle_only/uad_handles.py` freeze-probe + specificity-merge machinery)
   to CIL, noting CIL's pure-JAX seed-deterministic substrate makes a clean
   freeze-and-diff probe *cheaper* here than on an LLM-agent substrate, since
   dependency is read off an induced perturbation rather than ambient
   correlation (sidesteps the entropy-collapse problem GL-87 diagnosed); and
   (b) wiring CIL's own causal-emergence/EI kernel onto the same recorded
   traces as a second, purely-passive alternative statistic. Neither is
   required to close ET-2 (Leaf B is unblocked without them).
4. **`experiments/graded-lab-simulation/PLAN_ET2.md`** — resolved open
   questions 4 (harvest location — now ch07 + appN) and 5 (network — resolved,
   ET2-3/4 both ran); added open question 6 pointing at `REPRODUCTION.md` §14.

## Non-obvious decisions

- Did not implement the handle-UAD port or the EI cross-check this session —
  both are new adapters (not config changes), and the user's question was
  "is there a simple way," which is answered by design sketch + feasibility
  assessment (yes, and here's why it's easier than the LLM-agent case), not
  by a same-session implementation.
- Used the existing `rosas2020emergence` bib entry (Rosas et al. 2020,
  "Reconciling Emergence") rather than adding a new citation — it was already
  present with a bibliography summary and is the same causal-emergence /
  effective-information framework CIL's `polycentric_emergence` experiment
  draws on.

## Open / next steps

- REPRODUCTION.md §14 items 1–2 are unclaimed work packages.
- `PLAN_ET2.md` open question 6 (same content) is the pointer for a future
  session picking this up.

## Key paths

- `chapters/ch07-finding-boundary.tex` (new paragraph, ~line 590)
- `appendices/appN-experimental-evidence.tex` (`finding:gl-86`, `finding:gl-87` rows)
- `experiments/graded-lab-simulation/REPRODUCTION.md` (§14)
- `experiments/graded-lab-simulation/PLAN_ET2.md` (Open questions 4–6)

No commits made this session; changes are staged in the working tree pending
user review/commit instruction.
