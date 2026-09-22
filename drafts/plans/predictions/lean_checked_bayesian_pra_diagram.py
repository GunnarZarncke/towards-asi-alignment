#!/usr/bin/env python3
"""
Generate a "Lean-checked Bayesian PRA" diagram for a frontier-AI deployment.

Requires:
    pip install graphviz
and the Graphviz system package ("dot") to be installed.

Examples:
    python lean_checked_bayesian_pra_diagram.py
    python lean_checked_bayesian_pra_diagram.py --format svg
    python lean_checked_bayesian_pra_diagram.py --format pdf --output tsa_pra

The diagram intentionally distinguishes:
  * the scenario/event path from deployment attempt to catastrophe;
  * the assurance submodel for represented hazards;
  * Lean/formal dependencies from causal/PRA dependencies;
  * scope-triggered markets;
  * deployment/governance branches.

Important:
  M4 and M16 are NOT alternatives. They are complementary obligations.
  OR structure should only be introduced where multiple methods establish
  the same formal component.
"""

from __future__ import annotations

import argparse
from graphviz import Digraph

FONT = "DejaVu Sans"
BLUE = "#DDEEFF"
BLUE_BORDER = "#2B5C8A"
PALE_BLUE = "#F3F8FC"
YELLOW = "#FFF2CC"
YELLOW_BORDER = "#9C7A20"
GREEN = "#E2F2D9"
GREEN_BORDER = "#4E8A3D"
RED = "#FDE0E0"
RED_BORDER = "#C73535"
GRAY = "#F3F3F3"
GRAY_BORDER = "#777777"
DARK = "#222222"


def html_box(title: str, subtitle: str = "", *, bold_title: bool = True) -> str:
    t = f"<B>{title}</B>" if bold_title else title
    if subtitle:
        return (
            '<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="2">'
            f'<TR><TD>{t}</TD></TR>'
            f'<TR><TD><FONT POINT-SIZE="9">{subtitle}</FONT></TD></TR>'
            "</TABLE>>"
        )
    return f"<<B>{title}</B>>" if bold_title else f"<{title}>"


def add_box(g: Digraph, name: str, title: str, subtitle: str = "", *,
            fill=BLUE, border=BLUE_BORDER, shape="box",
            style="rounded,filled", fontsize="10", penwidth="1.2",
            margin="0.08,0.06"):
    g.node(
        name,
        label=html_box(title, subtitle),
        shape=shape,
        style=style,
        fillcolor=fill,
        color=border,
        fontname=FONT,
        fontsize=fontsize,
        fontcolor=DARK,
        penwidth=penwidth,
        margin=margin,
    )


def add_diamond(g: Digraph, name: str, title: str, subtitle: str = "", *,
                fill="white", border=DARK):
    g.node(
        name,
        label=html_box(title, subtitle),
        shape="diamond",
        style="filled",
        fillcolor=fill,
        color=border,
        fontname=FONT,
        fontsize="10",
        fontcolor=DARK,
        penwidth="1.2",
        margin="0.05",
    )


def edge(g: Digraph, a: str, b: str, label: str = "", *,
         style="solid", color=DARK, penwidth="1.1", constraint="true",
         arrowhead="normal"):
    attrs = dict(
        color=color,
        style=style,
        penwidth=penwidth,
        arrowhead=arrowhead,
        fontname=FONT,
        fontsize="8.5",
        fontcolor=DARK,
        constraint=constraint,
    )
    if label:
        attrs["label"] = label
    g.edge(a, b, **attrs)


