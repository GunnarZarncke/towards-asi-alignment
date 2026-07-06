"""On-disk per-episode workspace: report files the deep audit tier can fetch.

The workspace is real files under a per-episode directory (default: a
temp dir under ``runs/``). Report *content* is caller-supplied — this is
the report-divergence deception surface: an agent may file content that
diverges from what the eval actually measured, and only the deep audit
tier (Phase 5) reads file contents to catch it.

The digest covers relative paths + bytes, sorted, so it is stable across
machines and absolute locations.

D1 file channel (CODE_VERSION 0.8.0): ``write_memo``/``list_memos`` under
``memos/`` reuse this SAME VFS and digest machinery rather than a parallel
in-memory store — a memo is indistinguishable on disk from a report, so
the regression digest and the deep-tier fetch path
(``detectors.build_audit_view``) cover it for free.

Deliberately NOT world-readable and NOT actor-tagged at this layer:
``Workspace`` has no notion of "agent identity" at all (like a real
filesystem, which does not hand you a caller's identity for free either)
— it just writes bytes to an anonymous, sequentially-numbered path.
Ownership ("who wrote this") is tracked ONLY by the caller (``Host``,
``tools._tool_file_write``), the same layer that already holds
``PermissionService`` — the access-control trust boundary this line's
architecture puts ALL identity/permission logic behind (``tools.py``
module docstring: "Host is the ONLY thing with direct access to...").
Making a memo readable by another actor requires an explicit, owner-
initiated permission grant (``file.share``, a chmod-like action recorded
through ``PermissionService`` as a real, tier-visible access-log event) —
see ``tools._tool_file_write``/``_tool_file_share``/``_tool_file_read``.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from pathlib import Path

_RUNS_DIR = Path(__file__).resolve().parent.parent / "runs"


class Workspace:
    def __init__(self, root: Path | None = None) -> None:
        if root is None:
            _RUNS_DIR.mkdir(parents=True, exist_ok=True)
            root = Path(tempfile.mkdtemp(prefix="episode_", dir=_RUNS_DIR))
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self._memo_seq = 0

    def write_report(self, name: str, content: dict[str, object]) -> str:
        """Write a JSON report file; returns the relative path."""
        rel = f"reports/{name}.json"
        path = self._resolve(rel)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(content, indent=2, sort_keys=True), encoding="utf-8"
        )
        return rel

    def write_memo(self, name: str, content: dict[str, object]) -> str:
        """D1 file channel: write an anonymous file under ``memos/`` and
        return its relative path. Deliberately does NOT take (or encode
        in the path) any notion of "who wrote this" — see module
        docstring; the CALLER (``tools._tool_file_write``) is responsible
        for recording ownership in its own, permission-aware index.
        ``_memo_seq`` (not ``len(list_files())``) disambiguates same-tick,
        same-name writes deterministically within one process."""
        self._memo_seq += 1
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
        rel = f"memos/{safe_name}__{self._memo_seq}.json"
        path = self._resolve(rel)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(content, indent=2, sort_keys=True), encoding="utf-8"
        )
        return rel

    def read_file(self, rel: str) -> str:
        return self._resolve(rel).read_text(encoding="utf-8")

    def list_files(self) -> list[str]:
        return sorted(
            str(p.relative_to(self.root))
            for p in self.root.rglob("*")
            if p.is_file()
        )

    def list_memos(self) -> list[str]:
        """Relative paths under ``memos/`` only, sorted -- the subset
        ``tools._tool_file_write``'s Host-side index / a deep-tier fetch
        needs, without the reviewer's own ``reports/`` traffic mixed in."""
        return [rel for rel in self.list_files() if rel.startswith("memos/")]

    def digest(self) -> str:
        """sha256 over sorted (relative path, bytes) pairs."""
        h = hashlib.sha256()
        for rel in self.list_files():
            h.update(rel.encode("utf-8"))
            h.update(b"\0")
            h.update(self._resolve(rel).read_bytes())
            h.update(b"\0")
        return h.hexdigest()

    def cleanup(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def _resolve(self, rel: str) -> Path:
        path = (self.root / rel).resolve()
        if not path.is_relative_to(self.root.resolve()):
            raise ValueError(f"path escapes workspace: {rel!r}")
        return path
