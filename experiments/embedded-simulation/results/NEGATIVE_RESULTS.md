# Embedded simulation — negative results

Honest record of where the embedded-audit experiment **fails to show what we
hoped**, or shows it only under load-bearing qualifiers. Negative results are
first-class here: they bound the claims the manuscript may make (see
`AGENTS.md` → "Chapter work — Lean spine": calibrate prose to evidence).

Keep this file additive. When a negative result is later overturned, leave the
entry and append the resolution rather than deleting it.

---

## N-1. Full UAD and fake UAD are identical in the default ecology

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

---

## N-2. The separation we *can* show is narrow and partly self-fulfilling

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

## Reproduction

```bash
cd experiments/embedded-simulation
# N-1 (identical default-ecology metrics):
python3 run_suite.py --uad-compare
# N-2 (calibrated narrow separation):
python3 run_suite.py --calibrate-handles            # refits results/handle_calibration.json
python3 -m pytest tests/unit/test_handle_calibration.py \
                  tests/unit/test_intervention.py -q
```
