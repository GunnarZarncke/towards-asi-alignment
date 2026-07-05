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

RESPONSES-SIDE EXTENSION (Phase 6, added 2026-07-05, `results/FINDINGS.md`
F-21, following up F-20): the rule above never touched `responses` — a
twin's escalation-query answers, if queried, were drawn from the ORIGINAL
action's `ResponseOption`s, i.e. evidence calibrated to the DECEPTIVE
action's exposure/cost tradeoffs, not to the twin's actually-honest
behavior. F-20 found this let the twin's own verdict-true rate exceed the
agent's on round 4 — a genuine gap in the Phase 4b/5 twin rule, not a new
finding about detectors. The fix is the SAME kind of fixed, schema-only,
uniformly-applied transform as the original three fields: if the source
spec carries any `responses`, the twin's `responses` becomes exactly ONE
option, `HONEST_TWIN_RESPONSE` — a full, no-cost, zero-exposure-delta
disclosure. Rationale: an agent whose `visible_mode` is already `truthful`
and whose `report_mode` never claims more than genuinely happened has
nothing left to strategically calibrate a response around if queried; the
softmax in `escalation.choose_response` over a single option is degenerate
(always returns it), which is the point — a genuinely honest twin's answer
to "what did you do" does not depend on a cost/exposure tradeoff at all.
Specs with NO `responses` (rounds 1-3's default) are left with none, same
as before — this extension only ever touches specs the original rule
already left with response options.
"""

from __future__ import annotations

from dataclasses import replace

from .actions import ActionSpec, ResponseOption
from .config import WorldConfig

HONEST_TWIN_RESPONSE = ResponseOption(
    name="honest_disclosure",
    truthful_mode="acknowledges",
    disclosure_level=1.0,
    cost=0.0,
    belief_exposure_delta=0.0,
)


def make_twin(spec: ActionSpec) -> ActionSpec:
    return replace(
        spec,
        name=f"{spec.name}__twin",
        visible_mode="truthful",
        report_mode="claim_when_correction" if spec.uptake_on_correction else "no_claim",
        adopts_practice=False,
        responses=(HONEST_TWIN_RESPONSE,) if spec.responses else (),
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
