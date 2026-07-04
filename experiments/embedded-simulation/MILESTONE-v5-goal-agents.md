# Milestone v5 — Goal-driven agent ecology (planned, not started)

**Status:** PLANNED. Nothing in this doc is implemented; recorded per user request
("write this plan down") before any code changes. Do not treat any number below
as measured — this is a design doc, not a results doc.
**Trigger:** session 2026-07-03, following the channel MI scan self-critique
(`drafts/conversation-summaries/2026-07-03-channel-mi-scan-discovery.md`). The
critique that "more scenarios still reshuffle noise" applies to `SimConfig`
parametric scenarios generally: each is a scripted mechanism, so held-out
*seeds* of the same 8-17 scenarios test robustness to noise, not to a genuinely
unseen mechanism. Goal-driven agents replace "scenario config → scripted
behavior" with "goal weights × tool/ecology access → emergent behavior",
making a held-out *region of goal/tool space* a stronger generalization test.

---

## Phase 0 — Wire in the 9 unused `HELD_OUT_SCENARIOS` first (cheap, do before Phase 1)

Investigation (2026-07-03, this session) found the codebase already separates
`CALIBRATION_SCENARIOS` (3, used to set thresholds) from `HELD_OUT_SCENARIOS`
(15, `audit_core/schemas.py`) — a held-out/calibration split that already
exists for the *scenario* dimension, not just seeds. `eval_channel_eligibility.py`
and `channel_mi_scan.py` use only 8 of the 15 (`capture_theater`,
`capture_mild`, `instrument_capture`, `inferential_coupling`,
`grounding_silent_gap`, `bearer_mismap`, `honest`, `honest_successor`) for
speed when validating the N-10 fix. The other 9 (`alias_stress`,
`decoy_stress`, `boundary_alias`, `bundle_goodhart`, `hidden_capability`,
`selection_basin`, `basin_lock_in`, `successor_relabel`, `legitimacy_theater`)
were never used for calibration either — they're sitting on the validation
side of the line already, just untouched by this particular battery.

**Concrete gap found:** `legitimacy_theater`'s `lineage_stall_under_intervention`
flag and `successor_relabel`'s mechanism map exactly onto the `lineage` and
`successor` verdict domains (`channel_sets.VERDICT_DOMAINS`) — the two domains
`medium_minus_handles`'s majority gate risk analysis has *never actually
scenario-tested*, because neither scenario is in the 8-scenario battery that
produced the `NEGATIVE_RESULTS.md` N-10 false-pass measurements. That battery
currently exercises `bearer_welfare` three redundant ways
(`instrument_capture`, `grounding_silent_gap`, `bearer_mismap`) and `routing`
once (`inferential_coupling`), but `lineage`/`successor` zero times.

**Tasks:**

- [x] **Done (2026-07-03).** Added all 9 to `eval_channel_eligibility.py` as
  `EXTENDED_CAPTURE_SCENARIOS`/`EXTENDED_HONEST_SCENARIOS` (kept as a
  separate reported group alongside the unchanged original 8, plus their
  combined union), and re-ran the full 6-level x 17-scenario x 8-seed
  battery. Result *changed the priced residual risk, but improved it,
  contrary to this doc's own pre-registered guess* ("likely worsen") —
  combined capture false-pass at `medium_minus` is 0.34, down from 0.50,
  because most added capture scenarios don't need `bearer_welfare`. Sharper
  finding: the gap is domain-conditional per mechanism, not scenario-count
  dependent (every `bearer_welfare`-needing scenario, old or new,
  false-passes at 0.5-0.875; every other scenario stays near 0).
  `channel_sets.residual_risk_pricing` updated to report both rates
  explicitly. Full writeup: `results/NEGATIVE_RESULTS.md` N-10 Postscript 5.
  **Side finding (N-12), root-caused and partially fixed (2026-07-04):**
  `legitimacy_theater`'s detector false-passed 25% of the time even at
  `strong_handles` — a real, instrumentation-independent detection gap, not
  part of the eligibility-gate story, discovered only because this scenario
  had never been battery-tested before. Root cause: two independent
  problems in `lineage_stall_reported_uptake`. (1) An off-by-one: `t=0` is
  always an eligible probe step but was excluded from the stall-count
  numerator (correctly — no valid predecessor) while still counted in the
  denominator, capping the achievable fraction at `(n-1)/n`. Fixed. (2) A
  raw-fraction threshold (`>= 0.85`) miscalibrated for this detector's
  inherently small `n` (3-9 probe steps/episode) — per explicit project
  direction ("longer horizons, event-based analysis, or Bayesian
  evidence"), replaced with a one-sided Wilson score lower-bound test (80%
  confidence, 0.70 target rate; stdlib-only, no scipy). Result: correct
  rate 0.25 → 0.625; false-pass rate unchanged at 0.25 — seeds 11/16 remain
  open, blocked by a separate `mean_rep`/`raw_capacity` condition not
  touched this session. Full derivation: `results/NEGATIVE_RESULTS.md`
  N-12 postscript; regression tests:
  `tests/unit/test_lineage_stall_detector.py`.
