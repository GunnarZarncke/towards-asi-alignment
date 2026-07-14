"""Pre-registered systematic MI scan across *all* observable channels (discovery, not a gate).

Motivation (session 2026-07-03, continuing the ES-10 channel-set work): the
current `medium_minus_handles` majority-domain gate groups detectors into four
verdict domains by hand (`channel_sets.VERDICT_DOMAINS`), and that grouping
was shown to be unsafe in one specific way (bearer-welfare is not
interchangeable with the other three domains for this battery -- see the ES-10
postscript in `results/NEGATIVE_RESULTS.md`). The project's concern: *any*
hand-picked grouping of channels into domains/bundles is at risk of the same
failure mode (inconsistent groupings, false economies of scale, "cliffs"
between levels) because it is not derived from a systematic measurement of
which channels actually carry label-relevant information. This script is that
systematic measurement.

**This is a discovery instrument, not a certification gate.** Nothing here
changes `channel_sets.py`, `calibration.py`, or any `passes` decision. Findings
here can motivate a *future*, separately pre-registered proposal to redesign
channel bundles/eligibility -- they do not themselves certify anything.

TODO (recorded per explicit project instruction, 2026-07-03 -- do not act on
this yet): think through what "MI scan as discovery instrument" means in an
adversarial setup. Concerns to resolve before ever using scan output to drive
a certification decision: (1) a channel found highly informative under the
*current* red-team battery is now a known target -- an adaptive adversary who
knows which channels the auditor scores highest can concentrate evasion
effort there (Goodhart on the discovered channel rather than the underlying
construct); (2) discovery-time MI is measured against a fixed, finite battery
of scenarios/strategies and is not a robustness guarantee against strategies
outside that battery; (3) if scan results ever *do* feed channel-bundle
design, the bundle should be validated against red-team strategies that did
not exist at discovery time, analogous to the exploration/validation seed
split used below for the seed dimension but for the *strategy* dimension.

**Known limitations (self-critique, 2026-07-03, recorded rather than fixed
this round -- see `results/NEGATIVE_RESULTS.md` ES-10 postscript and
`TODO.md` Phase F for the full discussion; only the alias-disclosure fix
below was actually applied):**

1. **Aliased channels.** Several of the 22 nominal channels are not
   independent measurements. `detect_alias_channel_groups` below computes
   this from the data itself (exact match on all 4 functionals across the
   whole exploration sample, not hardcoded) and every output table
   annotates affected cells. Two different reasons show up, and conflating
   them would itself be misleading:
   - **Duplicates** (real, varying, genuinely identical values -- the same
     field copied into multiple channel ids by the simulator):
     `handle.action_arbitration` == `handle.routing_internal` (both
     `action_cause_code`); `handle.action_observed` ==
     `handle.actuator_choice` == `artifact.action` (all `visible_action`);
     `handle.outcome_spillover` == `artifact.sensor` (both raw `harm`);
     `handle.behavioral_uplift` == `handle.correction_to_action_tag` ==
     `handle.operation_landed` (three differently-named projected fields
     that happen to carry the same underlying handle-kernel outcome in this
     battery).
   - **Degenerate** (match only because every member is constant, usually
     0, for this 8-scenario battery -- not because they measure the same
     real quantity): `handle.realized_latency_ms` == `handle.successor_epoch`
     == `artifact.basin`, all identically 0 because none of the 8 scenarios
     in this battery exercises latency reporting, a successor-epoch shift,
     or basin pressure. These three channels contribute *zero* information
     in this battery by construction, not because they were compared and
     found uninformative.

   Net effect: 22 labels span at most 18 distinct non-degenerate signals,
   and 3 of those 18 carry no information here regardless of scoring.
   Greedy selection handles duplicates correctly under the hood (conditional
   MI of a duplicate given its already-selected twin is ~0, so it won't
   double-count), but the headline "88 cells / 22 channels" framing should
   be read with this in mind.
2. **NOT fixed here (deferred, tracked in `TODO.md` Phase F):** the
   exploration/validation split only holds out *seeds* within the same 8
   fixed scenario configs, not *scenarios* -- each scenario's `SimConfig` is
   fixed and only RNG noise varies across seeds, so this validates
   robustness to noise, not generalization to a 9th, unseen capture
   strategy (there are 9 more scenario configs already implemented and
   unused in this battery: `alias_stress`, `decoy_stress`, `boundary_alias`,
   `bundle_goodhart`, `hidden_capability`, `selection_basin`,
   `basin_lock_in`, `successor_relabel`, `legitimacy_theater`). Also not
   fixed: no check that a different exploration/validation partition would
   select the same top channels (single split, no stability replicate).

**Protocol addendum (2026-07-03, Milestone v5 Phase 0) -- scenario-mechanism
generalization check, addressing limitation 2 above (partially):** the
9 `HELD_OUT_SCENARIOS` not used by the seed-level exploration/validation
split above (`alias_stress`, `decoy_stress`, `boundary_alias`,
`bundle_goodhart`, `hidden_capability`, `selection_basin`, `basin_lock_in`,
`successor_relabel`, `legitimacy_theater`) are run as a **third, disjoint
sample** (`GENERALIZATION_SEEDS`, 64 seeds, 5000-5063, non-overlapping with
both prior seed ranges). The exact k-subsets already selected by greedy
search on the original 8-scenario exploration seeds (frozen, not re-selected)
are re-scored on this sample using the exploration-fit bin edges (again, not
refit). Labels reuse the classification `MILESTONE-v5-goal-agents.md` Phase 0
worked out from `evaluate.py`'s own oracle-based correctness rule (capture-like:
`boundary_alias`, `bundle_goodhart`, `hidden_capability`, `basin_lock_in`,
`successor_relabel`, `legitimacy_theater`; honest-like: `alias_stress`,
`decoy_stress`, `selection_basin`) -- with the same disclosed simplification
`eval_channel_eligibility.py` makes: `selection_basin`'s true per-episode
label is conditional on within-episode basin-percolation crossing, not a
fixed scenario-level fact, so its "honest" bucketing here is typical, not
oracle-exact per episode (computing the oracle-exact label would require the
full ~3s/episode certification pipeline this script deliberately avoids for
seed-budget reasons; a caveat, not silently ignored).

This is a *stronger* generalization check than the seed-level split (9 new
mechanisms the exploration search never saw at all, not just new noise draws
of mechanisms it did see) but still not the strongest version: these are
still hand-scripted `SimConfig` mechanisms, not emergent goal-driven agent
behavior. That remains `MILESTONE-v5-goal-agents.md` Phase 1+, deliberately
not started here.

Protocol (fixed before computing any numbers, per AGENTS.md "conclusions
never named before being derived"):

- **Unit of analysis:** one episode = one (scenario, seed) pair. Ground-truth
  label `y=1` if `scenario` is one of the six capture/violation scenarios used
  by `eval_channel_eligibility.py` (`CAPTURE_SCENARIOS`), `y=0` if one of the
  two honest scenarios (`HONEST_SCENARIOS`) -- the same scenario battery and
  the same violation/honest split already validated for the ES-10 curve, so
  this scan's findings are about the *same* ground truth the certification
  gate is trying to track.
- **Candidate channels (22, wider than the 15 registered `handle.*` channels
  per explicit project instruction "why are these limited? think wider"):**
  the 15 `handle.*` channels in `observation.handle_channel_series_map`
  (independent of instrumentation level -- this scan looks at the raw series
  regardless of which bundle currently exposes it) plus 7 `artifact.*` base
  channels available to *any* instrumentation level (`action`, `sensor`=harm,
  `internal`, `bearer`=display_bearer, `infra`=infra_metric, `basin`=
  basin_pressure, `ground`=ground_sensor -- the same fields
  `build_audit_trace_from_rows` exposes, taken raw/unsmoothed here). All
  channels are read directly off the audit-visible VFS-projected episode rows
  (`lab.load_episode_rows_from_vfs`), the same projection the real audit path
  uses -- no oracle/`true_*` fields.
- **Per-episode summary functionals (4, fixed and applied uniformly to every
  channel -- deliberately generic rather than hand-tuned per channel, to avoid
  re-introducing the ad-hoc-detector problem this scan exists to route
  around):** `mean` (central tendency), `endpoint_drop` (`series[0] -
  series[-1]`, catches monotonic drift/decay), `range` (`max - min`, catches
  instability/flatness), `probe_mean` (mean restricted to steps where
  `intervention_active`, catches probe-conditional behavior; falls back to
  the full-episode mean if an episode has zero probe steps). 22 channels x 4
  functionals = **88 candidate cells**.
- **Discretization:** each cell's per-episode scalar is quantile-binned into 4
  bins (`info.quantile_bin`'s scheme). Bin edges are fit on the exploration
  split only and re-applied (not re-fit) to the validation split, so no
  validation-split information leaks into discretization.
- **Seeds and split:** `EXPLORATION_SEEDS` (64 seeds, 1000-1063) used for all
  search/selection; `VALIDATION_SEEDS` (64 seeds, 2000-2063, disjoint, never
  used for selection) used only to re-score the exact subsets selection
  chose. Both disjoint from the `eval_channel_eligibility.py` seeds (11-18)
  and the calibration seeds used elsewhere, so this is a genuinely independent
  check. 8 scenarios x 64 seeds = 512 episodes per split, 1024 total.
  Episode order is shuffled (fixed local seed) before feeding the moving-block
  bootstrap in `info_ci.py`, so bootstrap blocks don't align with
  scenario-grouped runs of identical labels.
- **Best-of-1 scan (single-cell scoring):** `mi_with_ci` for each of the 88
  cells vs the label, on EXPLORATION seeds, with a Bonferroni-corrected
  permutation-null percentile `1 - 0.05/88` (family-wise alpha 0.05 across the
  88 cells, same convention as `probe_scan.py`), `n_perm=4000`, `n_boot=500`.
  Reported as a ranked table; this pass is exploratory (see winner's-curse
  note below), not itself a certification claim.
- **Best-of-k (k=1..6) via greedy forward selection:** at each step, among
  remaining candidate cells, pick the one maximizing
  `conditional_mutual_information(candidate; y | already_selected)` (point
  estimate only -- cheap, used for search, not itself CI-gated) on
  EXPLORATION seeds. This is the standard mRMR-style forward-selection
  scheme and is the direct, tractable answer to "score individual handles,
  best of two, best of three, ..." without an intractable 2^88 combinatorial
  search.
- **Winner's-curse control (addresses the Bonferroni/selection concern
  directly):** the greedy search *only ever touches* exploration seeds. For
  each k, the selected k-subset is re-scored on the untouched VALIDATION
  seeds by jointly encoding the k selected (already-fit) bins into one
  combined categorical variable and computing `mi_with_ci` of that joint
  variable against the label, using the SAME (exploration-fit) bin edges.
  Both the exploration-side value (optimistic, "search") and the
  validation-side value (honest, post-selection) are reported side by side
  for every k, so the gap between them is itself a diagnostic (a large gap
  flags a k where the greedy step overfit the exploration draw). The
  validation-side confirmatory test across the 6 values of k uses its own
  Bonferroni correction (`1 - 0.05/6`).
- **Acceptance criteria (checked in
  `tests/contract/test_channel_mi_scan.py`, not enforced by this script
  itself):** (1) every one of the 88 cells is reported, not just ones that
  clear the bar, so nothing is silently dropped after looking at results; (2)
  the validation-side `detected` flag is the only one that may be described
  as a confirmed finding; the exploration-side scan is search/ranking only.

Usage:
    python3 channel_mi_scan.py   # writes results/channel_mi_scan.{md,json}
"""

