#!/usr/bin/env python3
"""Assemble the monthly section-vintage review (§3.16).

Writes a review file whose excerpts are labeled TOP, TOP_OLD, RANDOM, or
RANDOM_OLD, and a sibling key file used only by score_monthly_review.py.

Current text is the working tree. An old excerpt is an earlier git blob of a
different path, and only if the shown window differs by at least
MATERIAL_WORDS word tokens. The same path is never used twice.

This script does not modify manuscript or site sources.

Stop (enforced by score_monthly_review.py, not here): every TOP and TOP_OLD
excerpt has exactly one label left, and it matches the key. RANDOM and
RANDOM_OLD are reported and do not fire the stop.

Frozen 2026-11-02:
  MIN_EXCERPTS = 6
  MIN_TOP = 3          # TOP + TOP_OLD
  TARGET_WORDS = 800
  WINDOW_WORDS = 130
  MATERIAL_WORDS = 20  # multiset symmetric difference in the window
"""

from __future__ import annotations

import argparse
import json
import random
import re
import secrets
import subprocess
import sys
from pathlib import Path

MIN_EXCERPTS = 6
MIN_TOP = 3
TARGET_OLD = 2
TARGET_CURRENT = 2
TARGET_WORDS = 800
WINDOW_WORDS = 130
MATERIAL_WORDS = 20
WORD_BAND = 80

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "drafts" / "project" / "self-audit" / "monthly-review"

LABELS = ("TOP", "TOP_OLD", "RANDOM", "RANDOM_OLD")
LABEL_BLOCK = "\n".join(LABELS)
HEADING_CMD = {
    "section": 1,
    "subsection": 2,
    "subsubsection": 3,
}


def git_show(rev: str, path: str) -> str | None:
    proc = subprocess.run(
        ["git", "show", f"{rev}:{path}"],
        cwd=ROOT,
        capture_output=True,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8", errors="replace")


def git_revs(path: str, limit: int = 25) -> list[str]:
    proc = subprocess.run(
        ["git", "log", "-n", str(limit), "--format=%H", "--", path],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return []
    return [line for line in proc.stdout.splitlines() if line]


def word_tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z]+)?", text)


def symdiff(a: list[str], b: list[str]) -> int:
    from collections import Counter

    ca = Counter(w.lower() for w in a)
    cb = Counter(w.lower() for w in b)
    return sum(abs(ca[k] - cb[k]) for k in set(ca) | set(cb))


def norm_heading(heading: str) -> str:
    heading = re.sub(r"\\[a-zA-Z]+\*?", "", heading)
    heading = heading.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", heading).strip().lower()


def strip_tex_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", text)


def _math_to_prose(inner: str) -> str:
    inner = re.sub(r"\\text\{([^{}]*)\}", r"\1", inner)
    inner = re.sub(r"\\[a-zA-Z]+", " ", inner)
    inner = inner.replace("{", " ").replace("}", " ")
    return " ".join(inner.split())


def display_tex(body: str) -> str:
    body = strip_tex_comments(body)
    body = re.sub(r"\\begin\{figure\*?\}.*?\\end\{figure\*?\}", " ", body, flags=re.S)
    body = re.sub(
        r"\\begin\{(?:equation|align|gather)\*?\}(.*?)\\end\{(?:equation|align|gather)\*?\}",
        lambda m: " " + _math_to_prose(m.group(1)) + " ",
        body,
        flags=re.S,
    )
    body = re.sub(r"\\\[(.*?)\\\]", lambda m: " " + _math_to_prose(m.group(1)) + " ", body, flags=re.S)
    body = re.sub(r"\$([^$]+)\$", lambda m: " " + _math_to_prose(m.group(1)) + " ", body)
    body = re.sub(r"\\begin\{authbar\}\{[^{}]*\}", " ", body)
    body = re.sub(r"\\end\{authbar\}", " ", body)
    body = re.sub(r"\\authbar(?:sub)?needspace", " ", body)
    body = re.sub(
        r"\\wikiq\{[^{}]*\}\{([^{}]*)\}\{([^{}]*)\}",
        r"\1: \2",
        body,
    )
    body = re.sub(r"\\(?:ref|eqref|pageref)\{([^{}]*)\}", r"(\1)", body)
    for _ in range(4):
        body = re.sub(
            r"\\(?:emph|textbf|textit|texttt|paragraph)\{([^{}]*)\}",
            r"\1",
            body,
        )
    body = re.sub(r"\\(?:label|index|leanspine|autocite|cite[a-z]*)\{[^{}]*\}", " ", body)
    body = re.sub(r"\\begin\{[^}]+\}", " ", body)
    body = re.sub(r"\\end\{[^}]+\}", " ", body)
    body = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", " ", body)
    body = body.replace("{", "").replace("}", "")
    body = body.replace("~", " ")
    body = re.sub(r"[ \t]+", " ", body)
    body = re.sub(r" *\n *", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def display_md(body: str) -> str:
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    body = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", body)
    body = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", body)
    return body.strip()


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.replace("\n", " "))
    return [p.strip() for p in parts if word_tokens(p)]