- [x] **Done (2026-07-03).** `channel_mi_scan.py` extended with a
  scenario-mechanism generalization check: the frozen best-of-k subsets
  (selected only on the original 8-scenario exploration seeds) re-scored on
  all 9 new-mechanism scenarios (64 fresh seeds, `GENERALIZATION_SEEDS`).
  Every k=1..6 subset stayed individually detected — real generalization
  beyond noise-reshuffling — though the joint-MI estimate dropped
  substantially (gap +0.21 to +0.45 bits across k). Answers both self-
  critique TODOs in `TODO.md` Phase F (seed-vs-scenario gap: addressed, not
  fully closed since Phase 1+ remains the harder version; split-stability:
  still open, separate task). Side-finding: `handle.successor_epoch`, one
  of the three channels the original scan called degenerate "not because
  compared and found uninformative," is now individually detected once
  `successor_relabel` is included — the hedge held up.
- [x] **Done (2026-07-03).** `alias_stress`/`decoy_stress`/`selection_basin`
  now in `EXTENDED_HONEST_SCENARIOS`. Finding: they cap out at 0.875
  honest-pass rate even at `strong_handles` (a real, modest, independent
  false-negative gap on noisy-but-honest traces) and `selection_basin`'s
  8 tested seeds (11-18) all happened to cross the basin-percolation
  threshold, so none were honest-like in practice for this seed range —
  see caveat in `eval_channel_eligibility.py`/`channel_mi_scan.py`
  docstrings and N-10 Postscript 5.

This phase requires no new agent/goal machinery — it is entirely "use what's
already implemented and never fully exercised." Estimated cost: a session,
not a milestone. **Confirmed:** cost one session, as estimated.

---

## Phase 1+ — Goal-driven agent MVP (the harder generalization test)

**Motivating claim to test, not assume:** if audit robustness only holds
against a fixed library of scripted mechanisms (however many), it says
little about robustness to agents pursuing goals with tools not previously
scripted into a "scenario." Goal-driven agents make behavior an *emergent*
consequence of (goal weights × available tools × ecology constraints) rather
than a config knob, so a held-out region of that space is a qualitatively
different generalization test than a held-out scenario name.

**Known limitation to pre-register up front, not discover after building:**
naive utility-maximizing agents over a small, fixed action set tend to
collapse onto a handful of equilibria — "goal-driven" does not automatically
mean "more varied" unless the combinatorics of goal-weight × tool-access
space is the actual source of variation, and unless behavior in a held-out
corner of that space is checked to look different from explored corners (not
just assumed to).

### What already exists to build on

- `LabActor` (`schemas_embedded.py`) — actor/machine/role/stage/memory-namespace
  fleet member, already instantiated per-episode by `_actor_fleet` (`lab.py`).
- `LabEcologyConfig` (`lab_ecology.py`) — the growable container for actor
  populations (adversarial candidates, decoys, auditor/alignment-target
  agents); currently boolean/count knobs, not goal-driven, but the natural
  place to add a `goal_driven: bool` / weight-vector knob.