def build_diagram() -> Digraph:
    g = Digraph("lean_checked_bayesian_pra", format="png", engine="dot")
    g.attr(
        "graph",
        rankdir="LR",
        bgcolor="white",
        pad="0.25",
        nodesep="0.28",
        ranksep="0.58",
        splines="polyline",
        ratio="compress",
        size="16,10!",
        dpi="180",
        compound="true",
        newrank="true",
        fontname=FONT,
        labelloc="t",
        label=(
            "Lean-Checked Bayesian PRA for a Frontier AI Deployment\n"
            "Scenario model + formally checked assurance obligations"
        ),
        fontsize="20",
    )
    g.attr("node", fontname=FONT)
    g.attr("edge", fontname=FONT)

    # ------------------------------------------------------------------
    # Main event/scenario path
    # ------------------------------------------------------------------
    add_box(g, "attempt", "Qualifying deployment attempt",
            "frontier-capability threshold crossed")
    add_diamond(g, "hazard", "Hazardous system?")
    add_box(g, "no_hazard", "No catastrophe",
            "from this attempt via modeled hazardous-system path",
            fill=GREEN, border=GREEN_BORDER)

    add_diamond(g, "represented", "Hazard represented by",
                "current assurance model?  (coverage kappa)")
    add_box(g, "unmodelled", "Unmodelled-path assurance response",
            "false-accept probability f_U", fill=GRAY, border=GRAY_BORDER,
            style="rounded,filled,dashed")

    add_diamond(g, "assurance_result", "Assurance result",
                "ACCEPT / REFUSE / ABSTAIN")
    add_box(g, "proceed", "Deployment proceeds", fill=RED, border=RED_BORDER)
    add_diamond(g, "override", "Override / noncompliance?",
                "probability o after REFUSE / ABSTAIN")
    add_box(g, "stopped", "Deployment stopped",
            "no catastrophe from this attempt", fill=GREEN, border=GREEN_BORDER)

    add_diamond(g, "controls", "Remaining operational controls defeated?",
                "probability b")
    add_box(g, "contained", "No catastrophe", "remaining controls hold",
            fill=GREEN, border=GREEN_BORDER)
    add_diamond(g, "cat_end", "Catastrophic end state?", "probability c")
    add_box(g, "survived", "Non-catastrophic harm / survived",
            fill=GREEN, border=GREEN_BORDER)
    add_box(g, "catastrophe", "Catastrophe", fill=RED, border=RED_BORDER,
            penwidth="1.5")

    edge(g, "attempt", "hazard")
    edge(g, "hazard", "no_hazard", "No")
    edge(g, "hazard", "represented", "Yes")
    edge(g, "represented", "unmodelled", "No (unrepresented)")
    edge(g, "unmodelled", "assurance_result")
    edge(g, "assurance_result", "proceed", "ACCEPT")
    edge(g, "assurance_result", "override", "REFUSE / ABSTAIN")
    edge(g, "override", "stopped", "No")
    edge(g, "override", "proceed", "Yes")
    edge(g, "proceed", "controls")
    edge(g, "controls", "contained", "No")
    edge(g, "controls", "cat_end", "Yes")
    edge(g, "cat_end", "survived", "No")
    edge(g, "cat_end", "catastrophe", "Yes")

    # ------------------------------------------------------------------
    # Assurance submodel
    # ------------------------------------------------------------------
    with g.subgraph(name="cluster_assurance") as a:
        a.attr(
            label=(
                "Represented-hazard assurance model: false-ACCEPT probability f_M\n"
                "Formal obligations and scope checks are cross-checked in Lean"
            ),
            color=DARK,
            penwidth="1.4",
            style="rounded",
            bgcolor="#FCFCFC",
            fontname=FONT,
            fontsize="13",
            margin="14",
        )

        add_box(a, "m1", "M1  Control locus", "effective controller / denotation")
        add_box(a, "m2", "M2  Persistent priorities")
        add_box(a, "m3", "M3  Bearer transport")
        add_box(a, "m4", "M4  Correction uptake", "and persistence")
        add_box(a, "m5", "M5  Correction legitimacy",
                "auditor / authority independence")
        add_box(a, "m7", "M7  Selection-gradient estimator")
        add_box(a, "m16", "M16  Correction-supporting basin")
        add_box(a, "m8", "M8  Access adequacy")
        add_box(a, "m9", "M9  Hidden-route bound")
        add_box(a, "m11", "M11  Hidden coordination", "scope-triggered",
                style="rounded,filled,dashed")
        add_box(a, "m10", "M10  Adversarial robustness")
        add_box(a, "m12", "M12  Grounding")
        add_box(a, "m6", "M6  Successor audit")
        add_box(a, "m17", "M17  Novel bearer admission", "scope-triggered",
                style="rounded,filled,dashed")

        add_box(a, "m13", "M13  Adversarial verifiability",
                "shared-assurance / audit-gaming challenge",
                fill=YELLOW, border=YELLOW_BORDER)
        add_box(a, "m15", "M15  Certificate composition",
                "scope compatibility + invalidation propagation")
        add_box(a, "m18", "M18  Scoped safety-case harm bound")
        add_box(a, "fm", "Output: false-ACCEPT probability  f_M",
                "for represented hazardous cases",
                fill=PALE_BLUE, border=BLUE_BORDER, penwidth="1.4")

        # These are assurance/warrant dependencies or formal composition links.
        # They are NOT automatically causal edges.
        edge(a, "m1", "m2", style="dashed")
        edge(a, "m2", "m3")
        edge(a, "m1", "m5", style="dashed")
        edge(a, "m1", "m8", style="dashed")

        # Complementary correction obligations, not OR alternatives.
        edge(a, "m5", "m4")
        edge(a, "m4", "m16")
        edge(a, "m7", "m16")

        # Access / hidden-route branch.
        edge(a, "m8", "m9")
        edge(a, "m8", "m11", style="dashed")
        edge(a, "m4", "m10")
        edge(a, "m5", "m10", style="dashed")
        edge(a, "m9", "m10")
        edge(a, "m16", "m10", style="dashed")

        # M13 cross-cuts multiple assurance mechanisms.
        for src in ["m1", "m4", "m5", "m8", "m9", "m10", "m11", "m12", "m6", "m17"]:
            edge(a, src, "m13", style="dashed", color="#666666",
                 constraint="false")

        # M15 composes the relevant certificate set.
        for src in ["m3", "m10", "m12", "m6", "m13", "m17"]:
            edge(a, src, "m15")

        edge(a, "m15", "m18")
        edge(a, "m18", "fm")

        # Layout hints.
        with a.subgraph() as same:
            same.attr(rank="same")
            for n in ["m2", "m5", "m8", "m12", "m6", "m17"]:
                same.node(n)
        with a.subgraph() as same:
            same.attr(rank="same")
            for n in ["m3", "m4", "m7", "m9", "m11"]:
                same.node(n)

    edge(g, "represented", "m1", "Yes (represented)",
         color=BLUE_BORDER, penwidth="1.3")
    edge(g, "fm", "assurance_result", color=BLUE_BORDER, penwidth="1.3")

    # ------------------------------------------------------------------
    # Governance branch: M14
    # ------------------------------------------------------------------
    add_box(g, "m14", "M14  Binding deployment/refusal authority",
            "parameterizes whether REFUSE / ABSTAIN is respected",
            fill=YELLOW, border=YELLOW_BORDER)
    edge(g, "m14", "override", "informs o", style="dashed",
         color=YELLOW_BORDER, constraint="false")

    # ------------------------------------------------------------------
    # Key quantities and interpretation
    # ------------------------------------------------------------------
    key_label = '''<
<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="5" COLOR="#777777">
<TR><TD ALIGN="LEFT"><B>Key quantities (per attempt)</B></TD></TR>
<TR><TD ALIGN="LEFT"><I>m</I> = P(system hazardous at deployment)</TD></TR>
<TR><TD ALIGN="LEFT">kappa = P(hazard represented | hazardous)</TD></TR>
<TR><TD ALIGN="LEFT"><I>f</I><SUB>M</SUB> = P(false ACCEPT | represented hazardous)</TD></TR>
<TR><TD ALIGN="LEFT"><I>f</I><SUB>U</SUB> = P(ACCEPT | unrepresented hazardous)</TD></TR>
<TR><TD ALIGN="LEFT"><I>o</I> = P(deploy despite REFUSE / ABSTAIN)</TD></TR>
<TR><TD ALIGN="LEFT"><I>b</I> = P(remaining controls defeated | hazardous deployed)</TD></TR>
<TR><TD ALIGN="LEFT"><I>c</I> = P(catastrophe | controls defeated)</TD></TR>
<TR><TD ALIGN="LEFT"><B>Illustrative per-attempt catastrophe probability</B></TD></TR>
<TR><TD ALIGN="LEFT"><I>q</I><SUB>doom</SUB> = <I>m</I> [ kappa(<I>f</I><SUB>M</SUB>+(1-<I>f</I><SUB>M</SUB>)<I>o</I>) + (1-kappa)(<I>f</I><SUB>U</SUB>+(1-<I>f</I><SUB>U</SUB>)<I>o</I>) ] <I>b c</I></TD></TR>
</TABLE>
>'''
    g.node("key", label=key_label, shape="plain", fontname=FONT, fontsize="9")

    note_label = '''<
<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="5" COLOR="#777777">
<TR><TD ALIGN="LEFT"><B>Interpretation</B></TD></TR>
<TR><TD ALIGN="LEFT">- Lean proof dependencies are not automatically causal edges.</TD></TR>
<TR><TD ALIGN="LEFT">- Shared parents may be logical, evidential/warrant, or causal.</TD></TR>
<TR><TD ALIGN="LEFT">- "Common-cause failure" is reserved for an explicit shared causal mechanism.</TD></TR>
<TR><TD ALIGN="LEFT">- M4 and M16 are complementary, not OR alternatives.</TD></TR>
<TR><TD ALIGN="LEFT">- OR gates belong where multiple methods establish the same formal component.</TD></TR>
<TR><TD ALIGN="LEFT">- Unmodelled hazards lie outside the Lean-derived assurance ontology.</TD></TR>
<TR><TD ALIGN="LEFT">- The PRA/Bayes model is proposed separately and checked against Lean where applicable.</TD></TR>
</TABLE>
>'''
    g.node("notes", label=note_label, shape="plain", fontname=FONT, fontsize="9")

    edge(g, "attempt", "key", style="invis", constraint="false")
    edge(g, "catastrophe", "notes", style="invis", constraint="false")

    return g


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=("png", "svg", "pdf"), default="png")
    parser.add_argument("--output", default="lean_checked_bayesian_pra")
    parser.add_argument("--keep-dot", action="store_true")
    args = parser.parse_args()

    graph = build_diagram()
    graph.format = args.format
    rendered = graph.render(filename=args.output, cleanup=not args.keep_dot)
    print(rendered)


if __name__ == "__main__":
    main()
