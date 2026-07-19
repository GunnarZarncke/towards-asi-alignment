# PLAN v4 — decoupled per-bridge rigs (DRAFT — partially implemented)

**Status: draft proposal (2026-07-18); V4-0 through V4-4 implemented
and scored for `R-MB1`, `R-MB4`, `R-MB9`, `R-MB7d`, and `R-MB6a`
(GL-79/GL-80/GL-81, same day).** Five rigs' preconditions,
predictions, and harvest sentences are frozen in `DESIGN.md`
("PLAN_v4 pre-registration" sections) and scored in
`results/FINDINGS.md` GL-79/GL-80/GL-81
(`results/v4_r_mb1.json`, `results/v4_r_mb4.json`,
`results/v4_r_mb9.json`, `results/v4_r_mb7d.json`,
`results/v4_r_mb6a.json`). The new `channel_severance` runtime
primitive R-MB7d needed (`world.py`) is added and tested, flagged
there for later human review. **`R-MB6b`, `R-MB7`, `R-MB2`, `R-MB5`,
`R-MB8`** remain unfrozen placeholders pending the "open questions"
section — do not cite constants/predictions for those rigs as
pre-registered.

**Spawn trigger:** V2-3's go gate failed honestly (GL-76: P1–P3 false,
referee-vantage EAI never reached mid band) and the failure **cascaded**
— V2-4, V2-5, and V2-6 were all descoped even though their machinery
questions (variation-operator sanity, selection noise floors, red-team
protocol) did not intrinsically depend on the failed property. One
grown ecology had to simultaneously satisfy every downstream stage's
preconditions; when it satisfied none of the ambiguity/coupling ones,
the whole program terminated with a single (real, harvested) null.

v4 restructures the program so that **each bridge assumption gets its
own rig** with its own declared precondition, its own substrate policy,
and its own pre-registered predictions. A failed precondition produces
a **SKIP-with-finding for that rig only**; the other rigs keep running.
This also matches the manuscript's own argument (ch42, 2026-07-17
harvest): safety-case leaves must not be collapsed into a single
"machinery transferred" checkbox — v4 is that argument as experiment
architecture.

---

## What v4 asks

Not one question with a gate chain, but a **portfolio**: for each
bridge assumption MBx that graded-lab can operationalize, a rig R-MBx
asks "does the frozen machinery / mechanism for MBx behave as the
bridge assumes, on a substrate that verifiably has the precondition
the test needs?" Each rig resolves independently to pass / null /
SKIP(precondition unsatisfied) — all three are reportable findings.

## What v4 is not

- **Not a rewrite.** Same codebase, same substrate, same plane
  discipline (`world_visible` / `agent_visible` / `oracle_only`), same
  oracle tiers, isolates, referee, and stats toolkit. v1/v2/v3 replay
  pins stay green at every landing (PLAN_v3 constraint 1).
- **Not a retreat from blinding.** Per-rig substrates are the main new
  risk (see "Substrate policy" — the anti-developed-to-the-test rule is
  the single most important pre-registration in this plan).
- **Not a claim upgrade.** Same epistemic contract: tentative, partial
  stress-tests of bridge cruxes; negatives recorded in
  `results/FINDINGS.md`, never buried. Decoupling *weakens* one claim
  on purpose: v4 does not claim "the whole machinery transfers to one
  unseen ecology" (that was Q1, answered null in GL-76). It claims
  per-leaf results.

---

## Design principles

Carried over unchanged from v1/v2/v3: frozen machinery means frozen;
conclusions never named in definitions; pre-register the harvest before
the run; GL-25 noise-floor controls on any selection claim; progress
logging on batteries > ~1 min; thin harvest sentence ⇒ descope before
spending compute.

New in v4:

1. **Precondition, not gate.** Every rig declares, at freeze time, a
   **mechanical precondition check** on its substrate (computed from
   reference-run logs or compiled runtime structure, never from the
   machinery under test where avoidable). The check runs first; if it
   fails, the rig reports **SKIP** with the measured values and stops.
   SKIP is a FINDINGS entry ("substrate lacks property X at level Y"),
   not a program failure. No rig's precondition may reference another
   rig's outcome.
