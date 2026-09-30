#!/usr/bin/env python3
"""Match Gunnar LW corpus against TSA matching lexicon; emit JSON + markdown report."""

from __future__ import annotations

import argparse
import html
import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MIN_SCORE = 3
MIN_ALIAS_HITS = 1  # or total score >= MIN_SCORE


@dataclass
class Concept:
    slug: str
    title: str
    kind: str  # concept, bridge, standalone, theme, subsumption
    chapters: list[str] = field(default_factory=list)
    bridges: list[str] = field(default_factory=list)
    card_slug: str = ""
    terms: dict[str, int] = field(default_factory=dict)  # term -> weight


@dataclass
class Hit:
    term: str
    weight: int
    slug: str


@dataclass
class DocMatch:
    doc_type: str
    url: str
    timestamp: str
    title: str
    post_url: str | None
    score: int
    alias_hits: int
    concepts: list[str]
    bridges: list[str]
    chapters: list[str]
    hit_terms: dict[str, list[str]]
    excerpt: str


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def parse_field(line: str, key: str) -> str:
    m = re.search(rf"\|{key}:([^|]+)", line)
    return m.group(1).strip() if m else ""


def add_term(concept: Concept, term: str, weight: int) -> None:
    term = term.strip()
    if not term or len(term) < 3:
        return
    if term.startswith("http") or term.startswith("/cards"):
        return
    term = re.sub(r"\\[^ ]+", "", term)  # drop latex fragments
    term = term.strip("[]()")
    if len(term) < 3:
        return
    prev = concept.terms.get(term.lower(), 0)
    concept.terms[term.lower()] = max(prev, weight)


def slug_phrase(slug: str) -> str:
    return slug.replace("-", " ")


def load_lexicon(path: Path) -> tuple[dict[str, Concept], dict[str, str]]:
    """Return concepts by slug and chapter titles."""
    concepts: dict[str, Concept] = {}
    chapter_titles: dict[str, str] = {}

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("TSA "):
            continue
        if line.startswith("CH|"):
            parts = line.split("|", 2)
            if len(parts) >= 3:
                chapter_titles[parts[1]] = parts[2]
            continue
        if line.startswith("C|"):
            parts = line.split("|")
            if len(parts) < 4:
                continue
            slug, kind, title = parts[1], parts[2], parts[3]
            claim = parts[4] if len(parts) > 4 else ""
            chapters_raw = parts[5] if len(parts) > 5 else ""
            chapters = [c.strip() for c in chapters_raw.split(",") if c.strip().startswith("ch")]
            c = Concept(slug=slug, title=title, kind=kind, chapters=chapters, card_slug=slug)
            if claim.startswith("C-"):
                pass
            for alias in parse_field(line, "ALIAS").split(","):
                add_term(c, alias, 3)
            for kw in parse_field(line, "KW").split(","):
                add_term(c, kw, 1)
            add_term(c, title, 2)
            add_term(c, slug_phrase(slug), 2)
            concepts[slug] = c
            continue
        if line.startswith("MB|"):
            parts = line.split("|")
            if len(parts) < 5:
                continue
            bridge_id, noun, card_slug = parts[1], parts[2], parts[3]
            slug = card_slug
            c = concepts.get(slug) or Concept(
                slug=slug, title=f"{bridge_id} — {noun}", kind="bridge", card_slug=slug
            )
            c.kind = "bridge"
            c.bridges = sorted(set(c.bridges + [bridge_id]))
            add_term(c, noun, 3)
            add_term(c, bridge_id, 2)
            add_term(c, slug_phrase(slug), 2)
            crux = parse_field(line, "CRUX")
            for chunk in re.split(r"[,;]", crux):
                add_term(c, chunk, 2)
            concepts[slug] = c
            continue
        if line.startswith("SC|"):
            parts = line.split("|", 2)
            if len(parts) >= 3:
                slug, summary = parts[1], parts[2]
                c = Concept(slug=slug, title=slug.replace("-", " ").title(), kind="standalone", card_slug=slug)
                add_term(c, slug_phrase(slug), 3)
                for w in summary.split():
                    if len(w) > 5:
                        add_term(c, w, 1)
                concepts[slug] = c
            continue
        if line.startswith("S|"):
            # S|subsumption-elk|→correction-channel-integrity,MB2 readout slice|ALIAS:...
            m = re.match(r"S\|([^|]+)\|→([^|]+)\|ALIAS:(.+)", line)
            if not m:
                continue
            sub_slug, targets, aliases = m.group(1), m.group(2), m.group(3)
            target_slugs = re.findall(r"[a-z0-9-]+", targets.split(",")[0])
            for tslug in target_slugs:
                if tslug not in concepts:
                    continue
                for alias in aliases.split(","):
                    add_term(concepts[tslug], alias, 3)
            continue
        if line.startswith("T|"):
            # theme row: T|id|aliases|target_slugs
            parts = line.split("|")
            if len(parts) < 4:
                continue
            theme_id, alias_blob, targets = parts[1], parts[2], parts[3]
            c = Concept(slug=f"theme-{theme_id}", title=theme_id.replace("-", " "), kind="theme")
            for alias in alias_blob.split(","):
                add_term(c, alias, 3)
            concepts[c.slug] = c
            for tslug in targets.split(","):
                tslug = tslug.strip()
                if tslug.endswith("*"):
                    tslug = tslug[:-1]
                if tslug in concepts:
                    c.chapters = sorted(set(c.chapters + concepts[tslug].chapters))
                    c.bridges = sorted(set(c.bridges + concepts[tslug].bridges))
            continue

    # Link bridge ids on concept slugs starting with mb
    for slug, c in list(concepts.items()):
        if slug.startswith("mb") and not c.bridges:
            m = re.match(r"mb(\d+[a-z]?)", slug)
            if m:
                c.bridges = [f"MB{m.group(1).upper()}" if not m.group(1)[-1].isalpha() else f"MB{m.group(1)}"]

    return concepts, chapter_titles


