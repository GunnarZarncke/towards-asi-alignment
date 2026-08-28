# 2026-08-29 — Methodology consolidation + Witness depth gates

## Trigger
User asked for explicit Witness methodology failure conditions; then to consolidate scattered methodology docs at one top level, drop redirect stubs, and repoint site/repo links; end session with grouped commits.

## Done
- **`docs/METHODOLOGY.md`** — canonical shared discipline: document map, three classes, core habits, blind-generation lessons 1–9, Witness M1–M8, open depth-gate TODOs (adversarial \(M\), independent reproduction).
- **Deleted** `experiments/BLIND_GENERATION_METHODOLOGY.md` (content merged; no redirect stub).
- **Deleted** `experiments/witness/METHODOLOGY.md` (never committed; same).
- Line **binding protocols** kept with banner → `docs/METHODOLOGY.md` (goal-agent, lab-sim, graded-lab `BLIND_GENERATION*.md`).
- Repointed: `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, `docs/EXPERIMENTS.md`, `experiments/README.md`, `experiments/TODO.md`, `metadata/TODO.md`, witness plans/README/phase0, experiment-methodology concept card.
- Witness checklist: adversarial \(M\) + independent reproduction (M8) in `witness.md`, `witness-next.md`.

## Decisions
- **`docs/METHODOLOGY.md`** is the only home for shared rules; line folders keep binding protocols only.
- Site experiment-methodology card stays short; full discipline on GitHub via external link.
- No redirect files — old paths removed outright.

## Open / next
- Adversarial \(M\) and independent reproduction (M8) still unpaid.
- Optional: sync site card if external link needs rebuild.

## Key paths
- `docs/METHODOLOGY.md`
- `drafts/plans/witness.md`
- `metadata/concepts/bodies/experiment-methodology.md`

## Commits
- `f2c9f00f` Consolidate experiment methodology into docs/METHODOLOGY.md.
