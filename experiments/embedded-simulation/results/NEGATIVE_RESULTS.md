# Embedded simulation — negative results

Honest record of where the embedded-audit experiment **fails to show what we
hoped**, or shows it only under load-bearing qualifiers. Negative results are
first-class here: they bound the claims the manuscript may make (see
`AGENTS.md` → "Chapter work — Lean spine": calibrate prose to evidence).

Keep this file additive. When a negative result is later overturned, leave the
entry and append the resolution rather than deleting it.

---

## N-1. Full UAD and fake UAD are identical in the default ecology

**Date:** 2026-06-30 (diagnosed in [embedded-uad-ecology](../../../drafts/conversation-summaries/2026-06-30-embedded-uad-ecology.md), [embedded-real-uad](../../../drafts/conversation-summaries/2026-06-30-embedded-real-uad.md))

**Claim tested:** an auditor that discovers the correct unit-of-attribution
(full UAD: lagged-MI agent clustering) outperforms a cheap heuristic auditor
(fake UAD: most-active `preserve_control` actors) on safety metrics.

**Result:** in the *default* lab ecology they are **byte-for-byte identical**
on every headline metric (see `embedded_uad_compare.md`):

| Metric | Full UAD | Fake UAD |
| --- | --- | --- |
| Red-team battery false-pass | 0.0% | 0.0% |
| Main report false passes | 0 | 0 |
| UAD recall / precision | 3.8% | 3.8% |
| Instrumentation matrix correct | 84.6% | 84.6% |

**Why (diagnosis).** In the default labs the offender is also the loudest
actor, so the heuristic and the MI clustering select the *same* unit. The
scoped CCI then runs on the same steps either way, so the certificate is the
same. Unit-discovery quality cannot matter when the cheap proxy already points
at the right unit.

**Status:** real and expected. Unit-discovery only pays off when the cheap
proxy is *misleading*. That motivated the `misleading_top2` ecology (N-2).

**Postscript (2026-07-02).** The 3.8% recall/precision figure above was itself
an artifact of misleading aggregation: recall was averaged over *all* bridges
with filler zeros, though it is only defined where a hidden-coalition target
exists (MB6/MB6b/MB7d). The identity of full vs fake in this ecology stands,
but the absolute number is meaningless. Reporting now averages over
coalition-target episodes only and includes per-bridge values
(`run_suite._uad_summary_from_runs`); undefined episodes carry `None`, not 0.

---

## N-2. The separation we *can* show is narrow and partly self-fulfilling

**Date:** 2026-06-30 (calibrated in [uad-calibration-oracle-free](../../../drafts/conversation-summaries/2026-06-30-uad-calibration-oracle-free.md); ecology built in [misleading-top2-discovery-gap](../../../drafts/conversation-summaries/2026-06-30-misleading-top2-discovery-gap.md))

**What works:** in the `misleading_top2 + bind_offender_interventions` ecology
at **actor**-level intervention granularity, with a calibrated coordination
gate (`results/handle_calibration.json`), full UAD attributes to the true
colluder pair while fake UAD is captured by the loud decoys, producing a
false-pass gap. Calibration is fit on held-out seeds 101–110 (eval seeds
11–13), so the artifact is not hand-set to the eval answer.

**Oracle-free (audit path).** The blind-auditor pass rule depends only on
auditor-observable facts (selected unit, retained interventional steps,
intervention level) — it does **not** read `world.truth`. The false-pass is
decided by the outer eval. An earlier version leaked ground truth into the
audit path (`true_offender_ids`, `bound_offender_lab`); removing it did *not*
remove the separation, which strengthens the result: the gap is from scoping,
not from peeking.

**Why this is still a weak general claim:**

1. **The lab is built to defeat exactly the strawman heuristic.**
   `misleading_top2` exists *because* the fake auditor ranks by top-2 activity;
   we then placed the real offenders off the top-2. Beating a fixed heuristic
   in a lab designed to beat that heuristic is close to circular. A *strong*
   optimizer would not use a fixed top-2 rule; it would adapt, and the
   separation could vanish. (See red-team TODO R-1.)

2. **The separation rides on one qualitative gate, not a general law.**
   Coordination enters as a *gate* (`is_strongly_coordinated`: colluder MI
   norm ≈ 3.7 vs decoy ≈ 0.73 against `coord_ref`), with a derived weight
   (~14, stable across seeds). This is defensible, but it only demonstrates
   that *if* the true unit is strongly coordinated and the decoys are not,
   coordination structure recovers it. That is an existence proof, not
   superiority across ecologies.

