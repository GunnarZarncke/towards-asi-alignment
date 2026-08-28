#!/usr/bin/env python3
"""SCDB justice-centered same-unit geometry vs issueArea; write h4-scotus fixture.

Protocol: drafts/plans/witness-c004-scotus.md (h4-scotus-v1.0.0).
"""

from __future__ import annotations

import csv
import json
import math
import urllib.error
import urllib.request
import zipfile
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "data" / "scotus"
ZIP_PATH = CACHE / "scdb.zip"
CSV_PATH = CACHE / "SCDB_2025_01_justiceCentered_Citation.csv"
OUT = ROOT / "fixtures" / "h4-scotus-v1.json"
PROTOCOL = "h4-scotus-v1.0.0"
SCDB_ZIP = "https://scdb.la.psu.edu/?jet_download=d9fd858d0211fe70abbe33bf7cd7ec832f3a2313"
UA = {"User-Agent": "towards-asi-alignment-witness/1.0"}
MIN_ROWS = 40
MIN_TEST = 8
MIN_INCLUDED = 9
LAMBDA = 1.0
MARGIN = 0.05
GEOM_EXTRA = [
    "lawType",
    "caseOrigin",
    "caseSource",
    "lcDisagreement",
    "jurisdiction",
    "decisionDirection",
]
ONED_COL = "issueArea"
UNIT_COL = "justiceName"
SORT_COLS = ["term", "caseId"]


def sigmoid(z: np.ndarray) -> np.ndarray:
    z = np.clip(z, -30.0, 30.0)
    return 1.0 / (1.0 + np.exp(-z))


def _update_alpha(y, p, w, unit_idx, n_units, alpha):
    resid = y - p
    sw = np.bincount(unit_idx, weights=w, minlength=n_units).astype(np.float64)
    sr = np.bincount(unit_idx, weights=resid, minlength=n_units).astype(np.float64)
    sw = np.clip(sw, 1e-6, None)
    dalpha = sr / sw
    alpha += dalpha
    return dalpha


def fit_fe_logit(X, y, unit_idx, n_units, lam, max_iter=80, alpha_inner=8):
    d = X.shape[1]
    beta = np.zeros(d, dtype=np.float64)
    alpha = np.zeros(n_units, dtype=np.float64)
    eye = np.eye(d, dtype=np.float64) if d else None
    last_delta = 0.0
    last_dalpha = 0.0
    it_done = 0
    for it in range(max_iter):
        it_done = it + 1
        for _ in range(alpha_inner):
            eta = alpha[unit_idx] + (X @ beta if d else 0.0)
            p = sigmoid(eta)
            w = np.clip(p * (1.0 - p), 1e-6, None)
            last_dalpha = float(np.max(np.abs(_update_alpha(y, p, w, unit_idx, n_units, alpha))))
        if d == 0:
            if last_dalpha < 1e-6:
                break
            continue
        eta = alpha[unit_idx] + X @ beta
        p = sigmoid(eta)
        w = np.clip(p * (1.0 - p), 1e-6, None)
        resid = y - p
        hess = X.T @ (X * w[:, None]) + lam * eye
        grad = X.T @ resid - lam * beta
        try:
            delta = np.linalg.solve(hess, grad)
        except np.linalg.LinAlgError:
            delta = np.linalg.lstsq(hess, grad, rcond=None)[0]
        beta += delta
        last_delta = float(np.max(np.abs(delta)))
        if it % 10 == 0 or it == max_iter - 1:
            print(f"    newton {it_done}/{max_iter} |dβ|={last_delta:.3e} |dα|={last_dalpha:.3e}")
        if last_delta < 1e-6 and last_dalpha < 1e-5:
            break
    return alpha, beta


def predict_acc_ll(X, y, unit_idx, alpha, beta, n_units):
    eta = alpha[unit_idx] + (X @ beta if X.shape[1] else 0.0)
    p = sigmoid(eta)
    pred = (p >= 0.5).astype(np.float64)
    nsum = np.clip(np.bincount(unit_idx, minlength=n_units).astype(np.float64), 1e-12, None)
    csum = np.bincount(unit_idx, weights=(pred == y).astype(np.float64), minlength=n_units)
    pp = np.clip(p, 1e-12, 1.0 - 1e-12)
    ll_i = -(y * np.log(pp) + (1.0 - y) * np.log(1.0 - pp))
    llsum = np.bincount(unit_idx, weights=ll_i, minlength=n_units)
    return csum / nsum, llsum / nsum


