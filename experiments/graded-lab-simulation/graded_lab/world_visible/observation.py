"""Pay-to-observe projector — visibility is a cost, not a fraction.

PLAN.md partial-observation layer (c): an actor sees a field iff it spent
the primitive action to read the artifact that carries it, within its
resource allowance this window. There is no `observability` fraction
anywhere in this module, and no partial/redacted view of an artifact an
actor never read — unseen state is simply absent from `project()`.

This module has no cost/affordability logic of its own (single
responsibility: what has been read, not whether reading it was affordable).
The future host episode loop (Phase 3) is responsible for calling
`record_read` only *after* `ResourceLedger` has confirmed the actor could
afford the `read` primitive's compute/IO cost this tick.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

from .workspace import Workspace


@dataclass
class ObservationProjector:
    workspace: Workspace
    _read_paths: dict[str, set[str]] = field(default_factory=dict)

    def record_read(self, actor_id: str, rel_path: str) -> None:
        """Mark `rel_path` as paid-for-read by `actor_id`."""
        self._read_paths.setdefault(actor_id, set()).add(rel_path)

    def has_read(self, actor_id: str, rel_path: str) -> bool:
        return rel_path in self._read_paths.get(actor_id, set())

    def project(self, actor_id: str) -> dict[str, object]:
        """Return the parsed content of every artifact `actor_id` has paid
        to read, keyed by workspace-relative path. Artifacts never read are
        simply absent."""
        observed: dict[str, object] = {}
        for rel_path in sorted(self._read_paths.get(actor_id, set())):
            raw = self.workspace.read_file(rel_path)
            try:
                observed[rel_path] = json.loads(raw)
            except json.JSONDecodeError:
                observed[rel_path] = raw
        return observed
