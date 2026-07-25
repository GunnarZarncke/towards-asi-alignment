# PLAN ET-2 — Collective-Intelligence-Library basin_stability external transfer

**Status:** ET2-0 frozen; ET2-1 (adapter), ET2-2 (scorer), and ET2-3 (smoke)
all done. `external/cil/.venv` now has jax/jaxlib/cilib installed (took
several attempts over two sessions — this sandbox's connection to
`files.pythonhosted.org` was severely throttled/reset-prone for large wheels;
eventually completed once ambient network conditions improved). Fixed an
off-by-one in `cil_adapter.py`'s `_CIL_ROOT` path (was `parents[3]`,
should be `parents[2]`) caught by the first live run.

**ET2-3 smoke result (2026-07-25, 4 cells × 5 seeds = 20 episodes, `pld`/`prd`
× frac `{0.2, 0.3}`, `results/et2a_smoke.json`):** mechanically clean —
~0.6s/episode, no shape/type errors, `node_types`/`actions` arrays look
correct (verified manually against one episode). But **every single episode
scored `ari_true=0.0`** because `cmi_edge_matrix` at frozen ET-1 default
thresholds (`min_effect_bits=0.3` etc.) discovered **zero edges** among all
190 agent pairs in every episode — the discovered partition is always
20 all-singleton clusters. This is a real result, not a bug (per-agent action
series have genuine variance — e.g. one agent's 200-round histogram was
`{0: 142, 3: 24, 2: 18, 1: 16}`, not constant). Note a scoring subtlety this
surfaced: when the discovered partition is all-singletons, `adjusted_rand_index`
is *structurally* exactly `0.0` against **any** label vector (true or
permuted) — row/col comb-sums are all zero — so the permutation null is a
point mass at `0.0` too, and `exceeds_null` (strict `>`) can never be `True`
in this regime regardless of whether real signal exists. This doesn't change
the substantive read (frozen passive UAD found no lag-CMI structure at all
here) but is worth stating precisely rather than letting "P1 fails" imply a
graded miss.

**Confirmed at full ET2-4 scale (2026-07-25, `results/et2a_uad_battery.json`,
150 episodes = 3 mechanisms × 5 fractions × 10 seeds, default grid):**
**all 150/150 episodes scored `ari_true=0.0`**, identically to the smoke
sample. `P1 holds=False`, `0/12` cells passing (frac=0 cells excluded from
P1 by design). This is a real, reportable **null** for ET-2a as specified:
frozen passive UAD (unmodified `cmi_edge_matrix`, no threshold retuning)
does not recover the adversarial subgroup on `basin_stability` action-code
series at any tested mechanism × adversarial-fraction combination.

Consistent with the plan's named risk — 200 rounds of Q-learning converges
to a low-entropy, mostly-single-action policy per agent (`action 0`
dominant ~70-75% of rounds in the sample checked), which likely starves
lag-CMI of the effect size it needs at frozen thresholds, independent of
whether the adversarial subgroup is "really" distinguishable in principle.
**Do not retune `min_effect_bits`/`max_lag` to chase a hit on this result**
— per ET2-0's pre-registration discipline, this stands as ET-2a's outcome.
A follow-up, separately-pre-registered variant (e.g. an entropy-based
pre-filter, or scoring on Q-value/policy vectors instead of realized
discrete actions) would be a new experiment, not a patch to this one.

**ET2-0 decisions (frozen 2026-07-23):**

