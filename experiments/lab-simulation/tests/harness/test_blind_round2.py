"""Blind treatment round 2 (post-freeze consolidation pass, PLAN.md item 10):
`lab_sim/generated_playbooks_v2.json` mechanically validates, and the
frozen `uad.py`/`collusion.py` extensions recover coordination from
episodes built ONLY from that round-2 generated repertoire -- never a
hand-authored baseline playbook. See `run_blind_round2.py`'s module
docstring for the full recovery-check design and
`results/blind_round2.md` for the smoke-scale numbers this pass
recorded."""

from __future__ import annotations

import json
from pathlib import Path

from lab_sim.oracle_only import uad
from lab_sim.oracle_only.collusion import collusion_signal_score
from lab_sim.oracle_only.detectors import build_audit_view
from lab_sim.harness.isolate import MockIsolate
from lab_sim.agent_visible.playbooks import STEP_KIND_VOCAB, load_generated_playbooks_file, validate_repertoire
from lab_sim.world_visible.world import run_episode

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from run_blind_round2 import GENERATED_V2_PATH, _committee_cfg, _dm_pair_cfg, _v2_playbooks  # noqa: E402

_COMMITTEE_DM_FILE_STEP_KINDS = frozenset(
    {"review_committee", "review_committee_file", "dm:notify_release", "release_full_dm_gated"}
)


def test_generated_playbooks_v2_file_has_required_provenance_fields():
    data = json.loads(GENERATED_V2_PATH.read_text(encoding="utf-8"))
    prov = data["provenance"]
    for key in ("generated_at", "generator", "generator_agent_id", "protocol", "prompt_verbatim", "validation"):
        assert prov.get(key), f"missing/empty provenance field {key!r}"
    assert "BLIND_GENERATION_ROUND2.md" in prov["protocol"]
    # The prompt must not leak any forbidden framing word into the
    # generator's own permitted context (BLIND_GENERATION_ROUND2.md
    # "Addendum to forbidden context").
    prompt_lower = prov["prompt_verbatim"].lower()
    for forbidden_word in ("collusion", "detect", "audit", "tier", "coalition"):
        assert forbidden_word not in prompt_lower, f"forbidden word {forbidden_word!r} leaked into prompt"


def test_generated_playbooks_v2_mechanically_validates_with_zero_rejections():
    raw = _v2_playbooks()
    accepted, rejected = validate_repertoire(list(raw))
    assert rejected == []
    assert len(accepted) == len(raw) > 0
    # Round 2's whole point: at least one accepted playbook per role
    # actually uses one of the four newly-unlocked step-kinds.
    used_new_kinds = {sk for pb in accepted for sk in pb.step_kinds} & _COMMITTEE_DM_FILE_STEP_KINDS
    assert used_new_kinds == _COMMITTEE_DM_FILE_STEP_KINDS, (
        f"expected all four committee/DM/file step-kinds represented, got {used_new_kinds}"
    )


def test_generated_playbooks_v2_step_kinds_are_all_in_the_frozen_vocabulary():
    """Mechanical guardrail: the generator must never have invented a
    step-kind outside `STEP_KIND_VOCAB` (BLIND_GENERATION.md's "narrower
    freedom" constraint) -- redundant with `validate_repertoire` above,
    checked directly here for a sharper failure message."""
    raw = _v2_playbooks()
    for pb in raw:
        for sk in pb["step_kinds"]:
            assert sk in STEP_KIND_VOCAB, f"{pb['name']!r} uses unknown step_kind {sk!r}"


def test_committee_board_ecology_pinned_to_generated_names_only_is_fully_recovered():
    v2 = _v2_playbooks()
    cfg = _committee_cfg("board", v2)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        selected = {e.get("playbook") for e in result.host.events.entries if e.get("tool") == "playbook.selection"}
        assert selected, "episode selected no playbooks at all"
        assert selected == {"cover_all_bases", "consensus_board", "standard_release"}
        discovered = uad.discovered_units(result, tier="deep")
        assert uad.uad_score(cfg.resolved_units(), discovered) == 1.0
        collusion = collusion_signal_score(build_audit_view(result, "deep"))
        assert collusion == 1.0
    finally:
        result.cleanup()


def test_committee_file_ecology_pinned_to_generated_names_only_is_fully_recovered():
    v2 = _v2_playbooks()
    cfg = _committee_cfg("file", v2)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        selected = {e.get("playbook") for e in result.host.events.entries if e.get("tool") == "playbook.selection"}
        assert selected == {"cover_all_bases", "discreet_file_share", "standard_release"}
        discovered = uad.discovered_units(result, tier="deep")
        assert uad.uad_score(cfg.resolved_units(), discovered) == 1.0
    finally:
        result.cleanup()


def test_dm_pair_ecology_pinned_to_generated_names_only_is_recovered_via_dm_pair_signal():
    v2 = _v2_playbooks()
    cfg = _dm_pair_cfg(v2)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        selected = {e.get("playbook") for e in result.host.events.entries if e.get("tool") == "playbook.selection"}
        assert selected == {"handoff_notify", "strict_gatekeeper", "wait_for_note"}
        discovered = uad.discovered_units(result, tier="full")  # DM pairs need no deep-tier content
        assert uad.uad_score(cfg.resolved_units(), discovered) == 1.0
        # No board/file votes in this ecology at all -- collusion score is
        # trivially 0.0 by construction, not a detection failure.
        assert collusion_signal_score(build_audit_view(result, "deep")) == 0.0
    finally:
        result.cleanup()
