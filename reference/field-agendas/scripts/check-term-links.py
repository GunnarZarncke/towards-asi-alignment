#!/usr/bin/env python3
"""Validate term-links.yml: existence + semantic match of phrase → URL targets.

Usage:
  python3 reference/field-agendas/scripts/check-term-links.py
  python3 reference/field-agendas/scripts/check-term-links.py --no-network
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
TERM_LINKS = REPO / "reference" / "field-agendas" / "data" / "term-links.yml"
CARDS_DIR = REPO / "site" / "src" / "content" / "cards"
GLOSSARY = REPO / "site" / "src" / "data" / "glossary.json"

# Phrase → slug when target is a deliberate alias (cousin term, not exact title).
ALIAS_OK = {
    ("adversarial verifiability", "certification-under-manipulation"),
    ("certification under manipulation", "certification-under-manipulation"),
    ("deceptive alignment", "strategic-opacity"),
    ("alignment faking", "strategic-opacity"),
    ("conserved properties", "successor-stability"),
    ("successor stability", "successor-stability"),
    ("successor", "successor-stability"),
    ("bearer map", "bearer-persistence"),
    ("bearer persistence", "bearer-persistence"),
    ("value bundle", "value-bundle-transport"),
    ("correction channel", "correction-channel-integrity"),
    ("Goodhart as selector", "goodhart-as-selector"),
    ("Goodhart Selection", "mb6-selection-and-basin-stability"),
    ("selection environment", "attractor-control"),
    ("alignment basin", "attractor-control"),
    ("deployment leverage", "attractor-control"),
    ("human simulator", "subsumption-elk"),
    ("direct translator", "subsumption-elk"),
    ("latent knowledge", "subsumption-elk"),
    ("scalable alignment", "subsumption-debate"),
    ("amplification", "subsumption-debate"),
    ("debate", "subsumption-debate"),
    ("recursive reward modeling", "subsumption-debate"),
    ("shutdown", "subsumption-shutdown"),
    ("ontology identification", "mb5-successor-ontology-shift"),
    ("Agent", "agent-without-anthropomorphism"),
    ("AI safety", "field"),
    ("glossary", "glossary"),
}

# External URLs that are org homepages / index pages (phrase won't appear in title).
ORG_HOME_OK = {
    "https://www.redwoodresearch.org/",
    "https://www.apolloresearch.ai/",
    "https://www.apolloresearch.ai/research",
    "https://www.alignmentforum.org/users/John+Wentworth",
    "https://www.alignmentforum.org/users/vanessa-kosoy",
    "https://intelligence.org/",
    "https://www.anthropic.com/research",
    "https://metr.org/",
    "https://longtermrisk.org/",
    "https://www.cooperativeai.com/",
    "https://www.conjecture.dev/",
    "https://www.meaningalignment.org/",
    "https://www.goodfire.com/",
    "https://www.neuronpedia.org/",
    "https://www.transluce.org/",
    "https://apartresearch.com/",
    "https://bluedot.org/",
    "https://www.matsprogram.org/",
    "https://humancompatible.ai/",
    "https://truthful.ai/",
    "https://www.far.ai/",
    "https://ae.studio/alignment",
    "https://ciris.ai/architecture/",
    "https://epoch.ai/",
    "https://www.metaculus.com/",
    "https://pauseai.info/",
    "https://controlai.org/",
    "https://sparai.org/",
    "https://pathfinder.kairos-project.org/",
    "https://www.globalchallengesproject.org/",
    "https://www.timaeus.ai/",
    "https://lawzero.org/en",
    "https://pascal-berrang.de/projects/zk_ai_security/",
    "https://heron.ing/aarm",
    "https://aria.org.uk/opportunity-spaces/mathematics-for-safe-ai/safeguarded-ai",
    "https://github.com/GunnarZarncke/agency-detect",
}


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower().strip())


def slug_from_url(url: str) -> str | None:
    m = re.match(r"^/cards/([^/]+)/?$", url)
    if m:
        return m.group(1)
    if url.rstrip("/") in ("/field", "/glossary"):
        return url.strip("/").split("/")[-1]
    return None


def load_card_index() -> dict[str, dict]:
    idx: dict[str, dict] = {}

    concepts = yaml.safe_load((REPO / "metadata/concepts.yml").read_text())
    for c in concepts.get("concepts", []):
        slug = c["slug"]
        body = ""
        body_path = REPO / "metadata/concepts/bodies" / c.get("body", f"{slug}.md").split("/")[-1]
        if body_path.exists():
            body = body_path.read_text()[:4000]
        idx[slug] = {
            "title": c.get("title", slug),
            "summary": c.get("summary", ""),
            "agenda": "",
            "headline": "",
            "body": body,
            "kind": c.get("kind", "concept"),
        }

    bridges = yaml.safe_load((REPO / "metadata/bridges.yml").read_text())
    for b in bridges.get("bridges", []):
        slug = b["slug"]
        body_path = REPO / "metadata/concepts/bodies" / b.get("body", "").split("/")[-1]
        body = body_path.read_text()[:4000] if body_path.exists() else ""
        idx[slug] = {
            "title": b.get("title", slug),
            "summary": b.get("summary", ""),
            "agenda": b.get("fieldCrux", ""),
            "headline": "",
            "body": body,
            "kind": "bridge",
        }

    index = yaml.safe_load((REPO / "metadata/bridges.yml").read_text())
    idx_entry = index.get("index")
    if idx_entry:
        slug = idx_entry["slug"]
        body_path = REPO / "metadata/concepts/bodies" / idx_entry.get("body", "").split("/")[-1]
        body = body_path.read_text()[:4000] if body_path.exists() else ""
        idx[slug] = {
            "title": idx_entry.get("title", slug),
            "summary": idx_entry.get("summary", ""),
            "agenda": "",
            "headline": "",
            "body": body,
            "kind": "bridge",
        }

    bridge_nouns = yaml.safe_load((REPO / "reference/field-agendas/data/bridges.yml").read_text())
    for b in bridge_nouns.get("bridges", []):
        slug = b.get("cardSlug")
        if slug and slug in idx:
            idx[slug]["noun"] = b.get("noun", "")

    projections = yaml.safe_load((REPO / "metadata/projections.yml").read_text())
    for p in projections.get("projections", []):
        slug = p["slug"]
        body_path = REPO / "metadata/concepts/bodies" / p.get("body", "").split("/")[-1]
        body = body_path.read_text()[:4000] if body_path.exists() else ""
        idx[slug] = {
            "title": p.get("title", slug),
            "summary": p.get("summary", ""),
            "agenda": p.get("agenda", ""),
            "headline": p.get("headline", ""),
            "body": body,
            "kind": "projection",
        }

    glossary = json.loads(GLOSSARY.read_text())
    for g in glossary:
        slug = g["slug"]
        if slug not in idx:
            idx[slug] = {"title": g["term"], "summary": g.get("definition", ""), "body": "", "kind": "glossary-only"}
        idx[slug].setdefault("glossary_terms", []).append(g["term"])

    return idx


def phrase_in_text(phrase: str, *texts: str) -> bool:
    p = norm(phrase)
    blob = norm(" ".join(t for t in texts if t))
    if p in blob:
        return True
    # Allow hyphen/space variants
    p2 = p.replace("-", " ")
    if p2 in blob:
        return True
    # Acronym in title (ELK, CIRL, etc.)
    if phrase.isupper() and len(phrase) <= 6:
        return phrase.lower() in blob or phrase in " ".join(texts)
    # Substantial word overlap for multi-word phrases
    words = [w for w in re.split(r"[\s/-]+", p) if len(w) > 3]
    if len(words) >= 2:
        hits = sum(1 for w in words if w in blob)
        if hits >= max(2, len(words) - 1):
            return True
    return False


def check_internal(phrase: str, url: str, idx: dict) -> tuple[str, str]:
    slug = slug_from_url(url)
    if slug in ("field", "glossary"):
        page = REPO / "site/src/pages" / slug / "index.astro"
        if not page.exists() and slug == "field":
            page = REPO / "site/src/content/field/intro.md"
        if not page.exists():
            return "missing", f"page not found for {url}"
        if (phrase, slug) in ALIAS_OK or phrase.lower() in ("field hub", "ai safety", "glossary"):
            return "ok", "hub page"
        return "ok", "hub page"

    card_path = CARDS_DIR / f"{slug}.md"
    if slug not in idx:
        return "missing", f"unknown card slug {slug!r} (no metadata; file={card_path.exists()})"
    if not card_path.exists():
        return "warn", f"card slug in metadata but no generated file {card_path.name} (run sync)"

    meta = idx[slug]
    if (phrase, slug) in ALIAS_OK:
        return "ok", "deliberate alias"

    texts = [meta.get("title", ""), meta.get("summary", ""), meta.get("agenda", ""), meta.get("headline", ""), meta.get("noun", ""), meta.get("body", "")]
    texts.extend(meta.get("glossary_terms", []))

    if phrase_in_text(phrase, *texts):
        return "ok", meta.get("title", slug)

    # Bridge noun exact match
    noun = meta.get("noun", "")
    if noun and norm(phrase) == norm(noun):
        return "ok", f"bridge noun {noun!r}"

    return "mismatch", f"phrase not found in card {slug!r} ({meta.get('title', '')[:60]})"


def fetch_url(url: str, timeout: int = 15) -> tuple[int | None, str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "term-links-check/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read(120_000)
            ctype = resp.headers.get("Content-Type", "")
            text = raw.decode("utf-8", errors="replace")
            title = ""
            m = re.search(r"<title[^>]*>([^<]+)</title>", text, re.I)
            if m:
                title = re.sub(r"\s+", " ", m.group(1)).strip()
            return resp.status, title, text[:8000]
    except urllib.error.HTTPError as e:
        try:
            body = e.read(2000).decode("utf-8", errors="replace")
        except Exception:
            body = ""
        return e.code, "", body
    except Exception as e:
        return None, "", str(e)


def check_external(phrase: str, url: str, use_network: bool) -> tuple[str, str]:
    if url in ORG_HOME_OK:
        if use_network:
            status, title, _ = fetch_url(url)
            if status and 200 <= status < 400:
                return "ok", f"org/index ({status}) {title[:50]}"
            if status:
                return "broken", f"HTTP {status}"
            return "warn", "network error (org homepage assumed ok offline)"
        return "ok", "org/index (offline)"

    if not use_network:
        return "skip", "network disabled"

    status, title, body = fetch_url(url)
    if status is None:
        return "warn", f"fetch failed: {body[:80]}"
    if status >= 400:
        return "broken", f"HTTP {status}"

    blob = norm(f"{title} {body}")
    p = norm(phrase)

    if p in blob or phrase.lower() in blob:
        return "ok", title[:70] or f"HTTP {status}"

    # arXiv: match id
    m = re.search(r"arxiv\.org/abs/(\d+\.\d+)", url)
    if m:
        aid = m.group(1)
        if aid in body or aid.replace(".", "") in blob:
            return "ok", f"arXiv {aid} ({title[:50]})"

    # LessWrong / AF: slug words
    words = [w for w in re.split(r"[\s/-]+", p) if len(w) > 3]
    if words:
        hits = sum(1 for w in words if w in blob)
        if hits >= max(1, len(words) - 1):
            return "ok", title[:70] or "keyword match"

    # Same URL used for multiple related phrases (intentional)
    if url in {
        "https://arxiv.org/abs/2405.06624",
        "https://www.lesswrong.com/posts/d9FJHawgkiMSPjagR/ai-control-improving-safety-despite-intentional-subversion",
    }:
        if any(w in blob for w in words[:3]):
            return "ok", title[:70] or "related content bundle"

    return "mismatch", f"phrase not in page title/body ({title[:60]})"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-network", action="store_true")
    args = ap.parse_args()
    use_network = not args.no_network

    terms = yaml.safe_load(TERM_LINKS.read_text())["terms"]
    idx = load_card_index()

    by_url: dict[str, list] = {}
    for t in terms:
        by_url.setdefault(t["url"], []).append(t["phrase"])

    results = {"ok": [], "warn": [], "mismatch": [], "missing": [], "broken": [], "skip": []}

    seen_url_phrase = set()
    for t in terms:
        phrase = t["phrase"]
        url = t["url"]
        key = (phrase, url)
        if key in seen_url_phrase:
            continue
        seen_url_phrase.add(key)

        if url.startswith("/"):
            status, detail = check_internal(phrase, url, idx)
        else:
            status, detail = check_external(phrase, url, use_network)

        results[status].append((phrase, url, detail))

    print(f"term-links.yml: {len(terms)} entries, {len(seen_url_phrase)} unique phrase→URL pairs\n")

    for status in ("broken", "missing", "mismatch", "warn", "skip"):
        items = results[status]
        if not items:
            continue
        print(f"## {status.upper()} ({len(items)})")
        for phrase, url, detail in items:
            print(f"  [{phrase}] → {url}")
            print(f"    {detail}")
        print()

    ok = len(results["ok"])
    print(f"OK: {ok}")
    print(f"WARN: {len(results['warn'])}  MISMATCH: {len(results['mismatch'])}  MISSING: {len(results['missing'])}  BROKEN: {len(results['broken'])}")

    if results["broken"] or results["missing"] or results["mismatch"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
