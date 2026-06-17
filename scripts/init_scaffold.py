#!/usr/bin/env python3
"""Generate the LaTeX book scaffold (first milestone)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PARTS = [
    ("part01-reframing", "The Alignment Problem Reframed", [
        ("ch01-wrong-object", "The Wrong Object of Alignment", "wrong-object"),
        ("ch02-artificial-civilization", "From Artificial Intelligence to Artificial Civilization", "artificial-civilization"),
        ("ch03-dynamical-guarantee", "Alignment as a Dynamical Guarantee", "dynamical-guarantee"),
        ("ch04-fixed-values-wrong-target", "Why Fixed Values Are the Wrong Target", "fixed-values-wrong-target"),
    ]),
    ("part02-agents-boundaries", "Agents, Boundaries, and Real Optimizers", [
        ("ch05-agent-without-anthropomorphism", "What Is an Agent Without Anthropomorphism?", "agent-without-anthropomorphism"),
        ("ch06-finding-boundary", "Finding the Boundary", "finding-boundary"),
        ("ch07-grow-split-merge", "Agents That Grow, Split, and Merge", "grow-split-merge"),
        ("ch08-composite-agent", "The Real Agent May Be Composite", "composite-agent"),
        ("ch09-strategic-opacity", "Agency Under Strategic Opacity", "strategic-opacity"),
    ]),
    ("part03-capability-growth", "Capability Growth and Competence", [
        ("ch10-capability-without-task-ontology", "Measuring Capability Without Task Ontology", "capability-without-task-ontology"),
        ("ch11-boundary-expansion", "Capability Growth Is Boundary Expansion", "boundary-expansion"),
        ("ch12-coordination-bottleneck", "The Coordination Bottleneck", "coordination-bottleneck"),
        ("ch13-intelligence-deepens-misalignment", "When Intelligence Deepens Misalignment", "intelligence-deepens-misalignment"),
    ]),
    ("part04-value-bundles", "Human Values as Bundle Geometry", [
        ("ch14-values-compressed-control", "Values Are Compressed Control Signals", "values-compressed-control"),
        ("ch15-value-bundle-model", "The Value-Bundle Model", "value-bundle-model"),
        ("ch16-low-dimensional-value-learning", "Why Low Dimensionality Makes Value Learning Possible", "low-dimensional-value-learning"),
        ("ch17-bearer-maps", "Bearers: What Values Apply To", "bearer-maps"),
        ("ch18-tradeoffs-bundle-geometry", "Tradeoffs and Bundle Geometry", "tradeoffs-bundle-geometry"),
    ]),
    ("part05-goal-inference", "Goal Inference", [
        ("ch19-reward-to-bundle-inference", "From Reward Inference to Bundle Inference", "reward-to-bundle-inference"),
        ("ch20-compression-test-intention", "The Compression Test for Intention", "compression-test-intention"),
        ("ch21-goal-transport", "Inferring Goal Transport", "goal-transport"),
        ("ch22-transport-types", "Semantic, Bundle, Bearer, and Correction Transport", "transport-types"),
    ]),
    ("part06-correction-channels", "Correction Channels", [
        ("ch23-correction-causal-channel", "Correction Is a Causal Channel", "correction-causal-channel"),
        ("ch24-correction-channel-integrity", "Correction-Channel Integrity", "correction-channel-integrity"),
        ("ch25-extrapolative-correction", "From Obedience to Extrapolative Correction", "extrapolative-correction"),
        ("ch26-manipulation-false-consent", "Manipulation, Domestication, and False Consent", "manipulation-false-consent"),
    ]),
    ("part07-successors", "Successors, Reproduction, and Continuity", [
        ("ch27-successor-central-test", "Successor Creation as the Central Alignment Test", "successor-central-test"),
        ("ch28-conserved-properties", "Conserved Properties Across Successors", "conserved-properties"),
        ("ch29-self-modeling-self-opacity", "Better Self-Modeling Can Be Worse", "self-modeling-self-opacity"),
        ("ch30-certification-without-construction", "Certification Without Construction", "certification-without-construction"),
    ]),
    ("part08-attractor-basins", "Attractor Basins and Socio-Technical Selection", [
        ("ch31-selection-environment", "Alignment Is Selected or Destroyed by Its Environment", "selection-environment"),
        ("ch32-cooperation-privacy-opacity", "Cooperation, Privacy, and Opacity", "cooperation-privacy-opacity"),
        ("ch33-cooperation-percolation", "Percolation of Cooperation", "cooperation-percolation"),
        ("ch34-parasites-correction-system", "Parasites in the Correction System", "parasites-correction-system"),
        ("ch35-alignment-attractor", "The Alignment Attractor", "alignment-attractor"),
    ]),
    ("part09-adversarial-measurement", "Adversarial Measurement and Practical Guarantees", [
        ("ch36-passive-observation-not-enough", "Passive Observation Is Not Enough", "passive-observation-not-enough"),
        ("ch37-goal-laundering", "Detecting Goal Laundering", "goal-laundering"),
        ("ch38-multiscale-decomposition", "Multi-Scale Decomposition", "multiscale-decomposition"),
        ("ch39-tripwires-stop-conditions", "Tripwires and Stop Conditions", "tripwires-stop-conditions"),
        ("ch40-safety-case", "A Safety Case for Superintelligence Alignment", "safety-case"),
    ]),
    ("part10-civilizational-limit", "The Philosophical and Civilizational Limit", [
        ("ch41-value-change-at-stake", "When Value Change Is the Thing at Stake", "value-change-at-stake"),
        ("ch42-merging-artificial-entities", "Merging With Artificial Entities", "merging-artificial-entities"),
        ("ch43-unconscious-value-drift", "The End of Unconscious Value Drift", "unconscious-value-drift"),
        ("ch44-cannot-be-solved-technically", "What Cannot Be Solved Technically", "cannot-be-solved-technically"),
        ("ch45-towards-alignments", "Towards Superintelligence Alignments", "towards-alignments"),
    ]),
]

APPENDICES = [
    ("appA-notation", "Notation Reference"),
    ("appB-worked-example-agent-boundary", "Worked Example: Agent Boundary"),
    ("appC-value-bundle-inference", "Value-Bundle Inference"),
    ("appD-correction-channel-audit", "Correction-Channel Audit"),
    ("appE-successor-certification", "Successor Certification"),
    ("appF-glossary", "Glossary"),
    ("appG-safety-case-template", "Safety-Case Template"),
    ("appH-research-program", "Research Program"),
]


def chapter_stub(filename: str, title: str, label: str) -> str:
    return f"""\\chapter{{{title}}}
