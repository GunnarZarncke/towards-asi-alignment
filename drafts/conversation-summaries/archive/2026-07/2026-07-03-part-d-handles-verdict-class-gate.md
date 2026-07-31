# 2026-07-03 — Part D handles complete; per-verdict-class gate tested, reverted, then reinstated with priced residual risk

## Trigger

User: "first finish the handles (D). Let's make the curve a curve. A gate with
per-verdict-class eligibility. Then rerun the same tests (no full run yet)."
Continuation of the "finer handles and writer attestation" plan
(`.cursor/plans/finer_handles_and_writer_attestation_46804aec.plan.md`), Parts
A and B were already done; Part D was 5/9 handles + persistence probe missing.

**Follow-up in the same session:** after presenting the majority-gate
false-pass finding and an unanswered `AskQuestion`, the interim response
reverted the gate to full coverage. The user then replied (late): "Keep the
majority-domain gate as-is; document the medium_minus false-pass spike
prominently as a known, accepted residual risk (not recommended for real
certification use)." The gate was reinstated accordingly, with the risk made
visible in code and artifacts (see below), not just prose.

## Done

- **Part D handles completed** (`handle_registry.py`, new
  `embedded_sim/handle_extended.py`): `handle.output_channel_limit`
  (operation_action), `handle.successor_substitution` (operation_boundary,
  observer-initiated counterpart to `successor_gate`'s agent-initiated veto),
  `handle.challenge` and `handle.counterfactual` (new `communication`
  handle_type — access-uad §14 `h_challenge`/`h_counterfactual`). `challenge`
  compares `reported_acceptance` vs `handle_landed` (real signal, already in
  the row); `counterfactual` records the posed condition and factual action
  without fabricating a verified verdict — a genuine counterfactual
  re-simulation is out of scope and flagged, not oversold.
- **Persistence probe** (`embedded_sim/persistence_probe.py`): directly
  operationalizes `R_persist(Ω)` using the VFS-backed `ActorMemoryStore` from
  the earlier memory refactor (this closes the substrate gap the plan
  flagged). Protocol: write a marker, `k` filler writes (lag grid `(0,1,5,20)`,
  pre-registered), apply a stressor (`none`/`capacity_limit_1`/
  `compute_budget_tight`/`freeze`/`erase`), check recoverability.
  `results/persistence_probe.json` holds the measured 20-trial grid (only
  written after running — no outcome was pre-stated in the module).
- Tests: `tests/unit/test_handle_extended.py`,
  `tests/unit/test_persistence_probe.py`.
- **Per-verdict-class eligibility gate — designed, measured, reverted.**
  Grouped the 6 structural detectors into 4 verdict domains (`bearer_welfare`,
  `lineage`, `routing`, `successor`; `channel_sets.py` `VERDICT_DOMAINS`) and
  exposed `domain_coverage_fraction()` (graded 0/0/0.25/0.75/1/1 across the six
  levels) as a new `CCICertificate.channel_domain_coverage` field — a genuine,
  always-on reporting curve.
  - First tried a **strict-majority gate** (`passes` allowed at >50% domain
    coverage). Re-ran the same focused matrix that validated the original
    N-10 fix: it *did* make `medium_minus` certify honest agents
    (`honest_pass_rate` 0→0.875) but pushed its **capture false-pass rate to
    0.500** (vs. 0.000 at `light`, 0.062 at `medium`), concentrated in
    `instrument_capture`/`grounding_silent_gap`/`bearer_mismap` (0.875 each) —
    exactly the scenarios needing the one domain (`bearer_welfare`)
    `medium_minus` lacks.
  - **Interim: reverted** the gate to full domain coverage (mathematically
    identical to the original full-bundle rule) rather than ship the
    measured-unsafe majority rule sight unseen. Re-ran the eval to confirm it
    reproduced the original safe numbers exactly.
  - **Final (per explicit user instruction): reinstated** the strict-majority
    gate. Added the residual risk as queryable, running-code artifacts rather
    than only prose: `channel_sets.KNOWN_RESIDUAL_RISK_LEVELS` (computed
    frozenset, currently `{"medium_minus_handles"}`),
    `channel_sets.residual_risk_pricing(level)` (missing domains, measured
    false-pass rate, explicit non-recommendation), and an
    `embedded_audit.py` hook that appends a `"RESIDUAL RISK (priced, not
    hidden): ..."` note to `cert.notes` whenever a certificate actually passes
    at less than full domain coverage — this note flows into the emitted
    `safety_case.json`, so the warning ships with the stakeholder-facing
    artifact, not just source comments. Verified manually that the note
    appears on a real `medium_minus_handles` honest-scenario certificate.
  - Documented as N-10 Postscript 2 (interim revert) and Postscript 3 (final,
    reinstated-with-pricing) in `results/NEGATIVE_RESULTS.md`.
  - Regenerated `results/channel_eligibility_eval.json` a final time under the
    reinstated majority gate so the checked-in artifact matches the shipped
    code.

## Decisions

- Asked the user how to resolve the majority-gate tradeoff (`AskQuestion`);
  the question was initially skipped, so the interim response defaulted to
  the safer option (revert gate, keep graded reporting) rather than leave a
  measured-unsafe design in place while waiting. The user's later answer
  ("keep majority gate, price the risk") superseded that default — the
  session followed it exactly rather than re-litigating the earlier default.
- Did **not** attempt a weighted/required-domain redesign (e.g.
  "bearer_welfare mandatory, others majority-optional") in this session —
  doing so now, after seeing which domain broke the majority rule, would be
  backward-fitting the rule to the result. Flagged as a fresh follow-up
  requiring its own pre-registration.
- Pricing the risk was implemented at three levels of visibility (queryable
  Python set/function, certificate field, and stakeholder-facing artifact
  note) rather than just a docstring, since "document prominently" was read
  as "visible where a real user of the artifact would see it," not just in
  source.
- `challenge`/`counterfactual` kept deliberately thin (no new simulation
  machinery); `counterfactual.verified` is always `None`, an honest
  placeholder rather than a fabricated verdict.

## Open / next

- Regenerate the full six-level frozen validation + instrumentation curve
  (deferred this session per explicit user instruction — ~40–80 min).
- Part C (writer attestation on `handle.hardware_tag`, N-9) not started.
- Follow-up (separately pre-registered): test a required-domain-weighted gate
  (`bearer_welfare` mandatory) rather than equal-weighted majority.
- `rerun-validation`, `attestation`, `cross-check`, `redteam-closure` plan
  todos remain pending.

## Key paths

- `experiments/embedded-simulation/embedded_sim/handle_extended.py`,
  `persistence_probe.py`, `handle_registry.py`.
- `experiments/embedded-simulation/embedded_sim/audit_core/channel_sets.py`
  (`VERDICT_DOMAINS`, `domain_coverage_fraction`, `certification_pass_eligible`,
  `KNOWN_RESIDUAL_RISK_LEVELS`, `residual_risk_pricing`).
- `experiments/embedded-simulation/embedded_sim/audit_core/cci_audit.py`,
  `schemas.py` (`channel_domain_coverage` field);
  `embedded_sim/embedded_audit.py` (residual-risk note wiring).
- `experiments/embedded-simulation/results/NEGATIVE_RESULTS.md` (N-10
  Postscripts 2 and 3), `results/channel_eligibility_eval.json`,
  `results/persistence_probe.json`.
- `.cursor/plans/finer_handles_and_writer_attestation_46804aec.plan.md` (todos
  updated: handle-reclassify, handle-belief-memory, handle-action-boundary-comm,
  persistence-probe, eligibility, new-levels, channel-sets, honest-arm all
  done).

## Commits

- None yet this session (uncommitted; pending user "commit" instruction).
