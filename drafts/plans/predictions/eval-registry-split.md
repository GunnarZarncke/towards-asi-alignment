# Eval registry split

Status: **step 4 of 7** (2026-10-06). Registry scaffolded locally and re-trialled; host next, after the author settles the open questions below. Do not rewrite Appendix P or list on Metaculus until a host org owns the sibling repo.

**Stop:** delete or attic this file when the registry URL is the live resolution source and the appendix boxes have been cut to pointers. Until then, a market whose bars still live only in the TeX box is not listable.

Lane: Predictions. Builds on [`assurance-risk-modelling.md`](assurance-risk-modelling.md) Phase 4 and [`bridge-prediction-markets.md`](bridge-prediction-markets.md). Public contracts stay in `appendices/appP-bridge-predictions.tex` until the rewrite in “Appendix P after the split”.

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

**Source order for bars:** Appendix P box → `contract-vK.yaml`, K = the book's `contractVersion` in `predictions.yml` (copied, then checked against the box by hand) → appendix shrinks to a pointer and `predictions.yml` drops `bars:`. Until the shrink, the TeX box wins on any disagreement. The `scientific` / `adversarialValidation` / `reportingInterface` split already in `predictions.yml` seeds the contract's bars vs qualification fields.

A YES in the registry is still not an `MB*` discharge. Prices still do not enter the safety-case demo as parameters.

## Registry scaffold (built 2026-10-06)

Local sibling repo **`../ai-safety-claims`** (git init, uncommitted, no GitHub remote). It is now the canonical place for everything this plan used to spell out; do not duplicate it here:

| Topic | Where |
|-------|-------|
| Vocabulary, attempt id format, filing rules, deadlines | `ai-safety-claims/README.md` |
| Host criteria, conflicts, disputes, tags, transfer | `ai-safety-claims/GOVERNANCE.md` |
| File formats (attempt, adversarial route, suite manifest, adjudication, contract, outcome) | `ai-safety-claims/schemas/` |
| Shared rules copied from Appendix P (qualification, adversarial routes and budgets, glossary, judgment stack, wrapping, statistics, deadlines, common human checks) | `ai-safety-claims/shared-rules/common-v1.yaml` |
| Contracts: Markets 1 and 4, v1 `draft`, each with `openQuestions` | `ai-safety-claims/market-contracts/` |
| Check order and reasons (reporting → dates → qualification → maintainer checks → bars) | `ai-safety-claims/validator/engine.py` docstring |
| Four fictional scenarios with intended outcomes fixed before the first run | `ai-safety-claims/examples/README.md` |

`python -m validator check` and `python -m validator test` pass (2026-10-06; quoted in the session log). Rules the scaffold settled: `wrapped` attempts filable by anyone; per-contract `adversarialBudget` and `freezeOrder` copied from the box; 60-day window, tag at its end, annul 30 days later; one outcome file per contract version; `dependsOnAttempts`; submitter-set outcome fields fail the build; `resolutionSource: false` in every outcome file until a host owns the repo.

## Per market: what goes in the contract

Guide for copying the remaining contracts (Markets 1 and 4 are done). Each contract copies its box verbatim, sets `adversarialBudget` and `freezeOrder` from the box (never stricter), and lists ambiguities under `openQuestions` instead of deciding them. Markets 19–20 need `stack` and `challenge` attempt types and the tournament order: protocol published → registration window → registration closes → hidden cases built after close → stacks evaluated → optional Market 20 challenge against one ACCEPT. Market 19: if a tournament-wide condition fails, no stack qualifies (OTHER). Market 20: YES/OTHER only.

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

**Stays, shortened:** opening; three-way rule; catalog table; per-market property paragraph + registry pointer; closest existing work; aggregation and \(F/R/U\); Market 21 wrapper note.

**Moves to `ai-safety-claims`:** common qualification, glossary procedure, adapter rules, per-market YES lists, unit rules, Market 19–20 fill guidance.

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

- Path: `submitted-attempts/tsa-<date>-<slug>/`.
- No merge on `adjudication/` or `market-outcomes/` after transfer.
- Partials are success for the registry, not a book claim of bridge discharge.
- Seed a non-TSA example attempt before the first TSA row.

## Order of work

1. This plan (done).
2. Scaffold **`ai-safety-claims`** (done 2026-10-06, local only): schemas, validator, contracts for Markets 1 and 4, `challenge-runs` fixture, `wrapped` example, four scenarios, static UI, CI workflow. Open before publishing it: license, GitHub location, author settles each contract's `openQuestions`.
3. Admin re-trial (done 2026-10-06): admin agent 6/6 cases as intended, posting defects fixed in `listing-template.md`; maintainer agent found the intended check sets, and its findings became rule text (human-check triggers, fail vs unsettled, per-instance certificate check, `freezeEvidence` for wrapped attempts) or contract `openQuestions`. Agent agreement is one instrument; rerun both trials after the open questions are settled.
4. Host (Plex first; host criteria in `GOVERNANCE.md`). Transfer org. Tag `snapshot-0` (all OTHER).
5. Shrink Appendix P and site to pointers. Sync predictions.
6. Metaculus for frozen contracts only.
7. Optional: Inspect register, Every Eval Ever export, HF for logs — none replace `market-outcomes/`.

## Open questions for the author (before any contract is frozen)

Checked against the chapters and Lean (2026-10-06; Market 1: Ch. 1, 7, `Evidence.lean`, `Core.lean`, `Defeaters.lean`; Market 4: Ch. 25, 26, 29, `Correction.lean`, `MB4CorrectionIntegrity.lean`, `Evidence.lean`). Where the book gave one answer it went into the box and the contract (Market 1 → v2, Market 4 → v3):

- Market 1: "unlabeled" = no agent-membership labels or prior ontology; interventions allowed (Ch. 7 "recovered from observations and interventions", "without a unit that is already known to be an agent"). The adversarial subset is ambiguous, composite, transformed, or adversarially presented control processes (Ch. 7 generator–detector game).
- Market 4: verbal agreement without behavior change is a failed genuine correction, not a sham (Ch. 25 "listens politely but does not change has no correction channel"). A captured or rerouted channel invalidates the certificate: zero successful channel captures, the 10% cap applies to fake/unauthorized inputs only (Ch. 26 `ValidRef` Boolean gate, "invalid rather than merely low-scoring").

Still open (book silent or plural; listed under `openQuestions` in `ai-safety-claims/market-contracts/market-01/contract-v2.yaml` and `market-04/contract-v3.yaml`): Market 1 floor and denominators, minimum adversarial effort, toy exclusion vs constructed systems, "previously unseen"; (Market 4 settled by the author 2026-10-06: persistence over all genuine corrections; the 100-episode floor pools genuine and sham; bars per required correction case, at least 20 genuine each; the unit rule does not bite because the rates are within-system rates.) Chapter gaps, with suggested resolutions: [`chapter-gaps-from-contracts.md`](chapter-gaps-from-contracts.md).

Settle each in the box first (the appendix wins), then copy into the contract and drop the `openQuestions` entry.

## Not in this split

- New bridges or bar changes smuggled in as schema tweaks.
- \(F/R/U\) or odds demo inside the registry.
- Resolving from LW tags, AISafety.com map, or HF leaderboards.
- Listing while the author can merge `market-outcomes/`.
