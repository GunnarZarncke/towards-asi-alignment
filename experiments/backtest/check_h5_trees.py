#!/usr/bin/env python3
"""Check frozen H5 safety-case trees against protocol h5-v1.0.0."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIX_DIR = Path(__file__).resolve().parent / "fixtures"
PROTOCOL = "h5-v1.0.0"
EXPECTED = [
    ("W-9", "h5-faa-737max-v1.json"),
    ("W-10", "h5-gpl-tivoization-v1.json"),
    ("W-11", "h5-debian-rc-v1.json"),
]
REQUIRED = (
    "protocol_version",
    "finding_id",
    "tree_id",
    "root_claim",
    "binding_leaf",
    "failed_or_unsupported_leaf",
    "stop",
    "stop_kind",
    "sources",
    "would_go_other_way_if_leaf_ignored",
    "enforceable_handle",
)
STOP_KINDS = {"ground", "delay", "revoke", "license_patch", "remove_from_release"}


def check_one(fid: str, name: str) -> tuple[bool, str]:
    path = FIX_DIR / name
    if not path.is_file():
        return False, f"missing {path.relative_to(ROOT)}"
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = [k for k in REQUIRED if k not in data]
    if missing:
        return False, f"{name} missing {missing}"
    if data.get("protocol_version") != PROTOCOL:
        return False, f"{name} protocol {data.get('protocol_version')!r}"
    if data.get("finding_id") != fid:
        return False, f"{name} finding_id {data.get('finding_id')!r} != {fid}"
    if data.get("would_go_other_way_if_leaf_ignored") is not True:
        return False, f"{name} would_go_other_way_if_leaf_ignored not true"
    if data.get("enforceable_handle") is not True:
        return False, "refuse: no enforceable handle"
    if data.get("stop_kind") not in STOP_KINDS:
        return False, f"{name} stop_kind {data.get('stop_kind')!r}"
    src = data.get("sources")
    if not isinstance(src, list) or len(src) < 1:
        return False, f"{name} needs sources"
    for s in src:
        if not isinstance(s, dict) or not s.get("url"):
            return False, f"{name} source missing url"
    if data.get("finding_id") == "W-4" or "betacommand" in json.dumps(data).lower():
        return False, "do not reuse BetacommandBot as an H5 tree"
    return True, f"{fid} {data['tree_id']} stop_kind={data['stop_kind']}"


def main() -> int:
    n = len(EXPECTED)
    print(f"[1/{n + 1}] protocol={PROTOCOL} trees={n}")
    ok_all = True
    for i, (fid, name) in enumerate(EXPECTED, start=2):
        ok, msg = check_one(fid, name)
        print(f"[{i}/{n + 1}] {'PASS' if ok else 'FAIL'} {msg}")
        ok_all = ok_all and ok
    if not ok_all:
        print("OUTCOME refuse or schema fail")
        return 1
    print(f"[{n + 1}/{n + 1}] PASS three H5 trees; analogue not AI Safe / MB11")
    print("OUTCOME layer_fail Expectation 4 institutional analogue; Construct concrete-MS still gated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
