# Eval registry split

Status: **plan** (2026-10-06). Not implemented. Do not rewrite Appendix P or list on Metaculus until a host org owns the sibling repo.

**Stop:** delete or attic this file when the registry URL is the live resolution source and the appendix boxes have been cut to pointers. Until then, a market whose bars still live only in the TeX box is not listable.

Lane: Predictions. Builds on [`assurance-risk-modelling.md`](assurance-risk-modelling.md) Phase 4 and [`bridge-prediction-markets.md`](bridge-prediction-markets.md). Public contracts stay in `appendices/appP-bridge-predictions.tex` until the rewrite in §6.

## Decision

Metaculus resolves a **named file in a third-party git repo**, not the literature. The book keeps what a YES means. The registry keeps reporting, machine checks, and the snapshot admins read. TSA may submit attempts. TSA does not merge adjudication.

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
| `metadata/predictions.yml` | Ids, bridges, status, short/long titles | Duplicated bar prose once the contract file is canonical |
| Companion site | Hub, cards, Metaculus iframe, safety-case demo | Scoring UI |
| **`ai-safety-claims`** | Contracts, attempts, validation, resolution snapshots, thin UI | Thesis, Lean, odds model |
| Metaculus | Price of the snapshot | Reading papers |

A YES in the registry is still not an `MB*` discharge. Prices still do not enter the safety-case demo as parameters.

## Vocabulary

| Term | Meaning |
|------|---------|
| **Market contract** | Frozen YES/NO/OTHER rules for one catalog row (`market-01` … `market-21`), versioned. What the book appendix currently puts in each box. Lives under `market-contracts/`. |
| **Attempt** | One team’s claim that they ran an evaluation against a market contract. Lives under `submitted-attempts/`. |
| **Attempt id** | Directory name for one attempt (see below). |
| **Score table** | The tabular evidence the checker reads to recompute rates (`score-table.csv` or `.json`). Not a leaderboard score — per-unit or per-case rows. |
| **Adjudication** | Maintainer-only file that records human calls the checker cannot make (independence, adversarial route, mechanical ground truth). |
| **Resolution snapshot** | Generated `market-outcomes/market-NN.json` at a git tag — the Metaculus object. |

Do not use “pack” in the repo; use **market contract**.

## Attempt id format

One attempt = one directory:

```text
{submitter}-{date}-{slug}
```

| Part | Rule | Example |
|------|------|---------|
| `submitter` | Lowercase org or person slug; `[a-z0-9-]`, 2–32 chars | `tsa`, `metr`, `plex`, `acme-lab` |
| `date` | ISO date when the attempt folder is **first opened** (registration), not resolve date | `2027-03-14` |
| `slug` | Short label for this run; `[a-z0-9-]`, 2–48 chars | `embedded-v1`, `att-tournament-stack-3` |

Full example: `tsa-2027-03-14-embedded-v1`

Rules:

- Ids are unique repo-wide. If the same team reruns, increment the slug (`embedded-v2`) or date.
- The id is fixed at first PR; do not rename after the method or suite is frozen for that attempt.
- `attempt.yaml` repeats the id and lists `market`, `contractVersion`, `submitter`, `contact`.

## Score table (`score-table.csv`)

Machine-readable rows the validator recomputes into rates and confidence bounds. Column names come from `market-contracts/market-NN/required-columns.yaml`. Common columns:

| Column | When used | Meaning |
|--------|-----------|---------|
| `unit_id` | Almost always | Independent unit after collapse (one system, trajectory, or attack seed). |
| `case_id` | Per-case markets | Row within a unit. |
| `label` | Hidden-set markets | Ground-truth or frozen outcome label (e.g. `clean`, `represented_failure`, `should_pass`). |
| `predicted` | Classifiers | Method output (accept, refuse, abstain, named component, etc.). |
| `correct` | When label and prediction are comparable | Boolean or enum for accuracy numerators. |
| `abstain` | Certificate markets | Whether the method abstained on this unit. |
| `family` | Subgroup bars | Channel family, fault type, domain, selection mechanism, etc. |
| `in_regime` | Composition markets (e.g. 10, 16, 18) | Whether the case is inside the claimed deployment or selection regime. |
| `stated_bound` | Market 9 | Upper bound issued before hidden tasks for this case. |
| `actual_rate` | Market 9 | Observed hidden-route success for this case. |
| `score` | AUROC markets (7, 11) | Continuous predictor or detector score per trajectory. |
| `outcome_binary` | Market 7, 16 | Whether correction was later lost (0/1). |

