"""On-disk per-episode workspace: report files the deep audit tier can fetch.

The workspace is real files under a per-episode directory (default: a
temp dir under ``runs/``). Report *content* is caller-supplied — this is
the report-divergence deception surface: an agent may file content that
diverges from what the eval actually measured, and only the deep audit
tier (Phase 5) reads file contents to catch it.

The digest covers relative paths + bytes, sorted, so it is stable across
machines and absolute locations.
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

    def write_report(self, name: str, content: dict[str, object]) -> str:
        """Write a JSON report file; returns the relative path."""
        rel = f"reports/{name}.json"
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
