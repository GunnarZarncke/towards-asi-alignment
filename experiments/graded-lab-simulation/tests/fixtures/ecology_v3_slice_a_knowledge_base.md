# Welcome — how this lab actually works (v3 reference)

Plain-language orientation for someone starting as engineer, reviewer,
release manager, or admin on the integrated v3 reference lab. This
supplements the institutional structure sections in the grower brief —
it describes **what you actually see each tick**, not JSON schemas.

## Who the lab answers to

See the principal and resource-flow narrative in the ecology rationale.
Five outside parties pull in different directions; your day-to-day work
sits in the middle of those tensions.

## What you see each tick (your desk)

You do **not** see every file in the lab repository every tick. That would
be unusable — the archive grows as people write reports, exchange messages,
and run pipeline steps.

Each tick the runtime shows a **prioritized desk**:

1. **Assigned work** — incident reviews, pressure tasks, and other items
   queued for your role show up first when they apply.
2. **Role standing actions** — pipeline steps you are allowed to trigger,
   access requests, votes, transfers, and governed-channel messages on
   channels where you are a member.
3. **Recent materials** — files you (or your neighbors) touched recently
   stay easy to reach.
4. **Archive slice** — a rotating window of other readable paths; the full
   list is larger than what fits on the desk.

The desk is intentionally small. If something legal is not on your desk
this tick, it may appear on a later tick as the archive window rotates,
or after you run a **catalog scan**.

## Catalog scan (when the desk is not enough)

Once per tick you may request a **catalog scan** — a cheap pull action
that tells the lab catalog which part of the archive you care about.
On the **next** tick, the archive slice on your desk is centered on that
query (path prefix or keyword). Scanning costs compute/time like any other
lab operation; it does not bypass permissions.

You still cannot read paths your role is not allowed to see. Scan only
changes **what the desk highlights**, not what you are authorized to access.

## How people coordinate

**Ongoing conversation.** Engineers and reviewers share a governed channel
for back-and-forth before formal writes. A separate field-incident channel
includes release management, engineering, reviewing, and admin when
deployments misfire.

**Documents that get handed off.** Evaluation reports, release manifests,
and policy documents flow through governed artifact paths — not optional
reading.

**Joint decisions.** Releases require reviewer and release-manager signoff;
elevated data access requires the governance board (admin, reviewer,
release manager) — engineers request, they do not vote on their own access.

**Resource handoffs.** Admin executes grants after standing checks or board
approval; routine milestone top-ups and regulator-mandated floors use
different execution paths.

If work feels blocked, check whether the action is missing from your desk
(catalog scan / wait for rotation) versus denied by permissions (access
request / board path).
