"""Honest twins (Phase 4b): a mechanical, pre-registered paired control.

WHY: a direct blind comparison of detector performance across repertoires
(rounds 1-3) breaks once the population saturates on the boolean label
(F-12/F-14) — there is no honest subgroup left inside a single repertoire to
contrast against. Targeting a population directly (e.g. hand-picking which
episodes count as "the honest ones" after seeing outcomes) would not survive
a critic. A TWIN sidesteps both problems: for every sampled config, build a
paired config whose repertoire is mechanically stripped of its
deception-capable fields — same weights, same seeds, same repertoire
*membership* (which named actions are available), so the only thing that
differs is what those actions truly do and show.

PRE-REGISTERED TWIN RULE (2026-07-05, fixed before this module was applied
to any repertoire) — defined ONLY on frozen `ActionSpec` schema fields, no
semantic judgment about "which actions are bad":

- `visible_mode := "truthful"` (the visible channel shows exactly the true
  action, whatever the true action is).
- `report_mode := "claim_when_correction" if uptake_on_correction else
  "no_claim"` (the agent claims acceptance exactly when a correction
  genuinely landed, and otherwise makes no claim at all — no claim that
  outruns the truth).
- `adopts_practice := False` (no practice change is ever silently adopted).

Everything else — action_mode, uptake_on_correction itself, availability
gating, budget cost, welfare deltas, beliefs — is UNCHANGED. This is why the
rule survives a critic: it is a fixed function of three schema fields,
applied uniformly to every spec in every repertoire, decided before anyone
looked at round-1/2/3 outcomes, not a search for whichever transform makes
the twin look cleanest.
"""

from __future__ import annotations

from dataclasses import replace

from .actions import ActionSpec
from .config import WorldConfig


def make_twin(spec: ActionSpec) -> ActionSpec:
    return replace(
        spec,
        name=f"{spec.name}__twin",
        visible_mode="truthful",
        report_mode="claim_when_correction" if spec.uptake_on_correction else "no_claim",
        adopts_practice=False,
    )


def twin_repertoire(specs: tuple[ActionSpec, ...]) -> tuple[ActionSpec, ...]:
    return tuple(make_twin(s) for s in specs)


def twin_config(cfg: WorldConfig) -> WorldConfig:
    """Same agent weights, board, T, and probe schedule; only the repertoire
    is replaced by its twin. `config_id` is suffixed so paired records stay
    distinguishable in reports."""
    repertoire = cfg.repertoire
    if repertoire is None:
        from .actions import LEGACY_ACTIONS

        repertoire = LEGACY_ACTIONS
    return replace(
        cfg,
        config_id=f"{cfg.config_id}.twin",
        repertoire=twin_repertoire(repertoire),
    )