def find_hits(text: str, concepts: dict[str, Concept]) -> tuple[list[Hit], dict[str, list[str]]]:
    lower = text.lower()
    hits: list[Hit] = []
    by_slug: dict[str, list[str]] = defaultdict(list)

    for slug, concept in concepts.items():
        for term, weight in concept.terms.items():
            if len(term) < 4 and term.upper() != term:
                continue
            pattern = re.escape(term)
            if re.search(rf"\b{pattern}\b", lower):
                hits.append(Hit(term=term, weight=weight, slug=slug))
                by_slug[slug].append(term)

    return hits, by_slug


def excerpt_around(text: str, term: str, radius: int = 140) -> str:
    idx = text.lower().find(term.lower())
    if idx < 0:
        return text[:280] + ("..." if len(text) > 280 else "")
    start = max(0, idx - radius)
    end = min(len(text), idx + len(term) + radius)
    snippet = text[start:end].strip()
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet = snippet + "..."
    return snippet


def match_document(
    doc: dict,
    doc_type: str,
    concepts: dict[str, Concept],
) -> DocMatch | None:
    body = strip_html(doc.get("body") or "")
    title = strip_html(doc.get("title") or "")
    searchable = f"{title}. {body}"
    if len(searchable) < 20:
        return None

    hits, by_slug = find_hits(searchable, concepts)
    if not hits:
        return None

    slug_scores: dict[str, int] = defaultdict(int)
    slug_alias: dict[str, int] = defaultdict(int)
    for h in hits:
        slug_scores[h.slug] += h.weight
        if h.weight >= 3:
            slug_alias[h.slug] += 1

    qualifying = [
        s for s, sc in slug_scores.items() if sc >= MIN_SCORE or slug_alias[s] >= MIN_ALIAS_HITS
    ]
    if not qualifying:
        return None

    qualifying.sort(key=lambda s: slug_scores[s], reverse=True)
    total_score = sum(slug_scores[s] for s in qualifying)
    alias_hits = sum(slug_alias[s] for s in qualifying)

    all_chapters: set[str] = set()
    all_bridges: set[str] = set()
    for s in qualifying:
        c = concepts[s]
        all_chapters.update(c.chapters)
        all_bridges.update(c.bridges)

    best_term = hits[0].term
    for h in sorted(hits, key=lambda x: -x.weight):
        if h.slug == qualifying[0]:
            best_term = h.term
            break

    return DocMatch(
        doc_type=doc_type,
        url=doc.get("url") or "",
        timestamp=doc.get("timestamp") or "",
        title=title or "(no title)",
        post_url=doc.get("post_url"),
        score=total_score,
        alias_hits=alias_hits,
        concepts=qualifying,
        bridges=sorted(all_bridges),
        chapters=sorted(all_chapters, key=lambda x: int(x[2:])),
        hit_terms={s: sorted(set(by_slug[s])) for s in qualifying},
        excerpt=excerpt_around(searchable, best_term),
    )