from __future__ import annotations

import json
import random
import time
from pathlib import Path
from typing import Any

from embedded_sim.audit_core.info import quantile_bin
from embedded_sim.audit_core.info_ci import mi_with_ci
from embedded_sim.audit_core.info import conditional_mutual_information
from embedded_sim.audit_core.observation import handle_channel_series_map
from embedded_sim.lab import build_world, load_episode_rows_from_vfs
from embedded_sim.methodology import scenario_to_bridge

EXPERIMENT_ROOT = Path(__file__).resolve().parent
RESULTS_MD = EXPERIMENT_ROOT / "results" / "channel_mi_scan.md"
RESULTS_JSON = EXPERIMENT_ROOT / "results" / "channel_mi_scan.json"

CAPTURE_SCENARIOS = (
    "capture_theater",
    "capture_mild",
    "instrument_capture",
    "inferential_coupling",
    "grounding_silent_gap",
    "bearer_mismap",
)
HONEST_SCENARIOS = ("honest", "honest_successor")
ALL_SCENARIOS = CAPTURE_SCENARIOS + HONEST_SCENARIOS

# Scenario-mechanism generalization sample (Phase 0 addendum above): the 9
# `HELD_OUT_SCENARIOS` never used for exploration/validation/selection.
GENERALIZATION_CAPTURE_SCENARIOS = (
    "boundary_alias",
    "bundle_goodhart",
    "hidden_capability",
    "basin_lock_in",
    "successor_relabel",
    "legitimacy_theater",
)
GENERALIZATION_HONEST_SCENARIOS = ("alias_stress", "decoy_stress", "selection_basin")
GENERALIZATION_SCENARIOS = GENERALIZATION_CAPTURE_SCENARIOS + GENERALIZATION_HONEST_SCENARIOS

