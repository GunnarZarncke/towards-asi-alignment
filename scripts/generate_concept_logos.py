#!/usr/bin/env python3
"""Generate minimalist square SVG logos for the site's concept cards.

Each logo is a small, single-stroke line-art icon on a 200x200 viewBox,
using `currentColor` so it inherits text color on the site. Output goes to
drafts/illustrations/concept-logos/<slug>.svg (not wired into the site yet).

Run: python3 scripts/generate_concept_logos.py
"""

import math
import os

OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "drafts", "illustrations", "concept-logos",
)

STROKE = 6
HEADER = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="3.5" markerHeight="3.5" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="currentColor"/>
    </marker>
  </defs>
  <g fill="none" stroke="currentColor" stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round">
""".format(stroke=STROKE)
FOOTER = "  </g>\n</svg>\n"


def rugged_oval(cx, cy, rx, ry, jitter, n=12, rotation=0.0):
    """Closed path approximating an ellipse with per-point radius jitter,
    giving the 'rugged oval' boundary look used throughout the deck."""
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n + rotation
        r = 1 + jitter[i % len(jitter)]
        x = cx + rx * r * math.cos(a)
        y = cy + ry * r * math.sin(a)
        pts.append((x, y))
    d = f"M {pts[0][0]:.1f},{pts[0][1]:.1f} "
    for i in range(1, n + 1):
        x, y = pts[i % n]
        d += f"L {x:.1f},{y:.1f} "
    d += "Z"
    return f'<path d="{d}"/>'


JITTER_A = [0.06, -0.04, 0.08, -0.02, 0.05, -0.07, 0.03, -0.03, 0.07, -0.05, 0.02, -0.06]
JITTER_B = [-0.05, 0.07, -0.02, 0.06, -0.08, 0.04, -0.03, 0.05, -0.06, 0.03, -0.04, 0.08]


def circle(cx, cy, r, dashed=False):
    dash = ' stroke-dasharray="6 7"' if dashed else ""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}"{dash}/>'


def dot(cx, cy, r=6):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="currentColor" stroke="none"/>'


def line(x1, y1, x2, y2, dashed=False, arrow=False):
    dash = ' stroke-dasharray="6 7"' if dashed else ""
    mk = ' marker-end="url(#arrow)"' if arrow else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{dash}{mk}/>'


def path(d, dashed=False, arrow=False):
    dash = ' stroke-dasharray="6 7"' if dashed else ""
    mk = ' marker-end="url(#arrow)"' if arrow else ""
    return f'<path d="{d}"{dash}{mk}/>'


def curve_arrow(x1, y1, x2, y2, bulge, arrow=True, dashed=False):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    cx, cy = mx + nx * bulge, my + ny * bulge
    d = f"M {x1},{y1} Q {cx:.1f},{cy:.1f} {x2},{y2}"
    return path(d, dashed=dashed, arrow=arrow)


def fluted_column(cx, base_y, height, w=10, stage=0):
    """Classical fluted pillar on a shared plinth; stage 0=intact .. 3=stump."""
    parts = []
    top = base_y - height
    if stage == 0:
        parts += [
            line(cx - w - 3, top + 2, cx + w + 3, top + 2),
            line(cx - w - 3, top + 2, cx - w - 3, top + 9),
            line(cx + w + 3, top + 2, cx + w + 3, top + 9),
            line(cx - w - 1, top + 9, cx - w - 1, top + 12),
            line(cx + w + 1, top + 9, cx + w + 1, top + 12),
            line(cx - w, top + 12, cx - w, base_y),
            line(cx + w, top + 12, cx + w, base_y),
        ]
        for i in range(3):
            fx = cx - w + (2 * w / 4) * (i + 1)
            parts.append(line(fx, top + 14, fx, base_y - 2))
    elif stage == 1:
        parts += [
            path(f"M {cx-w-2},{top+6} L {cx-2},{top} L {cx+3},{top+4} L {cx+w+1},{top+8}"),
            line(cx - w, top + 10, cx - w, base_y),
            line(cx + w, top + 10, cx + w, base_y),
        ]
        for i in range(3):
            fx = cx - w + (2 * w / 4) * (i + 1)
            parts.append(line(fx, top + 12, fx, base_y - 2))
        parts.append(path(f"M {cx+w},{top+18} L {cx+w+4},{top+24}"))
    elif stage == 2:
        broken_top = base_y - height * 0.52
        parts += [
            path(f"M {cx-w},{broken_top+10} L {cx-5},{broken_top} L {cx+2},{broken_top+6} "
                 f"L {cx+w},{broken_top+12}"),
            line(cx - w, broken_top + 12, cx - w, base_y),
            line(cx + w, broken_top + 12, cx + w, base_y),
            path(f"M {cx-w},{broken_top+22} L {cx-w-5},{broken_top+30}"),
        ]
        for i in range(2):
            fx = cx - w + (2 * w / 3) * (i + 1)
            parts.append(line(fx, broken_top + 14, fx, base_y - 2))
    else:
        stump_top = base_y - height * 0.2
        parts += [
            path(f"M {cx-w+1},{stump_top+7} L {cx-1},{stump_top} L {cx+2},{stump_top+5} "
                 f"L {cx+w-1},{stump_top+9}"),
            line(cx - w + 2, stump_top + 9, cx - w + 2, base_y),
            line(cx + w - 2, stump_top + 9, cx + w - 2, base_y),
        ]
    return parts


CONCEPTS = {}


def add(slug, body):
    CONCEPTS[slug] = body


# --- Core boundary / agent concepts -----------------------------------

add("agent-without-anthropomorphism", lambda: "\n".join([
    circle(100, 100, 46),
    # control loop: exits right, rounds under the boundary, re-enters on the left
    path("M 146,100 C 178,100 188,138 188,162 C 188,188 100,192 100,192 "
         "C 12,188 12,162 12,138 C 12,100 32,100 54,100", arrow=True),
]))

add("agent-detection-to-alignment-target", lambda: "\n".join([
    circle(75, 100, 34, dashed=True),
    circle(75, 100, 3),
    circle(140, 100, 20),
    line(112, 100, 128, 100, arrow=True),
]))

add("alignment-as-measurement", lambda: "\n".join([
    circle(80, 100, 30, dashed=True),
    dot(80, 100, 5),
    line(140, 60, 140, 140),
    line(110, 100, 170, 100),
    circle(140, 100, 10),
    dot(140, 100, 6),
]))

add("boundary-discovery", lambda: "\n".join([
    rugged_oval(100, 105, 55, 40, JITTER_A),
    path("M 30,60 A 90,90 0 0 1 170,60", dashed=True),
    dot(140, 66, 5),
]))

add("the-boundary-error", lambda: "\n".join([
    rugged_oval(104, 108, 58, 42, JITTER_B),
    circle(88, 96, 22),
    dot(88, 96, 5),
]))

add("boundary-residual", lambda: "\n".join([
    rugged_oval(100, 100, 62, 48, JITTER_A),
    rugged_oval(100, 100, 34, 26, JITTER_B, rotation=0.7),
    line(100, 74, 100, 52, dashed=True),
    line(100, 126, 100, 148, dashed=True),
]))

add("composite-agency", lambda: "\n".join([
    rugged_oval(100, 105, 62, 46, JITTER_A),
    circle(75, 95, 14),
    circle(112, 88, 12),
    circle(96, 122, 13),
    circle(128, 116, 11),
]))

add("strategic-opacity", lambda: "\n".join([
    f'<path d="M 100,40 A 60,60 0 0 1 100,160 A 60,60 0 0 1 100,40 Z"/>',
    rugged_oval(100, 100, 58, 44, JITTER_A),
    path("M 100,52 A 58,44 0 0 1 100,148", dashed=True),
]))

add("artificial-civilization", lambda: "\n".join([
    circle(100, 100, 20),
    circle(50, 60, 8),
    circle(150, 60, 8),
    circle(50, 140, 8),
    circle(150, 140, 8),
    path("M 58,60 L 142,60 L 150,68 L 150,132 L 142,140 L 58,140 L 50,132 L 50,68 Z", arrow=True),
]))

add("scaffold-misuse", lambda: "\n".join([
    line(30, 100, 85, 100, arrow=True),
    f'<rect x="85" y="70" width="60" height="60" rx="6"/>',
    path("M 145,100 L 170,70", arrow=True),
]))

# --- Correction / dynamics ---------------------------------------------

add("correction-channel-integrity", lambda: "\n".join([
    rugged_oval(105, 100, 55, 42, JITTER_A),
    line(30, 100, 78, 100, arrow=True),
    dot(105, 100, 6),
]))

add("anti-capture-correction-validity", lambda: "\n".join([
    rugged_oval(100, 100, 55, 42, JITTER_B),
    line(28, 100, 62, 100),
    path("M 62,100 C 70,120 90,132 108,124", arrow=True, dashed=True),
]))

add("dynamical-guarantee", lambda: "\n".join([
    line(25, 55, 175, 55),
    line(25, 145, 175, 145),
    path("M 35,120 C 65,60 95,150 125,70 C 145,30 160,90 170,100"),
]))

add("attractor-control", lambda: "\n".join([
    # wide double-well potential spanning the full frame; dot in one basin,
    # dashed curve hints at a competing socio-technical attractor
    path("M 12,158 C 12,32 48,32 78,32 C 98,32 98,158 98,158"),
    path("M 98,158 C 98,32 128,32 158,32 C 188,32 188,158 188,158"),
    dot(55, 118, 9),
    path("M 112,158 C 112,62 148,62 178,158", dashed=True),
]))

add("successor-stability", lambda: "\n".join([
    circle(55, 100, 26),
    circle(115, 100, 19),
    circle(160, 100, 13),
    line(81, 100, 96, 100, arrow=True),
    line(134, 100, 147, 100, arrow=True),
]))

add("bearer-persistence", lambda: "\n".join([
    rugged_oval(100, 100, 58, 44, JITTER_A),
    dot(100, 100, 7),
]))

add("bearer-map-commutation-failure", lambda: "\n".join([
    f'<rect x="45" y="45" width="110" height="110" rx="4"/>',
    line(45, 45, 155, 155, dashed=True, arrow=True),
    line(155, 45, 45, 138, dashed=True, arrow=True),
    dot(155, 155, 5),
    dot(45, 138, 5),
]))

add("conserved-properties-growth-split-merge", lambda: "\n".join([
    # split (left): one unit -> two; merge (right): two -> one; dot marks conserved property
    circle(40, 62, 20),
    circle(40, 138, 16),
    circle(78, 100, 16),
    line(56, 72, 68, 88, arrow=True),
    line(56, 128, 68, 110, arrow=True),
    dot(40, 62, 4),
    circle(132, 100, 22),
    circle(168, 62, 13),
    circle(168, 138, 13),
    line(148, 86, 158, 74, arrow=True),
    line(148, 114, 158, 126, arrow=True),
    dot(132, 100, 4),
]))

add("value-bundle-transport", lambda: "\n".join([
    line(35, 80, 80, 80, arrow=True),
    line(35, 100, 80, 100, arrow=True),
    line(35, 120, 80, 120, arrow=True),
    path("M 100,50 L 100,150", dashed=True),
    line(120, 80, 165, 80, arrow=True),
    line(120, 100, 165, 100, arrow=True),
    line(120, 120, 165, 120, arrow=True),
]))

add("value-change-vs-corruption", lambda: "\n".join([
    dot(42, 100, 8),
    # legitimate change: smooth continuous drift upward
    path("M 42,100 C 82,52 122,52 162,48", arrow=True),
    # corruption: runs level, snaps at a right angle, marked with × at the break
    path("M 42,100 L 82,100 L 82,168 L 130,168", arrow=True),
    path("M 74,92 L 90,108 M 90,92 L 74,108"),
]))

add("goodhart-as-selector", lambda: "\n".join([
    circle(100, 100, 52),
    circle(100, 100, 32),
    circle(100, 100, 12),
    # cracks radiating through the target — optimizing the proxy breaks it
    line(100, 100, 152, 58),
    line(100, 100, 48, 62),
    line(100, 100, 54, 148),
    line(100, 100, 148, 142),
    line(100, 100, 100, 48),
    path("M 132,52 L 142,46 L 136,58"),
    # strong arrow driven into the bullseye
    '<line x1="172" y1="28" x2="112" y2="88" stroke="currentColor" stroke-width="10" stroke-linecap="round"/>',
    '<path d="M 100,100 L 120,80 L 114,96 Z" fill="currentColor" stroke="none"/>',
]))

# --- Certification / evidence / method ----------------------------------

add("certification-under-manipulation", lambda: "\n".join([
    line(100, 35, 100, 165, dashed=True),
    path("M 55,140 L 65,150 L 82,120"),
    path("M 118,80 L 132,66 M 132,80 L 118,66"),
]))

add("evidence-and-uncertainty", lambda: "\n".join([
    dot(100, 100, 8),
    circle(100, 100, 26, dashed=True),
    circle(100, 100, 44, dashed=True),
]))

add("experiment-methodology", lambda: "\n".join([
    f'<rect x="40" y="40" width="120" height="120" rx="6"/>',
    line(100, 40, 100, 160, dashed=True),
    f'<rect x="90" y="88" width="20" height="24" rx="3"/>',
    path("M 94,88 L 94,78 A 6,6 0 0 1 106,78 L 106,88"),
]))

add("negative-results", lambda: "\n".join([
    # results ledger: successes, failures, and qualified findings all kept
    f'<rect x="48" y="42" width="104" height="116" rx="5"/>',
    line(62, 72, 118, 72),
    path("M 126,68 L 130,76 L 138,64"),
    line(62, 98, 118, 98),
    path("M 126,94 L 138,106 M 138,94 L 126,106"),
    line(62, 124, 118, 124),
    path("M 126,120 L 138,132 M 138,120 L 126,132"),
    line(62, 150, 118, 150),
    line(126, 150, 138, 150),
]))

add("inferential-coupling", lambda: "\n".join([
    circle(65, 100, 30),
    circle(135, 100, 30),
    path("M 55,88 L 75,112 M 55,112 L 75,88"),
    path("M 125,88 L 145,112 M 125,112 L 145,88"),
]))

add("intervention-supported-unit-discovery", lambda: "\n".join([
    circle(60, 100, 22),
    circle(140, 100, 22),
    line(82, 100, 118, 100, dashed=True),
    path("M 92,90 L 108,110 M 92,110 L 108,90"),
]))

add("unit-discovery-stress-test", lambda: "\n".join([
    # top: clean detected pair under a calm, sparse dotted backdrop
    path("M 35,45 L 165,45", dashed=True),
    circle(80, 62, 15),
    circle(120, 62, 15),
    line(95, 62, 105, 62),
    # divider
    line(30, 100, 170, 100, dashed=True),
    # bottom: same pair, now wobbling, under dense noisy crosshatching
    path("M 30,150 L 60,120 M 45,150 L 75,120 M 60,150 L 90,120 M 75,150 L 105,120 "
         "M 90,150 L 120,120 M 105,150 L 135,120 M 120,150 L 150,120 M 135,150 L 165,120"),
    circle(78, 142, 13),
    circle(122, 142, 13),
    line(91, 148, 109, 136),
]))

add("et-external-transfer", lambda: "\n".join([
    f'<rect x="88" y="40" width="24" height="40" rx="3"/>',
    rugged_oval(60, 145, 30, 22, JITTER_A),
    rugged_oval(140, 145, 30, 22, JITTER_B),
    line(100, 80, 100, 110, arrow=False),
    path("M 100,110 L 65,128", dashed=True),
    path("M 100,110 L 135,128", dashed=True),
]))

add("scope-and-correction-capacity", lambda: "\n".join([
    circle(100, 100, 70, dashed=True),
    rugged_oval(100, 100, 40, 30, JITTER_A),
]))

# --- Institutional case-study cards -------------------------------------

add("institutional-capability-latency-gap", lambda: "\n".join([
    line(70, 40, 70, 160),
    line(130, 40, 130, 160),
    line(70, 40, 130, 40),
    path("M 100,40 L 92,100 L 108,110 L 96,160"),
]))

add("institutional-constraint-inheritance", lambda: "\n".join([
    f'<rect x="80" y="40" width="40" height="30" rx="4"/>',
    dot(100, 55, 4),
    line(90, 70, 60, 105, arrow=True),
    line(110, 70, 140, 105, arrow=True),
    f'<rect x="40" y="105" width="40" height="30" rx="4"/>',
    f'<rect x="120" y="105" width="40" height="30" rx="4"/>',
    dot(60, 120, 4),
    dot(140, 120, 4),
]))

add("institutional-dual-mandate-genesis", lambda: "\n".join([
    f'<rect x="55" y="45" width="90" height="45" rx="5"/>',
    line(75, 90, 100, 68, arrow=True),
    line(125, 90, 100, 68, arrow=True),
    f'<rect x="45" y="120" width="45" height="40" rx="5"/>',
    f'<rect x="110" y="120" width="45" height="40" rx="5"/>',
    line(67, 140, 67, 122, arrow=True),
    line(132, 140, 132, 122, arrow=True),
]))

add("institutional-entrenchment-corrigibility", lambda: "\n".join([
    # temple with a split foundation — correction channel used to abolish itself
    # (Enabling Act); the institutional base no longer supports what stands on it
    path("M 100,48 L 58,92 L 142,92 Z"),
    line(74, 92, 74, 136),
    line(126, 92, 126, 136),
    line(42, 152, 84, 152),
    line(42, 152, 42, 162),
    line(84, 152, 84, 162),
    line(116, 152, 158, 152),
    line(116, 152, 116, 162),
    line(158, 152, 158, 162),
    path("M 84,152 L 90,146 L 86,154"),
    path("M 116,152 L 110,146 L 114,154"),
]))

add("institutional-evidence-before-authority", lambda: "\n".join([
    # a single timeline: solid recording runs from the left, straight through
    # and past a dashed authority flag that only appears partway along --
    # evidence predates and outlasts the enforcement mandate.
    line(35, 130, 170, 130),
    dot(50, 130, 8),
    f'<rect x="38" y="70" width="24" height="30" rx="3"/>',
    line(50, 100, 50, 130),
    # dashed triangular authority flag planted mid-timeline
    path("M 130,130 L 130,75 L 158,95 L 130,110", dashed=True),
]))

def ratchet_wheel(cx, cy, r, n=6):
    """A one-way ratchet gear: asymmetric sawtooth teeth, each preceded
    (counter-clockwise) by a small burst mark -- the catastrophe that
    forced that click forward."""
    parts = [circle(cx, cy, r * 0.55)]
    for i in range(n):
        a0 = 2 * math.pi * i / n
        a1 = a0 + 2 * math.pi / n
        # sawtooth: steep radial edge then shallow ramp (one-way look)
        steep_a = a0 + 0.06
        x0, y0 = cx + r * 0.55 * math.cos(a0), cy + r * 0.55 * math.sin(a0)
        x1, y1 = cx + r * math.cos(steep_a), cy + r * math.sin(steep_a)
        x2, y2 = cx + r * 0.55 * math.cos(a1), cy + r * 0.55 * math.sin(a1)
        parts.append(path(f"M {x0:.1f},{y0:.1f} L {x1:.1f},{y1:.1f} L {x2:.1f},{y2:.1f}"))
        # spark/burst just before (clockwise side of) each tooth
        burst_a = a0 - 0.35
        bx, by = cx + r * 1.28 * math.cos(burst_a), cy + r * 1.28 * math.sin(burst_a)
        parts.append(dot(bx, by, 3.5))
    return "\n".join(parts)


add("institutional-genesis-catastrophe-ratchet", lambda: ratchet_wheel(100, 100, 50, n=6))

add("institutional-genesis-chronic-threat", lambda: "\n".join([
    path("M 25,95 Q 45,70 65,95 T 105,95 T 145,95 T 185,95"),
    # a standing gate/dam: two posts + a crossbar sitting in the continuous wave
    line(75, 95, 75, 155),
    line(135, 95, 135, 155),
    line(65, 110, 145, 110),
    line(75, 155, 135, 155),
]))

add("institutional-genesis-money-at-risk", lambda: "\n".join([
    # danger/threat on the left drives creation of correction because capital
    # is already exposed -- hazard -> money at risk
    path("M 58,98 L 43,158 L 73,158 Z"),
    line(58, 126, 58, 140),
    dot(58, 148, 4),
    line(96, 100, 120, 100, arrow=True),
    circle(152, 100, 28),
    line(152, 78, 152, 122),
    path("M 165,86 C 147,80 137,86 137,94 C 137,102 165,96 165,104 C 165,112 155,116 145,110"),
]))

add("institutional-memory-refresh", lambda: "\n".join([
    circle(100, 100, 50, dashed=True),
    dot(100, 50, 6),
    dot(139, 79, 6),
    dot(139, 121, 6),
    dot(100, 150, 6),
    dot(61, 121, 6),
    dot(61, 79, 6),
    path("M 100,50 A 50,50 0 0 1 139,79", arrow=True),
]))

add("institutional-reform-decay", lambda: "\n".join([
    # Gibbon-style crumbling pillars: intact -> chipped -> broken -> stump
    line(34, 172, 166, 172),
    line(34, 172, 34, 178),
    line(166, 172, 166, 178),
    *fluted_column(54, 172, 108, stage=0),
    *fluted_column(88, 172, 108, stage=1),
    *fluted_column(122, 172, 108, stage=2),
    *fluted_column(148, 172, 108, stage=3),
]))

add("institutional-selection-gating", lambda: "\n".join([
    path("M 50,50 L 150,50 L 110,100 L 110,150"),
    path("M 150,50 L 50,50 L 90,100 L 90,150", dashed=True),
    dot(100, 120, 5),
    circle(100, 155, 15),
]))

def render():
    os.makedirs(OUT_DIR, exist_ok=True)
    written = []
    for slug, fn in CONCEPTS.items():
        body = fn()
        svg = HEADER + body + "\n" + FOOTER
        path_out = os.path.join(OUT_DIR, f"{slug}.svg")
        with open(path_out, "w") as f:
            f.write(svg)
        written.append(slug)
    print(f"[done] wrote {len(written)} SVGs to {OUT_DIR}")
    return written


if __name__ == "__main__":
    render()
