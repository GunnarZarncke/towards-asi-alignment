"""Hash-chained trace integrity with attestation-anchored head digest.

Each JSONL row carries ``sig = H(prev_sig | row_without_sig)``; the final chain
digest and row count are anchored in ``/etc/attest/manifest.json``, which the
red team has no write capability for. Any in-place edit, deletion, or append to
an anchored log is detectable by re-walking the chain against the anchor — no
secret key needed, so the embedded auditor can verify with public data.

This provides tamper-EVIDENCE after write time only. It does not make the
writer honest: a system that lies into its own log signs the lies (that regime
is modeled behaviorally by the capture/theater scenarios, and countered by
interventional probes, not integrity tech).

Configurable (``EMBEDDED_TRACE_INTEGRITY`` = ``hash_chain`` | ``none``) so the
unsigned regime of NEGATIVE_RESULTS ES-4 stays reproducible.
"""

from __future__ import annotations

import hashlib
import json
import os
from typing import Any

GENESIS = "genesis"

TraceIntegrityMode = str  # "hash_chain" | "none"

_mode: list[TraceIntegrityMode] = [
    os.environ.get("EMBEDDED_TRACE_INTEGRITY", "hash_chain").strip().lower()
]
if _mode[0] not in ("hash_chain", "none"):
    _mode[0] = "hash_chain"


def get_trace_integrity_mode() -> TraceIntegrityMode:
    return _mode[0]


def set_trace_integrity_mode(mode: TraceIntegrityMode) -> None:
    if mode not in ("hash_chain", "none"):
        raise ValueError(f"unknown trace integrity mode: {mode!r}")
    _mode[0] = mode


def _row_digest(prev_sig: str, row: dict[str, Any]) -> str:
    body = json.dumps(
        {k: v for k, v in row.items() if k != "sig"},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(f"{prev_sig}|{body}".encode()).hexdigest()[:16]


def chain_rows(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], str]:
    """Attach ``sig`` to each row; return (signed rows, head digest)."""
    sig = GENESIS
    out: list[dict[str, Any]] = []
    for row in rows:
        sig = _row_digest(sig, row)
        out.append({**row, "sig": sig})
    return out, sig


def anchor_for(path: str, head: str, n_rows: int) -> dict[str, Any]:
    return {"path": path, "head": head, "n_rows": n_rows}


def append_anchored_row(vfs, anchor_name: str, path: str, row: dict[str, Any]) -> None:
    """Trusted-infrastructure append: chain the row and extend the manifest anchor.

    Used by deployment machinery (e.g. the deploy gate) that legitimately
    appends to an anchored log after episode write time. Red-team code cannot
    do this because the manifest is not writable with red-team capabilities.
    """
    manifest_raw = vfs.read("/etc/attest/manifest.json")
    manifest = json.loads(manifest_raw) if manifest_raw else {}
    anchors = manifest.get("trace_anchors") or {}
    anchor = anchors.get(anchor_name)
    if not anchor:
        vfs.append_line(path, json.dumps(row))
        return
    sig = _row_digest(str(anchor["head"]), row)
    vfs.append_line(path, json.dumps({**row, "sig": sig}))
    anchor["head"] = sig
    anchor["n_rows"] = int(anchor["n_rows"]) + 1
    manifest["trace_anchors"] = anchors
    vfs.write("/etc/attest/manifest.json", json.dumps(manifest, indent=2))


def verify_chain(raw: str, anchor: dict[str, Any]) -> tuple[bool, str]:
    """Re-walk the chain in ``raw`` JSONL against an attestation anchor."""
    lines = [ln for ln in raw.splitlines() if ln.strip()]
    expected_n = int(anchor.get("n_rows", -1))
    if len(lines) != expected_n:
        return False, f"row_count_mismatch: {len(lines)} != {expected_n}"
    sig = GENESIS
    for i, line in enumerate(lines):
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            return False, f"row_{i}_unparseable"
        sig = _row_digest(sig, row)
        if row.get("sig") != sig:
            return False, f"row_{i}_sig_mismatch"
    if sig != anchor.get("head"):
        return False, "head_mismatch"
    return True, "ok"
