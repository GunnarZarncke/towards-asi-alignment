# TSA shipping benchmark (Jun 17 – Aug 28, 2026)

Cross-index of **Git history**, **conversation session logs**, and **release tags** for *Towards Superintelligence Alignment* (TSA). Use this as a baseline for “how fast does TSA content ship?”

**Sources:** `git log` (662 commits), 633 session logs in `drafts/conversation-summaries/` (618 archived + 15 recent), `RELEASE_NOTES.md`, `HANDOFF.md`.

**As-of:** 2026-08-28 (project still active; table includes in-progress items through that date).

---

## Methodology

### What counts as “shipped”

| Signal | Weight |
|--------|--------|
| Git commit landing durable artifact (`.tex`, `formal/`, `experiments/`, `site/`, `papers/`) | Primary |
| Release tag (`v1.x.0`) | Milestone marker |
| Session log with explicit “closed / shipped / commit hash” | Work-date corroboration |

Housekeeping-only commits (session-log hash updates, archive rolls) are excluded from deliverable rows but included in commit-intensity stats.

### Work-day estimation

A **work day** is any calendar date with:

- ≥1 conversation session log, **or**
- ≥3 git commits (catches commit-only days without a log)

**Assumption:** 8 hours of focused work per work day (not wall-clock span). Author context: typical window **10:00–03:00 Berlin time** with many interruptions — so 8h is an *effective* day, not clock time.

**Weekends included:** 18 of 62 work days (29%) fell on Sat/Sun.

### Parallel work

Multiple lanes often run on the same day (manuscript + Lean + experiments + site). For each deliverable:

- **Calendar span** = ship date − first work date (wall clock).
- **Est. work days** = distinct dates with tagged sessions for that deliverable (or corroborating commits when sessions are sparse).
- **Parallel note** = whether the item shipped alone, in a short burst, or as part of a multi-lane day.

**Do not sum** per-deliverable work days to get total effort — lanes overlap. The **budget ceiling** is **62 work days × 8h = 496 person-hours** over 73 calendar days.

**Parallel intensity (project-wide):** 633 sessions / 62 work days ≈ **10.2 agent sessions per work day**; tagged lanes average ~5 concurrent topic threads on heavy days.

---

## Summary metrics

| Metric | Value |
|--------|-------|
| Repo first commit | 2026-06-17 |
| Latest commit (as-of study) | 2026-08-28 |
| Calendar span | **73 days** |
| Estimated work days | **62** |
| Estimated person-hours (8h/day) | **496 h** |
| Git commits | **662** |
| Conversation session logs | **633** |
| Tagged releases | **7** (`draft-2026-06-20` … `v1.5.0`) |
| Major version releases | **6** (`v1.0.0` … `v1.5.0`) |
| Median days between minor releases | **~8 days** (v1.0→v1.5) |
| Peak parallel day | **2026-06-30** — 47 sessions, 34 commits |

### Release velocity

| Tag | Date | Days from repo init | Cumulative work days (est.) | Headline |
|-----|------|---------------------|----------------------------|----------|
| `draft-2026-06-20` | 2026-06-20 | +3 | ~4 | First integrated draft (Parts I–IV skeleton) |
| `v1.0.0` | 2026-06-30 | +13 | ~12 | 48-ch manuscript + Lean spine + toy/embedded experiments |
| `v1.1.0` | 2026-07-08 | +21 | ~16 | Legibility pass, institutional histories (App M), 5 experiment lines |
| `v1.2.0` | 2026-07-17 | +30 | ~22 | Companion site publication layer, graded-lab v3, App I evidence index |
| `v1.3.0` | 2026-07-25 | +38 | ~28 | Field news, ch01–16 art, graded-lab v4, ET-1/ET-2 |
| `v1.4.0` | 2026-08-02 | +46 | ~32 | Field hub v1, ET-3/ET-4, legibility/demotion pass |
| `v1.5.0` | 2026-08-22 | +66 | ~52 | Six-claims spine, Krym Lean architecture, field hub v2, spin-out papers |
| *(post-v1.5)* | 2026-08-27–28 | +71–73 | ~62 | Site quiz (211 q), A-* assumption boxes, project-identity reframing |

