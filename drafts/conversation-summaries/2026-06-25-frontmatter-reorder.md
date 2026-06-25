# 2026-06-25 — Frontmatter reorder

## Trigger
Execute session-end plan: split argument / meta / skim; stop Introduction front-running Part I.

## Done
- **Preface:** why (knowledge base), four audiences, reading paths, authorship note (from Current Status).
- **Executive Overview:** removed stubs; filled ``What This Book Tries to Establish''; dropped duplicate roadmap (→ Navigation pointers); kept TL;DR, thesis, rejected simplifications, non-claims, doom policy, App E.
- **Introduction:** trimmed §Standard Picture and §Which Alignment to forward refs (Part I, ch1/4/9/3–32); kept hook, loop, introclaims, artifacts, shaky, how to read, hope.
- **Current Status:** WIP + chapter map only (removed why-a-book and authorship → Preface).
- `./build.sh` passes.

## Decisions
- Authorship lives in Preface only (not duplicated in Current Status).
- EO five preservation bullets kept for funder skim; Introduction uses labeled `introclaim`s (different format, same spine).
- Part roadmap remains Introduction-only.

## Open / next
- Optional: tighten EO TL;DR vs introclaims further if still feels redundant on read-through.
- ch44 opening-promise discharge when synthesis chapter is written.

## Key paths
- `frontmatter/{preface,introduction,executive-overview,current-status}.tex`

## Commits
- none (not requested)
