#!/usr/bin/env python3
"""Renumber context/lw-references.md to match metadata/book.yml chapter numbers."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / "context" / "lw-references.md"

TITLE_MAP = {
    1: "The Wrong Object of Alignment",
    2: "From Artificial Intelligence to Artificial Civilization",
    3: "Alignment as a Dynamical Guarantee",
    4: "Why Fixed Values Are the Wrong Target",
    5: "Assumptions, Scope, and Failure Coverage",
    6: "What Is an Agent Without Anthropomorphism?",
    7: "Finding the Boundary",
    8: "Agents That Grow, Split, and Merge",
    9: "The Real Agent May Be Composite",
    10: "Agency Under Strategic Opacity",
    11: "Measuring Capability Without Task Ontology",
    12: "Capability Growth Is Boundary Expansion",
    13: "The Coordination Bottleneck",
    14: "When Intelligence Deepens Misalignment",
    15: "Values Are Compressed Control Signals",
    16: "The Value-Bundle Model",
    17: "Why Low Dimensionality Makes Value Learning Possible",
    18: "Bearers: What Values Apply To",
    19: "Tradeoffs and Bundle Geometry",
    20: "From Reward Inference to Bundle Inference",
    21: "The Compression Test for Intention",
    22: "Inferring Goal Transport",
    23: "Semantic, Bundle, Bearer, and Correction Transport",
    24: "Correction Is a Causal Channel",
    25: "Correction-Channel Integrity",
    26: "From Obedience to Extrapolative Correction",
    27: "Manipulation, Domestication, and False Consent",
    28: "Successor Creation as the Central Alignment Test",
    29: "Conserved Properties Across Successors",
    30: "Better Self-Modeling Can Be Worse",
    31: "Certification Without Construction",
    32: "Alignment Is Selected or Destroyed by Its Environment",
    33: "Multi-Agent Superintelligence and Strategic Coupling",
    34: "Parasites in the Correction System",
    35: "The Alignment Attractor",
    36: "Passive Observation Is Not Enough",
    37: "Detecting Goal Laundering",
    38: "Multi-Scale Decomposition",
    39: "A Safety Case for Superintelligence Alignment",
    40: "Lethality Stress Test and Open Issues",
    41: "When Value Change Is the Thing at Stake",
    42: "The End of Unconscious Value Drift",
    43: "The Bearers of Value",
    44: "Towards Superintelligence Alignment",
}

OLD_TO_NEW = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 6,
    6: 7,
    7: 8,
    8: 9,
    9: 10,
    10: 11,
    11: 12,
    12: 13,
    13: 14,
    14: 15,
    15: 16,
    16: 17,
    17: 18,
    18: 19,
    19: 20,
    20: 21,
    21: 22,
    22: 23,
    23: 24,
    24: 25,
    25: 26,
    26: 27,
    27: 28,
    28: 29,
    29: 30,
    30: 31,
    31: 32,
    32: 33,
    33: 33,
    34: 34,
    35: 35,
    36: 36,
    37: 37,
    38: 38,
    39: None,
    40: 39,
    41: 41,
    42: 43,
    43: 42,
    44: 44,
    45: 44,
}

PARTS = [
    (1, "# Part I — The Alignment Problem Reframed"),
    (6, "# Part II — Agents, Boundaries, and Real Optimizers"),
    (11, "# Part III — Capability Growth and Competence"),
    (15, "# Part IV — Human Values as Bundle Geometry"),
    (20, "# Part V — Goal Inference Upgraded"),
    (24, "# Part VI — Correction Channels and CEV-Like Processes"),
    (28, "# Part VII — Successors, Reproduction, and Continuity"),
    (32, "# Part VIII — Attractor Basins and Socio-Technical Selection"),
    (36, "# Part IX — Adversarial Measurement and Practical Guarantees"),
    (40, "# Part X — The Philosophical and Civilizational Limit"),
]

MERGE_NOTES = {
    (33, 33): "*Former LW §33 (Percolation of Cooperation); merged here because the book combines cooperation/percolation under ch33.*",
    (43, 42): "*Former LW §42 (Merging With Artificial Entities); placed under ch43 because bearer/patienthood questions dominate.*",
    (44, 44): "*Former LW §44 (What Cannot Be Solved Technically); placed under ch44 as civilizational-limit material.*",
    (44, 45): "*Former LW §45 (Towards Superintelligence Alignments).*",
}

CH05_PLACEHOLDER = """## 5. Assumptions, Scope, and Failure Coverage

*No curated LW entries yet.* See cross-cutting posts (AGI Ruin, Christiano disagreement, Goodhart Taxonomy) and Part I--IV references for scope/failure-mode background.
"""

CH40_BODY = """## 40. Lethality Stress Test and Open Issues

