#!/usr/bin/env python3
"""Link known terms in agenda YAML prose fields using data/term-links.yml.

Usage:
  python3 reference/field-agendas/scripts/link-agenda-terms.py
  python3 reference/field-agendas/scripts/link-agenda-terms.py --check
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
DATA = REPO / "reference" / "field-agendas" / "data"
AGENDAS = DATA / "agendas"
TERM_LINKS = DATA / "term-links.yml"

PROSE_FIELDS = [
    "overview",
    "statedIntent",
    "primaryCrux",
    "primaryArtifact",
    "contributes",
    "bookSeparates",
    "reviewStatus",
]
SIGNATURE_FIELD = "signatureVocabulary"
ALL_TEXT_FIELDS = PROSE_FIELDS + [SIGNATURE_FIELD]

PROTECT_RE = re.compile(
    r"(\[[^\]]*\]\([^)]+\)|https?://\S+|`[^`]+`)",
    re.MULTILINE,
)
STRIP_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")


def strip_links(text: str) -> str:
    """Remove markdown links, keeping display text (for clean re-link passes)."""
    prev = None
    cur = text
    while prev != cur:
        prev = cur
        cur = STRIP_LINK_RE.sub(r"\1", cur)
    return cur


def load_terms():
    raw = yaml.safe_load(TERM_LINKS.read_text())["terms"]
    return sorted(raw, key=lambda t: (-len(t["phrase"]), t["phrase"]))


def applies(term: dict, field: str, slug: str) -> bool:
    fields = term.get("fields", "all")
    if fields == "all":
        ok_field = True
    elif fields == "signature":
        ok_field = field == SIGNATURE_FIELD
    elif fields == "prose":
        ok_field = field in PROSE_FIELDS
    else:
        ok_field = False
    agendas = term.get("agendas")
    ok_agenda = agendas is None or slug in agendas
    return ok_field and ok_agenda


def _split_protected(text: str) -> list[tuple[str, str]]:
    parts = []
    last = 0
    for m in PROTECT_RE.finditer(text):
        if m.start() > last:
            parts.append(("raw", text[last : m.start()]))
        parts.append(("prot", m.group(0)))
        last = m.end()
    if last < len(text):
        parts.append(("raw", text[last:]))
    return parts


def link_text(text: str, terms: list, field: str, slug: str) -> str:
    if not text or not isinstance(text, str):
        return text

    # One link per phrase per field (same URL may appear on different phrases).
    used_phrases: set[str] = set()
    current = text
    for term in terms:
        if not applies(term, field, slug):
            continue
        phrase = term["phrase"]
        if phrase in used_phrases:
            continue
        url = term["url"]
        pattern = re.compile(
            r"(?<![A-Za-z0-9_/])(" + re.escape(phrase) + r")(?![A-Za-z0-9_/])"
        )
        rebuilt = []
        matched = False
        for kind, chunk in _split_protected(current):
            if kind == "prot" or matched:
                rebuilt.append(chunk)
                continue
            new_chunk, n = pattern.subn(
                lambda match, u=url: f"[{match.group(1)}]({u})", chunk, count=1
            )
            rebuilt.append(new_chunk)
            if n:
                matched = True
                used_phrases.add(phrase)
        current = "".join(rebuilt)
    return current


def fold_scalar(text: str) -> str:
    compact = re.sub(r"\s+", " ", text.strip())
    words = compact.split(" ")
    lines = []
    cur = ""
    for w in words:
        trial = w if not cur else f"{cur} {w}"
        if len(trial) > 88 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return ">-\n" + "\n".join("  " + line for line in lines)


def q(s: str) -> str:
    return yaml.dump(s, default_style='"').strip()


def dump_agenda(data: dict) -> str:
    lines = []
    order = [
        "slug",
        "title",
        "type",
        "generateCard",
        "matrixLink",
        "carrier",
        "overview",
        "primaryArtifact",
        "signatureVocabulary",
        "statedIntent",
        "primaryCrux",
        "bookBridges",
        "contributes",
        "bookSeparates",
        "reviewStatus",
        "manuscriptHooks",
        "links",
    ]
    seen = set()

    def emit(key: str) -> None:
        if key not in data or key in seen:
            return
        seen.add(key)
        val = data[key]
        if val is None:
            return
        if key in ALL_TEXT_FIELDS and isinstance(val, str):
            lines.append(f"{key}: {fold_scalar(val)}")
        elif key == "bookBridges":
            if not val:
                lines.append("bookBridges: []")
            else:
                lines.append("bookBridges:")
                for b in val:
                    lines.append(f"  - {b}")
        elif key == "manuscriptHooks":
            if not val:
                lines.append("manuscriptHooks: []")
            else:
                lines.append("manuscriptHooks:")
                for h in val:
                    hs = str(h)
                    if re.search(r"[:#{}[\],&*?|>!%@`'\\]", hs) or hs.startswith("`"):
                        lines.append(f"  - {q(hs)}")
                    else:
                        lines.append(f"  - {hs}")
        elif key == "links":
            lines.append("links:")
            for link in val:
                lines.append(f"  - label: {q(link['label'])}")
                url = link["url"]
                if len(url) > 88:
                    lines.append("    url: >-")
                    lines.append(f"      {url}")
                else:
                    lines.append(f"    url: {url}")
        elif key == "generateCard":
            lines.append(f"generateCard: {str(val).lower()}")
        elif isinstance(val, str):
            if "\n" in val or len(val) > 88:
                lines.append(f"{key}: {fold_scalar(val)}")
            elif re.search(r"[:#{}[\],&*?|>!%@`'\\]", val):
                lines.append(f"{key}: {q(val)}")
            else:
                lines.append(f"{key}: {val}")
        else:
            lines.append(f"{key}: {yaml.dump(val, default_flow_style=True).strip()}")

    for key in order:
        emit(key)
    for key in data:
        emit(key)
    return "\n".join(lines) + "\n"


def process(path: Path, terms: list, check: bool, relink: bool) -> bool:
    original = path.read_text()
    data = yaml.safe_load(original)
    slug = data["slug"]
    content_changed = False
    for field in ALL_TEXT_FIELDS:
        if field not in data or not data[field]:
            continue
        before = data[field]
        base = strip_links(before) if relink else before
        after = link_text(base, terms, field, slug)
        if after != before:
            data[field] = after
            content_changed = True

    if not content_changed:
        return False
    if check:
        return True

    path.write_text(dump_agenda(data))
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument(
        "--relink",
        action="store_true",
        help="Strip existing markdown links in prose fields, then re-apply term links.",
    )
    args = ap.parse_args()
    terms = load_terms()
    changed = []
    for path in sorted(AGENDAS.glob("*.yml")):
        if process(path, terms, check=args.check, relink=args.relink):
            changed.append(path.name)
    if args.check:
        if changed:
            print(f"link-agenda-terms --check: {len(changed)} file(s) need linking:")
            for f in changed:
                print(f"  {f}")
            sys.exit(1)
        print("link-agenda-terms --check: ok")
        return
    print(f"link-agenda-terms: updated {len(changed)} agenda file(s).")
    for f in changed:
        print(f"  {f}")


if __name__ == "__main__":
    main()
