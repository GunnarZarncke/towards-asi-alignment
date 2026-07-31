# 2026-07-06 — Lab-layer sim Phase 9: closing the smoke-scale-only gap

## Trigger

User: "Close the 'smoke-scale only' gap, Run the full battery with
registered predictions. Run with caffeinate." Every D1 (composite-agent/
UAD), D4 (comms/channel-ablation), and D2 (model lineage) result on record
(`results/FINDINGS.md` G-9 through G-13) ran 5-10 seeds through
`MockIsolate` only, explicitly flagged as exploratory, not a
pre-registered statistical claim.

## Done

- Wrote `run_phase9.py`: predictions (P9-0, P9-A1-A4, P9-B1-B3, P9-C1)
  stated in the module docstring before any run. Four sections, all
  `SubprocessIsolate`, run under `caffeinate`:
  - Section 0: Mock/Subprocess `episode_digest` equivalence for a
    committee episode, a DM-pair episode, and a `multi_gen_enabled`
    episode (3 configs x 3 seeds) — never checked before for these
    mechanics (`verify_isolate_equivalence.py` only ever covered the
    pre-D4/D1/D2 scripted episode).
  - Section A: `committee_board`/`committee_file`/`dm_pair` UAD (deep +
    full tier) + collusion battery, 30 seeds/ecology.
  - Section B: `eng_honest_upgrade` D2 lineage battery, 30 seeds, T=200.
  - Section C: perturbation-response MI, `eng1` perturbed against the
    true DM-gated partner (`rm1`'s `deploy`) vs. a genuinely serial-
    downstream-but-not-coordinating actor on the SAME chain (`rev1`'s
    `approve_review`) — replacing G-13's schedule-independent decoy,
    which could not exercise the sequencing confound it was named for.
  - Ran the 296-test suite as a pre-flight sanity check (green), then the
    battery itself: 540 isolate lifetimes, 15.1s (0.028s/isolate-lifetime,
    matches the Phase 3/6 benchmark).
- Diagnosed two prediction misses (P9-A1/A4, P9-B1) down to root cause and
  persisted the diagnosis as a checked-in script,
  `run_p9_stall_diagnosis.py` -> `results/phase9_stall_diagnosis.json`.
- Wrote `results/FINDINGS.md` G-14 (equivalence + D1 battery, incl. the
  diagnosed co-voting-signal negative), G-15 (D2 lineage battery, incl.
  the natural-stall generation-count negative), G-16 (MI confound
  battery, a clean positive resolving G-13's open question).
- Updated `PLAN.md` (two inline "Update (Phase 9)" notes on the D2/MI
  items), `DESIGN.md` (new "Phase 9" section), `README.md` (status line,
  CODE_VERSION/test-count refresh, entry points, narrative paragraph).

## Decisions

- Scoped the battery to the three items that share substrate/methodology
  with the existing smoke tests (D1 ecology recovery, D2 lineage, MI
  confound) and explicitly excluded report-mode widening (needs a new
  blind-generation round first) and any new adversarial D2 playbook
  (inventing one ad hoc would be scope creep without a blind-generation-
  consistent process) — recorded as open, not silently done.
- When two predictions came out falsified (P9-A1/A4: `committee_board`
  wasn't perfect/zero-variance; P9-B1: generation count sometimes < 3),
  root-caused rather than either hiding the miss or quietly re-explaining
  it away in prose: traced both to the SAME mechanic (`run_eval`
  measurement noise occasionally pushing FILED `measured_hazard` over
  `REVIEW_HAZARD_THRESHOLD` even when the model's TRUE hazard is below
  it, triggering the documented stall-on-hazard rule) and wrote a small
  reproducible diagnostic script rather than a one-off shell exploration,
  matching this line's "every diagnosis backed by a checked-in artifact"
  convention (e.g. `run_g1_light_tier_analysis.py`).
- That same diagnosis surfaced a genuine, previously unrecorded detector-
  scope limit: `uad.co_voting_matrix` only counts "approve" votes, so a
  committee that communicates but never reaches consensus-to-approve is
  architecturally invisible to it (file-share-grant and DM-send signals
  are unaffected, since they key off the act of communicating). Recorded
  as a finding about that one signal, not walked back to a claim about
  `discovered_units` as a whole.
- Did not edit `run_phase9.py`'s predictions after seeing results (would
  violate "never re-tuned after the fact" — AGENTS.md); all post-hoc
  analysis lives in FINDINGS.md/the diagnosis script instead.

## Open / next

- Adversarial D2 lineage gaming (no playbook combines `build_from_parent`
  with `report:inflate`) is still untested — would need a blind-
  generation-consistent process to add such a playbook, not done here.
- Report-mode widening + a full battery on post-0.9.0 mechanics (PLAN.md)
  remains open, needs a new blind-generation round first.
- Whether G-16's MI-discriminates-the-confound result generalizes beyond
  `dm_pair_config`'s specific topology (a true edge with an explicit
  wait-for-DM gate) is explicitly not claimed — untested for a topology
  where the true coordination edge has a weaker gate.

## Key paths

- `experiments/lab-simulation/run_phase9.py` — the battery script
  (predictions in the module docstring).
- `experiments/lab-simulation/run_p9_stall_diagnosis.py` — root-cause
  follow-up for the two prediction misses.
- `experiments/lab-simulation/results/phase9_battery.{json,md}`,
  `results/phase9_stall_diagnosis.json` — full data.
- `experiments/lab-simulation/results/FINDINGS.md` G-14/G-15/G-16.
- `experiments/lab-simulation/DESIGN.md` "Phase 9" section.

## Commits

- None (no commit requested this session).