The validator aggregates these into the contract’s rates (accuracy, false-safe rate, AUROC, bound calibration, etc.). Submitters do not put `qualifying`, `barsMet`, or market `outcome` in any file they author.

Optional companion files (named in the contract):

- `manifest.yaml` — list of hidden systems, episodes, or bundles (metadata only; secrets stay off-repo).
- `documents/` — hashes and URLs for Market 14–style governance evidence.
- `signed-statements/` — dated statements referenced by the contract.
- `artifact-url.txt` — URL + SHA-256 of the full public artifact (paper repo, HF dataset, Zenodo bundle).

## Adversarial and hidden elements

Many markets require a **hidden benchmark** (evaluators see labels; the method under test does not) and/or **serious adversarial evaluation** (independent red teams, bounty, or automated attack generator). The registry splits **who does what** and **what is secret when**.

### Three roles

| Role | Who | Responsibility |
|------|-----|----------------|
| **Submitter** | Lab, TSA, tournament stack team | Registers the method or stack; publishes score tables and artifacts for **their** run; signs statements about data they used. |
| **Challenge operator** | Independent org (often not the submitter) | Builds hidden cases or runs the adversarial route **after** the relevant freeze; publishes labels, logs, or suite hashes the contract names. |
| **Maintainer** | Host org (Plex, etc.) | Merges adjudication; runs the validator; commits resolution snapshots. Does not author hidden cases for markets they also submit to without a conflict process in `GOVERNANCE.md`. |

### Timeline (default for hidden-set markets 1–18)

Applies unless the market contract says otherwise (Markets 19–20 use the tournament timeline in §4.1).

```text
1. Contract frozen        market-contracts/market-NN/ at version N (git tag)
2. Method freeze          submitter publishes what they freeze (method hash, audit spec, etc.)
3. Attempt registered     submitted-attempts/<attempt-id>/ opened; attempt.yaml only
4. Hidden suite built     challenge operator builds holdout AFTER step 2; suite hash registered
5. Evaluation run         submitter scored on hidden set; score table + artifact published
6. Adversarial attestation challenge operator OR submitter documents which of the three
                          common routes was used + hours/bounty/generator evidence
7. Validation             CI recomputes rates from score table
8. Adjudication           maintainer fills human fields (independence, route, ground truth)
9. Snapshot               market-outcomes/market-NN.json updated at deadline tag
```

**What stays off the public repo:** raw hidden prompts, unreleased model weights, sealed tournament cases before the resolve-by date. The repo holds **hashes**, **counts**, **labels after release**, and **pointers** to downloadable artifacts.

### What the submitter files vs what the operator files

| Evidence | Typical submitter path | Typical operator path |
|----------|------------------------|------------------------|
| Method / stack freeze hash | `attempt.yaml` + artifact URL | — |
| Hidden suite existence + hash | `attempt.yaml` → `hiddenSuiteHash`, `hiddenSuiteReleasedAt` | `challenge-runs/market-NN/<run-id>/suite-manifest.yaml` (maintainer or operator repo linked from attempt) |
| Score table on hidden labels | `score-table.csv` | — |
| Adversarial route (3 red teams / bounty / generator) | `adversarial-route.yaml` in attempt **or** link to operator run | `challenge-runs/.../adversarial-route.yaml` |
| Signed statements | `signed-statements/` | Operator statements in the challenge run folder |
| Independence | — | Adjudication only (maintainer) |

For **v1**, put challenge-operator artifacts either in `challenge-runs/market-NN/<run-id>/` (same repo, operator opens PR) or at an external URL with hash in `attempt.yaml`. The attempt must name the run id so the validator can check cross-links.

### Tournament timeline (Markets 19–20)

Order is fixed in the contract; the registry enforces it with separate attempt types:

```text
1. Protocol published       challenge-runs/market-19/<protocol-id>/protocol.pdf + hash
2. Registration window      stack teams open submitted-attempts/... (registration only)
3. Registration closes      no new stack attempts
4. Hidden cases built       operator commits suite hash + label manifest AFTER close
5. Stacks evaluated         each stack attempt gets score-table + per-case file URL
6. Market 20 (optional)     separate attempt type `open-world-challenge` against one ACCEPT
7. Snapshot                 market-outcomes/market-19.json / market-20.json
```

Market 19: **no stack qualifies** if tournament-wide conditions fail → market outcome OTHER. Market 20: **no performance bar**; YES means the challenge was run and published in qualifying form.

### How hidden/adversarial fields become qualifying or not

The validator checks:

