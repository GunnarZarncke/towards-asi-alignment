#!/usr/bin/env python3
"""Downsize chapter-opening illustrations for web use.

The source PNGs in figures/illustrations/ are full-resolution exports meant
for print (used directly by \\includegraphics in the chapter .tex files).
This script derives smaller, compressed JPEGs in figures/illustrations/web/
for the companion site, which serves images straight from GitHub raw content
(see site/scripts/lib/tex-convert.mjs FIGURE_BASE) and has no benefit from
multi-megabyte print-resolution PNGs.

Usage:
    python3 scripts/generate_web_illustrations.py [--max-width 1600] [--quality 82]

Re-run whenever a source illustration in figures/illustrations/ changes or a
new one is added; only regenerates outputs that are missing or older than
their source.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "figures" / "illustrations"
WEB_DIR = SOURCE_DIR / "web"


def find_sources() -> list[Path]:
    return sorted(p for p in SOURCE_DIR.glob("ch*.png") if p.is_file())


def web_path_for(source: Path) -> Path:
    return WEB_DIR / f"{source.stem}.jpg"


def needs_regeneration(source: Path, target: Path) -> bool:
    if not target.exists():
        return True
    return source.stat().st_mtime > target.stat().st_mtime


def convert_one(source: Path, target: Path, max_width: int, quality: int) -> tuple[int, int]:
    with Image.open(source) as img:
        img = img.convert("RGB")
        if img.width > max_width:
            new_height = round(img.height * (max_width / img.width))
            img = img.resize((max_width, new_height), Image.LANCZOS)
        target.parent.mkdir(parents=True, exist_ok=True)
        img.save(target, "JPEG", quality=quality, optimize=True, progressive=True)
    return source.stat().st_size, target.stat().st_size


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-width", type=int, default=1600, help="Maximum output width in pixels (default: 1600)")
    parser.add_argument("--quality", type=int, default=82, help="JPEG quality 1-95 (default: 82)")
    parser.add_argument("--force", action="store_true", help="Regenerate even if the web version is up to date")
    args = parser.parse_args()

    sources = find_sources()
    if not sources:
        print(f"No source illustrations found in {SOURCE_DIR}")
        return 0

    total_before = 0
    total_after = 0
    skipped = 0
    for i, source in enumerate(sources, start=1):
        target = web_path_for(source)
        if not args.force and not needs_regeneration(source, target):
            skipped += 1
            print(f"[{i}/{len(sources)}] {source.name}: up to date, skipping")
            continue
        before, after = convert_one(source, target, args.max_width, args.quality)
        total_before += before
        total_after += after
        print(f"[{i}/{len(sources)}] {source.name}: {before / 1024:.0f} KB -> {target.relative_to(ROOT)} {after / 1024:.0f} KB")

    if total_before:
        print(
            f"Done. Regenerated {len(sources) - skipped}/{len(sources)} "
            f"({total_before / 1024 / 1024:.1f} MB -> {total_after / 1024 / 1024:.1f} MB)."
        )
    else:
        print(f"Done. All {len(sources)} web illustrations already up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