\\label{{ch:{label}}}

\\begin{{chapterthesis}}
\\textbf{{[STUB]}} One paragraph stating the chapter's core claim.
\\end{{chapterthesis}}

\\section{{Why This Matters}}

\\textbf{{[STUB]}} Explain the decision relevance.

\\section{{Plain-Language Model}}

\\textbf{{[STUB]}} Explain the idea without equations.

\\section{{Formal Model}}

\\textbf{{[STUB]}} Introduce variables, assumptions, and equations.

\\section{{Worked Example}}

\\textbf{{[STUB]}} Give one concrete example.

\\section{{Counterexample or Failure Mode}}

\\textbf{{[STUB]}} Give at least one case where the model fails, overreaches, or needs refinement.

\\section{{What Would Change This View}}

\\textbf{{[STUB]}} List evidence, argument, or empirical results that would weaken the chapter.

\\section{{Summary}}

\\begin{{itemize}}
  \\item \\textbf{{[STUB]}} Summary point 1.
  \\item \\textbf{{[STUB]}} Summary point 2.
  \\item \\textbf{{[STUB]}} Summary point 3.
\\end{{itemize}}

\\section*{{Chapter References}}

% Use BibLaTeX citations throughout. Do not manually format references.
"""


def appendix_stub(filename: str, title: str) -> str:
    label = filename.replace("app", "app").lower()
    return f"""\\chapter{{{title}}}
\\label{{{label}}}

\\textbf{{[STUB]}} Appendix content to be written.
"""


def part_file(part_name: str, part_title: str, chapters: list) -> str:
    lines = [f"\\part{{{part_title}}}", ""]
    for ch_file, _, _ in chapters:
        lines.append(f"\\input{{chapters/{ch_file}}}")
    lines.append("")
    return "\n".join(lines)


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def main() -> None:
    dirs = [
        "metadata", "frontmatter", "parts", "chapters", "appendices",
        "figures/source", "figures/generated", "figures/tikz",
        "tables", "references", "drafts/chapter-notes",
        "drafts/rejected-fragments", "drafts/conversation-summaries",
        "review", "dist/pdf", "dist/epub", "dist/html",
    ]
    for d in dirs:
        (ROOT / d).mkdir(parents=True, exist_ok=True)

    for part_name, part_title, chapters in PARTS:
        write_if_missing(
            ROOT / "parts" / f"{part_name}.tex",
            part_file(part_name, part_title, chapters),
        )
        for ch_file, ch_title, ch_label in chapters:
            write_if_missing(
                ROOT / "chapters" / f"{ch_file}.tex",
                chapter_stub(ch_file, ch_title, ch_label),
            )

    for app_file, app_title in APPENDICES:
        write_if_missing(
            ROOT / "appendices" / f"{app_file}.tex",
            appendix_stub(app_file, app_title),
        )

    print(f"Scaffold written under {ROOT}")


if __name__ == "__main__":
    main()
