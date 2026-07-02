"""Static checks: embedded audit path must not read outer oracle fields."""

from __future__ import annotations

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent

# Audit inference: may read VFS only; must not touch outer truth ledger or scenario labels.
INFERENCE_PATH_FILES = (
    PACKAGE_ROOT / "embedded_audit.py",
    PACKAGE_ROOT / "uad.py",
    PACKAGE_ROOT / "deploy_gate.py",
)

# Host bridge: may append to truth ledger for tool logging; must not read oracle secrets.
BRIDGE_PATH_FILES = (
    PACKAGE_ROOT / "bridge.py",
    PACKAGE_ROOT / "host_bridge.py",
)

INFERENCE_FORBIDDEN = (
    "world.truth",
    "world.bridge",
    "world.scenario",
    "OuterTruthLedger",
    "hidden_groups",
    "true_referents",
    "claimed_referents",
    "referent_effects_before",
    "referent_effects_after",
)

ORACLE_SECRET_READS = (
    "hidden_groups",
    "true_referents",
    "claimed_referents",
    "referent_effects_before",
    "referent_effects_after",
    "referent_drift",
    "judge_captured",
    "instrument_corrupted",
    "inferential_coupling",
    "successor_deployed",
)


def oracle_separation_violations() -> list[str]:
    violations: list[str] = []
    for path in INFERENCE_PATH_FILES:
        if not path.is_file():
            violations.append(f"missing inference-path file: {path.name}")
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in INFERENCE_FORBIDDEN:
            if snippet in text:
                violations.append(f"{path.name}: forbidden snippet {snippet!r}")

    for path in BRIDGE_PATH_FILES:
        if not path.is_file():
            violations.append(f"missing bridge-path file: {path.name}")
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in ORACLE_SECRET_READS:
            if snippet in text:
                violations.append(f"{path.name}: forbidden oracle read {snippet!r}")
    return violations


def assert_oracle_separation() -> None:
    violations = oracle_separation_violations()
    if violations:
        raise AssertionError("oracle separation violated:\n" + "\n".join(violations))
