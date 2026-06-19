# 2026-06-18 — Session end: Part III drafts, citations, structure fixes

## Trigger
User ended session after Part III chapter file correction (ch12 = boundary expansion, ch13 = coordination bottleneck per INSTRUCTIONS).

## Done this session (cumulative)

### Manuscript drafts
- **ch11** — restored to stub (*Measuring Capability Without Task Ontology*); boundary-expansion content moved to ch12.
- **ch12** — *Capability Growth Is Boundary Expansion* draft (~1,240 lines); opening bridge from ch11; conclusion bridge to ch13.
- **ch13** — *The Coordination Bottleneck* draft (~1,050 lines); label `ch:coordination-bottleneck`.
- **ch14** — *When Intelligence Deepens Misalignment* draft (~1,000 lines); added `Why This Matters`, `What Would Change This View`, `Summary` per INSTRUCTIONS §10.

### Source map & citations
- `metadata/source-canon.md` — deep-research report mapped to chapters.
- `references/*.bib` — 16+ new entries; surgical cites in drafted ch03–ch12, ch40; `TODO(deep-research)` in stubs.
- `context/towards-asi-alignment-deep-research-report.md` — untracked input (not committed).

### Metadata
- `metadata/book.yml` — ch11 stub, ch12/ch13/ch14 draft titles and status aligned with INSTRUCTIONS.
- `tables/chapter-map.tex` — ch12–ch14 status updated to draft.

### Build
- `./build.sh` succeeds. Pre-existing multiply-defined labels: `sec:self-modeling-transparency`, `sec:example-helpful-assistant`.

## Decisions
- Part III filenames unchanged; content placed per INSTRUCTIONS chapter numbers (not per mistaken integration targets).
- ch11 measurement chapter deferred; ch12 assumes ch11 will supply task-agnostic competence measure.
- No git commit this session (user did not request).

## Open / next
1. **Draft ch11** — Measuring Capability Without Task Ontology (BIQ / boundary competence formalization).
2. **ch12/ch13** — add `What Would Change This View` if full §10 parity with ch03/ch08/ch14 desired.
3. **Duplicate labels** — resolve `sec:self-modeling-transparency` and `sec:example-helpful-assistant` across chapters.
4. **ch13 reserved stub** — IDE may show stale 12-line buffer; on-disk file is full draft (reload if needed).
5. **Commit** — large unstaged tree: Part III chapters, bib, source-canon, stub TODO blocks, conversation logs; exclude LaTeX aux/pdf and untracked deep-research report unless user wants it in repo.

## Key paths
- `chapters/ch11-capability-without-task-ontology.tex` (stub)
- `chapters/ch12-boundary-expansion.tex` (draft)
- `chapters/ch13-coordination-bottleneck.tex` (draft)
- `chapters/ch14-intelligence-deepens-misalignment.tex` (draft)
- `metadata/book.yml`, `metadata/source-canon.md`
- `INSTRUCTIONS.md` §10, Part III list (lines 606–609)

## Commits
- (none)
