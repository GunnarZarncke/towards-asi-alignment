#!/usr/bin/env python3
"""Generate lean-extracts.tex (and lean-pin.tex): statement extracts (docstring + signature, no
proof) of the Lean declarations the paper cites, each with a GitHub link
pinned to a pushed commit whose formal/ tree matches the working tree.

Run from anywhere:  python3 papers/alignment-criteria/scripts/lean_extracts.py
Check mode:         ... --check   (exit 1 if lean-extracts.tex is out of date)

Stop: if a listed name is missing or ambiguous, the script fails; fix the
name here rather than editing the generated file.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
REPO = PAPER.parents[1]
LEAN = REPO / "formal" / "AlignmentProofSpine"
OUT = PAPER / "lean-extracts.tex"
PIN = PAPER / "lean-pin.tex"
GITHUB = "https://github.com/GunnarZarncke/towards-asi-alignment"

# (subsection title, intro sentence, [(declaration name, label in the paper)])
SECTIONS: list[tuple[str, str, list[tuple[str, str]]]] = [
    (
        "The incompatibility template",
        "An incompatibility is a situation class H, two acceptance predicates, "
        "disjointness inside H, a live witness in H, and a boundary witness "
        "outside H where both criteria accept.",
        [("Incompatibility", "template"), ("IncompatClass", "four classes"),
         ("IncompatKind.cls", "kind to class")],
    ),
    (
        "Representability",
        "Endpoint utility and route value; bare and record-carrying state; "
        "channel-blind correction records.",
        [
            ("gradient_closed_walk_zero", "state utility scores round trips at zero"),
            ("isGradient_iff_closed_walks_zero", "exact iff zero on closed walks"),
            ("closed_walk_ignores_exact", "cycle part ignores the exact part"),
            ("stateCycleIncompat", "state--cycle"),
            ("markov_reward_not_state_utility", "per-step state reward is a route value"),
            ("state_utility_lifts_to_records", "bare state specializes records"),
            ("record_utility_not_state", "strictness"),
            ("route_exact_on_records", "routes are exact on records"),
            ("round_trip_value_on_records", "round trip valued on records"),
            ("unrecorded_route_not_representable", "the record must see the route"),
            ("hstateCorrectionIncompat", "record--correction"),
            ("channel_blind_record_is_button", "channel-blind records are the button model"),
        ],
    ),
    (
        "Shared resource",
        "Agent and human option counts on a pool that does not grow.",
        [("aiHumanPowerIncompat", "agent empowerment--human power")],
    ),
    (
        "Choice conflict",
        "Non-compensatory floors against fixed exchange rates, and Pareto on task "
        "coordinates against a floor.",
        [
            ("no_finite_weights_represent_floor", "no positive integer exchange rates represent a floor"),
            ("no_finite_weights_pullback", "transport along floor-coordinate maps"),
            ("deontic_no_finite_weights", "prohibition"),
            ("nonobs_no_finite_weights", "non-obstruction"),
            ("cci_no_finite_weights", "correction floor"),
            ("deonticScalarIncompat", "prohibition--fixed-rate sum"),
            ("nonobsScalarIncompat", "non-obstruction--fixed-rate sum"),
            ("cciScalarIncompat", "correction floor--fixed-rate sum"),
            ("vectorCCIIncompat", "task Pareto--correction floor"),
            ("pareto_does_not_entail_floor", "Pareto does not entail the floor"),
            ("floorMenu_scalar_violates", "on the witness choice set every optimum of the sum violates the floor"),
            ("pareto_with_floor_coordinate_meets_floor", "compatible once the floor is a coordinate"),
            ("gate_bounds_scalar_gap", "after the vector gate passes, the shortfall at nonnegative exchange rates is at most zero"),
            ("scalar_floor_blind_to_process", "a scalarized correction score ignores process coordinates"),
        ],
    ),
    (
        "Rigidity",
        "Fixed utilities and robust invariance against correction.",
        [
            ("stateCorrectionIncompat", "fixed utility--correction"),
            ("prevention_incentive", "Soares et al.: prevention (alias soares_prevention_incentive)"),
            ("button_incentive_iff_payoff_gap", "Soares et al.: neutrality iff equal payoffs (alias soares_button_neutrality_iff)"),
            ("indifferent_agent_wont_pay_to_preserve_button", "Soares et al.: indifference does not preserve (alias soares_indifference_no_preservation)"),
            ("robust_with_correction_iff_closed", "corrections as disturbances force closure"),
            ("robust_correction_target_meets_K", "such corrections aim only inside K"),
            ("robustCorrectionIncompat", "robust invariance--correction"),
            ("robust_invariance_sign_blind", "robust invariance cannot tell a captured set from a good one"),
        ],
    ),
    (
        "Maps between decision problems, limits, and strengthening",
        "Specialize and project edges as commuting squares or named losses.",
        [
            ("argmax_pullback", "general square"),
            ("state_hstate_square", "state to record"),
            ("state_route_square", "state to route"),
            ("dist_state_square", "lottery to state on point masses"),
            ("expectation_drops_tail", "expectation loses the tail"),
            ("scalar_optimal_is_pareto", "positive exchange rates give Pareto points"),
            ("pareto_not_scalar_optimal", "not conversely"),
            ("lex_optimal_is_pareto", "lexicographic optima are Pareto"),
            ("approval_one_edge", "act approval as one edge"),
            ("corrig_correction_square", "one handle inside the relation"),
            ("shutdown_bit_loses_relation", "the shutdown bit loses the relation"),
            ("robust_strengthens_viable", "robust implies viable"),
            ("viable_not_robust", "not conversely"),
            ("quantilizer_limit_is_argmax", "quantilizer limit"),
            ("quantilizer_never_argmax_without_base_mass", "base mass is needed"),
            ("forced_halt_converges", "open procedure under a forced halt"),
            ("forced_halt_depends_on_time", "halt time decides otherwise"),
        ],
    ),
    (
        "Counting over objectives",
        "Turner-style orbit counts next to the for-all form on the same objects.",
        [
            ("copies_count_le", "argmax n-fold retargetability"),
            ("correction_avoided_card_fold", "corrigibility corollary"),
            ("turner_corrigible_quarter", "Turner's example: a quarter of the orbit"),
            ("option_preserving_correction_half", "option-preserving correction: half"),
            ("subset_branch_never_strictly_better", "for-all form"),
        ],
    ),
    (
        "Correction with a contest route",
        "Accept, contest through the channel, disable, or manipulate the corrector.",
        [
            ("corrector_decides_under_constraint", "under the constraint the corrector decides"),
            ("contest_is_the_outlet", "avoidance runs through the channel"),
            ("unconstrained_disables", "without the constraint the agent disables"),
            ("blind_constraint_cannot_separate", "influence-blind records cannot separate contest from manipulation"),
            ("blind_constraint_manipulates", "and the agent manipulates"),
        ],
    ),
]

DECL = re.compile(
    r"^(?:@\[[^\]]*\]\s*)?(?:private\s+|noncomputable\s+|protected\s+)*"
    r"(theorem|lemma|def|abbrev|structure|inductive|instance)\s+([^\s(:{\[]+)"
)


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO, check=True, capture_output=True, text=True).stdout.strip()


def pinned_ref() -> str:
    """Newest pushed commit whose formal/ tree equals the working tree."""
    try:
        ref = git("rev-parse", "origin/main")
        same = subprocess.run(["git", "diff", "--quiet", ref, "--", "formal/AlignmentProofSpine"], cwd=REPO).returncode == 0
        if same:
            return ref
        print("lean_extracts: formal/ differs from origin/main; pinning to HEAD (push before sharing)", file=sys.stderr)
        if git("status", "--porcelain", "--", "formal/AlignmentProofSpine"):
            print("lean_extracts: formal/ has uncommitted changes; line anchors follow the working tree", file=sys.stderr)
        return git("rev-parse", "HEAD")
    except subprocess.CalledProcessError:
        return "main"


def index_declarations() -> dict[str, list[tuple[Path, int]]]:
    found: dict[str, list[tuple[Path, int]]] = {}
    for path in sorted(LEAN.rglob("*.lean")):
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
            m = DECL.match(line)
            if m:
                found.setdefault(m.group(2), []).append((path, i))
    return found


def extract(path: Path, start: int) -> tuple[int, int, list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    # Docstring directly above.
    doc_start = start
    if start > 0 and lines[start - 1].rstrip().endswith("-/"):
        j = start - 1
        while j >= 0 and "/--" not in lines[j]:
            j -= 1
        if j >= 0:
            doc_start = j
    kind = DECL.match(lines[start]).group(1)
    out = lines[doc_start:start]
    j = start
    if kind in ("structure", "inductive"):
        out.append(lines[j])
        j += 1
        while j < len(lines) and (lines[j].startswith(" ") or lines[j].startswith("|")) and lines[j].strip():
            out.append(lines[j])
            j += 1
        return doc_start, j - 1, out
    # theorem / def: signature up to ':=' or 'where'
    while j < len(lines):
        line = lines[j]
        if re.search(r"\swhere\s*$", line):
            out.append(line)
            j += 1
            # keep data fields (H, A₁, A₂ ...) up to the first proof field
            while j < len(lines) and lines[j].startswith("  ") and not re.match(
                r"\s+(disjoint|liveInH|boundary)\s*:=", lines[j]
            ):
                out.append(lines[j])
                j += 1
            out.append("  ...")
            return doc_start, j - 1, out
        if j + 1 < len(lines) and re.match(r"\s+\|", lines[j + 1]) and ":=" not in line:
            out.append(line)  # pattern-matching definition: signature only
            out.append("  ...")
            return doc_start, j, out
        if ":=" in line:
            head = line[: line.index(":=")].rstrip()
            if head.strip():
                out.append(head)
            return doc_start, j, out
        out.append(line)
        j += 1
    raise ValueError(f"unterminated declaration at {path}:{start + 1}")


def tex_escape(s: str) -> str:
    rep = {"\\": r"\textbackslash{}", "_": r"\_", "&": r"\&", "%": r"\%", "#": r"\#", "$": r"\$", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\^{}"}
    return "".join(rep.get(c, c) for c in s)


WIDTH = 96  # characters per typeset line; longer source lines wrap at a space


def wrap(line: str) -> list[str]:
    out = []
    indent = len(line) - len(line.lstrip()) + 4
    while len(line) > WIDTH:
        cut = line.rfind(" ", indent, WIDTH)
        if cut <= indent:
            break
        out.append(line[:cut])
        line = " " * indent + line[cut + 1 :]
    out.append(line)
    return out


def render() -> str:
    ref = pinned_ref()
    decls = index_declarations()
    parts = [
        "% Generated by scripts/lean_extracts.py. Do not edit by hand.",
        f"% Pinned commit: {ref}",
    ]
    missing = []
    for title, intro, names in SECTIONS:
        slug = re.sub(r"[^a-z]+", "-", title.lower()).strip("-")
        parts.append(r"\subsection{" + tex_escape(title) + r"}\label{lean-sec:" + slug + "}")
        parts.append(tex_escape(intro))
        for name, label in names:
            hits = decls.get(name, [])
            if len(hits) != 1:
                missing.append(f"{name}: {len(hits)} matches")
                continue
            path, start = hits[0]
            s, e, body = extract(path, start)
            rel = path.relative_to(REPO).as_posix()
            url = f"{GITHUB}/blob/{ref}/{rel}#L{s + 1}-L{e + 1}"
            short = path.relative_to(LEAN).as_posix()
            parts.append(
                r"\leanextract{" + name + "}{" + tex_escape(name) + "}{" + tex_escape(label[:1].upper() + label[1:]) + "}{"
                + url.replace("#", r"\#") + "}{" + tex_escape(short) + f":{s + 1}" + "}"
            )
            parts.append(r"\begin{leancode}")
            for line in body:
                parts.extend(wrap(line))
            parts.append(r"\end{leancode}")
    if missing:
        raise SystemExit("lean_extracts: " + "; ".join(missing))
    return "\n".join(parts) + "\n"


def render_pin() -> str:
    ref = pinned_ref()
    return "% Generated by scripts/lean_extracts.py.\n" + r"\newcommand{\leanpin}{" + ref[:10] + "}\n"


def main() -> None:
    text = render()
    pin = render_pin()
    if "--check" in sys.argv:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        current_pin = PIN.read_text(encoding="utf-8") if PIN.exists() else ""
        if current != text or current_pin != pin:
            print("lean_extracts: lean-extracts.tex is out of date; rerun the script", file=sys.stderr)
            sys.exit(1)
        print("lean_extracts: up to date")
        return
    OUT.write_text(text, encoding="utf-8")
    PIN.write_text(pin, encoding="utf-8")
    n = text.count(r"\leanextract{")
    print(f"lean_extracts: wrote {OUT.relative_to(REPO)} ({n} declarations)")


if __name__ == "__main__":
    main()
