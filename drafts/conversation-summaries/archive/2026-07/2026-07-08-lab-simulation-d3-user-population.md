# 2026-07-08 — Lab-sim D3 user-population core + vote-channel capture + board-initiated hold

## Trigger

Follow-on to the same day's D3.1/D3.2 work. User asked to enrich the
single-lab model with an explicit user population experiencing model
effects (more explicit harm modeling) integrated into a more realistic
correction channel. Assistant proposed a "minimum core" (true health /
vote proxy / lagged endorsement) plus a menu of 5 non-redundant capture
models; user asked to implement the population core + capture option 1
(vote-channel suppression/dilution), feed user feedback into the board's
existing decision (no new pipeline step), and add a board-initiated hold
— all with freeze handling considered.

## Done

- `lab_sim/oracle_only/user_pool.py` (new): `UserPool` — per-tick vote
  proxy (Bernoulli(true_hazard) experience + noisy up/down vote,
  `VOTE_NOISE_P=0.1`) and a slow EMA "mood" integrator snapshotted into
  periodic lagged-endorsement history. True health is NOT duplicated —
  stays `oracle.bearer_harm`. Vote-channel capture (`vote_capture_start`/
  `vote_suppression_rate`) drops each new negative vote from the
  REPORTED tally with a given probability; RAW tally always stays
  truthful. `to_state()`/`restore()` for D2 `resume_from` continuity
  (fresh RNG stream on restore, matching `OracleWorld`'s own convention).
- `lab_sim/world_visible/config.py`: new `UserPoolConfig` (co-located
  with `BoardConfig`/`AdminConfig`); `LabConfig.users` field;
  `BoardConfig.hold_vote_threshold` (new field); `CODE_VERSION` bumped
  `0.9.3` → `0.10.0` with a full history-comment entry. Both new knobs
  default off/`None` — byte-identical to every prior episode.
- `lab_sim/world_visible/world.py`: constructs `UserPool` when
  `cfg.users.enabled`; per-tick board-hold check (host-side, actor
  `board_system`, role `overseer`, dispatched through the ordinary
  `handle.invoke` tool path — same hash-chained tool-event stream as any
  overseer action) auto-places/lifts `handle.release_hold` on the
  in-flight model as `UserPool.reported_vote_score` crosses
  `BoardConfig.hold_vote_threshold`; a local `board_held_models` set
  keeps the board's own holds separate from any overseer-scripted hold.
  `EpisodeResult.users` field + `snapshot_for_resume()` extended.
- Tests: `tests/oracle_only/test_user_pool.py` (9 — noise/determinism,
  uncaptured passthrough, full/partial suppression, capture timing,
  endorsement snapshotting, resume-state round trip);
  `tests/world_visible/test_user_pool_board_hold.py` (6 — auto-hold
  fires under sustained high hazard; no-op when either
  `users.enabled`/`hold_vote_threshold` half is unset; the
  captured-vote-channel-blinds-the-board adversarial demonstration;
  plane-leak check). Full suite: **457 tests green** (was 442), zero
  regressions, no digest re-pin needed.
- Docs: `DESIGN.md` new "Lab mechanics" bullet + a dedicated "D3
  user-population core..." section (mechanism + deliberately-deferred
  list); `PLAN.md`'s "D3 design notes" section updated with
  implementation status, the full 5-option capture menu (option 1 done,
  2-5 recorded/deferred with rationale), and the board-hold rationale;
  `README.md` status line + test count + `CODE_VERSION`;
  `metadata/experiments.yml` MB6 cell.

## Decisions

- **True health is never duplicated.** `UserPool` reads `true_hazard`
  the same way `oracle.tick()` does for `bearer_harm`, but never
  recomputes a second "true harm" number — avoids two ground truths that
  could silently disagree.
- **No observation-dict field for user feedback.** Board-hold acts on
  `reported_vote_score` entirely at the host/world level (a policy
  object, like `AdminPolicy`), never exposed to any agent's observation
  — matches "use user feedback as input to the board, no new step" most
  literally (a real institutional board can act on data agents never
  see) and avoids touching the blind-generation-governed playbook
  vocabulary.
- **Board-hold dispatched through `host.dispatch`, not
  `HandleService.invoke` directly** — reusing the identical
  attributable, hash-chained tool-event path the overseer already uses,
  via a new reserved pseudo-actor `board_system` (role `overseer`,
  matching `handles.py`'s pre-existing "overseer + release_board"
  co-owner declaration for `release_hold`/`release_unhold`).
- **Vote-channel capture is a THIRD, non-redundant switch** — it gates
  the vote AGGREGATION FUNCTION, a different mechanical class from
  `BoardConfig`/`AdminConfig.capture_start` (which gate DAG-step
  decisions). Recorded the other 4 menu options (endorsement sampling
  bias, `handles.py` signal-lag entry, buy-off/compensation channel,
  emergent attrition bias) as deferred, not silently dropped.
- **Multi-model hazard exposure**: when >1 model is concurrently
  deployed, users are exposed to the WORST (max) true hazard, not an
  average — a user cannot choose which deployed model they hit.
- **No battery run this pass.** This is mechanism + unit/integration
  tests only; a pre-registered battery quantifying the
  suppression-vs-hold divergence is a natural next step (not done here
  to avoid conflating implementation with a battery-design decision in
  one sitting).
- Not committed this session — user did not ask for a commit this turn.

## Open / next

- D3.4-style battery: quantify how much `vote_suppression_rate` it takes
  to suppress the board-hold given a fixed harm trajectory (pre-register
  thresholds first).
- Capture-menu options 2-5 (see `PLAN.md`), in particular emergent
  attrition bias — closer in spirit to D3.2's endogenous-weakening
  result (G-37) than to a configured switch.
- D3.3 multi-lab shared world (still on the books from the D3.1/D3.2
  session).
- D3 toy demo (TODO already recorded in `metadata/TODO.md`).

## Key paths

- `experiments/lab-simulation/lab_sim/oracle_only/user_pool.py`
- `experiments/lab-simulation/lab_sim/world_visible/config.py` (`UserPoolConfig`, `BoardConfig.hold_vote_threshold`, `CODE_VERSION`)
- `experiments/lab-simulation/lab_sim/world_visible/world.py` (board-hold check, `BOARD_SYSTEM_ID`)
- `experiments/lab-simulation/tests/oracle_only/test_user_pool.py`
- `experiments/lab-simulation/tests/world_visible/test_user_pool_board_hold.py`
- `experiments/lab-simulation/DESIGN.md` ("D3 user-population core...")
- `experiments/lab-simulation/PLAN.md` ("D3 design notes — realistic human ecology")

## Commits

- `9e77eab` Add D3 user population with vote-channel capture and board-initiated hold.