def classify(acc_g: float, acc_1d: float, acc_i: float) -> str:
    beat_1d = acc_g >= acc_1d + MARGIN
    beat_i = acc_g >= acc_i + MARGIN
    if beat_1d and beat_i:
        return "layer_fail_and_detection_pass"
    if beat_1d or beat_i:
        return "ambig"
    return "null"


def _sort_key(row: tuple) -> tuple:
    term, case_id = row[0], row[1]
    try:
        t = int(float(term))
    except (TypeError, ValueError):
        t = term
    try:
        c = int(float(case_id))
    except (TypeError, ValueError):
        c = case_id
    return (t, c)


def _f(v: str) -> float:
    return float(v)


def _ensure_csv() -> str:
    CACHE.mkdir(parents=True, exist_ok=True)
    if CSV_PATH.is_file() and CSV_PATH.stat().st_size > 1_000_000:
        print("  cache hit", CSV_PATH.name)
        return "cache"
    print("[download] SCDB 2025 Release 01 justice-centered citation zip")
    req = urllib.request.Request(SCDB_ZIP, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as resp:
        ZIP_PATH.write_bytes(resp.read())
    print("  wrote", ZIP_PATH, "bytes", ZIP_PATH.stat().st_size)
    with zipfile.ZipFile(ZIP_PATH) as zf:
        names = zf.namelist()
        target = None
        for name in names:
            if name.endswith("SCDB_2025_01_justiceCentered_Citation.csv"):
                target = name
                break
        if target is None:
            raise FileNotFoundError(
                "SCDB_2025_01_justiceCentered_Citation.csv not in zip: " + str(names)
            )
        print("  extract", target)
        with zf.open(target) as src, CSV_PATH.open("wb") as dst:
            dst.write(src.read())
    print("  wrote", CSV_PATH, "bytes", CSV_PATH.stat().st_size)
    return SCDB_ZIP


def _refuse(reason: str, **extra) -> int:
    OUT.write_text(
        json.dumps(
            {
                "protocol_version": PROTOCOL,
                "frozen": "2026-08-29",
                "host": "H4",
                "status": "refuse",
                "reason": reason,
                "n_units_included": 0,
                **extra,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print("OUTCOME refuse", reason)
    return 0


def main() -> int:
    print("[1/6] source")
    try:
        source_url = _ensure_csv()
    except (urllib.error.URLError, FileNotFoundError, TimeoutError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        return _refuse(f"SCDB CSV missing: {exc}")

    print("[2/6] parse", CSV_PATH.name)
    by_justice: dict[str, list[tuple]] = defaultdict(list)
    dropped_geom: list[str] = []
    with CSV_PATH.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise SystemExit("empty csv")
        fields = list(reader.fieldnames)
        print("  columns", len(fields))
        need = [UNIT_COL, "direction", ONED_COL, *SORT_COLS, *GEOM_EXTRA]
        missing = [c for c in need if c not in fields]
        if missing:
            return _refuse(f"missing columns {missing}")
        dropped_geom = [c for c in GEOM_EXTRA if c not in fields]
        geom_cols = [c for c in GEOM_EXTRA if c in fields]
        feature_cols = [ONED_COL, *geom_cols]
        n_rows = 0
        n_skip = 0
        for row in reader:
            n_rows += 1
            if n_rows % 20_000 == 0:
                print(f"  [{n_rows:,} rows]")
            d = row.get("direction", "").strip()
            if d not in ("1", "2"):
                n_skip += 1
                continue
            y = 1.0 if d == "1" else 0.0
            try:
                vals = [_f(row[c]) for c in feature_cols]
            except (TypeError, ValueError):
                n_skip += 1
                continue
            if not all(math.isfinite(v) for v in vals):
                n_skip += 1
                continue
            jname = str(row[UNIT_COL]).strip()
            if not jname:
                n_skip += 1
                continue
            term = row.get("term", "")
            case_id = row.get("caseId", "")
            by_justice[jname].append((term, case_id, y, vals))
    print(f"  rows={n_rows} skip={n_skip} justices={len(by_justice)}")

    print("[3/6] split")
    train_rows: list[tuple] = []
    test_rows: list[tuple] = []
    included: list[str] = []
    for jname, recs in by_justice.items():
        if len(recs) < MIN_ROWS:
            continue
        recs_sorted = sorted(recs, key=_sort_key)
        n = len(recs_sorted)
        n_train = n * 7 // 10
        train, test = recs_sorted[:n_train], recs_sorted[n_train:]
        if len(test) < MIN_TEST:
            continue
        uid = len(included)
        included.append(jname)
        for *_, y, vals in train:
            train_rows.append((uid, y, vals))
        for *_, y, vals in test:
            test_rows.append((uid, y, vals))
    n_units = len(included)
    print(f"  included={n_units} train_obs={len(train_rows)} test_obs={len(test_rows)}")
    if n_units < MIN_INCLUDED:
        return _refuse(
            f"included justices {n_units} < {MIN_INCLUDED}",
            n_units_included=n_units,
        )

    def pack(rows, geom: bool):
        y = np.array([r[1] for r in rows], dtype=np.float64)
        u = np.array([r[0] for r in rows], dtype=np.int64)
        if geom:
            x = np.array([r[2] for r in rows], dtype=np.float64)
        else:
            x = np.array([[r[2][0]] for r in rows], dtype=np.float64)
        return x, y, u

    print("[4/6] fit intercept / 1-D / geometry")
    _, y_tr, u_tr = pack(train_rows, False)
    X0 = np.zeros((len(y_tr), 0), dtype=np.float64)
    a0, b0 = fit_fe_logit(X0, y_tr, u_tr, n_units, LAMBDA)
    X1, _, _ = pack(train_rows, False)
    a1, b1 = fit_fe_logit(X1, y_tr, u_tr, n_units, LAMBDA)
    Xg, _, _ = pack(train_rows, True)
    ag, bg = fit_fe_logit(Xg, y_tr, u_tr, n_units, LAMBDA)

    print("[5/6] held-out")
    X0t, y_te, u_te = pack(test_rows, False)
    X0t = np.zeros((len(y_te), 0), dtype=np.float64)
    acc0, ll0 = predict_acc_ll(X0t, y_te, u_te, a0, b0, n_units)
    X1t, _, _ = pack(test_rows, False)
    acc1, ll1 = predict_acc_ll(X1t, y_te, u_te, a1, b1, n_units)
    Xgt, _, _ = pack(test_rows, True)
    accg, llg = predict_acc_ll(Xgt, y_te, u_te, ag, bg, n_units)
    m_acc = {
        "intercept": round(float(acc0.mean()), 6),
        "oned_issue_area": round(float(acc1.mean()), 6),
        "geometry": round(float(accg.mean()), 6),
    }
    m_ll = {
        "intercept": round(float(ll0.mean()), 6),
        "oned_issue_area": round(float(ll1.mean()), 6),
        "geometry": round(float(llg.mean()), 6),
    }
    status = classify(m_acc["geometry"], m_acc["oned_issue_area"], m_acc["intercept"])
    print("[6/6]", status, m_acc)

    feature_names = [c for c in feature_cols if c not in dropped_geom or c == ONED_COL]
    fixture = {
        "protocol_version": PROTOCOL,
        "frozen": "2026-08-29",
        "host": "H4",
        "source": "SCDB 2025 Release 01 justiceCentered_Citation",
        "source_fetch": source_url,
        "unit_key": UNIT_COL,
        "n_csv_rows": n_rows,
        "n_skip": n_skip,
        "n_units_included": n_units,
        "included_justices": included,
        "n_train_obs": len(train_rows),
        "n_test_obs": len(test_rows),
        "dropped_geom_columns": dropped_geom,
        "feature_names": feature_names,
        "heldout_accuracy": m_acc,
        "heldout_logloss": m_ll,
        "margin_geometry_minus_oned": round(m_acc["geometry"] - m_acc["oned_issue_area"], 6),
        "margin_geometry_minus_intercept": round(m_acc["geometry"] - m_acc["intercept"], 6),
        "beta_oned": [round(float(x), 6) for x in b1],
        "beta_geometry": [round(float(x), 6) for x in bg],
        "status": status,
        "lambda": LAMBDA,
        "margin": MARGIN,
    }
    OUT.write_text(json.dumps(fixture, indent=2) + "\n", encoding="utf-8")
    print("wrote", OUT)
    print("OUTCOME", status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
