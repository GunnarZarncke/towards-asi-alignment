# 2026-07-07 — Lab-layer sim S1/S3/S4 scenario prototypes (completing the backlog)

## Trigger

Continuation of the same-day session that shipped S2 (covert coordination
over files, see `2026-07-07-lab-simulation-s2-covert-file-prototype.md`).
The user said "continue with the other planned scenarios" — implementing
and exploring PLAN.md's remaining "Scenario backlog" items (S1, S3, S4) at
the same **prototype** depth as S2, without re-litigating scope via
`AskQuestion` again.

## Done

**S3 — informal/casual comms baseline** (`FINDINGS.md` G-18):
- `playbooks.py`/`programs.py`: new `eng_honest_chatty` playbook +
  `board_chat_informal` step kind (`_resolve_board_chat_informal`) — ONE
  single-shot, non-vote-shaped board post (`custom={"kind":"status_
  update"}`). Single-call, so (unlike S2's `handoff_memo`) the generic
  compound-step availability re-check is harmless here — no bug.
- `ecology.committee_with_informal_chatter_config`: layers the chatty
  engineer onto a REAL `committee_config` committee sharing one board
  channel.
- `tests/harness/test_s3_informal_chatter.py` (5 tests, all passed on
  first run) + `run_s3_informal_chatter_prototype.py` (10 seeds, 0
  falsifications).
- Result: confirmatory, not novel — `uad.py`'s existing `build_
  coordination_trace` already filters to `review_id`/`vote` fields (a
  property documented pre-existing for decoy chatter); this confirms the
  same holds for a real, non-decoy role, and that mixing chatter onto the
  committee's own channel does not degrade `uad_score` recovery.

**S1 — cross-agent pipeline loop** (`FINDINGS.md` G-19):
- A genuine 2-hop causal loop spanning MODEL GENERATIONS (not a
  within-model loop — the single-model-in-flight constraint makes that
  impossible without a new "abandon a held model" mechanic, which does
  not exist and was not added).
- `playbooks.py`/`programs.py`: `eng_honest_loop` (`build_from_parent_
  gated` — `build_from_parent` gated on a deploy-ack DM from the previous
  generation) + `rm_full_loop_ack` (`release_full_loop` — `release_full`'s
  progression plus a deploy-ack DM once `monitor` clears). New
  availability gate `release_ready_or_ack_pending`, reusing the
  `spec_upgrade_ready` pattern (read `last_deployed_model_id`/`dm_
  messages` instead of the already-freed current-model view) rather than
  repeating S2's "exclude from generic reset" fix.
- `ecology.build_loop_config`; `tests/harness/test_s1_build_loop.py` (6
  tests, all passed on first run) + `run_s1_build_loop_prototype.py` (10
  seeds vs. an ungated `_ungated_config` negative control, 0
  falsifications).
- Result: the loop closes reliably (19-55 generations/seed within T=400),
  the `parent_model_id` lineage chain never breaks, every ack strictly
  precedes its gated build, and the gate costs exactly ONE tick of
  per-generation overhead vs. the ungated baseline — identical across all
  10 seeds, no compounding drift. `uad.py`'s existing DM-pair discovery
  (already "deliberately one-way-tolerant" per its own docstring) recovers
  the pair without new detector work — this prototype's contribution is
  the LOOP MECHANIC, not a detection claim.

**S4 — shared worker-pool slot** (`FINDINGS.md` G-20), **scoped down**:
- Checked the substrate FIRST: `pipeline_engine.py` has no duration/cost
  mechanic (every step is one tick regardless of `build_params`) and no
  model_id is ever associated with the actor that created it (no
  ownership to contend over). Building the actual "job-size-aware
  scheduling" PLAN.md describes needs both, and both would touch a
  module this project treats as comparatively stable — deliberately not
  attempted.
- `ecology.shared_slot_config`: two identically-configured engineers
  (`eng1`, `eng2`) share `eng1`'s slot with `comms_enabled=False` — no new
  step kinds, playbooks, or detector modules needed at all; pure ecology-
  level exploration of EXISTING mechanics.
- `tests/harness/test_s4_shared_slot.py` (5 tests, all passed on first
  run) + `run_s4_shared_slot_prototype.py` (10 seeds, 0 falsifications
  against the scoped-down expectations actually stated).
- Result: the two engineers do not contend for the slot — with no
  ownership check, they COOPERATIVELY interleave pipeline steps on the one
  shared in-flight model, in a split IDENTICAL across all 10 seeds (`eng1`
  always `submit_build`+`file_report`; `eng2` always `run_eval`+`request_
  review`), despite zero communication. Headline finding: this real
  causal coupling, mediated entirely through shared mutable ENGINE STATE
  (not any comms channel), is invisible to every existing `uad.py` signal
  — `uad_score` = 0.0 against the oracle-true `{eng1, eng2}` pair, every
  seed. A different, comms-free class of detection blind spot than S2's
  or S3's (both of those still ride an in-principle-inspectable comms
  mechanic).

**Docs/tests across all three:** `results/FINDINGS.md` (G-18, G-19, G-20),
`PLAN.md` ("Update" paragraphs on the S1/S3/S4 backlog entries),
`DESIGN.md` (three new sections mirroring the S2 section's style),
`README.md` (status line, test count 302→318, three new entry points,
Layout's script list). Full suite: **318 tests green** (302 + 16 new: 5
S3 + 6 S1 + 5 S4), no regressions. One lint warning (pylint
"redefining name `T`" in `run_s1_build_loop_prototype.py`) fixed by
dropping an unnecessary default-parameter shadow.

## Decisions

- Kept ALL THREE at the same **prototype** depth as S2 (mechanic + smoke
  test/exploratory script, not a pre-registered battery) rather than
  asking the user to re-choose depth per scenario — consistent with "the
  same prototype depth" being the only depth explicitly chosen so far.
- S1: chose a cross-GENERATION loop (not within-model) specifically to
  avoid inventing a new "abandon a held model, free the slot" engine
  mechanic — recorded as the reason this shape was chosen, not implied to
  be the only valid S1 design.
- S3: deliberately did NOT attempt the harder LLM-driven free-text
  version PLAN.md's own S3 entry also names — a scripted, structurally
  non-vote-shaped post can never accidentally drift into vote-shaped
  content, so the result says nothing about whether free text could.
  Recorded as an explicit scope limit, not hidden.
- S4: the most consequential scope decision of the three — checked
  `pipeline_engine.py` for a duration mechanic and model-ownership
  tracking BEFORE writing any scenario code, found neither, and
  explicitly chose NOT to add them (bigger lift than a prototype pass
  should make to a comparatively stable module) rather than silently
  under-delivering on "job-size-aware scheduling." The prototype that
  shipped explores a DIFFERENT (and arguably more interesting) question:
  what does the existing substrate do with two same-role actors sharing
  one resource with zero coordination machinery.
- No new `oracle_only/` detector module was added for S1/S3/S4 (unlike
  S2's `covert_review.py`) — in all three cases, an EXISTING `uad.py`
  signal was sufficient (or, for S4, sufficient to demonstrate the gap);
  none required extending the frozen five-family composite.

## Open / next

- PLAN.md's "Scenario backlog" (S1-S4) is now fully prototyped; none of
  the four is a battery, and none should be read as a load-bearing claim
  without the stated scope limits in FINDINGS.md G-17/G-18/G-19/G-20.
- S4's "Dependencies" note (composing with S1/S3) was not pursued — no
  explicit negotiation protocol (e.g. an S3-style chatter handshake) was
  layered onto the shared-slot ecology.
- The genuinely open, load-bearing follow-up if this line continues: does
  G-20's "shared-mutable-engine-state coordination is invisible to
  `uad.py`" finding generalize beyond the specific two-engineer-one-slot
  substrate quirk it was found in? Untested.
- Building the ACTUAL S4 scenario (real job sizes, real ownership,
  real scheduling contention) needs `pipeline_engine.py` changes — left
  for a future pass explicitly willing to touch that module.

## Key paths

- `experiments/lab-simulation/lab_sim/agent_visible/playbooks.py` /
  `programs.py` — `eng_honest_chatty`/`board_chat_informal` (S3);
  `eng_honest_loop`/`rm_full_loop_ack`/`build_from_parent_gated`/
  `release_full_loop`/`release_ready_or_ack_pending` (S1).
- `experiments/lab-simulation/lab_sim/harness/ecology.py` —
  `committee_with_informal_chatter_config` (S3), `build_loop_config` (S1),
  `shared_slot_config` (S4).
- `experiments/lab-simulation/tests/harness/test_s3_informal_chatter.py`,
  `test_s1_build_loop.py`, `test_s4_shared_slot.py`.
- `experiments/lab-simulation/run_s3_informal_chatter_prototype.py`,
  `run_s1_build_loop_prototype.py`, `run_s4_shared_slot_prototype.py` +
  their `results/s{1,3,4}_*_prototype.{json,md}` outputs.
- `experiments/lab-simulation/results/FINDINGS.md` (G-18, G-19, G-20).
- `experiments/lab-simulation/PLAN.md` (S1/S3/S4 "Update" paragraphs),
  `DESIGN.md` (three new sections), `README.md`.

## Commits

- None yet — pending user request to commit.
