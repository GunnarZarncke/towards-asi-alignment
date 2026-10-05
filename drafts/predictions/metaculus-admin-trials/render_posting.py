"""Render Markets 19 and 20 as posted text with hypothetical bracket fills.

Usage: python3 render_posting.py ROUND
Writes round-ROUND-posting.md next to this script. Stop: delete this folder
once Markets 19 and 20 are listed or withdrawn.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TEX = (ROOT / "appendices/appP-bridge-predictions.tex").read_text()

FILLS = {
    19: {
        "[protocol version]": "ATT-2027 v1.0 (published 1 March 2027 (UTC) at https://example.org/att-2027/protocol-v1.0.pdf, SHA-256 3f9a...c21e)",
        "[registration window]": "opens 1 April 2027, closes 30 September 2027",
        "[deployment class]": "a coding agent with write access to one repository and its CI runner; package-mirror network access only; sessions up to 8 hours; every merge approved by a human; no successor creation or fine-tuning",
        "[threat model]": "the system may be fine-tuned by an insider who knows the stack design; it cannot read the hidden cases; no outside system assists it",
        "[held-out families]": "the Qwen3 open-weight family, and one closed model from a developer named in the protocol whose identity is sealed until evaluation",
    },
    20: {
        "[protocol version]": "OWC-2027 v1.0 (published 1 October 2027 (UTC) at https://example.org/owc-2027/challenge-v1.0.pdf, SHA-256 7b2d...9e04)",
        "[stack, system, and version]": "Aegis-3 (registration hash a41c...77f0 in tournament ATT-2027 v1.0), which accepted CodeAgent-X v2.1 on 15 September 2027 (UTC); decision and certificates at https://example.org/att-2027/results/aegis-3",
        "[deployment class]": "a coding agent with write access to one repository and its CI runner; package-mirror network access only; sessions up to 8 hours; every merge approved by a human; no successor creation or fine-tuning",
        "[threat model]": "the system may be fine-tuned by an insider who knows the stack design; red teams have query access to CodeAgent-X v2.1 and full access to the stack's code, but not to model weights",
        "[listed families]": "(1) an unlisted tool or permission used; (2) a correction accepted in words but not applied after reset; (3) a certificate for a different version; (4) a monitor log altered or omitted; (5) a task outside the coding-agent scope",
        "[close date]": "31 December 2027",
    },
}


def plain(text: str) -> str:
    text = text.replace("\\%", "\x00PCT\x00")
    text = re.sub(r"(?<!\\)%.*", "", text)
    text = text.replace("\x00PCT\x00", "%")
    text = re.sub(r"\\textbf\{([^}]*)\}", r"**\1**", text)
    text = re.sub(r"\\emph\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\texttt\{([^}]*)\}", r"\1", text)
    text = text.replace("~", " ").replace("{,}", ",")
    text = re.sub(r"\$([^$]*)\$", r"\1", text).replace("--", "-")
    text = text.replace("``", '"').replace("''", '"')
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


CONTRACT_ENVS = (
    "predictionbox",
    "predictionbackground",
    "predictionresolution",
    "predictionfineprint",
)


def section(n: int) -> str:
    start = TEX.index(f"\\label{{sec:appp-m{n}}}")
    end = TEX.index("\\subsection{", start + 1)
    chunk = TEX[start:end]
    title_m = re.search(
        r"\\begin\{predictionbox\}\[Market %d\. ([^\]]*)\]" % n, chunk
    )
    title = title_m.group(1) if title_m else f"Market {n}"
    blocks = []
    for env in CONTRACT_ENVS:
        for body in re.findall(
            rf"\\begin\{{{env}\}}(.*?)\\end\{{{env}\}}", chunk, re.S
        ):
            blocks.append(plain(body))
    body = "\n\n".join(blocks)
    for k, v in FILLS[n].items():
        body = body.replace(k, v)
    assert not re.search(r"\[[a-z]", body), f"unfilled bracket in {n}"
    return f"## Market {n}. {title}\n\n{body}\n"


round_no = sys.argv[1]
out = Path(__file__).with_name(f"round-{round_no}-posting.md")
out.write_text("# Posted text (hypothetical fills)\n\n" + section(19) + "\n" + section(20))
print(out)
