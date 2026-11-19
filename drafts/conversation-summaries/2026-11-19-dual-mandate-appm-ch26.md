# 2026-11-19 — Dual-mandate pattern (App M, Ch 26)

kind: new-work
uptake: status

## Trigger
User asked to center the build-authority plus uncapped-claim problem in App M (not a news card or App C), generalize dual-mandate beyond Ch. 34, add East India Company sourcing, cite Plan R as untested remedy; then shorten EIC prose and simplify Ch. 26 paragraph. End of session: commit.

Prompts: (paraphrase-only; no prompt id in telemetry)

## Done
- content: App M `sec:appm-dual-mandate` restructured into three founding forms (promote/regulate; check/paid by checked; build/uncapped claim) with shortened EIC flagship; frontier-firm instance + `\textcite{roko2026planr}`; table row and appendix references updated.
- content: Ch. 26 plain-language `\mathrm{ValidRef}` founding-failure paragraph after coordinate table; pointer to App M.
- content: Ch. 34 removed build-authority section and revenue-channel pointer; one sentence in internal-alignment block points to App M third form.
- content: Bib `stern2011companystate`, `dalrymple2019anarchy` (`references/institutional-histories.bib`); `roko2026planr` (`references/external-alignment.bib`); matching `\bibsummary` lines.
- housekeeping: Session log, HANDOFF, INDEX.
- gate: `make check` passed — citations pass (533 cited); bibliography summaries pass (593/593); claim spine pass.

## Decisions
- Pattern lives in App M; Ch. 26 states institutional principle only (not model-scale grader-knowledge as ValidRef founding failure).
- Plan R: no field-news card; cited as untested structural remedy in App M only.
- Ch. 34 specialization rolled back in favor of App M home.

## Open / next
- Site concept `metadata/concepts/bodies/institutional-dual-mandate-genesis.md` still uses old two-case framing; update when user asks.
- Score-4 LW scan candidates remain in `drafts/lw-scan-report-2026-09-19-to-2026-11-19.md`.

## Key paths
- `appendices/appM-institutional-histories.tex` (`sec:appm-dual-mandate`)
- `chapters/ch26-correction-channel-integrity.tex`
- `references/institutional-histories.bib`

## Commits
- `311e889ef2` Generalize dual-mandate genesis in App M and Ch. 26.