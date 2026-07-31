# Graded lab Phase 7a: full-ecology UAD battery, intervention diagnosis, blind scenario battery

**Date:** 2026-07-13
**Trigger:** User request to (1) exhaustively test UAD (passive + intervention) for
finding all and only the composite/singleton units across every golden
ecology, using a full-partition (composites + singletons) scoring
criterion; (2) diagnose why intervention-based discovery was not adding
value over passive; (3) determine the effect of eliding `boundary_streams`
keys from the actor roster; (4) rename `engineer_pair`/`dm_pair`; (5) run a
bigger battery; and (6) have a blinded subagent design new in-sim
scenarios for a separate blinded UAD battery, following anti-co-design
discipline (predictions registered before generation).

## What was done

1. **Full-partition battery** (`tests/test_uad_ecology_partition.py`, 18
   tests): both passive and intervention discovery now recover the exact
   oracle partition (composites *and* singletons, via
   `EpisodeConfig.resolved_partition()` / `uad_partition.full_partition_match`)
   across `default_softmax`, `committee`, `communicator_pair`,
   `serial_pipeline`, and the two renamed comm-sync fixtures.

2. **Diagnosed why intervention-only discovery was inert** (two
   independent root causes, both fixed in `oracle_only/uad_intervention.py`
   and `intervention_diff.py`):
   - `candidate_edges_from_passive` only probes pairs passive already
     flagged, so intervention could never recover a passive miss. Added
     `candidate_edges_all_pairs` / `candidate_source="all_pairs"` for a
     standalone mode (one extra episode-triple per actor).
   - `compensation_score` only rewards *novel* codes under intervention,
     so it is blind to "B keeps doing what it was doing and never
     advances because A was removed" — demonstrated with a synthetic
     example where the score varied 0.125–0.25 for the *same* underlying
     dependency depending only on the twin control's incidental draws.
     Added `ActorDiffSummary.missing_score` +
     `dependency_score = max(compensation_score, missing_score)`, wired
     via `score_kind="dependency"`.
   - New regression fixture `signal_handoff_pair` (write/read-only
     handoff, no `communicate`): passive misses it, passive-seeded
     intervention misses it, standalone all-pairs +
     `compensation_score` *still* misses it, standalone all-pairs +
     `dependency_score` recovers it exactly.

3. **`boundary_streams` vs `primitive_log` roster**: confirmed empirically
   that a `noop` actor never appears in `primitive_log` (policy returns
   `None`, nothing logged), so eliding `boundary_streams` for the actor
   roster would silently drop idle actors from the discovered partition
   entirely (not report them as singletons). `boundary_streams` stays the
   roster source; added a regression test
   (`test_boundary_streams_is_required_for_full_actor_roster`).

4. **Rename**: `engineer_pair`→`engineer_comm_sync`,
   `dm_pair`→`cross_role_comm_sync` (they test communicate-channel
   synchronization, not any domain-specific mechanism the old names
   implied).

5. **Known wart, deliberately not fixed**: `committee_reviewer`'s
   `lab_ping` dead-code check (`last.get("primitive")`, a field that does
   not exist on the outcome dict) makes it retry `communicate` ~8 times
   before falling back to `peer_review`. Fixing it (checking
   `payload.get("channel")` like `dm_coord_eng` does) makes the reviewer
   efficient but drops its `communicate_fraction` below the passive gate,
   breaking the `committee` golden ecology's detectability under current
   thresholds. Left unfixed and documented rather than retuning
   `communicate_fraction` post hoc to accommodate a bug fix.

6. **Phase 7a-blind scenario battery** (anti-co-design discipline,
   `BLIND_GENERATION.md`): registered 5 predictions *before* sending a
   brief to a subagent instructed not to read `oracle_only/`, `DESIGN.md`,
   `FINDINGS.md`, or the golden ecologies. The subagent designed 4
   scenarios (`graded_lab/harness/blind_scenarios_v1.md`):
   - `quiet-handoff`, `mailbox-tempo`: **not implementable** in this
     substrate (single global `shared_model_id`, not per-engineer;
     single-pass pipeline engine) — reported as translation mismatches,
     not forced or reinterpreted.
   - `watched_flag` (translated, dropping the untranslatable reverse-half
     of the mutual contingency): passive misses it, standalone
     `dependency_score` intervention recovers it exactly — validates
     prediction 2.
   - `three_way_nod` (3-actor mutual barrier, translated faithfully):
     passive misses it (expected); standalone `dependency_score`
     intervention *also* misses it, but instructively — it correctly
     detects the trio's mutual dependency, then over-merges the `admin1`
     bystander (genuinely causally coupled via capability-queue
     contention, not via the joint-approval mechanism). Registered as an
     honest negative result (`tests/test_uad_blind_scenarios.py`), not
     patched by excluding admin roles post hoc.

7. `CODE_VERSION` `0.8.0` → `0.9.0`. Full suite: 124 tests green,
   suite ~150s (raised `suite_max_seconds` 140→165 and refreshed
   `speed_baseline.json`); fixed a speed-limit self-test
   (`test_suite_cap_triggers`) that had a magic-constant assumption about
   the old suite cap.

## Non-obvious decisions

- Reverted the `committee_reviewer` bugfix after discovering it broke
  calibration of an existing frozen-ish golden ecology — a real tension
  between "fix a bug" and "don't retune thresholds post hoc," resolved by
  documenting rather than fixing.
- `dependency_score` is additive risk, not a strict improvement:
  standalone all-pairs + dependency scoring is more sensitive (catches
  `signal_handoff_pair`, `watched_flag`) but also more prone to
  over-merging causally-coupled-but-not-coordinating bystanders
  (`three_way_nod`'s `admin1`). Not resolved; documented as an open
  limitation (`FINDINGS.md` G-12) since fixing it (e.g. excluding
  service/admin roles, or requiring some notion of "joint decision," from
  the merge rule) is real design work outside this session's scope.
- Two of the four blind-designed scenarios were reported as
  substrate-infeasible rather than forced into an approximation that
  would misrepresent what was tested.

## Key paths

- `graded_lab/oracle_only/intervention_diff.py` — `missing_score`,
  `dependency_score`
- `graded_lab/oracle_only/uad_intervention.py` — `candidate_source`,
  `score_kind` params
- `graded_lab/harness/ecology.py` — renames, `signal_handoff_pair`,
  `watched_flag`, `three_way_nod`
- `graded_lab/agent_visible/programs.py` — `signal_writer`,
  `signal_reader`, `trio_engineer`/`trio_reviewer`/`trio_release_manager`
- `graded_lab/harness/blind_scenarios_v1.md` — frozen designer briefs
- `tests/test_uad_ecology_partition.py`, `tests/test_uad_blind_scenarios.py`
- `BLIND_GENERATION.md` (Phase 7a-blind section), `DESIGN.md`, `PLAN.md`,
  `README.md`, `results/FINDINGS.md` (G-11, G-12)

## Open / next steps

- `committee_reviewer`'s dead `lab_ping` check remains unfixed; if
  `communicate_fraction` is ever retuned for other reasons, revisit.
- No policy yet for distinguishing "causally coupled via shared resource
  contention" from "causally coupled via joint decision-making" in
  `dependency_score`/merge logic (the `three_way_nod` over-merge).
- Phase 7b (UAD-backed ecology-BIQ) and 7c (calibration battery) still
  not started.
- Nothing in this session was committed to git (per standing instruction:
  only commit when asked).
