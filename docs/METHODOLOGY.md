# Experimental methodology

**Canonical discipline doc** for all empirical work in this repository. Narrative
per line: [`EXPERIMENTS.md`](EXPERIMENTS.md). Structured site index:
[`metadata/experiments.yml`](../metadata/experiments.yml). Reader-facing summary:
[experiment-methodology concept](../metadata/concepts/bodies/experiment-methodology.md)
→ `/cards/concept/experiment-methodology/`.

**Claim strength:** methodology-building and sanity checks only. No experiment
line validates the full book thesis, proves deployable alignment, or substitutes
for the Lean dependency spine's explicit bridge axioms (`MB1`–`MB10`).

**Repo rule (AGENTS.md):** conclusions are never named in definitions before
being derived — fix thresholds, data, and protocols first; report whatever the
derivation yields, including failures and weak bounds.

---

## Document map

Use this table before adding rules in a new file. **Shared discipline lives
here.** Line folders keep only **binding protocols** for what that line actually
did (prompts, schemas, frozen JSON, checkers).

| What | Location |
|------|----------|
| **This file** | `docs/METHODOLOGY.md` — shared habits, blind-generation lessons, Witness failure conditions |
| **Experiment narrative + finding tables** | [`docs/EXPERIMENTS.md`](EXPERIMENTS.md) |
| **Site / coverage matrix** | [`metadata/experiments.yml`](../metadata/experiments.yml) |
| **Witness charter + Exp. 1–6 pass/fail/refuse** | [`drafts/plans/witness-phase0.md`](../drafts/plans/witness-phase0.md) |
| **Witness phase index + finding template** | [`drafts/plans/witness.md`](../drafts/plans/witness.md) |
| **Witness v2 (plan only)** | [`drafts/plans/witness-v2.md`](../drafts/plans/witness-v2.md) — Phase 1 Moltbook; [`witness-v2-moltbook-inventory.md`](../drafts/plans/witness-v2-moltbook-inventory.md); **MB7a freeze** [`witness-v2-moltbook-mb7a.md`](../drafts/plans/witness-v2-moltbook-mb7a.md) |
| **Witness per-host freezes** | `drafts/plans/witness-phase*.md`, `witness-c004-*.md`, `witness-v2-moltbook-mb7a.md` |
| **Witness ledger + checkers** | [`experiments/witness/`](../experiments/witness/) |
| **Sim blind-generation (binding)** | [`goal-agent-simulation/BLIND_GENERATION.md`](../experiments/goal-agent-simulation/BLIND_GENERATION.md), [`lab-simulation/BLIND_GENERATION.md`](../experiments/lab-simulation/BLIND_GENERATION.md), [`lab-simulation/lab_sim/agent_visible/BLIND_GENERATION_ROUND2.md`](../experiments/lab-simulation/lab_sim/agent_visible/BLIND_GENERATION_ROUND2.md), [`lab-simulation/lab_sim/oracle_only/BLIND_DETECTOR_GENERATION.md`](../experiments/lab-simulation/lab_sim/oracle_only/BLIND_DETECTOR_GENERATION.md), [`graded-lab-simulation/BLIND_GENERATION.md`](../experiments/graded-lab-simulation/BLIND_GENERATION.md) |
| **External-test preregistration** | e.g. `experiments/lab-simulation/runners/et4_secret_loyalties/*_preregistration.json`, [`graded-lab-simulation/PLAN_ET1.md`](../experiments/graded-lab-simulation/PLAN_ET1.md) |
| **Embedded audit-plane projection** | [`embedded-simulation/embedded_sim/audit_projection.py`](../experiments/embedded-simulation/embedded_sim/audit_projection.py) (sensor-plausible fields for the auditor) |

---

## Three experiment classes

| Class | Examples | Primary discipline |
|-------|----------|-------------------|
| **Simulations** | toy, embedded, goal-agent, lab, graded-lab | Blind generation where applicable; three-plane separation; twin baselines; numbered findings ledgers |
| **External tests** | ET-1–ET-4 | Frozen instrument on foreign substrate; **substrate-suitability stop**; JSON/plan preregistration before scored run |
| **Witness tests** | W-1–W-15 | Per-host protocol freeze before fixture; fail / refuse / null; no sixth sim; H0 not deployment witness |

None of the three is proof on a frontier system.

---

## Core habits (all classes)

1. **Freeze before you score.** Thresholds, margins, splits, detectors, and
   scenario batteries are fixed before the evaluating run. A genuine change
   (bug fix, new variant) gets a new version string and a ledger entry — not a
   silent edit to old numbers.

2. **Register predictions before results.** Expected outcomes (pass band, layer
   fail, refuse branch) are written down before the scored run. Sim lines use
   blind-generation rounds or plan-section preregistrations; Witness uses
   per-host protocol files; ET lines use `*_preregistration.json` or frozen
   plan slices.

