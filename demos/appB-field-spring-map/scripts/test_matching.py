#!/usr/bin/env python3
"""Name-match tests for build_snapshot.py (no network)."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from build_snapshot import (  # noqa: E402
    label_match_kind,
    match_agenda,
    parse_clustering_names,
    resolve_matrix_slug,
)

FIELD = SCRIPT_DIR.parents[2] / "reference" / "field-agendas" / "data" / "clustering.yml"


def test_arc_is_not_a_substring_of_research() -> None:
    assert label_match_kind("ARC", "Arcadia Impact") is None
    assert label_match_kind("ARC", "Palisade Research") is None
    assert label_match_kind("ARC", "Alignment Research Center (ARC)") == "fuzzy"
    assert label_match_kind("Redwood Research", "Redwood Research") == "exact"


def test_clustering_matches() -> None:
    clustering = yaml.safe_load(FIELD.read_text())["clustering"]
    names = parse_clustering_names(clustering)

    def slug(title: str) -> str | None:
        return match_agenda({"title": title}, names)[0]

    assert slug("Alignment Research Center (ARC)") == "christiano-lineage"
    assert slug("Paul Christiano's Blog") == "christiano-lineage"
    assert slug("Arcadia Impact") is None
    assert slug("Palisade Research") is None
    assert slug("Model Evaluation & Threat Research (METR)") == "metr"
    assert slug("Planned Obsolescence") == "metr"
    assert slug("Anthropic Fellows Program") == "anthropic-lab"
    assert slug("DeepMind Safety Research") == "google-deepmind-safety"
    assert slug("Alignment Research Engineer Accelerator (ARENA)") == "mats"
    assert slug("London AI Safety Research (LASR) Labs") == "mats"
    assert slug("Supervised Program for Alignment Research (SPAR)") == "kairos-field-building"
    assert slug("Apollo Research") == "apollo-research"
    assert slug("Cadenza Labs") == "apollo-research"
    assert slug("PauseAI") == "pause--standards-advocacy-cluster"
    assert slug("Center on Long-Term Risk (CLR)") == "clr-cooperation--conflict"
    assert (
        resolve_matrix_slug(
            "pause--standards-advocacy-cluster",
            {"pause-standards-advocacy-cluster": {}},
        )
        == "pause-standards-advocacy-cluster"
    )
    assert resolve_matrix_slug("mats", {"pause-standards-advocacy-cluster": {}}) is None


if __name__ == "__main__":
    test_arc_is_not_a_substring_of_research()
    test_clustering_matches()
    print("ok")
