#!/usr/bin/env python3
"""Generate a dense TSA concept lexicon for matching against external text (e.g. LW dump)."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONCEPTS_DIR = ROOT / "metadata/concepts/bodies"
STOPWORDS = frozenset(
    "a an the and or but if in on at to for of is are was were be been being "
    "that this which what when where who how not only also into from with as by "
    "it its their they them we you your our can may will would should could ask "
    "before after whether than then into over under about through".split()
)

# Field-term → TSA slug (subsumption + crosswalk). Dense alias layer for LW matching.
SUBSUMPTION: dict[str, list[str]] = {
    "subsumption-embedded-agency": [
        "embedded agency",
        "Demski-Garrabrant",
        "Cartesian box",
        "agent-environment cut",
        "markov blanket",
        "real optimizer",
        "subsystem",
    ],
    "subsumption-elk": [
        "ELK",
        "elicit latent knowledge",
        "reporter",
        "simulator",
        "naive oversight",
        "latent readout",
    ],
    "subsumption-cirl": [
        "CIRL",
        "cooperative IRL",
        "cooperative inverse reinforcement learning",
        "assistance game",
        "Hadfield-Menell",
        "deference",
        "inquiry",
    ],
    "subsumption-corrigibility": [
        "Christiano corrigibility",
        "dynamical corrigibility",
        "corrigibility theater",
        "amplification",
        "basin contraction",
    ],
    "subsumption-shutdown": [
        "shutdown",
        "off-switch",
        "Soares corrigibility",
        "shutdownability",
        "Thornley",
        "interrupt",
    ],
    "subsumption-interruptibility": [
        "safe interruptibility",
        "Orseau",
        "kill switch",
        "interrupt neutrality",
    ],
    "subsumption-debate": [
        "debate",
        "scalable oversight",
        "amplification",
        "HCH",
        "iterated amplification",
        "Irving debate",
        "judge error",
    ],
    "subsumption-hidden-biq": [
        "inner alignment",
        "deceptive alignment",
        "mesa-optimizer",
        "alignment faking",
        "scheming",
        "hidden capability",
        "AI control",
        "Hubinger",
    ],
    "subsumption-grounding-drift": [
        "grounding drift",
        "conservative abstraction",
        "GSAI",
        "open agency",
        "proof-carrying code",
        "nonrealizability",
        "misspecification",
    ],
    "subsumption-deployment-gate": [
        "safety case",
        "deployment safety",
        "regret bound",
        "episode battery",
        "eval-to-deployment",
    ],
    "subsumption-low-impact": [
        "AUP",
        "attainable utility preservation",
        "relative reachability",
        "low impact",
        "side effect",
    ],
    "subsumption-quantilization": [
        "quantilization",
        "quantilizer",
        "optimizer's curse",
        "Goodhart under optimization",
    ],
    "subsumption-selection-basin": [
        "Goodhart selection",
        "gradual disempowerment",
        "multipolar",
        "lock-in",
        "alignment tax",
        "race dynamics",
    ],
}

# Gunnar / project-specific terms likely in LW corpus
AUTHOR_TERMS: dict[str, list[str]] = {
    "unsupervised-agent-discovery": [
        "UAD",
        "unsupervised agent discovery",
        "agency-detect",
        "agent discovery",
        "boundary discovery",
    ],
    "neglected-approaches": [
        "neglected approaches",
        "AE Studio alignment",
        "many shots on goal",
        "AI Safety Interventions",
    ],
    "brain-like-agi": [
        "brain-like AGI",
        "Brain-Like AGI Safety",
        "Byrnes",
        "steve byrnes",
    ],
    "inferential-coupling": [
        "acausal trade",
        "ECL",
        "evidential cooperation",
        "program equilibrium",
        "FDT",
        "superrationality",
    ],
}

GUNNAR_LW_THEMES = """
# GUNNAR LW THEMES (early/recurring topics → TSA slugs)
T|parenting-rationality|numerate children,bedtime stories,rationalist parenting,Adlerian,ZPD,authoritative parenting,soft paternalism|value-change-vs-corruption,correction-channel-integrity,paternalism-boundary
T|games-education|Games for Rationalists,estimation game,overconfidence,cognitive biases,serious games,edutainment|experiment-methodology,goodhart-as-selector
T|worldview-baseline|Great Filter,simulation argument,singularity skepticism,complexity limits,colonization explosion|scope-and-correction-capacity,artificial-civilization,dynamical-guarantee
T|neglected-portfolio|Neglected Approaches,AE Studio,AI Safety Interventions,many shots on goal,SOO,self-other overlap|unsupervised-agent-discovery,field-coverage
T|agency-lines|agency-detect,UAD,Unsupervised Agent Discovery,Brain-Like AGI,Byrnes,steve byrnes|boundary-discovery,unsupervised-agent-discovery,mb1-boundary-estimator-soundness
T|value-discovery|value-detect,value discovery,signature rate,two-axis map|value-bundle-transport,mb2-bundle-identifiability
T|institutional|freemasonry,community building,phyg,LessWrong exclusivity|attractor-control,institutional-*
T|forecasting|Metaculus,predictions,timelines,compute estimates|evidence-and-uncertainty,predictions markets
"""

HOMOGRAPHS = """
HOMOGRAPH|field sense|TSA sense|disambiguate with
selection|Demski inside-optimizer search|deployment ecology Goodhart selection (MB6)|socio-technical vs gradient
corrigibility|MIRI/CHAI shutdown preference|correction-channel integrity trajectory (MB4)|dynamical vs one-bit
pointing problem|field umbrella|identification vs realization vs preservation split|three questions
BIQ|graded-lab boundary quality|hidden productive BIQ bound (MB7)|experimental vs adversarial
fitness|biological|deployment growth rate Fit_E (ch34)|formula label only
Verify|CIRIS attestation|green path ≠ real-loop integrity (MB4a)|attestation vs control
"""

SPINE = """
SPINE|six thesis claims (Intro contract; ch48 status)
C-003 boundary-discovery|find real control locus before goals|MB1|boundary,UAD,composite,wrong object,ε-boundary
C-004 value-bundle-transport|values as steering directions survive transform|MB2|bundle geometry,transport layers,goal transport
C-012 grounding-viability|checked abstractions stay tied to value-relevant reality|MB9|grounding,conservativity,capture of grounding
C-005 correction-channel-integrity|human correction causally changes behavior in time|MB4,MB4a|CCI,corrigibility,capture,handles
C-006 successor-stability|copies/delegates inherit value+correction structure|MB5,MB10|tiling,successor,conserved properties,forgeability
C-007 attractor-control|deployment selection preserves or destroys alignment|MB6|selection environment,basin,Goodhart selector,leverage
SECONDARY|C-008 differential growth|C-009 transport/laundering|C-010 adversarial measurement|C-011 civilizational limit
LIFECYCLE|specify→construct→identify→certify→act/refuse↻|preserve=repeat cycle property|not fifth stage
POINTING|identification(MB2/3)|realization(ConstructionCrux ch33)|preservation(MB4/MB4a/MB6+)
"""


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_book_chapters(path: Path) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """Parse chapter/part titles without loading LaTeX-heavy YAML."""
    text = path.read_text(encoding="utf-8")
    chapters = re.findall(
        r"^\s+(ch\d+):\s*\n\s+title:\s*\"([^\"]+)\"",
        text,
        re.MULTILINE,
    )
    parts = re.findall(
        r"^\s+(part\d+):\s*\n\s+summary:\s*\"([^\"]+)\"",
        text,
        re.MULTILINE,
    )
    return chapters, parts


def compact(text: str | None, max_len: int = 220) -> str:
    if not text:
        return ""
    s = re.sub(r"\s+", " ", text.strip())
    s = s.replace("|", "/")
    if len(s) > max_len:
        return s[: max_len - 3] + "..."
    return s


def glossary_aliases(entry: dict) -> list[str]:
    terms = []
    for gt in entry.get("glossaryTerms") or []:
        if isinstance(gt, dict) and gt.get("term"):
            terms.append(gt["term"])
    if entry.get("term"):
        terms.append(entry["term"])
    return terms


def read_body_terms(slug: str, body_rel: str | None) -> tuple[str, list[str]]:
    """Return (snippet, extra terms) from concept body markdown."""
    if not body_rel:
        return "", []
    path = CONCEPTS_DIR / body_rel.replace("bodies/", "")
    if not path.is_file():
        return "", []
    raw = path.read_text(encoding="utf-8")
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        raw = parts[2] if len(parts) >= 3 else raw
    raw = raw.strip()
    snippet = compact(re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", raw), 280)
    terms: list[str] = []
    terms.extend(re.findall(r"\*\*([^*]+)\*\*", raw))
    terms.extend(re.findall(r"\[([^\]]+)\]\(", raw))
    terms.extend(re.findall(r"`([^`]+)`", raw))
    return snippet, terms[:12]


def keyword_tokens(*chunks: str) -> str:
    seen: set[str] = set()
    out: list[str] = []
    for chunk in chunks:
        for word in re.findall(r"[A-Za-z][A-Za-z0-9\-/]{2,}", chunk):
            w = word.lower()
            if w in STOPWORDS or w in seen:
                continue
            seen.add(w)
            out.append(word)
    return ",".join(out[:18])


def slug_aliases(slug: str) -> list[str]:
    out: list[str] = []
    out.extend(AUTHOR_TERMS.get(slug, []))
    for sub_slug, terms in SUBSUMPTION.items():
        core = sub_slug.replace("subsumption-", "")
        if core in slug or slug in core:
            out.extend(terms)
    if slug.startswith("mb"):
        out.append(slug.replace("-", " "))
    return out


def chapter_block(chapters: list[tuple[str, str]], parts: list[tuple[str, str]]) -> list[str]:
    lines = ["# CHAPTERS (book map; LW posts may echo themes pre-TSA)"]
    for key, title in chapters:
        lines.append(f"CH|{key}|{title}")
    lines.append("# PARTS")
    for pk, summary in parts:
        lines.append(f"PT|{pk}|{compact(summary, 200)}")
    return lines


def predictions_block(predictions: dict) -> list[str]:
    lines = ["# PREDICTION MARKETS 2027 (App P; operational bridge tests)"]
    for m in predictions.get("markets", []):
        mid = m.get("id", "")
        title = compact(m.get("title", m.get("shortQuestion", "")), 120)
        bridge = m.get("primaryBridge", "")
        lines.append(f"P|{mid}|{bridge}|{title}")
    return lines


def bridge_block(bridges_data: dict, field_bridges: dict) -> list[str]:
    lines = ["# BRIDGES (MB1–MB11; testable handoffs)"]
    field_by_key = {b["key"]: b for b in field_bridges.get("bridges", [])}
    for b in bridges_data.get("bridges", []):
        bid = b.get("id", "")
        fb = field_by_key.get(bid, {})
        noun = fb.get("noun", "")
        crux = compact(fb.get("cruxWording", b.get("fieldCrux", "")), 180)
        summary = compact(b.get("summary", ""), 200)
        decision = compact(b.get("decision", ""), 160)
        move = compact(b.get("bookMove", ""), 140)
        agendas = compact(b.get("owningAgenda", ""), 100)
        lines.append(
            f"MB|{bid}|{noun}|{b.get('slug','')}|{summary}|ASK:{decision}|FIELD:{agendas}|MOVE:{move}|CRUX:{crux}"
        )
    return lines


def concept_block(concepts_data: dict) -> list[str]:
    lines = ["# CONCEPTS (companion cards; match keywords in prose)"]
    for c in concepts_data.get("concepts", []):
        kind = c.get("kind", "concept")
        slug = c.get("slug", "")
        title = c.get("title") or c.get("term") or slug
        summary = compact(c.get("summary", ""), 200)
        decision = compact(c.get("decision", ""), 140)
        claim = c.get("claimId", "")
        chapters = ",".join(c.get("bookChapters") or [])[:40]
        body_snip, body_terms = read_body_terms(slug, c.get("body"))
        aliases = glossary_aliases(c) + slug_aliases(slug) + body_terms
        alias_str = ",".join(dict.fromkeys(a for a in aliases if a))[:240]
        kw = keyword_tokens(title, summary, decision, alias_str)
        lines.append(
            f"C|{slug}|{kind}|{title}|{claim}|{chapters}|{summary}|ASK:{decision}|ALIAS:{alias_str}|KW:{kw}|BODY:{body_snip}"
        )
    return lines


def subsumption_block() -> list[str]:
    lines = ["# SUBSUMPTION (field agenda term → TSA object)"]
    slug_to_tsa = {
        "subsumption-embedded-agency": "boundary-discovery,MB1",
        "subsumption-elk": "correction-channel-integrity,MB2 readout slice",
        "subsumption-cirl": "value-bundle-transport,MB2",
        "subsumption-corrigibility": "correction-channel-integrity,MB4",
        "subsumption-shutdown": "correction-channel-integrity,MB4",
        "subsumption-interruptibility": "correction-channel-integrity,MB4",
        "subsumption-debate": "correction-channel-integrity,MB4a",
        "subsumption-hidden-biq": "strategic-opacity,MB7",
        "subsumption-grounding-drift": "grounding-viability,MB9",
        "subsumption-deployment-gate": "target-realization,MB11",
        "subsumption-low-impact": "correction-channel-integrity",
        "subsumption-quantilization": "correction-channel-integrity",
        "subsumption-selection-basin": "attractor-control,MB6",
    }
    for slug, aliases in SUBSUMPTION.items():
        tsa = slug_to_tsa.get(slug, "")
        lines.append(f"S|{slug}|→{tsa}|ALIAS:{','.join(aliases)}")
    return lines


def standalone_block() -> list[str]:
    return [
        "# STANDALONE CLAIMS (extractable memos)",
        "SC|anti-capture-correction-validity|correction invalid when target captured reference/handles/grounding",
        "SC|bearer-map-commutation-failure|translate-then-apply ≠ apply-then-translate across ontologies",
        "SC|certification-under-manipulation|κ* threshold: honest measurand vs affordable theater",
        "SC|goodhart-as-selector|proxy-as-selector reverses conditional expectations; population shift",
    ]


def experiment_block() -> list[str]:
    return [
        "# EXPERIMENTS (Gunnar empirical lines; LW may cite)",
        "E|toy-simulation|embedded-simulation|goal-agent-simulation|lab-simulation|graded-lab-simulation",
        "E|agency-detect|UAD precursor|boundary discovery operationalized",
        "E|value-detect|value discovery|signature rates|two-axis map",
        "E|ET-1..ET-4|external-substrate transfer|frozen instrument on foreign traces",
        "E|M1-M8|methodology|preregister|blind generation|honest negatives|VFS|BIQ|EAI",
        "E|W-|backtest|weak findings",
    ]


def agenda_block() -> list[str]:
    return [
        "# FIELD AGENDAS (names in LW; see what-tsa-fails-to-represent for gaps)",
        "A|MIRI|embedded agency,tiling,CEV,real optimizer,EU maximizer",
        "A|Redwood|AI control,alignment faking,evaluator gap,scheming",
        "A|CHAI/FAR|CIRL,assistance game,value learning",
        "A|Christiano|debate,amplification,HCH,dynamical corrigibility,ELK→ARC",
        "A|ARC|ELK,reporter,sensor tampering",
        "A|davidad/GSAI|guaranteed safe,safety case,conservative abstraction,open agency",
        "A|Safeguarded AI|composite agency,machine-checkable proof",
        "A|Wentworth|natural abstractions,selection theorems,value directions",
        "A|Kosoy/LTA|infra-Bayesianism,regret,superimitation,PreDCA",
        "A|CLR|acausal trade,ECL,s-risk,inferential coupling",
        "A|Orthogonal|QACI,boundary discovery",
        "A|Anthropic|Constitutional AI,RLAIF,interpretability,circuits",
        "A|OpenAI|preparedness,weak-to-strong,process supervision,anti-scheming",
        "A|Apollo|scheming eval,deception tests",
        "A|METR|autonomous work duration,evals",
        "A|CIRIS|constitution,runtime,attestation,WA independence",
        "A|GovAI/AISI|evaluation binding,institutional",
        "A|Neglected Approaches|Gunnar,AE Studio,many shots,UAD,SOO,RLNF,BCI",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data/lesswrong/tsa_matching_lexicon.txt",
    )
    args = parser.parse_args()

    concepts = load_yaml(ROOT / "metadata/concepts.yml")
    bridges = load_yaml(ROOT / "metadata/bridges.yml")
    field_bridges = load_yaml(ROOT / "reference/field-agendas/data/bridges.yml")
    book_chapters, book_parts = load_book_chapters(ROOT / "metadata/book.yml")
    predictions_path = ROOT / "metadata/predictions.yml"
    predictions = load_yaml(predictions_path) if predictions_path.is_file() else {}

    parts: list[str] = [
        "TSA MATCHING LEXICON v1",
        "PURPOSE: dense concept index for semantic match against Gunnar_Zarncke LessWrong corpus",
        "FORMAT: TYPE|id|fields... pipe-separated; ALIAS= comma terms; ASK= decision trigger",
        "SOURCE: metadata/concepts.yml, metadata/bridges.yml, field crosswalk, subsumption cards",
        "",
        "# SPINE",
        SPINE.strip(),
        "",
    ]
    parts.extend(chapter_block(book_chapters, book_parts))
    parts.append("")
    parts.extend(bridge_block(bridges, field_bridges))
    parts.append("")
    parts.extend(concept_block(concepts))
    if predictions.get("markets"):
        parts.append("")
        parts.extend(predictions_block(predictions))
    parts.append("")
    parts.extend(subsumption_block())
    parts.append("")
    parts.extend(standalone_block())
    parts.append("")
    parts.extend(experiment_block())
    parts.append("")
    parts.extend(agenda_block())
    parts.append("")
    parts.append(GUNNAR_LW_THEMES.strip())
    parts.append("")
    parts.append("# HOMOGRAPHS (same English, different object)")
    parts.extend(HOMOGRAPHS.strip().splitlines())

    text = "\n".join(parts) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")

    chars = len(text)
    lines = text.count("\n")
    est_tokens = chars // 4
    print(f"Wrote {args.output}")
    print(f"  {lines} lines, {chars:,} chars, ~{est_tokens:,} est. tokens (chars/4)")


if __name__ == "__main__":
    main()