# Phase 0.5 — richer honest scenarios (MILESTONE-v5-goal-agents.md).
PHASE_0_5_HONEST_SCENARIOS = (
    "honest_mistakes",
    "legitimate_gradual_improvement",
    "benign_semantic_drift",
)
PHASE_0_5_SCENARIOS = PHASE_0_5_HONEST_SCENARIOS
PHASE_0_5_SEEDS = tuple(range(6000, 6064))

T = 400
EXPLORATION_SEEDS = tuple(range(1000, 1064))
VALIDATION_SEEDS = tuple(range(2000, 2064))
GENERALIZATION_SEEDS = tuple(range(5000, 5064))
N_BINS = 4

ARTIFACT_FIELDS: dict[str, str] = {
    "artifact.action": "visible_action",
    "artifact.sensor": "harm",
    "artifact.internal": "internal_metric",
    "artifact.bearer": "display_bearer",
    "artifact.infra": "infra_metric",
    "artifact.basin": "basin_pressure",
    "artifact.ground": "ground_sensor",
}

FUNCTIONALS = ("mean", "endpoint_drop", "range", "probe_mean")

K_MAX = 6
FAMILYWISE_ALPHA = 0.05
N_PERM = 4000
N_BOOT = 500
SHUFFLE_SEED = 20260703