def take_window(sents: list[str], start: int, n_words: int) -> tuple[str, int]:
    chosen: list[str] = []
    count = 0
    for sentence in sents[start:]:
        chosen.append(sentence)
        count += len(word_tokens(sentence))
        if count >= n_words:
            break
    return " ".join(chosen), count


def split_tex(text: str) -> list[dict]:
    text = strip_tex_comments(text)
    marks: list[tuple[int, int, str, int]] = []
    for match in re.finditer(r"\\(section|subsection|subsubsection)\*?\{", text):
        level = HEADING_CMD[match.group(1)]
        start = match.end()
        depth = 1
        j = start
        while j < len(text) and depth:
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
            j += 1
        if depth != 0:
            continue
        marks.append((match.start(), j, text[start : j - 1].strip(), level))
    sections = []
    for i, (_s, body_at, title, level) in enumerate(marks):
        end = len(text)
        for later in marks[i + 1 :]:
            if later[3] <= level:
                end = later[0]
                break
        sections.append({"heading": title, "body": text[body_at:end], "kind": "tex"})
    return sections


def split_md(text: str) -> list[dict]:
    title = ""
    front = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    if front:
        found = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', front.group(1), flags=re.M)
        title = found.group(1).strip() if found else ""
        text = text[front.end() :]
    marks = list(re.finditer(r"^##+ (.+)$", text, flags=re.M))
    if not marks:
        body = text.strip()
        return [{"heading": title or "(opening)", "body": body, "kind": "md"}] if body else []
    sections = []
    for i, match in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        sections.append(
            {"heading": match.group(1).strip(), "body": text[match.end() : end], "kind": "md"}
        )
    return sections


def split_file(text: str, path: str) -> list[dict]:
    if path.endswith(".tex"):
        return split_tex(text)
    return split_md(text)


def prose(section: dict) -> str:
    if section["kind"] == "tex":
        return display_tex(section["body"])
    return display_md(section["body"])


def source_files() -> list[str]:
    paths: list[Path] = []
    paths.extend(sorted((ROOT / "chapters").glob("*.tex")))
    paths.extend(sorted((ROOT / "appendices").glob("*.tex")))
    for path in sorted((ROOT / "site" / "src" / "content").rglob("*.md")):
        if "quiz" in path.parts:
            continue
        paths.append(path)
    rels = []
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        if path.stat().st_size < 400:
            continue
        rels.append(rel)
    return rels


def load_text(path: str, rev: str | None) -> str | None:
    if rev is None:
        file_path = ROOT / path
        if not file_path.is_file():
            return None
        return file_path.read_text(encoding="utf-8", errors="replace")
    return git_show(rev, path)


def find_section(text: str, path: str, heading: str) -> dict | None:
    want = norm_heading(heading)
    for section in split_file(text, path):
        if norm_heading(section["heading"]) == want:
            return section
    return None


def material_pair(new_prose: str, old_prose: str, n_words: int) -> tuple[str, str, int] | None:
    new_sents = sentences(new_prose)
    old_sents = sentences(old_prose)
    if not new_sents or not old_sents:
        return None
    limit = max(len(new_sents), len(old_sents))
    for start in range(limit):
        new_window, _n = take_window(new_sents, start, n_words)
        old_window, _o = take_window(old_sents, start, n_words)
        if not new_window or not old_window:
            continue
        delta = symdiff(word_tokens(new_window), word_tokens(old_window))
        if delta >= MATERIAL_WORDS:
            return new_window, old_window, delta
    return None


def best_changed_section(path: str, heading_hint: str, n_words: int) -> dict | None:
    current = load_text(path, None)
    if current is None:
        return None
    sections = split_file(current, path)
    if heading_hint:
        wanted = norm_heading(heading_hint)
        sections = [s for s in sections if norm_heading(s["heading"]) == wanted]
    blob_cache: dict[str, str | None] = {}
    for rev in git_revs(path):
        if rev not in blob_cache:
            blob_cache[rev] = load_text(path, rev)
        old_text = blob_cache[rev]
        if old_text is None:
            continue
        for section in sections:
            old_section = find_section(old_text, path, section["heading"])
            if old_section is None:
                continue
            pair = material_pair(prose(section), prose(old_section), n_words)
            if pair is None:
                continue
            _new_window, _old_window, _delta = pair
            # Most recent rev wins; first changed section in that rev.
            return {
                "path": path,
                "heading": section["heading"],
                "current": _new_window,
                "old": _old_window,
                "rev": rev,
                "delta": _delta,
            }
    # No historical contrast. Still usable as a current excerpt.
    for section in sections:
        window, count = take_window(sentences(prose(section)), 0, n_words)
        if count >= 60:
            return {
                "path": path,
                "heading": section["heading"],
                "current": window,
                "old": None,
                "rev": None,
                "delta": 0,
            }
    return None


