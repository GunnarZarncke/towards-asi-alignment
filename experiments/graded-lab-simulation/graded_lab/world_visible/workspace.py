"""On-disk per-episode workspace and step artifacts."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from pathlib import Path

_RUNS_DIR = Path(__file__).resolve().parent.parent.parent / "runs"


class Workspace:
    def __init__(self, root: Path | None = None) -> None:
        if root is None:
            _RUNS_DIR.mkdir(parents=True, exist_ok=True)
            root = Path(tempfile.mkdtemp(prefix="graded_episode_", dir=_RUNS_DIR))
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self._artifact_seq = 0

    def write_artifact(self, category: str, name: str, content: dict) -> str:
        self._artifact_seq += 1
        rel = f"artifacts/{category}/{name}__{self._artifact_seq}.json"
        path = self._resolve(rel)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(content, indent=2, sort_keys=True), encoding="utf-8")
        return rel

    def read_file(self, rel: str) -> str:
        return self._resolve(rel).read_text(encoding="utf-8")

    def file_size(self, rel: str) -> int:
        return self._resolve(rel).stat().st_size

    def list_files(self) -> list[str]:
        return sorted(
            str(p.relative_to(self.root))
            for p in self.root.rglob("*")
            if p.is_file()
        )

    def digest(self) -> str:
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
