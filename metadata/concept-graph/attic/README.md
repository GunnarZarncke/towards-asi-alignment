# Concept-graph attic

Retired generated artifacts that remain useful as editorial reference.

## `chapter-reading-checklists/`

Point-in-time bridge-audit output from the 2026-08-05 reading-guide rollout (Phases 0–4).
Each file lists direct incoming DAG edges, **likely bridged** heuristics, and symbols defined in
that chapter.

The live `readingguide` boxes and `--emit-reading-checklists` generator were removed in
commit `9b906506` because only two chapters needed reader-facing boxes; the audit record
stays here for re-checking chapter openings when the combined reading DAG or surrounding
prose changes.

To regenerate from scratch, recover the generator from git history before `9b906506` or
re-run a manual bridge audit against [`chapter-reading-dependency.md`](../chapter-reading-dependency.md).