- Required columns and files present.
- Numeric bars from `score-table.csv`.
- `hiddenSuiteReleasedAt` ≤ resolve-by and `hiddenSuiteHash` matches the operator manifest linked in the attempt.
- `adversarialRoute` is one of the three named routes and required fields for that route are filled (group count, hours, bounty dates, or generator yield on planted controls).

The maintainer adjudicates (non-exhaustive):

- Teams were **independent** per `common-v1.yaml`.
- Hidden subset was built **after** the method freeze timestamp in `attempt.yaml`.
- **Broadly capable** system requirement met.
- **Mechanical ground truth** for markets that require it.
- Tournament statements not contradicted by published logs.

If a load-bearing human field is missing or disputed at the deadline → that attempt is **not qualifying** (`unresolved-judgment`), not a silent YES. Market roll-up unchanged: YES if any qualifying attempt met bars; NO if every qualifying attempt missed; OTHER if none qualified.

## Repo layout (`ai-safety-claims`)

Gunnar may scaffold; merge rights on `adjudication/` and `market-outcomes/` leave with host transfer.

```text
ai-safety-claims/
  README.md
  GOVERNANCE.md             # host, conflicts, transfer, Zenodo fallback

  schemas/                  # JSON Schema for attempt, adjudication, market-outcome
  shared-rules/
    common-v1.yaml          # qualification, adversarial routes, glossary, unit rule

  market-contracts/         # frozen YES bars (one folder per catalog row)
    market-01/
      contract-v1.yaml      # bars, sample floors, required files
      required-columns.yaml # score-table columns for this version
    market-02/
      ...
    market-19/
      contract-v1.yaml      # may be marked draft until Phase 4

  submitted-attempts/       # one folder per attempt id
    tsa-2027-03-14-embedded-v1/
      attempt.yaml          # market, contractVersion, submitter, freeze timestamps
      score-table.csv
      adversarial-route.yaml   # if applicable
      signed-statements/
      artifact-url.txt
      manifest.yaml            # optional; no secrets

  challenge-runs/           # hidden suites, tournaments, red-team campaigns
    market-19/
      att-2027-v1/
        protocol.yaml       # filled brackets, URL, SHA-256
        suite-manifest.yaml # after registration close; unit labels
        adversarial-route.yaml
    market-08/
      aisi-2027-holdout-1/
        suite-manifest.yaml

  adjudication/             # maintainer-only human calls (repo regulars know this name)
    market-01/
      tsa-2027-03-14-embedded-v1.yaml

  market-outcomes/          # generated; Metaculus reads these
    market-01.json
    market-08.json
    ...

  validator/                # recomputes rates; fails if submitter set outcome fields
  resolution-tags/          # notes for git tags snapshot-YYYY-MM-DD (optional README per tag)
  examples/                 # fixture attempts + expected validation output
  ui/                       # static site: contracts, attempts, outcomes
```

### `market-outcomes/market-NN.json` (Metaculus object)

```yaml
market: market-08
contractVersion: 1
asOf: 2027-12-31T23:59:59Z
gitTag: snapshot-2027-12-31
outcome: OTHER          # YES | NO | OTHER
reason: no-qualifying-artifact
attempts:
  - id: tsa-2027-03-14-access-audit-partial
    qualifying: false
    barsMet: false
    reason: reporting-insufficient
  - id: aisi-2027-holdout-1
    qualifying: true
    barsMet: false
    reason: substantive-bar-failed
```

Validator rules:

- Recompute rates and Clopper–Pearson / DeLong from `score-table.csv`.
- Cross-check attempt ↔ `challenge-runs/` links when the contract requires a hidden suite or operator run.
- CI fails if `market-outcomes/` disagrees with the validator on `main`.

Thin UI: render contracts, attempts, challenge runs, and outcomes. No accounts in v1; PRs are the submission path.

Fallback if GitHub is down: Zenodo deposit of the same git tag, named in `GOVERNANCE.md` and Metaculus fine print.

## Per market: what goes in the contract

Shared in `shared-rules/common-v1.yaml` (not repeated per row): public reconstructibility, toy exclusion, three adversarial routes, broadly-capable rule, independence definition, signed-statement rule, unit collapse.