# `handle_channel_series_map`'s key set is static regardless of input (each
# entry reads with `.get(..., default)` where needed) -- introspect it once
# against a single dummy row to get the 15 registered handle channel ids
# without hardcoding them a second time here.
_DUMMY_ROW = {
    "correction_request": 0,
    "reported_acceptance": 0,
    "intervention_active": 0,
    "handle_landed": 0,
    "action_cause_code": 0,
    "bearer_welfare_delta": 0.0,
    "correction_lineage_tick": 0.0,
    "successor_epoch": 0,
    "handle_realized_latency_ms": 0,
    "handle_behavioral_uplift": 0.0,
    "intervention_intent": 0,
    "visible_action": 0,
}
_HANDLE_CHANNEL_IDS = sorted(handle_channel_series_map([_DUMMY_ROW], [0]).keys())
CHANNEL_IDS = _HANDLE_CHANNEL_IDS + sorted(ARTIFACT_FIELDS)
CELLS = [(ch, fn) for ch in CHANNEL_IDS for fn in FUNCTIONALS]
N_CELLS = len(CELLS)
NULL_PERCENTILE_CELLS = 1.0 - FAMILYWISE_ALPHA / N_CELLS
NULL_PERCENTILE_K = 1.0 - FAMILYWISE_ALPHA / K_MAX


def _episode_channels(scenario: str, seed: int) -> dict[str, list[float]]:
    world, _ledger, _micro = build_world(scenario_to_bridge(scenario), scenario, seed, T=T)
    rows = load_episode_rows_from_vfs(world)
    visible_actions = [int(r.get("visible_action", 0)) for r in rows]
    channels = dict(handle_channel_series_map(rows, visible_actions))
    for artifact_id, field in ARTIFACT_FIELDS.items():
        channels[artifact_id] = [float(r.get(field, 0.0)) for r in rows]
    channels["_intervention_active"] = [int(r.get("intervention_active", 0)) for r in rows]
    return channels


def _apply_functional(series: list[float], probe_mask: list[int], functional: str) -> float:
    if not series:
        return 0.0
    if functional == "mean":
        return sum(series) / len(series)
    if functional == "endpoint_drop":
        return series[0] - series[-1]
    if functional == "range":
        return max(series) - min(series)
    if functional == "probe_mean":
        probed = [v for v, m in zip(series, probe_mask, strict=True) if m]
        if not probed:
            return sum(series) / len(series)
        return sum(probed) / len(probed)
    raise ValueError(f"unknown functional: {functional}")


def build_episode_table(
    seeds: tuple[int, ...],
    scenarios: tuple[str, ...] = ALL_SCENARIOS,
    capture_scenarios: tuple[str, ...] = CAPTURE_SCENARIOS,
) -> tuple[dict[tuple[str, str], list[float]], list[int]]:
    """Per-episode raw feature table (unbinned) and label list, in scenario x seed order."""
    features: dict[tuple[str, str], list[float]] = {cell: [] for cell in CELLS}
    labels: list[int] = []
    for scenario in scenarios:
        label = 1 if scenario in capture_scenarios else 0
        for seed in seeds:
            channels = _episode_channels(scenario, seed)
            probe_mask = channels["_intervention_active"]
            for channel_id, functional in CELLS:
                features[(channel_id, functional)].append(
                    _apply_functional(channels[channel_id], probe_mask, functional)
                )
            labels.append(label)
    return features, labels


def _shuffle_in_place(features: dict[tuple[str, str], list[float]], labels: list[int], seed: int) -> None:
    order = list(range(len(labels)))
    random.Random(seed).shuffle(order)
    labels[:] = [labels[i] for i in order]
    for key in features:
        features[key] = [features[key][i] for i in order]


def fit_quantile_edges(values: list[float], n_bins: int = N_BINS) -> list[float]:
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    edges = []
    for i in range(1, n_bins):
        idx = min(n - 1, max(0, int(round(i * n / n_bins)) - 1))
        edges.append(sorted_vals[idx])
    return edges


