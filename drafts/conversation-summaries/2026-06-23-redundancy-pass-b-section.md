# 2026-06-23 — Redundancy pass (fix-plans §B)

## Trigger
Execute redundancy fixes from `review/fix-plans-2026-06-22.md` §B (all items except B5 self-modeling preview creep), remove unused `decisionbox` env documentation, add TODO to review the conjectural U-shape claim.

## Done
- **B1** — ch28: conserved-property subsections replaced with named preview of ch29's seven; ch31: certification class aligned to same seven + competence/successor as audit checks.
- **B2** — CEV contrast deduped: ch24/25/27/42 → reminder or simple-ref to ch26; ch41 kept add-context CEV section.
- **B3** — Legitimacy criteria: ch04/ch27/ch42 trimmed to refs + chapter-specific add-ons; ch41 keeps substrate-awareness only beyond ch26.
- **B4** — ch23 successor laundering → ch37 cross-ref; ch36 four-stage laundering → simple-ref to ch37 layers/GLI.
- **B7** — ch11 collective-competence + U-shape compressed; forward-ref to ch13 (`sec:mid-scale-collapse`).
- **B8** — ch28 eight-claim safety case → preview pointing to ch31 ten-claim schema.
- **B9** — Local-first: canonical ch32; ch31/ch34/ch35 reduced to clause + ref.
- **B11** — Named callbacks: helpful-lie (ch20 home), recommender + frontier-lab → ch09, ch21/ch24/ch27 updated.
- **B12** — ch12/ch42 Conclusion+Summary merged to `\section{Summary}`; ch23 front summary dropped, tail renamed Summary, `eq:transport-stack` moved to opening of transport section.
- **Misc** — `INSTRUCTIONS.md` box-env list trimmed to `chapterthesis` only (preamble already clean); `metadata/TODO.md` U-shape review item added.
- **B5** — ch10 preview + `eq:opacity-preview-ch10`; ch06/08/12/14/22/25/28/29 trimmed to forward-refs; ch30 unchanged as home.
- **Build** — `./build.sh` clean after `sec:mid-scale-collapse` ref fix and B5 pass.

## Decisions
- **B5 (follow-up)** — ch30 home; ch10 sole pre-ch30 preview (includes $\tau = 1 - \MI(M;\hat{M})/H(M)$ as `eq:opacity-preview-ch10`); ch06/08/12/14/22/25/28/29 → minimal forward-refs to ch10 § + ch30.
- **B5 skipped (initial)** per user: self-modeling / τ preview creep deferred for discussion (resolved above).
- **Helpful-lie home** — ch20 kept as canonical labeled instance (fix-plan said ch04 but ch04 has no full worked case).
- **U-shape** — explicitly marked *conjectural* in ch11 forward-ref; full treatment remains ch13; TODO added for claim-strength review.

## Open / next
- ~~**B5** — Discuss whether τ/self-transparency previews should move earlier…~~ **Done 2026-06-23:** ch10 preview (with `eq:opacity-preview-ch10`); ch30 home; ch06/08/12/14/22/25/28/29 minimal forward-refs.
- **U-shape TODO** — empirical backing or uncertainty-ledger downgrade.
- **§C9** — ch36 stages vs ch37 layers still open in fix-plans (B4 home reconciliation).
- **§A** — formula re-derivation pass still open.

## Key paths
- `chapters/ch11-capability-without-task-ontology.tex`, ch28/29/31, ch04/24/25/27/41/42, ch23/36, ch12/20/21/24/27/34/35`
- `metadata/TODO.md`, `INSTRUCTIONS.md`

## Commits
None (user did not request commit).
