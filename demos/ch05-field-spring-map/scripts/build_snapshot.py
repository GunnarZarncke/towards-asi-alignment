#!/usr/bin/env python3
"""Build frozen snapshot.json for the field spring-map demo.

Fetches AISafety.com organizations (CC-BY-4.0), matches to field agendas via
clustering.yml, inherits matrix/evidence weights, and scores unmatched listings
with heuristics (or optional OpenAI classification).

Usage (from repo root):
  python3 demos/ch05-field-spring-map/scripts/build_snapshot.py
  python3 demos/ch05-field-spring-map/scripts/build_snapshot.py --llm
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

SCRIPT_DIR = Path(__file__).resolve().parent
DEMO_DIR = SCRIPT_DIR.parent
REPO_ROOT = DEMO_DIR.parents[1]
FIELD_DATA = REPO_ROOT / "reference" / "field-agendas" / "data"
OUT_PATH = DEMO_DIR / "data" / "snapshot.json"
LOGOS_DIR = DEMO_DIR / "data" / "logos"

LIVE_BRIDGES = [
    "MB1", "MB2", "MB3", "MB4", "MB4a", "MB5", "MB6",
    "MB7", "MB7d", "MB9", "MB10", "MB11",
]

# AISafety.com ids → field matrix slug when clustering labels miss a match.
LISTING_AGENDA_OVERRIDES: dict[str, str] = {
    "rec1QpsZCIfnfTF1y": "this-project-towards-superintelligence-alignment-tsa",
    "recQA1xIcTe6j8tjr": "neglected-approaches-portfolio",
    # CHAI / cooperative IRL lineage (Algorithmic Alignment Group, MIT)
    "recDaHglyXODmpBkV": "chai-russell",
    # MIRI-adjacent alignment wiki (Yudkowsky; foundational concepts and open problems)
    "recAa8UuevcBb6LFI": "miri",
}

# Curated bridge weights when no matrix row exists (field-evidence style scores, not discharge).
LISTING_WEIGHT_OVERRIDES: dict[str, dict] = {
    "reccBIIZjZT5Bh5wc": {
        "rationale": (
            "ACS: multi-agent / hierarchical-agency / civilization-scale ecosystem alignment "
            "(acsresearch.org; AF announcing post)"
        ),
        "weights": {
            # MB1 Embedded Agency — core “theory of hierarchical agency”; superagent/subagent relations
            "MB1": 0.85,
            # MB2 Value Learning — alignment proposals grounded in how humans actually reason/value
            "MB2": 0.55,
            # MB3 Value Referent — whose values / institutions count as alignment targets in multi-agent settings
            "MB3": 0.5,
            # MB5 Reflective Stability — some overlap via ontology shift across nested agents / ecosystems
            "MB5": 0.35,
            # MB6 Selection & Basin Stability — flagship: AI ecosystems, incremental disempowerment, multi-agent selection
            "MB6": 0.95,
            # MB7 Inner Alignment — InterLab empirics on deception/manipulation in multi-agent LLM settings
            "MB7": 0.5,
            # MB10 Eval Gaming — some empirical protocol work; not successor-audit center of gravity
            "MB10": 0.25,
            # MB11 Deployment Safety — institutional protocols, governance of human–AI ecosystems at scale
            "MB11": 0.65,
        },
    },
    "receBiOcbBtR6nuL6": {
        "rationale": (
            "CSER: existential-risk governance, international AI certification (IAIO), "
            "frontier oversight and cross-cultural AI ethics (cser.ac.uk)"
        ),
        "weights": {
            # MB4a Audit Independence — IAIO jurisdictional certification, evaluator/regulator independence
            "MB4a": 0.85,
            # MB6 Selection & Basin Stability — x-risk, arms-race dynamics, competitive AI development
            "MB6": 0.75,
            # MB10 Eval Gaming — FLI “Paradigms of AGI” / risk-assessment projects; eval of transformative AI
            "MB10": 0.45,
            # MB11 Deployment Safety — frontier oversight, safety standards, responsible scaling governance
            "MB11": 0.95,
        },
    },
    "recgpFFzVbWtsvCdi": {
        "rationale": (
            "Yampolskiy: AI control / corrigibility / capability vs motivational control, "
            "uncontrollability and unpredictability theses (Uncontrollability of AI; On Controllability)"
        ),
        "weights": {
            # MB2 Value Learning — “motivational control” vs capability control; alignment of goals/values
            "MB2": 0.75,
            # MB4 Corrigibility — centerpiece: shutdown/off-switch, corrigibility as control mechanism (also challenged)
            "MB4": 0.95,
            # MB6 Selection & Basin Stability — existential-risk framing; uncontrollable ASI as systemic failure
            "MB6": 0.5,
            # MB7 Inner Alignment — unpredictability of internal optimization; mesa-style control worries
            "MB7": 0.45,
            # MB9 Grounding Drift — unverifiability / unpredictability arguments overlap specification-trust crux
            "MB9": 0.4,
            # MB11 Deployment Safety — moratoria, partial bans, policy levers when full control fails
            "MB11": 0.55,
        },
    },
    "recXHj29OAxeP2F1M": {
        "rationale": (
            "Team Shard: shard theory — RL-shaped contextual value shards; reward design for "
            "reliable value instillation (Turner/Udell; field evidence #51 on MB2)"
        ),
        "weights": {
            # MB2 Value Learning — primary: reward functions that instill values (shard theory outer loop)
            "MB2": 0.95,
            # MB7 Inner Alignment — primary mechanistic lane: contextual shards vs intended reward (field ev. #51)
            "MB7": 0.75,
        },
    },
    "recu9yuBKbPAYgRz8": {
        "rationale": (
            "AIXI Labs: formal-agent risk models via AIXI variants and translation to real agents "
            "(aixi-labs.com)"
        ),
        "weights": {
            # MB1 Embedded Agency — idealized agents, formal decision-theoretic agency models
            "MB1": 0.9,
            # MB2 Value Learning — risk factors and mitigations framed as preference/reward structure
            "MB2": 0.6,
            # MB5 Reflective Stability — self-modifying / unbounded optimizers in formal setting
            "MB5": 0.45,
            # MB9 Grounding Drift — bridging formal models to deployed systems; specification gap
            "MB9": 0.75,
        },
    },
    "recxg7Q2L2NEFP8NV": {
        "rationale": (
            "Dovetail: foundational mathematics for the nature of AI agents (dovetail.ai)"
        ),
        "weights": {
            # MB1 Embedded Agency — primary: mathematical theory of agents and environments
            "MB1": 0.95,
            # MB2 Value Learning — some overlap via utility/representation in agent foundations
            "MB2": 0.5,
            # MB5 Reflective Stability — tiling/self-reference in formal agent theory
            "MB5": 0.6,
            # MB9 Grounding Drift — formal foundations vs real systems
            "MB9": 0.55,
        },
    },
    "rec8UWo45vym2oLBS": {
        "rationale": (
            "MAISI: Mathematical AI Safety Institute — mathematical foundations for powerful-AI safety "
            "(maisi.org)"
        ),
        "weights": {
            # MB1 Embedded Agency — formal models of agency under mathematical safety programme
            "MB1": 0.7,
            # MB2 Value Learning — preference/utility formalization threads
            "MB2": 0.5,
            # MB9 Grounding Drift — flagship: mathematical foundations, verification, specification
            "MB9": 0.95,
            # MB10 Eval Gaming — formal eval and measurement foundations (secondary)
            "MB10": 0.4,
        },
    },
    "recop5s8QpZlOHzkT": {
        "rationale": (
            "Paradigm 3: science of evals, near-term transformative-AI evidence, differential development "
            "(paradigm3.org)"
        ),
        "weights": {
            # MB6 Selection & Basin Stability — differential development, competitive dynamics
            "MB6": 0.55,
            # MB7 Inner Alignment — empirical eval of deceptive/scheming behavior (secondary)
            "MB7": 0.45,
            # MB10 Eval Gaming — primary: eval science, forgeability, measurement protocols
            "MB10": 0.95,
            # MB11 Deployment Safety — evidence for near-term TAI deployment decisions
            "MB11": 0.7,
        },
    },
    "recucg98qMKaCWj0G": {
        "rationale": (
            "CARMA: interdisciplinary global AI risk management; policy and technical research "
            "(carma.org)"
        ),
        "weights": {
            # MB4a Audit Independence — regulator/evaluator independence in global risk management
            "MB4a": 0.65,
            # MB6 Selection & Basin Stability — systemic x-risk and competitive deployment pressures
            "MB6": 0.7,
            # MB11 Deployment Safety — primary: global AI risk management and governance
            "MB11": 0.9,
        },
    },
    "rec3oqODxzqGFwo7y": {
        "rationale": (
            "GCRI: Global Catastrophic Risk Institute — existential-risk scholarship and policy "
            "(gcrinstitute.org)"
        ),
        "weights": {
            # MB6 Selection & Basin Stability — primary: existential / global catastrophic risk framing
            "MB6": 0.85,
            # MB11 Deployment Safety — real-world decision-making for risk reduction
            "MB11": 0.75,
        },
    },
    "rec1XEk9LnTSTvpvN": {
        "rationale": (
            "Forethought: navigating the transition to superintelligent AI (forethought.org)"
        ),
        "weights": {
            # MB2 Value Learning — alignment and values under superintelligence transition
            "MB2": 0.7,
            # MB6 Selection & Basin Stability — transition dynamics, disempowerment trajectories
            "MB6": 0.8,
            # MB7 Inner Alignment — scheming/deception under advanced systems
            "MB7": 0.5,
            # MB11 Deployment Safety — preparedness and governance for superintelligent transition
            "MB11": 0.75,
        },
    },
    "recbT1xoUenprVP5I": {
        "rationale": (
            "Narrow Path: ControlAI policymaker proposals for surviving artificial superintelligence "
            "(controlai.org/narrow-path)"
        ),
        "weights": {
            # MB4a Audit Independence — oversight and certification proposals in policy package
            "MB4a": 0.5,
            # MB6 Selection & Basin Stability — ASI race dynamics, pause/standards advocacy cluster
            "MB6": 0.8,
            # MB11 Deployment Safety — primary: deployment governance and survival-oriented policy
            "MB11": 0.95,
        },
    },
    "recIOkOheFHYAMbAp": {
        "rationale": (
            "Partnership on AI: multi-stakeholder AI safety and governance convening (partnershiponai.org)"
        ),
        "weights": {
            # MB4a Audit Independence — shared audit/eval norms across industry and civil society
            "MB4a": 0.55,
            # MB10 Eval Gaming — shared eval practices and responsible-release frameworks
            "MB10": 0.45,
            # MB11 Deployment Safety — primary: deployment governance and societal outcomes
            "MB11": 0.7,
        },
    },
    "rec1JabBvTzkHKqwA": {
        "rationale": (
            "GPAI: Global Partnership on AI — OECD-aligned international trustworthy-AI governance"
        ),
        "weights": {
            # MB4a Audit Independence — international certification and oversight norms
            "MB4a": 0.6,
            # MB6 Selection & Basin Stability — geopolitical AI development and race dynamics
            "MB6": 0.5,
            # MB11 Deployment Safety — primary: human-centric deployment governance
            "MB11": 0.8,
        },
    },
}

TYPE_MULT = {"T": 1.0, "D": 1.0, "E": 0.8, "S": 0.8, "P": 0.8, "C": 0.5, "O": 0.3}


def direction_mult(direction: str | None) -> float:
    if direction in ("support", "challenge"):
        return 1.0
    return 0.1


def fetch_organizations() -> list[dict]:
    url = "https://aisafety.com/api/v1/organizations"
    with urllib.request.urlopen(url, timeout=60) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    return payload["data"]


def parse_clustering_names(clustering: list[dict]) -> dict[str, str | None]:
    """Map normalized listing name -> agenda slug (or None if not an agenda)."""
    name_to_slug: dict[str, str | None] = {}

    for row in clustering:
        slug = row.get("rollsUpSlug")
        labels: list[str] = []
        for link in row.get("listingLinks") or []:
            if link.get("label"):
                labels.append(link["label"])
        text = row.get("listings") or ""
        for match in re.finditer(r"\[([^\]]+)\]", text):
            labels.append(match.group(1))
        for part in re.split(r",(?![^[]*\])", text):
            part = re.sub(r"\[[^\]]+\]\([^)]+\)", "", part).strip()
            part = re.sub(r"https?://\S+", "", part).strip()
            if part and not part.startswith("**"):
                labels.append(part)

        for label in labels:
            norm = normalize_name(label)
            if not norm or not name_tokens(norm):
                continue
            name_to_slug[norm] = slug

    return name_to_slug


STOP_TOKENS = {"the", "of", "and", "for", "a", "an", "at", "to", "in", "on", "aka"}


def normalize_name(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^\w\s&/-]", "", s)
    return s


def name_tokens(s: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", s.lower()) if t and t not in STOP_TOKENS]


def label_match_kind(key: str, name: str) -> str | None:
    """Exact or token match. Never treat 'arc' as a substring of 'research'."""
    kn = normalize_name(key)
    nn = normalize_name(name)
    if not kn or not nn:
        return None
    if kn == nn:
        return "exact"
    kt = name_tokens(kn)
    nt = name_tokens(nn)
    if not kt or not nt:
        return None
    if len(kt) == 1:
        token = kt[0]
        if token in nt and 2 <= len(token) <= 12:
            return "fuzzy"
        return None
    if all(t in nt for t in kt):
        return "fuzzy"
    nsig = [t for t in nt if len(t) > 1]
    if len(nsig) >= 2 and all(t in kt for t in nsig):
        return "fuzzy"
    return None


def match_agenda(org: dict, name_to_slug: dict[str, str | None]) -> tuple[str | None, str]:
    candidates = [
        org.get("title") or "",
        org.get("shortName") or "",
        org.get("tooltipTitle") or "",
    ]
    best: tuple[str | None, str, int] = (None, "none", -1)
    for raw in candidates:
        if not raw:
            continue
        for key, slug in name_to_slug.items():
            kind = label_match_kind(key, raw)
            if not kind:
                continue
            score = 1000 + len(key) if kind == "exact" else len(name_tokens(key)) * 10 + len(key)
            if score > best[2]:
                best = (slug, kind, score)
    return best[0], best[1]


def load_evidence_by_id(evidence_rows: list[dict]) -> dict[int, dict]:
    return {row["id"]: row for row in evidence_rows}


def agenda_weight_vectors(
    matrix_rows: list[dict],
    evidence_by_id: dict[int, dict],
) -> dict[str, dict]:
    """slug -> { weights, provenance per bridge }"""
    result: dict[str, dict] = {}

    for row in matrix_rows:
        slug = row.get("slug")
        if not slug:
            continue
        weights = {b: 0.0 for b in LIVE_BRIDGES}
        provenance: dict[str, list[dict]] = {b: [] for b in LIVE_BRIDGES}

        for bridge, cells in (row.get("cells") or {}).items():
            if bridge not in LIVE_BRIDGES or not cells:
                continue
            total = 0.0
            for cell in cells:
                ctype = cell.get("type", "O")
                for eid in cell.get("ids") or []:
                    ev = evidence_by_id.get(eid)
                    if not ev:
                        continue
                    w = ev.get("weight") or 0.3
                    contrib = w * TYPE_MULT.get(ctype, 0.3) * direction_mult(ev.get("direction"))
                    total += contrib
                    tagged = set(ev.get("bridges") or [])
                    provenance[bridge].append({
                        "evidenceId": eid,
                        "type": ctype,
                        "direction": ev.get("direction"),
                        "weight": w,
                        "contrib": round(contrib, 4),
                        "summary": (ev.get("evidence") or "")[:120],
                        "evidenceBridges": sorted(tagged),
                        "tagMismatch": bool(tagged) and bridge not in tagged,
                    })
            weights[bridge] = min(1.0, total)

        result[slug] = {"weights": weights, "provenance": provenance}

    return result


def heuristic_weights(org: dict, bridge_meta: list[dict]) -> tuple[dict[str, float], str]:
    text = " ".join(
        filter(None, [org.get("title"), org.get("description"), org.get("category")])
    ).lower()

    category = (org.get("category") or "").lower()
    scores = {b: 0.0 for b in LIVE_BRIDGES}

    keyword_map: dict[str, list[str]] = {
        "MB1": ["embedded agency", "embedded agents", "agent-environment", "cartesian boundary"],
        "MB2": ["value learning", "cirl", "inverse reinforcement", "preference learning", "outer alignment"],
        "MB3": ["moral patient", "whose values", "value referent", "extrapolated volition"],
        "MB4": ["corrigib", "off-switch", "off switch", "shutdown problem", "interruptibility"],
        "MB4a": ["audit independence", "regulator capture", "evaluator independence"],
        "MB5": ["tiling agents", "vingean", "reflective stability", "ontology identification"],
        "MB6": ["goodhart", "gradual disempowerment", "selection pressure", "deployment ecology", "basin stability"],
        "MB7": ["inner alignment", "scheming", "deceptive alignment", "alignment faking", "mesa-optim"],
        "MB7d": ["acausal", "logical decision", "evidential cooperation", "superrational"],
        "MB9": ["grounding drift", "specification gaming", "guaranteed safe", "safeguarded ai", "formal verification"],
        "MB10": ["eval gaming", "forgeability", "successor audit", "checklist gaming", "sandbagging"],
        "MB11": ["safety case", "responsible scaling", "deployment safety", "pre-deployment eval"],
    }

    for bridge, keywords in keyword_map.items():
        hits = sum(1 for kw in keywords if kw in text)
        if hits:
            scores[bridge] = min(1.0, 0.15 * hits)

    if "governance" in category or "advocacy" in category:
        scores["MB6"] = max(scores["MB6"], 0.35)
        scores["MB11"] = max(scores["MB11"], 0.3)
    if "empirical" in category or "capabilities" in category:
        scores["MB7"] = max(scores["MB7"], 0.25)
    if "conceptual" in category:
        scores["MB1"] = max(scores["MB1"], 0.15)
        scores["MB2"] = max(scores["MB2"], 0.15)
    if "forecast" in category:
        scores["MB6"] = max(scores["MB6"], 0.2)
    if "funding" in category or "career" in category or "blog" in category:
        for b in LIVE_BRIDGES:
            scores[b] *= 0.3

    for bridge_row in bridge_meta:
        key = bridge_row.get("key")
        if key not in LIVE_BRIDGES:
            continue
        noun = (bridge_row.get("noun") or "").lower()
        if noun and len(noun) >= 8 and noun in text:
            scores[key] = max(scores[key], 0.4)

    top = max(scores.values()) if scores else 0
    rationale = f"Heuristic keyword/category match (top={top:.2f})"
    return scores, rationale


def logo_extension(url: str) -> str:
    path = url.split("?", 1)[0].lower()
    for ext in (".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif"):
        if path.endswith(ext):
            return ext
    if ".svg" in path:
        return ".svg"
    return ".png"


def download_logos(orgs: list[dict], listings: list[dict]) -> int:
    LOGOS_DIR.mkdir(parents=True, exist_ok=True)
    org_by_id = {o.get("id"): o for o in orgs}
    downloaded = 0
    for listing in listings:
        org = org_by_id.get(listing["id"]) or {}
        url = org.get("mapLogo") or org.get("logo")
        if not url:
            continue
        ext = logo_extension(url)
        local_name = f"{listing['id']}{ext}"
        local_path = LOGOS_DIR / local_name
        listing["mapLogoUrl"] = url
        if not local_path.exists():
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "towards-asi-alignment-demo/1.0"})
                with urllib.request.urlopen(req, timeout=30) as resp:
                    local_path.write_bytes(resp.read())
                downloaded += 1
            except Exception as exc:
                print(f"  logo skip {listing['title'][:40]}: {exc}")
                continue
        listing["logoLocal"] = f"logos/{local_name}"
    return downloaded


def resolve_matrix_slug(slug: str | None, agenda_vectors: dict) -> str | None:
    if not slug:
        return None
    if slug in agenda_vectors:
        return slug
    collapsed = slug.replace("--", "-")
    if collapsed in agenda_vectors:
        return collapsed
    return None
    dot = sum(a[k] * b[k] for k in LIVE_BRIDGES)
    na = math.sqrt(sum(a[k] ** 2 for k in LIVE_BRIDGES))
    nb = math.sqrt(sum(b[k] ** 2 for k in LIVE_BRIDGES))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--llm", action="store_true", help="Use OpenAI for unmatched (requires OPENAI_API_KEY)")
    parser.add_argument("--remap-existing", action="store_true", help="Re-score listings already in snapshot.json (no API fetch)")
    parser.add_argument("--out", type=Path, default=OUT_PATH)
    args = parser.parse_args()

    prev_by_id: dict[str, dict] = {}
    if args.remap_existing:
        print("[1/4] Reusing listings from existing snapshot …")
        prev = json.loads(args.out.read_text(encoding="utf-8"))
        orgs = []
        for listing in prev.get("listings") or []:
            prev_by_id[listing["id"]] = listing
            orgs.append({
                "id": listing.get("id"),
                "title": listing.get("title"),
                "shortName": listing.get("shortName"),
                "description": listing.get("description"),
                "category": listing.get("category"),
                "status": listing.get("status"),
                "link": listing.get("link"),
                "scale": listing.get("scale"),
                "x": listing.get("mapX"),
                "y": listing.get("mapY"),
            })
        print(f"  {len(orgs)} listings")
    else:
        print("[1/4] Fetching organizations from aisafety.com …")
        orgs = fetch_organizations()
        print(f"  {len(orgs)} listings")

    print("[2/4] Loading field YAML …")
    clustering = yaml.safe_load((FIELD_DATA / "clustering.yml").read_text())["clustering"]
    matrix_doc = yaml.safe_load((FIELD_DATA / "matrix.yml").read_text())
    evidence_doc = yaml.safe_load((FIELD_DATA / "evidence.yml").read_text())
    bridges_doc = yaml.safe_load((FIELD_DATA / "bridges.yml").read_text())

    name_to_slug = parse_clustering_names(clustering)
    evidence_by_id = load_evidence_by_id(evidence_doc.get("evidence") or evidence_doc)
    agenda_vectors = agenda_weight_vectors(matrix_doc.get("rows") or [], evidence_by_id)

    bridge_labels = {
        b["key"]: b.get("noun") or b["key"]
        for b in bridges_doc.get("bridges") or []
        if b.get("key") in LIVE_BRIDGES
    }

    print("[3/4] Assigning crux weights …")
    listings = []
    matched = 0
    inherited = 0
    heuristic = 0

    for org in orgs:
        slug, match_kind = match_agenda(org, name_to_slug)
        override_slug = LISTING_AGENDA_OVERRIDES.get(org.get("id") or "")
        if override_slug:
            slug = override_slug
            match_kind = "override"
        matrix_slug = resolve_matrix_slug(slug, agenda_vectors)
        source = "unmatched"
        weights = {b: 0.0 for b in LIVE_BRIDGES}
        provenance: dict = {}
        rationale = ""

        manual = LISTING_WEIGHT_OVERRIDES.get(org.get("id") or "")

        if matrix_slug:
            matched += 1
            source = "inherited"
            inherited += 1
            weights = dict(agenda_vectors[matrix_slug]["weights"])
            provenance = {
                "agendaSlug": matrix_slug,
                "clusterSlug": slug,
                "matchKind": match_kind,
                "bridgeEvidence": agenda_vectors[matrix_slug]["provenance"],
            }
        elif manual:
            source = "manual"
            weights = {b: float(manual["weights"].get(b, 0.0)) for b in LIVE_BRIDGES}
            provenance = {"rationale": manual["rationale"]}
        else:
            weights, rationale = heuristic_weights(org, bridges_doc.get("bridges") or [])
            if max(weights.values()) > 0.05:
                source = "heuristic"
                heuristic += 1
            provenance = {"rationale": rationale}

        listings.append({
            "id": org.get("id"),
            "title": org.get("title") or org.get("shortName") or "Untitled",
            "shortName": org.get("shortName"),
            "description": org.get("description") or "",
            "category": org.get("category") or "",
            "status": org.get("status") or "",
            "link": org.get("link") or "",
            "scale": org.get("scale"),
            "mapX": org.get("x"),
            "mapY": org.get("y"),
            "source": source,
            "agendaSlug": matrix_slug or slug,
            "weights": {k: round(v, 4) for k, v in weights.items()},
            "provenance": provenance,
        })

    print(f"  matched={matched} inherited={inherited} heuristic={heuristic} unmatched={len(orgs)-matched-heuristic}")

    mismatches = []
    for listing in listings:
        be = (listing.get("provenance") or {}).get("bridgeEvidence") or {}
        for bridge, evs in be.items():
            for ev in evs:
                if ev.get("tagMismatch"):
                    mismatches.append((listing.get("agendaSlug"), bridge, ev.get("evidenceId")))
    if mismatches:
        print(f"  matrix cells citing evidence not tagged for that bridge: {len(mismatches)}")
        shown = sorted(set(mismatches))
        for row in shown[:20]:
            print(f"    {row[0]} {row[1]} evidence #{row[2]}")
        if len(shown) > 20:
            print(f"    … {len(shown) - 20} more")

    if args.remap_existing:
        print("[4/4] Keeping existing logos …")
        for listing in listings:
            prev = prev_by_id.get(listing["id"]) or {}
            for key in ("logoLocal", "mapLogoUrl"):
                if prev.get(key):
                    listing[key] = prev[key]
        logo_count = sum(1 for l in listings if l.get("logoLocal"))
        print(f"  {logo_count} logos retained")
    else:
        print("[4/5] Downloading map logos …")
        logo_new = download_logos(orgs, listings)
        logo_count = sum(1 for l in listings if l.get("logoLocal"))
        print(f"  {logo_count} logos on disk ({logo_new} newly fetched)")

    snapshot = {
        "meta": {
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "source": "https://aisafety.com",
            "license": "CC-BY-4.0",
            "licenseUrl": "https://creativecommons.org/licenses/by/4.0/",
            "attribution": "AISafety.com",
            "listingCount": len(listings),
            "bridgeKeys": LIVE_BRIDGES,
            "note": "Weights are field-evidence inheritance or heuristic scores — not bridge discharge.",
        },
        "bridges": bridge_labels,
        "listings": listings,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[5/5] Wrote {args.out} ({args.out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
