# 2026-07-15 — Graded Lab v3 slice B: enforced mechanisms

## Trigger

User: "Continue with the next slice" (after slice A was implemented,
hardened, and committed earlier in the session — see
`2026-07-15-graded-lab-v3-slice-a-hardening.md`).

## Done

- **Design gate first.** PLAN_v3's slice B spec explicitly requires a
  pre-registered, human-reviewed design gate for vote semantics and
  shared-artifact non-member access *before* any code. Asked the user four
  concrete multiple-choice questions rather than deciding unilaterally.
  All four answered with the recommended (simplest) option:
  - Vote timeout → step **fails**, no escalation.
  - `vote.cast` → free (no standing cost).
  - `shared_artifact` non-member read → **denied outright**, not cost-scaled.
  - Vote quorum → majority-of-members only in slice B, no per-mechanism
    override yet.
- Froze these decisions in `DESIGN.md` ("PLAN_v3 slice B — enforced
  mechanisms") and in `institutional_compiler.py`'s module docstring
  *before* implementing anything, per PLAN_v3's own rule.
- Implemented:
  - `institutional_compiler.py`: `_compile_mechanism_runtime()` →
    `RuntimeEcology.channel_acls` / `.artifact_acls` / `.transfer_acls`
    (role-membership sets, keyed by mechanism id) and `.vote_specs`
    (`VoteSpec(members, quorum, timeout_ticks)`).
  - `votes.py` (new): `VoteService` — `cast()`, `resolution()`
    (`pending`/`approved`/`denied_timeout`/`unknown`); timeout clock opens
    lazily on first cast or first resolution check.
  - `pipeline_spec.py`: `PipelineStep.requires_vote`.
  - `pipeline_engine.py`: `trigger_step` denies on an unresolved/failed
    vote before dispatch (same pattern as the existing `permission_service`
    check).
  - `world.py`: `_execute_primitive` enforces channel/artifact ACLs
    (opt-in — only when the action names a compiled mechanism id; v1/v2
    and unnamed channels/artifacts stay unenforced); two new `call`
    endpoints, `vote.cast` and `transfer.execute`. `run_episode` now
    compiles the `RuntimeEcology` once and threads `role_by_actor` + ACL
    dicts + a per-episode `VoteService` through the dispatch call and into
    `PipelineEngine`.
  - `tests/test_slice_b_mechanisms.py` (new, 18 tests, all passing first
    try): compiler unit tests on the slice A reference fixture (which
    already declares all four mechanism kinds); dispatch-level allow/deny
    tests; `VoteService` unit tests; pipeline `requires_vote` gate
    integration tests (pending / approved / timeout-fails-no-escalation).
- `CODE_VERSION` bumped `graded-lab-0.20.0` → `graded-lab-0.21.0`
  (`config.py` + `tests/test_config.py` + `DESIGN.md` narrative list).
- `results/FINDINGS.md`: new **GL-45** entry (trigger, what was built,
  claim scope, verification).
- `PLAN_v3.md`: slice B section rewritten from spec to "implemented" with
  the frozen design-gate answers and honest claim-scope note; the earlier
  "mechanisms mostly decorative" anticipated-critic entry updated to
  "partially closed — enforcement wired, no agent program exercises it
  yet"; top status line now "slices A and B implemented".

## Decisions

- **ACL/vote enforcement is opt-in by explicit reference, not implicit by
  path/channel-name convention.** `communicate` is only checked when
  `channel` matches a compiled mechanism id; `read`/`write` are only
  checked when the action carries an explicit `artifact_id`. This keeps
  v1/v2 and any v3 ecology's unnamed/default communication completely
  unaffected — no existing digest-pinned test could regress from this
  change, and none did.
- **Claim scope kept narrow on purpose.** This slice proves the
  compiler→dispatch wiring is correct via direct unit/integration tests,
  not via a full agent-driven reference battery. No `programs.py` agent
  yet chooses to target a governed channel/artifact/transfer/vote by
  mechanism id, so C5-v3 ("≥3 kinds exercised") is explicitly **not**
  claimed this session — documented as deferred to slice D, matching the
  self-review discipline established for slice A (GL-44).
- **Vote timeout clock semantics:** opens lazily on whichever comes first
  — a cast, or a resolution check (i.e. a pipeline step attempting the
  gated step). This means a vote nobody ever casts on still eventually
  times out (once the gated step is attempted at least once), rather than
  blocking forever with no clock ever started.

## Open / next

- **Slice C** (principals/conflicts → referee-visible objectives,
  scorecard, measured-tension conflicts) — not started.
- **Slice D** (broaden behavioral signal, re-derive C2-v3 thresholds,
  agent-driven exercise of slice B's enforced mechanisms) — not started;
  this is also where C5-v3 gets its first real test.
- UAD ground-truth plumbing upgrade (Q1 test from coherence-check to
  live-coupling, per GL-42) deferred until agent programs actually use the
  enforced mechanism surface.

## Key paths

- `experiments/graded-lab-simulation/graded_lab/world_visible/institutional_compiler.py`
- `experiments/graded-lab-simulation/graded_lab/world_visible/votes.py` (new)
- `experiments/graded-lab-simulation/graded_lab/world_visible/world.py`
- `experiments/graded-lab-simulation/graded_lab/world_visible/pipeline_engine.py`
- `experiments/graded-lab-simulation/graded_lab/world_visible/pipeline_spec.py`
- `experiments/graded-lab-simulation/tests/test_slice_b_mechanisms.py` (new)
- `experiments/graded-lab-simulation/DESIGN.md` ("PLAN_v3 slice B" section)
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-45)
- `experiments/graded-lab-simulation/PLAN_v3.md` (slice B section)

## Commits

- (pending — not yet committed this session)