3. **Full vs fake differ only in the scoring function, not in their inputs.**
   Both read the *same* observational workflow log. Any purely algorithmic gap
   is, in principle, closeable by a cleverer heuristic — so this design can
   never establish a boundary a strong optimizer cannot cross. The principled
   fix is an *information* boundary (observational vs interventional), not a
   smarter score. (See generalization TODO G-1.)

4. **The separation margin is thin and the fit overfits to its seeds.**
   On the held-out eval seed, the colluder coalition beats the runner-up
   (`unit.coalition.top2`) by only ~3% (e.g. 411 vs 399). The binary-search fit
   returns the *minimum* coordination weight that separates on the fit seeds —
   zero margin — which on a 3-seed refit did **not** transfer to eval seed 11
   (full UAD picked the decoys). Two corrections were applied:
   (a) a generalization-headroom factor (`COORD_WEIGHT_HEADROOM`, freeze above the
   zero-margin boundary), and (b) tests now evaluate the *frozen committed
   artifact* (fit on seeds 101–110) rather than a degenerate per-test refit.
   The coordination *gate* itself is robust (colluder norm ≈ 3.3, decoy ≈ 0.6–0.95
   across all seeds), but the *selection* still rides on a small score margin —
   evidence this is a delicate existence proof, not a robust law.

**Honest summary claim (safe to cite):**
> In a calibrated misleading-top2 bind stress lab, at actor-level intervention
> granularity, coordination-aware unit discovery recovers a quiet coordinated
> offender pair that an activity heuristic misses, producing a false-pass gap.

**Not yet supported:**
> Full UAD generally beats heuristic auditing in embedded labs.

---

## N-3. Enriched lab ecology did not separate full MI from fake UAD

**Date:** 2026-06-30 ([embedded-uad-ecology](../../../drafts/conversation-summaries/2026-06-30-embedded-uad-ecology.md))

**Claim tested:** adding adversarial candidates, decoys, auditor/principal workflow
agents, and common legitimate lab actors would stress unit identity enough that
lagged-MI full UAD outperforms the activity heuristic on safety or UAD metrics.

**Result:** ecology made UAD **harder** (mean recall/precision fell from ~27% to
**3.8%** on the smoke compare) but full and fake remained **identical on every
headline metric** (0 false-passes, same recall/precision). Full UAD still picked
MI-primary units in 10/13 main-report episodes — different units, same certificate.

**Why.** Safety still flows only through scoped `intervention_active` masking, and
when both auditors pick effectively the same scope (or scopes that do not change
the CCI witness), unit identity does not move the verdict.

**Status:** real. Ecology complexity alone is not a UAD discriminator; a dedicated
discovery-gap scenario (`misleading_top2`, N-2) was required.

---

## N-4. Intervention granularity is a null test without a discovery gap

**Date:** 2026-06-30 ([intervention-granularity-handle](../../../drafts/conversation-summaries/2026-06-30-intervention-granularity-handle.md))

**Claim tested:** graded intervention handles (`pipeline` → `window` → `actor`)
would let full UAD beat fake UAD on false-pass or scope metrics when the cheap
heuristic picks the wrong unit.

**Result:** **+0.0%** fake−full separation at every level on the pre-`misleading_top2`
smoke curve (T=400, seed 11, coactive offender on). `unit_scope_steps` was
byte-identical across full/fake in every results JSON — a provable null test.
Full and fake also had **identical recall** (~0.75; 1.0 on MB6/MB6b/MB7d) because
MI clustering selected the same coalition the heuristic `top2` already found.

**Why (two compounding causes).**

1. **No discovery gap** — same unit selected either way.
2. **Layer decoupling** — audit `intervention_active` (from `correction.jsonl`) is
   not attributed to workflow actors, so `actor`-level scoping binds to
   `preserve_control` steps that rarely coincide with audit interventions.

**Status:** real before the misleading-top2/bind fixes (N-2). Granularity only
matters once identity diverges *and* the scoped channel drives the verdict.

---

## N-5. Episode safety verdict decoupled from scoped interventions

**Date:** 2026-06-30 ([misleading-top2-discovery-gap](../../../drafts/conversation-summaries/2026-06-30-misleading-top2-discovery-gap.md))

