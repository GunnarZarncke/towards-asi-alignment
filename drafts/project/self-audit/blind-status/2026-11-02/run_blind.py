#!/usr/bin/env python3
"""§3.6 blind status reads. Packets contain stripped chapter text only."""

from __future__ import annotations

import asyncio
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "scripts" / "sandboxed-agent-mcp"))

from sandboxed_agent_mcp.auth_info import auth_summary  # noqa: E402
from sandboxed_agent_mcp.sandbox import run_sandboxed  # noqa: E402

HERE = Path(__file__).resolve().parent
PACKETS = HERE / "packets"
RESULTS = HERE / "results"

CHAPTERS = [
    ("ch42", "chapters/ch42-safety-case.tex"),
    ("ch01", "chapters/ch01-wrong-object.tex"),
    ("ch07", "chapters/ch07-finding-boundary.tex"),
    ("ch15", "chapters/ch15-values-compressed-control.tex"),
    ("ch25", "chapters/ch25-correction-causal-channel.tex"),
]

MODEL = "claude-sonnet-5-5"
EFFORT = "medium"

SYSTEM = """\
You are a reader of one chapter of a technical book. The only files you may use are in the current directory. You have no access to the rest of the repository, to version history, or to any editorial label. Do not try to leave this directory. Do not edit the file. Read it, then answer.
"""

PROMPT = """\
Read chapter.tex. Judge the chapter as it stands on the page.

Reply in plain text with exactly these three parts:

MATURITY: one of sketch, draft, working, stable
- sketch: the argument is not yet something a reader could check
- draft: the argument is assembled, and major claims run ahead of the support written on the page
- working: the main claims are stated together with their support and their limits
- stable: a careful reader could rely on the claims as stated, with only local gaps

WHY: one short paragraph. Say what is supported on the page and what is not. Do not guess at a hidden editorial label.

WEAKEST:
1. A short quote of the claim, the section heading it sits under, and one sentence on why it is weak.
2. Same.
3. Same.

Use only the file in this directory.
"""

BOX = re.compile(
    r"\\begin\{epistemicstatus\}.*?\\end\{epistemicstatus\}\s*",
    re.DOTALL,
)


def export() -> None:
    PACKETS.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    (HERE / "prompt.txt").write_text(SYSTEM + "\n---\n" + PROMPT, encoding="utf-8")
    for key, rel in CHAPTERS:
        src = (ROOT / rel).read_text(encoding="utf-8")
        n = len(BOX.findall(src))
        stripped = BOX.sub("", src)
        left = stripped.count("epistemicstatus")
        dest = PACKETS / key
        dest.mkdir(parents=True, exist_ok=True)
        out = dest / "chapter.tex"
        out.write_text(stripped, encoding="utf-8")
        print(
            f"export {key}: removed_boxes={n} leftover_mentions={left} bytes={out.stat().st_size}",
            flush=True,
        )


async def one(i: int, n: int, key: str) -> None:
    root = PACKETS / key
    print(f"[{i}/{n}] start {key}", flush=True)
    try:
        text = await run_sandboxed(
            prompt=PROMPT,
            root=str(root),
            system_prompt=SYSTEM,
            allow_write=False,
            max_turns=16,
            model=MODEL,
            effort=EFFORT,
        )
    except Exception as exc:
        text = f"ERROR: {type(exc).__name__}: {exc}"
        print(f"[{i}/{n}] fail {key}: {text}", flush=True)
    else:
        print(f"[{i}/{n}] done {key} chars={len(text)}", flush=True)
    (RESULTS / f"{key}.txt").write_text(text, encoding="utf-8")


async def main() -> int:
    print("auth:", json.dumps(auth_summary()), flush=True)
    print(f"model={MODEL} effort={EFFORT} allow_write=false", flush=True)
    export()
    n = len(CHAPTERS)
    await asyncio.gather(*(one(i, n, key) for i, (key, _) in enumerate(CHAPTERS, 1)))
    print("all finished", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
