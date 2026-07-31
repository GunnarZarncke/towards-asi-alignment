# 2026-07-18 — Graded lab: PLAN_v4 draft (per-bridge rigs) + v3 line closure (GL-78)

## Trigger
User, after the GL-76 go-gate cascade: decouple the stages along bridge
assumptions so a failed gate no longer ruins the whole program; draft a
detailed PLAN_v4; assess which other MBs build easily on graded-lab;
move stretch items to REPRODUCTION.md; close the v3 line.

## Done
- **`PLAN_v4.md` (new, DRAFT — not frozen):** decoupled per-bridge rig
  architecture. Rig contract (`check_precondition` → `run_rig` →
  per-prediction eval; SKIP-with-finding semantics), three-class
  substrate policy (S-blind / S-fixture / S-inherited) with the
  anti-developed-to-the-test rule (growth may target a rig's
  *precondition*, never its *outcome* metrics), rig catalog
  (R-MB1/2/4/5/6a/6b/7/7d/8/9), staged build order V4-0…V4-8 with small
  builds (R-MB9, R-MB7d) at V4-3 and medium builds (R-MB2, R-MB5,
  R-MB8) at V4-5, risks, coverage table, open freeze questions.
- **`REPRODUCTION.md` §12–§13 (new):** §12 v4 stretch rigs — R-MB3
  bearer maps (prerequisite: per-archetype harm-ledger split in
  `oracle.py`, GL-50-class blast radius) and MB10 scoped out to the
  embedded-simulation line; §13 all-bridges integration — cross-line
  bridge-coverage ledger (`metadata/` YAML + generator + `make check`
  script) and per-bridge synthesis doc.
- **v3 line closed (GL-78):** FINDINGS closure entry; `PLAN_v3.md`
  header → LINE CLOSED with carry-forward note; stale GL-66 step-7 row
  fixed (satisfied by GL-69 freeze, annotated); `PLAN_v2.md` v3 phase
  row updated from "spec written" to done + closed.

## Decisions (non-obvious)
- Q1's go gate is scoped down to **one rig** (R-MB6b evasion-under-
  ambiguity, expected-SKIP on v3 grown) instead of gating three phases;
  R-MB7 red-team and R-MB6a selection-machinery sanity run regardless.
- v4 deliberately **drops** the joint "whole machinery transfers to one
  unseen ecology" claim (answered null in GL-76) in favor of per-leaf
  claims — matches the ch42 safety-case-leaves harvest.
- S-fixture results are permanently labeled coherence-grade; class
  moves down require a FINDINGS entry and relabel prior results.
- R-MB8 named first cut candidate; R-MB3/MB10 are not v4 stages
  (design gate + freeze addendum required to enter).
- PLAN_v4 is a **draft**: no constants, predictions, or harvest
  sentences frozen; V4-1 is the freeze session.

## Open / next
- V4-1 freeze session: per-rig precondition constants, substrate
  classes, predictions, pass/null/SKIP harvest sentences → DESIGN.md.
- User input wanted on PLAN_v4 open questions 1–3 (R-MB6b growth vs
  declared SKIP; R-MB7 model class + budget; keep/cut R-MB5/R-MB8).
- V4-0 refactor (fixture layer; decompose `machinery_transfer.py`;
  GL-76 must reproduce bit-for-bit).
- Noted, not fixed: `PLAN_v2.md` *header* status line still stale
  (pre-Q1); `REPRODUCTION.md` has a pre-existing duplicate "§8".

## Key paths
- `experiments/graded-lab-simulation/PLAN_v4.md`
- `experiments/graded-lab-simulation/REPRODUCTION.md` (§12, §13)
- `experiments/graded-lab-simulation/PLAN_v3.md`, `PLAN_v2.md`
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-78)

## Commits
- `de694a3` Draft PLAN_v4 (decoupled per-bridge rigs) and close the v3 line (GL-78). (amended → final hash in `git log`)