3. **Separate author from scorer where possible.** Blind generation breaks
   generator/detector co-design loops (see § Blind generation). Witness has no
   authored-world generator but still separates protocol author from scorer via
   frozen checkers.

4. **Refuse and null are first-class.** Weak hosts, wrong units, and
   non-adversarial measurands → **refuse**. Frozen pipelines that miss
   pre-registered margins → **null**, not retune (Witness W-14, W-15; graded-lab
   GL-85 method limit).

5. **Substrate-suitability stop.** If the instrument reports the coupling the
   substrate actually has (ET-1 shared script; W-7 country unit for C-004),
   **stop** and record — do not fetch a cleaner world to recover a pass.

6. **Negatives stay in the ledger.** Every line keeps a running numbered log.
   Failures are not deleted when a later fix lands. Site key findings are curated
   extracts; full history stays on GitHub (`FINDINGS.md` / `NEGATIVE_RESULTS.md`).

7. **Honest twins / severity-first referee** (sim lines). Detectors are checked
   against episodes with deceptive behavior removed so flags are not merely
   “activity visible.”

8. **Progress logging on long runs.** Batteries and multi-seed sweeps print
   `[i/n]` (or equivalent) progress — see AGENTS.md.

---

## Blind generation (simulation lines)

Every simulation line that uses blind generation follows the same goal: a
generator that has **not** seen the evaluation rubric produces content; a
**frozen** evaluator scores it with no re-fitting. Detection failures are
headline results, not bugs.

**Binding protocols** (prompts, verbatim rounds, frozen JSON) stay in each
line's `BLIND_GENERATION.md` (see document map). The lessons below are
cross-line failure modes (graded-lab v2 GL-34–GL-38 and siblings).

### Lesson 1 — blind the measurement, never the phenomenon

Blind the evaluated party to the **evaluator's rubric**, not to their own
system's behavior. If a criterion requires observing a run (e.g. joint
scheduling liveness), give the generator a **sandbox pilot** with
sensor-plausible outcomes only — never scorer output. Same discipline as
`embedded-simulation` `audit_projection.py` for the auditor plane; apply
symmetrically to the generator before scoring.

### Lesson 2 — coarsened feedback is still a leak

Do not enrich between-round feedback with rubric-derived signals (“too sparse,”
which sub-check failed). Any signal derived from the checker's threshold
predicate is a coarsened readout; the generator can binary-search it. If bool-only
feedback stalls, ask whether a **world fact** is missing (Lesson 3) or parameters
are misplaced (Lesson 4) — not whether to “give a hint.”

### Lesson 3 — world fact vs threshold

Disclosing a missing world fact (e.g. “one actor per role”) is legitimate if a
**domain-coherence reviewer who never saw the rubric** would flag it on a cold
read of the brief alone. If the fix requires knowing what is measured or which
side of a threshold the generator is on, it is a leak.

### Lesson 4 — own free parameters correctly

List every parameter the criterion depends on. **World/design facts** the
generator may set; **engine/implementer facts** must be frozen by the
implementer in the same preregistration phase — not delegated to the blinded
generator's JSON because they look numeric.

### Lesson 5 — known-live check for reference-agent bands

Before freezing “reference roster must land in band X,” run that roster on at
least one known-understood substrate and confirm the band is reachable.

### Lesson 6 — fraction of plausible designs that pass

**Corner filters** (most coherent designs pass) vs **rare-property generators**
(narrow parameter region). For the latter, change the substrate or do not freeze
as a pure blind-growth target.

### Lesson 7 — misdiagnosis under opaque feedback

Attribute stalls to **information available**, not generator quality, unless a
leak-safe signal was available and unused.

### Lesson 8 — archive contaminated rounds

Preserve leaked rounds as evidence; void them from the round budget. For agentic
generators, **physically remove** sensitive files from the working tree — do not
rely on “do not read X” instructions across rounds.

### Lesson 9 — honest negatives in blind protocols

Stalled growth attempts are findings in `results/FINDINGS.md`, not buried retries.

### Checklist — new blind-growth criterion

Before freezing in `DESIGN.md` / `PLAN.md`:

1. Decidable from declared output only, or requires a run? (Lesson 1)
2. If run: sandboxed non-scoring pilot with sensor-plausible outputs? (Lesson 1)
3. Every free parameter: world fact vs engine fact — engine facts frozen by implementer? (Lesson 4)
4. Reference-agent band: known-live check on existing substrate? (Lesson 5)
5. Rough fraction of realistic designs that pass unassisted? (Lesson 6)
6. Between-round “missing facts”: cold-read coherence test? (Lessons 2–3)
7. Feedback plan avoids coarsened threshold predicates? (Lesson 2)

