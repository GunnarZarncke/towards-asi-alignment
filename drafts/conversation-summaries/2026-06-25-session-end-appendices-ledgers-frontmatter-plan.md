# 2026-06-25 — Session end: appendices, ledgers, frontmatter plan

## Trigger
Multi-task session: glossary/appendix work, INSTRUCTIONS slim-down, notation & assumptions appendices, roadmap dedup, assumptions ledger verification, frontmatter architecture discussion. User asked to end session with frontmatter reorder plan and commit.

## Done (this session)
- **INSTRUCTIONS.md** slim-down; cross-ref updates (`AGENTS.md`, `README.md`, metadata, review scripts).
- **Appendix A:** generated notation index from `metadata/notation.md`; removed `tables/notation-table.tex`.
- **Appendix E:** assumptions index from `metadata/assumptions-ledger.md` (replaced removed successor-certification stub); A-001–A-012 + Lean S07/MB1–MB8.
- **Global bibliography:** `manuscript-citations.bib`, `generate_global_nocite.py`, `metadata/global-nocite.tex`.
- **Glossary** selection terms; **appH** research program; **appE** removed (successor certification).
- **Frontmatter:** duplicate part roadmap removed (EO + Current Status); EO Assumptions stub removed → pointer to Appendix E.
- **Roadmap:** single `part-roadmap.tex`; dropped `part-roadmap-overview.tex`.
- Session logs in `drafts/conversation-summaries/`.

## Decisions
- Notation & assumptions: single markdown source → generated LaTeX index (like chapter tables).
- Assumptions: stated in chapters, collated in Appendix E; scope gate in ch05.
- Frontmatter duplication is intentional only where audiences differ (see plan below).

## Next session — frontmatter reorder (do not start until authorized)

**Goal:** Split *argument* vs *meta* vs *skim*; stop Introduction front-running Part I.

### Target structure

```text
Preface           — why / who / reading paths (expand stub)
Executive Overview — funder skim: TL;DR, thesis, rejected simplifications,
                     non-claims, doom-as-checklist, assumptions → App E
Introduction      — orientation only: hook, loop, five introclaims (promises),
                     progress artifacts, shaky points, how to read, practical hope
Current Status    — WIP, authorship, chapter status table only
```

### Edits to plan

| Action | Source | Target |
|--------|--------|--------|
| Expand | `current-status.tex` §Why this is a book | **Preface** (short) |
| Add | audience routing (researcher / engineer / funder / generalist) | **Preface** |
| Keep | TL;DR, thesis, rejected simplifications, doom policy, App E pointer | **Executive Overview** |
| Trim | §Standard Picture (five complications) to ~½ page + forward refs ch1, ch4 | **Introduction** |
| Trim | §Which Alignment? to pointer ch1/ch9 | **Introduction** |
| Keep | `introclaim` blocks, artifacts, shaky, how to read, practical hope | **Introduction** |
| Remove | any re-list of five preservation Qs in Intro if redundant with `introclaim`s | **Introduction** |
| Do not duplicate | part roadmap | **Introduction only** (EO/Status → pointers) |

### Verification after frontmatter pass
- `./build.sh`; check Intro + Part I read without repeated reframing blocks.
- Update `metadata/TODO.md` opening-promise reconciliation when ch44 lands.

## Open / next
- Execute frontmatter plan above (next session).
- Optional: discharge EO stubs (Diagram in Words, What This Book Tries to Establish).

## Key paths
- `frontmatter/{preface,introduction,executive-overview,current-status}.tex`
- `metadata/assumptions-ledger.md`, `appendices/appE-assumptions.tex`
- `metadata/notation.md`, `appendices/appA-notation.tex`

## Commits
- `4b84ad1` — Add generated appendices, global bibliography, and slim project instructions.
