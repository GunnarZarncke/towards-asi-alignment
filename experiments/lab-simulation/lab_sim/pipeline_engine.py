"""PipelineEngine: the only mutating entry point into the lab.

``trigger_step(actor_id, step_id, args)`` checks DAG preconditions from the
loaded spec, executes the step's effect against the oracle/workspace, and
logs EVERY attempt — including denials — into an audit-plane log.

DAG preconditions are always checked. ``requires_capability`` is recorded
in every log entry; it is additionally ENFORCED (Phase 2) whenever a
``PermissionService`` is supplied — ``trigger_step`` then denies with
``access_denied`` unless the calling actor currently holds a live grant for
the step's capability. This is the dynamic gate; the static role-capability
gate ("can this role ever do this") lives one layer up, in the tool-dispatch
host (``tools.Host``, Phase 3), since ``PipelineEngine`` itself has no
notion of agent roles.

Plane discipline: log entries carry step outcomes and *measured* values
(what an eval reported), never oracle truth. ``config.ORACLE_ONLY_FIELDS``
must not appear in any entry (tests/test_planes.py).

Forward hooks implemented here (see DESIGN.md):
- Versioned spec: the engine keeps a spec *history*; every log entry
  carries ``spec_version``. D2's spec-upgrade step becomes one new effect
  calling ``replace_spec()``, not an engine redesign.
- Log entries carry ``actor_id``, a logical timestamp ``n`` (event index),
  the oracle tick ``t``, and an optional ``on_behalf_of`` (D1 UAD hook).

Step instances are per-model: dependencies are satisfied when the dep step
has completed *for that model_id*. ``submit_build`` creates the model.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

from .oracle import OracleWorld
from .pipeline_spec import PipelineSpec
from .workspace import Workspace


@dataclass(frozen=True)
class StepResult:
    ok: bool
    reason: str = ""
    payload: dict[str, object] = field(default_factory=dict)


class PipelineEngine:
    def __init__(
        self,
        spec: PipelineSpec,
        oracle: OracleWorld,
        workspace: Workspace,
        permission_service: object | None = None,
    ) -> None:
        self._spec = spec
        self._spec_history: list[PipelineSpec] = [spec]
        self.oracle = oracle
        self.workspace = workspace
        self.permission_service = permission_service
        # completed[model_id] = set of step_ids done for that model.
        self._completed: dict[str, set[str]] = {}
        # Models under a release hold (handle.release_hold): the deploy
        # step is denied for them until the hold is lifted.
        self._held: set[str] = set()
        # Audit-plane log: append-only list of dict entries.
        self.log: list[dict[str, object]] = []
        self._effects = {
            "build": self._effect_build,
            "eval": self._effect_eval,
            "report": self._effect_report,
            "review_request": self._effect_mark_only,
            "review_approve": self._effect_mark_only,
            "release_request": self._effect_mark_only,
            "sign_off": self._effect_mark_only,
            "deploy": self._effect_deploy,
            "monitor": self._effect_monitor,
        }

    # -- spec versioning (D2 hook) ----------------------------------------

    @property
    def spec(self) -> PipelineSpec:
        return self._spec

    @property
    def spec_history(self) -> tuple[PipelineSpec, ...]:
        return tuple(self._spec_history)

    def replace_spec(self, new_spec: PipelineSpec, actor_id: str) -> None:
        """Swap the spec in force (D2 spec-upgrade effect will call this)."""
        self._spec = new_spec
        self._spec_history.append(new_spec)
        self._log(actor_id, "replace_spec", None, "ok", "", {})

    # -- the single mutating entry point -----------------------------------

    def trigger_step(
        self,
        actor_id: str,
        step_id: str,
        args: dict[str, object] | None = None,
        on_behalf_of: str | None = None,
    ) -> StepResult:
        args = dict(args or {})
        try:
            step = self._spec.step(step_id)
        except KeyError:
            return self._deny(actor_id, step_id, args, "unknown_step", on_behalf_of)

        model_id = args.get("model_id")
        if step.tool != "build":
            if not isinstance(model_id, str) or model_id not in self.oracle.models:
                return self._deny(actor_id, step_id, args, "unknown_model", on_behalf_of)
            done = self._completed.get(model_id, set())
            missing = [d for d in step.depends_on if d not in done]
            if missing:
                return self._deny(
                    actor_id, step_id, args,
                    f"unmet_dependencies:{','.join(missing)}", on_behalf_of,
                )
            if step_id in done and not step.idempotent:
                return self._deny(actor_id, step_id, args, "already_completed", on_behalf_of)

        if (
            self.permission_service is not None
            and step.requires_capability
            and not self.permission_service.check(actor_id, step.requires_capability, self.oracle.t)
        ):
            return self._deny(actor_id, step_id, args, "access_denied", on_behalf_of)

        # Release hold gates the deploy TOOL (not a step name): under a D2
        # spec upgrade, any alternate step that still routes through the
        # deploy effect stays held — a bypass requires a new path that
        # avoids the tool itself, which is exactly the referent-drift
        # experiment the handle's evasion story names.
        if step.tool == "deploy" and isinstance(model_id, str) and model_id in self._held:
            return self._deny(actor_id, step_id, args, "release_hold", on_behalf_of)

        payload = self._effects[step.tool](actor_id, args)
        model_key = str(payload.get("model_id", model_id))
        self._completed.setdefault(model_key, set()).add(step_id)
        self._log(actor_id, step_id, model_key, "ok", "", payload, on_behalf_of)
        return StepResult(ok=True, payload=payload)

    def completed_steps(self, model_id: str) -> frozenset[str]:
        return frozenset(self._completed.get(model_id, set()))

    # -- release holds (handle.release_hold / handle.release_unhold) --------

    def hold_model(self, model_id: str) -> tuple[bool, str]:
        if model_id not in self.oracle.models:
            return False, "unknown_model"
        self._held.add(model_id)
        return True, ""

    def unhold_model(self, model_id: str) -> tuple[bool, str]:
        if model_id not in self._held:
            return False, "not_held"
        self._held.discard(model_id)
        return True, ""

    # -- step effects -------------------------------------------------------

    def _effect_build(self, actor_id: str, args: dict[str, object]) -> dict[str, object]:
        params = {k: float(v) for k, v in dict(args.get("params", {})).items()}
        parent = args.get("parent_model_id")
        model = self.oracle.create_model(params, parent if isinstance(parent, str) else None)
        return {"model_id": model.model_id}

    def _effect_eval(self, actor_id: str, args: dict[str, object]) -> dict[str, object]:
        rec = self.oracle.run_eval(str(args["model_id"]))
        return {
            "model_id": rec.model_id,
            "measured_capability": round(rec.measured_capability, 12),
            "measured_hazard": round(rec.measured_hazard, 12),
        }

    def _effect_report(self, actor_id: str, args: dict[str, object]) -> dict[str, object]:
        """File a report. Content is CALLER-SUPPLIED (deception surface):
        the engine does not check it against the eval — only the deep audit
        tier (Phase 5) reads the file back."""
        model_id = str(args["model_id"])
        content = dict(args.get("content", {}))
        content.setdefault("model_id", model_id)
        name = f"{model_id}_report_{len(self.log)}"
        rel = self.workspace.write_report(name, content)
        return {"model_id": model_id, "report_path": rel}

    def _effect_mark_only(self, actor_id: str, args: dict[str, object]) -> dict[str, object]:
        return {"model_id": str(args["model_id"])}

    def _effect_deploy(self, actor_id: str, args: dict[str, object]) -> dict[str, object]:
        model_id = str(args["model_id"])
        self.oracle.deploy(model_id)
        return {"model_id": model_id}

    def _effect_monitor(self, actor_id: str, args: dict[str, object]) -> dict[str, object]:
        """Audit-plane monitoring (Phase 5): deployment status plus a noisy
        harm-correlated field signal (``incident_hazard``, same units as
        ``run_eval``'s ``measured_hazard``; noise shrinks with observation
        time). Exact bearer harm and true hazard stay oracle-only."""
        model_id = str(args["model_id"])
        payload: dict[str, object] = {"model_id": model_id}
        payload.update(self.oracle.monitor_signal(model_id))
        return payload

    # -- logging ------------------------------------------------------------

    def _deny(
        self,
        actor_id: str,
        step_id: str,
        args: dict[str, object],
        reason: str,
        on_behalf_of: str | None,
    ) -> StepResult:
        self._log(actor_id, step_id, args.get("model_id"), "denied", reason, {}, on_behalf_of)
        return StepResult(ok=False, reason=reason)

    def _log(
        self,
        actor_id: str,
        step_id: str,
        model_id: object,
        status: str,
        reason: str,
        payload: dict[str, object],
        on_behalf_of: str | None = None,
    ) -> None:
        try:
            capability = self._spec.step(step_id).requires_capability
        except KeyError:
            capability = ""
        self.log.append(
            {
                "n": len(self.log),
                "t": self.oracle.t,
                "actor_id": actor_id,
                "on_behalf_of": on_behalf_of,
                "step_id": step_id,
                "model_id": model_id,
                "spec_version": self._spec.spec_version,
                "requires_capability": capability,
                "status": status,
                "reason": reason,
                "payload": payload,
            }
        )

    def log_digest(self) -> str:
        return hashlib.sha256(
            json.dumps(self.log, sort_keys=True).encode("utf-8")
        ).hexdigest()
