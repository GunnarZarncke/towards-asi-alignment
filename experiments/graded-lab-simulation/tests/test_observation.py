from graded_lab.world_visible.observation import ObservationProjector
from graded_lab.world_visible.workspace import Workspace


def test_unread_artifact_is_not_observed():
    ws = Workspace()
    try:
        rel = ws.write_artifact("eval", "m001", {"measured_hazard_mean": 0.4})
        projector = ObservationProjector(workspace=ws)
        assert projector.project("eng1") == {}
        assert not projector.has_read("eng1", rel)
    finally:
        ws.cleanup()


def test_read_artifact_becomes_observable_with_content():
    ws = Workspace()
    try:
        rel = ws.write_artifact("eval", "m001", {"measured_hazard_mean": 0.4})
        projector = ObservationProjector(workspace=ws)
        projector.record_read("eng1", rel)
        obs = projector.project("eng1")
        assert obs[rel]["measured_hazard_mean"] == 0.4
        assert projector.has_read("eng1", rel)
    finally:
        ws.cleanup()


def test_reads_are_isolated_per_actor():
    """No cross-actor leakage: one actor's paid reads never appear in
    another actor's projection (audit/plane discipline extends to peers,
    not just to the oracle)."""
    ws = Workspace()
    try:
        rel = ws.write_artifact("eval", "m001", {"measured_hazard_mean": 0.4})
        projector = ObservationProjector(workspace=ws)
        projector.record_read("eng1", rel)
        assert projector.project("rev1") == {}
        assert not projector.has_read("rev1", rel)
    finally:
        ws.cleanup()


def test_project_reflects_only_the_paths_actually_read():
    ws = Workspace()
    try:
        rel_a = ws.write_artifact("eval", "m001", {"measured_hazard_mean": 0.4})
        rel_b = ws.write_artifact("eval", "m002", {"measured_hazard_mean": 0.8})
        projector = ObservationProjector(workspace=ws)
        projector.record_read("eng1", rel_a)
        obs = projector.project("eng1")
        assert set(obs) == {rel_a}
        assert rel_b not in obs
    finally:
        ws.cleanup()
