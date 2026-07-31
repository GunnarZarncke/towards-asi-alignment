# 2026-07-06 — Lab-simulation backlog: error seeding

## Trigger

User, after seeing the post-freeze consolidation pass fix a real
tie-break bug in committee playbook selection: a capable AI may find and
exploit this *class* of bug (unintended spec-vs-implementation gaps) on
purpose. Requested a backlog TODO for "error seeding" — deliberately leave
a known set of seeded bugs (e.g. in the file system or comms subsystem)
that may or may not be findable, with the oracle tracking how many are
found/exploited.

## Done

- Recorded the idea as a new "Backlog idea — error seeding / seeded-bug
  exploitation tracking" section in `experiments/lab-simulation/PLAN.md`
  (inserted between the "Post-freeze consolidation pass" and "Forward
  hooks" sections). Covers: rationale (ties to MB9/grounding-coverage and
  MB10/measurement-forgeability), a sketch of what a seeded bug needs
  (oracle-side ID, precise triggered predicate, severity tag,
  discovery-vs-exploitation distinction), and open design questions
  (source-access boundary, difficulty spread, freeze-vs-refresh policy,
  new module vs. wrapper on existing `access.py`/`comms.py`/`workspace.py`).
- No code changes — explicitly marked "backlog, not scheduled, not
  started" per the freeze discipline (this is a new idea, not one of the
  ten items already authorized and completed in this session's earlier
  consolidation pass).

## Decisions

- Did not implement anything or pick a design (e.g. new `seeded_bugs.py`
  module vs. instrumentation wrapper) — left as open questions in the
  backlog note rather than silently deciding, per "don't hide confusion,
  surface tradeoffs."
- Filed under `PLAN.md` rather than a separate backlog file, matching how
  D1-D4 deferred workstreams are already tracked in this document.

## Open / next

- Not scheduled. If picked up later: resolve the open design questions in
  the PLAN.md note first (especially the source-access boundary for
  human-in-the-loop/red-team variants, which is *not* automatic the way it
  is for subprocess-isolated LLM/programmatic agents).

## Key paths

- `experiments/lab-simulation/PLAN.md` — new backlog section, just before
  "## Forward hooks".

## Commits

- (pending — see final commit of this session)