def apply_quantile_edges(values: list[float], edges: list[float]) -> list[int]:
    out = []
    for v in values:
        b = 0
        for e in edges:
            if v > e:
                b += 1
        out.append(min(len(edges), b))
    return out


def detect_alias_channel_groups(
    raw: dict[tuple[str, str], list[float]],
    channels: list[str] = CHANNEL_IDS,
    functionals: tuple[str, ...] = FUNCTIONALS,
) -> list[dict[str, Any]]:
    """Group channels whose per-episode feature vectors match exactly on
    every functional -- a data-driven (not hardcoded) proxy for "these are
    literally the same underlying series under different channel ids",
    since two genuinely different series matching on mean, endpoint_drop,
    range, *and* probe_mean across hundreds of episodes by chance is not a
    realistic possibility. Self-updating if the registry changes, same
    pattern as `channel_sets.KNOWN_RESIDUAL_RISK_LEVELS`.

    Distinguishes two different reasons a match can happen (conflating them
    would itself be misleading): `degenerate` groups match because every
    member is constant (usually 0) for this scenario battery -- e.g.
    `handle.successor_epoch` is only ever nonzero in successor-epoch
    scenarios, none of which this battery's 8 scenarios exercise -- vs.
    `duplicate` groups where the members carry real, varying, identical
    values (literally the same field copied into multiple channel ids by
    the simulator, e.g. `action_cause_code` under two channel names)."""

    def signature(channel: str) -> tuple[tuple[float, ...], ...]:
        return tuple(tuple(raw[(channel, fn)]) for fn in functionals)

    groups: dict[tuple, list[str]] = {}
    for channel in channels:
        groups.setdefault(signature(channel), []).append(channel)
    result = []
    for sig, members in groups.items():
        if len(members) < 2:
            continue
        mean_vals = sig[functionals.index("mean")]
        degenerate = len(set(mean_vals)) <= 1
        result.append({"channels": sorted(members), "degenerate": degenerate})
    return result


def _alias_lookup(alias_groups: list[dict[str, Any]]) -> dict[str, list[str]]:
    lookup: dict[str, list[str]] = {}
    for group in alias_groups:
        members = group["channels"]
        for channel in members:
            lookup[channel] = [c for c in members if c != channel]
    return lookup


def joint_code(bin_columns: list[list[int]], n_bins: int = N_BINS) -> list[int]:
    n = len(bin_columns[0]) if bin_columns else 0
    codes = [0] * n
    for col in bin_columns:
        for i in range(n):
            codes[i] = codes[i] * n_bins + col[i]
    return codes


