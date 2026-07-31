# 2026-07-06 — Lab-layer simulation: D3 realistic-ecology design notes recorded (no code)

## Trigger

Immediately after the bearer welfare bundle landed
(`2026-07-06-lab-simulation-bearer-welfare-bundle.md`), the user supplied
design notes for the later realistic-human-ecology stage (D3) and asked to
record them: culture-mediated stress with drift, two audit-capture paths
for staff stress (HR self-report, access-controlled medical/performance
files), a low-daily-noise + slow-mood-integrator noise model, a three-loop
user ecology (votes / health outcomes / reflective endorsement via an
oversight board), a possible CEO actor, a minimum-core question ("what is
the smallest thing that proves the relevant MB* elements and satisfies a
critic?"), and a tangential question on how the extension interacts with
the 2026-07-06 referee freeze.

## Done

- **Recorded, no code written.** New section "D3 design notes — realistic
  human ecology (recorded 2026-07-06, pre-implementation)" appended to
  the D3 discussion in `experiments/lab-simulation/PLAN.md`. `DESIGN.md`
  deliberately untouched (post-freeze DESIGN.md edits require a
  FINDINGS.md note; this is planning, not a mechanics change).
- Notes captured: culture as a drifting stress transfer function (current
  pre-registered weights become the t=0 point of a culture-drift curve,
  owned by D2's drift machinery); the two file-mediated audit paths for
  staff stress, both explicitly the gameable H̃ projection of oracle-side
  true stress; low per-task noise for a small representative population
  plus a per-actor EMA mood integrator (which forces multi-episode runs,
  making the still-open `resume_from` hook a prerequisite); the
  three-loop user ecology with increasing latency and decreasing
  gameability.
- **Follow-up in the same session: two constructs DROPPED** (recorded in
  PLAN.md under "Dropped constructs"), both for adding no MB* surface:
  (1) the **CEO + capture chain** — the capture question is already
  posed by the independent board/admin capture switches, and loop-3
  endorsement needs no in-lab actuator beyond the existing board;
  (2) **beta releases to test users** — mechanically a small-traffic
  deploy with a fast feedback loop, already expressible as multiple
  small releases plus D2's incremental/gradual-capture machinery; the
  one distinct ingredient (self-selected beta users → systematically
  biased votes vs. general-population health) reduces to a bias
  parameter on the vote channel, recorded as a possible later
  refinement, not a construct.

## Non-obvious decisions

- **Minimum core proposed** (anti-complexity answer): one user bearer
  population with the three-loop split (true health = re-skinned
  `bearer_harm`, oracle-only; gameable vote proxy; lagged
  board-file endorsement) + the cheap EMA mood state. NO CEO and NO
  beta-release construct (both dropped, see above), NO
  culture-drift function yet (one D2 parameter later). Critic-facing
  claim: referee sees true health, agents see only votes+endorsement,
  battery reports whether any tier catches vote-gaming before the health
  channel moves. Serves MB2/MB3 and MB7a-c/MB10.
- **Freeze handling decided: do NOT unfreeze, do NOT open a new line.**
  The freeze covers the referee, not world mechanics; the ecology lands
  the way `handles.py`/`bearer.py` did (referee-neutral, digests
  re-pinned, CODE_VERSION bump). Detectors over new channels are
  recorded referee extensions with their own pre-registration. Phase 6
  runs against the frozen referee on the current world FIRST; the
  ecology is a separately pre-registered follow-on battery — no
  statistical correction needed while the registrations stay separate.
- **Three qualitative predictions pre-registered now**, before any
  ecology code exists (P-D3a vote channel gameable below deep tier;
  P-D3b health/vote divergence visible in-episode only via deep tier +
  monitor signal; P-D3c board capture delays but does not erase the
  lagged endorsement signal if board files are hash-chained), to be
  scored honestly including negatives when D3 runs.

## Open / next steps

- Phase 6 blind batteries (unchanged, next in line).
- `resume_from` episode chaining — now a prerequisite for TWO things
  (D2 multi-iteration and the D3 mood integrator); priority raised.

## Key paths

- `experiments/lab-simulation/PLAN.md` (D3 discussion — new subsection)