def opening_section(path: str, n_words: int, rng: random.Random) -> dict | None:
    current = load_text(path, None)
    if current is None:
        return None
    sections = [s for s in split_file(current, path) if len(word_tokens(prose(s))) >= 60]
    if not sections:
        return None
    rng.shuffle(sections)
    section = sections[0]
    window, count = take_window(sentences(prose(section)), 0, n_words)
    if count < 60:
        return None
    return {
        "path": path,
        "heading": section["heading"],
        "current": window,
        "old": None,
        "rev": None,
        "delta": 0,
    }


def opening_old(path: str, n_words: int, rng: random.Random) -> dict | None:
    current = load_text(path, None)
    if current is None:
        return None
    sections = split_file(current, path)
    rng.shuffle(sections)
    for rev in git_revs(path, limit=15):
        old_text = load_text(path, rev)
        if old_text is None:
            continue
        for section in sections:
            old_section = find_section(old_text, path, section["heading"])
            if old_section is None:
                continue
            new_window, _ = take_window(sentences(prose(section)), 0, n_words)
            old_window, old_count = take_window(sentences(prose(old_section)), 0, n_words)
            if old_count < 60 or not new_window:
                continue
            if symdiff(word_tokens(new_window), word_tokens(old_window)) < MATERIAL_WORDS:
                continue
            return {
                "path": path,
                "heading": section["heading"],
                "current": new_window,
                "old": old_window,
                "rev": rev,
                "delta": symdiff(word_tokens(new_window), word_tokens(old_window)),
            }
    return None


def select_top(picks: list[dict], n_words: int) -> list[dict]:
    prepared = []
    for pick in picks:
        path = pick["path"]
        print(f"[top] {path}", flush=True)
        found = best_changed_section(path, pick.get("heading") or "", n_words)
        if found is None:
            print(f"[top] skip {path}: no usable section", flush=True)
            continue
        found["reason"] = pick.get("reason") or ""
        prepared.append(found)
    chosen: list[dict] = []
    used: set[str] = set()
    n_old = 0
    n_cur = 0
    for item in prepared:
        if item["path"] in used:
            continue
        want_old = (
            n_old < TARGET_OLD and n_old <= n_cur and item["old"] is not None
        )
        if want_old:
            label, vintage = "TOP_OLD", "old"
            n_old += 1
        elif n_cur < TARGET_CURRENT:
            label, vintage = "TOP", "current"
            n_cur += 1
        else:
            continue
        used.add(item["path"])
        chosen.append({**item, "label": label, "vintage": vintage})
        if n_old >= 1 and n_cur >= 1 and n_old + n_cur >= max(MIN_TOP, TARGET_OLD + TARGET_CURRENT):
            if n_old >= TARGET_OLD and n_cur >= TARGET_CURRENT:
                break
    if n_old < 1 or n_cur < 1 or n_old + n_cur < MIN_TOP:
        raise SystemExit(
            f"need at least {MIN_TOP} top excerpts with both vintages; "
            f"got current={n_cur} old={n_old}"
        )
    return chosen


def select_rest(chosen: list[dict], rng: random.Random, n_words: int) -> list[dict]:
    used = {item["path"] for item in chosen}
    pool = [path for path in source_files() if path not in used]
    rng.shuffle(pool)
    rest: list[dict] = []

    print("[random] current", flush=True)
    for path in pool:
        found = opening_section(path, n_words, rng)
        if found is None:
            continue
        rest.append({**found, "label": "RANDOM", "vintage": "current", "reason": ""})
        used.add(path)
        break
    else:
        raise SystemExit("no random current section")

    print("[random] old", flush=True)
    for path in pool:
        if path in used:
            continue
        found = opening_old(path, n_words, rng)
        if found is None:
            continue
        rest.append({**found, "label": "RANDOM_OLD", "vintage": "old", "reason": ""})
        used.add(path)
        break
    else:
        raise SystemExit("no random old section with a material opening change")

    # Fill to MIN_EXCERPTS, alternating leftover random current then old.
    while len(chosen) + len(rest) < MIN_EXCERPTS:
        want_old = len(rest) % 2 == 1
        found_one = False
        for path in pool:
            if path in used:
                continue
            found = opening_old(path, n_words, rng) if want_old else opening_section(path, n_words, rng)
            if found is None:
                continue
            label = "RANDOM_OLD" if want_old else "RANDOM"
            vintage = "old" if want_old else "current"
            rest.append({**found, "label": label, "vintage": vintage, "reason": ""})
            used.add(path)
            found_one = True
            break
        if not found_one:
            raise SystemExit("could not fill the excerpt count")
    return rest


