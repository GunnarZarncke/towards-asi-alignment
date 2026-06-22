# 2026-06-22 — Citation/reference-section conformance pass

## Trigger
User wanted a uniform reference style across all chapters: inline `\autocite` where a source is directly referenced + a short per-chapter related-work summary + a per-chapter sub-bibliography. Asked to audit all chapters (table), then bring every non-conforming chapter up to the standard and check whether thin-inline chapters need more inline cites.

## Done
- Audited all 44 chapters (inline-cite count, summary-paragraph presence, `printbib`, `refsection`, distinct refs). Target pattern met by 35; deviations fixed below.
- ch01, ch02: added the missing related-work **summary paragraph** before `\printbibliography` (they already had inline cites + refsection). Summaries wired only to keys each chapter already cites.
- ch40: added the missing `\begin{refsection}...\end{refsection}` wrapper (it had inline cites + summary + printbib but no refsection, so its sub-bibliography was not chapter-scoped).
- ch33: wrapped in `refsection`; added inline cites (`hamilton1964genetical` at the cooperativity index; `wang2013percolation,zarncke2025attractor` at percolation; `zarncke2025acausal` at the ICI/acausal-coordination definition); replaced the `\section*{Chapter References}` TODO block with a real summary paragraph + `\printbibliography`.
- ch05, ch39, ch43, ch44 (stubs): added `refsection` + short summary paragraph + `\printbibliography`, wiring the keys named in each chapter's `% TODO(deep-research)` note (all keys verified to exist).
- ch13 (only genuinely under-cited chapter inline): added 3 inline cites — `salge2014empowerment` + `zarncke2025biq,zarncke2025uad` at the local-competence measure; `hamilton1964genetical` at the `κ_ij` index; `goodhart1984problems,manheim2018goodhart` at metric substitution.
- Build: `./build.sh` exits 0 after each batch; no lint errors; no undefined-reference or duplicate-label warnings.
- Re-ran audit: all 44 chapters now have `refsection` + summary + `printbib`.

## Decisions
- Did NOT force inline cites into ch06/ch12/ch17/ch19/ch21: counting *distinct keys* (not `\autocite` calls) they already have 4–6 inline; their summary-only keys are legitimate background/related-work. Over-citing would violate the project's "don't over-cite" guidance. Only ch13 was genuinely thin inline (2 keys) and got fixed.
- Matched the canonical pattern exactly (ch03 as reference): `\section*{Chapter References}` + prose + `\printbibliography[heading=subbibliography,title={Chapter References}]` inside `refsection`.
- Used internal `zarncke2025acausal` for ch33's acausal-coordination cite; no external superrationality/open-source-game-theory key exists in the bib (did not invent one).

## Open / next
- Stub chapters ch39/ch43/ch44 (and ch05/ch33 bodies) still need prose; their reference sections are now in place but short. As bodies are drafted, move background keys into inline cites at the relevant claims.
- Optional: external acausal-trade / superrationality references (Hofstadter, Oesterheld, open-source game theory) are not in the bib; add if ch33 is expanded.
- Not committed (no commit requested).

## Key paths
- `chapters/ch01,ch02,ch05,ch13,ch33,ch39,ch40,ch43,ch44`
- canonical pattern reference: `chapters/ch03-dynamical-guarantee.tex` (tail)

## Commits
- none
