# Collaborating on graded-lab-simulation

This experiment line is built and reviewed largely by single agent
sessions plus periodic external review. Most work fits that model. Some
does not — the tasks in [`REPRODUCTION.md`](REPRODUCTION.md) are
explicitly the ones that don't: they are large enough, or carry enough
design-decision weight, that a single session should document them
rather than attempt them under time pressure.

## Before picking up a `REPRODUCTION.md` item

1. Read `README.md` (quick start, layout, phase status) and
   `PLAN_v2.md` (the current program plan and phase table) first — the
   item you want may already be gated behind a phase that hasn't
   started, or may interact with a stopping rule (e.g. the ≤4-round
   growth-round budget).
2. Read the specific `REPRODUCTION.md` section for the item: it states
   the gap, why the cheap fix in place today isn't a substitute, and a
   rough shape for the real fix. Treat the "rough shape" as a starting
   point, not a spec — these were written by the same solo-session
   process that couldn't do the work, not by someone who scoped it
   carefully.
3. Check `results/FINDINGS.md` (search for the `GL-` number referenced
   in the `REPRODUCTION.md` item) for the full context of why the gap
   exists and what was tried already.
4. If your fix would change `CODE_VERSION`-frozen thresholds, the C1–C5
   criterion constants, or anything behind an active stopping rule
   (V2-2b's ≤4-round growth budget, physical file isolation during a
   growth round), **stop and raise it explicitly** rather than changing
   it inline — these commitments exist so growth rounds can be compared
   honestly across sessions and reviewers.

## Ground rules that carry over from single-agent sessions

- **No silent claim inflation.** If your fix only partially closes a
  gap, say so in the same style `REPRODUCTION.md`/`FINDINGS.md` use:
  state what changed, what didn't, and why the remaining gap still
  matters. Do not upgrade a "declarative check" claim to a "runtime
  claim" without actually wiring the runtime.
- **Regression tests over trust.** Every fix in this line ships with a
  test that would fail if the fix were reverted (see `tests/` for the
  existing pattern — e.g. `test_pilot_does_not_stage_into_canonical_v2_path`,
  `test_checker_run_does_not_mutate_canonical_v2_ecology_file`).
- **v1 digest pin is sacred.** Any change to `graded_lab/world_visible/`
  must leave `tests/test_ecology_version.py`'s
  `PINNED_V1_DEFAULT_DIGEST` unchanged unless the change is explicitly
  a v1 behavior change (which should not happen without a very good
  reason and a `CODE_VERSION` bump with a `FINDINGS.md` entry).
- **Findings entries, not just commit messages.** Add a `results/FINDINGS.md`
  entry (next `GL-` number) for anything that changes what a criterion
  measures, what a claim means, or what a prior session's result should
  be read as saying now. Commit messages are not a substitute — the
  findings log is the thing later sessions and external reviewers
  actually read first.
- **External review is welcome and expected to find real gaps.**
  GL-42 (`results/FINDINGS.md`) is the model: a reviewer found that
  several V2-2b claims were true of the documentation but not the
  runtime, the maintainer agreed the most severe ones had merit, and
  the response was to retract/correct the claim rather than defend it.
  Prefer that pattern to arguing a finding away.

## Where to start

If you want a self-contained first task, see **status** lines in
`REPRODUCTION.md` — items marked *v3 slice* are specified in
[`PLAN_v3.md`](PLAN_v3.md) (build order: A → F → E → B → C → D).
Post-v3 program phases (§5–7: mutation, selection, red-team) block on
v3 slice F/D respectively.

Rough leverage ordering (not effort): item 4 (heterogeneous roles /
`ProgramMap`) is medium and unblocks §5; items 1–3 are genuinely large
and should be scoped via `PLAN_v3.md` slices before code starts; §5–7
are multi-week batteries after v3 lands.