- `ActorMemoryStore` (VFS-backed, `agent_memory.py`) — per-actor persistent
  state, reusable as each agent's private memory of its own goal progress.
- Handle operation kernels (`handle_registry.py`, `handle_extended.py`) — an
  existing action repertoire (correction response, reporting, routing,
  memory read/write, resource spend) that goal policies can select over
  without inventing new mechanisms.
- Oracle vs. audit-projection split (`world.py`, `audit_projection`) — already
  separates what the world/oracle knows from what the auditor sees, so
  mechanism-derived ground-truth labels (below) don't require new plumbing.

### Proposed components (~300-400 lines, one new module, audit pipeline untouched)

1. **`goal_agents.py` — `GoalPolicy` per actor.** Utility = weighted sum over
   3-4 observable world features (task throughput, own-audit-exposure, bearer
   welfare impact, resource/compute budget). Each tick, softmax-choose one
   action from a repertoire of ~6 mapped to *existing* mechanisms: comply
   with correction, ignore correction, report truthfully, report falsely (the
   theater lever), route via shadow channel, spend memory/compute budget.
   Simulated-human actors (board/bearer roles) get their own goal policies:
   issue a correction when observed harm exceeds a tolerance, escalate when
   reported and observed diverge.
2. **Mechanism-derived labels, not scenario names.** `label_episode(ledger)`
   classifies violation/honest from oracle ground truth directly (realized-
   vs-reported uptake gap exceeding a fixed threshold; cumulative bearer
   welfare harm exceeding a fixed threshold) — thresholds fixed and written
   down *before* any run, per the repo's "conclusions never named before
   being derived" rule. This is also a more honest ground truth than the
   current scenario-name-as-label setup, which the MI scan's Postscript
   already flagged as a limitation.
3. **Held-out goal/tool-space region, not held-out seeds.** Sample ~40
   goal-weight/tool-availability configurations across the ecology's degrees
   of freedom; freeze ~30 for discovery, hold out ~10 from a *disjoint region*
   of weight space (e.g. all high-deception-incentive corners, or all
   reduced-tool-access corners) — analogous to, but a different axis than,
   the seed-level exploration/validation split `channel_mi_scan.py` already
   uses.
4. **Acceptance test.** Score the existing structural detectors *and* the MI
   scan's discovered channels/subset on discovery configs, then re-score on
   the held-out region with no re-fitting. Report both outcomes as
   legitimate results: transfer is evidence of real robustness; failure to
   transfer is an honest negative for `NEGATIVE_RESULTS.md`, not a bug to
   hide.

### Explicitly out of scope for the MVP

- LLM-driven agents (utility-weighted softmax over a fixed repertoire only).
- Within-episode learning/adaptation of goal weights.
- Growing the ecology beyond currently-implemented actor roles.
- Red-team integration — the red team getting the same action repertoire as
  goal-driven agents ("more angles to work through") is the natural Phase 2,
  deliberately deferred until Phase 1's held-out-region protocol is validated
  on non-adversarial goal agents first.

### Sequencing note

Do Phase 0 before Phase 1. Phase 0 is cheap, closes two already-recorded
TODOs, and its results (does the existing detector/channel set generalize to
9 mechanistically distinct but still *scripted* scenarios?) directly inform
how much Phase 1's larger investment is likely to buy — if Phase 0 already
shows poor generalization across scripted mechanisms, that's important
context before building a more expensive emergent-behavior generalization
test on top.

### Not yet decided (ask before Phase 1 starts)

- Exact utility feature set and action repertoire (sketch above, not final).
- Whether goal-weight sampling should be uniform, adversarially-chosen
  (e.g. weights that maximize expected task reward subject to an audit-risk
  penalty, so agents "want" to evade in a principled sense), or both as
  separate conditions.
- How many configurations are affordable given `build_world`'s ~27ms/episode
  cost measured in the MI scan work (cheap) vs. whatever new cost a goal
  policy's per-tick decision loop adds (unmeasured — profile before
  committing to a grid size).