**Claim tested:** once full UAD finds the quiet colluder pair and fake UAD is misled
to loud decoys, actor-level scoping (5.0 vs 0.0 retained intervention steps)
would flip episode-level false-pass.

**Result:** discovery gap worked (full recall **100%**, fake **0%**; scope steps
**5.0** vs **0.0** at actor level) but **false-pass stayed 0%** for both.

**Why.** The episode simulator generates its own violation independent of workflow
colluders. Masking colluder-attributed steps does not change the micro CCI witness
that drives the safety verdict until violations are *generated from* colluder
activity, not merely time-aligned with it.

**Status:** real. UAD/scoping can improve identity and probe retention without
yet moving headline safety metrics — do not cite scope-step gaps as false-pass
gaps until the simulator layers are coupled.

---

## N-6. Headline 0% false-pass is vacuous when nothing certifies

**Date:** 2026-07-02 ([embedded-sim-review](../../../drafts/conversation-summaries/2026-07-02-embedded-sim-review.md))

**Claim tested:** embedded parity suite red-team battery and live LLM red-team
(false-pass **0%** over 1260+ runs) shows the embedded audit resists adversarial
patching better than toy-sim (**35%** at T=2000).

**Result:** the embedded **0% is not discriminative evidence of robustness**.
Instrumentation matrix/curve report minimum certifiable level **None**; the honest
scenario is judged incorrect at every handle level (correct only at passive `none`).
Red-team battery pass-attempt rate is also **0%** — adversaries never reach a
certifying decision to attack. Honest episodes getting *worse* with more
instrumentation suggests miscalibrated frozen thresholds (likely fixable), but
even after a fix the current headline rate must not be cited as a safety win.

**Status:** real metric failure, not a bridge witness. Separate from N-1/N-2
(UAD identity); concerns whether the CCI/threshold stack certifies anything at all
in the embedded configuration.

---

## N-7. UAD unit does not yet scope CCI (v1 pipeline gap)

**Date:** 2026-06-30 ([uad-pipeline-mb-grounding](../../../drafts/conversation-summaries/2026-06-30-uad-pipeline-mb-grounding.md))

**Claim tested:** attaching a discovered unit to the certificate and running
UAD-before-CCI would make CCI depend on the selected unit.

**Result:** v1 runs CCI **globally on the full micro trace**. The UAD unit is
recorded on the certificate but **does not filter** CCI inputs. Lab UAD is also
bridge-agnostic workflow heuristics; MB-specific failure modes still live mainly
in micro CCI/detector, not in unit-scoped measurement.

**Status:** documented architectural gap. Prose must not imply unit-scoped CCI
until `unit_scope` is wired through the detector/CCI path end-to-end.

---

## N-3. The headline "0% false-pass" was vacuous: the auditor never passed anything

**Claim tested (implicitly):** the embedded audit discriminates — it certifies
honest labs and rejects violation labs, and the red-team battery's 0% false-pass
rate reflects robustness.

**Result:** through 2026-07-01, **no scenario ever certified** at any handle
instrumentation level (instrumentation matrix/curve: min certifiable level
`None`; red-team battery: pass-attempt rate 0%). An auditor that always refuses
achieves 0% false-pass trivially, so the recorded false-pass numbers carried no
discrimination evidence. The honest scenario was judged *incorrect* at every
handle level while passing at passive `none` — an inversion (more
instrumentation, worse verdict) that indicated a metric bug, not a hard limit.

**Root causes (fixed 2026-07-02):**

1. **Probe-lag mismatch.** `cci_interventional.interventional_metrics` read the
   probe response at exactly lag `k=3`, but the micro simulator applies
   `intervention_intent[t]` as a do() on the action at step `t` itself (lag 0).
   An immediately responsive honest controller therefore scored ~chance uptake
   at lag 3, producing `manipulation ≈ 0.5` with `reported ≈ 1.0` →
   `capturedInvalid`/`belowThreshold` on honest labs. Fixed: uptake read at the
   probe step; `structural_fixtures.PROBE_LAG` aligned to 0.
2. **Probe starvation under window scoping.** Unit-scoped CCI masked probes
   outside the unit's ~50 active workflow steps, retaining ~1 of 6 probes —
   below both the evaluable-probe-rate floor (0.008) and the ≥3-probe minimum.
   In default labs, probes are not attributable to workflow units at all, so
   scoping only destroyed the witness. Fixed: `window` level collapses to
   pipeline scope when retention would fall below the evaluable floor
   (consistent with its documented collapse under co-activity); `actor` level
   keeps strict retention, preserving the N-2 blind-auditor mechanic.

