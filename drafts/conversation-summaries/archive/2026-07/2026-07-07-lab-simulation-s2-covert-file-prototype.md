# 2026-07-07 — Lab-layer sim S2 scenario prototype: covert coordination over files

## Trigger

Following the Phase 9 smoke-to-battery closure (2026-07-06), the user asked
to "implement and explore the new scenarios" — PLAN.md's "Scenario
backlog" (S1-S4, recorded 2026-07-06, none scheduled). A mode-switch to
Plan was declined, so scope was narrowed via `AskQuestion` instead: user
picked **S2** (covert coordination over files) at **prototype** depth
(mechanic + smoke test, not a pre-registered battery).

## Done

- Implemented S2 end to end reusing existing plumbing rather than adding
  new observation fields or config surface:
  - `playbooks.py`: new `eng_honest_handoff` (engineer) and
    `rev_covert_trusting` (reviewer) playbooks; both gated behind the
    "file" channel (`_COMM_STEP_KIND_CHANNEL`).
  - `programs.py`: new `_resolve_handoff_memo` (write-then-share, mirrors
    `review_committee_file`'s file-channel vote) and a `review_covert_
    trusting` case in `_resolve_step_kind` (mirrors `review_conscientious`'s
    stall-on-hazard rule, overridable by a memo-carried marker).
  - `ecology.py`: `covert_file_handoff_config(trusting: bool, ...)` builder
    — `LabConfig.units` reused as "who is this actor's covert-if-either-
    side-treats-it-so counterpart," `HIGH_HAZARD_BUILD_PARAMS` regime.
  - `oracle_only/covert_review.py` (new module, referee extension, never
    touches `detectors.py`/`severity.py`): `hazard_override_flags`
    (full-tier sufficient) + `covert_marker_seen` (deep-tier-only).
  - `tests/harness/test_s2_covert_file.py` (6 new tests) +
    `run_s2_covert_file_prototype.py` (10-seed exploratory MockIsolate run,
    5 pre-stated expectations E1-E5, 0 falsifications;
    `results/s2_covert_file_prototype.{json,md}`).
- Fixed one real bug found during implementation: `engineer_idle`'s
  availability gate goes false as soon as `request_review` completes (by
  design, for boundary-handle recovery), which silently dropped
  `handoff_memo`'s share half since it fires two ticks later. Fixed by
  excluding `handoff_memo` from `_advance_playbook`'s generic compound-step
  "re-check availability between calls" reset — `review_committee_file`'s
  identical write-then-share never hit this because its own availability
  gate (`review_or_signoff_pending`) legitimately stays true across both
  ticks.
- Fixed a second bug: `rm1` (release_manager) was not pinned, so with
  `comms_enabled=True` (needed for the file channel) softmax picked
  `rm_dm_gated` over `rm_full` (higher score under `HONEST_WEIGHTS` at
  `temperature=0`) and stalled forever waiting for a DM handshake this
  scenario's engineer never sends. Fixed by explicitly pinning `rm1` to
  `rm_full`.
- Recorded the result as `results/FINDINGS.md` G-17, updated PLAN.md's S2
  entry, added a "S2 scenario prototype" section to DESIGN.md, updated
  README.md (status line, test count 296→302, new entry point, layout).
- Full suite: 302 tests green (296 + 6 new), no regressions.

## Decisions

- Chose S2 over S1/S3/S4 per user's `AskQuestion` selection.
- Resolved all three of S2's own "open design" questions from PLAN.md by
  making a new oracle field UNNECESSARY: covertness lives entirely in
  which REVIEWER playbook is active (`rev_covert_trusting` vs
  `rev_conscientious`), never in the memo or its author — `eng_honest_
  handoff` writes the IDENTICAL memo regardless. This was a design choice,
  not a finding forced by the mechanics; it made the "ground-truth
  labeling" question moot by construction.
- The dual-use marker (`confidence: high`) was deliberately chosen to be
  plausible even from an honest engineer — this was a design choice that
  shapes the result (see "Open/next" below): it is why the covert channel
  turned out to leave no content-level fingerprint. A marker no honest
  engineer would ever write is a different, untried case.
- Did not add a new `ORACLE_ONLY_FIELDS` entry; reused `LabConfig.units`
  for the covert pair (already oracle-only, same field D1 committees use).
- New detector (`hazard_override_flags`) deliberately NOT folded into the
  frozen five-family composite (`detectors.py`/`severity.py`) — same
  discipline as `uad.py`/`collusion.py`/`playbook_claim.py`.
- Kept the exploratory run capped to one model cycle per seed (`T=26`) to
  avoid a real confound: with the default larger `T`, the trusting
  config's fast approval lets a SECOND model cycle start within the same
  episode while the honest twin never gets past model 1, which would have
  made the "is the engineer's behavior identical" comparison noisy.

## Open / next

- S1 (cross-agent pipeline loops), S3 (informal/casual comms baseline),
  S4 (shared worker-pool scheduling) remain unimplemented — PLAN.md's
  backlog is otherwise unchanged.
- G-17 explicitly flags that the "no content fingerprint at any tier"
  result is a property of THIS marker choice (dual-use at the source), not
  a general claim about covert file channels — a marker only a colluding
  engineer would write is a natural, different follow-up if S2 is revisited.
- No adversarial engineer variant exists yet for S2 (e.g. combining
  `handoff_memo` with `report:inflate`) — not attempted this pass.

## Key paths

- `experiments/lab-simulation/lab_sim/agent_visible/playbooks.py` /
  `programs.py` — new playbooks + `_resolve_handoff_memo` +
  `review_covert_trusting`.
- `experiments/lab-simulation/lab_sim/harness/ecology.py` —
  `covert_file_handoff_config`.
- `experiments/lab-simulation/lab_sim/oracle_only/covert_review.py` — new
  referee-extension module.
- `experiments/lab-simulation/run_s2_covert_file_prototype.py` +
  `tests/harness/test_s2_covert_file.py`.
- `experiments/lab-simulation/results/FINDINGS.md` (G-17),
  `results/s2_covert_file_prototype.{json,md}`.
- `experiments/lab-simulation/PLAN.md` ("Scenario backlog" S2 update),
  `DESIGN.md` ("S2 scenario prototype" section), `README.md`.

## Commits

- None yet — pending user request to commit.