* **Eliezer Yudkowsky, "AGI Ruin: A List of Lethalities," 5 Jun 2022**
  URL: [https://www.lesswrong.com/posts/uMQ3cqWDPHhjtiesc/agi-ruin-a-list-of-lethalities](https://www.lesswrong.com/posts/uMQ3cqWDPHhjtiesc/agi-ruin-a-list-of-lethalities)
  Summary: Canonical checklist of reasons alignment may fail under capability growth; cited throughout ch40. **[Y, K]** ([lesswrong.com][18])

* **Nate Soares, "On how various plans miss the hard bits of the alignment challenge," 11 Jul 2022**
  URL: [https://www.lesswrong.com/posts/3pinFH3jerMzAvmza/on-how-various-plans-miss-the-hard-bits-of-the-alignment](https://www.lesswrong.com/posts/3pinFH3jerMzAvmza/on-how-various-plans-miss-the-hard-bits-of-the-alignment)
  Summary: Field-failure row in ch40 lethality checklist. **[K, T]** ([lesswrong.com][36])

* **Paul Christiano, "Where I agree and disagree with Eliezer," 19 Jun 2022**
  URL: [https://www.lesswrong.com/posts/CoZhXrhpQxpy9xw9y/where-i-agree-and-disagree-with-eliezer](https://www.lesswrong.com/posts/CoZhXrhpQxpy9xw9y/where-i-agree-and-disagree-with-eliezer)
  Summary: Useful for separating answered vs reframed lethalities. **[K]** ([lesswrong.com][53])
"""

TRIPWIRE_ORPHAN = """
### Orphan reference: Tripwires and Stop Conditions (former LW §39)

No dedicated book chapter; closest fit is ch39 (safety case) and ch40 (lethality stress test).

* **Evan Hubinger, "RSPs are pauses done right," 13 Oct 2023**
  URL: [https://www.lesswrong.com/posts/mcnWZBnbeDz7KKtjJ/rsps-are-pauses-done-right](https://www.lesswrong.com/posts/mcnWZBnbeDz7KKtjJ/rsps-are-pauses-done-right)
  Summary: Trigger-based pauses before dangerous capability thresholds. **[K]** ([lesswrong.com][42])

* **Ryan Greenblatt et al., "The case for ensuring that powerful AIs are controlled," 24 Jan 2024**
  URL: [https://www.lesswrong.com/posts/kcKrE9mzEHrdqtDpE/the-case-for-ensuring-that-powerful-ais-are-controlled](https://www.lesswrong.com/posts/kcKrE9mzEHrdqtDpE/the-case-for-ensuring-that-powerful-ais-are-controlled)
  Summary: Red flags and control-evaluation concerns for powerful AI deployment. **[T]** ([lesswrong.com][43])
"""


def parse_sections(text: str) -> tuple[str, dict[int, list[tuple[int, str]]]]:
    """Return (suffix after last chapter section, old_num -> [(old_num, body)])."""
    split_at = text.find("\n## Cross-cutting posts")
    if split_at == -1:
        split_at = text.find("\n[1]:")
    main = text[:split_at]
    suffix = text[split_at:]

    blocks = re.split(r"(?m)^## (\d+)\. .+\n", main)
    # blocks[0] is intro; then alternating num, body, num, body...
    sections: dict[int, list[tuple[int, str]]] = {}
    i = 1
    while i + 1 < len(blocks):
        old_num = int(blocks[i])
        body = blocks[i + 1]
        body = re.sub(r"\n---\n\n# Part[^\n]+\n+", "\n", body)
        body = body.strip()
        new_num = OLD_TO_NEW.get(old_num)
        if new_num is None:
            i += 2
            continue
        sections.setdefault(new_num, []).append((old_num, body))
        i += 2
    return suffix, sections


def update_cross_cutting(suffix: str) -> str:
    replacements = {
        "Use in: chapters 2, 3, 11, 13, 27, 39, 40.": "Use in: chapters 2, 3, 12, 14, 28, 39, 40.",
        "Use in: chapters 3, 13, 24, 30, 40, 45.": "Use in: chapters 3, 14, 25, 31, 40, 44.",
        "Use in: chapters 11, 13, 21, 27.": "Use in: chapters 12, 14, 22, 28.",
        "Use in: chapters 14, 17, 19, 21, 22.": "Use in: chapters 15, 18, 20, 22, 23.",
        "Use in: chapters 18, 26, 31, 34, 39.": "Use in: chapters 19, 27, 32, 35, 39.",
    }
    for old, new in replacements.items():
        suffix = suffix.replace(old, new)
    return suffix


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    suffix, sections = parse_sections(text)
    suffix = update_cross_cutting(suffix)

    intro = (
        "Commented LW references relevant for each chapter.\n\n"
        "Chapter numbers follow `metadata/book.yml` (including ch05 and ch40).\n"
        "BibTeX keys for cited posts live in `references/external-alignment.bib`.\n"
    )

    out: list[str] = [intro, ""]
    part_idx = 0

    for ch in range(1, 45):
        while part_idx < len(PARTS) and PARTS[part_idx][0] == ch:
            if out[-1].strip():
                out.append("")
            out.append("---")
            out.append("")
            out.append(PARTS[part_idx][1])
            out.append("")
            part_idx += 1

        if ch == 5:
            out.append(CH05_PLACEHOLDER.strip())
            out.append("")
            continue

        if ch == 40:
            out.append(CH40_BODY.strip())
            out.append("")
            continue

        title = TITLE_MAP[ch]
        out.append(f"## {ch}. {title}")
        out.append("")

        if ch not in sections:
            out.append("*No curated LW entries yet.*")
            out.append("")
            continue

        for old_num, body in sections[ch]:
            note = MERGE_NOTES.get((ch, old_num))
            if note:
                out.append(note)
                out.append("")
            out.append(body.strip())
            out.append("")

        if ch == 39:
            out.append(TRIPWIRE_ORPHAN.strip())
            out.append("")

    out.append("---")
    out.append("")
    out.append(suffix.lstrip())

    PATH.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {PATH}")


if __name__ == "__main__":
    main()
