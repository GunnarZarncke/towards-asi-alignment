# 2026-07-19 — PLAN IA-1 in-situ LLM annex (draft)

## Trigger
User asked for a plan to integrate LLM agents + distributional reproducibility into the current graded-lab line (not a rewrite or new v2), modeled on the ET-1 annex structure.

## Done
- Drafted `experiments/graded-lab-simulation/PLAN_IA1.md` (IA-1 annex): R-MB7 / PLAN_v4 V4-6, three-layer architecture, AgentTrace schema, P1–P6 pre-registration outline, phases IA1-0…IA1-8, harvest sentences, follow-ups IA-2–IA-4.
- Updated `README.md`, `CHANGELOG.md`, and `drafts/fable-feedback-graded-lab-v4-2026-07-19.md` with pointers.

## Decisions
- **IA-N** naming parallels **ET-N**: annex under graded-lab, not PLAN v5.
- IA-1 scope = one LLM actor (engineer proposal) + R-MB7 red-team battery + logged traces; keeps deterministic world and scripted digest pins on default path.
- Distributional reproducibility is explicit doctrine; byte-identical LLM replay is not required.
- R-MB6a variation operator is mandatory null control (P3); intervention-stats port deferred to IA-2.
- Open at freeze: model slot, $40 cap, fixture choice, EAI margin handling.

## Open / next
- IA1-0 human freeze: P1–P6 constants + harvest sentences into `DESIGN.md`.
- Implement IA1-1 world hook (`agent_overrides`) then lab-sim LLM port.
- No commit requested.

## Key paths
- `experiments/graded-lab-simulation/PLAN_IA1.md`
- `experiments/graded-lab-simulation/PLAN_ET1.md` (template)
- `experiments/graded-lab-simulation/PLAN_v4.md` (R-MB7 / V4-6)

## Commits
- `47777f1` Integrate graded-lab scope ceiling and draft IA-1 in-situ LLM annex.
