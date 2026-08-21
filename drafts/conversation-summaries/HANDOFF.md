# Agent handoff (conversation summaries)

**Read this first** when resuming work, then skim recent session logs in [INDEX.md](INDEX.md). Also `metadata/book.yml` and **`metadata/TODO.md`** (canonical work map). [RECOVERY.md](RECOVERY.md) lists only logs **pruned** because a later session superseded them.

Last updated: 2026-08-21 (program map: Voice / Witness / Field lanes).

---

## Open work

**Canonical list:** [`metadata/TODO.md`](../../metadata/TODO.md) — lanes, boards, sizes, gates. Do not duplicate here.

**Active lanes:**

- **Voice** — [`drafts/plans/voice.md`](../plans/voice.md). §2 `chapterthesis` boxes and §5 progress deferred; §1, §3, §4, §6–§8 done.
- **Witness** — [`drafts/plans/witness.md`](../plans/witness.md). Not frozen; Phase 0 = measurand freeze sheet + charter.

Closed 2026-08-17–18 work: **Compressed history (Aug 2026)** and `drafts/attic/`.

---

## Compressed history (Jun–Jul 2026)

Theme rollup only — per-session detail stays in `archive/` and recent logs in this folder.

- **Manuscript arc:** scaffold (Jun 17) → integrated ch01–ch48 drafts → chapter splits/renumber → epistemic-status pass → bridge crosswalk (App. B) + institutional histories (App. M/C) → field-news surgical cites (Jul 2026).
- **Lean spine:** proof skeleton → Mathlib adoption → field-agenda finite rederivations (ELK, debate, off-switch, Bellman) → hostile-critique fixes (MB4a, MB11, S10) → MB10 forgeability counterexample → Chokepoint.lean (shared steerability) → credibility plan P1–P4 (tiling contrast).
- **Experiments:** toy → embedded → goal-agent → lab-sim → graded-lab v4; external-transfer lines ET-1 (stopped), ET-2 (null), ET-3 (closed), ET-4 (hackathon); negatives honored in `NEGATIVE_RESULTS.md` / FINDINGS; sibling precursors **agency-detect** + **deployment-pipeline-simulator** indexed in `docs/EXPERIMENTS.md`.
- **Companion site:** Astro thin slice → concept cards + Lean playground → experiments/findings UX → field-news `/news/` layer + RSS + offline PWA.
- **Notation / voice:** canonical symbol pass (Jun 23) → update-operator envelope refactor → CCI vectorization → v1.1 terminology demotion (plain-first) → two-register narrative voice policy.

## Compressed history (Aug 2026)

Theme rollup — per-session detail in `archive/2026-08/`.

- **Architecture:** Krym Phases 1–6 (MB2 checkable, MB4 uptake/legitimacy, construction + MB8 gravestone, crux Props); `{leanbox}`; MB6b∨MB8 two-route prose retired; CEV as `AlignmentTarget`.
- **Consciousness / bearers:** ch18 Phases 0–5 closed (conservative exclusion inside MB3; no Rainbow).
- **Reader contract:** six-claims spine Phases 0–6; site `six-thesis-claims` card; `check_claim_spine.py`.
- **Field hub:** `/field/` → `/field/v2/` + `/field/coverage/`; stance SVG icons; specify/construct instances; MB7a–c cards; agenda merges + Kosoy/Iliad.
- **Site:** card-notes triage closed; offline PWA v9–v10; translation spine `/lean/`; field news (Black Hat, jailbreak, Anthropic risk report).
- **Papers / ch34:** feedback-horizon gap + verifier-construction spin-outs; selection ecology integration; constructing-alignment-attractors companion (explicit SB). **Construction not in manuscript** — Construct lane in `metadata/TODO.md`; gate = Witness real stop.

## This week

- **2026-08-21:** Program map — plans in `drafts/plans/` (`voice.md`, `witness.md`, `field.md`); Expectation 7 removed from Witness; HANDOFF compacted. Log: `2026-08-21-program-tracks-map.md`.
- **2026-08-21:** Executive overview rewritten for six-claim / three-question sync. Log: `2026-08-21-executive-overview-sync.md`.
- **2026-08-21:** Voice §1, §3, §4, §6–§8. Log: `2026-08-21-track-b-claim-strength-voice.md`.
- **2026-08-21:** Construction papers stay spin-outs (reviewer: unearned weight). Logs: `2026-08-21-constructing-alignment-attractors.md`, `2026-08-21-construction-manuscript-todo.md`.
- **2026-08-20:** ch21 Turner Reward≠OT hedge; README sync; erasure pass.
- **2026-08-19:** Anthropic Risk Report field news.

## Where durable state lives (do not re-derive from old logs)

| Topic | Canonical location |
|-------|-------------------|
| Cross-cutting tasks | `metadata/TODO.md` |
| Open uncertainties | `metadata/uncertainty-ledger.md` |
| Chapter status | `metadata/book.yml` |
| Experiment outcomes | `experiments/*/results/FINDINGS.md`, `NEGATIVE_RESULTS.md` |
| Field agenda crosswalk | `reference/field-agendas/field-agenda-index.md` |
| Bridge ↔ field map (manuscript) | `appendices/appB-bridge-crosswalk.tex` |
| Lean status | `formal/README.md`, Appendix G |
| Field news | `metadata/field-news.yml` |
| CIRIS cross-review | `~/repos/ciris/review/findings/` |

## Pruned sessions (superseded by later logs)

Only delete a session log when a **later conversation** explicitly supersedes it. See [RECOVERY.md](RECOVERY.md).

## Maintenance

- Update **This week** when a session changes load-bearing state.
- Write a new per-session log at session end (see [README.md](README.md)).
- Roll older logs: `python3 scripts/archive_conversation_summaries.py`.
