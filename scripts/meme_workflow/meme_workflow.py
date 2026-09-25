#!/usr/bin/env python3
"""Minimal meme workflow: find template, detect text boxes, render captions.

Steps:
  1. Match a natural-language description to an imgflip blank template and download it.
  2. Infer caption rectangles from template layout (imgflip metadata + heuristics).
  3. Draw wrapped text into those rectangles.

Usage:
  python3 scripts/meme_workflow/meme_workflow.py
  python3 scripts/meme_workflow/meme_workflow.py --job huang-release-rule
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
TEMPLATES_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT / "output"
JOBS_PATH = ROOT / "memes.json"
IMGFLIP_MEMES_URL = "https://api.imgflip.com/get_memes"

# Extra keywords for fuzzy template search (description token -> template name tokens).
SEARCH_ALIASES: dict[str, tuple[str, ...]] = {
    "anakin": ("anakin", "padme", "panel"),
    "padme": ("anakin", "padme", "panel"),
    "star": ("anakin", "padme"),
    "wars": ("anakin", "padme"),
    "right": ("anakin", "padme"),
    "midwit": ("bell", "curve"),
    "iq": ("bell", "curve"),
    "bell": ("bell", "curve"),
    "curve": ("bell", "curve"),
    "commons": ("bell", "curve"),
    "fine": ("this", "is", "fine"),
    "burning": ("this", "is", "fine"),
    "dog": ("this", "is", "fine"),
    "office": ("this", "is", "fine"),
    "pigeon": ("pigeon",),
    "butterfly": ("pigeon",),
    "anime": ("pigeon",),
    "ruler": ("pigeon",),
    "stop": ("pigeon",),
}


@dataclass(frozen=True)
class MemeTemplate:
    template_id: str
    name: str
    url: str
    width: int
    height: int
    box_count: int


@dataclass(frozen=True)
class TextBox:
    x: int
    y: int
    w: int
    h: int


# Fallback if the imgflip catalog request is blocked offline.
LOCAL_CATALOG: tuple[MemeTemplate, ...] = (
    MemeTemplate("322841258", "Anakin Padme 4 Panel", "https://i.imgflip.com/5c7lwq.png", 768, 768, 3),
    MemeTemplate("533936279", "Bell Curve", "https://i.imgflip.com/8tw3vb.png", 675, 499, 3),
    MemeTemplate("55311130", "This Is Fine", "https://i.imgflip.com/wxica.jpg", 580, 282, 2),
    MemeTemplate("100777631", "Is This A Pigeon", "https://i.imgflip.com/1o00in.jpg", 1587, 1425, 3),
)


def _urlopen(url: str, timeout: int = 30) -> object:
    req = urllib.request.Request(url, headers={"User-Agent": "towards-asi-alignment-meme-workflow/1.0"})
    return urllib.request.urlopen(req, timeout=timeout)


def fetch_imgflip_catalog() -> list[MemeTemplate]:
    with _urlopen(IMGFLIP_MEMES_URL) as resp:
        payload = json.load(resp)
    return [
        MemeTemplate(
            template_id=str(item["id"]),
            name=item["name"],
            url=item["url"],
            width=int(item["width"]),
            height=int(item["height"]),
            box_count=int(item["box_count"]),
        )
        for item in payload["data"]["memes"]
    ]


def tokenize(text: str) -> set[str]:
    return {t for t in re.split(r"[^a-z0-9]+", text.lower()) if t}


def score_template(description: str, template: MemeTemplate) -> int:
    desc_tokens = tokenize(description)
    name_tokens = tokenize(template.name)
    score = len(desc_tokens & name_tokens) * 3
    for token in desc_tokens:
        for alias in SEARCH_ALIASES.get(token, ()):
            if alias in name_tokens:
                score += 2
    return score


def find_template(description: str, catalog: list[MemeTemplate]) -> MemeTemplate:
    ranked = sorted(catalog, key=lambda t: score_template(description, t), reverse=True)
    if not ranked or score_template(description, ranked[0]) == 0:
        raise RuntimeError(f"No imgflip template matched description: {description!r}")
    return ranked[0]


def download_template(template: MemeTemplate, force: bool = False) -> Path:
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    suffix = Path(urllib.parse.urlparse(template.url).path).suffix or ".jpg"
    path = TEMPLATES_DIR / f"{template.template_id}{suffix}"
    if path.exists() and not force:
        return path
    print(f"  [1/3] download {template.name} -> {path.name}")
    with _urlopen(template.url, timeout=60) as resp:
        path.write_bytes(resp.read())
    return path


def _norm_boxes(width: int, height: int, rel_boxes: list[tuple[float, float, float, float]]) -> list[TextBox]:
    out: list[TextBox] = []
    for rx, ry, rw, rh in rel_boxes:
        out.append(
            TextBox(
                x=int(rx * width),
                y=int(ry * height),
                w=max(1, int(rw * width)),
                h=max(1, int(rh * height)),
            )
        )
    return out


def layout_boxes(template: MemeTemplate, text_count: int) -> list[tuple[float, float, float, float]]:
    name = template.name.lower()

    if "anakin padme" in name and text_count == 4:
        # 2x2 panels; captions sit in the upper band of each quadrant (panel 3 stays blank).
        return [
            (0.03, 0.02, 0.44, 0.16),
            (0.53, 0.02, 0.44, 0.16),
            (0.03, 0.52, 0.44, 0.16),
            (0.53, 0.52, 0.44, 0.16),
        ]

    if "bell curve" in name and text_count == 3:
        return [
            (0.04, 0.58, 0.24, 0.34),
            (0.34, 0.62, 0.32, 0.30),
            (0.72, 0.58, 0.24, 0.34),
        ]

    if "this is fine" in name and text_count == 1:
        return [(0.10, 0.62, 0.80, 0.30)]

    if "pigeon" in name and text_count == 2:
        return [
            (0.58, 0.10, 0.34, 0.14),  # butterfly label
            (0.12, 0.93, 0.76, 0.06),  # subtitle bar (covers template caption)
        ]

    # Generic fallback: stack equal horizontal bands using imgflip box_count.
    bands = max(text_count, template.box_count, 1)
    step = 1.0 / bands
    return [(0.05, i * step + 0.02, 0.90, step - 0.04) for i in range(text_count)]


def prepare_template_image(image: Image.Image, template: MemeTemplate) -> Image.Image:
    name = template.name.lower()
    if "this is fine" in name:
        # imgflip ships a two-panel strip; keep the left panel only.
        w, h = image.size
        return image.crop((0, 0, w // 2, h))
    if "pigeon" in name:
        out = image.copy()
        draw = ImageDraw.Draw(out)
        w, h = out.size
        draw.rectangle((0, int(h * 0.905), w, h), fill="black")
        return out
    return image


def detect_text_regions(image: Image.Image, template: MemeTemplate, texts: list[str]) -> list[TextBox]:
    """Infer caption rectangles from template identity and image size."""
    rel = layout_boxes(template, len(texts))
    boxes = _norm_boxes(image.width, image.height, rel)
    print(f"  [2/3] detected {len(boxes)} text region(s) for {template.name} ({image.width}x{image.height})")
    for i, box in enumerate(boxes, start=1):
        print(f"        box {i}: x={box.x} y={box.y} w={box.w} h={box.h}")
    return boxes


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Impact.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def wrap_text(text: str, font: ImageFont.ImageFont, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        trial = f"{current} {word}"
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def fit_font(
    text: str,
    box: TextBox,
    draw: ImageDraw.ImageDraw,
    max_size: int = 48,
    min_size: int = 12,
) -> tuple[ImageFont.ImageFont, list[str]]:
    for size in range(max_size, min_size - 1, -2):
        font = load_font(size)
        lines = wrap_text(text, font, box.w - 8, draw)
        if not lines:
            return font, []
        line_heights = [font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines]
        total_h = sum(line_heights) + max(0, len(lines) - 1) * 2
        max_line_w = max(draw.textlength(line, font=font) for line in lines)
        if total_h <= box.h - 6 and max_line_w <= box.w - 8:
            return font, lines
    font = load_font(min_size)
    return font, wrap_text(text, font, box.w - 8, draw)


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    box: TextBox,
    text: str,
    fill: str = "white",
    stroke_fill: str = "black",
    stroke_width: int = 2,
) -> None:
    if not text.strip():
        return
    font, lines = fit_font(text, box, draw)
    if not lines:
        return
    line_heights = [font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines]
    total_h = sum(line_heights) + max(0, len(lines) - 1) * 2
    y = box.y + max(0, (box.h - total_h) // 2)
    for line, lh in zip(lines, line_heights):
        line_w = draw.textlength(line, font=font)
        x = box.x + max(0, (box.w - line_w) // 2)
        draw.text((x, y), line, font=font, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)
        y += lh + 2


def paste_text(image: Image.Image, boxes: list[TextBox], texts: list[str]) -> Image.Image:
    out = image.copy()
    draw = ImageDraw.Draw(out)
    print(f"  [3/3] pasting {len(texts)} caption(s)")
    for box, text in zip(boxes, texts):
        draw_centered_text(draw, box, text)
    return out


def run_job(job: dict, catalog: list[MemeTemplate], force_download: bool = False) -> Path:
    job_id = job["id"]
    description = job["template_description"]
    texts = job["texts"]
    print(f"\n=== {job_id} ===")
    template = find_template(description, catalog)
    print(f"  matched template: {template.name} ({template.url})")
    path = download_template(template, force=force_download)
    with Image.open(path) as image:
        image = prepare_template_image(image.convert("RGB"), template)
        boxes = detect_text_regions(image, template, texts)
        result = paste_text(image, boxes, texts)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        out_path = OUTPUT_DIR / f"{job_id}.jpg"
        result.save(out_path, "JPEG", quality=92)
        print(f"  wrote {out_path}")
        return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--job", help="Run a single job id from memes.json")
    parser.add_argument("--force-download", action="store_true", help="Re-download templates")
    args = parser.parse_args()

    jobs = json.loads(JOBS_PATH.read_text(encoding="utf-8"))
    if args.job:
        jobs = [j for j in jobs if j["id"] == args.job]
        if not jobs:
            print(f"Unknown job id: {args.job}", file=sys.stderr)
            return 1

    try:
        catalog = fetch_imgflip_catalog()
    except urllib.error.URLError as exc:
        print(f"imgflip catalog unavailable ({exc}); using local fallback catalog", file=sys.stderr)
        catalog = list(LOCAL_CATALOG)

    outputs: list[Path] = []
    for job in jobs:
        outputs.append(run_job(job, catalog, force_download=args.force_download))

    print(f"\nDone. {len(outputs)} meme(s) in {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