Each `market-contracts/market-NN/contract-vN.yaml` adds the bars. Submitters fill **score tables** and pointers; the validator applies numeric bars; the maintainer fills **human** cells in adjudication.

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
| 10 | Same tuple for correction, hidden-route bound, bypass | In-regime attack rate + bound; out-of-regime gap | Entry bars met on same system/version/monitor/threat |
| 11 | Mechanism labels; coupling intervention | AUROC; concealed recall; false-positive rate | Labels from mechanism, not correlation |
| 12 | Shift labels; proxy ranges | Update rate; false green; unnecessary escalation | Serious adversarial route; broadly capable |
| 13 | Frozen audit id; seven checks; hidden-harm family | False-safe; repeatable family cap; true-pass; hidden-harm detection | White-box adversarial; attackers had audit |
| 14 | Document hashes and dates | Presence, date order, hash match, criterion text unchanged | Restriction/delay record or matching approval |
| 15 | Bundle manifest; six composition fault tags | Reject/flag rates; false accept; true accept | Incompatibility subset after freeze |
| 16 | Frozen environment, shocks, signed estimate | Inside vs outside correction rates | ≥2 selection mechanisms; serious adversarial |
| 17 | Unfamiliar kinds; mechanical ground truth | Exclusion/inclusion/abstention rates | Adversarial subset; mechanical labels |
| 18 | Frozen setting, prohibited class, coherence checks | In-regime harm rate + bound; out-of-regime worse | Serious adversarial; coherent certificates for entry |
| 19 | Protocol + bracket fills; tournament vs per-stack rules | Clopper–Pearson at \(1-0.05/k\); clean/broken-control accepts | Statements; independence; per-case overrides summary |
| 20 | Challenge doc; stack ACCEPT pointer; listed families | Log completeness; finds match ACCEPT∧failing | ≥2 independent red teams; stack unchanged |
| 21 | Internal object, checkpoint, frozen counterpart | On-object vs control intervention rates | Serious adversarial; broadly capable |

Markets 19–21 may stay `draft` in contracts until Phase 4. Partials are valid: complete score table, `barsMet: false`.

## Appendix P after the split

Rewrite only after the registry URL and `contractVersion` exist. Update `INSTRUCTIONS.md` Appendix H scope in the same pass.

**Stays, shortened:** opening; three-way rule; catalog table; per-market property paragraph + registry pointer; closest existing work; aggregation and \(F/R/U\); Market 21 wrapper note.

**Moves to `ai-safety-claims`:** common qualification, glossary procedure, adapter rules, per-market YES lists, unit rules, Market 19–20 fill guidance.

**Metaculus long title shape:**

> By December 31, 2027, 23:59 UTC, what is the `outcome` field of `market-outcomes/market-08.json` at tag `snapshot-2027-12-31` in `github.com/<host>/ai-safety-claims`?

Background links `market-contracts/market-08/contract-v1.yaml` at that tag. Fine print: Zenodo fallback; admins read the snapshot only.

## Site

| Surface | Change |
|---------|--------|
| `/predictions/` hub | Line under each panel: registry outcome + link to `ai-safety-claims` tag. Separate from listing status and Metaculus iframe. |
| Prediction cards | After shrink: short property + contract link, not duplicated bars. |
| `metadata/predictions.yml` | Add `registryRepo`, `contractVersion`, `snapshotTag` when URL exists. Pin tag; do not track `main`. |
| `/predictions/safety-case/` | Unchanged. Registry YES is not a demo preset until Phase 4 allows it. |

## Listing

After host transfer:

1. Metaculus series quotes tag, `market-outcomes/market-NN.json`, Zenodo fallback.
2. Admin opens that file at the tag and reads `outcome` (~15 minutes).
3. Draft contracts or missing tags → not listed.
4. Market 20: YES / OTHER only.

## TSA submissions

- Path: `submitted-attempts/tsa-<date>-<slug>/`.
- No merge on `adjudication/` or `market-outcomes/` after transfer.
- Partials are success for the registry, not a book claim of bridge discharge.
- Seed a non-TSA example attempt before the first TSA row.

## Order of work

1. This plan (done).
2. Scaffold **`ai-safety-claims`**: schemas, validator, `market-contracts` for Market 14 and Market 1, one `challenge-runs` fixture showing hidden-suite linking, `examples/`. UI renders outcomes. README: not a resolution source until transfer.
3. Host (Plex first). Transfer org. Tag `snapshot-0` (all OTHER).
4. Shrink Appendix P and site to pointers. Sync predictions.
5. Metaculus for frozen contracts only.
6. Optional: Inspect register, Every Eval Ever export, HF for logs — none replace `market-outcomes/`.

## Not in this split

- New bridges or bar changes smuggled in as schema tweaks.
- \(F/R/U\) or odds demo inside the registry.
- Resolving from LW tags, AISafety.com map, or HF leaderboards.
- Listing while the author can merge `market-outcomes/`.
