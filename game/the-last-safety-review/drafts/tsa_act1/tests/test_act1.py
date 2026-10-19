"""Pytest-compatible wrappers for the Act I verifier."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine import Game
import check


def test_schema(): check.validate_schema(Game())
def test_abstract_solving(): check.abstract_exhaustive(Game())
def test_full_playthrough(): check.canonical_playthrough(Game())
def test_branch_variation(): check.branch_regression(Game())
def test_constructive_completion(): check.check_guaranteed_route(Game())
def test_random_history_completion(): check.randomized_recovery(Game(), trials=100, length=30)
