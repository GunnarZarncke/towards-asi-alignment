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
        ("ch05-assumptions-scope-failure-coverage", "Assumptions, Scope, and Failure Coverage", "assumptions-scope-failure-coverage"),
    ]),
    ("part02-agents-boundaries", "Agents, Boundaries, and Real Optimizers", [
        ("ch06-agent-without-anthropomorphism", "What Is an Agent Without Anthropomorphism?", "agent-without-anthropomorphism"),
        ("ch07-finding-boundary", "Finding the Boundary", "finding-boundary"),
        ("ch08-grow-split-merge", "Agents That Grow, Split, and Merge", "grow-split-merge"),
        ("ch09-composite-agent", "The Real Agent May Be Composite", "composite-agent"),
        ("ch10-strategic-opacity", "Agency Under Strategic Opacity", "strategic-opacity"),
    ]),
    ("part03-capability-growth", "Capability Growth and Competence", [
        ("ch11-capability-without-task-ontology", "Measuring Capability Without Task Ontology", "capability-without-task-ontology"),
        ("ch12-boundary-expansion", "Capability Growth Is Boundary Expansion", "boundary-expansion"),
        ("ch13-coordination-bottleneck", "The Coordination Bottleneck", "coordination-bottleneck"),
        ("ch14-intelligence-deepens-misalignment", "When Intelligence Deepens Misalignment", "intelligence-deepens-misalignment"),
    ]),
    ("part04-value-bundles", "Human Values as Bundle Geometry", [
        ("ch15-values-compressed-control", "Values Are Compressed Control Signals", "values-compressed-control"),
        ("ch16-value-bundle-model", "The Value-Bundle Model", "value-bundle-model"),
        ("ch17-low-dimensional-value-learning", "Why Low Dimensionality Makes Value Learning Possible", "low-dimensional-value-learning"),
        ("ch18-bearer-maps", "Bearers: What Values Apply To", "bearer-maps"),
        ("ch19-tradeoffs-bundle-geometry", "Tradeoffs and Bundle Geometry", "tradeoffs-bundle-geometry"),
        ("ch20-measuring-stress-testing-bundle-geometry", "Measuring and Stress-Testing Bundle Geometry", "measuring-stress-testing-bundle-geometry"),
    ]),
        ("part05-goal-inference", "Goal Inference", [
        ("ch21-reward-to-bundle-inference", "From Reward Inference to Bundle Inference", "reward-to-bundle-inference"),
        ("ch22-compression-test-intention", "The Compression Test for Intention", "compression-test-intention"),
        ("ch23-goal-transport", "Inferring Goal Transport", "goal-transport"),
        ("ch24-transport-types", "Semantic, Bundle, Bearer, and Correction Transport", "transport-types"),
    ]),
        ("part06-correction-channels", "Correction Channels", [
        ("ch25-correction-causal-channel", "Correction Is a Causal Channel", "correction-causal-channel"),
        ("ch26-correction-channel-integrity", "Correction-Channel Integrity", "correction-channel-integrity"),
        ("ch27-correction-channels-adversarial-pressure", "Correction Channels under Adversarial Pressure", "correction-channels-adversarial-pressure"),
        ("ch28-extrapolative-correction", "From Obedience to Extrapolative Correction", "extrapolative-correction"),
        ("ch29-manipulation-false-consent", "Manipulation, Domestication, and False Consent", "manipulation-false-consent"),
    ]),
        ("part07-successors", "Successors, Reproduction, and Continuity", [
        ("ch30-successor-central-test", "Successor Creation as the Central Alignment Test", "successor-central-test"),
        ("ch31-conserved-properties", "Conserved Properties Across Successors", "conserved-properties"),
        ("ch32-self-modeling-self-opacity", "Better Self-Modeling Can Be Worse", "self-modeling-self-opacity"),
        ("ch33-certification-without-construction", "Certification Without Construction", "certification-without-construction"),
    ]),
        ("part08-attractor-basins", "Attractor Basins and Socio-Technical Selection", [
        ("ch34-selection-environment", "Alignment Is Selected or Destroyed by Its Environment", "selection-environment"),
        ("ch35-multi-agent-strategic-coupling", "Multi-Agent Superintelligence and Inferential Coupling", "multi-agent-strategic-coupling"),
        ("ch36-parasites-correction-system", "Parasites in the Correction System", "parasites-correction-system"),
        ("ch37-alignment-attractor", "The Alignment Attractor", "alignment-attractor"),
        ("ch38-conductive-artifacts-pivotal-processes", "Conductive Artifacts and Pivotal Processes", "conductive-artifacts-pivotal-processes"),
    ]),
        ("part09-safety-cases", "Safety Cases, Adversaries, and Open Cruxes", [
        ("ch39-passive-observation-not-enough", "Passive Observation Is Not Enough", "passive-observation-not-enough"),
        ("ch40-goal-laundering", "Detecting Goal Laundering", "goal-laundering"),
        ("ch41-multiscale-decomposition", "Multi-Scale Decomposition", "multiscale-decomposition"),
        ("ch42-safety-case", "A Safety Case for Superintelligence Alignment", "safety-case"),
        ("ch43-verifiability-and-ontology-adequacy", "What Survives an Adversary", "verifiability-and-ontology-adequacy"),
        ("ch44-lethality-stress-test-open-issues", "Lethality Stress Test and Open Issues", "lethality-stress-test-open-issues"),
    ]),
        ("part10-civilizational-limit", "The Philosophical and Civilizational Limit", [
        ("ch45-value-change-at-stake", "When Value Change Is the Thing at Stake", "value-change-at-stake"),
        ("ch46-unconscious-value-drift", "The End of Unconscious Value Drift", "unconscious-value-drift"),
        ("ch47-bearers-of-value", "The Bearers of Value", "bearers-of-value"),
        ("ch48-towards-alignment", "Towards Superintelligence Alignment", "towards-alignment"),
    ]),
]

APPENDICES = [
    ("appA-notation", "Notation Reference"),
    ("appB-bridge-crosswalk", "Bridges and the Field: A Crosswalk"),
    ("appC-institutional-translation", "Institutional Translation Guide"),
    ("appD-worked-example", "Worked Example: BioShield"),
    ("appE-glossary", "Glossary"),
    ("appF-research-program", "Research Program"),
    ("appG-lean-proof-spine", "Lean Proof Spine"),
    ("appH-boundary-worked-example", "Worked Example: Agent Boundary"),
    ("appI-value-bundle-inference", "Value-Bundle Inference"),
    ("appJ-correction-channel-audit", "Correction-Channel Audit"),
    ("appK-safety-case-template", "Safety-Case Template"),
    ("appL-assumptions", "Assumptions Index"),
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
