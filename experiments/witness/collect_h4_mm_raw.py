#!/usr/bin/env python3
"""Moral Machine raw same-unit bundle effect; write h4-mm-raw fixture.

Protocol: drafts/plans/witness-c004-raw.md (h4-mm-raw-v1.0.0).
Streams SharedResponses.csv.tar.gz; does not extract the CSV to disk.
"""

from __future__ import annotations

import csv
import io
import json
import random
import subprocess
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
TAR_PATH = ROOT / "data" / "moral-machine" / "SharedResponses.csv.tar.gz"
PASS1_CACHE = ROOT / "data" / "moral-machine" / "h4-mm-raw-pass1-v1.json"
PASS2_CACHE = ROOT / "data" / "moral-machine" / "h4-mm-raw-pass2-v1.npz"
OUT = ROOT / "fixtures" / "h4-mm-raw-v1.json"
PROTOCOL = "h4-mm-raw-v1.0.0"
SEED = 7
CAP_UNITS = 20_000
MIN_PAIRS = 8
MIN_INCLUDED = 500
LAMBDA = 1.0
MARGIN = 0.05

STRUCT = ["PedPed", "Barrier", "CrossingSignal", "NumberOfCharacters"]
TYPES = [
    "Man",
    "Woman",
    "Pregnant",
    "Stroller",
    "OldMan",
    "OldWoman",
    "Boy",
    "Girl",
    "Homeless",
    "LargeWoman",
    "LargeMan",
    "Criminal",
    "MaleExecutive",
    "FemaleExecutive",
    "FemaleAthlete",
    "MaleAthlete",
    "FemaleDoctor",
    "MaleDoctor",
    "Dog",
    "Cat",
]
FEAT = STRUCT + TYPES
HUMAN_TYPES = [t for t in TYPES if t not in ("Dog", "Cat")]


def _nullish(v: str | None) -> bool:
    if v is None:
        return True
    s = str(v).strip()
    return s == "" or s.lower() in {"nan", "na", "none", "null"}


def _f(v: str) -> float:
    return float(v)


