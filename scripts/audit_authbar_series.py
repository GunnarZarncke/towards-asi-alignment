#!/usr/bin/env python3
"""§3.1 authbar word-share on load-bearing chapters.

Weights each \\begin{authbar} span by prose word count (authbar lines and
comments excluded; LaTeX commands stripped approximately). Emits a CSV and
prints the GZ-touched share.

Stop (frozen 2026-11-02):
  GZ_TOUCHED_MIN = 0.02   # share of words on spans keyed GZ or GZ+AI
  Volume gate (optional --month YYYY-MM): manuscript interval lines and tracked
  lines must be >= October 2026 totals in edit-attribution/2026-10.csv
  (4346 manuscript, 11591 tracked). Below that volume the stop does not arm.

Exit 0: share at or above threshold, or volume gate not met.
Exit 1: stop armed and GZ-touched share below threshold.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "hooks"))
from edit_attr import AUTH_BEGIN_RE, AUTH_END, parse_authbar_spans  # noqa: E402

GZ_TOUCHED_MIN = 0.02
LOAD_BEARING = ("ch03", "ch16", "ch25", "ch26", "ch30", "ch34", "ch42", "ch43", "ch48")
VOLUME_BASELINE = ROOT / "drafts/project/self-audit/edit-attribution/2026-10.csv"
MIN_MANUSCRIPT_LINES = 4346
MIN_TRACKED_LINES = 11591
OUT_DIR = ROOT / "drafts/project/self-audit/edit-attribution"


def chapter_id(path: Path) -> str | None:
    m = re.match(r"ch(\d+)", path.name)
    return f"ch{int(m.group(1)):02d}" if m else None


def load_bearing_files() -> list[Path]:
    out: list[Path] = []
    for ch in LOAD_BEARING:
        matches = sorted((ROOT / "chapters").glob(f"{ch}-*.tex"))
        if not matches:
            raise SystemExit(f"missing chapter file for {ch}")
        out.append(matches[0])
    return out


def strip_prose(text: str) -> str:
    text = re.sub(r"(?<!\\)%.*", "", text)
    text = re.sub(r"\\begin\{[^}]+\}", " ", text)
    text = re.sub(r"\\end\{[^}]+\}", " ", text)
    text = re.sub(r"\\(?:label|index|leanspine|autocite|cite[a-z]*|wikiq)\{[^{}]*\}", " ", text)
    text = re.sub(r"\\(?:emph|textbf|textit|texttt)\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\[a-zA-Z@]+\*?(?:\[[^\]]*\])?", " ", text)
    text = text.replace("{", " ").replace("}", " ")
    return text


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z]+)?", strip_prose(text)))


def span_body_words(lines: list[str], start: int, end: int) -> int:
    """start/end are 1-based inclusive authbar span bounds."""
    chunk: list[str] = []
    for i in range(start - 1, end):
        line = lines[i]
        if AUTH_BEGIN_RE.search(line) or AUTH_END in line:
            continue
        chunk.append(line)
    return word_count("\n".join(chunk))


def measure_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    spans = parse_authbar_spans(text)
    by_key = {"GZ": 0, "GZ+AI": 0, "AI": 0}
    for start, end, key in spans:
        if key not in by_key:
            by_key[key] = 0
        by_key[key] += span_body_words(lines, start, end)
    total = sum(by_key.values())
    touched = by_key.get("GZ", 0) + by_key.get("GZ+AI", 0)
    share = (touched / total) if total else 0.0
    return {
        "chapter": chapter_id(path) or path.stem,
        "file": path.relative_to(ROOT).as_posix(),
        "words_gz": by_key.get("GZ", 0),
        "words_gz_ai": by_key.get("GZ+AI", 0),
        "words_ai": by_key.get("AI", 0),
        "words_total": total,
        "gz_touched_share": share,
    }


def parse_month_volume(month: str) -> tuple[int, int] | None:
    path = OUT_DIR / f"{month}.csv"
    if not path.is_file():
        return None
    manuscript = 0
    tracked = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# unattributed_share"):
            m = re.search(r"tracked_lines,(\d+)", line)
            if m:
                tracked = int(m.group(1))
            continue
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split(",", 5)
        if len(parts) < 5 or parts[0] == "kind":
            continue
        _kind, cls, _ch, added, removed = parts[:5]
        n = int(added) + int(removed)
        if cls == "manuscript":
            manuscript += n
    if tracked == 0:
        return None
    return manuscript, tracked


def volume_gate_met(month: str | None) -> tuple[bool, str]:
    if not month:
        return False, "no --month; volume gate not evaluated (stop not armed)"
    vol = parse_month_volume(month)
    if vol is None:
        return False, f"no edit-attribution/{month}.csv; volume gate not met"
    manuscript, tracked = vol
    if manuscript >= MIN_MANUSCRIPT_LINES and tracked >= MIN_TRACKED_LINES:
        return True, f"volume ok (manuscript={manuscript}, tracked={tracked})"
    return False, (
        f"volume below October baseline (manuscript={manuscript}/{MIN_MANUSCRIPT_LINES}, "
        f"tracked={tracked}/{MIN_TRACKED_LINES})"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--month", help="YYYY-MM for volume gate (edit-attribution CSV)")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="CSV path (default: edit-attribution/authbar-series-<UTC-date>.csv)",
    )
    args = parser.parse_args()

    rows = [measure_file(p) for p in load_bearing_files()]
    total_words = sum(r["words_total"] for r in rows)
    touched_words = sum(r["words_gz"] + r["words_gz_ai"] for r in rows)
    aggregate_share = (touched_words / total_words) if total_words else 0.0

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out_path = args.out or (OUT_DIR / f"authbar-series-{ts[:10]}.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "chapter",
        "file",
        "words_gz",
        "words_gz_ai",
        "words_ai",
        "words_total",
        "gz_touched_share",
    ]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow({k: (f"{row[k]:.4f}" if k == "gz_touched_share" else row[k]) for k in fieldnames})
        w.writerow(
            {
                "chapter": "TOTAL",
                "file": "",
                "words_gz": sum(r["words_gz"] for r in rows),
                "words_gz_ai": sum(r["words_gz_ai"] for r in rows),
                "words_ai": sum(r["words_ai"] for r in rows),
                "words_total": total_words,
                "gz_touched_share": f"{aggregate_share:.4f}",
            }
        )
        f.write(f"# generated_at,{ts}\n")
        f.write(f"# gz_touched_min,{GZ_TOUCHED_MIN}\n")

    gate, gate_msg = volume_gate_met(args.month)
    print(f"wrote {out_path.relative_to(ROOT)}")
    print(
        f"load-bearing words {total_words}: GZ {sum(r['words_gz'] for r in rows)} "
        f"GZ+AI {sum(r['words_gz_ai'] for r in rows)} "
        f"AI {sum(r['words_ai'] for r in rows)}"
    )
    print(f"gz_touched_share {aggregate_share:.4f} (stop below {GZ_TOUCHED_MIN:.2f})")
    print(gate_msg)

    for row in rows:
        print(
            f"  {row['chapter']:5}  share {row['gz_touched_share']:.3f}  "
            f"words {row['words_total']}"
        )

    if gate and aggregate_share < GZ_TOUCHED_MIN:
        print("STOP: GZ-touched share below threshold on load-bearing chapters.")
        return 1
    if gate:
        print("PASS: share at or above threshold (volume gate met).")
    else:
        print("PASS: stop not armed (volume gate not met).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