---

## Witness tests

Witness applies the core habits to **existing traces** (Linux git, Wikipedia,
published evals, CIRIS-shaped mock, institutional documents). It does **not**
use sim-style blind generation.

**Charter and Exp. 1–6 tables:** [`witness-phase0.md`](../drafts/plans/witness-phase0.md).
**Phase index:** [`witness.md`](../drafts/plans/witness.md).
**Ledger:** [`experiments/witness/results/FINDINGS.md`](../experiments/witness/results/FINDINGS.md).

### Finding shape

Every `W-*` entry includes: Host · Frozen protocol (version, snapshot) ·
Expectation/claim · Outcome (`pass` | `fail` | `refuse` | `null`) · Stop
condition triggered? · Artifact paths. Per-host freeze files are the
preregistration record — committed with or before the first scored fixture.

### Host-level failure (Expectations 1–6)

Summary of Phase 0 “Fail (Witness unmet)” — full table in `witness-phase0.md`:

| Exp. | Witness **unmet** when |
|------|------------------------|
| **1** | Any C-003–C-007 has only H0 backing or only green with no disagreement on H1–H5 |
| **2** | Still only embedded `honestCert` / authored JSON; no pinned H1–H4 Lean fixture |
| **3** | Honesty/AUROC reported as discharging A-009 without refuse or \(\kappa\) bound |
| **4** | Only in-sim deploy gates; no enforceable handle in the archive episode |
| **5** | Only imagined or H0 pairs for green-artifact + failed uptake |
| **6** | Only book-authored sims where an external table was required |

**Single finding failure:** `pass` with no stop while prose would still treat
the leaf as safe.

### Methodology failure conditions (M1–M8)

If any trigger, the **Witness program** fails its epistemic bar — not merely a
host leaf.

| ID | Fail if | Remedy |
|----|---------|--------|
| **M1** | No pre-registered condition to stop adding hosts or declare the lane unsuccessful; every outcome narrated only as “payment” | Sprint boundaries + success/failure gates before next block |
| **M2** | Protocol freeze post-dates scored fixture, or margins chosen after held-out inspection | Git-order freeze; checker reads frozen fields only |
| **M3** | `pass` without stop while deployment/bridge wording still strong | Reclassify; add stop language |
| **M4** | H0/authored mock cited as H1–H5 witness without tag | W-1 / W-8 / W-15 tagging template |
| **M5** | Null followed by silent retune without new protocol version + finding ID | Version bump (`h4-cpc2015-v2.0.0`), not v1 edit |
| **M6** | New host repeats refused unit error or substitute data | Refuse fast (W-7, W-13 pattern) |
| **M7** | Next block only increases W-count without depth objective | Name expectation or M-gap addressed |
| **M8** | Load-bearing cite without external reproduction attempt or documented refusal window | Log repro or downgrade claim strength |

**W-1–W-15 sprint (Aug 2026):** bounded process demonstration; **M8 open**; no
adversarial \(M\) at \(\kappa^*\); no live CIRIS bypass demo.

### Open depth gates (canonical TODOs)

Tracked in [`drafts/plans/witness.md`](../drafts/plans/witness.md) and
[`metadata/TODO.md`](../metadata/TODO.md):

- [ ] **Adversarial \(M\)** (Expectation 3): stated \(\kappa^*\) + cost-of-faking
  on one frozen host, **or** named closure that H1–H5 cannot supply one (W-2
  MASK refuse alone does not pay this).
- [ ] **Independent reproduction** (M8): external rerun of frozen checkers;
  first targets W-12 (`check_h4_mm_raw.py`), W-3 (`check_h2.py`); log before
  load-bearing cites.

Before a new Witness block: state which expectation or M-gap it addresses; for
CIRIS work include a **pre-defer positive-control** arm.

---

## External tests (ET)

ET lines apply frozen in-repo instruments to substrates this project did not
build. Discipline:

- Pre-register protocol + stop criteria (`PLAN_ET*.md`, `*_preregistration.json`).
- **Substrate-suitability stop** when the instrument answers the wrong question
  (ET-1 GL-86, ET-2 GL-87/88).
- Nulls and closes are outcomes — not prompts to retune the instrument on the
  same substrate.

---

## When editing methodology

- **Shared rule?** Add or amend **this file** only.
- **Line-specific prompt, schema, or frozen artifact?** That line's
  `BLIND_GENERATION.md`, `PLAN*.md`, or Witness per-host freeze — not here.
- **New finding?** Ledger + optional Appendix I; do not duplicate outcome prose
  here.
- **Site card** [`experiment-methodology.md`](../metadata/concepts/bodies/experiment-methodology.md):
  keep short; link here for full discipline.
