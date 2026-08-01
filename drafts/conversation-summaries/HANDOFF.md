# Agent handoff (conversation summaries)

**Read this first** when resuming work, then skim recent session logs in [INDEX.md](INDEX.md). Also `metadata/book.yml` and `metadata/TODO.md`. [RECOVERY.md](RECOVERY.md) lists only logs **pruned** because a later session superseded them (git recovery).

Last updated: 2026-08-01.

---

## Open work (load-bearing)

- **CIRIS composite / boundary_decouple counterexample** — Eric-facing key task: Verify+Lens can read green while WA-blind composite fails (named-identity bet vs real intervening unit). Charter: `~/repos/ciris/review/findings/2026-07-30-key-task-composite-boundary-counterexample.md`. Reuse: toy T-9 `boundary_decouple`, lab LS-28, MB1/composite-agency cards. Pointer: `experiments/TODO.md`.
- **Correlated steerability chokepoint** — WWCTV surfaces share adversarial-verifiability antecedent; disjunctive MB6b/MB8 routes may be one failure point. Formalized in `Chokepoint.lean`; still need per-chapter WWCTV forward refs and U-ledger reconciliation. Pointer: `metadata/TODO.md` BIG REVIEW.
- **Conserved-property forgeability (MB10)** — finite counterexample in Lean; prose wired. Still open: non-enumerability of conserved set across capability jumps; toy red-team of audit forgeability. Pointer: `metadata/TODO.md`, `Forgeability.lean`.
- **Terminology demotion follow-through** — plain-first vocabulary audit (deployment leverage, preservation conditions, etc.). Pointer: `metadata/TODO.md`; source log: `archive/2026-07/2026-07-08-glossary-terminology-demotion-release-notes.md`.
- **Measurand instantiation table** — composite indices bottom out in deferred estimators; needs mapping to experiment scripts. Pointer: `review/adversarial-steerability-correlated-failure-2026-06-30.md`.
- **Presentation / site-first** — de-center PDF as flagship; per-part display renumbering (high risk). Pointer: `metadata/TODO.md` § Presentation.

## Compressed history (Jun–Jul 2026)

Theme rollup only — per-session detail stays in `archive/` and recent logs in this folder.

- **Manuscript arc:** scaffold (Jun 17) → integrated ch01–ch48 drafts → chapter splits/renumber → epistemic-status pass → bridge crosswalk (App. B) + institutional histories (App. M/C) → field-news surgical cites (Jul 2026).
- **Lean spine:** proof skeleton → Mathlib adoption → field-agenda finite rederivations (ELK, debate, off-switch, Bellman) → hostile-critique fixes (MB4a, MB11, S10) → MB10 forgeability counterexample → Chokepoint.lean (shared steerability) → credibility plan P1–P4 (tiling contrast).
- **Experiments:** toy → embedded → goal-agent → lab-sim → graded-lab v4; external-transfer lines ET-1 (stopped), ET-2 (null), ET-3 (closed), ET-4 (hackathon); negatives honored in `NEGATIVE_RESULTS.md` / FINDINGS.
- **Companion site:** Astro thin slice → concept cards + Lean playground → experiments/findings UX → field-news `/news/` layer + RSS + offline PWA.
- **Notation / voice:** canonical symbol pass (Jun 23) → update-operator envelope refactor → CCI vectorization → v1.1 terminology demotion (plain-first) → two-register narrative voice policy.

## Recently shipped (Jul–Aug 2026 themes)

- **Manuscript:** Ch. 2/7/34 cite Sterman (systems-dynamics CLDs); Ch. 7 adds CCD / cyclic causal discovery as calibrated passive baseline for feedback coupling (not full agent discovery). Bib: Richardson CCD, Zanga survey, Sterman *Business Dynamics*.
- **Manuscript (Jul):** Ch. 17 cites Africa/Irving thousand-dimensional persona structure (with hedges vs control-rank). App. B links MIRI agent-foundations writeups on bridge rows. App. C note on MIRI hard-pause vs Plan A spectrum. AI 2040 Plan A surgical cites + news card.
- **Companion site:** Field-news layer (`metadata/field-news.yml`); “Read more in” chapter footers; RSS; offline PWA; link-type indicators; concept logos; experiment findings UX (`**Key finding:**` extraction).
- **Experiments:** ET-1 Orbit line **stopped** (passive UAD detects scripted macro-agent; channel independence). ET-2 CIL **null** (150/150 zero passive UAD edges). ET-3 AI 2027 **closed** (LS-48). ET-4 Secret Loyalties hackathon organism + replay demo + paper under `papers/`. Graded-lab v4 + v1.3.0 tag.
- **Formal:** MB10 forgeability; Chokepoint.lean; field rederivation batch (ELK, debate, off-switch, etc.); RiskGap rename; credibility plan P1–P4 (tiling contrast).
- **Repo hygiene:** Conversation logs restored from git (2026-07-31); selective prune of superseded sessions only; archive roll keeps ~15 recent logs in root.

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

## Pruned sessions (superseded by later logs)

Only delete a session log when a **later conversation** explicitly supersedes it (e.g. partial field-news rollout → full tier A/B log; ET-1 intermediate Colosseum runs → line-stopped conclusion). **Do not** delete chapter-draft, session-end, or micro-logs merely because the work landed in the repo — those logs remain historical context.

Examples pruned 2026-07-31: tier-B field-news partial → `2026-07-25-field-news-tier-ab`; ET-1 Colosseum intermediates → `2026-07-24-et1-lockstep-fsm-root-cause`; lab-sim freeze-review → handles-freeze. See [RECOVERY.md](RECOVERY.md).

## Maintenance

- Update **Open work** and **Recently shipped** when a session changes load-bearing state.
- Write a new per-session log at session end (see [README.md](README.md)).
- Roll older logs: `python3 scripts/archive_conversation_summaries.py`.
- Prune superseded logs: `python3 scripts/prune_superseded_conversation_logs.py --apply` (dry-run without `--apply`).