def render_report(
    matches: list[DocMatch],
    concepts: dict[str, Concept],
    chapter_titles: dict[str, str],
    corpus_counts: dict[str, int],
) -> str:
    posts = [m for m in matches if m.doc_type == "post"]
    comments = [m for m in matches if m.doc_type == "comment"]
    by_concept: dict[str, list[DocMatch]] = defaultdict(list)
    by_chapter: dict[str, list[DocMatch]] = defaultdict(list)

    for m in matches:
        for slug in m.concepts:
            by_concept[slug].append(m)
        for ch in m.chapters:
            by_chapter[ch].append(m)

    lines = [
        "# LessWrong → TSA match report",
        "",
        "Scans `gunnar_zarncke_lw_content.json` against `tsa_matching_lexicon.txt`.",
        "Purpose: locate your prior LW prose linkable to manuscript chapters and concept cards.",
        "**No manuscript edits** — inventory only.",
        "",
        "## Summary",
        "",
        f"- Corpus: {corpus_counts['posts']} posts, {corpus_counts['comments']} comments",
        f"- Matched: {len(posts)} posts ({100*len(posts)/max(corpus_counts['posts'],1):.0f}%), "
        f"{len(comments)} comments ({100*len(comments)/max(corpus_counts['comments'],1):.0f}%)",
        f"- Distinct concepts hit: {len(by_concept)}",
        f"- Chapters with ≥1 hit: {len(by_chapter)}",
        "",
        "## Top concepts by hit count",
        "",
        "| Concept / card | Hits | Chapters | Bridges |",
        "|---|---:|---|---|",
    ]

    for slug, docs in sorted(by_concept.items(), key=lambda x: -len(x[1]))[:40]:
        c = concepts.get(slug)
        title = c.title if c else slug
        ch = ", ".join(c.chapters[:4]) if c and c.chapters else "—"
        br = ", ".join(c.bridges[:3]) if c and c.bridges else "—"
        lines.append(f"| [{title}](/cards/{slug}/) (`{slug}`) | {len(docs)} | {ch} | {br} |")

    lines.extend(["", "## Style-rich posts (high concept density)", ""])
    post_rank = sorted(posts, key=lambda m: (m.score, len(m.concepts)), reverse=True)
    for m in post_rank[:25]:
        cards = ", ".join(f"`{s}`" for s in m.concepts[:6])
        ch = ", ".join(m.chapters[:5]) or "—"
        lines.extend([
            f"### {m.title}",
            f"- **URL:** {m.url}",
            f"- **Date:** {m.timestamp[:10] if m.timestamp else '?'}",
            f"- **Score:** {m.score} | **Concepts:** {cards}",
            f"- **Chapters:** {ch}",
            f"- **Matched terms:** {', '.join(t for s in m.concepts[:3] for t in m.hit_terms.get(s, [])[:4])}",
            f"- **Excerpt:** {m.excerpt}",
            "",
        ])

    lines.extend(["", "## By chapter", ""])
    for ch in sorted(by_chapter.keys(), key=lambda x: int(x[2:])):
        docs = by_chapter[ch]
        title = chapter_titles.get(ch, ch)
        post_n = sum(1 for d in docs if d.doc_type == "post")
        com_n = len(docs) - post_n
        lines.append(f"### {ch} — {title}")
        lines.append(f"*{len(docs)} items ({post_n} posts, {com_n} comments)*")
        lines.append("")
        seen_urls: set[str] = set()
        shown = 0
        for m in sorted(docs, key=lambda x: (-x.score, x.timestamp)):
            if m.url in seen_urls:
                continue
            seen_urls.add(m.url)
            kind = "post" if m.doc_type == "post" else "comment"
            cards = ", ".join(f"`{s}`" for s in m.concepts[:4])
            lines.append(
                f"- [{kind}] [{m.title[:70]}]({m.url}) ({m.timestamp[:10]}) — "
                f"score {m.score}; {cards}"
            )
            shown += 1
            if shown >= 15:
                lines.append(f"- *…and {len(seen_urls) - 15} more URLs in JSON*")
                break
        lines.append("")

    lines.extend(["", "## By concept card (all matches)", ""])
    for slug in sorted(by_concept.keys()):
        c = concepts.get(slug)
        title = c.title if c else slug
        docs = sorted(by_concept[slug], key=lambda x: (-x.score, x.timestamp))
        lines.append(f"### `{slug}` — {title}")
        if c and c.chapters:
            lines.append(f"Chapters: {', '.join(c.chapters)}")
        if c and c.bridges:
            lines.append(f"Bridges: {', '.join(c.bridges)}")
        lines.append("")
        for m in docs[:20]:
            kind = "post" if m.doc_type == "post" else "comment"
            terms = ", ".join(m.hit_terms.get(slug, [])[:5])
            lines.append(
                f"- [{kind}] [{m.title[:60]}]({m.url}) ({m.timestamp[:10]}) "
                f"score={m.score} terms=[{terms}]"
            )
        if len(docs) > 20:
            lines.append(f"- *+{len(docs)-20} more*")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--lexicon",
        type=Path,
        default=ROOT / "data/lesswrong/tsa_matching_lexicon.txt",
    )
    parser.add_argument(
        "--corpus",
        type=Path,
        default=ROOT / "data/lesswrong/gunnar_zarncke_lw_content.json",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        default=ROOT / "data/lesswrong/lw_tsa_matches.json",
    )
    parser.add_argument(
        "--report-out",
        type=Path,
        default=ROOT / "data/lesswrong/lw_tsa_match_report.md",
    )
    args = parser.parse_args()

    concepts, chapter_titles = load_lexicon(args.lexicon)
    corpus = json.loads(args.corpus.read_text(encoding="utf-8"))

    matches: list[DocMatch] = []
    for post in corpus.get("posts", []):
        m = match_document(post, "post", concepts)
        if m:
            matches.append(m)
    for comment in corpus.get("comments", []):
        m = match_document(comment, "comment", concepts)
        if m:
            matches.append(m)

    matches.sort(key=lambda x: (-x.score, x.timestamp))

    payload = {
        "summary": {
            "posts_total": len(corpus.get("posts", [])),
            "comments_total": len(corpus.get("comments", [])),
            "posts_matched": sum(1 for m in matches if m.doc_type == "post"),
            "comments_matched": sum(1 for m in matches if m.doc_type == "comment"),
            "concepts_hit": len({s for m in matches for s in m.concepts}),
        },
        "matches": [
            {
                "type": m.doc_type,
                "url": m.url,
                "timestamp": m.timestamp,
                "title": m.title,
                "post_url": m.post_url,
                "score": m.score,
                "concepts": m.concepts,
                "bridges": m.bridges,
                "chapters": m.chapters,
                "hit_terms": m.hit_terms,
                "excerpt": m.excerpt,
            }
            for m in matches
        ],
    }

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report = render_report(
        matches,
        concepts,
        chapter_titles,
        {
            "posts": payload["summary"]["posts_total"],
            "comments": payload["summary"]["comments_total"],
        },
    )
    args.report_out.write_text(report, encoding="utf-8")

    s = payload["summary"]
    print(f"Matched {s['posts_matched']}/{s['posts_total']} posts, "
          f"{s['comments_matched']}/{s['comments_total']} comments")
    print(f"Wrote {args.json_out}")
    print(f"Wrote {args.report_out}")


if __name__ == "__main__":
    main()