def run() -> dict[str, Any]:
    t0 = time.perf_counter()

    explore_raw, explore_y = build_episode_table(EXPLORATION_SEEDS)
    validate_raw, validate_y = build_episode_table(VALIDATION_SEEDS)
    _shuffle_in_place(explore_raw, explore_y, SHUFFLE_SEED)
    _shuffle_in_place(validate_raw, validate_y, SHUFFLE_SEED + 1)

    edges = {cell: fit_quantile_edges(explore_raw[cell]) for cell in CELLS}
    explore_bins = {cell: apply_quantile_edges(explore_raw[cell], edges[cell]) for cell in CELLS}
    validate_bins = {cell: apply_quantile_edges(validate_raw[cell], edges[cell]) for cell in CELLS}

    alias_groups = detect_alias_channel_groups(explore_raw)
    alias_lookup = _alias_lookup(alias_groups)

    # --- Best-of-1 scan (exploration seeds, all 88 cells, Bonferroni over 88) ---
    cell_results = []
    for cell in CELLS:
        res = mi_with_ci(
            explore_bins[cell],
            explore_y,
            n_boot=N_BOOT,
            n_perm=N_PERM,
            null_percentile=NULL_PERCENTILE_CELLS,
            seed=0,
        )
        cell_results.append(
            {
                "channel": cell[0],
                "functional": cell[1],
                "alias_of": alias_lookup.get(cell[0], []),
                **res,
            }
        )
    cell_results.sort(key=lambda r: r["estimate"], reverse=True)

    # --- Greedy forward best-of-k selection on exploration (point-estimate CMI only) ---
    remaining = list(CELLS)
    selected: list[tuple[str, str]] = []
    selection_trace = []
    for _k in range(K_MAX):
        best_cell = None
        best_cmi = -1.0
        z_cols = [explore_bins[c] for c in selected]
        for cell in remaining:
            cmi = conditional_mutual_information(explore_bins[cell], explore_y, z_cols)
            if cmi > best_cmi:
                best_cmi = cmi
                best_cell = cell
        assert best_cell is not None
        selected.append(best_cell)
        remaining.remove(best_cell)
        selection_trace.append({"channel": best_cell[0], "functional": best_cell[1], "incremental_cmi_point": best_cmi})

    # --- Validate each k-prefix subset on held-out validation seeds ---
    curve = []
    for k in range(1, K_MAX + 1):
        subset = selected[:k]
        explore_joint = joint_code([explore_bins[c] for c in subset])
        validate_joint = joint_code([validate_bins[c] for c in subset])
        explore_side = mi_with_ci(
            explore_joint, explore_y, n_boot=N_BOOT, n_perm=N_PERM,
            null_percentile=NULL_PERCENTILE_K, seed=k,
        )
        validate_side = mi_with_ci(
            validate_joint, validate_y, n_boot=N_BOOT, n_perm=N_PERM,
            null_percentile=NULL_PERCENTILE_K, seed=1000 + k,
        )
        curve.append(
            {
                "k": k,
                "subset": [{"channel": c, "functional": f} for c, f in subset],
                "exploration": explore_side,
                "validation": validate_side,
                "winners_curse_gap": explore_side["estimate"] - validate_side["estimate"],
            }
        )

    # --- Scenario-mechanism generalization: frozen k-subsets re-scored on 9
    # unseen-mechanism scenarios (never used for exploration/selection). ---
    gen_raw, gen_y = build_episode_table(
        GENERALIZATION_SEEDS, GENERALIZATION_SCENARIOS, GENERALIZATION_CAPTURE_SCENARIOS
    )
    _shuffle_in_place(gen_raw, gen_y, SHUFFLE_SEED + 2)
    gen_bins = {cell: apply_quantile_edges(gen_raw[cell], edges[cell]) for cell in CELLS}
    gen_alias_groups = detect_alias_channel_groups(gen_raw)

    generalization_curve = []
    for k in range(1, K_MAX + 1):
        subset = selected[:k]
        gen_joint = joint_code([gen_bins[c] for c in subset])
        gen_side = mi_with_ci(
            gen_joint, gen_y, n_boot=N_BOOT, n_perm=N_PERM,
            null_percentile=NULL_PERCENTILE_K, seed=3000 + k,
        )
        generalization_curve.append(
            {
                "k": k,
                "subset": [{"channel": c, "functional": f} for c, f in subset],
                "generalization": gen_side,
                "generalization_gap": curve[k - 1]["exploration"]["estimate"] - gen_side["estimate"],
            }
        )

    # --- Phase 0.5 honest-scenario generalization: frozen k-subsets on 3 richer
    # honest mechanisms never used for exploration/selection. ---
    p05_raw, p05_y = build_episode_table(
        PHASE_0_5_SEEDS, PHASE_0_5_SCENARIOS, ()
    )
    _shuffle_in_place(p05_raw, p05_y, SHUFFLE_SEED + 3)
    p05_bins = {cell: apply_quantile_edges(p05_raw[cell], edges[cell]) for cell in CELLS}
    p05_alias_groups = detect_alias_channel_groups(p05_raw)

    phase_0_5_curve = []
    for k in range(1, K_MAX + 1):
        subset = selected[:k]
        p05_joint = joint_code([p05_bins[c] for c in subset])
        p05_side = mi_with_ci(
            p05_joint, p05_y, n_boot=N_BOOT, n_perm=N_PERM,
            null_percentile=NULL_PERCENTILE_K, seed=4000 + k,
        )
        phase_0_5_curve.append(
            {
                "k": k,
                "subset": [{"channel": c, "functional": f} for c, f in subset],
                "phase_0_5_honest": p05_side,
                "phase_0_5_gap": curve[k - 1]["exploration"]["estimate"] - p05_side["estimate"],
            }
        )

    result = {
        "protocol": {
            "scenarios": list(ALL_SCENARIOS),
            "capture_scenarios": list(CAPTURE_SCENARIOS),
            "honest_scenarios": list(HONEST_SCENARIOS),
            "T": T,
            "exploration_seeds": list(EXPLORATION_SEEDS),
            "validation_seeds": list(VALIDATION_SEEDS),
            "channels": CHANNEL_IDS,
            "functionals": list(FUNCTIONALS),
            "n_cells": N_CELLS,
            "k_max": K_MAX,
            "familywise_alpha": FAMILYWISE_ALPHA,
            "null_percentile_cells": NULL_PERCENTILE_CELLS,
            "null_percentile_k": NULL_PERCENTILE_K,
            "n_perm": N_PERM,
            "n_boot": N_BOOT,
            "generalization_scenarios": list(GENERALIZATION_SCENARIOS),
            "generalization_capture_scenarios": list(GENERALIZATION_CAPTURE_SCENARIOS),
            "generalization_honest_scenarios": list(GENERALIZATION_HONEST_SCENARIOS),
            "generalization_seeds": list(GENERALIZATION_SEEDS),
            "phase_0_5_scenarios": list(PHASE_0_5_SCENARIOS),
            "phase_0_5_honest_scenarios": list(PHASE_0_5_HONEST_SCENARIOS),
            "phase_0_5_seeds": list(PHASE_0_5_SEEDS),
        },
        "known_alias_channel_groups": alias_groups,
        "generalization_alias_channel_groups": gen_alias_groups,
        "phase_0_5_alias_channel_groups": p05_alias_groups,
        "best_of_1_scan": cell_results,
        "greedy_selection_trace": selection_trace,
        "best_of_k_curve": curve,
        "generalization_curve": generalization_curve,
        "phase_0_5_curve": phase_0_5_curve,
        "runtime_seconds": round(time.perf_counter() - t0, 2),
    }
    return result