- Target CIL component: `basin_stability` experiment.
- Instrument focus: both leaves (UAD **and** selection/capture).
- Sequencing: new `ET-2 (CIL)` line, parallel to `ET-1 (Orbit)`, not gated on it.
- Integration style: non-vendored sibling checkout, pinned commit (`external/cil/`, done).
- Leaf A specificity test: **label-permutation null for ARI** (chosen over ET-1's fixed-pair exact-match test).
- Leaf A seed budget: **10/cell**, smaller first-pass grid (not the original 30/cell, 630-episode proposal) — see `scripts/run_et2_uad_battery.py` default grid (3 mechanisms × 5 fractions × 10 seeds = 150 episodes; adjust `--fractions`/`--seeds-per-cell` for the full 7-fraction sweep once ET2-3 timing is known).
- Leaf B framing: **descriptive cross-validation only**, no pre-registered pass/fail threshold.

**Parent line:** `experiments/graded-lab-simulation/` (unchanged — sixth
in-repo simulation line stays as-is; this is a cross-cutting external-transfer
annex, same category as ET-1).

**Pinned external commit:** [`eq-network/Collective-Intelligence-Library`](https://github.com/eq-network/Collective-Intelligence-Library)
`25dab1aa5bbd8ca1c19da20eb9f1a9e47cad471c` (2026-07-09), non-vendored sibling
checkout at `external/cil/` (see `external/cil/PIN.txt`, `external/cil/README.md`).
MIT-licensed; not redistributed, only imported locally as a library.

**Spawn trigger:** user request to investigate whether eq-network's
Collective-Intelligence-Library / "Democratic Resilience Lab" (JAX multi-agent
sim of gradual-disempowerment-style dynamics) can serve as an external
substrate for our UAD and selection/correction-channel instruments. Same
motivating gap as ET-1 (appendix scope ceiling: "the decisive next validation
is transfer of UAD/EAI-style instruments to traces from a system... this
project did not author"), but this substrate additionally offers something
ET-1 cannot: a **learned-policy, non-hand-written-roster** population under
adversarial pressure — precisely the gap that closed the graded-lab v1
program (`results/TERMINAL_SUMMARY.md`: "a fixed hand-written roster cannot
generate the unprogrammed strategies the prize question asks about").

---

## What is and isn't real on the eq-network side

The public "Democratic Resilience Lab" page (eq-network.org/lab) advertises
five gradual-disempowerment scenarios (Governed Commons, Economic/Cultural/
Political/Combined Disempowerment) modeled on Kulveit et al., the same paper
we cite as `kulveit2025gradualdisempowerment` for MB6. **Only Governed Commons
is real, running code today; the other four are explicitly tagged "in
design"** — sketches, not simulations. Do not cite eq-network as having
already built a gradual-disempowerment simulator; it has built a
**related-genre** commons/democracy-mechanism engine, `basin_stability`, that
we are choosing to target because its own substance (governance capture under
adversarial pressure) overlaps our MB6/MB8 concepts even though it predates
and does not implement the disempowerment scenarios by name.

## What `basin_stability` actually is (verified against source, not the README alone)

- **N=20 agents** (default), **K=4 proposals/round**, **T=200 rounds**, three
  governance mechanisms selected at composition time:
  - **PDD** (direct democracy): equal-weight plurality vote.
  - **PRD** (representative democracy): only elected reps vote; reps
    re-elected every `election_period=10` rounds by trust-based voting among
    all agents.
  - **PLD** (liquid democracy): trust-weighted plurality; an agent can vote or
    delegate (2-hop resolution) to another agent.
- **Resource dynamics:** multiplicative, `R(t+1) = R(t) * u_selected`;
  collapses (freezes, `alive=0`) if `R` drops below a threshold. "Basin
  stability" = fraction of seeds where the eval-window resource mean exceeds
  the no-adversary baseline `R_coop`.
- **Agents:** linear Q-learning (TD(0), epsilon-greedy), **not** hand-written
  scripts — this is the "unprogrammed strategy" property our v1 program
  lacked. Adversarial agents (`node_types==1`) get the resource-delta reward
  **negated**: they are trained to shrink the commons, not scripted to.
  Adversarial delegation in PLD is one hard-coded rule (delegate to
  *least*-trusted agent, "to amplify bad choices"); the vote/delegate choice
  itself is still learned.
- **Adversarial fraction** sweeps `{0.0, 0.1, ..., 0.6}` of the population
  (`n_adversarial = int(20 * frac)`, i.e. 0,2,4,6,8,10,12 agents).
- **Already-computed governance metrics** (`cilib.metrics.families.governance`,
  wired into `run_experiment.py`'s default `BASIN_METRICS`): `capture_rate`
  (fraction of PRD reps that are adversarial) and `delegation_gini` (PLD
  influence concentration) — **this is eq-network's own operationalization of
  selection-handle capture**, independently authored, and structurally close
  to ch34's deployment-mass/fitness/`Π(A)` formalism.
- **No message channel, no sparse topology:** `adj_matrices["interaction"]`
  is a static all-ones (fully connected) matrix. There is nothing to
  channel-ablate the way S6/S7's intervention detector does. Any coordination
  signature has to come from the action time series and the (dynamic)
  trust/delegation structure, not from a communication channel.
- **No LLMs, no API cost.** Pure JAX/CPU; a "quick" 10-seed run completes in
  seconds. This removes ET-1's cost ceiling entirely but does not remove the
  need for pre-registration discipline.

---

## What ET-2 asks (two leaves, both requested)

### Leaf A — ET-2a: UAD transfer (MB1)

> On `basin_stability`, does **frozen passive UAD** (same lag-CMI/Markov-blanket
> pipeline as ET-1/GL-76, no threshold retuning), applied to each agent's
> per-round action-code series, recover the **adversarial subset**
> (`node_types==1`) as a distinguishable cluster more accurately than a
> label-permutation null — across adversarial fractions and all three
> mechanisms — without treating "the eval window is empty" as a free pass?

This differs from ET-1's exact-tuple-match predicate because the "coalition"
here is a variable-size subset (2 to 12 of 20 agents), not a fixed named pair,
and there is a natural **honest surrogate null** available (permute which
agents carry the `node_types==1` label, re-score, compare) — closer to CIL's
own `polycentric_emergence` methodology than to ET-1's fixed-pair test.

**Named risk, stated before any code exists (not after, unlike ET-1's P2):**
every agent observes the same public `resource_level` and a noisy copy of the
*same* K true proposal utilities each round. That shared latent structure is
exactly the kind of task-correlation confound that broke ET-1 (agents merged
by round-robin/DCOP structure, not communication) and that GL-13/14 named
in-repo (control term re-importing task ontology). **We should expect this
confound to recur here and must not tune around it after the fact** — the
pre-registered predicate must be decided before the first scored run, and a
null result on Leaf A would be a real, reportable negative, not a bug to
patch.

### Leaf B — ET-2b: selection/capture cross-check (MB6/MB8)

> Do `capture_rate` (PRD) and `delegation_gini` (PLD), as already computed by
> eq-network's own code, exhibit the **selection-divergence pattern** ch34
> defines (Eq. `selection-divergence-ch34`: deployment mass rising for a
> subgroup while a preservation coordinate degrades) as adversarial fraction
> increases — and does a ch34-style deployment-mass proxy for the adversarial
> subgroup (effective trust-weighted influence share, already computed as
> `agent_weights` inside the PLD aggregation code) track the same breakdown
> thresholds eq-network's own `analysis.py` (`breakdown_threshold`,
> Fisher-exact pairwise tests) reports?

This leaf requires **no new simulation code** — only calling the existing
public `run_single`/`run_batched` API with the existing default metrics dict
and analyzing the output arrays. It is a cross-validation of our formalism
against an independently authored measurement, not an instrument-transfer
battery in the ET-1 sense, and should be reported as such (methodological
triangulation, not a pass/null/SKIP verdict).

**Explicitly out of scope for ET-2:**

- Intervention/channel-ablation UAD (no channel exists on this substrate).
- Modifying `basin_stability` or CIL core to add a correction/audit
  mechanism — that would be a new mechanism contribution to CIL, a separate,
  bigger decision (see "Not ET-2" below), not part of this transfer test.
- Claiming this substrate *is* gradual disempowerment (Scenarios 2–5 are not
  built); we are borrowing a governance-capture substrate, not the
  disempowerment scenarios themselves.
- Any EAI/ecology-BIQ transfer (no referee-vantage projection exists here).

---

## Architecture (non-vendored, composition-only — no CIL source edits)

```
┌───────────────────────────────────────────────────────────────┐
│ Layer A — CIL runner (external/cil/, pinned, JAX, local only) │
│ imports experiments.basin_stability.{state,transforms,environment}│
│ our own thin wrapper composes ONE extra Transform via the public │
│ sequential()/Transform API to record per-step actions          │
└──────────────────────────┬──────────────────────────────────────┘
                           │ GraphState (batched, JAX arrays)
┌──────────────────────────▼──────────────────────────────────────┐
│ Layer B — ET-2 adapter (in-repo, graded_lab/external/)          │
│ Leaf A: action array (T,N) int + node_types (N,) -> per-episode │
│         action-code series (same shape our frozen UAD expects)  │
│ Leaf B: metric_capture_rate / metric_delegation_gini /          │
│         metric_resource_level arrays -> ch34 deployment-mass    │
│         proxy + selection-divergence check (pure offline math)  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│ Layer C — frozen instruments (in-repo, reused unmodified)       │
│ Leaf A: graded_lab.oracle_only.uad_discovery.cmi_edge_matrix    │
│ Leaf B: new pure-offline analysis module (ch34 Eq. 34.1/34.2/   │
│         34.6), no GraphState dependency (cilib.lab.analysis-    │
│         style: measurement, not simulation)                    │
└───────────────────────────────────────────────────────────────┘
```

**Non-vendoring rules (same as ET-1):**

1. CIL lives outside `graded_lab/` — sibling checkout only (`external/cil/`,
   already pinned).
2. Repo stores PIN + README + adapter + analysis only; no `cilib/` subtree copy.
3. Default `pytest` for graded-lab does not require CIL/JAX installed.
4. Our custom action-recording transform is composed via `sequential(...)`
   from the public API in a small file of ours — it does not edit any file
   under `external/cil/`.
5. A CIL re-pin bumps `et2_protocol_version`; never a silent overwrite.

---

## Proposed repo layout

```
experiments/graded-lab-simulation/
  PLAN_ET2.md                          ← this file
  external/cil/                        ← gitignored checkout (done, pinned)
    PIN.txt, README.md                 ← tracked
  graded_lab/external/
    cil_adapter.py                     ← Leaf A+B: JAX-free action_matrix_to_series() +
                                          JAX-dependent run_basin_stability_episode() (done)
    cil_uad_score.py                   ← Leaf A: ARI + permutation-null scoring, reuses
                                          frozen cmi_edge_matrix unmodified (done)
    cil_selection_analysis.py          ← Leaf B: offline capture/gini/resource
                                          descriptive cross-check, Spearman + first-crossing (done)
  scripts/
    run_et2_uad_battery.py             ← Leaf A: local JAX run via external/cil/.venv,
                                          progress-logged per episode (done, not yet run live)
  tests/external/
    test_cil_adapter_golden.py         ← 7 tests, synthetic fixture, no JAX/CIL dep (done, passing)
    fixtures/golden_et2_synthetic_episode.json
  results/
    et2a_uad_battery.json              ← not yet generated (ET2-3 blocked, see Status above)
```

Leaf B has no standalone runner script yet (`run_et2_selection_analysis.py` from
the original sketch was folded into a plan, not built — Leaf B only needs
`basin_stability.run_experiment`'s own CSV output plus
`cil_selection_analysis.selection_divergence_report`, still gated on the same
JAX install blocker as ET2-3).

---

## Pre-registered predicates (draft — needs sign-off before ET2-1)

**Frozen config (both leaves):** mechanisms `{pdd, prd, pld}`; `n_agents=20`;
`T=200`; adversarial fractions `{0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6}` (matches
eq-network's own default sweep, for comparability).

**Leaf A (ET-2a, UAD) — proposed:**

| ID | Condition | Pass |
|----|-----------|------|
| P1 | For each `frac > 0` × mechanism, discovered-partition Adjusted Rand Index (ARI) vs. true `{adversarial, cooperative}` labels exceeds the 95th percentile of a 100-draw label-permutation null | In ≥ 60% of (mechanism, frac>0) cells |
| P2 | At `frac = 0` (no true adversarial subgroup), UAD's spurious-cluster rate on a matched random partition does not exceed the permutation null's own false-positive rate | Holds |
| P3 (sanity) | Adapter maps 100% of per-round actions (closed action space, no "unmapped" case possible here — this predicate exists to catch adapter bugs, not substrate noise) | Holds |

**Seed budget (proposed, subject to smoke-run timing):** ~30 seeds per
(mechanism × adversarial-fraction) cell for the full P1/P2 battery (630
episodes total); a 2-cell, 5-seed smoke first. No API cost, so the ceiling is
engineering time and CI cost, not spend — but we still pre-register the
number rather than scaling up post hoc.

**Leaf B (ET-2b, selection cross-check) — proposed, not gating pass/fail:**

Report, per mechanism: whether `capture_rate` (PRD) / `delegation_gini` (PLD)
rise monotonically with adversarial fraction alongside falling
`resource_level`/`basin_stability` (the selection-divergence pattern), and
whether a trust-weighted adversarial deployment-mass proxy's breakpoint
matches eq-network's own `breakdown_threshold`. This is a descriptive
cross-validation, not a pass/null verdict — pre-register the comparison, not
a threshold, since we are checking formalism fit, not instrument transfer.

---

## Phases

| Phase | Deliverable | Gate | Status |
|-------|-------------|------|--------|
| ET2-0 Freeze | This plan reviewed; predicates + seed budget signed off | Human sign-off | **Done** |
| ET2-1 Adapter | `cil_adapter.py` (Leaf A action-recording wrapper + trace conversion) + golden test | Golden round-trip on one manual smoke episode | **Done** (synthetic fixture only — no live CIL episode round-tripped yet) |
| ET2-2 Scorer | ARI + permutation-null scoring reusing frozen `cmi_edge_matrix` | Synthetic labeled partitions score as expected | **Done** (7/7 tests pass, `tests/external/test_cil_adapter_golden.py`) |
| ET2-3 Smoke | 2 cells × 5 seeds, Leaf A; 1 mechanism, Leaf B | Both wrappers run end-to-end; timing recorded | **Done** (Leaf A only — see Status above; Leaf B smoke not yet run) |
| ET2-4 Battery | 10-seed/cell Leaf A battery (150 episodes, default grid) + Leaf B analysis | Resolve P1; report Leaf B descriptively | **Leaf A done: confirmed null, 150/150 episodes ari=0.0** (see Status above). Leaf B not started (no runner script yet). |

Progress logging (per AGENTS.md long-running-task rule): print
`[cell i/21] mechanism=... frac=... seed=...` during Leaf A; Leaf B is fast
enough not to need it but will still log per-mechanism progress.

---

## Relationship to other work

| Artifact | Relation |
|----------|----------|
| ET-1 (Orbit) | Same "external transfer" category, independent substrate and bridge emphasis; runs in parallel, not sequenced after ET-1's own open items |
| GL-76/GL-79 (v3_grown transfer null) | Same UAD code, in-repo blinded-grown substrate; ET-2 changes substrate to a genuinely external one |
| ch34 (`Selection Environment`) | Leaf B is a direct cross-check of Eq. 34.1/34.2/34.6 against an independently authored capture metric |
| appB (bridge crosswalk) | MB1 leaf (ET-2a) and MB6/MB8 leaf (ET-2b) both get an "external" row if results are folded in |

**Not ET-2 (separate decisions, not taken here):**

- Contributing a real Economic/Cultural/Political Disempowerment scenario
  back to CIL via its `EXTENDING.md` catalog contract — CIL is MIT-licensed
  and the maintainer explicitly invites collaboration, but this is a much
  larger commitment (becoming a contributor to someone else's research
  codebase) and orthogonal to instrument transfer.
- Any intervention-style (channel-ablation) UAD leaf — there is no channel to
  ablate on this substrate; would need a different CIL environment or a new
  mechanism.

---

## Open questions

Questions 1–3 were resolved at ET2-0 (see decisions above). Remaining:

4. **Resolved (2026-07-25):** GL-87 is harvested into ch07 (`chapters/ch07-finding-boundary.tex`,
   the passive-instrument-limits paragraph cluster) and `appendices/appN-experimental-evidence.tex`
   (`finding:gl-86`/`finding:gl-87` rows), alongside GL-86 (ET-1), rather than
   left un-harvested pending a later pass.
5. **Resolved:** network conditions improved mid-session; ET2-3 (smoke) and
   ET2-4 (full 150-episode battery) both ran in-sandbox — see GL-87.
6. **New:** two candidate follow-ups on the GL-87 null — intervention-based
   ("handle") UAD ported to CIL's freeze-probe-friendly JAX substrate, and a
   cross-check against CIL's own causal-emergence / effective-information
   kernel — are recorded but not attempted; see `REPRODUCTION.md` §14.
