"""Workspace: file writes, path safety, digest stability."""

from __future__ import annotations

import pytest

from lab_sim.world_visible.workspace import Workspace


def test_write_and_read_report(tmp_path):
    ws = Workspace(root=tmp_path / "ws")
    rel = ws.write_report("m001_report", {"measured_hazard": 0.1})
    assert rel == "reports/m001_report.json"
    assert '"measured_hazard": 0.1' in ws.read_file(rel)
    assert ws.list_files() == [rel]


def test_digest_depends_on_content_not_location(tmp_path):
    ws1 = Workspace(root=tmp_path / "a")
    ws2 = Workspace(root=tmp_path / "b")
    for ws in (ws1, ws2):
        ws.write_report("r", {"x": 1})
    assert ws1.digest() == ws2.digest()
    ws2.write_report("r2", {"x": 2})
    assert ws1.digest() != ws2.digest()


def test_path_escape_rejected(tmp_path):
    ws = Workspace(root=tmp_path / "ws")
    with pytest.raises(ValueError, match="escapes"):
        ws.read_file("../outside.txt")


def test_default_root_under_runs_and_cleanup():
    ws = Workspace()
    try:
        assert ws.root.parent.name == "runs"
    finally:
        ws.cleanup()
    assert not ws.root.exists()
