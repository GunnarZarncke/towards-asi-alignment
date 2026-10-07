# Eval registry split

Status: **step 5 of 7** (2026-10-07). Appendix P and the site hub now point at the claims registry ([site](https://aintelope.github.io/ai-safety-claims/), [source](https://github.com/aintelope/ai-safety-claims)). aintelope hosts it for now and is **not independent**, so `resolutionSource` stays false and attempts by aintelope or Gunnar Zarncke are not accepted. Runnable evaluations live in [`aintelope/ai-safety-claims-workbench`](https://github.com/aintelope/ai-safety-claims-workbench). Next: an independent host, then Metaculus for frozen contracts only.

**Stop:** delete or attic this file when the registry URL is the live resolution source (`resolutionSource` true after an independent host tags a snapshot). Markets without a published registry contract (other than Market 14) are not listable.

Lane: Predictions. Builds on [`assurance-risk-modelling.md`](assurance-risk-modelling.md) Phase 4 and [`bridge-prediction-markets.md`](bridge-prediction-markets.md). Public bars live in the registry; Appendix P keeps property paragraphs and pointers.

## Decision

Metaculus resolves a **named file in a third-party git repo**, not the literature. Exception: Market 14 (below). The book keeps the property each market tests and the three-way rule. The registry keeps the numeric bars, reporting, machine checks, and the snapshot admins read. TSA may submit attempts. TSA does not merge adjudication.

The registry maintainer adjudicates; Metaculus admins only read the snapshot. This supersedes “the host platform adjudicates” in [`bridge-prediction-markets.md`](bridge-prediction-markets.md) (Q1, Q6, P4) once a host owns the repo. [`resolution-advisors.md`](../../predictions/resolution-advisors.md) stays a candidate list for maintainers, nothing more.

**Same meaning as the appendix.** The registry must not change what YES, NO, or OTHER means. Published work counts even if its authors never file it (wrapped attempts, below). Process rules come from the appendix box per market; no default may be stricter than the box.

**Market 14 is outside the registry.** Its evidence is a few public dated documents (criteria, approving body, decision record), with no score table, statistics, hidden suite, or adversarial route. It lists directly on Metaculus from its box, the platform adjudicates, and it has two outcomes: YES if every box condition is met, NO otherwise. No OTHER. Box and reading rules updated 2026-10-06.

Sibling repo name: **`ai-safety-claims`** (directory beside this repo, not inside it). Transfer the GitHub org before any question URL is frozen.

## What already exists

Nothing public scores “did this attempt meet frozen bars for market *k*?” as YES / NO / OTHER. Neighbors, and what to borrow:

| Place | What it is | Use |
|-------|------------|-----|
| [Hugging Face Community Evals](https://huggingface.co/blog/community-evals) ([eval results](https://huggingface.co/docs/hub/eval-results)) | Benchmark `eval.yaml` plus one numeric score per model in `.eval_results/*.yaml`. “Verified” means an Inspect/LightEval job on HF, not our bars. | Optional mirror of **runnable** code or logs. Not the resolution source. |
| [Inspect Evals register](https://github.com/UKGovernmentBEIS/inspect_evals/blob/main/EVAL_REGISTER.md) | Pointer to a pinned commit of an eval in the author’s repo. | Register runnable task code. Do not resolve the contract from the register. |
| [Every Eval Ever](https://github.com/evaleval/every_eval_ever) | Shared schema for model × eval scores. | Export numeric rates for reuse. Metaculus still reads our status file. |
| [METR task standard](https://github.com/METR/task-standard) | Agent task package format. | Hidden suites that are tasks. Not a claims ledger. |
| [AISafety.com map](https://www.aisafety.com/map), [aisafetyagendas.com](https://aisafetyagendas.com/) | Directories. | Link to a row. Do not host status. |

## Who owns what

| Layer | Keeps | Loses |
|-------|--------|--------|
| Appendix P | Property in one paragraph, resolve-by (UTC), three-way rule, registry id + contract version, “closest existing work,” aggregation and \(F/R/U\) | Checklists, sample floors, Clopper–Pearson, independence procedure, literature search |
| `metadata/predictions.yml` | Ids, bridges, status, short/long titles | The `bars:` summaries once the contract file is canonical |
| Companion site | Hub, cards, Metaculus iframe, safety-case demo | Scoring UI |
| **`ai-safety-claims`** | Contracts, attempts, validation, resolution snapshots, thin UI | Thesis, Lean, odds model |
| Metaculus | Price of the snapshot | Reading papers |

**Source order for bars:** the registry contract at `contractVersion` in `predictions.yml` is authoritative. The appendix does not restate numeric bars. Market 14 is the exception (box only).

A YES in the registry is still not an `MB*` discharge. Prices still do not enter the safety-case demo as parameters.

## Registry and workbench (public 2026-10-07)

Sibling checkouts `../ai-safety-claims` ([registry](https://github.com/aintelope/ai-safety-claims)) and `../ai-safety-claims-workbench` ([workbench](https://github.com/aintelope/ai-safety-claims-workbench)). They are the canonical place for everything this plan used to spell out; do not duplicate it here:

| Topic | Where |
|-------|-------|
| Vocabulary, attempt id format, filing rules, evidence files, deadlines | `ai-safety-claims/README.md` |
| Interim host, host criteria, conflicts, disputes, tags, decoupling | `ai-safety-claims/GOVERNANCE.md`, `registry.yaml` |
| File formats (attempt, freeze, frozen cases, trial record, adapter, adversarial route, suite manifest, adjudication, contract, outcome) | `ai-safety-claims/schemas/` |
| Shared rules copied from Appendix P, plus registry rules (exercised bars, evidence, hash-only hidden suites) | `ai-safety-claims/shared-rules/common-v1.yaml` |
| Contracts: Markets 1–13 and 15–18, `frozen` as versions (2026-10-07); not a resolution source | `ai-safety-claims/market-contracts/` |
| Check order and reasons (reporting → dates → qualification → maintainer checks → bars) | `ai-safety-claims/validator/engine.py` docstring |
| Sketches (unfinished attempts no outcome reads), dry run, submit, adjudication helpers | `ai-safety-claims/sketches/README.md` |
| Fictional scenarios with intended outcomes fixed before their first run | `ai-safety-claims/examples/README.md` |
| Registry-side plans and progress | `ai-safety-claims/docs/plans/` |
| Running an evaluation: freeze, run, export a sketch (Inspect by default) | `ai-safety-claims-workbench/README.md` |

The score table is no longer self-reported: every attempt carries its frozen cases, per-trial records, and raw log, and the validator re-derives the table from them. The site publishes `ui/index.html` on every push after `validator check`.

## Per market: what goes in the contract

Guide for Markets 19–21 (catalog 1–18 except 14 is copied and frozen as versions). Each contract copies its box verbatim, sets `adversarialBudget` and `freezeOrder` from the box (never stricter), and lists ambiguities under `openQuestions` instead of deciding them. Markets 19–20 need `stack` and `challenge` attempt types and the tournament order: protocol published → registration window → registration closes → hidden cases built after close → stacks evaluated → optional Market 20 challenge against one ACCEPT. Market 19: if a tournament-wide condition fails, no stack qualifies (OTHER). Market 20: YES/OTHER only.

| # | Contract adds | Validator reads from score table | Human (adjudication) |
|---|---------------|----------------------------------|----------------------|
| 1 | Hidden-suite manifest spec; five system families; per-system freeze fields | ID rate; false complete-boundary + 95% upper bound; coverage | Subset adversarial after freeze; broadly capable |
| 2 | Pair and conflict lists; intervention statistic frozen before outcomes | Distinguishing / direction / intervention accuracies | Hidden trade-offs trained; ≥2 families |
| 3 | Four failure families; mechanical ground-truth required | Target accuracy; false acceptance | Ground truth is mechanical |
| 4 | Episode freeze; sham types | Uptake, persistence, sham rate; n≥100 | Serious adversarial route; not tool-removal only |
| 5 | Four attack families; planted bypasses | Per-family success; bypass discovery | Auditor is the designated component |
| 6 | Seven checks; one-failure-at-a-time; version ids | Detection overall and per check; false-safe | Fresh audit per successor version |
| 7 | Trajectory table; pre-outcome signed estimate | n≥20; AUROC; false-safe; CI bound if n<40 | ≥2 selection mechanisms; deployment-like process |
| 8 | Five channel families; complete-interface controls | Detection overall and per family; false “sufficient”; true-complete floor | Adversarial incomplete subset after freeze |
| 9 | Bound issued before hidden tasks | Bound holds ≥95%; median bound; planted-route detection | Serious adversarial route |
| 10 | Same tuple for correction, hidden-route bound, bypass | In-regime attack rate + bound; out-of-regime gap; entry bars via `dependsOnAttempts` | Same system/version/monitor/threat |
| 11 | Mechanism labels; coupling intervention | AUROC; concealed recall; false-positive rate | Labels from mechanism, not correlation |
| 12 | Shift labels; proxy ranges | Update rate; false green; unnecessary escalation | Serious adversarial route; broadly capable |
| 13 | Frozen audit id; seven checks; hidden-harm family | False-safe; repeatable family cap; true-pass; hidden-harm detection | White-box adversarial; attackers had audit |
| 14 | No contract: lists directly on Metaculus, YES/NO (see Decision) | — | — |
| 15 | Bundle manifest; six composition fault tags | Reject/flag rates; false accept; true accept | Incompatibility subset after freeze |
| 16 | Frozen environment, shocks, signed estimate | Inside vs outside correction rates | ≥2 selection mechanisms; serious adversarial |
| 17 | Unfamiliar kinds; mechanical ground truth | Exclusion/inclusion/abstention rates | Adversarial subset; mechanical labels |
| 18 | Frozen setting, prohibited class, coherence checks | In-regime harm rate + bound; out-of-regime worse; entry certificates via `dependsOnAttempts` | Serious adversarial; certificates coherent |
| 19 | Protocol + bracket fills; tournament vs per-stack rules | Clopper–Pearson at \(1-0.05/k\); clean/broken-control accepts | Statements; independence; per-case overrides summary |
| 20 | Challenge doc; stack ACCEPT pointer; listed families | Log completeness; finds match ACCEPT∧failing | ≥2 independent red teams; stack unchanged |
| 21 | Internal object, checkpoint, frozen counterpart | On-object vs control intervention rates | Serious adversarial; broadly capable |

The table is a summary. Each contract copies its full box, including items left out here (e.g. Market 4 channel-preservation family, Market 9 ≥70% unrestricted success, Market 11 ≥2 mechanisms). Markets 19–20 contracts carry the admin-trial rules verbatim from the box (signed statements, per-case data over the summary table, any amendment is a new version, deployment-class boundary, barred-targets list).

Markets 19–21 may stay `draft` in contracts until Phase 4. Partials are valid: complete score table, `barsMet: false`.

## Appendix P after the split

Rewrite only after the registry URL and `contractVersion` exist. Update `INSTRUCTIONS.md` Appendix H scope in the same pass.

**Stays, shortened (catalog 1–18 except 14):** opening; three-way rule; catalog table; per-market property paragraph + registry pointer; closest existing work; aggregation and \(F/R/U\); Market 21 wrapper note.

**Stays full-box in Appendix P until Phase 4:** Markets 19–21 (not copied to the registry in step 5).

**Moves to `ai-safety-claims`:** common qualification, glossary procedure, adapter rules, per-market YES lists, unit rules; Market 19–20 fill guidance moves only when those contracts are copied.

**“How a market can resolve”** shrinks to: published work counts whoever files it; the registry maintainer adjudicates; OTHER means no qualifying attempt, not a missing snapshot.

**Metaculus question text:** `ai-safety-claims/listing-template.md` (admin-trial-tested; title, dates, criteria, fine print with Zenodo concept DOI and annulment rules).

## Site

| Surface | Change |
|---------|--------|
| `/predictions/` hub | Line under each panel: registry outcome + link to `ai-safety-claims` tag. Separate from listing status and Metaculus iframe. |
| Prediction cards | After shrink: short property + contract link, not duplicated bars. |
| `metadata/predictions.yml` | Add `registryRepo` and `snapshotTag` when URL exists (`contractVersion` already exists). Pin tag; do not track `main`. Drop `bars:` at the shrink. |
| `/predictions/safety-case/` | Unchanged. Registry YES is not a demo preset until Phase 4 allows it. |

## Listing

After host transfer:

1. Metaculus series quotes tag, `market-outcomes/market-NN-vK.json`, Zenodo fallback, annulment rule.
2. Admin opens that file at the tag and reads `outcome` (~15 minutes).
3. Draft contracts → not listed.
4. Market 20: YES / OTHER only. Market 14: YES / NO only, listed from the box without the registry.

## TSA submissions

- Until an independent host owns the registry, attempts submitted or authored by aintelope or Gunnar Zarncke are not accepted (`GOVERNANCE.md`). Sketches are fine, since no outcome reads them: the first is the lab-simulation intervention UAD sketch for Market 1 (`sketches/zarncke-2026-10-07-lab-sim-intervention-uad/`, frozen and run in the workbench).
- After the transfer: no merge on `adjudication/` or `market-outcomes/`.
- Partials are success for the registry, not a book claim of bridge discharge.
- Seed a non-TSA example attempt before the first TSA row.

## Order of work

1. This plan (done).
2. Scaffold **`ai-safety-claims`** (done 2026-10-06; public under `aintelope` 2026-10-07 with Apache-2.0 / CC BY 4.0, CI, and the Pages site). The contracts' `openQuestions` were settled in the chapters (G1–G7). Added 2026-10-07: exercised-bars rule (also in the Appendix P reading rules), sketches and contributor tools, evidence files behind every score table, and the workbench repo.
3. Admin re-trial (done 2026-10-06): admin agent 6/6 cases as intended, posting defects fixed in `listing-template.md`; maintainer agent found the intended check sets, and its findings became rule text (human-check triggers, fail vs unsettled, per-instance certificate check, `freezeEvidence` for wrapped attempts) or contract `openQuestions`. Agent agreement is one instrument; rerun both trials after the open questions are settled.
4. Independent host (Plex first; host criteria in `GOVERNANCE.md`). aintelope hosts in the meantime, without resolution power. Transfer org. Tag `snapshot-0` (all OTHER).
5. Shrink Appendix P and site to pointers (done 2026-10-07). Sync predictions.
   Decouple fully, not only shorten: the registry's contracts and shared rules become the authoritative text; the registry may hold non-TSA contracts and diverge from or drop TSA ones; contract versions number independently of the book. Needed for host independence. Recorded in `ai-safety-claims/GOVERNANCE.md` § Decoupling from the manuscript.
6. Metaculus for frozen contracts only.
7. Optional: Inspect register, Every Eval Ever export, HF for logs — none replace `market-outcomes/`.

## Open questions for the author (before any contract is frozen)

Settled: the questions the contracts first listed (Market 1 floor and denominators, adversarial effort, toy versus constructed systems, "previously unseen"; Market 4 persistence, episode floor, per-case bars) are in the chapters, the boxes, and the contracts; see [`chapter-gaps-from-contracts.md`](chapter-gaps-from-contracts.md) G1–G7.

Settled (2026-10-07 author picks; registry text in `ai-safety-claims/shared-rules/common-v1.yaml` and Market 1 contract). These rules are **fixed for this contract version**. Later versions, if any, go through the usual community process for new contract versions; that is not an open question now.

1. **Minimum negative cases.** One design-supplied case per bar is enough (`exercisedBars` / `exercisedBy`). No extra floor for Market 4 fake corrections or Market 1 correlation-not-control systems beyond that.
2. **Distinct benchmark systems (Market 1).** Different seeds count as distinct.
3. **"Unlabeled" when interventions rerun the system (Market 1).** Rerunning a system with its own configuration counts as allowed access, not as reading labels.
4. **Who assigns families (Market 1).** **Maintainer check** that each scored system belongs to the families the benchmark claims.
5. **Checking the freeze fields (Market 1).** The attempt must **show per scored system** that perturbing the unit hits the minimum change and that removing a non-listed component stays in the no-effect range.
6. **Several trials per case.** **One trial per case** only (validator rejects a second trial for the same `case_id`). Repeated runs are not allowed.

Registry-only follow-ups live in `ai-safety-claims/docs/plans/registry-open-questions.md`.

## Not in this split

- New bridges or bar changes smuggled in as schema tweaks.
- \(F/R/U\) or odds demo inside the registry.
- Resolving from LW tags, AISafety.com map, or HF leaderboards.
- Listing while the author can merge `market-outcomes/`.
