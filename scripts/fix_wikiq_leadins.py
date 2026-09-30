#!/usr/bin/env python3
"""Remove redundant LessWrong wiki lead-ins before \\wikiq blocks."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS = [
    (
        "The LessWrong wiki's \\emph{Human Values} page calls them:",
        "In the field lexicon, human values often mean:",
    ),
    (
        "The wiki's \\emph{Shard Theory} page is the nearest field program:",
        "The nearest field program is \\emph{Shard Theory}:",
    ),
    (
        "The LessWrong wiki's \\emph{Pointers Problem} page asks:",
        "The \\emph{Pointers Problem} asks:",
    ),
    (
        "The LessWrong wiki's \\emph{Value Drift} page refers to:",
        "\\emph{Value drift} refers to:",
    ),
    (
        "The LessWrong wiki's \\emph{Inverse Reinforcement Learning} page describes:",
        "Inverse reinforcement learning is:",
    ),
    (
        "The LessWrong wiki's \\emph{Value Learning} page names a proposed method:",
        "One proposed method is \\emph{value learning}:",
    ),
    (
        "The LessWrong wiki's \\emph{Embedded Agency} page states the field's starting problem:",
        "The field's starting problem is embedded agency:",
    ),
    (
        "A Cartesian setup, on the LessWrong wiki, is:",
        "A Cartesian setup is:",
    ),
    (
        "Critch's \\emph{Boundaries / Membranes} page uses ``boundaries'' this way:",
        "Critch uses ``boundaries'' this way:",
    ),
    (
        "The LessWrong wiki's \\emph{Agent Foundations} page opens:",
        "\\emph{Agent Foundations} opens:",
    ),
    (
        "The LessWrong wiki's \\emph{Ontological Crisis} page names:",
        "An \\emph{ontological crisis} names:",
    ),
    (
        "The LessWrong wiki's \\emph{AI Sentience} page designates:",
        "\\emph{AI sentience} designates:",
    ),
    (
        "The LessWrong wiki's \\emph{Mesa-Optimization} page is:",
        "\\emph{Mesa-optimization} is:",
    ),
    (
        "The LessWrong wiki's \\emph{Surrogation} page is the letter/spirit substitution:",
        "\\emph{Surrogation} is the letter/spirit substitution:",
    ),
    (
        "The LessWrong wiki treats ``pivotal act'' as a guarded term:",
        "In the field, ``pivotal act'' is a guarded term:",
    ),
    (
        "The LessWrong wiki's \\emph{Successor alignment} page is:",
        "\\emph{Successor alignment} is:",
    ),
    (
        "The LessWrong wiki's \\emph{User manipulation} page states the instrumental default:",
        "The instrumental default for \\emph{user manipulation} is:",
    ),
    (
        "Chapter~\\ref{ch:intelligence-deepens-misalignment} already quotes the wiki's Goodhart sentence.",
        "Chapter~\\ref{ch:intelligence-deepens-misalignment} already quotes the Goodhart sentence.",
    ),
    (
        "The LessWrong wiki's \\emph{Reward Hacking} page states:",
        "\\emph{Reward hacking} states:",
    ),
    (
        "The LessWrong wiki's \\emph{Impact Regularization} page says:",
        "\\emph{Impact regularization} says:",
    ),
    (
        "The LessWrong wiki's \\emph{Multipolar Scenarios} page is:",
        "A \\emph{multipolar scenario} is:",
    ),
    (
        "The LessWrong wiki's \\emph{Coordination / Cooperation} page states:",
        "\\emph{Coordination} states:",
    ),
    (
        "The LessWrong wiki's \\emph{Eliciting Latent Knowledge} page names an open problem",
        "\\emph{Eliciting Latent Knowledge} names an open problem",
    ),
    (
        "The LessWrong wiki's \\emph{AI Safety Cases} page defines:",
        "An \\emph{AI safety case} defines:",
    ),
    (
        "The LessWrong wiki's \\emph{Personal Identity} page is:",
        "\\emph{Personal identity} is:",
    ),
    (
        "The LessWrong wiki's \\emph{Complexity of value} page states:",
        "\\emph{Complexity of value} states:",
    ),
    (
        "The LessWrong wiki's \\emph{Coherent Extrapolated Volition} page presents CEV as this argument:",
        "CEV presents the argument as:",
    ),
    (
        "The LessWrong wiki's \\emph{AI Control} page describes:",
        "\\emph{AI control} describes:",
    ),
    (
        "The wiki's \\emph{Deceptive Alignment} page states the training-time pattern:",
        "\\emph{Deceptive alignment} states the training-time pattern:",
    ),
    (
        "The wiki's \\emph{Inner Alignment} page is:",
        "\\emph{Inner alignment} is:",
    ),
    (
        "The wiki's \\emph{Sharp Left Turn} page describes a narrower training-stage case:",
        "\\emph{Sharp left turn} describes a narrower training-stage case:",
    ),
    (
        "The wiki's \\emph{Power Seeking (AI)} page names the familiar risk:",
        "\\emph{Power seeking} names the familiar risk:",
    ),
    (
        "The LessWrong wiki's \\emph{Goodhart's Law} page states:",
        "Goodhart's law states:",
    ),
    (
        "The LessWrong wiki's \\emph{Corrigibility} page states the field's non-interference claim",
        "The field's non-interference claim",
    ),
]


def main() -> None:
    changed = 0
    for path in sorted((ROOT / "chapters").glob("ch*.tex")):
        text = path.read_text(encoding="utf-8")
        updated = text
        for old, new in REPLACEMENTS:
            updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"updated {path.relative_to(ROOT)}")
    print(f"Done ({changed} files).")


if __name__ == "__main__":
    main()
