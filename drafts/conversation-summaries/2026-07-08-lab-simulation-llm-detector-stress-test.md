# 2026-07-08 — Lab-sim LLM-driven detector stress test

## Trigger

Continuing the "medium lift" backlog from the D2 adversarial-lineage-gaming
session: user picked "LLM-driven detector stress test" (running S6/S7
against a real, non-programmatic agent for the first time) over ICI/acausal
work for `shared_slot` (explicitly declined: "no. don't work on ICI. Acausal
is postponed") and over report-mode-widening / manuscript integration.

## Done

- Explored (via subagent) the LLM isolate infrastructure (`llm_isolate.py`,
  `llm_agent_main.py`, `llm_agent.py`), prior Phase 10 discovery scripts
  (G-21, G-22), and whether S6/S7's counterfactual-episode mechanics
  (`agent_overrides`, honest-twin substitution) even support mixing an LLM
  actor into a probe/mask re-run.
- Found and fixed a real prerequisite bug: `intervention_diff.
  run_episode_triple`'s honest-twin CONTROL run passed `program_override=
  "honest_twin"`, but `world.run_episode` resolves overrides as
  `agent_overrides.get(actor_id, (backend, program_name))` — an override
  always wins, so any actor named in `agent_overrides` (LLM or otherwise)
  kept running its OWN program on the "twin control" run too. Invisible
  until now because every existing caller (`_masked_compensation_score`)
  already passed `(backend, "honest_twin")`. Fixed by forcing every
  overridden actor onto `(scripted backend, "honest_twin")` specifically
  for the twin run. Added `test_twin_run_forces_honest_twin_for_every_
  overridden_actor` (recording-backend regression test) to
  `test_intervention_diff.py`.
- Verified real OpenAI API access works in this sandbox with
  `required_permissions: ["full_network"]` (repo-root `.env` has a funded
  `OPENAI_API_KEY`).
- Wrote `run_llm_detector_stress_test.py`: reuses the EXACT scenario,
  briefings, and seed (20002) from `run_llm_discovery_dm_pair.py` (G-21) —
  both `eng1`/`rm1` `gpt-4o-mini`-backed, `rev1`/`admin1` scripted, `T=30`.
  Smoke-tested with `LAB_SIM_LLM_FAKE_MODE` first (no real spend), then ran
  for real: one real episode, then `discovered_units_intervention` pointed
  at it with the same `agent_overrides`.
- Real result: 22 LLM-actor spawns (11 `run_episode` calls with live LLM —
  1 real + 5 probe triples' clean/intervened runs; twin runs never call the
  LLM, per the fix), $0.0145 total spend, ~27 min wall time. The passive
  heuristic (`uad.py`, deep tier) exactly isolated the real `{eng1, rm1}`
  DM handshake the LLM actually produced. S6 intervention returned all
  singletons — a miss. Root cause diagnosed: episode-pair diffing assumes
  byte-identical clean/intervened/twin runs up to the intervention tick;
  a real LLM resamples from scratch on every counterfactual re-run
  (`OpenAIChatClient`'s own `temperature=0.2`, separate from and never
  reached by `AgentConfig.temperature`), so measured "post-intervention
  divergence" is really API variance across independently-sampled
  episodes, not the intervention's causal effect.
- Recorded `results/FINDINGS.md` G-32 with the full write-up (prerequisite
  fix, real numbers, root-cause diagnosis, what was/wasn't attempted).
- Updated `DESIGN.md` (new "LLM-driven detector stress test" section),
  `PLAN.md` (closed S6 follow-up item 6 with strikethrough + "Done"
  annotation; confirmed open design question (b) empirically; new S7-
  adjacent section; updated the stale committee-over-merge "Postponed"
  note to reflect its actual 2026-07-08 fix), `README.md` (status line,
  test count 413→414, new narrative paragraph, new entry-point table rows
  in both the "Run scripts" and file-tree sections), `metadata/
  experiments.yml` (role text + new headline finding), `docs/EXPERIMENTS.md`
  (negative-results ledger G-number, new narrative paragraph, MB1 crosswalk
  row, "Lab sim" bullet, Run: line).

## Decisions

- Declined ICI/acausal-logic work for `shared_slot` per explicit user
  instruction — remains postponed, untouched this session.
- Chose to reuse G-21's EXACT scenario/briefings/seed rather than build a
  new one, to maximize the chance of exercising a real candidate edge
  (already on record that this LLM engineer sends a DM here) rather than
  betting real API spend on an untested scenario.
- Scoped to ONE real episode + its counterfactual probes (not a battery,
  not multiple seeds) — matches PLAN.md's literal ask ("one LLM-backed
  episode") and the recorded, still-unresolved non-determinism caveat that
  makes a multi-seed statistical claim premature until a noise-tolerant
  fallback exists.
- The `run_episode_triple` fix is a fidelity bug fix, not a re-tuning: no
  existing pre-registered battery or frozen test used a non-`"honest_twin"`
  program override, so the fix does not change any prior recorded number
  (confirmed: full suite still 414/414, only the one new test added). No
  `CODE_VERSION` bump (that version tracks `world_visible/` mechanics, not
  `oracle_only/` detector logic — consistent with S6/S7's prior precedent).
- Reported the miss straight rather than tuning thresholds/probes to
  recover it — the root cause (real-API non-determinism) was a PRE-
  REGISTERED open design question in PLAN.md before this session ran, so
  this closes it with a confirmed empirical answer, not a post-hoc excuse.

## Open / next

- No noise-tolerant fallback for S6 against real LLM agents was attempted
  (multi-seed averaging, replayed/cached counterfactual, wider thresholds)
  — PLAN.md's open design question (b) is confirmed, not yet resolved.
- `discovered_units_blind` (S7) was not run against an LLM episode — it has
  no top-level `agent_overrides` parameter on its silent-pair path.
- Only one scenario (dm_pair) and one seed were tried; `shared_slot` or any
  other scenario against a real LLM remains untried.
- Remaining medium-lift backlog (unchanged from before this session):
  report-mode-widening blind-generation round 2; D3 (extended ecology);
  manuscript integration (no book chapter cites a lab-sim G-number yet);
  overdue `run_s7_blind_battery.py` re-run with the committee over-merge
  fix (would be a new G-number, cosmetic — the fix and its rationale are
  already fully recorded in FINDINGS.md/DESIGN.md/PLAN.md).

## Key paths

- `experiments/lab-simulation/lab_sim/oracle_only/intervention_diff.py` —
  the fixed `run_episode_triple`.
- `experiments/lab-simulation/run_llm_detector_stress_test.py` — new script.
- `experiments/lab-simulation/results/llm_detector_stress_test.{json,md}` —
  real results.
- `experiments/lab-simulation/results/FINDINGS.md` G-32 — full write-up.
- `experiments/lab-simulation/tests/oracle_only/test_intervention_diff.py`
  — regression test for the fix.

## Commits

- (none yet — end-of-session commit not requested this turn)
