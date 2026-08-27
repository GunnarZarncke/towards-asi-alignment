# 2026-08-28 — Project identity, not manuscript-first

## Trigger
User: README still leads with “research manuscript”; the project is no longer only or primarily a manuscript.

## Done
- Recast README opener to match the Preface: knowledge base and roadmap; book is the long-form argument among Lean, experiments, field map, papers, demos, and site.
- Renamed “Manuscript at a glance” → “Project at a glance.”
- Same identity on CONTRIBUTING, AGENTS.md, `llms.txt`, site About heading, OG alt text.
- Synced `site/public/llms.txt` and `llms-full.txt`.
- `INSTRUCTIONS.md`: this file governs the book; project identity is `README.md`.
- PDF Current Status companion-site sentence: orientation layer for the project, not “the book’s materials.”

## Decisions
- Used the Preface’s own phrase (“knowledge base and roadmap”) rather than inventing a new project genre label.
- `INSTRUCTIONS.md` stays book-scoped; a scope note points agents at `README.md` for project identity.
- `REVIEWING_FOR_AGENTS.md` stays manuscript-scoped (reviewing the book).

## Open / next
- GitHub About / description is outside the repo; check if it still says “research manuscript.”
- Left uncommitted (other sessions): `drafts/plans/construct.md` (Scaling Trust note), `site/src/data/chapter-reading-graph.json` (timestamp).

## Key paths
- `README.md`
- `frontmatter/preface.tex` (source of the knowledge-base framing)

## Commits
- `6af8c1ff` Present TSA as a knowledge base and roadmap, not a manuscript-first project.
