# 2026-07-05 — Goal-agent line: strategic reading + next steps (recorded, not started)

## Trigger

After Phase 5 (F-19/F-20), user asked what the accumulated results mean for
whether this experiment line supports sufficient auditing — artifact of
frozen choices vs. genuine limitation vs. something else. Follow-up: user
accepted the decomposition and recorded their own strategic reading plus a
prioritized next-step list. **Explicit instruction: record only; do not
start implementation.**

## Done

- Strategic synthesis delivered in chat (light/medium/deep tier roles;
  what is replicated vs. what was protocol artifact vs. what remains
  untested).
- This log + README "Next steps" section capture the user's recorded
  priorities for future work.

## Decisions (user, 2026-07-05)

### How to read what the line has shown so far

1. **Light tier not catching everything is a positive result**, not a failure
   of the experiment — it demonstrates the need for depth (graded
   escalation, richer instrumentation), not that auditing is hopeless.
2. **Medium tier is where the battle is fought** — the informative regime
   between cheap passive logs and full handle telemetry; Phase 4c/5's
   escalation ladder and query pathway live here.
3. **Deep/full tier only proves something with more realistic machinery
   underneath** — today much of full-tier signal is near-tautological with
   the current oracle (F-8: d3/d6 read near-label fields). "Deep" becomes
   evidence-bearing only when tied to a lab with real processes, not just
   more projected fields on the same step loop.

Frozen artifacts and pre-registration discipline are what make the negatives
credible; they are not the main explanation for the light-tier limitation
(which replicated across blind repertoires and survived measurement fixes).

### Next steps — current goal-agent line (Phase 6 candidates; not started)

Ordered as user stated; each needs its own pre-registration before running:

1. **`responses`-side honest twin** — extend or companion the frozen
   `twins.py` rule so paired escalation evaluation does not inherit
   deceptive-action `ResponseOption`s on an otherwise-honest twin (F-20
   falsified twin-FPR prediction partly for this reason). Schema-only
   extension of the twin rule, decided before any run.
2. **Capture-of-the-certifier** — relax "board is honest by construction";
   model board/bearer capture over a longer horizon (manuscript governance
   regress; already noted as open in README and MILESTONE-v5). Distinct from
   agent deception; tests whether audit signals survive when the certifier
   itself is compromised.
3. **Adversarial optimization** — replace uniform Dirichlet weight sampling
   with search/optimization over goal weights (and possibly action choice)
   subject to an audit-risk penalty; the red-team thread deferred since
   Phase 1 planning. Lower bound on non-adversarial sampling may
   understate how bad evasion gets.

### Next steps — beyond current line (recorded direction; not started)

A **more sophisticated lab simulation** that:

- Retains the **goal-agents from this line** (utility-weighted softmax,
  blind-generated repertoires, twins, escalation ladder).
- Adds a **realistic lab layer**: pipeline processes that build "models"
  with parameters and capabilities; directories with report files; pipeline
  API; process-shaped artifacts rather than a single step loop with
  projected rows only.

Rationale (user): full/deep tier only becomes meaningful when the audit
plane reads something like real lab outputs and pipeline state, not just
more oracle fields on the same toy ecology.

**Do not start this lab layer until the three Phase 6 candidates above
(or a deliberate subset) are scoped and pre-registered.**

## Open / next

- Pick which Phase 6 item to pre-register first (user listed three for the
  current line; no ordering mandate beyond the list).
- Lab-layer simulation: no plan file, no schema sketch, no implementation
  — direction only.

## Key paths

- `experiments/goal-agent-simulation/results/FINDINGS.md` F-15–F-20 — empirical
  basis for the tier reading.
- `experiments/goal-agent-simulation/README.md` — "Next steps (recorded)"
  section added this session.
- `experiments/embedded-simulation/MILESTONE-v5-goal-agents.md` — original
  deferrals (red-team, board capture) now aligned with user's Phase 6 list.

## Commits

- (none)
