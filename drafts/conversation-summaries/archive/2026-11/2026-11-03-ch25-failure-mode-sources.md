# 2026-11-03 — Ch. 25 failure modes; Scott autograntor lens

kind: correction
uptake: status

## Trigger
Chapter 25 failure modes lacked external sources; user wanted standard names and one citation per mode. Thread continued with Scott Alexander's autograntor post (correction channel / tsa-on-itself parallel), LW comment draft and publish, label renames, and session close.
Prompts: paraphrase-only (no prompt id resolved).

## Done
- content: `chapters/ch25-correction-causal-channel.tex` §Failure Modes — standard names, one quoted source per mode, labels: `sec:tokenism`, `sec:evaluation-gaming`, `sec:authority-decay`, `sec:ontology-drift`, `sec:surface-compliance`, `sec:preference-capture`, `sec:successor-escape`. Authority decay (not subsection title "Gradual disempowerment") with Kulveit GD in footnote → Ch. 34 / Ch. 47. Ontology drift rewritten; successor escape cites Ch. 30. Opening preview: token correction channel → `sec:tokenism`.
- content: bib + `\bibsummary` for `arnstein1969ladder`, `carroll2024influenceable`, `schoen2025antischeming`; fixed `deblanc2011ontological` summary.
- content: Site sync (`npm run sync:chapters`, `sync:chapter-cards`) — generated `site/src/content/book/` (gitignored).
- notes: Scott autograntor mapped to LW open problems (Embedded Agency, Value Learning, Corrigibility, …); tokenism / preference capture / authority decay tied to anchor + glaze + Common Law quotes.
- housekeeping: Published LW comment archived → `context/extracts/scott-autograntor-zarncke-comment-2026-11-03.md`; `context/lw-references.md` index row.

## Decisions
- Failure-mode labels renamed with no backward compatibility (no manuscript `\ref` to old labels).
- Goodhart / proxy optimization in Scott's post discussed under user's crux names; Ch. 25 keeps **Authority decay** at channel scale, GD named only in footnote.

## Open / next
- Successor escape naming vs AI-control "escape" usage.
- Ch. 4 / Ch. 27 could cross-ref Ch. 25 cites.
- Optional: cite §The Question preview sentences (Arnstein, Carroll, etc.).

## Key paths
- `chapters/ch25-correction-causal-channel.tex`
- `context/extracts/scott-autograntor-zarncke-comment-2026-11-03.md`
- `drafts/plans/tsa-on-itself.md`

## Commits
- `4e85d1a22a` — Ch. 25 failure modes + bib (prior commit this session).
- (this session close) — LW comment extract + conversation logs.

## Verification
- `make check`: "Bibliography summary check passed (565 summaries for 565 bib keys)" (full `make check` still fails on 19 markdown links to untracked drafts elsewhere in tree).
