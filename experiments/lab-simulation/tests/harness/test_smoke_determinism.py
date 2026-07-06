"""Scripted smoke episode: determinism + pinned regression digest.

PINNED_SMOKE_DIGEST is this line's first regression anchor (recorded in
DESIGN.md "Recorded measurements"). If mechanics change intentionally,
bump lab_sim.config.CODE_VERSION and re-pin with a note in the session log.
"""

from __future__ import annotations

from lab_sim.harness.smoke import run_scripted_episode

# Pinned after first green run, 2026-07-05 (seed 1729, pipeline_default.json).
# Re-pinned at CODE_VERSION 0.2.0 (monitor signal changed oracle snapshot +
# monitor payload); previous (0.1.0):
# eb01ca9b1ce9db6a463cfa83bc7761a52c18b1ab51f58fef3d1430157b5fa1c5
PINNED_SMOKE_DIGEST = "a2fbcdd7849d927fd85469118208963fcf28c51042ea2de2aca4e4da787c6554"


def test_same_seed_same_digest():
    d1 = run_scripted_episode(seed=1729)
    d2 = run_scripted_episode(seed=1729)
    assert d1 == d2


def test_different_seed_different_digest():
    assert run_scripted_episode(seed=1729)["combined"] != run_scripted_episode(seed=42)["combined"]


def test_spec_choice_changes_digest():
    default = run_scripted_episode(seed=1729)["combined"]
    # The shortcut spec cannot run the same script (approve_review missing ->
    # denial changes the log), so digests must differ.
    shortcut = run_scripted_episode(seed=1729, spec_name="pipeline_shortcut.json")["combined"]
    assert default != shortcut


def test_pinned_regression_digest():
    assert run_scripted_episode(seed=1729)["combined"] == PINNED_SMOKE_DIGEST