**Benchmark shorthand:** first major release in **13 calendar days / ~12 work days**; five minor releases in the next **53 calendar days / ~40 work days** (~8 calendar days per minor release).

---

## Deliverable table (content → time)

Sorted by ship date. **Conv. logs** = representative session filenames (full index: `drafts/conversation-summaries/archive/`).

| # | Deliverable | Category | Work start | Ship date | Cal. days | Est. work days (8h) | Parallel context | Conv. logs (sample) |
|---|-------------|----------|------------|-----------|-----------|---------------------|------------------|---------------------|
| 1 | Repo + 44-ch book scaffold, intro, source-map bib | Manuscript | 2026-06-17 | 2026-06-17 | 1 | 1 | Solo init day | `2026-06-17-init-scaffold.md`, `2026-06-17-source-map-references-import.md` |
| 2 | Core draft ch01–10 + disconfirming sections | Manuscript | 2026-06-17 | 2026-06-18 | 2 | 2 | + ch03 dynamical guarantee same burst | `2026-06-17-ch03-dynamical-guarantee-draft.md`, `2026-06-18-what-would-change-this-view-sections.md` |
| 3 | Draft ch04–07, ch08–10; LW bib workflow | Manuscript | 2026-06-18 | 2026-06-18 | 1 | 1 | Same-day multi-chapter burst | `2026-06-18-session-end-ch04-ch06-ch07-drafts.md`, `2026-06-18-session-end-ch08-ch09-ch10-drafts.md` |
| 4 | Lean proof spine v0 (`formal/`) | Lean | 2026-06-19 | 2026-06-19 | 1 | 1 | Parallel with ch15–25 drafting | `2026-06-19-lean-spine-risk-derivation.md` |
| 5 | Part IV draft ch15–25 (value bundles, correction) | Manuscript | 2026-06-19 | 2026-06-19 | 1 | 1 | Parallel with Lean v0 | `2026-06-19-ch21-compression-test-intention-draft.md`, `2026-06-19-ch26-extrapolative-correction` (commits) |
| 6 | Chapter demos scaffold + ch09 UAD demo | Demos | 2026-06-19 | 2026-06-20 | 2 | 2 | Demo lane starts early | `2026-06-19-chapter-demos` (commit), `2026-06-20-ch09-uad-coalition-board-demo.md` |
| 7 | **`draft-2026-06-20` tag** — integrated draft snapshot | Release | 2026-06-17 | 2026-06-20 | 4 | ~4 | End of first sprint | `2026-06-20-draft-release` (commit) |
| 8 | Author draft integration ch28–38, 41–42; title simplification | Manuscript | 2026-06-22 | 2026-06-22 | 1 | 1 | Single-day integration | `2026-06-22-ch32-selection-environment-draft.md`, commit `ca6ff9cb` |
| 9 | Canonical notation pass + full-book review/fix plans | Manuscript | 2026-06-23 | 2026-06-23 | 1 | 1 | Review infrastructure | `2026-06-23-redundancy-pass-b-section.md`, `2026-06-23-chapter-epigraphs-pass.md` |
| 10 | Appendices generated, global bibliography, CCI ch25 consolidation | Manuscript | 2026-06-25 | 2026-06-26 | 2 | 2 | Lean UAD bridges same window | `2026-06-25-lean-proof-graphs-book-split.md`, `2026-06-25-cci-consolidation` (sessions) |
| 11 | Frontmatter split; ch35 split; update-operator refactor | Manuscript | 2026-06-26 | 2026-06-28 | 3 | 3 | Architecture cleanup lane | `2026-06-26-frontmatter-split.md`, `2026-06-28-ch35-split-implementation.md`, `2026-06-28-update-operator-refactor.md` |
| 12 | Toy simulation line (`experiments/toy-simulation/`) | Experiments | 2026-06-29 | 2026-06-30 | 2 | 2 | MB scenario burst | `2026-06-29-correction-capture-toy.md`, `2026-06-30-toy-simulation-subfolder.md` |
| 13 | Embedded simulation v1–v3 (UAD, MB scenarios, redteam parity) | Experiments | 2026-06-30 | 2026-06-30 | 1 | 1 | **Heavy parallel day** with v1.0 prep | `2026-06-30-embedded-audit-simulation.md`, `2026-06-30-embedded-simulation-v3-complete.md` |
| 14 | Mathlib adoption + field-agenda finite rederivations (CIRL, ELK, debate…) | Lean | 2026-06-30 | 2026-06-30 | 1 | 1 | Same burst as #12–13 | `2026-06-30-mathlib-adoption.md`, `2026-06-30-field-derivation-tranche.md` |
| 15 | Chapter/appendix renumbering → 48 ch + print order | Manuscript | 2026-06-30 | 2026-06-30 | 1 | 1 | Same burst | `2026-06-30-chapter-appendix-renumbering.md` |
| 16 | **`v1.0.0`** — first official major release | Release | 2026-06-17 | 2026-06-30 | 13 | ~12 | Peak day: 47 sessions | `2026-06-30-chapter-appendix-renumbering.md` (marks release) |
| 17 | Institutional histories appendix (App M) + site overview hub | Manuscript/Site | 2026-06-29 | 2026-07-08 | 10 | 3 | Woven into v1.1 window | `2026-06-29-institutional-translation-appendix.md`, `2026-07-08-institutional-histories-prior-art.md` |
| 18 | Bridge crosswalk (App B) + research-order composition | Manuscript | 2026-06-28 | 2026-07-08 | 11 | 4 | v1.1 packaging | `2026-06-28-research-order-composition-argument.md`, `2026-07-07-bridge-crosswalk` (sessions) |
| 19 | **`v1.1.0`** — legibility, site thin slice, 5 experiment lines named | Release | 2026-06-30 | 2026-07-08 | 8 | ~4 | Post-v1.0 consolidation | `2026-07-08-glossary-terminology-demotion-release-notes.md` |
| 20 | Companion site Astro layer (sync, cards, Lean web) | Site | 2026-07-02 | 2026-07-02 | 1 | 1 | New publication lane | `2026-07-02-companion-site` (commit: Astro companion site) |
| 21 | Goal-agent simulation (Milestone v5 Phase 1) | Experiments | 2026-07-05 | 2026-07-05 | 1 | 1 | Sequential after embedded | `2026-07-05-goal-agent-line-next-steps-recorded.md` |
| 22 | Lab simulation line Phases 0–8 | Experiments | 2026-07-06 | 2026-07-18 | 13 | 9 | Longest experiment lane to v1.2 | `2026-07-06-lab-simulation` … `2026-07-18-graded-lab-plan-v4` |
| 23 | Graded-lab v3 (Q1 transfer null, institutional runtime) | Experiments | 2026-07-10 | 2026-07-17 | 8 | 8 | Parallel with site v1.2 | `2026-07-15-graded-lab-v3-slice-e-pressure.md`, `2026-07-17-graded-lab-gl69-freeze-growth-brief.md` |
| 24 | **`v1.2.0`** — site publication layer, App I evidence index | Release | 2026-07-02 | 2026-07-17 | 15 | ~10 | Site + graded-lab converge | `2026-07-17-site-releases-updates-page.md` |
| 25 | Lean credibility P1–P4 (RiskGap, tiling contrast, MB11) | Lean | 2026-07-19 | 2026-07-20 | 2 | 2 | Hostile-critique response burst | `2026-07-19-lean-spine-hostile-critique-fixes.md`, `2026-07-20-lean-spine-credibility-p4-tiling.md` |
| 26 | Field rederivation batch 2 (ELK, debate, off-switch…) | Lean | 2026-07-19 | 2026-07-19 | 1 | 1 | Same burst as #25 | `2026-07-19-field-rederivation-batch-2.md` |
| 27 | Graded-lab v4 architecture + GL-79–85 harvest | Experiments | 2026-07-18 | 2026-07-19 | 2 | 2 | Per-bridge rig redesign | `2026-07-19-graded-lab-v4-manuscript-harvest.md`, `2026-07-19-graded-lab-v4-5-r-mb2-scorecard-goodhart.md` |
| 28 | ET-1 Orbit external transfer (closed, lockstep FSM root cause) | Experiments | 2026-07-19 | 2026-07-24 | 6 | 3 | ET lane starts | `2026-07-19-et1-orbit-external-transfer-freeze.md`, `2026-07-24-et1-lockstep-fsm-root-cause.md` |
| 29 | ET-2 CIL live null + ET-4 hackathon paper/replay | Experiments | 2026-07-23 | 2026-07-27 | 5 | 4 | Hackathon sprint | `2026-07-25-et2-cil-live-smoke-null.md`, `2026-07-27-et4-replay-demo.md` |
| 30 | Field news layer (9+ cards) + RSS + chapter footers | Site | 2026-07-25 | 2026-07-25 | 1 | 1 | v1.3 packaging day | `2026-07-25-field-news-tier-ab.md`, `2026-07-25-rss-feed-and-news-dates.md` |
| 31 | Chapter illustrations ch01–16 | Manuscript/Site | 2026-07-25 | 2026-07-25 | 1 | 1 | Same v1.3 burst (39 commits) | `2026-07-25-chapter-illustrations.md` |
| 32 | **`v1.3.0`** — field news, art, graded-lab v4, ET-1/2 | Release | 2026-07-17 | 2026-07-25 | 8 | ~6 | 24 sessions on ship day | `2026-07-25-v1-3-0-release-notes.md` |
| 33 | Offline PWA v9+ (opt-in caching, hourly refresh) | Site | 2026-07-27 | 2026-07-27 | 1 | 1 | | `2026-07-27-site-offline-pwa.md` |
| 34 | Field hub v1 (`/field/`, 32 agendas, matrix, bridge cards) | Site/Field | 2026-08-02 | 2026-08-02 | 1 | 1 | v1.4 ship day (28 commits) | `2026-08-02-field-hub` (commit), `2026-08-02-bridge-cards-field-first` (sessions) |
| 35 | ET-3 AI2027 annex closed + ET-4 site cards | Experiments | 2026-07-26 | 2026-08-02 | 8 | 2 | Closed in v1.4 window | `2026-07-26-et3-ai2027-integration.md`, `2026-07-29-et4-secret-loyalties-news.md` |
| 36 | **`v1.4.0`** — field crosswalk hub, legibility, ET-3/4 | Release | 2026-08-02 | 2026-08-02 | 0* | ~4 | *Tag on same day as #34–35 | `2026-08-02-v1-4-0-release-notes` (RELEASE_NOTES.md) |
| 37 | Translation spine `/lean/` + field-first Lean on-ramp | Site/Lean | 2026-08-04 | 2026-08-04 | 1 | 1 | Post-v1.4 reader path | `2026-08-04-translation-spine-on-ramp.md` |
| 38 | Chapter reading graph + eq-chain tooling | Site/Manuscript | 2026-08-05 | 2026-08-05 | 1 | 1 | 24 sessions, 20 commits | `2026-08-05-chapter-reading-graph-site.md`, `2026-08-05-equation-chain-def-use-graphs.md` |
| 39 | Page notes overlay (localStorage, highlights) | Site | 2026-08-07 | 2026-08-07 | 1 | 1 | | `2026-08-07-page-notes-overlay.md` |
| 40 | Krym architecture Phases 1–6 (MB2/MB4/MB8, `{leanbox}`, crux Props) | Lean/Manuscript | 2026-08-15 | 2026-08-17 | 3 | 3 | **Aug 17 mega-burst** (27 sessions) | `2026-08-15-krym-phase1-early-scope.md` … `2026-08-17-krym-phase6-crux-props-field-v2.md` |
| 41 | Six-claims reader contract + `check_claim_spine.py` | Manuscript/Site | 2026-08-17 | 2026-08-17 | 1 | 1 | Parallel with #40 on Aug 17 | `2026-08-17-six-claims-spine-phase0-2.md`, `2026-08-17-six-claims-spine-phase6` (commits) |
| 42 | Field hub v2 (`/field/v2/`, lifecycle, stance SVGs) | Site/Field | 2026-08-17 | 2026-08-18 | 2 | 2 | Parallel with #40–41 | `2026-08-17-field-v2-cutover.md`, `2026-08-18-field-stance-icons.md` |
| 43 | Consciousness/bearer overlay ch18 Phases 0–5 | Manuscript | 2026-08-17 | 2026-08-17 | 1 | 1 | Same burst | `2026-08-17-consciousness-tsa-phase0.md` … `phase5-lean-mb3.md` |
| 44 | Spin-out papers: Feedback Horizon Gap, Alignment Under Selection, Verifier Construction, Constructing Alignment Attractors | Papers | 2026-08-15 | 2026-08-21 | 7 | 3 | Not in PDF; companion `papers/` | `2026-08-15-feedback-horizon-gap-paper.md`, `2026-08-21-constructing-alignment-attractors.md` |
| 45 | ch34 selection ecology integration + spin-out weave | Manuscript | 2026-08-15 | 2026-08-15 | 1 | 1 | Same Aug 15 burst | `2026-08-15-ch34-selection-spin-out-integration.md` |
| 46 | Authorship bars PDF + site chips (48 ch + appendices) | Manuscript/Site | 2026-08-21 | 2026-08-22 | 2 | 2 | ~1440 pp PDF | `2026-08-21-authorship-bars.md`, `2026-08-22-authorship-bars-rollout.md` |
| 47 | **`v1.5.0`** — six-claims, Krym, field v2, authorship | Release | 2026-08-15 | 2026-08-22 | 8 | ~6 | Largest architecture release | `2026-08-22-v1-5-0-release-notes.md` |
| 48 | Construct 2.0 plan + adverse-process generator + harm-path v1 weave | Planning/Manuscript | 2026-08-24 | 2026-08-25 | 2 | 2 | 2.0 lane; v1 MS gated | `2026-08-24-construct-2-0-plan.md`, `2026-08-25-harm-path-v1-weave.md` |
| 49 | Site nav landings + essay path + book contents map | Site | 2026-08-26 | 2026-08-26 | 1 | 1 | 25 commits, 11 sessions | `2026-08-26-site-nav-landings.md`, `2026-08-26-generalist-essay-path.md` |
| 50 | Card slug migration (684 redirects) | Site | 2026-08-26 | 2026-08-26 | 1 | 1 | Same burst as #49 | `2026-08-26-card-slug-migration.md` |
| 51 | Site quiz bank (211 questions, blind eval, length-tell checks) | Site | 2026-08-27 | 2026-08-27 | 1 | 1 | 14 sessions on one day | `2026-08-27-quiz-phase-1.md` … `2026-08-27-quiz-blind-eval.md` |
| 52 | A-* assumption boxes in home chapters + `\akey{}` links | Manuscript | 2026-08-27 | 2026-08-28 | 2 | 2 | Voice/lean axiom distinction same window | `2026-08-27-manuscript-a-keys.md`, `2026-08-27-voice-lean-axioms.md` |
| 53 | Project identity reframing (knowledge base, not manuscript-first) | Meta | 2026-08-28 | 2026-08-28 | 1 | 1 | README + INSTRUCTIONS scope | `2026-08-28-project-not-manuscript.md` |
| 54 | Alignment Crux Map grant draft | Meta/Field | 2026-08-28 | 2026-08-28 | 1 | 1 | External listing, not repo core | `2026-08-28-alignment-crux-map.md` |

