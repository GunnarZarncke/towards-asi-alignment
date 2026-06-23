# 2026-06-23 — Chapter epigraphs pass

## Trigger
User requested better external epigraphs at chapter starts: research 6 categories × 45 chapters, then iterative selection and LaTeX application through Ch44.

## Done
- Launched 10 part-level subagents; consolidated **270** candidate quotes into:
  - `drafts/chapter-epigraph-candidates-2026-06-23.md` (full + “why it fits”)
  - `drafts/chapter-epigraph-candidates-compact-2026-06-23.md` (one 6-row table per chapter)
  - `drafts/epigraph-data.json`
  - `drafts/epigraph-research-*.md` (10 part extracts)
- Replaced author-written `\epigraph{}` aphorisms with attributed external quotes on **Ch01–Ch44** (except **Ch39b** — unchanged).
- **Part VI** opener + **Executive Overview**: Ashby, *“Only variety can destroy variety.”*
- Notable multi-quote / special placements:
  - **Ch06** Wiener + Luhmann (*Defining a boundary does not mean isolating the system*)
  - **Ch07** Xu/Hubinger + Luhmann (*Boundary maintenance is system maintenance*)
  - **Ch09** expanded Vinge *A Fire Upon the Deep* (Tines pack-mind)
  - **Ch12** Clark & Chalmers (skin/skull counter-view)
  - **Ch17** three epigraphs (Yudkowsky, Wiener, Christiano)
  - **Ch23** Tarski Convention T (moved from mistaken Ch32 placement)
- User-driven picks for unsatisfied chapters:
  - **Ch29** von Neumann (1948) offspring/activity description copy
  - **Ch30** Nietzsche *Gay Science* §335 on “know thyself” as mockery
  - **Ch39** Gall axiom 4 (*The crucial variables are discovered by accident*)
  - **Ch42** Gall Functional Indeterminacy Theorem
- **Ch02** `\begin{quote}` → `\epigraph`; **Ch05, Ch33, Ch40, Ch43, Ch44** gained first epigraphs.
- `./build.sh` succeeds after all changes.

## Decisions
- **Ch19** Hanson forager/farmer values (not Berlin) per user unsatisfaction with scalar-pluralism quote.
- **Ch30** Nietzsche instead of Delphic maxim (user wanted “know thyself goes wrong”).
- **Ch34** Brandeis *contradicting* quote (transparency) — user choice; chapter argues selective visibility.
- **Ch39b** left with author thermometer epigraph — not in user’s final list.
- Attribution format: `\epigraph{quote}{--- Author, source (year)}` throughout.

## Open / next
- **Ch39b** epigraph still author-written; user did not specify external quote.
- Verify fragile attributions before print: podcast quotes (Dafoe, Ng), Heraclitus translation (Ch22 Kirk & Raven), Gall page numbers if needed for publisher.
- Optional: bib entries for frequently cited epigraph sources not already in `references/`.
- **Not committed** — user did not request commit; many other untracked LaTeX aux/PDF files in tree.

## Key paths
- All `chapters/ch*.tex` epigraph blocks (Ch01–Ch44)
- `parts/part06-correction-channels.tex`, `frontmatter/executive-overview.tex`
- `drafts/chapter-epigraph-candidates-compact-2026-06-23.md` (audit table)

## Commits
- None this session.
