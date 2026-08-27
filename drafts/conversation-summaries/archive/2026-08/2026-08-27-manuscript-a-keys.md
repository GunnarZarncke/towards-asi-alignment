# 2026-08-27 — Manuscript A-* definitions in home chapters

## Trigger

User: `A-*` keys in TeX had no reader-facing definitions. App B one-liners were too compact; ch05 mixed three assumptions awkwardly; ch43 used unexplained “correlated steerability.”

## Done

- Named `\begin{assumption}[A-00x]\label{ass:A-00x}` in fourteen home chapters with self-contained definitions.
- Dropped App B assumption-key table; `\akey{A-00x}` in preamble hyperlinks to boxed statements. Intro + A-011 footnote introduce the convention.
- ch05 **Scope Assumptions** only: boxes **A-003** and **A-005**; no **A-004** forward reference (home ch07).
- ch43: certification-under-manipulation paragraph states A-009 vs MB7b–d; removed “correlated steerability” jargon.
- Ledger homes synced; PDF rebuilt (`dist/pdf/towards-superintelligence-alignment.pdf`).

## Decisions

- No `appL-assumptions.tex`; ledger stays maintainer-only.
- ch05 owns correction capacity + deployment gating only.

## Open / next

- Optional: `\akey` remaining plain `A-00x` strings in App B note paragraphs.

## Key paths

- `chapters/ch02`, `ch03`, `ch05`, `ch07`, `ch14`, `ch16`, `ch22`, `ch26`, `ch30`, `ch34`, `ch35`, `ch43`
- `appendices/appB-bridge-crosswalk.tex`, `appendices/appG-lean-proof-spine.tex`
- `metadata/assumptions-ledger.md`, `metadata/preamble.tex`, `INSTRUCTIONS.md`, frontmatter intro/preface/overview

## Commits

- (this session)

## Not in this commit

Unrelated dirty tree: README/project-identity, site quiz/seo, construct plan, session-log archive moves — left unstaged.