---

## Parallel burst calendar (multi-lane days)

Days where **≥10 sessions** or **≥20 commits** indicate heavy parallel shipping:

| Date | Sessions | Commits | Lanes active (from logs) | Notable ships |
|------|----------|---------|--------------------------|---------------|
| 2026-06-17 | 9 | 9 | Manuscript scaffold | Repo init, ch01–02, ch03 |
| 2026-06-18 | 21 | 5 | Manuscript | ch04–10 |
| 2026-06-19 | 19 | 10 | Manuscript + Lean + demos | Lean spine, ch15–25, demos |
| 2026-06-30 | **47** | **34** | Manuscript + Lean + experiments | **v1.0.0**, toy + embedded sim, Mathlib, renumber |
| 2026-07-02 | 23 | 29 | Site + manuscript | Astro companion site launch |
| 2026-07-15 | 22 | 11 | Graded-lab | v3 slices, symbol audit |
| 2026-07-17 | 22 | 26 | Site + graded-lab | **v1.2.0** prep |
| 2026-07-19 | 17 | 21 | Lean + graded-lab + ET | Credibility plan, v4 harvest |
| 2026-07-25 | **24** | **39** | Site + field news + ET + art | **v1.3.0** |
| 2026-08-02 | 18 | 28 | Field hub + legibility | **v1.4.0** |
| 2026-08-05 | 24 | 20 | Site + eq-chains + field news | Reading graph, jailbreak news |
| 2026-08-17 | **27** | 21 | Lean + manuscript + site + field | Krym Ph 3–6, six-claims, field v2, ch18 |
| 2026-08-26 | 11 | 25 | Site IA | Nav landings, essay path, card slugs |
| 2026-08-27 | 14 | 9 | Site + voice | Quiz ship, chapterthesis audits |

