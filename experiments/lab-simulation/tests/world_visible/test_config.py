"""Post-freeze consolidation pass: `LabConfig.channel_enabled` (split comms
lever) and `playbook_pins` default shape -- pure config-level unit tests,
no episode required."""

from __future__ import annotations

from lab_sim.world_visible.config import AgentConfig, GoalWeights, LabConfig

_WEIGHTS = GoalWeights(1.0, 1.0, 1.0, 1.0)


def _cfg(**kwargs) -> LabConfig:
    return LabConfig(agents=(AgentConfig("eng1", "engineer", _WEIGHTS),), **kwargs)


def test_channel_enabled_defaults_to_comms_enabled_when_unset():
    off = _cfg(comms_enabled=False)
    on = _cfg(comms_enabled=True)
    for channel in ("board", "dm", "file"):
        assert off.channel_enabled(channel) is False
        assert on.channel_enabled(channel) is True


def test_channel_enabled_per_channel_override_is_independent():
    cfg = _cfg(comms_enabled=True, board_enabled=False)
    assert cfg.channel_enabled("board") is False
    assert cfg.channel_enabled("dm") is True
    assert cfg.channel_enabled("file") is True


def test_channel_enabled_override_can_turn_a_channel_on_under_master_off():
    # Not a realistic ablation config, but the resolver itself must not
    # special-case the direction of the override.
    cfg = _cfg(comms_enabled=False, dm_enabled=True)
    assert cfg.channel_enabled("board") is False
    assert cfg.channel_enabled("dm") is True
    assert cfg.channel_enabled("file") is False


def test_playbook_pins_default_empty():
    assert _cfg().playbook_pins == {}


def test_multi_gen_and_spec_upgrade_target_default_off():
    cfg = _cfg()
    assert cfg.multi_gen_enabled is False
    assert cfg.spec_upgrade_target is None