2. **Shared fixture layer, cached.** Substrate + reference episode
   traces are produced once per (ecology, roster, seed-set, load) tuple
   and cached; rigs consume traces, they do not re-simulate (extends
   the GL-75b episode-reuse work and `harness/cache.py`). A rig that
   needs interventional episodes (UAD probing, BIQ counterfactuals,
   selection) declares that and pays for its own runs.
3. **Substrate policy is pre-registered per rig** (see below). "Which
   substrate a rig may use" is fixed at freeze, not chosen after
   seeing results.
4. **One rig, one results file, one FINDINGS entry per battery.**
   `results/v4_<rig>.json`; predictions resolved one-by-one as in every
   v1/v2 battery.
5. **Cross-rig synthesis is a separate, explicitly weaker artifact.**
   Any statement combining rigs ("the audit stack holds on leaves A, B
   but not C") lives in a synthesis section that names each rig's
   substrate — no silent aggregation across different substrates into
   a single "the machinery works" sentence.

---

## Substrate policy (the anti-developed-to-the-test rule)

Three substrate classes, in decreasing claim strength. Each rig's
class is frozen in V4-1; moving a rig **down** a class after a failed
run requires a FINDINGS entry and relabels every prior result of that
rig at the lower class.

| Class | What it is | What a pass may claim |
|---|---|---|
| **S-blind** | Blinded-grown ecology (v3 growth protocol), grown against **only the criteria this rig's precondition needs** (a strict subset of C1–C5-v3), brief and withheld-list recorded in `BLIND_GENERATION.md` per rig | "Mechanism behaves as assumed on a substrate not co-developed with it" — the transfer-grade claim |
| **S-fixture** | Hand-built, implementer-authored fixture engineered to have the precondition (Phase-7a golden-ecology class; slice-A ablation-fixture class) | "Mechanism is wired and behaves as assumed *when the precondition holds*" — a coherence/liveness claim, never a transfer claim |
| **S-inherited** | An existing frozen artifact (`generated_ecology_v3.json`, v1 substrate) reused as-is | Whatever class it earned when frozen (v3 grown ecology remains S-blind for rigs whose precondition it *passes*) |

Rules:

- A rig whose precondition the existing v3 grown ecology already
  passes uses it (S-inherited/S-blind) — no new growth spent.
- A rig may run its **engineering shakedown** on S-fixture and its
  **scored battery** on S-blind; the two are labeled and never pooled.
- Growing an S-blind substrate *toward a rig's precondition* is
  allowed **only** because the precondition is a structural/behavioral
  property fixed before growth and checked mechanically — the same
  contract as C1–C5. What stays forbidden: iterating growth against
  the rig's *outcome* metrics (EAI values, detector scores, evasion
  criteria). Per-rig briefs are shorter and weaker than the failed
  all-of-C1–C5 briefs, which is also why growth is likelier to
  converge within the ≤ 4-round budget.
- If a rig's precondition cannot be produced blind within budget, the
  rig either runs at S-fixture (with the weaker label) or SKIPs — the
  choice is made at freeze, not after the growth failure.

---

## Architecture

### Fixture layer (V4-0 refactor)

