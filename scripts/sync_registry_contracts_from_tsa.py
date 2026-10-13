#!/usr/bin/env python3
"""Bump ai-safety-claims contract versions: question + background from TSA; bars unchanged."""
from __future__ import annotations

import re
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO.parent / "ai-safety-claims"
TEX = REPO / "appendices" / "appP-bridge-predictions.tex"
META = REPO / "metadata" / "predictions.yml"

SKIP = {1, 4, 14, 19, 20, 21}

QUESTION_SUFFIX = (
    ": YES (at least one qualifying attempt met the frozen performance bars), "
    "NO (every qualifying attempt missed those bars), "
    "or OTHER (no qualifying attempt existed)?"
)


def git_head() -> str:
    out = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"], cwd=REPO, text=True
    )
    return out.strip()


def strip_comments(tex: str) -> str:
    return re.sub(r"(?m)^%.*$", "", tex)


def extract_predictionbackground(tex: str, num: int) -> str:
    label = f"\\label{{sec:appp-m{num}}}"
    i = tex.find(label)
    if i < 0:
        raise ValueError(f"Market {num}: label not found")
    chunk = tex[i : i + 8000]
    m = re.search(
        r"\\begin\{predictionbackground\}(.*?)\\end\{predictionbackground\}",
        chunk,
        re.DOTALL,
    )
    if not m:
        raise ValueError(f"Market {num}: predictionbackground not found")
    return m.group(1).strip()


def background_to_plain(latex: str) -> str:
    s = latex
    s = re.sub(
        r"\n?\s*See also \\href\{[^}]+\}\{[^}]+\}\.\s*",
        "\n",
        s,
        flags=re.MULTILINE,
    )
    s = s.replace("``", '"').replace("''", '"')
    s = re.sub(r"\\emph\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\textbf\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\textit\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\autocite\{[^}]+\}", "", s)
    s = re.sub(r"\\textcite\{[^}]+\}", "", s)
    s = re.sub(r"---", "—", s)
    s = s.replace("~", " ")
    s = re.sub(r"\\,", " ", s)
    s = re.sub(r"\\%", "%", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def registry_question(long_title: str) -> str:
    t = long_title.strip()
    if t.endswith("?"):
        t = t[:-1].rstrip()
    return t + QUESTION_SUFFIX


def load_contract(market_id: str, version: int) -> tuple[Path, dict]:
    path = REGISTRY / "market-contracts" / market_id / f"contract-v{version}.yaml"
    if not path.exists():
        raise FileNotFoundError(path)
    return path, yaml.safe_load(path.read_text(encoding="utf-8"))


def dump_contract(path: Path, contract: dict, header_lines: list[str]) -> None:
    body = yaml.safe_dump(
        contract,
        sort_keys=False,
        allow_unicode=True,
        width=1000,
        default_style=None,
    )
    # Quote YES/NO in outcomes if needed
    body = body.replace("- YES\n", "- 'YES'\n").replace("- NO\n", "- 'NO'\n")
    text = "\n".join(header_lines) + "\n" + body
    path.write_text(text, encoding="utf-8")


def main() -> int:
    if not REGISTRY.is_dir():
        print(f"Registry not found: {REGISTRY}", file=sys.stderr)
        return 1

    head = git_head()
    tex = strip_comments(TEX.read_text(encoding="utf-8"))
    meta = yaml.safe_load(META.read_text(encoding="utf-8"))
    updates: list[tuple[int, str, int, int]] = []

    for m in meta["markets"]:
        num = m["number"]
        if num in SKIP:
            continue
        mid = m["id"]
        old_v = int(m["contractVersion"])
        new_v = old_v + 1

        _, contract = load_contract(mid, old_v)
        bg_latex = extract_predictionbackground(tex, num)
        bg_plain = background_to_plain(bg_latex)
        q = registry_question(m["longTitle"])

        new_contract = deepcopy(contract)
        new_contract["version"] = new_v
        new_contract["status"] = "frozen"
        new_contract["title"] = m["title"]
        new_contract["question"] = q
        new_contract["background"] = bg_plain

        out_path = REGISTRY / "market-contracts" / mid / f"contract-v{new_v}.yaml"
        header = [
            f"# Market {num}, contract version {new_v}. Listing text synced from TSA Appendix H at HEAD {head}.",
            f"# yesRequires, bars, and machine checks copied from contract-v{old_v} unchanged.",
            "# status: frozen as a contract version. Not a resolution source until an independent host tags snapshot-0.",
        ]
        dump_contract(out_path, new_contract, header)
        old_path = REGISTRY / "market-contracts" / mid / f"contract-v{old_v}.yaml"
        if old_path.exists() and old_path != out_path:
            old_path.unlink()

        cols_path = REGISTRY / "market-contracts" / mid / "required-columns.yaml"
        cols = yaml.safe_load(cols_path.read_text(encoding="utf-8"))
        cols["contractVersion"] = new_v
        cols_path.write_text(
            yaml.safe_dump(cols, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )

        updates.append((num, mid, old_v, new_v))
        print(f"market-{num:02d}: v{old_v} -> v{new_v} ({out_path.name})")

    # Write machine-readable manifest for TSA follow-up
    manifest = REPO / "drafts" / "predictions" / ".registry-sync-manifest.yaml"
    manifest.write_text(
        yaml.safe_dump({"head": head, "updates": updates}, sort_keys=False),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