**Idle gaps ≥2 days:** 2026-07-20→23 (2d), 2026-08-08→15 (6d).

---

## Lane cross-index (conversation tags → dates)

Approximate session counts by topic keyword in log filenames (633 total; many sessions untagged or multi-topic):

| Lane | Sessions | Active dates | First | Last |
|------|----------|--------------|-------|------|
| Manuscript (chapters, voice, appendices) | 105 | 24 | 2026-06-17 | 2026-08-27 |
| Experiments (5 lines + ET) | 140 | 22 | 2026-06-29 | 2026-08-15 |
| Site (Astro, field hub, quiz, PWA) | 59 | 25 | 2026-06-18 | 2026-08-27 |
| Lean spine | 25 | 10 | 2026-06-19 | 2026-08-17 |
| Spin-out papers | 5 | 4 | 2026-06-25 | 2026-08-21 |
| Untagged / housekeeping / meta | ~299 | — | — | — |

Full per-date index: `drafts/conversation-summaries/archive/2026-{06,07,08}-INDEX.md` and root `INDEX.md` (15 most recent).

---

## Throughput benchmarks (for planning)

Use these as **order-of-magnitude** targets, not promises.

| Content class | Typical calendar span | Est. work days | Example |
|---------------|----------------------|----------------|---------|
| Single chapter draft (from outline) | 1–2 days | 1 | ch03 on 2026-06-17 |
| Major integrated slice (10+ chapters) | 1 day | 1 | ch28–38 integration 2026-06-22 |
| New experiment line (0→frozen v1) | 1–13 days | 1–9 | toy: 2d; lab-sim: 13d cal / 9d work |
| Companion site feature (medium) | 1–15 days | 1–10 | Astro launch: 1d; publication layer: 15d |
| Lean architecture revision (multi-bridge) | 3 days | 3 | Krym Ph 1–6: Aug 15–17 |
| Minor release (`v1.x.0`) | 7–8 days since prior | 4–6 | v1.0→v1.1: 8d cal |
| Major release milestone | 13 days from init | ~12 | v1.0.0 |
| Site quiz (200+ q, checks, blind eval) | 1 day | 1 | 2026-08-27 (14 sessions) |

**Effective parallel factor:** On peak days, **3–5 durable artifacts** can land simultaneously (e.g. 2026-06-30: renumber + embedded sim + Mathlib + v1.0 tag). Planning assumption: **~2–3 shippable artifacts per heavy work day**, **~1 per light day**.

---

## Caveats

1. **Session logs ≠ human-only time.** Most sessions are agent-assisted; 8h/day is the author's effective budget, not agent wall time.
2. **Commit timestamps are UTC dates** on GitHub; Berlin work window may shift session log date vs commit date by ±1 day on late-night commits.
3. **Pre-repo work** (prior drafts imported 2026-06-17) is not counted in work-day totals.
4. **In-progress at cut-off:** Construct 2.0, Voice § audits, alignment crux map — started but not release-tagged.
5. **Double-counting:** Summing the "Est. work days" column (~90+) exceeds 62 because lanes overlap; use **62 work days / 496h** as the global budget.

---

## Maintenance

- Re-run commit/session stats after major releases.
- Update ship dates from `RELEASE_NOTES.md` and new session logs.
- Optional script: extend `scripts/` to regenerate tables from `git log` + conversation filenames.