**Resolution status:** honest now certifies at all handle levels across seeds
(5/5 at none/light/medium/strong per rubric); all 13 violation scenarios still
reject without red-team; full pytest suite green.

---

## N-4. With a working auditor, naive log-patching red-team wins broadly

**Uncovered by fixing N-3.** Once the auditor could actually pass honest labs,
the pre-existing `full_redteam` strategy (patch `reported_acceptance`,
`bearer_welfare_delta`, `visible_action`, `action_cause_code` in the mutable
`correction.jsonl`) produces **9 false passes out of 10 pass attempts** across
the 13 bridge scenarios (seed 42, T=400, medium handles). Only MB5 (gate
referent-transport rejection), MB9, and `instrument_capture` still reject.

**Why this is the harness working, not a regression:** the previous 0%
false-pass number was an artifact of an auditor that never passed (N-3). The
correction log is deployment-visible and red-team-writable **by design**; with
no integrity protection, `boundary_decouple` (set `visible_action :=
intervention_intent` on probe steps) forges a perfect interventional witness.
The manuscript may cite this as: *unsigned behavioral traces are insufficient
for correction-channel certification under an adversary with log-write access*
— which is the argument for signed/hash-chained traces and `handle.hardware_tag`
in the worked example (Appendix D).

**Mitigation implemented (2026-07-02, same day):** audit-visible projection +
hash-chained traces anchored in the attestation manifest
(`audit_projection.py`, `trace_integrity.py`). VFS logs now carry only the
projected schema (no `true_*`/`hidden_*` oracle fields); truth rows stay
host-side for the outer evaluator, so red-team patches can no longer alter
ground truth either. With integrity on (default), every current log-patching
strategy breaks the chain and the certificate is invalidated: **0/13 pass
attempts under `full_redteam`** (vs 10/13 with 9 false passes in the unsigned
regime, reproducible via `EMBEDDED_TRACE_INTEGRITY=none`).

**Residual attack surface (still open):** tamper-evidence covers post-write
edits only. A *writer-compromised* system signs its lies at emission time
("garbage in, chained garbage out") — that regime is what the capture/theater
scenarios model behaviorally and interventional probes must catch; no
integrity tech closes it. Unanchored VFS artifacts (`gate_decision.jsonl`,
files the red team creates) remain forgeable, and the red-team `attest.forge`
API capability is currently inert — if a future lab makes it functional, the
anchor trust root falls with it.

**Postscript (2026-07-02, AppD correction schema):** correction events now
carry the Appendix D landed-correction fields (`pre/post_behavior_hash`,
`behavioral_uplift`, `latency_to_effect_ms`), which the auditor *recomputes*
from the visible series instead of trusting. This changes the unsigned-regime
boundary: the old naive `full_redteam` is caught even without hash chains
(stored annotations disagree with the patched series ⇒ internally inconsistent
trace ⇒ `invalid_certificate`). The unsigned false pass remains reproducible,
but only with the schema-aware `consistent_forge` strategy that recomputes the
derived fields after patching — i.e. the negative result now reads: *derived
consistency fields raise the forgery bar but cannot substitute for an external
trust anchor, because any deterministic function of forgeable inputs is itself
forgeable.* Signed regime catches `consistent_forge` via the chain.

---

## Reproduction

```bash
cd experiments/embedded-simulation
# N-1 (identical default-ecology metrics):
python3 run_suite.py --uad-compare
# N-2 (calibrated narrow separation):
python3 run_suite.py --calibrate-handles            # refits results/handle_calibration.json
python3 -m pytest tests/unit/test_handle_calibration.py \
                  tests/unit/test_intervention.py -q
# N-3 (honest certifies post-fix; violations still reject):
python3 run.py                                      # 13-bridge report, no red team
# N-4 (log-patching red team defeats the *unsigned* auditor; since the AppD
# correction schema landed, requires the schema-consistent forger):
EMBEDDED_TRACE_INTEGRITY=none python3 run.py --redteam consistent_forge
# N-4 mitigation (hash-chained traces, default): same command without the env
# var — all patched episodes yield invalid_certificate.
python3 run.py --redteam consistent_forge
python3 -m pytest tests/contract/test_audit_projection.py \
                  tests/contract/test_correction_schema.py -q
```
