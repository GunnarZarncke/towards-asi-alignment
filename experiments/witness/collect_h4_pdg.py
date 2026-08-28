#!/usr/bin/env python3
"""Collect frozen H4 PDG protocol h4-pdg-v1.0.0. Refuse if no eligible public table."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "fixtures" / "h4-pdg-v1.json"
PROTOCOL = "h4-pdg-v1.0.0"
UA = {"User-Agent": "towards-asi-alignment-witness/1.0"}

OSF_NODES = ("h5x2a", "x69t7")
# Source 2 metadata only (do not download microdata in this collector).
DV_C81EJA = "doi:10.34894/c81eja"
DV_OTHER = (
    "doi:10.25397/eur.14916531",
    "doi:10.25397/eur.c.5809043",
    "doi:10.25397/eur.12783161",
)


def _get(url: str) -> tuple[bytes, str]:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45) as resp:
        return resp.read(), resp.headers.get("Content-Type", "")


def _osf_files(node: str) -> tuple[list[str], str]:
    url = f"https://api.osf.io/v2/nodes/{node}/files/osfstorage/?page%5Bsize%5D=100"
    try:
        raw, _ = _get(url)
        payload = json.loads(raw)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return [], f"osf {node}: {exc}"
    names = [(item.get("attributes") or {}).get("name") or "" for item in payload.get("data") or []]
    return names, f"osf {node} files: {names}"


def _dv_record(doi: str) -> tuple[dict | None, str]:
    url = f"https://dataverse.nl/api/datasets/:persistentId/?persistentId={doi}"
    try:
        raw, ctype = _get(url)
    except (urllib.error.URLError, TimeoutError) as exc:
        return None, f"{doi}: fetch error {exc}"
    if raw.lstrip()[:1] != b"{":
        snippet = raw[:120].decode("utf-8", errors="replace")
        return None, f"{doi}: non-JSON ({ctype!r}, {snippet!r})"
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        return None, f"{doi}: JSON parse error {exc}"
    return payload, f"{doi}: JSON ok"


def _file_names(payload: dict) -> list[str]:
    files = ((payload.get("data") or {}).get("latestVersion") or {}).get("files") or []
    names = []
    for item in files:
        df = item.get("dataFile") or {}
        names.append(str(df.get("filename") or ""))
    return names


def main() -> int:
    print("[1/3] OSF prereg nodes")
    osf_notes = []
    osf_tabular = False
    for node in OSF_NODES:
        names, note = _osf_files(node)
        osf_notes.append(note)
        print(" ", note)
        for name in names:
            if name.lower().endswith((".csv", ".tsv", ".sav", ".xlsx", ".xls", ".dta")):
                osf_tabular = True

    print("[2/3] DataverseNL source-1 DOIs")
    other_notes = []
    for doi in DV_OTHER:
        payload, note = _dv_record(doi)
        other_notes.append(note)
        print(" ", note)

    print("[3/3] DataverseNL source-2 metadata (no microdata download)")
    payload, note = _dv_record(DV_C81EJA)
    print(" ", note)
    c81_files = _file_names(payload) if payload else []
    if c81_files:
        print("  files:", c81_files)

    reason = (
        "Source 1 (Urban Rotterdam longitudinal PDG on OSF h5x2a/x69t7 and EUR "
        "10.25397/eur.14916531) has no public person×wave×target table (prereg PDFs "
        "and/or missing Dataverse records). Source 2 (van de Groep et al. 2020, "
        "doi:10.34894/c81eja) lists unrestricted SPSS files including "
        "Brainlinks_Covid19_Giving_time_target_GEE.sav, but that dump is the PLOS ONE "
        "daily-diary cohort ages 10–20. Protocol refuses scoring that microdata. "
        "Do not substitute Moral Machine or paper bar charts."
    )
    fixture = {
        "protocol_version": PROTOCOL,
        "frozen": "2026-08-28",
        "host": "H4",
        "status": "refuse",
        "reason": reason,
        "osf_notes": osf_notes,
        "osf_tabular_listed": osf_tabular,
        "dataverse_other_notes": other_notes,
        "dataverse_c81eja_note": note,
        "dataverse_c81eja_files": c81_files,
        "n_units_included": 0,
        "unit_key": None,
        "scored": False,
    }
    OUT.write_text(json.dumps(fixture, indent=2) + "\n", encoding="utf-8")
    print("OUTCOME refuse")
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
