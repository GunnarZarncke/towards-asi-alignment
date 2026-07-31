# 2026-06-18 — Chapter 11 boundary expansion draft

## Trigger
User provided a full draft for chapter 11 and asked to integrate it into `chapters/ch11-capability-without-task-ontology.tex`, following project instructions and context.

## Done
- Replaced stub chapter with integrated draft: epigraph, chapter thesis, 22 sections (including subsections), five growth modes, expansion-correction ratio, operational checklist, stop/start/continue criteria, failure modes, formal summary, key definitions, BibLaTeX references.
- Fixed LaTeX from draft source: `\MI` for mutual information, subscript `*` artifacts, table row endings, align line breaks, `\left\{`/`\right\}`, prose math delimiters.
- Adjusted opening to bridge from Chapter 10 (strategic opacity) and foreshadowed competence measure in Chapter 7.
- Renamed duplicate label `sec:conserved-properties` → `sec:conserved-properties-capability-growth` (conflicted with ch08).
- Updated `metadata/book.yml` ch11 title and status (`draft`, ~5600 words).
- `./build.sh` succeeds; PDF now 339 pages.

## Decisions
- Used draft title **Capability Growth Is Boundary Expansion** in `\chapter{}` (matches draft content; previously book.yml listed this as ch12 and ch11 as "Measuring Capability Without Task Ontology").
- Left `ch12-boundary-expansion.tex` stub unchanged; ch11/ch12 title overlap is now an explicit open item.
- Converted manual reference list to `\autocite{}` block matching ch08/ch10 pattern (Ashby 1956 not in bib; cited via Conant–Ashby regulator theorem).

## Open / next
- Resolve ch11 vs ch12 scope: either draft ch12 "Measuring Capability Without Task Ontology" or retire/merge the ch12 stub.
- Sync `INSTRUCTIONS.md` chapter list and `frontmatter/roadmap.tex` if chapter titles/order change.
- Optional: add "What Would Change This View" section per other drafted chapters.

## Key paths
- `chapters/ch11-capability-without-task-ontology.tex`
- `metadata/book.yml`
- `dist/pdf/towards-superintelligence-alignment.pdf`