def _open_csv(tar_path: Path):
    # Known member from OSF dump; listing the tar would decompress ~11 GB first.
    member = "SharedResponses.csv"
    print(f"  tar -xO {member}")
    proc = subprocess.Popen(
        ["tar", "-xOzf", str(tar_path), member],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    assert proc.stdout is not None
    text = io.TextIOWrapper(proc.stdout, encoding="utf-8", newline="")
    return proc, text


def _iter_complete_pairs(tar_path: Path, need_features: bool, eligible_units: set[str] | None = None, unit_key: str | None = None):
    proc, text = _open_csv(tar_path)
    try:
        reader = csv.reader(text)
        header = next(reader)
        idx = {name: i for i, name in enumerate(header)}
        required_ids = ["ResponseID", "ExtendedSessionID", "UserID", "Intervention", "Saved"]
        missing = [c for c in required_ids + FEAT if c not in idx]
        print(f"  header cols={len(header)} missing={missing or 'none'}")
        pending: dict[str, list] = {}
        n_rows = 0
        n_pairs = 0
        n_incomplete_end = 0
        n_odd = 0
        for row in reader:
            n_rows += 1
            if n_rows % 500_000 == 0:
                print(f"  [{n_rows:,} rows] pairs={n_pairs:,} pending={len(pending):,}")
            if len(row) < len(header):
                continue
            rid = row[idx["ResponseID"]]
            if _nullish(rid):
                continue
            if eligible_units is not None:
                raw_u = row[idx["UserID"]] if unit_key == "UserID" else row[idx["ExtendedSessionID"]]
                if _nullish(raw_u):
                    if rid not in pending:
                        continue
                elif str(raw_u) not in eligible_units and rid not in pending:
                    continue
            rec = row if need_features else (
                row[idx["UserID"]],
                row[idx["ExtendedSessionID"]],
                row[idx["Intervention"]],
                row[idx["Saved"]],
            )
            slot = pending.get(rid)
            if slot is None:
                pending[rid] = [rec]
            elif len(slot) == 1:
                slot.append(rec)
                a, b = slot
                del pending[rid]
                n_pairs += 1
                yield idx, header, a, b, missing
            else:
                n_odd += 1
        n_incomplete_end = len(pending)
        print(
            f"  done rows={n_rows:,} complete_pairs={n_pairs:,} "
            f"unpaired={n_incomplete_end:,} extra_rows={n_odd:,}"
        )
        text.close()
        code = proc.wait()
        if code != 0:
            raise RuntimeError(f"tar -xO failed ({code})")
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()


def _pair_ids(idx: dict[str, int], a, b, features: bool):
    if features:
        def get(row, col):
            return row[idx[col]]

        ua, ub = get(a, "UserID"), get(b, "UserID")
        sa, sb = get(a, "ExtendedSessionID"), get(b, "ExtendedSessionID")
        ia, ib = get(a, "Intervention"), get(b, "Intervention")
        ya, yb = get(a, "Saved"), get(b, "Saved")
        rid = get(a, "ResponseID")
    else:
        ua, sa, ia, ya = a
        ub, sb, ib, yb = b
        rid = ""
    return rid, ua, ub, sa, sb, ia, ib, ya, yb


def _delta_xy(idx: dict[str, int], a: list[str], b: list[str], feat_names: list[str]):
    def vec(row):
        return np.array([_f(row[idx[c]]) for c in feat_names], dtype=np.float64)

    ia = int(float(a[idx["Intervention"]]))
    ib = int(float(b[idx["Intervention"]]))
    if {ia, ib} != {0, 1}:
        return None
    row1, row0 = (a, b) if ia == 1 else (b, a)
    y_s = row1[idx["Saved"]]
    y0 = row0[idx["Saved"]]
    if _nullish(y_s) or _nullish(y0):
        return None
    y = _f(y_s)
    if y not in (0.0, 1.0):
        return None
    dx = vec(row1) - vec(row0)
    rid = a[idx["ResponseID"]]
    return rid, dx, y


def sigmoid(z: np.ndarray) -> np.ndarray:
    z = np.clip(z, -35.0, 35.0)
    return 1.0 / (1.0 + np.exp(-z))


def _update_alpha(y, p, w, unit_idx, n_units, alpha):
    resid = y - p
    sw = np.bincount(unit_idx, weights=w, minlength=n_units).astype(np.float64)
    sr = np.bincount(unit_idx, weights=resid, minlength=n_units).astype(np.float64)
    sw = np.clip(sw, 1e-6, None)
    dalpha = sr / sw
    alpha += dalpha
    return dalpha


def fit_fe_logit(
    X: np.ndarray,
    y: np.ndarray,
    unit_idx: np.ndarray,
    n_units: int,
    lam: float,
    max_iter: int = 80,
    alpha_inner: int = 8,
) -> tuple[np.ndarray, np.ndarray, dict]:
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
            if it % 10 == 0 or it == max_iter - 1:
                print(f"    newton {it_done}/{max_iter} |dα|={last_dalpha:.3e}")
            if last_dalpha < 1e-6:
                break
            continue
        eta = alpha[unit_idx] + X @ beta
        p = sigmoid(eta)
        w = np.clip(p * (1.0 - p), 1e-6, None)
        resid = y - p
        xw = X * w[:, None]
        hess = X.T @ xw + lam * eye
        grad_ascent = X.T @ resid - lam * beta
        try:
            delta = np.linalg.solve(hess, grad_ascent)
        except np.linalg.LinAlgError:
            delta = np.linalg.lstsq(hess, grad_ascent, rcond=None)[0]
        beta += delta
        last_delta = float(np.max(np.abs(delta)))
        if it % 5 == 0 or it == max_iter - 1:
            print(
                f"    newton {it_done}/{max_iter} |dβ|={last_delta:.3e} |dα|={last_dalpha:.3e}"
            )
        if last_delta < 1e-6 and last_dalpha < 1e-5:
            break
    diag = {
        "iterations": it_done,
        "max_abs_d_beta": last_delta,
        "max_abs_d_alpha": last_dalpha,
        "alpha_converged": last_dalpha <= 1e-4,
        "beta_converged": d == 0 or last_delta <= 1e-6,
    }
    return alpha, beta, diag


def predict_unit_stats(
    X: np.ndarray,
    y: np.ndarray,
    unit_idx: np.ndarray,
    alpha: np.ndarray,
    beta: np.ndarray,
    n_units: int,
) -> tuple[np.ndarray, np.ndarray]:
    eta = alpha[unit_idx] + (X @ beta if X.shape[1] else 0.0)
    p = sigmoid(eta)
    pred = (p >= 0.5).astype(np.float64)
    nsum = np.bincount(unit_idx, minlength=n_units).astype(np.float64)
    csum = np.bincount(unit_idx, weights=(pred == y).astype(np.float64), minlength=n_units)
    pp = np.clip(p, 1e-12, 1.0 - 1e-12)
    ll_i = -(y * np.log(pp) + (1.0 - y) * np.log(1.0 - pp))
    llsum = np.bincount(unit_idx, weights=ll_i, minlength=n_units)
    nsum = np.clip(nsum, 1e-12, None)
    return csum / nsum, llsum / nsum


def bootstrap_margins(
    acc_i: np.ndarray,
    acc_1: np.ndarray,
    acc_g: np.ndarray,
    seed: int,
    n_boot: int = 1000,
) -> dict:
    rng = np.random.default_rng(seed)
    n = len(acc_g)
    m1 = np.empty(n_boot)
    mi = np.empty(n_boot)
    for b in range(n_boot):
        ix = rng.integers(0, n, n)
        m1[b] = float(acc_g[ix].mean() - acc_1[ix].mean())
        mi[b] = float(acc_g[ix].mean() - acc_i[ix].mean())
    return {
        "n_boot": n_boot,
        "seed": seed,
        "margin_vs_oned_p025": round(float(np.percentile(m1, 2.5)), 6),
        "margin_vs_oned_p975": round(float(np.percentile(m1, 97.5)), 6),
        "margin_vs_intercept_p025": round(float(np.percentile(mi, 2.5)), 6),
        "margin_vs_intercept_p975": round(float(np.percentile(mi, 97.5)), 6),
        "both_margins_hold_in_all_replicates": bool(
            np.all(m1 >= MARGIN) and np.all(mi >= MARGIN)
        ),
    }


def classify(acc_g: float, acc_1d: float, acc_i: float) -> str:
    beat_1d = acc_g >= acc_1d + MARGIN
    beat_i = acc_g >= acc_i + MARGIN
    if beat_1d and beat_i:
        return "layer_fail_and_detection_pass"
    if beat_1d or beat_i:
        return "ambig"
    return "null"


def main() -> int:
    print("[1/6] source", TAR_PATH)
    if not TAR_PATH.exists():
        payload = {
            "protocol_version": PROTOCOL,
            "status": "refuse",
            "reason": "missing SharedResponses.csv.tar.gz (do not substitute CountriesChangePr.csv)",
        }
        OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print("OUTCOME refuse missing dump")
        return 0

    print("[2/6] pass 1: pair counts and UserID coverage")
    types_missing: list[str] = []
    feat_names = list(FEAT)
    cache = None
    if PASS1_CACHE.exists():
        cache = json.loads(PASS1_CACHE.read_text(encoding="utf-8"))
        if cache.get("protocol_version") != PROTOCOL or cache.get("downsample_seed") != SEED:
            cache = None
    if cache:
        print("  reuse", PASS1_CACHE.name)
        unit_key = cache["unit_key"]
        frac_uid = cache["userid_pair_fraction"]
        n_pairs = cache["n_complete_pairs"]
        n_ge8 = cache["n_units_ge8"]
        n_before_cap = n_ge8
        eligible = cache["eligible_units"]
        types_missing = cache.get("dropped_type_columns") or []
        feat_names = cache.get("feature_names") or [c for c in FEAT if c not in types_missing]
        eligible_set = set(eligible)
        print(f"  complete_pairs_with_Saved={n_pairs:,} UserID_frac={frac_uid:.4f} unit_key={unit_key}")
        print(f"  units with ≥{MIN_PAIRS} pairs: {n_ge8:,}; selected {len(eligible_set):,}")
    else:
        n_pairs = 0
        n_userid = 0
        missing_cols: list[str] = []
        counts_user: dict[str, int] = defaultdict(int)
        counts_sess: dict[str, int] = defaultdict(int)
        for idx, header, a, b, missing in _iter_complete_pairs(TAR_PATH, need_features=False):
            missing_cols = missing
            rid, ua, ub, sa, sb, ia, ib, ya, yb = _pair_ids(idx, a, b, features=False)
            if _nullish(ya) or _nullish(yb):
                continue
            n_pairs += 1
            uid = ua if not _nullish(ua) else ub
            sid = sa if not _nullish(sa) else sb
            if not _nullish(uid):
                n_userid += 1
                counts_user[str(uid)] += 1
            if not _nullish(sid):
                counts_sess[str(sid)] += 1

        if missing_cols:
            types_missing = [c for c in missing_cols if c in TYPES]
            ids_missing = [c for c in missing_cols if c not in TYPES]
            if ids_missing:
                payload = {
                    "protocol_version": PROTOCOL,
                    "status": "refuse",
                    "reason": f"missing columns {ids_missing}",
                    "missing_columns": missing_cols,
                }
                OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
                print("OUTCOME refuse missing columns")
                return 0
            feat_names = [c for c in FEAT if c not in types_missing]
            print("  refuse-column (drop from all models):", types_missing)
        else:
            types_missing = []
            feat_names = list(FEAT)

        if n_pairs == 0:
            payload = {
                "protocol_version": PROTOCOL,
                "status": "refuse",
                "reason": "cannot pair ResponseID",
            }
            OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            print("OUTCOME refuse no pairs")
            return 0

        frac_uid = n_userid / n_pairs
        if frac_uid >= 0.5:
            unit_key = "UserID"
            counts = counts_user
        else:
            unit_key = "ExtendedSessionID"
            counts = counts_sess
        print(f"  complete_pairs_with_Saved={n_pairs:,} UserID_frac={frac_uid:.4f} unit_key={unit_key}")

        eligible = [u for u, c in counts.items() if c >= MIN_PAIRS]
        n_ge8 = len(eligible)
        print(f"  units with ≥{MIN_PAIRS} pairs: {n_ge8:,}")
        if n_ge8 < MIN_INCLUDED:
            payload = {
                "protocol_version": PROTOCOL,
                "status": "refuse",
                "reason": f"included units {len(eligible)} < {MIN_INCLUDED} after ≥{MIN_PAIRS} filter",
                "unit_key": unit_key,
                "n_units_ge8": n_ge8,
                "n_complete_pairs": n_pairs,
            }
            OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            print("OUTCOME refuse too few units")
            return 0

        rng = random.Random(SEED)
        n_before_cap = n_ge8
        if len(eligible) > CAP_UNITS:
            rng.shuffle(eligible)
            eligible = eligible[:CAP_UNITS]
            print(f"  downsample seed={SEED} {n_before_cap:,} → {len(eligible):,}")
        eligible_set = set(eligible)
        del counts_user, counts_sess, counts
        PASS1_CACHE.write_text(
            json.dumps(
                {
                    "protocol_version": PROTOCOL,
                    "downsample_seed": SEED,
                    "unit_key": unit_key,
                    "userid_pair_fraction": frac_uid,
                    "n_complete_pairs": n_pairs,
                    "n_units_ge8": n_ge8,
                    "dropped_type_columns": types_missing,
                    "feature_names": feat_names,
                    "eligible_units": eligible,
                }
            )
            + "\n",
            encoding="utf-8",
        )
        print("  wrote", PASS1_CACHE.name)

    print("[3/6] pass 2: features for selected units")
    loaded_pass2 = False
    if PASS2_CACHE.exists() and cache:
        z = np.load(PASS2_CACHE, allow_pickle=False)
        if (
            int(z["n_units"]) == len(eligible_set)
            and list(z["feature_names"]) == feat_names
        ):
            Xtr = z["Xtr"]
            Xte = z["Xte"]
            ytr = z["ytr"]
            yte = z["yte"]
            utr = z["utr"]
            ute = z["ute"]
            n_units = int(z["n_units"])
            loaded_pass2 = True
            print(f"  reuse {PASS2_CACHE.name} train={len(ytr):,} test={len(yte):,}")
    if not loaded_pass2:
        by_unit: dict[str, list[tuple[str, np.ndarray, float]]] = defaultdict(list)
        for idx, header, a, b, _ in _iter_complete_pairs(
            TAR_PATH, need_features=True, eligible_units=eligible_set, unit_key=unit_key
        ):
            ua = a[idx["UserID"]] if not _nullish(a[idx["UserID"]]) else b[idx["UserID"]]
            sa = (
                a[idx["ExtendedSessionID"]]
                if not _nullish(a[idx["ExtendedSessionID"]])
                else b[idx["ExtendedSessionID"]]
            )
            uid = str(ua) if unit_key == "UserID" else str(sa)
            if uid not in eligible_set:
                continue
            parsed = _delta_xy(idx, a, b, feat_names)
            if parsed is None:
                continue
            rid, dx, y = parsed
            by_unit[uid].append((rid, dx, y))

        kept: dict[str, list[tuple[str, np.ndarray, float]]] = {}
        dropped_split = 0
        for uid, pairs in by_unit.items():
            pairs.sort(key=lambda t: t[0])
            n = len(pairs)
            if n < MIN_PAIRS:
                continue
            n_train = n * 7 // 10
            n_test = n - n_train
            if n_test < 2:
                dropped_split += 1
                continue
            kept[uid] = pairs
        print(f"  split-eligible units={len(kept):,} dropped_test<2={dropped_split}")
        del by_unit

        if len(kept) < MIN_INCLUDED:
            payload = {
                "protocol_version": PROTOCOL,
                "status": "refuse",
                "reason": f"split-eligible units {len(kept)} < {MIN_INCLUDED}",
                "unit_key": unit_key,
            }
            OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            print("OUTCOME refuse after split filter")
            return 0

        units = sorted(kept)
        print("[4/6] design matrices")
        rows_tr = []
        y_tr = []
        u_tr = []
        rows_te = []
        y_te = []
        u_te = []
        u_map = {u: i for i, u in enumerate(units)}
        for uid in units:
            pairs = kept[uid]
            n = len(pairs)
            n_train = n * 7 // 10
            ui = u_map[uid]
            for j, (_rid, dx, y) in enumerate(pairs):
                if j < n_train:
                    rows_tr.append(dx)
                    y_tr.append(y)
                    u_tr.append(ui)
                else:
                    rows_te.append(dx)
                    y_te.append(y)
                    u_te.append(ui)
        Xtr = np.vstack(rows_tr)
        Xte = np.vstack(rows_te)
        ytr = np.array(y_tr, dtype=np.float64)
        yte = np.array(y_te, dtype=np.float64)
        utr = np.array(u_tr, dtype=np.int32)
        ute = np.array(u_te, dtype=np.int32)
        n_units = len(units)
        np.savez_compressed(
            PASS2_CACHE,
            Xtr=Xtr,
            Xte=Xte,
            ytr=ytr,
            yte=yte,
            utr=utr,
            ute=ute,
            n_units=np.array(n_units),
            feature_names=np.array(feat_names, dtype="U40"),
        )
        print(f"  wrote {PASS2_CACHE.name}")
    else:
        print("[4/6] design matrices (from cache)")

    nfeat = Xtr.shape[1]
    print(f"  train_obs={len(ytr):,} test_obs={len(yte):,} units={n_units:,} d={nfeat}")
    i_num = feat_names.index("NumberOfCharacters")
    type_idx = [feat_names.index(t) for t in TYPES if t in feat_names]
    number_minus_types = Xtr[:, i_num] - Xtr[:, type_idx].sum(axis=1)
    collinear = {
        "number_equals_sum_of_type_deltas": bool(float(np.max(np.abs(number_minus_types))) < 1e-9),
        "max_abs_number_minus_type_sum": round(float(np.max(np.abs(number_minus_types))), 8),
        "note": (
            "NumberOfCharacters is the sum of the 20 type counts; joint geometry "
            "coefficients on Number vs types are not separately identified. "
            "Use prediction, not individual beta_number in the geometry model."
        ),
    }
    print(
        "  collinearity max|ΔNumber-ΣΔtypes|=",
        collinear["max_abs_number_minus_type_sum"],
        "exact" if collinear["number_equals_sum_of_type_deltas"] else "not exact",
    )
    Xtr_1d = Xtr[:, [i_num]]
    Xte_1d = Xte[:, [i_num]]
    Xtr_i = np.zeros((len(ytr), 0))
    Xte_i = np.zeros((len(yte), 0))
    drop_num = [j for j in range(nfeat) if j != i_num]
    Xtr_g0 = Xtr[:, drop_num]
    Xte_g0 = Xte[:, drop_num]

    print("[5/6] fit intercept / 1-D / geometry (λ=1.0, FE α_i)")
    print("  intercept-only")
    a_i, b_i, d_i = fit_fe_logit(Xtr_i, ytr, utr, n_units, lam=LAMBDA)
    print("  1-D Number")
    a_1, b_1, d_1 = fit_fe_logit(Xtr_1d, ytr, utr, n_units, lam=LAMBDA)
    print("  geometry")
    a_g, b_g, d_g = fit_fe_logit(Xtr, ytr, utr, n_units, lam=LAMBDA)
    print("  geometry without Number (validation only)")
    a_g0, b_g0, d_g0 = fit_fe_logit(Xtr_g0, ytr, utr, n_units, lam=LAMBDA)

    u_acc_i, u_ll_i = predict_unit_stats(Xte_i, yte, ute, a_i, b_i, n_units)
    u_acc_1, u_ll_1 = predict_unit_stats(Xte_1d, yte, ute, a_1, b_1, n_units)
    u_acc_g, u_ll_g = predict_unit_stats(Xte, yte, ute, a_g, b_g, n_units)
    u_acc_g0, u_ll_g0 = predict_unit_stats(Xte_g0, yte, ute, a_g0, b_g0, n_units)
    acc_i, ll_i = float(np.mean(u_acc_i)), float(np.mean(u_ll_i))
    acc_1, ll_1 = float(np.mean(u_acc_1)), float(np.mean(u_ll_1))
    acc_g, ll_g = float(np.mean(u_acc_g)), float(np.mean(u_ll_g))
    acc_g0, ll_g0 = float(np.mean(u_acc_g0)), float(np.mean(u_ll_g0))
    print(
        f"  held-out mean accuracy  intercept={acc_i:.4f}  1-D={acc_1:.4f}  geom={acc_g:.4f}  geom_no_number={acc_g0:.4f}"
    )
    print(
        f"  held-out mean log-loss  intercept={ll_i:.4f}  1-D={ll_1:.4f}  geom={ll_g:.4f}"
    )
    boot = bootstrap_margins(u_acc_i, u_acc_1, u_acc_g, seed=SEED)
    conv_ok = (
        d_i["alpha_converged"]
        and d_1["alpha_converged"]
        and d_g["alpha_converged"]
        and d_1["beta_converged"]
        and d_g["beta_converged"]
    )
    print(
        "  bootstrap margins vs 1-D",
        boot["margin_vs_oned_p025"],
        boot["margin_vs_oned_p975"],
        "vs intercept",
        boot["margin_vs_intercept_p025"],
        boot["margin_vs_intercept_p975"],
    )
    if not conv_ok:
        print("  WARN intercepts or slopes not fully converged")

    beta = {name: float(b_g[k]) for k, name in enumerate(feat_names)}
    pets = float(beta.get("Dog", 0.0) + beta.get("Cat", 0.0))
    humans = float(sum(beta.get(t, 0.0) for t in HUMAN_TYPES if t in feat_names))
    species = pets - humans
    status = classify(acc_g, acc_1, acc_i)
    reason = (
        f"geom acc {acc_g:.4f} vs 1-D {acc_1:.4f} (Δ={acc_g - acc_1:.4f}) "
        f"vs intercept {acc_i:.4f} (Δ={acc_g - acc_i:.4f}); margins both ≥{MARGIN}"
        if status == "layer_fail_and_detection_pass"
        else f"geom={acc_g:.4f} 1-D={acc_1:.4f} intercept={acc_i:.4f}"
    )

    print("[6/6] write fixture")
    payload = {
        "protocol_version": PROTOCOL,
        "frozen": "2026-08-28",
        "host": "H4",
        "source": "OSF 3hvt2 SharedResponses.csv.tar.gz (Awad et al. Nature 2018)",
        "osf_storage_id": "5b54f679c86a8c0010444782",
        "unit_key": unit_key,
        "userid_pair_fraction": round(frac_uid, 6),
        "n_complete_pairs": n_pairs,
        "n_units_ge8": n_before_cap,
        "n_units_included": n_units,
        "cap_units": CAP_UNITS,
        "downsample_seed": SEED if n_before_cap > CAP_UNITS else None,
        "n_train_obs": int(len(ytr)),
        "n_test_obs": int(len(yte)),
        "delta_rule": "x(Intervention=1) - x(Intervention=0); y=Saved on Intervention=1",
        "dropped_type_columns": types_missing,
        "feature_names": feat_names,
        "lambda": LAMBDA,
        "margin": MARGIN,
        "heldout_accuracy": {
            "intercept": round(acc_i, 6),
            "oned_number": round(acc_1, 6),
            "geometry": round(acc_g, 6),
        },
        "heldout_logloss": {
            "intercept": round(ll_i, 6),
            "oned_number": round(ll_1, 6),
            "geometry": round(ll_g, 6),
        },
        "margin_geometry_minus_oned": round(acc_g - acc_1, 6),
        "margin_geometry_minus_intercept": round(acc_g - acc_i, 6),
        "beta_number": round(float(b_g[i_num]), 6),
        "beta_species_pets_minus_human_types_sum": round(species, 6),
        "beta_pets_dog_cat_sum": round(pets, 6),
        "beta_human_types_sum": round(humans, 6),
        "beta_number_oned_model": round(float(b_1[0]), 6),
        "status": status,
        "reason": reason,
        "validation": {
            "estimator": "FE logit; 8 inner Newton steps on alpha_i per outer iter; max 80 outer",
            "converged": conv_ok,
            "fit_intercept": d_i,
            "fit_oned": d_1,
            "fit_geometry": d_g,
            "collinearity": collinear,
            "geometry_without_number_heldout_accuracy": round(acc_g0, 6),
            "geometry_without_number_heldout_logloss": round(ll_g0, 6),
            "unit_bootstrap": boot,
        },
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("OUTCOME", status, reason)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
