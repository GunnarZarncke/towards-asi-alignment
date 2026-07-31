# Agent handoff (conversation summaries)

**Read this first** when resuming work. Then `metadata/book.yml` and `metadata/TODO.md` for tasks. Git history and [RECOVERY.md](RECOVERY.md) recover deleted session logs.

Last compressed: 2026-07-31.

---

## Open work (load-bearing)

- **CIRIS composite / boundary_decouple counterexample** — Eric-facing key task: Verify+Lens can read green while WA-blind composite fails (named-identity bet vs real intervening unit). Charter: `~/repos/ciris/review/findings/2026-07-30-key-task-composite-boundary-counterexample.md`. Reuse: toy T-9 `boundary_decouple`, lab LS-28, MB1/composite-agency cards. Pointer: `experiments/TODO.md`.
- **Correlated steerability chokepoint** — WWCTV surfaces share adversarial-verifiability antecedent; disjunctive MB6b/MB8 routes may be one failure point. Formalized in `Chokepoint.lean`; still need per-chapter WWCTV forward refs and U-ledger reconciliation. Pointer: `metadata/TODO.md` BIG REVIEW.
- **Conserved-property forgeability (MB10)** — finite counterexample in Lean; prose wired. Still open: non-enumerability of conserved set across capability jumps; toy red-team of audit forgeability. Pointer: `metadata/TODO.md`, `Forgeability.lean`.
- **Terminology demotion follow-through** — plain-first vocabulary audit (deployment leverage, preservation conditions, etc.). Pointer: `metadata/TODO.md`; demotion source log retired → RECOVERY `2026-07-08-glossary-terminology-demotion`.
- **Measurand instantiation table** — composite indices bottom out in deferred estimators; needs mapping to experiment scripts. Pointer: `review/adversarial-steerability-correlated-failure-2026-06-30.md`.
- **Presentation / site-first** — de-center PDF as flagship; per-part display renumbering (high risk). Pointer: `metadata/TODO.md` § Presentation.

## Recently shipped (Jul 2026 themes)

- **Manuscript:** Ch. 17 cites Africa/Irving thousand-dimensional persona structure (with hedges vs control-rank). App. B links MIRI agent-foundations writeups on bridge rows. App. C note on MIRI hard-pause vs Plan A spectrum. AI 2040 Plan A surgical cites + news card.
- **Companion site:** Field-news layer (`metadata/field-news.yml`); “Read more in” chapter footers; RSS; offline PWA; link-type indicators; concept logos; experiment findings UX (`**Key finding:**` extraction).
- **Experiments:** ET-1 Orbit line **stopped** (passive UAD detects scripted macro-agent; channel independence). ET-2 CIL **null** (150/150 zero passive UAD edges). ET-3 AI 2027 **closed** (LS-48). ET-4 Secret Loyalties hackathon organism + replay demo + paper under `papers/`. Graded-lab v4 + v1.3.0 tag.
- **Formal:** MB10 forgeability; Chokepoint.lean; field rederivation batch (ELK, debate, off-switch, etc.); RiskGap rename; credibility plan P1–P4 (tiling contrast).
- **Repo hygiene:** Conversation logs compressed to HANDOFF + RECOVERY (476 session files deleted 2026-07-31); per-session logs retired.

## Where durable state lives (do not re-derive from old logs)

| Topic | Canonical location |
|-------|-------------------|
| Cross-cutting tasks | `metadata/TODO.md` |
| Open uncertainties | `metadata/uncertainty-ledger.md` |
| Chapter status | `metadata/book.yml` |
| Experiment outcomes | `experiments/*/results/FINDINGS.md`, `NEGATIVE_RESULTS.md` |
| Bridge ↔ field map | `appendices/appB-bridge-crosswalk.tex` |
| Lean status | `formal/README.md`, Appendix I |
| Field news | `metadata/field-news.yml` |
| CIRIS cross-review | `~/repos/ciris/review/findings/` |

## Superseded — ignore unless git archaeology

- **Individual `ch*-draft` session logs** — chapters integrated; use git + `metadata/book.yml`.
- **`session-end-*` / commit-only logs** — git history sufficient.
- **Graded-lab `gl*` / `phase*` micro-logs** — outcomes in `experiments/graded-lab-simulation/results/FINDINGS.md` and `REPRODUCTION.md`.
- **Lab-sim / embedded-sim incremental logs** — `experiments/*/PLAN.md`, FINDINGS, NEGATIVE_RESULTS.
- **Field-news rollout logs (Jul 25–30)** — cards live in `metadata/field-news/`; tier-a/b partial logs superseded by `field-news-tier-ab` rollout.
- **Site UX / astro / sync fix logs** — shipped; site `README.md` and git.
- **Lean spine incremental session logs** — `formal/` + Appendix I supersede.

## Maintenance

- Update **Open work** and **Recently shipped** when a session changes load-bearing state.
- Do **not** recreate per-session `.md` files unless a multi-day thread needs a scratch pad; merge into HANDOFF instead.
- One-line recovery lines: [RECOVERY.md](RECOVERY.md) (regenerate from git before bulk delete if needed: `scripts/compress_conversation_summaries.py`).
