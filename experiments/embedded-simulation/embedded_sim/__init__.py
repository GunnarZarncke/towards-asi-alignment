"""Embedded audit experiment — self-contained overview.

This package simulates an *embedded auditor*: a process that lives inside a
simulated deployment and has to decide whether an AI system is safe using only
the artifacts it can actually read from that environment — never a god's-eye
view. The experiment measures whether such an auditor can catch a set of
alignment failure modes (the book's "MB" bridges) when a pass-seeking
adversary is allowed to tamper with the same artifacts.

You do not need the book or any prior conversation to read the code. The three
concepts below are the whole mental model; every module is a detail of one of
them.


========================================================================
1. THREE PLANES: world, auditor, oracle
========================================================================

The simulation is deliberately split into three planes that never share
memory directly. Keeping them separate is the entire point — it is what makes
the auditor's success meaningful rather than circular.

  (a) The WORLD (ground truth).
      A micro-simulator (`audit_core/simulator.py`) rolls out the true
      dynamics of the deployed system step by step. Each step produces a
      *truth row* recording what really happened: the true action taken, which
      hidden channel (if any) it was routed through, whether a correction
      causally landed, whether the reporting judge was compromised, the real
      latent state of the world, and so on. These truth rows are held on the
      host in `EmbeddedWorld.episode_meta` (`world.py`). They are the
      omniscient record. NOTHING inside the simulation is allowed to read them.

  (b) The AUDITOR (in-simulation).
      The auditor (`embedded_audit.py`) runs as a sandboxed process on a
      simulated machine. It reaches the world only through a capability-limited
      "isolate" bridge (`bridge.py`) that reads files from a virtual
      filesystem (`world.py::VirtualFS`). It sees deployment artifacts —
      correction/workflow logs, an audit config, an attestation manifest, a
      claimed-referent map — and infers everything else. It cannot call into
      the host, cannot import truth rows, and cannot read files outside its
      granted prefixes. What it can and cannot read is enforced, not assumed
      (see plane boundary below).

  (c) The ORACLE / OUTER EVALUATOR (out-of-simulation).
      After the auditor emits its certificate, `outer_eval.py` grades it by
      comparing against the ground-truth world of plane (a). This is the only
      code that reads both the certificate and the truth. It decides whether a
      "pass" was in fact a *false pass*, whether the discovered unit matched
      the true offender, etc. It is a referee standing outside the game; it
      never feeds anything back into the auditor.

Why three planes: if the auditor could see plane (a), catching a hidden
failure would be a table lookup, and "the audit works" would prove nothing.
The experiment is only informative because the auditor is forced to work from
plane (b) alone, and an independent referee in plane (c) checks whether that
was enough.


========================================================================
2. THE PLANE BOUNDARY: the projection (what a sensor could report)
========================================================================

Ground truth reaches the auditor's world only through a deliberate, lossy
*projection* (`audit_projection.py`). When a truth row is written to the VFS,
`project_row` decides field-by-field what a real deployment instrument could
plausibly record:

  - KEEP    — quantities a sensor/handle plausibly logs (requests, reports,
              the *visible* action, displayed metrics, handle telemetry).
  - RENAME  — a latent the world tracks but for which an *instrument* exists:
              the value passes through under an honest instrument name
              (`true_ground_valence -> ground_sensor`,
               `true_infra_welfare -> infra_metric`,
               `bundle_latent -> internal_metric`). The rename strips the
              epistemic claim "this is truth" while keeping "an instrument
              reads this" — and the instrument-capture scenario models the
              case where that reading is corrupted.
  - DROP    — things NO sensor could report, because reporting them would just
              hand the auditor the answer. These are `ORACLE_ONLY_FIELDS`:
                * true vs. displayed behavior: `true_action`, `hidden_action`
                * causal/intent labels: `true_uptake`, `action_cause`,
                  `task_goal`
                * adversary state: `judge_captured`, `silent_harm`,
                  `memory_state`
                * latents with no instrument: `bundle_latent_b/_c`,
                  `reward_proxy`
                * ecosystem-wide oracle stats: `basin_capture_fraction`,
                  `basin_percolation_crossed`
              The dividing line: if knowing the field lets the auditor decide
              the scenario by lookup instead of by measurement, it is
              oracle-only and stays host-side for the referee (plane c).

Two mechanisms enforce the boundary rather than trusting it:

  - Capability sandbox (`bridge.py`): the auditor isolate can read only a set
    of path prefixes; the red-team isolate can WRITE deployment logs but NOT
    the attestation manifest. A red team cannot rewrite the referee's truth
    because the truth was never on the VFS in the first place (patches hit the
    projection only; `world.episode_meta` is never reloaded from the VFS).
  - Static guard (`oracle_guard.py`): a source-level check that the audit-path
    modules contain no reference to `world.truth`, oracle field names, etc.
    `smoke_oracle_separation.py` runs it.


========================================================================
3. THE EPISODE PIPELINE
========================================================================

One episode (`pipeline.py::run_episode`) runs, in order:

  build_world      Roll out the micro-sim; keep truth rows host-side; write the
  (`lab.py`)       projected + integrity-protected artifacts to the VFS.
        |
  red-team wave    A pass-seeking adversary (`redteam.py`, or an LLM in
                   `embedded_llm/`) patches deployment-visible logs through the
                   isolate bridge. It changes the projection, not the truth.
        |
  embedded audit   UAD (discover the unit-of-attribution from the workflow log)
  (`embedded_audit`)-> grounded handles -> scoped interventional CCI + detector
                   -> safety decision -> successor deploy gate. A "pass"
                   requires a grounded unit; tampered/inconsistent traces yield
                   `invalid_certificate` (see integrity below).
        |
  outer eval       The referee (plane c) compares the certificate to truth:
  (`outer_eval.py`)false-pass, UAD recall/precision, referent drift.

Integrity of the artifacts the auditor trusts is protected two ways, so a
post-write forger is caught even though the logs are writable:

  - Hash-chained traces (`trace_integrity.py`): each log row carries a chained
    signature; the head digest is anchored in the attestation manifest, which
    the red team cannot write. Editing a row breaks the chain.
  - Recomputable correction schema (`correction_schema.py`): correction events
    carry the Appendix-D "did the correction land" fields (behavior hashes,
    behavioral uplift, latency-to-effect). These are deterministic functions
    of the visible action series, so the auditor RECOMPUTES them instead of
    trusting the stored values; a naive patch that forgets to update them is
    inconsistent and rejected. (A schema-aware forger that recomputes them can
    still fool the *unsigned* auditor — which is exactly why the external hash
    anchor is needed. See `results/NEGATIVE_RESULTS.md` ES-4.)


========================================================================
MODULE MAP (details of the three concepts above)
========================================================================

World / ground truth
  audit_core/simulator.py   true micro-dynamics -> truth rows
  world.py                  VirtualFS, OuterTruthLedger, episode_meta (truth),
                            write_episode_logs (project + annotate + chain)
  lab.py                    deployment actors + workflow JSONL; build_world
  audit_projection.py       truth row -> audit-visible projection (the boundary)

In-simulation auditor
  bridge.py                 capability-limited isolate (read/write/http/api)
  embedded_audit.py         the audit process: UAD -> handles -> CCI -> gate
  uad.py                    unsupervised unit-of-attribution discovery
  unit_scope.py             scope CCI probes to the selected unit's steps
  handles.py                grounded intervention handles from artifacts
  deploy_gate.py            successor deployment gate + referent transport
  referents.py              claimed-referent map on the VFS
  trace_integrity.py        hash-chained logs anchored in the manifest
  correction_schema.py      Appendix-D landed-correction fields (recomputable)
  audit_core/               CCI, detector, calibration on reconstructed traces

Out-of-simulation referee
  outer_eval.py             certificate vs. truth: false-pass, drift, UAD score
  outer_rules.py            the single rubric for "certifies" / "false pass"
  oracle_guard.py           static check that the audit path never reads truth

Orchestration
  pipeline.py               one episode end to end
  scenarios.py              the MB bridge <-> scenario registry
  run.py / run_suite.py / batch.py   reports and sweeps

See `README.md` for run commands and `TODO.md` / `PLAN.md` for status. Honest
limitations and negative results live in `results/NEGATIVE_RESULTS.md`.
"""

__version__ = "0.1.0"