def excerpt_body(excerpt: dict) -> str:
    return excerpt["old"] if excerpt["vintage"] == "old" else excerpt["current"]


def render(month: str, excerpts: list[dict]) -> tuple[str, int]:
    words = sum(len(word_tokens(excerpt_body(excerpt))) for excerpt in excerpts)
    lines = [
        f"# Monthly section review — {month}",
        "",
        "Each excerpt is either the text in the working tree (`current`) or an earlier git version (`old`).",
        "Paths and revisions are not in this file.",
        "",
        f"About {words} words in {len(excerpts)} excerpts.",
        "",
        "Excerpt order (E1, E2, …) is shuffled. It does not indicate priority.",
        "",
        "Under each excerpt, four label lines appear: TOP, TOP_OLD, RANDOM, RANDOM_OLD.",
        "Delete all but the one that fits. Leave the prose as it is. Then score:",
        "",
        "```",
        f".venv/bin/python scripts/score_monthly_review.py drafts/project/self-audit/monthly-review/{month}.md",
        "```",
        "",
        "Open the sibling `.key.json` only after scoring.",
        "Top labels are the stop. Random labels are recorded and do not fire it.",
        "",
    ]
    for excerpt in excerpts:
        lines.extend(
            [
                f"## {excerpt['id']}",
                "",
                LABEL_BLOCK,
                "",
                f"### {excerpt['heading']}",
                "",
                excerpt_body(excerpt),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n", words


def key_payload(month: str, seed: str, excerpts: list[dict], words: int) -> dict:
    rows = []
    for excerpt in excerpts:
        rows.append(
            {
                "id": excerpt["id"],
                "label": excerpt["label"],
                "vintage": excerpt["vintage"],
                "path": excerpt["path"],
                "heading": excerpt["heading"],
                "rev": excerpt["rev"] if excerpt["vintage"] == "old" else "WORKTREE",
                "words": len(word_tokens(excerpt_body(excerpt))),
                "reason": excerpt.get("reason") or "",
            }
        )
    return {
        "month": month,
        "seed": seed,
        "target_words": TARGET_WORDS,
        "words": words,
        "material_words": MATERIAL_WORDS,
        "excerpts": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--month", required=True, help="YYYY-MM")
    parser.add_argument("--tops", required=True, type=Path, help="JSON {picks:[{path,heading,reason}]}")
    parser.add_argument("--force", action="store_true")
    parser.add_argument(
        "--shuffle-seed",
        default=None,
        help="Seed for excerpt order (default: random hex stored in the key file)",
    )
    args = parser.parse_args()
    if not re.fullmatch(r"\d{4}-\d{2}", args.month):
        raise SystemExit("--month must be YYYY-MM")
    tops = json.loads(args.tops.read_text(encoding="utf-8"))
    picks = tops["picks"] if isinstance(tops, dict) else tops
    if len(picks) < MIN_TOP:
        raise SystemExit(f"need at least {MIN_TOP} picks")
    for pick in picks:
        if not (ROOT / pick["path"]).is_file():
            raise SystemExit(f"missing pick: {pick['path']}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    md_path = OUT_DIR / f"{args.month}.md"
    key_path = OUT_DIR / f"{args.month}.key.json"
    if (md_path.exists() or key_path.exists()) and not args.force:
        raise SystemExit(f"{md_path} exists; pass --force to replace")

    pool_rng = random.Random(args.month)
    shuffle_seed = args.shuffle_seed or secrets.token_hex(16)
    order_rng = random.Random(shuffle_seed)
    top = select_top(picks, WINDOW_WORDS)
    rest = select_rest(top, pool_rng, WINDOW_WORDS)
    excerpts = top + rest
    order_rng.shuffle(excerpts)
    for i, excerpt in enumerate(excerpts, start=1):
        excerpt["id"] = f"E{i}"

    text, words = render(args.month, excerpts)
    if not (TARGET_WORDS - WORD_BAND <= words <= TARGET_WORDS + WORD_BAND):
        print(f"[warn] word count {words} outside {TARGET_WORDS}±{WORD_BAND}", flush=True)
    md_path.write_text(text, encoding="utf-8")
    key_path.write_text(
        json.dumps(key_payload(args.month, shuffle_seed, excerpts, words), indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"shuffle_seed {shuffle_seed}", flush=True)
    labels = {label: sum(1 for e in excerpts if e["label"] == label) for label in LABELS}
    print(
        f"wrote {md_path.relative_to(ROOT)} ({words} words, "
        + ", ".join(f"{k}={v}" for k, v in labels.items() if v)
        + ")"
    )


if __name__ == "__main__":
    main()