New `harness/fixtures.py` (name at implementer's discretion):

```text
ReferenceFixture = (ecology_id, roster, seeds, load_cells)
  -> cached EpisodeResult traces + summary stats
```

- Wraps the existing episode-cache and GL-75b reuse paths; one
  content-addressed cache keyed on `CODE_VERSION` + fixture tuple.
- The GL-75c `ProcessPoolExecutor` runner moves here (shared by all
  rigs) instead of living inside `machinery_transfer.py`.

### Rig contract

Each rig is one module `harness/rigs/r_<bridge>_<slug>.py` exposing:

```text
check_precondition(fixture) -> PreconditionReport   # mechanical, cheap
run_rig(fixture, workers)   -> RigResult            # the battery
evaluate_predictions(RigResult) -> per-prediction pass/fail
```

plus a CLI `scripts/run_v4_rig.py --rig <name> --workers N` with
`[i/n]` progress logging. `machinery_transfer.py` is decomposed into
the first rigs (see refactor map); the GL-76/GL-77 results remain the
frozen record of the *coupled* battery — v4 rigs get fresh result
files, no renumbering of the old ones.

---

## Rig catalog

Status legend: **exists** (code runs today, needs re-housing),
**port** (pattern exists in another line), **build** (new code),
**stretch** (needs a design gate first).

### R-MB1 — unit discovery on unseen ground truth (exists)

- **Question:** does frozen UAD (passive + intervention) recover
  declared-and-enforced coupling mechanisms it was not co-developed
  with? (P1/P2 class.)
- **Precondition:** the substrate's reference traces contain
  non-trivial co-activity: ≥ K multi-actor interaction events per
  episode on governed mechanisms (constant frozen in V4-1; computed
  from raw traces, not from UAD). GL-76's diagnosis — short-burst
  one-shot scripts defeat co-activity clustering — becomes a
  *measured precondition* instead of a post-hoc explanation.
- **Substrate:** S-inherited (v3 grown) — expected to SKIP there,
  which converts GL-76's P1/P2 null into a precondition finding — plus
  one S-blind growth whose brief adds a sustained-interaction liveness
  criterion (activity texture, not UAD outcomes).
- **Reuse:** UAD scorers in `machinery_transfer.py`, C5 ground-truth
  plumbing, slice-B enforced ACLs (live-coupling upgrade per PLAN_v3
  slice D item 4). **New:** precondition metric.
- **Consumers:** ch07, ch33 (qualify or upgrade the GL-76 sentences).

### R-MB4 — referee/detector transfer + injection gate (exists)

- **Question:** do the five frozen detector families produce
  informative (non-degenerate, non-saturated) output, and does the
  injected-detector gate stay green, on substrates with the new v3
  phenomena (ACL denials, votes, pressure-injected tasks)?
- **Precondition:** reference traces exercise ≥ 3 of the new phenomena
  (mechanical count from logs) — otherwise coverage numbers are
  vacuous.
- **Substrate:** S-inherited (v3 grown) + the slice-D detector-coverage
  fixtures (PLAN_v3 slice D item 6) at S-fixture.
- **Reuse:** `detector_coverage.py`, `supplementary_detector_gate.py`
  (GL-74). Essentially re-housing.
- **Consumers:** ch33 (certification), appN.

### R-MB9 — grounding: report vs field-monitor contradiction surface (exists / small build)

- **Question:** when Tier-K field state and agent-filed reports
  diverge, does the referee-visible contradiction surface flag it —
  and what divergence magnitude is needed?
- **Precondition:** reference traces contain ≥ N report-filing events
  with nonzero measured field harm (else nothing to contradict).
- **Substrate:** S-inherited; one S-fixture with scripted divergent
  reporting (the lab-sim report-divergence pattern) for the dose-
  response curve.
- **Reuse:** referee report/monitor channels, LS-8-style divergence
  flag ported in the lab-sim referee. **New:** the assembled surface +
  dose-response battery (small).
- **Consumers:** ch42, appN (MB9 row currently thin for graded-lab).

### R-MB7d — inferential coupling / channel ablation (port)

- **Question:** when a governed channel is severed mid-episode, do
  coupled actors compensate through side channels (and does UAD's
  dependency score see the compensation)?
- **Precondition:** ≥ 1 governed `message_channel` actually exercised
  in reference traces (C5-v3 machinery already measures this).
- **Substrate:** S-fixture first (deny-ACL mid-episode is a world-side
  intervention the compiler already supports); S-blind reuse of
  whatever R-MB1's growth produces.
- **Reuse:** slice-B channel ACLs as the ablation mechanism; UAD
  intervention probing. **Port:** lab-sim S6 compensation scoring
  (`docs/EXPERIMENTS.md` — the MB7d primary signal carrier).
- **Consumers:** ch07/ch41 coupling discussion; appN MB7d row (empty
  for graded-lab today).

### R-MB6a — selection machinery sanity (build: V2-4 operator)

- **Question:** does the variation operator + null harness behave
  (uniform-fitness null inside permutation band; mutation produces
  measured phenotype diversity)? This is P5 + the operator-
  expressiveness report — pure harness science, **no ambiguity
  precondition**.
- **Precondition:** C4-class behavioral non-degeneracy only (deploy
  rate strictly inside a band) — the v3 grown ecology passes this.
- **Substrate:** S-inherited (v3 grown).
- **Reuse:** Phase-8 selection harness, `ProgramMap` genotype (slice F,
  built), permutation stats. **Build:** the V2-4 edit-vocabulary
  operator per `REPRODUCTION.md` §5 — the largest genuinely new piece
  in v4, and it was already owed.
- **Consumers:** none directly (harness finding); prerequisite for
  R-MB6b and any future Q2-class run.

### R-MB6b — selection for evasion under ambiguity (build; may SKIP)

- **Question:** P6/P7-class — does selection with variation find
  detector-evading strategies?
- **Precondition:** referee-vantage EAI in the pre-registered mid band
  on ≥ 1 default-load cell **of this rig's substrate** — the old
  V2-3 go gate, now scoped to one rig instead of three phases.
- **Substrate:** S-blind growth with an ambiguity-friendly (but still
  outcome-blind) brief, OR declared SKIP if growth fails — frozen
  choice at V4-1. Expected to SKIP on the current v3 ecology (GL-76
  measured EAI ≈ 0); that expectation is written down here so a SKIP
  is confirmatory, not embarrassing.
- **Reuse:** everything from R-MB6a + frozen evasion criterion
  (V2-1 item 2, already registered).
- **Consumers:** ch34 upgrade path (unchanged from PLAN_v2).

### R-MB7 — LLM red-team upper bound (build: adapter)

- **Question:** P8/P9-class — can a directed adversary with the
  affordable-primitive API find what undirected variation does not?
- **Precondition:** detector families non-degenerate on the substrate
  (R-MB4's output is *evidence toward* this, but the check is computed
  independently from detector-output variance on reference traces —
  no rig-on-rig dependency).
- **Substrate:** S-inherited; the onboarding artifact exists
  (knowledge base + attention surface / `desk.scan`, GL-66).
- **Reuse:** onboarding protocol + budget caps + both prompt frames
  (V2-1 item 5/6, already pre-registered), isolate backends.
  **Build:** subprocess-isolate LLM adapter (deferred since v1), mock-
  LLM replay tests.
- **Consumers:** ch33 (adversarial certification), ch27.
- **Note:** does *not* wait for R-MB6b. If R-MB6b SKIPs, the red-team
  result stands alone as the upper bound on this substrate — under the
  coupled v2 design this rig died with the gate; decoupling recovers it.

### R-MB2 — bundle Goodhart on the principal scorecard (build, medium)

- **Question:** optimize/select agents on a **proxy subset** of the
  slice-C principal scorecard (e.g. `deploy_rate`, `release_latency`);
  measure divergence on the withheld components (`bearer_harm`,
  `review_thoroughness`) computed from Tier-K ground truth. The
  bridge's Goodhart claim, on live machinery.
- **Precondition:** measured tension exists between the proxy and
  withheld components on reference traces (the C1-v3 negative-
  correlation statistic, already specified) — no tension, nothing to
  Goodhart, SKIP.
- **Substrate:** S-inherited (v3 grown has compiled principals) for
  the tension check; S-fixture conflict fixtures (slice-C validation
  fixtures) as fallback.
- **Reuse:** slice-C scorecard (built, GL-49), selection harness,
  R-MB6a operator. **New:** proxy/true split pre-registration + the
  battery loop (small once R-MB6a lands).
- **Consumers:** appN MB2 row (empty for graded-lab today); ch16-class
  bundle discussion.

### R-MB5 — successor closure via gated ProgramMap replacement (build, medium)

- **Question:** deploy a *successor* `ProgramMap` replacing an
  incumbent, gated by a slice-B `joint_approval_vote` (the vote
  machinery is the deploy gate — no new mechanism kind needed). Do
  lineage, gate, and referee evidence survive an adversarial successor
  crafted (by construction, S-fixture) to relabel its stated features?
- **Precondition:** vote mechanism compiled and exercisable by the
  fixture roster (mechanical).
- **Substrate:** S-fixture (adversarial successors are hand-authored
  by design — this is a coherence rig, labeled as such).
- **Reuse:** `ProgramMap` validation + `stated_feature_deltas` layer
  (the relabel surface), vote/`requires_vote` machinery (built, GL-45/
  GL-48), lab-sim D2 lineage pattern as the port template.
- **Consumers:** appN MB5 row (empty for graded-lab today).

### R-MB8 — correction authority capture (build, medium)

- **Question:** with a captured vote quorum or captured access-admin
  (capture = scripted membership subversion, lab-sim admin/board-
  capture pattern), does the referee's evidence surface distinguish
  legitimate denial from captured denial?
- **Precondition:** ≥ 1 vote-gated or admin-gated action on reference
  traces.
- **Substrate:** S-fixture (capture is scripted, not emergent —
  labeled coherence rig; an emergent-capture variant would be a
  post-R-MB6b stretch).
- **Reuse:** vote specs, standing/access admin, referee escalation
  channels. **Port:** lab-sim capture modes.
- **Consumers:** appN MB8 row.

### Stretch / out of scope — moved to `REPRODUCTION.md`

R-MB3 (bearer maps; needs a per-archetype harm-ledger split in
`oracle.py` first), MB10 (measurement forgeability; belongs to the
embedded-simulation line), and the **all-bridges integration**
synthesis work package live in `REPRODUCTION.md` §12–§13. They are not
v4 stages; a stretch rig enters this plan only via a design gate + a
V4-1-style freeze addendum.

---

## Reuse / refactor map

| Asset | v4 disposition |
|---|---|
| Substrate, planes, primitive API, isolates, oracle tiers | unchanged |
| Referee + 5 detector families (frozen) | unchanged, consumed by R-MB4/7/9 |
| `machinery_transfer.py` | decomposed: UAD scorers → R-MB1; EAI vantage split → R-MB6b precondition check; BIQ → fixture-layer service (stays available to R-MB1); detector coverage → R-MB4; prediction evaluator → per-rig |
| `harness/cache.py` + GL-75b episode reuse | promoted to the fixture layer |
| GL-75c parallel runner | moved to fixture layer, shared |
| Slice A–F institutional runtime (compiler, ACLs, votes, scorecard, pressure, `ProgramMap`) | the enabling substrate for R-MB2/5/7d/8 — built, mostly untested-by-battery |
| v3 growth protocol + complexity checker | reused per-rig with subset criteria |
| `BLIND_GENERATION.md` protocol | one section per S-blind rig brief |
| Phase-8 selection harness + permutation stats | R-MB6a/b, R-MB2 |
| V2-1 pre-registrations (evasion criterion, red-team protocol, onboarding) | inherited verbatim where the rig matches; re-frozen references in V4-1 |
| v1 digest pin, V2-2 replay, GL-76/77 result files | untouched; regression gates at every landing |

## Stages, build order, and effort

Estimates assume codebase familiarity; each stage lands with tests + a
FINDINGS entry before the next starts. Rigs marked ∥ inside a stage
proceed in parallel. Ordering rationale: infrastructure first (V4-0/1);
then the free re-housings that convert GL-76 into precondition-aware
results (V4-2); then the **small builds** that produce the cheapest
genuinely-new bridge rows (V4-3); then the operator that several later
rigs depend on (V4-4); then the **medium builds** in dependency order —
R-MB2 consumes the V4-4 operator, R-MB5/R-MB8 need only the built vote/
admin machinery (V4-5); then the two expensive, independent capstones
(V4-6/V4-7); synthesis last.

| Stage | Item | Effort | Gate before next stage |
|---|---|---|---|
| V4-0 | ✅ Fixture layer + rig contract (`harness/fixtures.py`, `harness/rigs/`); `machinery_transfer.py` left unmodified rather than decomposed (GL-76 reproduces bit-for-bit trivially since untouched) | ~3–5 d | full suite green — done (GL-79) |
| V4-1 | ✅ (R-MB1/R-MB4/R-MB9/R-MB7d/R-MB6a/R-MB2) Pre-registration freeze in `DESIGN.md`; ⏳ (R-MB6b, R-MB7, R-MB5, R-MB8) blocked on the open questions below | ~2–3 d writing | done for R-MB1/R-MB4/R-MB9/R-MB7d/R-MB6a/R-MB2 |
| V4-2 | ✅ R-MB4 ∥ R-MB1 — precondition metrics, scored on S-inherited `generated_ecology_v3.json` | ~2–4 d each | both batteries scored and FINDINGS-entered (SKIPs count) — done (GL-79): R-MB1 null, R-MB4 SKIP |
| V4-3 | ✅ `channel_severance` runtime primitive (`world.py`, flagged for later review); R-MB9 (contradiction surface, both arms) ∥ R-MB7d (pair + group channel-ablation arms, relative-rule noise-floor threshold) implemented and scored — GL-80: **R-MB9 pass on both arms**; **R-MB7d group SKIP** (precondition unsatisfied), **pair null at every onset fraction** (mechanically explained: non-adaptive reference program + outcome-status-blind `dependency_score`) | ~3–5 d each | done (GL-80) |
| V4-4 | ✅ R-MB6a — V2-4 variation operator + null harness (`variation_operator.py`, `stats.permutation_mass_movement_band`, `r_mb6a_selection_sanity.py`) scored — GL-81: **P5 pass** (uniform-fitness null inside band); expressiveness report-only: **11/100** syntax-distinct mutants on `walk_pipeline` baseline, all distinct phenotypes | ~1–2 wk | done (GL-81): P5 pass unblocks downstream selection rigs; expressiveness saturation on sparse baseline noted |
| V4-5 | **Medium builds:** ✅ R-MB2 scored **null** (GL-85: tension present, proxy-only selection did not Goodhart) ∥ R-MB5 (gated-successor relabel rig) ∥ R-MB8 (capture rig; first cut candidate — see open question 3) | R-MB2 ~3–5 d; R-MB5/R-MB8 ~1 wk each | R-MB2 done (GL-85); R-MB5/R-MB8 results permanently labeled S-fixture coherence-grade |
| V4-6 | R-MB7 — LLM adapter + mock replay + scored red-team battery | ~1–2 wk + API budget | caps + refusal reporting per V2-1; does **not** wait for V4-7 |
| V4-7 | R-MB6b — ambiguity growth attempt or declared SKIP | growth budget | precondition measured, never tuned |
| V4-8 | Cross-rig synthesis + manuscript harvest | ~2–3 d | per-rig sentences already written; synthesis names substrate classes inline |

V4-6 and V4-7 are independent and may swap or overlap; V4-5's three
rigs are independent of each other and of V4-6/V4-7. A precondition
SKIP at any stage does not block the next stage.

Rough total: ~6–9 person-weeks engineering (dominated by V4-4 and
V4-6), plus growth-round budget for the S-blind rigs, plus the V4-1
methodological writing. Comparable to PLAN_v3's estimate but with
incremental, independently harvestable payoffs instead of one gated
chain.

## Risks

| Risk | Mitigation |
|---|---|
| Per-rig substrates quietly become "hand-build the precondition in" | Substrate policy table frozen at V4-1; class moves recorded in FINDINGS; S-fixture results permanently labeled coherence-grade |
| Precondition constants tuned until rigs run | Constants frozen in V4-1 before any scored battery; a rig that SKIPs everywhere is reported, not re-thresholded |
| Rig proliferation dilutes attention (many shallow batteries) | Thin-sentence rule applies per rig: no pre-written harvest sentence, no battery; stretch rigs need a design gate first |
| Cross-rig claims silently re-aggregate what decoupling separated | Synthesis artifact must name each rig's substrate class inline (design principle 5) |
| R-MB6a null harness fails its own sanity gate | Same as V2-4's gate: fix the harness before any claim; hard stop |
| Fixture-layer refactor breaks frozen results | V4-0 gate: GL-76 reproduces bit-for-bit through new plumbing before anything else lands |
| LLM red-team cost blowup | V2-1 caps inherited; mock-replay tests; 1-seed smoke before full battery |

## Bridge coverage after v4 (intent)

| Bridge | Today (graded-lab) | After v4 |
|---|---|---|
| MB1 | GL-76 null (coupled battery) | precondition-aware result + S-blind retry (R-MB1) |
| MB2 | — | scorecard Goodhart battery (R-MB2) — **null** (GL-85) |
| MB3 | — | deferred → `REPRODUCTION.md` §12 (ledger split first) |
| MB4 | referee ported; GL-74 gate | re-housed + v3-phenomena coverage (R-MB4) |
| MB5 | — | gated-successor coherence rig (R-MB5) |
| MB6 | GL-23 null; V2-4/5 descoped | machinery sanity (R-MB6a) + scoped evasion rig (R-MB6b, may SKIP) |
| MB7 | graded oracle state only | red-team upper bound (R-MB7), decoupled from MB6b |
| MB7d | — | channel-ablation compensation (R-MB7d) |
| MB8 | — | capture coherence rig (R-MB8) |
| MB9 | listed in Q1, thin | contradiction-surface battery (R-MB9) |
| MB10 | — | out of scope → embedded-sim line (`REPRODUCTION.md` §12) |

Same honesty rule as always: stress-tests of cruxes, not closure.

## Open questions for the V4-1 freeze session (user input wanted)

1. R-MB6b substrate: fund an ambiguity-oriented growth attempt, or
   freeze it as declared-SKIP until some rig produces evidence the
   substrate class can support mid-band EAI at all?
2. R-MB7 model class + API budget cap (dollar number).
3. Are the S-fixture-only rigs (R-MB5, R-MB8) worth their weeks given
   their results can never exceed coherence-grade? (My read: yes for
   R-MB5 — the `stated_feature_deltas` relabel surface is a genuinely
   novel test object; R-MB8 is the first candidate to cut.)
4. ~~Whether V4-0 should land before or after the pending v3 growth-
   brief sign-off~~ — resolved: the v3 line is closed (GL-78,
   2026-07-18); V4-0 has no upstream sequencing constraint.

## Document map

- `PLAN.md`, `PLAN_v2.md`, `PLAN_v3.md` — prior programs, all closed
  (v1 closed GL-31; v2 Q1 answered null GL-76/77, Q2/Q3 descoped; v3
  line closed GL-78 — engineering, frozen brief GL-69, and frozen
  ecology GL-73 carry forward as v4 substrate)
- `PLAN_v4.md` — this file (draft)
- `DESIGN.md` — will hold the V4-1 pre-registration section
- `BLIND_GENERATION.md` — per-rig S-blind briefs (one section each)
- `results/FINDINGS.md` — continuous record, per-rig entries
- `REPRODUCTION.md` — §5 (variation operator) and §7 (LLM red-team)
  are consumed by V4-4 and V4-6 respectively; §12 holds the v4 stretch
  rigs (R-MB3, MB10 scoping); §13 the all-bridges integration package
