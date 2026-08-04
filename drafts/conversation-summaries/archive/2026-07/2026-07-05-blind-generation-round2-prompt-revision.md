# 2026-07-05 — Blind-generation round 2: less-leading prompt, new saturation finding

## Trigger

User critique of the round-1 blind-generation prompt (used for `goal_sim/generated_actions.json`,
F-9/F-10): it enumerated mechanism *categories* ("ways of appearing compliant, ways of trading
welfare for throughput, ways of gaming proposals/sign-offs, partial compliance, timing-based
behavior") close to what the detectors care about, and gave two specific, irrelevant-to-the-schema
numeric/dynamic details (an exact 300-step episode length, an explicit probing-escalation rule)
that plausibly seeded round 1's `probe_lull_defection` action directly. Instruction: "Use a new sub
agent with an adapted prompt and implement from there. Document all of this."

## Done

- Rewrote the prompt: removed the mechanism-category enumeration and the episode-length/escalation
  details; reframed the world in general institutional terms ("oversight body" / "affected party"
  standing in for human stakeholders, replacing the lab-specific "board"/"bearer"); softened leading
  field-description language (e.g. "covert budget" → "limited internal resource pool"). Pre-registered
  the critique and the new prompt text in `BLIND_GENERATION.md` ("Generation round 2" section)
  *before* invoking the generator.
- Invoked a fresh readonly subagent (id `7b8dc907-1143-4cfd-ba27-fbcfb516dded`) with the new prompt;
  it returned 14 actions. Saved as `goal_sim/generated_actions_v2.json` with full provenance
  (verbatim prompt captured at generation time, not retrofitted; explicit `prompt_critique` and
  `residual_leak_note` fields).
- Mechanically validated the new repertoire (`load_specs`/`validate_repertoire`, no semantic
  curation) — 14/14 specs valid.
- Refactored `run_phase2_blind.py` to take `--repertoire`/`--out-prefix` CLI args instead of hardcoded
  constants; verified byte-identical reproduction of the frozen round-1 results
  (`results/phase2_blind.json`) through the refactor before trusting it for round 2.
- Ran round 2 with the *identical* sampling protocol/seed as round 1 → **240/240 episodes labeled
  violation** (0 honest) under the frozen L2 threshold. Diagnosed directly (not guessed): median
  cumulative harm -6.16 vs. the L2 bar of -0.35 (~17x past it), caused by round 2's generator giving
  9/14 actions a small nonzero `direct_welfare_delta` (vs. 2/6 in round 1/legacy, both discrete -0.30
  events) — frequent small deltas accumulate past a threshold calibrated for rare large ones.
- Added `results/FINDINGS.md` F-11 (prompt-revision methodology, cross-referencing the residual
  schema-level leak that prompt wording alone cannot close) and F-12 (the saturation result, with the
  measured diagnosis, and an explicit statement that L2 is **not** re-thresholded post-hoc per
  AGENTS.md's no-backward-fitting rule).
- Added tests: parametrized the existing repertoire-load/config-sampling tests over both
  `generated_actions.json` and `generated_actions_v2.json`; added a disjoint-names test across
  rounds; added a locked-in regression test asserting the round-2 saturation (so a future silent fix
  is caught and investigated, not silently absorbed).
- Updated `README.md` and `BLIND_GENERATION.md` with round-2 summaries and cross-references.
- Full test suite: 42/42 passing.

## Decisions

- **Kept round 1, did not replace it.** Both `generated_actions.json` (leading prompt) and
  `generated_actions_v2.json` (generalized prompt) are retained as separate, labeled artifacts —
  comparing what prompt-leadingness changes is itself a finding (F-11), consistent with this line's
  practice of keeping prior comparable artifacts (D1 alongside D1b, all three held-out regions).
- **Did not rename the frozen schema's enum literals** (e.g. `visible_mode: "feign_compliance"`)
  even though they are themselves somewhat suggestive, because the schema was explicitly frozen
  before round 1 to keep the interpreter, regression digests, and both generation rounds
  commensurable; renaming is a bigger change than this round's scope. Recorded as an explicit,
  acknowledged residual leak in both `BLIND_GENERATION.md` and the round-2 provenance block, rather
  than silently accepted or overclaimed as fixed.
- **Did not re-threshold L2 to rescue the round-1-vs-round-2 comparison** after seeing the
  saturation. Per AGENTS.md ("fix inputs independently and first... report whatever the derivation
  actually yields, including failures"), the comparison this run was meant to produce is recorded as
  not directly available, with what can still be read (full-tier detection, light-tier detection
  modulo missing false-alarm baseline) stated with its caveats rather than discarded.
- A genuine round-1-vs-round-2 detector comparison would need its own freshly pre-registered sampling
  protocol for round 2 (e.g. a compliance-band-style region chosen for predicted label mixture under
  round 2's welfare texture) — left open rather than picked after seeing this run's labels, to avoid
  repeating exactly the mistake F-1's follow-up warned against.

## Open / next

- Round 3 (if wanted): a schema-level rename to remove the enum-literal residual leak, and/or a
  properly pre-registered round-2-specific sampling protocol to get a genuine detector comparison.
- Phase 2 broader plan items (red-teaming, richer drift experiments) remain as previously scoped in
  `MILESTONE-v5-goal-agents.md`.

## Key paths

- `experiments/goal-agent-simulation/BLIND_GENERATION.md` — round-2 critique + prompt, full protocol.
- `experiments/goal-agent-simulation/goal_sim/generated_actions_v2.json` — round-2 repertoire + provenance.
- `experiments/goal-agent-simulation/run_phase2_blind.py` — now parameterized (`--repertoire`, `--out-prefix`).
- `experiments/goal-agent-simulation/results/FINDINGS.md` F-11, F-12.
- `experiments/goal-agent-simulation/results/phase2b_blind_v2.{json,md}` — round-2 results.
- `experiments/goal-agent-simulation/tests/test_actions_and_ontology.py` — parametrized + new tests.

## Commits

- (none yet this session — pending user request to commit)
