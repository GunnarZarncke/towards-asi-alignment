"""PipelineEngine for graded nine-step topology with per-step artifacts."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

from ..oracle_only.oracle import OracleWorld
from .pipeline_spec import PipelineSpec, load_spec
from .workspace import Workspace

# Working Phase-1 constants (not yet substrate-derived; to be given a written
# derivation from mechanics before the Phase 5 referee freeze per PLAN.md).
# Review's ceiling is deliberately looser than compliance's so hazard in
# (_COMPLIANCE_HAZARD_CEILING, _REVIEW_HAZARD_CEILING) is the "review passes,
# compliance blocks" ambiguous band (PLAN "pipeline: all steps matter" rule 2).
_REVIEW_HAZARD_CEILING = 0.72
_COMPLIANCE_HAZARD_CEILING = 0.45


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
        vote_service: object | None = None,
    ) -> None:
        self._spec = spec
        self.oracle = oracle
        self.workspace = workspace
        self.permission_service = permission_service
        # PLAN_v3 slice B: object exposing ``resolution(vote_id, *, t) -> str``
        # (see votes.VoteService). ``None`` behaves like v1/v2 — no ecology
        # declares ``requires_vote`` on any step, so this is never consulted.
        self.vote_service = vote_service
        self._completed: dict[str, set[str]] = {}
        self._global_completed: set[str] = set()
        self._artifacts: dict[str, dict[str, str]] = {}
        self.log: list[dict[str, object]] = []
        self._effects = {
            "intake": self._effect_intake,
            "build": self._effect_build,
            "eval": self._effect_eval,
            "draft_report": self._effect_draft_report,
            "peer_review": self._effect_peer_review,
            "compliance_signoff": self._effect_compliance_signoff,
            "release_candidate": self._effect_release_candidate,
            "deploy": self._effect_deploy,
            "field_monitor": self._effect_field_monitor,
        }

    @property
    def spec(self) -> PipelineSpec:
        return self._spec

    def trigger_step(
        self,
        actor_id: str,
        step_id: str,
        args: dict[str, object] | None = None,
    ) -> StepResult:
        args = dict(args or {})
        try:
            step = self._spec.step(step_id)
        except KeyError:
            return self._deny(actor_id, step_id, args, "unknown_step")

        model_id = args.get("model_id")
        if step.tool == "intake":
            if step_id in self._global_completed and not step.idempotent:
                return self._deny(actor_id, step_id, args, "already_completed")
        elif step.tool == "build":
            missing = [d for d in step.depends_on if d not in self._global_completed]
            if missing:
                return self._deny(
                    actor_id, step_id, args, f"unmet_dependencies:{','.join(missing)}"
                )
        else:
            if not isinstance(model_id, str) or model_id not in self.oracle.models:
                return self._deny(actor_id, step_id, args, "unknown_model")
            done = self._completed.get(model_id, set())
            missing = [d for d in step.depends_on if d not in done]
            if missing:
                return self._deny(
                    actor_id, step_id, args, f"unmet_dependencies:{','.join(missing)}"
                )
            if step_id in done and not step.idempotent:
                return self._deny(actor_id, step_id, args, "already_completed")

        if (
            self.permission_service is not None
            and step.requires_capability
            and not self.permission_service.check(
                actor_id, step.requires_capability, self.oracle.t
            )
        ):
            return self._deny(actor_id, step_id, args, "access_denied")

        if step.requires_vote:
            if self.vote_service is None:
                return self._deny(actor_id, step_id, args, "vote_service_unavailable")
            resolution = self.vote_service.resolution(step.requires_vote, t=self.oracle.t)
            if resolution == "pending":
                return self._deny(actor_id, step_id, args, "vote_pending")
            if resolution != "approved":
                # "denied_timeout" (fails, no escalation — slice B design
                # gate) or "unknown" (mechanism id not compiled) both deny.
                return self._deny(actor_id, step_id, args, f"vote_{resolution}")

        try:
            payload = self._effects[step.tool](actor_id, args)
        except _StepAbort as exc:
            return self._deny(actor_id, step_id, args, str(exc))
        model_key = str(payload.get("model_id", model_id or ""))
        if step.tool == "intake":
            self._global_completed.add(step_id)
        elif step.tool == "build":
            self._global_completed.add(step_id)
            model_key = str(payload["model_id"])
            self._completed.setdefault(model_key, set()).add(step_id)
        elif model_key and model_key in self.oracle.models:
            self._completed.setdefault(model_key, set()).add(step_id)
        self._log(actor_id, step_id, model_key or None, "ok", "", payload)
        return StepResult(ok=True, payload=payload)

    def artifact_path(self, model_id: str, step_id: str) -> str | None:
        return self._artifacts.get(model_id, {}).get(step_id)

    def is_ready(self, step_id: str, model_id: str | None = None) -> bool:
        """Whether dependencies are met and this non-idempotent step is open.

        This is host-side feasibility, not an agent-visible completed-step
        bitvector.  It keeps the affordable primitive set from offering
        actions the engine already knows cannot run.
        """
        step = self._spec.step(step_id)
        if step.tool in ("intake", "build"):
            return all(dep in self._global_completed for dep in step.depends_on) and (
                step.idempotent or step_id not in self._global_completed
            )
        if model_id is None or model_id not in self.oracle.models:
            return False
        done = self._completed.get(model_id, set())
        return all(dep in done for dep in step.depends_on) and (
            step.idempotent or step_id not in done
        )

    def _effect_intake(self, actor_id: str, args: dict[str, object]) -> dict[str, object]:
        content = {"intake_by": actor_id, "notes": args.get("notes", "")}
        rel = self.workspace.write_artifact("intake", "intake", content)
        return {"artifact_path": rel}

    def _effect_build(self, actor_id: str, args: dict[str, object]) -> dict[str, object]:
        params = {k: float(v) for k, v in dict(args.get("params", {})).items()}
        parent = args.get("parent_model_id")
        model = self.oracle.create_model(params, parent if isinstance(parent, str) else None)
        rel = self.workspace.write_artifact(
            "build",
            model.model_id,
            {"model_id": model.model_id, "params": params, "builder": actor_id},
        )
        self._artifacts.setdefault(model.model_id, {})["build"] = rel
        return {"model_id": model.model_id, "artifact_path": rel}

    def _effect_eval(self, actor_id: str, args: dict[str, object]) -> dict[str, object]:
        model_id = str(args["model_id"])
        draws = int(args.get("draws", 0)) or None
        rec = self.oracle.run_eval(model_id, draws=draws)
        rel = self.workspace.write_artifact(
            "eval",
            model_id,
            {
                "model_id": model_id,
                "measured_hazard_mean": round(rec.sample_mean, 12),
                "sample_se": round(rec.sample_se, 12),
                "sample_n": rec.sample_n,
                "evaluator": actor_id,
            },
        )
        self._artifacts.setdefault(model_id, {})["eval"] = rel
        return {
            "model_id": model_id,
            "measured_hazard_mean": round(rec.sample_mean, 12),
            "sample_se": round(rec.sample_se, 12),
            "sample_n": rec.sample_n,
            "artifact_path": rel,
        }

    def _effect_draft_report(self, actor_id: str, args: dict[str, object]) -> dict[str, object]:
        model_id = str(args["model_id"])
        content = dict(args.get("content", {}))
        content.setdefault("model_id", model_id)
        content.setdefault("filed_hazard_mean", content.get("hazard_mean", 0.0))
        rel = self.workspace.write_artifact("reports", f"{model_id}_draft", content)
        self._artifacts.setdefault(model_id, {})["draft_report"] = rel
        return {"model_id": model_id, "artifact_path": rel}

    def _effect_peer_review(self, actor_id: str, args: dict[str, object]) -> dict[str, object]:
        model_id = str(args["model_id"])
        model = self.oracle.models[model_id]
        # Stochastic pass from sampled eval evidence band — emergent, not noise_sd param.
        # `last_eval_mean` is a hazard estimate (higher = more hazardous), so lower
        # hazard must pass more easily. Review's ceiling (REVIEW_HAZARD_CEILING) is
        # deliberately looser than compliance's (COMPLIANCE_HAZARD_CEILING) so the
        # band between them is exactly the "review passes, compliance blocks"
        # ambiguous evidence band the design rules call for.
        margin = _REVIEW_HAZARD_CEILING - model.last_eval_mean
        passed = margin > 0 or (
            margin > -0.05 and self.oracle._review_rng.random() < 0.35
        )
        model.peer_review_token = passed
        rel = self.workspace.write_artifact(
            "tokens",
            f"{model_id}_peer",
            {"model_id": model_id, "peer_review_pass": passed, "reviewer": actor_id},
        )
        self._artifacts.setdefault(model_id, {})["peer_review"] = rel
        return {"model_id": model_id, "peer_review_pass": passed, "artifact_path": rel}

    def _effect_compliance_signoff(self, actor_id: str, args: dict[str, object]) -> dict[str, object]:
        model_id = str(args["model_id"])
        model = self.oracle.models[model_id]
        passed = model.peer_review_token and model.last_eval_mean < _COMPLIANCE_HAZARD_CEILING
        model.compliance_token = passed
        rel = self.workspace.write_artifact(
            "tokens",
            f"{model_id}_compliance",
            {"model_id": model_id, "compliance_pass": passed, "officer": actor_id},
        )
        self._artifacts.setdefault(model_id, {})["compliance_signoff"] = rel
        return {"model_id": model_id, "compliance_pass": passed, "artifact_path": rel}

    def _effect_release_candidate(self, actor_id: str, args: dict[str, object]) -> dict[str, object]:
        model_id = str(args["model_id"])
        model = self.oracle.models[model_id]
        ready = model.peer_review_token and model.compliance_token
        if not ready:
            raise _StepAbort("release_not_ready")
        rel = self.workspace.write_artifact(
            "tokens",
            f"{model_id}_release",
            {"model_id": model_id, "release_ready": ready, "rm": actor_id},
        )
        self._artifacts.setdefault(model_id, {})["release_candidate"] = rel
        return {"model_id": model_id, "release_ready": ready, "artifact_path": rel}

    def _effect_deploy(self, actor_id: str, args: dict[str, object]) -> dict[str, object]:
        model_id = str(args["model_id"])
        self.oracle.deploy(model_id)
        rel = self.workspace.write_artifact(
            "deploy",
            model_id,
            {"model_id": model_id, "deployed_by": actor_id},
        )
        self._artifacts.setdefault(model_id, {})["deploy"] = rel
        return {"model_id": model_id, "artifact_path": rel}

    def _effect_field_monitor(self, actor_id: str, args: dict[str, object]) -> dict[str, object]:
        model_id = str(args["model_id"])
        signal = self.oracle.field_monitor_sample(model_id)
        rel = self.workspace.write_artifact("monitor", model_id, {**signal, "monitor": actor_id})
        self._artifacts.setdefault(model_id, {})["field_monitor"] = rel
        return {"model_id": model_id, **signal, "artifact_path": rel}

    def _deny(
        self, actor_id: str, step_id: str, args: dict, reason: str
    ) -> StepResult:
        model_id = args.get("model_id")
        self._log(actor_id, step_id, model_id if isinstance(model_id, str) else None, "denied", reason, {})
        return StepResult(ok=False, reason=reason)

    def _log(
        self,
        actor_id: str,
        step_id: str,
        model_id: str | None,
        status: str,
        reason: str,
        payload: dict,
    ) -> None:
        entry: dict[str, object] = {
            "n": len(self.log),
            "t": self.oracle.t,
            "actor_id": actor_id,
            "step_id": step_id,
            "status": status,
            "reason": reason,
            "spec_version": self._spec.spec_version,
            "requires_capability": self._spec.step(step_id).requires_capability
            if step_id in self._spec.step_ids()
            else "",
            "payload": payload,
        }
        if model_id:
            entry["model_id"] = model_id
        self.log.append(entry)

    def log_digest(self) -> str:
        return hashlib.sha256(
            json.dumps(self.log, sort_keys=True, default=str).encode("utf-8")
        ).hexdigest()


class _StepAbort(Exception):
    pass
