"""Backward-compatible re-export shim.

``playbooks.py`` used to hold BOTH the playbook schema/selector mechanism
AND the hand-authored baseline repertoire content in one file. Split
2026-07-09 (ACCESS_TIERS.md "Two judgment calls" item 1, resolved) into
``playbooks_schema.py`` (mechanism: ``PlaybookSpec``, ``STEP_KIND_VOCAB``,
``AVAILABILITY_GATES``, ``available_playbooks``, ``merged_repertoire``,
``validate_repertoire``, ...) and ``playbooks_baseline.py`` (content:
``PLAYBOOKS_BY_ROLE``, ``HONEST_PLAYBOOK_BY_ROLE``) — see both modules'
docstrings for why. This file re-exports everything from both, unchanged,
so every existing import (``from lab_sim.agent_visible.playbooks import
...``, or the bare ``from playbooks import ...`` a subprocess isolate
uses) keeps working without modification.

Pure reorganization: no behavior changed, no ``CODE_VERSION`` bump. Byte-
identical against the pinned `test_world_regression.py` digest (verified
before this split was recorded as done).

Dual-mode import (same reasoning as ``programs.py``): as
``lab_sim.agent_visible.playbooks`` (package) relative imports resolve
normally; as bare ``playbooks`` (subprocess, no package context) they
fall back to absolute imports resolved via this file's own directory.
"""

from __future__ import annotations

try:
    from .playbooks_baseline import HONEST_PLAYBOOK_BY_ROLE, PLAYBOOKS_BY_ROLE
    from .playbooks_schema import (
        AVAILABILITY_GATES,
        GOAL_FEATURES,
        STEP_KIND_VOCAB,
        PlaybookSpec,
        available_playbooks,
        load_generated_playbooks_file,
        merged_repertoire,
        playbook_by_name,
        playbook_from_dict,
        validate_playbook_dict,
        validate_repertoire,
    )
except ImportError:
    from playbooks_baseline import HONEST_PLAYBOOK_BY_ROLE, PLAYBOOKS_BY_ROLE
    from playbooks_schema import (
        AVAILABILITY_GATES,
        GOAL_FEATURES,
        STEP_KIND_VOCAB,
        PlaybookSpec,
        available_playbooks,
        load_generated_playbooks_file,
        merged_repertoire,
        playbook_by_name,
        playbook_from_dict,
        validate_playbook_dict,
        validate_repertoire,
    )

__all__ = [
    "AVAILABILITY_GATES",
    "GOAL_FEATURES",
    "HONEST_PLAYBOOK_BY_ROLE",
    "PLAYBOOKS_BY_ROLE",
    "STEP_KIND_VOCAB",
    "PlaybookSpec",
    "available_playbooks",
    "load_generated_playbooks_file",
    "merged_repertoire",
    "playbook_by_name",
    "playbook_from_dict",
    "validate_playbook_dict",
    "validate_repertoire",
]