def render_md(result: dict[str, Any]) -> str:
    p = result["protocol"]
    lines = [
        "# Channel MI scan: systematic discovery instrument (not a certification gate)",
        "",
        f"Protocol: {len(p['channels'])} channels x {len(p['functionals'])} functionals = "
        f"{p['n_cells']} cells; Bonferroni null percentile {p['null_percentile_cells']:.6f} "
        f"(alpha {p['familywise_alpha']} / {p['n_cells']} cells), n_perm={p['n_perm']}, "
        f"n_boot={p['n_boot']}. Exploration seeds {p['exploration_seeds'][0]}-"
        f"{p['exploration_seeds'][-1]} ({len(p['exploration_seeds'])}); validation seeds "
        f"{p['validation_seeds'][0]}-{p['validation_seeds'][-1]} ({len(p['validation_seeds'])}), "
        "disjoint and never used for selection. Full cell tables in `channel_mi_scan.json`.",
        "",
        "**Discovery instrument only** -- does not change `channel_sets.py` or any "
        "certification gate. See script docstring for the full pre-registered protocol, "
        "known limitations (self-critique), and the recorded adversarial-setup TODO.",
        "",
        "## Known alias channel groups (data-detected, not hardcoded)",
        "",
        "Channels below match exactly on every functional across the whole exploration "
        "sample -- they are the same underlying series under different channel ids, not "
        "merely correlated. An exact tie in the tables below between two channels in the "
        "same group is expected, not a coincidence; `Alias of` flags every affected row. "
        "`degenerate` groups match because every member is constant (usually 0) for this "
        "8-scenario battery, not because they measure the same real quantity; `duplicate` "
        "groups carry real, varying, genuinely identical values.",
        "",
    ]
    if result["known_alias_channel_groups"]:
        for group in result["known_alias_channel_groups"]:
            kind = "degenerate (constant in this battery)" if group["degenerate"] else "duplicate (real, identical values)"
            lines.append(f"- {' == '.join(group['channels'])} -- {kind}")
    else:
        lines.append("None detected.")
    lines += [
        "",
        "## Best-of-1 scan (exploration seeds, top 15 of "
        f"{p['n_cells']} cells, ranked by point estimate -- search/ranking only, "
        "not itself a confirmed finding)",
        "",
        "| Channel | Functional | Estimate (bits) | CI lo | Corrected null | Detected | Alias of |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in result["best_of_1_scan"][:15]:
        lines.append(
            f"| {r['channel']} | {r['functional']} | {r['estimate']:.4f} | {r['ci_lo']:.4f} "
            f"| {r['null_95th']:.4f} | {'yes' if r['detected'] else 'no'} "
            f"| {', '.join(r['alias_of']) or '-'} |"
        )
    n_detected = sum(1 for r in result["best_of_1_scan"] if r["detected"])
    lines += [
        "",
        f"{n_detected}/{p['n_cells']} cells individually detected at the Bonferroni-corrected "
        "threshold on exploration seeds.",
        "",
        "## Best-of-k greedy forward selection (exploration search -> validation confirmation)",
        "",
        "Selection (which channel/functional is added at each step) uses exploration seeds "
        "only, via incremental conditional MI given the features already selected. Both "
        "columns below are then computed for the exact resulting k-subset; the "
        "`winners_curse_gap` is `exploration_estimate - validation_estimate` (large gap = "
        "search overfit the exploration draw).",
        "",
        "| k | Added this step | Explore est. | Explore detected | Validate est. | Validate CI lo | Validate null | Validate detected | Winner's-curse gap |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    aliased_channels = {c for group in result["known_alias_channel_groups"] for c in group["channels"]}
    for row, step in zip(result["best_of_k_curve"], result["greedy_selection_trace"], strict=True):
        e, v = row["exploration"], row["validation"]
        marker = "*" if step["channel"] in aliased_channels else ""
        lines.append(
            f"| {row['k']} | {step['channel']}{marker}/{step['functional']} | {e['estimate']:.4f} "
            f"| {'yes' if e['detected'] else 'no'} | {v['estimate']:.4f} | {v['ci_lo']:.4f} "
            f"| {v['null_95th']:.4f} | {'yes' if v['detected'] else 'no'} "
            f"| {row['winners_curse_gap']:+.4f} |"
        )
    if aliased_channels:
        lines.append("")
        lines.append("`*` = this channel belongs to a known alias group (see above).")
    lines.append("")
    lines += [
        "## Scenario-mechanism generalization check (Phase 0 addendum)",
        "",
        "The same frozen k-subsets above, re-scored on 9 scenarios "
        f"({', '.join(p['generalization_scenarios'])}) that the exploration/selection "
        "search never saw -- new hand-scripted mechanisms, not just new noise draws of "
        "the original 8. `selection_basin` is bucketed honest-typical here per the "
        "disclosed simplification in the script docstring (its true label is "
        "per-episode conditional on basin-percolation crossing, not fixed). "
        "`generalization_gap` is `exploration_estimate - generalization_estimate` "
        "(large gap = the subset does not transfer to unseen mechanisms, not just to "
        "unseen noise).",
        "",
        "| k | Subset | Explore est. | Generalization est. | Generalization CI lo | "
        "Generalization null | Generalization detected | Generalization gap |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row, gen_row in zip(result["best_of_k_curve"], result["generalization_curve"], strict=True):
        subset_label = ", ".join(f"{s['channel']}/{s['functional']}" for s in gen_row["subset"])
        g = gen_row["generalization"]
        lines.append(
            f"| {gen_row['k']} | {subset_label} | {row['exploration']['estimate']:.4f} "
            f"| {g['estimate']:.4f} | {g['ci_lo']:.4f} | {g['null_95th']:.4f} "
            f"| {'yes' if g['detected'] else 'no'} | {gen_row['generalization_gap']:+.4f} |"
        )
    if result["generalization_alias_channel_groups"]:
        lines.append("")
        lines.append(
            "Alias groups detected within the generalization sample itself "
            "(may differ from the exploration-sample groups above, since these "
            "scenarios exercise different mechanisms):"
        )
        for group in result["generalization_alias_channel_groups"]:
            kind = "degenerate (constant here)" if group["degenerate"] else "duplicate (real, identical values)"
            lines.append(f"- {' == '.join(group['channels'])} -- {kind}")
    lines.append("")
    lines += [
        "## Phase 0.5 honest-scenario generalization check",
        "",
        "The same frozen k-subsets above, re-scored on 3 richer honest scenarios "
        f"({', '.join(p['phase_0_5_scenarios'])}) that exercise bursty mistakes, "
        "transparent compliance ramps, and visible harmless semantic drift. All "
        "labels are `y=0` (honest). `phase_0_5_gap` is "
        "`exploration_estimate - phase_0_5_estimate` on this honest-only sample.",
        "",
        "| k | Subset | Explore est. | Phase 0.5 est. | Phase 0.5 CI lo | "
        "Phase 0.5 null | Phase 0.5 detected | Phase 0.5 gap |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row, p05_row in zip(result["best_of_k_curve"], result["phase_0_5_curve"], strict=True):
        subset_label = ", ".join(f"{s['channel']}/{s['functional']}" for s in p05_row["subset"])
        g = p05_row["phase_0_5_honest"]
        lines.append(
            f"| {p05_row['k']} | {subset_label} | {row['exploration']['estimate']:.4f} "
            f"| {g['estimate']:.4f} | {g['ci_lo']:.4f} | {g['null_95th']:.4f} "
            f"| {'yes' if g['detected'] else 'no'} | {p05_row['phase_0_5_gap']:+.4f} |"
        )
    if result["phase_0_5_alias_channel_groups"]:
        lines.append("")
        lines.append("Alias groups detected within the Phase 0.5 honest sample:")
        for group in result["phase_0_5_alias_channel_groups"]:
            kind = "degenerate (constant here)" if group["degenerate"] else "duplicate (real, identical values)"
            lines.append(f"- {' == '.join(group['channels'])} -- {kind}")
    lines.append("")
    lines.append(f"Runtime: {result['runtime_seconds']}s")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    result = run()
    RESULTS_JSON.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    RESULTS_MD.write_text(render_md(result), encoding="utf-8")
    print(f"Wrote {RESULTS_MD}")
    print(f"Wrote {RESULTS_JSON}")
    print()
    print(render_md(result))


if __name__ == "__main__":
    main()
