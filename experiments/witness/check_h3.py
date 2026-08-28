#!/usr/bin/env python3
"""Check frozen H3 Wikipedia protocol fixture h3-v1.1.0 (richer sources)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "h3-wikipedia-v1.json"
PROTOCOL = "h3-v1.1.0"


def main() -> int:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    print("[1/5] load", FIXTURE.name)
    if data.get("protocol_version") != PROTOCOL:
        print("FAIL protocol")
        return 1
    snap = data["snap_rfa"]
    joined = snap.get("has_later_edit_traces") is True and snap.get("file_downloaded") is True
    print(f"[2/5] {'PASS' if joined else 'FAIL'} SNAP downloaded and later traces joined")
    rfa = data["c005_causal_rfa_to_edits"]
    rfa_ok = rfa.get("status") == "refuse" and rfa.get("passed_2012_with_oppose", 0) >= 21
    print(f"[3/5] {'PASS' if rfa_ok else 'FAIL'} causal RfA refuse (join, no control)")
    om = data["orangemoody"]
    capture = (
        om.get("helper_socks_mark_reviewed_other_socks_articles") is True
        and om.get("same_operator_both_ends_of_review_channel") is True
        and om.get("cu_linked_socks", 0) >= 381
    )
    print(f"[4/5] {'PASS' if capture else 'FAIL'} Orangemoody same-operator review channel")
    bot = data["c006_bot_brfa_to_block"]
    bot_ok = bot.get("status") == "layer_fail" and (bot.get("episode") or {}).get("user") == "BetacommandBot"
    spi = data["spi_as_M"]
    spi_ok = spi.get("status") == "refuse" and spi.get("wiki_socks_investigations", 0) >= 20000
    print(f"[5/5] {'PASS' if bot_ok and spi_ok else 'FAIL'} C-006 BetacommandBot fail; SPI M refuse")
    if not (joined and rfa_ok and capture and bot_ok and spi_ok):
        return 1
    print("OUTCOME C-005 causal refuse; anti-capture fail; C-006 fail; Exp3 SPI refuse")
    return 0


if __name__ == "__main__":
    sys.exit(main())
