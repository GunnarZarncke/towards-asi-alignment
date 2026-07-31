# 2026-06-30 — Frontmatter + ch01 AI slop pass

## Trigger
User asked for a surgical pass over frontmatter and chapter 1 to remove or simplify AI-slop phrasing (Paul Graham style: simpler words, no template rhetoric). End-of-session commit.

## Done
- `frontmatter/introduction.tex`: renamed "If You Remember One Thing" → "In Brief"; replaced 8× "X matters because" with term: explanation colons; cut hedged filler; simplified closing practical-hope and bridge paragraphs.
- `frontmatter/preface.tex`: "navigable source" → "structured source".
- `frontmatter/executive-overview.tex`: dropped generic "conceptual and formal framework" / "positive framework" phrasing.
- `chapters/ch01-wrong-object.tex`: removed defensive/meta slop ("philosophical decoration", "mature alignment regime", "This chapter has argued", 7× "It may be", "guardrail"); tightened boundary-discovery and chapter-close prose.

## Decisions
- Left staccato concrete lists (Some learn / It can create tools) and "Do not X only Y" decision blocks — repetitive but content-bearing, not empty template.
- Did not commit unrelated working-tree changes (ch09, dedication, experiments, other logs).

## Open / next
- Continue same slop pass on ch02+ if desired.
- Pre-existing build warnings: undefined refs `appe-assumptions`, `app:lean-proof-spine`.

## Key paths
- `frontmatter/introduction.tex`, `frontmatter/preface.tex`, `frontmatter/executive-overview.tex`
- `chapters/ch01-wrong-object.tex`

## Commits
- (this session)
