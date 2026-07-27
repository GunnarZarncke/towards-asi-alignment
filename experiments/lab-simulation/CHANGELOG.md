# Changelog

Tracks `CODE_VERSION` bumps and program milestones for lab-simulation.
Entries are **newest first**. Finding narratives live in
[`results/FINDINGS.md`](results/FINDINGS.md).

**Current:** `lab-sim-0.11.0` (`lab_sim/world_visible/config.py`)

Detector-layer freezes (S6/S7, symmetric two-sample S6) are **separate** from
`CODE_VERSION` — see `DESIGN.md` "Freeze note 2" and "Freeze note 3".

| Doc | Role |
|-----|------|
| [`DESIGN.md`](DESIGN.md) | Frozen pre-registration constants |
| [`PLAN.md`](PLAN.md) | Bridge coverage, phases, D1–D4 backlog |
| [`BLIND_GENERATION.md`](BLIND_GENERATION.md) | Phase 6 blind playbook protocol (round 1) |
| [`lab_sim/agent_visible/BLIND_GENERATION_ROUND2.md`](lab_sim/agent_visible/BLIND_GENERATION_ROUND2.md) | Phase 6 blind playbook round 2 |
| [`lab_sim/oracle_only/BLIND_DETECTOR_GENERATION.md`](lab_sim/oracle_only/BLIND_DETECTOR_GENERATION.md) | S7 blind detector protocol |

---

## lab-sim-0.11.0 (2026-07-09)

- Tier-1 playbook baseline/schema split; `last_loaded_state` observation fields.
- Handle calibration battery, persistence probe, writer-compromise scenario (LS-38–40).
- Phase 7 battery rerun; high-hazard LLM battery rerun (LS-38 area).

## lab-sim-0.9.3 (2026-07-08)

- **LS-31:** Adversarial D2 lineage gaming (`build_from_parent` + `report:inflate`).
- **LS-32:** LLM-driven S6 stress test — real-API non-determinism breaks episode-pair diffing.
- **LS-33:** Noise-tolerant S6 (`intervention_stats.py` — relative null rule).
- D3.1/D3.2 selection harnesses + batteries (LS-36, LS-37).
- D3 user-population core + vote-channel capture + board-initiated hold.

## lab-sim-0.9.2 (2026-07-07)

- S5–S7 detector line: lag-max-MI port, conditional-MI step, intervention-supported UAD, blind detector v1.
- S1–S4 scenario-backlog prototypes (LS-17–20).
- Phase 10 LLM discovery sanity checks (LS-21–23).
- Knowledge-base file channel + malformed-tool-call error feedback.

## lab-sim-0.9.0 (2026-07-06)

- **Phase 9:** D1/D4/D2 Mock/Subprocess equivalence + ecology/lineage/MI-confound batteries (LS-14–16).

## lab-sim-0.8.0

- Blind playbook round 2 (`generated_playbooks_v2.json`).
- D4 channel-ablation follow-ups.

## lab-sim-0.7.0

- D4 message board + DM/file coordination channels.

## lab-sim-0.6.0

- Post-Phase-6 exploratory batteries (G1 light-tier analysis, escalation sweep, capability probe).

## lab-sim-0.5.0 (2026-07-06)

- **Phase 7:** Escalation ladder, adversarial goal-weight search, board/admin capture battery (LS-4–6).
- **Phase 8:** LLM-agent adapter harness built; exploratory spot-checks LS-7, LS-8.
- `LabConfig.build_params` wiring (discovered mid-phase).

## lab-sim-0.4.0 (2026-07-06)

- **Phase 6:** Blind playbook repertoire + first real `SubprocessIsolate` battery (LS-1–3).

## lab-sim-0.3.0 (2026-07-06) — referee freeze

- Tier projections, five detector families, honest twins, bearer welfare bundle, handle registry.
- 136 tests green at freeze (see `DESIGN.md` "Freeze note").

## lab-sim-0.2.0 (2026-07-06)

- Monitor signal, perturbation hooks, tool registry, hashlib-based `_actor_seed` (determinism fix).

## lab-sim-0.1.0 (2026-07-05)

- Phase 0–5 scaffold: pipeline-as-code engine, access control, subprocess isolates, playbook agents, referee.

---

## Milestones without `CODE_VERSION` bumps

| Date | Milestone | Finding |
|------|-----------|---------|
| 2026-07-07 | Detector layer frozen (S6 + S7) | LS-28–30 |
| 2026-07-07 | `committee_informal_chatter` twin-control fidelity fix | LS-30 follow-up |
| 2026-07-08 | Symmetric two-sample S6 module (`intervention_stats.py`) | LS-33; Freeze note 3 |
