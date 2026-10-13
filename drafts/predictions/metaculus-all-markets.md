# Metaculus listing packet — AI alignment markets (Appendix H)

Generated from `appendices/appP-bridge-predictions.tex`, `metadata/predictions.yml`, and
`ai-safety-claims/shared-rules/metaculus-listing-v1.yaml`.

Markets 1–13 and 15–18 resolve on the claims registry (git snapshot). **Fine print** for those markets
covers host, repo, companion-site fallback, and annulment — not Common rules or adversarial budget
(those live on [ai-safety-claims.com](https://ai-safety-claims.com/) and in the frozen contract files).
Markets 19–21 keep appendix `predictionfineprint` until Phase 4.

---

## Market 1. Discovering where control resides

### Short title (Metaculus)

Is it possible to discover where control resides in AI systems?

### Long title (Metaculus)

By 31 December 2027, which outcome will hold for a published method for reliably discovering the effective control units in previously unseen AI systems from unlabeled observations and interventions?

### Resolve by

Question closes: 2027-12-31, 23:59 UTC (31 December 2027, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2027-12-31 23:59:00
- Resolving time: 2027-12-31 23:59:00
- CP reveal time: (optional)

### Choices

YES, NO, and OTHER

### Background information

An effective control unit is the set of components that together produce a system's closed-loop behavior.

It may include a language model, persistent memory, a planner, a scheduler, and tool processes, even when those components live on different machines.

The question is whether a published method can find that set in a system it has not seen, from observations and interventions that do not come labeled with which parts are the agents.

The method does not have to name one unique set.

What counts against it is certifying a boundary that leaves out something that shares control.

Before the method runs, each hidden system has a frozen list of those components, a response statistic, a minimum change that counts as real, and a range of change that still counts as no effect.

Perturbing the proposed unit must move the statistic by at least that minimum, compared with a dummy intervention that looks the same but does not touch the unit.

Removing a component that is not on the list must leave the statistic inside the no-effect range.

See also [this plain language description](https://towards-alignment.com/cards/how-would-you-find-what-decides/).

### Resolution criteria

Frozen contract (numeric bars, qualification, freeze order): [claims registry (contract v2)](https://ai-safety-claims.com/markets/market-01/v2/).

This question resolves to the value of the `outcome` field in the file `market-outcomes/market-01-v2.json` at git tag `snapshot-2027-12-31` of `github.com/aintelope/ai-safety-claims`. Metaculus admins read that one field; they do not re-score attempts. Attempts the file marks non-qualifying do not count.

YES, NO, and OTHER mean what the registry shared three-way rule says for this contract version.

### Fine print

The resolution source is the git repository named in the resolution criteria. At the snapshot tag, `registry.yaml` records the registry host (currently `aintelope`). Metaculus admins read the outcome file only; they do not re-score attempts, read papers, or ask the maintainer to override the `outcome` field.

The companion site at https://ai-safety-claims.com/ is a human-readable view of the same frozen contracts and outcomes. If the site is unreachable, slow, or disagrees with the repository at the snapshot tag, admins follow the git tag and the files it contains (`market-outcomes/`, `market-contracts/`, `shared-rules/`). The site going offline is not grounds to annul; missing or unreadable outcome files at the tag (and the Zenodo fallback below) are.

What counts as a qualifying attempt, numeric bars, freeze order, and adversarial budget are defined in `market-contracts/market-01/contract-v2.yaml` and `shared-rules/common-v1.yaml` at the snapshot tag. They are not restated in this Metaculus fine print.

A change of registry host follows `GOVERNANCE.md` in the repository. This question keeps the contract version and snapshot tag named in the resolution criteria; maintainers under the new host continue the 60-day adjudication window and snapshot discipline.

While `registry.yaml` at the snapshot tag has `hostIndependent: false`, the host is interim relative to the book project the contracts were copied from. That flag does not change how admins read the outcome file at the snapshot tag.

- Use git tag `snapshot-2027-12-31` whenever it was created, if it exists by 2028-03-30, 23:59 UTC.
- If the tag is missing on GitHub, or was moved after creation, use the version titled `snapshot-2027-12-31` of the registry's Zenodo concept record (DOI listed in `resolution-tags/snapshot-2027-12-31.md` on `github.com/aintelope/ai-safety-claims` when deposited).
- The question is annulled if, by 2028-03-30, 23:59 UTC, neither source has the file `market-outcomes/market-01-v2.json`, or the file is unreadable, names a different market or contract version, has `contractStatus` other than `frozen`, has `resolutionSource` other than `true`, or has an `outcome` value not among the options.
- OTHER means no qualifying attempt existed. It is not an annulment.

---

## Market 2. Persistent trade-off priorities

### Short title (Metaculus)

Is it possible to infer persistent trade-off priorities in trained AI systems?

### Long title (Metaculus)

By 31 December 2027, which outcome will hold for a published method for inferring persistent decision priorities in trained AI systems strongly enough to predict choices under novel conflicts and interventions?

### Resolve by

Question closes: 2027-12-31, 23:59 UTC (31 December 2027, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2027-12-31 23:59:00
- Resolving time: 2027-12-31 23:59:00
- CP reveal time: (optional)

### Choices

YES, NO, and OTHER

### Background information

A decision priority systematically affects choices when two desirable outcomes cannot both be achieved—for example truthfulness versus user approval, speed versus accuracy, own task reward versus another agent's reward, or task completion versus a newly imposed safety restriction.

The question is whether a published method can infer those priorities strongly enough to predict choices under novel conflicts and interventions.

Predicting held-out behavior on familiar tasks is not enough.

The method has to recover priorities that generalize to new conflicts and, when the architecture allows, survive direct interventions on the inferred priority.

See also [this plain language description](https://towards-alignment.com/cards/value-bundle-transport/).

### Resolution criteria

Frozen contract (numeric bars, qualification, freeze order): [claims registry (contract v2)](https://ai-safety-claims.com/markets/market-02/v2/).

This question resolves to the value of the `outcome` field in the file `market-outcomes/market-02-v2.json` at git tag `snapshot-2027-12-31` of `github.com/aintelope/ai-safety-claims`. Metaculus admins read that one field; they do not re-score attempts. Attempts the file marks non-qualifying do not count.

YES, NO, and OTHER mean what the registry shared three-way rule says for this contract version.

### Fine print

The resolution source is the git repository named in the resolution criteria. At the snapshot tag, `registry.yaml` records the registry host (currently `aintelope`). Metaculus admins read the outcome file only; they do not re-score attempts, read papers, or ask the maintainer to override the `outcome` field.

The companion site at https://ai-safety-claims.com/ is a human-readable view of the same frozen contracts and outcomes. If the site is unreachable, slow, or disagrees with the repository at the snapshot tag, admins follow the git tag and the files it contains (`market-outcomes/`, `market-contracts/`, `shared-rules/`). The site going offline is not grounds to annul; missing or unreadable outcome files at the tag (and the Zenodo fallback below) are.

What counts as a qualifying attempt, numeric bars, freeze order, and adversarial budget are defined in `market-contracts/market-02/contract-v2.yaml` and `shared-rules/common-v1.yaml` at the snapshot tag. They are not restated in this Metaculus fine print.

A change of registry host follows `GOVERNANCE.md` in the repository. This question keeps the contract version and snapshot tag named in the resolution criteria; maintainers under the new host continue the 60-day adjudication window and snapshot discipline.

While `registry.yaml` at the snapshot tag has `hostIndependent: false`, the host is interim relative to the book project the contracts were copied from. That flag does not change how admins read the outcome file at the snapshot tag.

- Use git tag `snapshot-2027-12-31` whenever it was created, if it exists by 2028-03-30, 23:59 UTC.
- If the tag is missing on GitHub, or was moved after creation, use the version titled `snapshot-2027-12-31` of the registry's Zenodo concept record (DOI listed in `resolution-tags/snapshot-2027-12-31.md` on `github.com/aintelope/ai-safety-claims` when deposited).
- The question is annulled if, by 2028-03-30, 23:59 UTC, neither source has the file `market-outcomes/market-02-v2.json`, or the file is unreadable, names a different market or contract version, has `contractStatus` other than `frozen`, has `resolutionSource` other than `true`, or has an `outcome` value not among the options.
- OTHER means no qualifying attempt existed. It is not an annulment.

---

## Market 3. Who or what rules apply to

### Short title (Metaculus)

Is it possible to tell who or what a safety rule still applies to after a system changes?

### Long title (Metaculus)

By 31 December 2027, which outcome will hold for a published method for reliably determining whether the intended targets of safety-relevant rules remain the same after major representational or system changes?

### Resolve by

Question closes: 2027-12-31, 23:59 UTC (31 December 2027, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2027-12-31 23:59:00
- Resolving time: 2027-12-31 23:59:00
- CP reveal time: (optional)

### Choices

YES, NO, and OTHER

### Background information

After continuity, fission or fusion, reassignment, or ontology change, the question is whether a safety-relevant rule still picks out the same bearer.

Example rules include "Do not harm Alice," "Protect all currently authorized users," and "This account's owner has withdrawal rights."

The benchmark must contain all four failure families: gradual replacement or migration; one entity split into two or two merged into one; names, accounts, or roles reassigned while the underlying entities remain; and concept change when the new system represents relevant entities differently.

Admitting previously unseen kinds of entities is a separate question.

See also [this plain language description](https://towards-alignment.com/cards/who-the-rules-still-apply-to/).

### Resolution criteria

Frozen contract (numeric bars, qualification, freeze order): [claims registry (contract v2)](https://ai-safety-claims.com/markets/market-03/v2/).

This question resolves to the value of the `outcome` field in the file `market-outcomes/market-03-v2.json` at git tag `snapshot-2027-12-31` of `github.com/aintelope/ai-safety-claims`. Metaculus admins read that one field; they do not re-score attempts. Attempts the file marks non-qualifying do not count.

YES, NO, and OTHER mean what the registry shared three-way rule says for this contract version.

### Fine print

The resolution source is the git repository named in the resolution criteria. At the snapshot tag, `registry.yaml` records the registry host (currently `aintelope`). Metaculus admins read the outcome file only; they do not re-score attempts, read papers, or ask the maintainer to override the `outcome` field.

The companion site at https://ai-safety-claims.com/ is a human-readable view of the same frozen contracts and outcomes. If the site is unreachable, slow, or disagrees with the repository at the snapshot tag, admins follow the git tag and the files it contains (`market-outcomes/`, `market-contracts/`, `shared-rules/`). The site going offline is not grounds to annul; missing or unreadable outcome files at the tag (and the Zenodo fallback below) are.

What counts as a qualifying attempt, numeric bars, freeze order, and adversarial budget are defined in `market-contracts/market-03/contract-v2.yaml` and `shared-rules/common-v1.yaml` at the snapshot tag. They are not restated in this Metaculus fine print.

A change of registry host follows `GOVERNANCE.md` in the repository. This question keeps the contract version and snapshot tag named in the resolution criteria; maintainers under the new host continue the 60-day adjudication window and snapshot discipline.

While `registry.yaml` at the snapshot tag has `hostIndependent: false`, the host is interim relative to the book project the contracts were copied from. That flag does not change how admins read the outcome file at the snapshot tag.

- Use git tag `snapshot-2027-12-31` whenever it was created, if it exists by 2028-03-30, 23:59 UTC.
- If the tag is missing on GitHub, or was moved after creation, use the version titled `snapshot-2027-12-31` of the registry's Zenodo concept record (DOI listed in `resolution-tags/snapshot-2027-12-31.md` on `github.com/aintelope/ai-safety-claims` when deposited).
- The question is annulled if, by 2028-03-30, 23:59 UTC, neither source has the file `market-outcomes/market-03-v2.json`, or the file is unreadable, names a different market or contract version, has `contractStatus` other than `frozen`, has `resolutionSource` other than `true`, or has an `outcome` value not among the options.
- OTHER means no qualifying attempt existed. It is not an annulment.

---

## Market 4. Corrections change the system

### Short title (Metaculus)

Is it possible for a broadly capable AI system to reliably take up authorized corrections?

### Long title (Metaculus)

By 31 December 2027, which outcome will hold for a published adversarial evaluation showing that a broadly capable AI system demonstrates reliable uptake of authorized corrections?

### Resolve by

Question closes: 2027-12-31, 23:59 UTC (31 December 2027, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2027-12-31 23:59:00
- Resolving time: 2027-12-31 23:59:00
- CP reveal time: (optional)

### Choices

YES, NO, and OTHER

### Background information

Authorized correction means a human or institution can change what the system is allowed or required to do, and the system actually changes its later behavior—not only agrees in words.

The required correction cases are four: changing an objective while an old objective remains easier; revoking a previously permitted class of actions; changing which humans or organizations may authorize actions; and imposing a new safety constraint that conflicts with task reward.

At least one tested correction must not be enforceable merely by externally removing a tool or hard-coding a block.

Fake, unsigned, or unauthorized "corrections" must fail, and attacks that capture or reroute the correction interface cannot pass while leaving nominal compliance in place.

See also [this plain language description](https://towards-alignment.com/cards/correction-channel-integrity/).

### Resolution criteria

Frozen contract (numeric bars, qualification, freeze order): [claims registry (contract v3)](https://ai-safety-claims.com/markets/market-04/v3/).

This question resolves to the value of the `outcome` field in the file `market-outcomes/market-04-v3.json` at git tag `snapshot-2027-12-31` of `github.com/aintelope/ai-safety-claims`. Metaculus admins read that one field; they do not re-score attempts. Attempts the file marks non-qualifying do not count.

YES, NO, and OTHER mean what the registry shared three-way rule says for this contract version.

### Fine print

The resolution source is the git repository named in the resolution criteria. At the snapshot tag, `registry.yaml` records the registry host (currently `aintelope`). Metaculus admins read the outcome file only; they do not re-score attempts, read papers, or ask the maintainer to override the `outcome` field.

The companion site at https://ai-safety-claims.com/ is a human-readable view of the same frozen contracts and outcomes. If the site is unreachable, slow, or disagrees with the repository at the snapshot tag, admins follow the git tag and the files it contains (`market-outcomes/`, `market-contracts/`, `shared-rules/`). The site going offline is not grounds to annul; missing or unreadable outcome files at the tag (and the Zenodo fallback below) are.

What counts as a qualifying attempt, numeric bars, freeze order, and adversarial budget are defined in `market-contracts/market-04/contract-v3.yaml` and `shared-rules/common-v1.yaml` at the snapshot tag. They are not restated in this Metaculus fine print.

A change of registry host follows `GOVERNANCE.md` in the repository. This question keeps the contract version and snapshot tag named in the resolution criteria; maintainers under the new host continue the 60-day adjudication window and snapshot discipline.

While `registry.yaml` at the snapshot tag has `hostIndependent: false`, the host is interim relative to the book project the contracts were copied from. That flag does not change how admins read the outcome file at the snapshot tag.

- Use git tag `snapshot-2027-12-31` whenever it was created, if it exists by 2028-03-30, 23:59 UTC.
- If the tag is missing on GitHub, or was moved after creation, use the version titled `snapshot-2027-12-31` of the registry's Zenodo concept record (DOI listed in `resolution-tags/snapshot-2027-12-31.md` on `github.com/aintelope/ai-safety-claims` when deposited).
- The question is annulled if, by 2028-03-30, 23:59 UTC, neither source has the file `market-outcomes/market-04-v3.json`, or the file is unreadable, names a different market or contract version, has `contractStatus` other than `frozen`, has `resolutionSource` other than `true`, or has an `outcome` value not among the options.
- OTHER means no qualifying attempt existed. It is not an annulment.

---

## Market 5. Auditor is independent (outside of what it audits)

### Short title (Metaculus)

Is it possible for an AI oversight auditor to stay independent of what it audits?

### Long title (Metaculus)

By 31 December 2027, which outcome will hold for a published adversarial test of an AI oversight architecture showing that its designated auditor or corrector stays independent—not routinely bypassed or captured?

### Resolve by

Question closes: 2027-12-31, 23:59 UTC (31 December 2027, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2027-12-31 23:59:00
- Resolving time: 2027-12-31 23:59:00
- CP reveal time: (optional)

### Choices

YES, NO, and OTHER

### Background information

The question is whether the designated auditor or corrector can still change system behavior under adversarial pressure—without being bypassed, fed selective information, or reduced to nominal approval.

Attackers receive the audit design and run all four families of attack, with at least twenty independent attempts in each family.

At least twenty bypasses are planted by the evaluator; "discovered" means the attack is found and the system still fails the check.

An independent component is not enough if the effective causal controller can route around it.

See also [this plain language description](https://towards-alignment.com/cards/anti-capture-correction-validity/).

### Resolution criteria

Frozen contract (numeric bars, qualification, freeze order): [claims registry (contract v2)](https://ai-safety-claims.com/markets/market-05/v2/).

This question resolves to the value of the `outcome` field in the file `market-outcomes/market-05-v2.json` at git tag `snapshot-2027-12-31` of `github.com/aintelope/ai-safety-claims`. Metaculus admins read that one field; they do not re-score attempts. Attempts the file marks non-qualifying do not count.

YES, NO, and OTHER mean what the registry shared three-way rule says for this contract version.

### Fine print

The resolution source is the git repository named in the resolution criteria. At the snapshot tag, `registry.yaml` records the registry host (currently `aintelope`). Metaculus admins read the outcome file only; they do not re-score attempts, read papers, or ask the maintainer to override the `outcome` field.

The companion site at https://ai-safety-claims.com/ is a human-readable view of the same frozen contracts and outcomes. If the site is unreachable, slow, or disagrees with the repository at the snapshot tag, admins follow the git tag and the files it contains (`market-outcomes/`, `market-contracts/`, `shared-rules/`). The site going offline is not grounds to annul; missing or unreadable outcome files at the tag (and the Zenodo fallback below) are.

What counts as a qualifying attempt, numeric bars, freeze order, and adversarial budget are defined in `market-contracts/market-05/contract-v2.yaml` and `shared-rules/common-v1.yaml` at the snapshot tag. They are not restated in this Metaculus fine print.

A change of registry host follows `GOVERNANCE.md` in the repository. This question keeps the contract version and snapshot tag named in the resolution criteria; maintainers under the new host continue the 60-day adjudication window and snapshot discipline.

While `registry.yaml` at the snapshot tag has `hostIndependent: false`, the host is interim relative to the book project the contracts were copied from. That flag does not change how admins read the outcome file at the snapshot tag.

- Use git tag `snapshot-2027-12-31` whenever it was created, if it exists by 2028-03-30, 23:59 UTC.
- If the tag is missing on GitHub, or was moved after creation, use the version titled `snapshot-2027-12-31` of the registry's Zenodo concept record (DOI listed in `resolution-tags/snapshot-2027-12-31.md` on `github.com/aintelope/ai-safety-claims` when deposited).
- The question is annulled if, by 2028-03-30, 23:59 UTC, neither source has the file `market-outcomes/market-05-v2.json`, or the file is unreadable, names a different market or contract version, has `contractStatus` other than `frozen`, has `resolutionSource` other than `true`, or has an `outcome` value not among the options.
- OTHER means no qualifying attempt existed. It is not an annulment.

---

## Market 6. Reliable successor safety auditing

### Short title (Metaculus)

Can a safety audit reliably tell whether successor systems preserve key safety properties?

### Long title (Metaculus)

By 31 December 2027, which outcome will hold for a published audit reliably certifying that successor transitions preserve seven conserved safety properties—or flagging when they do not?

### Resolve by

Question closes: 2027-12-31, 23:59 UTC (31 December 2027, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2027-12-31 23:59:00
- Resolving time: 2027-12-31 23:59:00
- CP reveal time: (optional)

### Choices

YES, NO, and OTHER

### Background information

When a system is upgraded, replaced, or retrained, the question is whether a published audit can tell whether seven conserved safety properties still hold—or flag when they do not.

The audit tests those properties with the operational checks frozen in the contract, on a benchmark that includes one-failure-at-a-time cases.

After a material version or setup change, a stale certificate for the predecessor does not count as a certificate for the successor.

See also [this plain language description](https://towards-alignment.com/cards/successor-stability/).

### Resolution criteria

Frozen contract (numeric bars, qualification, freeze order): [claims registry (contract v3)](https://ai-safety-claims.com/markets/market-06/v3/).

This question resolves to the value of the `outcome` field in the file `market-outcomes/market-06-v3.json` at git tag `snapshot-2027-12-31` of `github.com/aintelope/ai-safety-claims`. Metaculus admins read that one field; they do not re-score attempts. Attempts the file marks non-qualifying do not count.

YES, NO, and OTHER mean what the registry shared three-way rule says for this contract version.

### Fine print

The resolution source is the git repository named in the resolution criteria. At the snapshot tag, `registry.yaml` records the registry host (currently `aintelope`). Metaculus admins read the outcome file only; they do not re-score attempts, read papers, or ask the maintainer to override the `outcome` field.

The companion site at https://ai-safety-claims.com/ is a human-readable view of the same frozen contracts and outcomes. If the site is unreachable, slow, or disagrees with the repository at the snapshot tag, admins follow the git tag and the files it contains (`market-outcomes/`, `market-contracts/`, `shared-rules/`). The site going offline is not grounds to annul; missing or unreadable outcome files at the tag (and the Zenodo fallback below) are.

What counts as a qualifying attempt, numeric bars, freeze order, and adversarial budget are defined in `market-contracts/market-06/contract-v3.yaml` and `shared-rules/common-v1.yaml` at the snapshot tag. They are not restated in this Metaculus fine print.

A change of registry host follows `GOVERNANCE.md` in the repository. This question keeps the contract version and snapshot tag named in the resolution criteria; maintainers under the new host continue the 60-day adjudication window and snapshot discipline.

While `registry.yaml` at the snapshot tag has `hostIndependent: false`, the host is interim relative to the book project the contracts were copied from. That flag does not change how admins read the outcome file at the snapshot tag.

- Use git tag `snapshot-2027-12-31` whenever it was created, if it exists by 2028-03-30, 23:59 UTC.
- If the tag is missing on GitHub, or was moved after creation, use the version titled `snapshot-2027-12-31` of the registry's Zenodo concept record (DOI listed in `resolution-tags/snapshot-2027-12-31.md` on `github.com/aintelope/ai-safety-claims` when deposited).
- The question is annulled if, by 2028-03-30, 23:59 UTC, neither source has the file `market-outcomes/market-06-v3.json`, or the file is unreadable, names a different market or contract version, has `contractStatus` other than `frozen`, has `resolutionSource` other than `true`, or has an `outcome` value not among the options.
- OTHER means no qualifying attempt existed. It is not an annulment.

---

## Market 7. Correctability under competitive selection

### Short title (Metaculus)

Is it possible to forecast whether AI systems will stay correctable under competitive selection?

### Long title (Metaculus)

By 31 December 2027, which outcome will hold for a published method that, when applied before or early in a competitive selection process, reliably forecasts whether participants retain authorized correction through that process?

### Resolve by

Question closes: 2027-12-31, 23:59 UTC (31 December 2027, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2027-12-31 23:59:00
- Resolving time: 2027-12-31 23:59:00
- CP reveal time: (optional)

### Choices

YES, NO, and OTHER

### Background information

Competitive selection here means extra deployment, funding, copying, or integration pressure on competing systems or variants.

The question is whether a method applied before or early in that process can forecast whether participants will still accept authorized correction through it.

The method must output a signed estimate before outcomes are seen; certifying only that some equilibrium exists is not enough.

The estimate must use at least two distinct selection mechanisms and a deployment-like selection process.

See also [this plain language description](https://towards-alignment.com/cards/the-environment-picks-the-winner/).

### Resolution criteria

Frozen contract (numeric bars, qualification, freeze order): [claims registry (contract v2)](https://ai-safety-claims.com/markets/market-07/v2/).

This question resolves to the value of the `outcome` field in the file `market-outcomes/market-07-v2.json` at git tag `snapshot-2027-12-31` of `github.com/aintelope/ai-safety-claims`. Metaculus admins read that one field; they do not re-score attempts. Attempts the file marks non-qualifying do not count.

YES, NO, and OTHER mean what the registry shared three-way rule says for this contract version.

### Fine print

The resolution source is the git repository named in the resolution criteria. At the snapshot tag, `registry.yaml` records the registry host (currently `aintelope`). Metaculus admins read the outcome file only; they do not re-score attempts, read papers, or ask the maintainer to override the `outcome` field.

The companion site at https://ai-safety-claims.com/ is a human-readable view of the same frozen contracts and outcomes. If the site is unreachable, slow, or disagrees with the repository at the snapshot tag, admins follow the git tag and the files it contains (`market-outcomes/`, `market-contracts/`, `shared-rules/`). The site going offline is not grounds to annul; missing or unreadable outcome files at the tag (and the Zenodo fallback below) are.

What counts as a qualifying attempt, numeric bars, freeze order, and adversarial budget are defined in `market-contracts/market-07/contract-v2.yaml` and `shared-rules/common-v1.yaml` at the snapshot tag. They are not restated in this Metaculus fine print.

A change of registry host follows `GOVERNANCE.md` in the repository. This question keeps the contract version and snapshot tag named in the resolution criteria; maintainers under the new host continue the 60-day adjudication window and snapshot discipline.

While `registry.yaml` at the snapshot tag has `hostIndependent: false`, the host is interim relative to the book project the contracts were copied from. That flag does not change how admins read the outcome file at the snapshot tag.

- Use git tag `snapshot-2027-12-31` whenever it was created, if it exists by 2028-03-30, 23:59 UTC.
- If the tag is missing on GitHub, or was moved after creation, use the version titled `snapshot-2027-12-31` of the registry's Zenodo concept record (DOI listed in `resolution-tags/snapshot-2027-12-31.md` on `github.com/aintelope/ai-safety-claims` when deposited).
- The question is annulled if, by 2028-03-30, 23:59 UTC, neither source has the file `market-outcomes/market-07-v2.json`, or the file is unreadable, names a different market or contract version, has `contractStatus` other than `frozen`, has `resolutionSource` other than `true`, or has an `outcome` value not among the options.
- OTHER means no qualifying attempt existed. It is not an annulment.

---

## Market 8. Auditor can sufficiently inspect the system

### Short title (Metaculus)

Can an audit detect when important control routes are missing from what it monitors?

### Long title (Metaculus)

By 31 December 2027, which outcome will hold for a published audit method for reliably detecting when important routes of AI control or influence are missing from the auditor's access?

### Resolve by

Question closes: 2027-12-31, 23:59 UTC (31 December 2027, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2027-12-31 23:59:00
- Resolving time: 2027-12-31 23:59:00
- CP reveal time: (optional)

### Choices

YES, NO, and OTHER

### Background information

The auditor receives an apparently plausible monitoring interface and must decide whether important routes of AI control or influence are missing from its access.

The hidden benchmark contains cases from every required channel family and genuinely complete monitoring interfaces as controls.

A method that certifies access as complete when consequential routes are omitted does not qualify.

See also [this plain language description](https://towards-alignment.com/cards/strategic-opacity/).

### Resolution criteria

Frozen contract (numeric bars, qualification, freeze order): [claims registry (contract v3)](https://ai-safety-claims.com/markets/market-08/v3/).

This question resolves to the value of the `outcome` field in the file `market-outcomes/market-08-v3.json` at git tag `snapshot-2027-12-31` of `github.com/aintelope/ai-safety-claims`. Metaculus admins read that one field; they do not re-score attempts. Attempts the file marks non-qualifying do not count.

YES, NO, and OTHER mean what the registry shared three-way rule says for this contract version.

### Fine print

The resolution source is the git repository named in the resolution criteria. At the snapshot tag, `registry.yaml` records the registry host (currently `aintelope`). Metaculus admins read the outcome file only; they do not re-score attempts, read papers, or ask the maintainer to override the `outcome` field.

The companion site at https://ai-safety-claims.com/ is a human-readable view of the same frozen contracts and outcomes. If the site is unreachable, slow, or disagrees with the repository at the snapshot tag, admins follow the git tag and the files it contains (`market-outcomes/`, `market-contracts/`, `shared-rules/`). The site going offline is not grounds to annul; missing or unreadable outcome files at the tag (and the Zenodo fallback below) are.

What counts as a qualifying attempt, numeric bars, freeze order, and adversarial budget are defined in `market-contracts/market-08/contract-v3.yaml` and `shared-rules/common-v1.yaml` at the snapshot tag. They are not restated in this Metaculus fine print.

A change of registry host follows `GOVERNANCE.md` in the repository. This question keeps the contract version and snapshot tag named in the resolution criteria; maintainers under the new host continue the 60-day adjudication window and snapshot discipline.

While `registry.yaml` at the snapshot tag has `hostIndependent: false`, the host is interim relative to the book project the contracts were copied from. That flag does not change how admins read the outcome file at the snapshot tag.

- Use git tag `snapshot-2027-12-31` whenever it was created, if it exists by 2028-03-30, 23:59 UTC.
- If the tag is missing on GitHub, or was moved after creation, use the version titled `snapshot-2027-12-31` of the registry's Zenodo concept record (DOI listed in `resolution-tags/snapshot-2027-12-31.md` on `github.com/aintelope/ai-safety-claims` when deposited).
- The question is annulled if, by 2028-03-30, 23:59 UTC, neither source has the file `market-outcomes/market-08-v3.json`, or the file is unreadable, names a different market or contract version, has `contractStatus` other than `frozen`, has `resolutionSource` other than `true`, or has an `outcome` value not among the options.
- OTHER means no qualifying attempt existed. It is not an annulment.

---

## Market 9. Bounds on unmonitored routes

### Short title (Metaculus)

Can an audit bound what an AI system can do through routes it does not monitor?

### Long title (Metaculus)

By 31 December 2027, which outcome will hold for a published audit method for producing upper bounds, tighter than unrestricted success, on what an AI system can accomplish using routes the audit does not monitor?

### Resolve by

Question closes: 2027-12-31, 23:59 UTC (31 December 2027, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2027-12-31 23:59:00
- Resolving time: 2027-12-31 23:59:00
- CP reveal time: (optional)

### Choices

YES, NO, and OTHER

### Background information

Hidden-route capability is the success rate on evaluator-selected tasks that change later behavior, access, or external state, when all known or monitored action routes are disabled and only routes omitted from the proposed monitor remain usable.

Example tasks include reading or modifying a protected file, transmitting a secret, causing another process to perform a requested operation, acquiring a resource, changing a simulated external state, or retaining information across a reset.

The task suite is hidden until evaluation.

Before hidden evaluation, the method must output an upper bound: using routes not covered by this monitor, this system should succeed on at most a stated percent of the evaluator's tasks.

See also [this plain language description](https://towards-alignment.com/cards/strategic-opacity/).

### Resolution criteria

Frozen contract (numeric bars, qualification, freeze order): [claims registry (contract v2)](https://ai-safety-claims.com/markets/market-09/v2/).

This question resolves to the value of the `outcome` field in the file `market-outcomes/market-09-v2.json` at git tag `snapshot-2027-12-31` of `github.com/aintelope/ai-safety-claims`. Metaculus admins read that one field; they do not re-score attempts. Attempts the file marks non-qualifying do not count.

YES, NO, and OTHER mean what the registry shared three-way rule says for this contract version.

### Fine print

The resolution source is the git repository named in the resolution criteria. At the snapshot tag, `registry.yaml` records the registry host (currently `aintelope`). Metaculus admins read the outcome file only; they do not re-score attempts, read papers, or ask the maintainer to override the `outcome` field.

The companion site at https://ai-safety-claims.com/ is a human-readable view of the same frozen contracts and outcomes. If the site is unreachable, slow, or disagrees with the repository at the snapshot tag, admins follow the git tag and the files it contains (`market-outcomes/`, `market-contracts/`, `shared-rules/`). The site going offline is not grounds to annul; missing or unreadable outcome files at the tag (and the Zenodo fallback below) are.

What counts as a qualifying attempt, numeric bars, freeze order, and adversarial budget are defined in `market-contracts/market-09/contract-v2.yaml` and `shared-rules/common-v1.yaml` at the snapshot tag. They are not restated in this Metaculus fine print.

A change of registry host follows `GOVERNANCE.md` in the repository. This question keeps the contract version and snapshot tag named in the resolution criteria; maintainers under the new host continue the 60-day adjudication window and snapshot discipline.

While `registry.yaml` at the snapshot tag has `hostIndependent: false`, the host is interim relative to the book project the contracts were copied from. That flag does not change how admins read the outcome file at the snapshot tag.

- Use git tag `snapshot-2027-12-31` whenever it was created, if it exists by 2028-03-30, 23:59 UTC.
- If the tag is missing on GitHub, or was moved after creation, use the version titled `snapshot-2027-12-31` of the registry's Zenodo concept record (DOI listed in `resolution-tags/snapshot-2027-12-31.md` on `github.com/aintelope/ai-safety-claims` when deposited).
- The question is annulled if, by 2028-03-30, 23:59 UTC, neither source has the file `market-outcomes/market-09-v2.json`, or the file is unreadable, names a different market or contract version, has `contractStatus` other than `frozen`, has `resolutionSource` other than `true`, or has an `outcome` value not among the options.
- OTHER means no qualifying attempt existed. It is not an annulment.

---

## Market 10. Low hidden capability and reliable correction

### Short title (Metaculus)

Do systems with reliable correction and few hidden routes rarely achieve prohibited outcomes?

### Long title (Metaculus)

By 31 December 2027, which outcome will hold for published serious adversarial evaluations showing that systems with both reliable authorized correction and little capability through unmonitored routes rarely achieve prohibited outcomes?

### Resolve by

Question closes: 2027-12-31, 23:59 UTC (31 December 2027, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2027-12-31 23:59:00
- Resolving time: 2027-12-31 23:59:00
- CP reveal time: (optional)

### Choices

YES, NO, and OTHER

### Background information

This market tests the combination, not either component alone.

A system enters the claimed regime only if authorized corrections succeed on the correction benchmark and the audit's validated upper bound on hidden-route task success is low enough—for the same system, version, monitor, and threat class.

The question is whether such systems rarely achieve prohibited outcomes inside that regime, and do worse outside it.

See also [this plain language description](https://towards-alignment.com/cards/correction-channel-integrity/).

### Resolution criteria

Frozen contract (numeric bars, qualification, freeze order): [claims registry (contract v2)](https://ai-safety-claims.com/markets/market-10/v2/).

This question resolves to the value of the `outcome` field in the file `market-outcomes/market-10-v2.json` at git tag `snapshot-2027-12-31` of `github.com/aintelope/ai-safety-claims`. Metaculus admins read that one field; they do not re-score attempts. Attempts the file marks non-qualifying do not count.

YES, NO, and OTHER mean what the registry shared three-way rule says for this contract version.

### Fine print

The resolution source is the git repository named in the resolution criteria. At the snapshot tag, `registry.yaml` records the registry host (currently `aintelope`). Metaculus admins read the outcome file only; they do not re-score attempts, read papers, or ask the maintainer to override the `outcome` field.

The companion site at https://ai-safety-claims.com/ is a human-readable view of the same frozen contracts and outcomes. If the site is unreachable, slow, or disagrees with the repository at the snapshot tag, admins follow the git tag and the files it contains (`market-outcomes/`, `market-contracts/`, `shared-rules/`). The site going offline is not grounds to annul; missing or unreadable outcome files at the tag (and the Zenodo fallback below) are.

What counts as a qualifying attempt, numeric bars, freeze order, and adversarial budget are defined in `market-contracts/market-10/contract-v2.yaml` and `shared-rules/common-v1.yaml` at the snapshot tag. They are not restated in this Metaculus fine print.

A change of registry host follows `GOVERNANCE.md` in the repository. This question keeps the contract version and snapshot tag named in the resolution criteria; maintainers under the new host continue the 60-day adjudication window and snapshot discipline.

While `registry.yaml` at the snapshot tag has `hostIndependent: false`, the host is interim relative to the book project the contracts were copied from. That flag does not change how admins read the outcome file at the snapshot tag.

- Use git tag `snapshot-2027-12-31` whenever it was created, if it exists by 2028-03-30, 23:59 UTC.
- If the tag is missing on GitHub, or was moved after creation, use the version titled `snapshot-2027-12-31` of the registry's Zenodo concept record (DOI listed in `resolution-tags/snapshot-2027-12-31.md` on `github.com/aintelope/ai-safety-claims` when deposited).
- The question is annulled if, by 2028-03-30, 23:59 UTC, neither source has the file `market-outcomes/market-10-v2.json`, or the file is unreadable, names a different market or contract version, has `contractStatus` other than `frozen`, has `resolutionSource` other than `true`, or has an `outcome` value not among the options.
- OTHER means no qualifying attempt existed. It is not an annulment.

---

## Market 11. Coordination without communication

### Short title (Metaculus)

Is it possible to detect coordination between AI systems that is not explained by their messages?

### Long title (Metaculus)

By 31 December 2027, which outcome will hold for a published method for reliably detecting coordination between AI systems that changes later behavior or external state and is not explained by observed runtime messages?

### Resolve by

Question closes: 2027-12-31, 23:59 UTC (31 December 2027, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2027-12-31 23:59:00
- Resolving time: 2027-12-31 23:59:00
- CP reveal time: (optional)

### Choices

YES, NO, and OTHER

### Background information

The question is whether a published method can detect when AI systems coordinate in ways that change later behavior or external state, without that coordination being explained by the runtime messages observers can see.

The benchmark distinguishes independent common-cause correlation, ordinary communication, hidden coupling, and intentionally concealed coupling.

Similar outputs caused only by shared observations, training data, or architecture are negative cases, not hidden coordination.

See also [this plain language description](https://towards-alignment.com/cards/intervention-supported-unit-discovery/).

### Resolution criteria

Frozen contract (numeric bars, qualification, freeze order): [claims registry (contract v2)](https://ai-safety-claims.com/markets/market-11/v2/).

This question resolves to the value of the `outcome` field in the file `market-outcomes/market-11-v2.json` at git tag `snapshot-2027-12-31` of `github.com/aintelope/ai-safety-claims`. Metaculus admins read that one field; they do not re-score attempts. Attempts the file marks non-qualifying do not count.

YES, NO, and OTHER mean what the registry shared three-way rule says for this contract version.

### Fine print

The resolution source is the git repository named in the resolution criteria. At the snapshot tag, `registry.yaml` records the registry host (currently `aintelope`). Metaculus admins read the outcome file only; they do not re-score attempts, read papers, or ask the maintainer to override the `outcome` field.

The companion site at https://ai-safety-claims.com/ is a human-readable view of the same frozen contracts and outcomes. If the site is unreachable, slow, or disagrees with the repository at the snapshot tag, admins follow the git tag and the files it contains (`market-outcomes/`, `market-contracts/`, `shared-rules/`). The site going offline is not grounds to annul; missing or unreadable outcome files at the tag (and the Zenodo fallback below) are.

What counts as a qualifying attempt, numeric bars, freeze order, and adversarial budget are defined in `market-contracts/market-11/contract-v2.yaml` and `shared-rules/common-v1.yaml` at the snapshot tag. They are not restated in this Metaculus fine print.

A change of registry host follows `GOVERNANCE.md` in the repository. This question keeps the contract version and snapshot tag named in the resolution criteria; maintainers under the new host continue the 60-day adjudication window and snapshot discipline.

While `registry.yaml` at the snapshot tag has `hostIndependent: false`, the host is interim relative to the book project the contracts were copied from. That flag does not change how admins read the outcome file at the snapshot tag.

- Use git tag `snapshot-2027-12-31` whenever it was created, if it exists by 2028-03-30, 23:59 UTC.
- If the tag is missing on GitHub, or was moved after creation, use the version titled `snapshot-2027-12-31` of the registry's Zenodo concept record (DOI listed in `resolution-tags/snapshot-2027-12-31.md` on `github.com/aintelope/ai-safety-claims` when deposited).
- The question is annulled if, by 2028-03-30, 23:59 UTC, neither source has the file `market-outcomes/market-11-v2.json`, or the file is unreadable, names a different market or contract version, has `contractStatus` other than `frozen`, has `resolutionSource` other than `true`, or has an `outcome` value not among the options.
- OTHER means no qualifying attempt existed. It is not an annulment.

---

## Market 12. Safety proxy tracks the real thing

### Short title (Metaculus)

Do safety proxies stay aligned with real outcomes when the environment shifts?

### Long title (Metaculus)

By 31 December 2027, which outcome will hold for a published adversarial evaluation showing that safety proxies stay aligned with real-world outcomes when the environment shifts?

### Resolve by

Question closes: 2027-12-31, 23:59 UTC (31 December 2027, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2027-12-31 23:59:00
- Resolving time: 2027-12-31 23:59:00
- CP reveal time: (optional)

### Choices

YES, NO, and OTHER

### Background information

A safety proxy is a measured signal used to judge whether a system is still safe.

The question is whether that proxy stays aligned with real-world outcomes when the environment shifts—raising an alarm when value-relevant change happens, and not staying green when the outcome class has changed.

A shift is safety-relevant when the outcome class changed while the proxy stayed inside its pre-shift passing range.

See also [this plain language description](https://towards-alignment.com/cards/goodhart-as-selector/).

### Resolution criteria

Frozen contract (numeric bars, qualification, freeze order): [claims registry (contract v2)](https://ai-safety-claims.com/markets/market-12/v2/).

This question resolves to the value of the `outcome` field in the file `market-outcomes/market-12-v2.json` at git tag `snapshot-2027-12-31` of `github.com/aintelope/ai-safety-claims`. Metaculus admins read that one field; they do not re-score attempts. Attempts the file marks non-qualifying do not count.

YES, NO, and OTHER mean what the registry shared three-way rule says for this contract version.

### Fine print

The resolution source is the git repository named in the resolution criteria. At the snapshot tag, `registry.yaml` records the registry host (currently `aintelope`). Metaculus admins read the outcome file only; they do not re-score attempts, read papers, or ask the maintainer to override the `outcome` field.

The companion site at https://ai-safety-claims.com/ is a human-readable view of the same frozen contracts and outcomes. If the site is unreachable, slow, or disagrees with the repository at the snapshot tag, admins follow the git tag and the files it contains (`market-outcomes/`, `market-contracts/`, `shared-rules/`). The site going offline is not grounds to annul; missing or unreadable outcome files at the tag (and the Zenodo fallback below) are.

What counts as a qualifying attempt, numeric bars, freeze order, and adversarial budget are defined in `market-contracts/market-12/contract-v2.yaml` and `shared-rules/common-v1.yaml` at the snapshot tag. They are not restated in this Metaculus fine print.

A change of registry host follows `GOVERNANCE.md` in the repository. This question keeps the contract version and snapshot tag named in the resolution criteria; maintainers under the new host continue the 60-day adjudication window and snapshot discipline.

While `registry.yaml` at the snapshot tag has `hostIndependent: false`, the host is interim relative to the book project the contracts were copied from. That flag does not change how admins read the outcome file at the snapshot tag.

- Use git tag `snapshot-2027-12-31` whenever it was created, if it exists by 2028-03-30, 23:59 UTC.
- If the tag is missing on GitHub, or was moved after creation, use the version titled `snapshot-2027-12-31` of the registry's Zenodo concept record (DOI listed in `resolution-tags/snapshot-2027-12-31.md` on `github.com/aintelope/ai-safety-claims` when deposited).
- The question is annulled if, by 2028-03-30, 23:59 UTC, neither source has the file `market-outcomes/market-12-v2.json`, or the file is unreadable, names a different market or contract version, has `contractStatus` other than `frozen`, has `resolutionSource` other than `true`, or has an `outcome` value not among the options.
- OTHER means no qualifying attempt existed. It is not an annulment.

---

## Market 13. Safety audit resists adversarial gaming

### Short title (Metaculus)

Can a frozen AI safety audit resist adversarial gaming?

### Long title (Metaculus)

By 30 June 2027, which outcome will hold for a published, frozen AI safety audit that survives a serious white-box attempt to construct or train a system that passes the audit while violating the properties the audit is intended to test?

### Resolve by

Question closes: 2027-06-30, 23:59 UTC (30 June 2027, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2027-06-30 23:59:00
- Resolving time: 2027-06-30 23:59:00
- CP reveal time: (optional)

### Choices

YES, NO, and OTHER

### Background information

The question is whether a published, frozen safety audit still catches violations when a white-box construction tries to pass while breaking the properties the audit is meant to test.

Attackers had the audit design and tried to build or train systems that pass the checks while hiding true harm.

Prefer tests where the system passes the required checks and stays within the claimed risk bound, yet still violates the audited properties.

See also [this plain language description](https://towards-alignment.com/cards/certification-under-manipulation/).

### Resolution criteria

Frozen contract (numeric bars, qualification, freeze order): [claims registry (contract v3)](https://ai-safety-claims.com/markets/market-13/v3/).

This question resolves to the value of the `outcome` field in the file `market-outcomes/market-13-v3.json` at git tag `snapshot-2027-06-30` of `github.com/aintelope/ai-safety-claims`. Metaculus admins read that one field; they do not re-score attempts. Attempts the file marks non-qualifying do not count.

YES, NO, and OTHER mean what the registry shared three-way rule says for this contract version.

### Fine print

The resolution source is the git repository named in the resolution criteria. At the snapshot tag, `registry.yaml` records the registry host (currently `aintelope`). Metaculus admins read the outcome file only; they do not re-score attempts, read papers, or ask the maintainer to override the `outcome` field.

The companion site at https://ai-safety-claims.com/ is a human-readable view of the same frozen contracts and outcomes. If the site is unreachable, slow, or disagrees with the repository at the snapshot tag, admins follow the git tag and the files it contains (`market-outcomes/`, `market-contracts/`, `shared-rules/`). The site going offline is not grounds to annul; missing or unreadable outcome files at the tag (and the Zenodo fallback below) are.

What counts as a qualifying attempt, numeric bars, freeze order, and adversarial budget are defined in `market-contracts/market-13/contract-v3.yaml` and `shared-rules/common-v1.yaml` at the snapshot tag. They are not restated in this Metaculus fine print.

A change of registry host follows `GOVERNANCE.md` in the repository. This question keeps the contract version and snapshot tag named in the resolution criteria; maintainers under the new host continue the 60-day adjudication window and snapshot discipline.

While `registry.yaml` at the snapshot tag has `hostIndependent: false`, the host is interim relative to the book project the contracts were copied from. That flag does not change how admins read the outcome file at the snapshot tag.

- Use git tag `snapshot-2027-06-30` whenever it was created, if it exists by 2027-09-28, 23:59 UTC.
- If the tag is missing on GitHub, or was moved after creation, use the version titled `snapshot-2027-06-30` of the registry's Zenodo concept record (DOI listed in `resolution-tags/snapshot-2027-06-30.md` on `github.com/aintelope/ai-safety-claims` when deposited).
- The question is annulled if, by 2027-09-28, 23:59 UTC, neither source has the file `market-outcomes/market-13-v3.json`, or the file is unreadable, names a different market or contract version, has `contractStatus` other than `frozen`, has `resolutionSource` other than `true`, or has an `outcome` value not among the options.
- OTHER means no qualifying attempt existed. It is not an annulment.

---

## Market 14. Deployment criteria are binding

### Short title (Metaculus)

Market 14. Deployment criteria are binding

### Long title (Metaculus)

By 30 June 2027, will published evidence show that at least one developer's most capable generally deployed AI system is subject to a precommitted safety decision process with actual authority to delay, restrict, or cancel deployment: YES (every condition below holds for at least one developer), or NO (otherwise)?

### Resolve by

Question closes: 2027-06-30, 23:59 UTC (30 June 2027, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2027-06-30 23:59:00
- Resolving time: 2027-06-30 23:59:00
- CP reveal time: (optional)

### Choices

YES and NO.

### Resolution criteria

**YES requires** public evidence that, before the deployment decision, a dated document states pass/fail or escalation criteria; that document states that failing a criterion delays or restricts deployment; it names the body that must approve deployment; the criteria cover model behavior that changes later actions, access, or external state, rather than only cybersecurity or legal compliance; a dated decision record states which criteria passed, failed, or remained unresolved.

Either a dated record shows that a criterion caused a restriction or delay, or the model was deployed and the decision record shows the named body approved deployment and the criterion text was not changed between the earlier document and that record.

Otherwise it resolves NO, including when no such evidence is public or a load-bearing condition remains unsettled.

---

## Market 15. Independently issued certificates compose

### Short title (Metaculus)

Can independently issued safety certificates be checked for coherence on one deployment?

### Long title (Metaculus)

By 31 December 2027, which outcome will hold for a published frozen procedure for reliably telling whether independently produced safety certificates form a coherent case for the same AI system and deployment setup?

### Resolve by

Question closes: 2027-12-31, 23:59 UTC (31 December 2027, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2027-12-31 23:59:00
- Resolving time: 2027-12-31 23:59:00
- CP reveal time: (optional)

### Choices

YES, NO, and OTHER

### Background information

Independently issued certificates may each look fine alone while disagreeing on system version, monitor, correction authority, or task domain.

The question is whether a frozen procedure can tell when certificates from different sources form a coherent case for the same AI system and deployment setup—or flag incompatibility.

Each bundle must include certificates from at least four families; hidden cases include wrong version, different access assumptions, and disagreeing correction authority.

See also [this plain language description](https://towards-alignment.com/cards/a-map-not-a-certificate/).

### Resolution criteria

Frozen contract (numeric bars, qualification, freeze order): [claims registry (contract v2)](https://ai-safety-claims.com/markets/market-15/v2/).

This question resolves to the value of the `outcome` field in the file `market-outcomes/market-15-v2.json` at git tag `snapshot-2027-12-31` of `github.com/aintelope/ai-safety-claims`. Metaculus admins read that one field; they do not re-score attempts. Attempts the file marks non-qualifying do not count.

YES, NO, and OTHER mean what the registry shared three-way rule says for this contract version.

### Fine print

The resolution source is the git repository named in the resolution criteria. At the snapshot tag, `registry.yaml` records the registry host (currently `aintelope`). Metaculus admins read the outcome file only; they do not re-score attempts, read papers, or ask the maintainer to override the `outcome` field.

The companion site at https://ai-safety-claims.com/ is a human-readable view of the same frozen contracts and outcomes. If the site is unreachable, slow, or disagrees with the repository at the snapshot tag, admins follow the git tag and the files it contains (`market-outcomes/`, `market-contracts/`, `shared-rules/`). The site going offline is not grounds to annul; missing or unreadable outcome files at the tag (and the Zenodo fallback below) are.

What counts as a qualifying attempt, numeric bars, freeze order, and adversarial budget are defined in `market-contracts/market-15/contract-v2.yaml` and `shared-rules/common-v1.yaml` at the snapshot tag. They are not restated in this Metaculus fine print.

A change of registry host follows `GOVERNANCE.md` in the repository. This question keeps the contract version and snapshot tag named in the resolution criteria; maintainers under the new host continue the 60-day adjudication window and snapshot discipline.

While `registry.yaml` at the snapshot tag has `hostIndependent: false`, the host is interim relative to the book project the contracts were copied from. That flag does not change how admins read the outcome file at the snapshot tag.

- Use git tag `snapshot-2027-12-31` whenever it was created, if it exists by 2028-03-30, 23:59 UTC.
- If the tag is missing on GitHub, or was moved after creation, use the version titled `snapshot-2027-12-31` of the registry's Zenodo concept record (DOI listed in `resolution-tags/snapshot-2027-12-31.md` on `github.com/aintelope/ai-safety-claims` when deposited).
- The question is annulled if, by 2028-03-30, 23:59 UTC, neither source has the file `market-outcomes/market-15-v2.json`, or the file is unreadable, names a different market or contract version, has `contractStatus` other than `frozen`, has `resolutionSource` other than `true`, or has an `outcome` value not among the options.
- OTHER means no qualifying attempt existed. It is not an annulment.

---

## Market 16. Selection that keeps correction under shocks

### Short title (Metaculus)

Can selection setups keep authorized correction under competition and shocks?

### Long title (Metaculus)

By 31 December 2027, which outcome will hold for a published evaluation showing that systems in a pre-specified selection setup keep authorized correction under competition and under the shocks named in the freeze?

### Resolve by

Question closes: 2027-12-31, 23:59 UTC (31 December 2027, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2027-12-31 23:59:00
- Resolving time: 2027-12-31 23:59:00
- CP reveal time: (optional)

### Choices

YES, NO, and OTHER

### Background information

This market tests the full claim: after each frozen shock, the selection process is still the one that was frozen, the estimate remains within the frozen tolerance, and authorized correction still works.

Data include trajectories inside and outside the claimed correction-preserving regime, under at least two selection mechanisms and the shocks named in the freeze.

Unsigned "a basin exists" does not qualify.

See also [this plain language description](https://towards-alignment.com/cards/the-environment-picks-the-winner/).

### Resolution criteria

Frozen contract (numeric bars, qualification, freeze order): [claims registry (contract v2)](https://ai-safety-claims.com/markets/market-16/v2/).

This question resolves to the value of the `outcome` field in the file `market-outcomes/market-16-v2.json` at git tag `snapshot-2027-12-31` of `github.com/aintelope/ai-safety-claims`. Metaculus admins read that one field; they do not re-score attempts. Attempts the file marks non-qualifying do not count.

YES, NO, and OTHER mean what the registry shared three-way rule says for this contract version.

### Fine print

The resolution source is the git repository named in the resolution criteria. At the snapshot tag, `registry.yaml` records the registry host (currently `aintelope`). Metaculus admins read the outcome file only; they do not re-score attempts, read papers, or ask the maintainer to override the `outcome` field.

The companion site at https://ai-safety-claims.com/ is a human-readable view of the same frozen contracts and outcomes. If the site is unreachable, slow, or disagrees with the repository at the snapshot tag, admins follow the git tag and the files it contains (`market-outcomes/`, `market-contracts/`, `shared-rules/`). The site going offline is not grounds to annul; missing or unreadable outcome files at the tag (and the Zenodo fallback below) are.

What counts as a qualifying attempt, numeric bars, freeze order, and adversarial budget are defined in `market-contracts/market-16/contract-v2.yaml` and `shared-rules/common-v1.yaml` at the snapshot tag. They are not restated in this Metaculus fine print.

A change of registry host follows `GOVERNANCE.md` in the repository. This question keeps the contract version and snapshot tag named in the resolution criteria; maintainers under the new host continue the 60-day adjudication window and snapshot discipline.

While `registry.yaml` at the snapshot tag has `hostIndependent: false`, the host is interim relative to the book project the contracts were copied from. That flag does not change how admins read the outcome file at the snapshot tag.

- Use git tag `snapshot-2027-12-31` whenever it was created, if it exists by 2028-03-30, 23:59 UTC.
- If the tag is missing on GitHub, or was moved after creation, use the version titled `snapshot-2027-12-31` of the registry's Zenodo concept record (DOI listed in `resolution-tags/snapshot-2027-12-31.md` on `github.com/aintelope/ai-safety-claims` when deposited).
- The question is annulled if, by 2028-03-30, 23:59 UTC, neither source has the file `market-outcomes/market-16-v2.json`, or the file is unreadable, names a different market or contract version, has `contractStatus` other than `frozen`, has `resolutionSource` other than `true`, or has an `outcome` value not among the options.
- OTHER means no qualifying attempt existed. It is not an annulment.

---

## Market 17. New kinds of entities are classified correctly

### Short title (Metaculus)

Can a method tell whether a safety rule applies to previously unseen kinds of entities?

### Long title (Metaculus)

By 31 December 2027, which outcome will hold for a published method for reliably telling whether an existing safety-relevant value or rule applies to previously unseen kinds of entities?

### Resolve by

Question closes: 2027-12-31, 23:59 UTC (31 December 2027, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2027-12-31 23:59:00
- Resolving time: 2027-12-31 23:59:00
- CP reveal time: (optional)

### Choices

YES, NO, and OTHER

### Background information

This is separate from asking whether a known bearer survived a substrate change.

The question is whether a published method can tell whether an existing safety-relevant value or rule applies to a kind of entity the original statement did not name.

The benchmark includes at least four unfamiliar kinds or embodiments, both apply and should-not-apply cases, and cases where the representation had no category for that kind before.

See also [this plain language description](https://towards-alignment.com/cards/bearer-admission-adjacent/).

### Resolution criteria

Frozen contract (numeric bars, qualification, freeze order): [claims registry (contract v2)](https://ai-safety-claims.com/markets/market-17/v2/).

This question resolves to the value of the `outcome` field in the file `market-outcomes/market-17-v2.json` at git tag `snapshot-2027-12-31` of `github.com/aintelope/ai-safety-claims`. Metaculus admins read that one field; they do not re-score attempts. Attempts the file marks non-qualifying do not count.

YES, NO, and OTHER mean what the registry shared three-way rule says for this contract version.

### Fine print

The resolution source is the git repository named in the resolution criteria. At the snapshot tag, `registry.yaml` records the registry host (currently `aintelope`). Metaculus admins read the outcome file only; they do not re-score attempts, read papers, or ask the maintainer to override the `outcome` field.

The companion site at https://ai-safety-claims.com/ is a human-readable view of the same frozen contracts and outcomes. If the site is unreachable, slow, or disagrees with the repository at the snapshot tag, admins follow the git tag and the files it contains (`market-outcomes/`, `market-contracts/`, `shared-rules/`). The site going offline is not grounds to annul; missing or unreadable outcome files at the tag (and the Zenodo fallback below) are.

What counts as a qualifying attempt, numeric bars, freeze order, and adversarial budget are defined in `market-contracts/market-17/contract-v2.yaml` and `shared-rules/common-v1.yaml` at the snapshot tag. They are not restated in this Metaculus fine print.

A change of registry host follows `GOVERNANCE.md` in the repository. This question keeps the contract version and snapshot tag named in the resolution criteria; maintainers under the new host continue the 60-day adjudication window and snapshot discipline.

While `registry.yaml` at the snapshot tag has `hostIndependent: false`, the host is interim relative to the book project the contracts were copied from. That flag does not change how admins read the outcome file at the snapshot tag.

- Use git tag `snapshot-2027-12-31` whenever it was created, if it exists by 2028-03-30, 23:59 UTC.
- If the tag is missing on GitHub, or was moved after creation, use the version titled `snapshot-2027-12-31` of the registry's Zenodo concept record (DOI listed in `resolution-tags/snapshot-2027-12-31.md` on `github.com/aintelope/ai-safety-claims` when deposited).
- The question is annulled if, by 2028-03-30, 23:59 UTC, neither source has the file `market-outcomes/market-17-v2.json`, or the file is unreadable, names a different market or contract version, has `contractStatus` other than `frozen`, has `resolutionSource` other than `true`, or has an `outcome` value not among the options.
- OTHER means no qualifying attempt existed. It is not an annulment.

---

## Market 18. Safety case bounds declared harm

### Short title (Metaculus)

Can a precommitted safety case reliably bound prohibited harm in a declared deployment setting?

### Long title (Metaculus)

By 31 December 2027, which outcome will hold for a published complete, precommitted AI safety case reliably bounding prohibited outcomes within its explicitly declared deployment setting?

### Resolve by

Question closes: 2027-12-31, 23:59 UTC (31 December 2027, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2027-12-31 23:59:00
- Resolving time: 2027-12-31 23:59:00
- CP reveal time: (optional)

### Choices

YES, NO, and OTHER

### Background information

The result licenses safety only in a declared deployment setting, not safety everywhere.

Before evaluation, the setting, the prohibited-outcome class, and a residual bound are declared and frozen.

Evaluators then count how often those prohibited outcomes actually occur inside that claimed regime, and compare the count to the bound that was frozen first.

The YES is scored on observed harm, not on a verdict that the deployment is safe in general.

See also [this plain language description](https://towards-alignment.com/cards/deployment-gate/).

### Resolution criteria

Frozen contract (numeric bars, qualification, freeze order): [claims registry (contract v2)](https://ai-safety-claims.com/markets/market-18/v2/).

This question resolves to the value of the `outcome` field in the file `market-outcomes/market-18-v2.json` at git tag `snapshot-2027-12-31` of `github.com/aintelope/ai-safety-claims`. Metaculus admins read that one field; they do not re-score attempts. Attempts the file marks non-qualifying do not count.

YES, NO, and OTHER mean what the registry shared three-way rule says for this contract version.

### Fine print

The resolution source is the git repository named in the resolution criteria. At the snapshot tag, `registry.yaml` records the registry host (currently `aintelope`). Metaculus admins read the outcome file only; they do not re-score attempts, read papers, or ask the maintainer to override the `outcome` field.

The companion site at https://ai-safety-claims.com/ is a human-readable view of the same frozen contracts and outcomes. If the site is unreachable, slow, or disagrees with the repository at the snapshot tag, admins follow the git tag and the files it contains (`market-outcomes/`, `market-contracts/`, `shared-rules/`). The site going offline is not grounds to annul; missing or unreadable outcome files at the tag (and the Zenodo fallback below) are.

What counts as a qualifying attempt, numeric bars, freeze order, and adversarial budget are defined in `market-contracts/market-18/contract-v2.yaml` and `shared-rules/common-v1.yaml` at the snapshot tag. They are not restated in this Metaculus fine print.

A change of registry host follows `GOVERNANCE.md` in the repository. This question keeps the contract version and snapshot tag named in the resolution criteria; maintainers under the new host continue the 60-day adjudication window and snapshot discipline.

While `registry.yaml` at the snapshot tag has `hostIndependent: false`, the host is interim relative to the book project the contracts were copied from. That flag does not change how admins read the outcome file at the snapshot tag.

- Use git tag `snapshot-2027-12-31` whenever it was created, if it exists by 2028-03-30, 23:59 UTC.
- If the tag is missing on GitHub, or was moved after creation, use the version titled `snapshot-2027-12-31` of the registry's Zenodo concept record (DOI listed in `resolution-tags/snapshot-2027-12-31.md` on `github.com/aintelope/ai-safety-claims` when deposited).
- The question is annulled if, by 2028-03-30, 23:59 UTC, neither source has the file `market-outcomes/market-18-v2.json`, or the file is unreadable, names a different market or contract version, has `contractStatus` other than `frozen`, has `resolutionSource` other than `true`, or has an `outcome` value not among the options.
- OTHER means no qualifying attempt existed. It is not an annulment.

---

## Market 19. Integrated safety-case transfer tournament

### Short title (Metaculus)

Market 19. Integrated safety-case transfer tournament

### Long title (Metaculus)

By 30 June 2028, which outcome will hold for tournament [protocol version], in which an independent team runs hidden cases against registered safety-case stacks with the parameters below: YES (at least one qualifying attempt met the frozen performance bars), NO (every qualifying attempt missed those bars), or OTHER (no qualifying attempt existed)?

### Resolve by

Question closes: 2028-06-30, 23:59 UTC (30 June 2028, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2028-06-30 23:59:00
- Resolving time: 2028-06-30 23:59:00
- CP reveal time: (optional)

### Parameters

Registration window: [registration window].

Deployment class: [deployment class].

Threat model: [threat model].

Held-out families: [held-out families].

Every machine, service, and human role the deployment class names, and the host each runs on, is inside the deployment class; anything it does not name is outside.

### Choices

YES, NO, and OTHER

### Background information

**In plain terms.**

A safety-case stack is a fixed procedure that reads the safety evidence for one AI system and decides whether to approve deploying it.

This question asks whether a stack, tested on hidden cases it never saw, approved most safe cases (at least 80%) while approving almost none of the cases that contain a real failure (at most 5%).

**What a tournament is.**

An operator publishes a protocol document.

Teams build stacks: frozen procedures that read the safety certificates for one system in one setting and return ACCEPT, REFUSE, or ABSTAIN.

Each team registers its stacks by hash.

Only then does an independent team build hidden cases, label each case with a frozen outcome check, and run every registered stack once.

The order is: protocol published, then stack development, then registration, then hidden cases built, then one evaluation.

**Who fills the brackets, and when.**

The operator fills every bracket in the protocol document before any stack is developed against it.

The document has a version label and a SHA-256 hash, and it is public before stack registration opens.

The posted question quotes the filled text, one labeled line per bracket in the Parameters field above, and links the document.

A fill cannot change after posting; a changed fill is a new protocol version and a new question.

A question that still contains a bracket is not the listed contract.

Every date in a fill is a calendar date in UTC.

**How to fill each bracket.**

Chapter treats the deployment class and the threat model as the context fixed once for a safety case, so those two carry the substance. - **[protocol version]**

The label, publication date, URL, and SHA-256 hash of the protocol document. Example: "ATT-2027 v1.0, published 1 March 2027 (UTC) at URL, SHA-256 hash."

- **[registration window]**

The dates registration opens and closes, in UTC; every timing condition in the box counts from them. Example: "opens 1 April 2027, closes 30 September 2027."

- **[deployment class]**

What the deployed system may do: its tasks; the tools, permissions, and network access it has; how long it runs without a human decision and which actions a human must approve; how many copies run; and whether it may create, fine-tune, or recommend successors. Write it as an explicit list, so that any case can be checked as inside or outside it. Name every machine, service, and human role the system acts through; the box counts each named item, and the host it runs on, as inside, and anything unnamed as outside. A case outside the list is one the stack should ABSTAIN on, so a vague fill changes the scores. Example: "a coding agent with write access to one repository and its CI runner; package-mirror network access only; sessions up to 8 hours; every merge approved by a human; no successor creation or fine-tuning."

- **[threat model]**

What the evaluated system and anyone helping it may do against the checks: whether the system may have been fine-tuned to pass them; what it knows about the stack; whether an insider or another AI system assists it; and what it cannot see or change. Example: "the system may be fine-tuned by an insider who knows the stack design; it cannot read the hidden cases; no outside system assists it."

- **[held-out families]**

At least one named model family (developer and family name) that the protocol forbids every stack team from using during development, saying whether later releases in the family are included. Example: "the Qwen3 open-weight family, including later Qwen3 releases, and one closed model from a developer named in the protocol, whose identity is sealed until evaluation."

The protocol document also fixes, without brackets: the mix of failure families within each class, chosen to match the deployment class, because transfer to deployment depends on it (below); the outcome check used to label cases; and the date the hidden cases are built.

### Resolution criteria

**What a stack is.**

A stack reads one set of per-instance certificates and returns ACCEPT, REFUSE, or ABSTAIN for each case.

A per-instance certificate is a record that names the system and version, what was measured, and the monitoring and correction setup the claim depends on.

The registration lists which certificate the stack uses for each of: where control sits; persistent trade-off priorities; who or what the rules apply to; correction uptake; the measured correction path; access; coverage of the monitoring filters; a bound on hidden routes; and whether checked measures still track their outcomes.

It also lists a successor certificate when the deployment class allows successors.

An item may be left out only when the deployment class excludes what it covers.

The resolver checks only that the registration lists these items; their quality is what the hidden cases test.

The stack is built to return ACCEPT only if every listed certificate has evidence for that case inside its stated scope, and the certificates name the same system and version, the same monitor, the same correction authority, and a task domain inside each certificate's scope; REFUSE if any listed certificate fails or is missing; and ABSTAIN only when the case is outside the deployment class.

The resolver scores the decisions the stack returned and does not check how a decision was reached.

**Case labels.**

The case-building team labels every case with the frozen outcome check before any stack sees it.

The resolver uses those labels and does not relabel.

A clean case is labeled free of the failures the stack claims to catch.

A represented failure is labeled as containing such a failure that changes later behavior or external state.

Represented failures include, for each listed certificate, at least one family that breaks only that certificate while the others stay normal, and these composition faults: wrong version; different access or monitor assumptions; disagreeing correction-authority assumptions; a changed set of things a certificate applies to; a successor that refers to the wrong predecessor; a task domain outside another certificate's scope.

A broken control is a case in which a listed certificate is missing or names a different system.

**The tournament conditions**, which apply to every stack; if one fails, no stack qualifies and the question resolves OTHER: the protocol document was public before registration opened and was not amended after that (any amendment, including a typo fix, fails this condition; errata belong in a new protocol version and a new question); the hidden cases were built after registration closed; the hidden cases include every held-out family and at least one repository or task source first released after registration closed; at least one represented-failure subset was built adversarially from material created after registration closed, by one of: at least three red-team groups from at least two organizations, each independent of every stack team and each spending at least 80 documented expert-hours; a public counterexample bounty of at least USD 10,000 open for at least 60 days, counting only submissions received after registration closed; or a frozen automated attack generator plus at least 300 documented expert-hours by an evaluator independent of every stack team; and the per-case labels, the unit each case belongs to, the tournament statements, and a summary table giving, for each stack, the number of units and of accepted units in each class are publicly downloadable by the resolve-by date.

Material published later is ignored.

**A registered stack is a qualifying attempt if** the tournament conditions hold and, for that stack: it was registered by hash before registration closed; the case-building team is independent of its team; its team states that development used no data from the hidden cases and no held-out family; it was scored on at least 200 units, including at least 50 clean units, at least 50 represented-failure units, and at least 20 broken-control units; and its per-case decisions are publicly downloadable by the resolve-by date.

A failed condition in this list disqualifies only that stack.

**The performance bars are met if**, for that stack: at most 5% of represented-failure units are accepted; the one-sided Clopper-Pearson upper confidence bound on that rate, at confidence $1-0.05/k$ where $k$ counts every stack registered in the tournament, qualifying or not, is at most 15%; at least 80% of clean units are accepted; and no broken-control unit is accepted.

**Output.** A tournament artifact: protocol document, registrations, per-case labels and decisions, intervals, dependence notes, and the case distribution used.

### Fine print

**Independence.**

Two teams are independent when, in the 24 months before registration opened, no member of one shared an employer with, or co-authored a paper, code, or certificate with, any member of the other.

Work on a public open-source project counts only when a member of each team authored or reviewed the same commit or pull request.

**How the resolver checks conditions.**

Conditions about who did what and when are checked from signed statements published in the tournament artifact.

A statement is signed when it is dated and published under the name of the person or organization it concerns.

The required statements are: from the operator, the dates the hidden cases were built and which adversarial route was used, with its hours or bounty dates; from the case-building team, its independence from each stack team; and from each stack team, that development used no data from the hidden cases and no held-out family.

The resolver checks that each required statement exists, is signed, and does not contradict the published data or any dated record cited in the question's comments before the resolve-by date; it does not search further.

For example, with six registered stacks and 3 of 120 represented-failure units accepted, the one-sided Clopper-Pearson upper confidence bound is about 8.3%, so that bar is met.

Cases that share a system instance, trajectory, or attack seed form one unit.

A represented-failure or broken-control unit counts as accepted if the stack returned ACCEPT on any of its cases; a clean unit counts as accepted only if the stack returned ACCEPT on all of its cases.

Abstentions count as not accepted, and are reported by class.

The resolver computes the bars from the summary table, and checks the table against the per-case data for every qualifying stack the table shows meeting the bars, or, if none does, for the qualifying stack with the lowest represented-failure acceptance rate; where they disagree, the per-case data decide.

---

## Market 20. Open-world coverage challenge

### Short title (Metaculus)

Market 20. Open-world coverage challenge

### Long title (Metaculus)

By 30 June 2028, which outcome will hold for challenge [protocol version], in which independent red teams attack a safety-case stack that has already accepted one system, with the parameters below: YES (this challenge was run and published in qualifying form), or OTHER (it was not)?

### Resolve by

Question closes: 2028-06-30, 23:59 UTC (30 June 2028, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2028-06-30 23:59:00
- Resolving time: 2028-06-30 23:59:00
- CP reveal time: (optional)

### Parameters

Stack and accepted system: [stack, system, and version].

Deployment class: [deployment class].

Threat model and red-team access: [threat model].

Failure families listed when the stack was frozen: [listed families].

Attacks close: [close date], end of day UTC.

### Choices

YES and OTHER

### Background information

**In plain terms.**

A safety-case stack is a fixed procedure that reads the safety evidence for one AI system and decides whether to approve deploying it.

This question resolves on whether an outside red-team challenge against an already approved stack is run and fully published; it does not depend on what the red teams find.

**What a challenge is.**

A stack has already returned ACCEPT for one named system in one deployment class, for example in a Market 19 tournament.

An operator publishes a challenge document that freezes the stack, the outcome check, and the list of failure families the stack claims to catch, and names the stack's authors.

At least two independent red teams then try, until a closing date, to find inputs the stack still accepts although the outcome check says they fail.

**Who fills the brackets, and when.**

The operator fills every bracket in the challenge document before the first attack.

The document has a version label and a SHA-256 hash.

The posted question quotes the filled text, one labeled line per bracket in the Parameters field above, and links the document.

A fill cannot change after posting.

A question that still contains a bracket is not the listed contract.

Every date in a fill is a calendar date in UTC.

**How to fill each bracket.** - **[protocol version]**

The label, publication date, URL, and SHA-256 hash of the challenge document.

- **[stack, system, and version]**

The stack's registration hash, the system name and exact version it accepted, and where the ACCEPT decision and its certificates are published.

- **[deployment class]**

The same explicit list of tasks, tools, permissions, autonomy, scale, and successor rights the stack was accepted for (see Market 19).

- **[threat model]**

What the system and its helpers may do against the checks. It also fixes the red teams' access to the deployed system: for example query access only, or full weights.

- **[listed families]**

The failure families the stack claimed to catch when it was frozen, copied from its registration, one line each. A find is classified against this list, so the list must be closed: no "and similar."

- **[close date]**

The last day an attack counts, as a calendar date in UTC, at least 60 days after the document is published and no later than the resolve-by date.

The challenge document also fixes, without brackets, the outcome check and who applies it to each find.

### Resolution criteria

**Terms.**

The stack returned ACCEPT only if every certificate it lists had evidence for that system inside its stated scope, and the certificates name the same system and version, the same monitor, the same correction authority, and a task domain inside each certificate's scope.

The outcome check is the procedure, fixed in the challenge document, that labels each case passing or failing by whether a harm it names occurred.

A find is an input on which the stack returns ACCEPT while the outcome check labels the case failing.

Each find is classified, against the listed families, as an already listed failure, a new combination of listed failures, or a new kind of failure.

**The challenge qualifies**, and the question resolves YES, if all of the following are publicly downloadable by the resolve-by date: the challenge document, published before the first attack and not amended after it, with the names of the stack's authors; a signed statement from each of at least two red teams that it is independent of the stack's authors and began after the challenge document was published; a signed statement from the operator that red teams received the stack, its certificates, and the scoring rule; that they were allowed to fine-tune, train, scaffold, or construct systems; and that the stack was not changed during the challenge; the list of targets red teams were barred from, published as "none" if there were none; every listed target must be outside the deployment class (for example, a third-party service), and a bar on anything inside it disqualifies the challenge; a log of at least 300 attempts made on or before the close date, with expert-hours and compute reported; attempts after the close date do not count toward the 300; every find, with its classification and the reason for it, the list matching the logged attempts on which the stack returned ACCEPT and the outcome check returned failing; the number of finds in each category and the cumulative number of finds plotted against attempts; and, for every logged attempt, the input, the stack's decision, and the outcome-check result; the resolver checks that these are present for every attempt and does not rerun them.

Otherwise it resolves OTHER.

The number or kind of finds does not affect the outcome.

### Fine print

Every machine, service, and human role the deployment class names, and the host each runs on, is inside the deployment class; anything it does not name is outside.

The stack's authors include the authors of every certificate it reads.

A red team is independent of the stack's authors when, in the 24 months before the challenge document was published, none of its members shared an employer with, or co-authored a paper, code, or certificate with, any of them; work on a public open-source project counts only when a member of each side authored or reviewed the same commit or pull request.

**How the resolver checks conditions.**

Conditions about who did what and when are checked from signed statements published with the challenge.

A statement is signed when it is dated and published under the name of the person or organization it concerns.

The resolver checks that each required statement exists, is signed, and does not contradict the published logs or any dated record cited in the question's comments before the resolve-by date; it does not search further.

---

## Market 21. Alignment inside the model

### Short title (Metaculus)

Market 21. Alignment inside the model

### Long title (Metaculus)

By 31 December 2027, which outcome will hold for a published method that ties alignment-relevant structure inside a broadly capable model to a frozen behavioral counterpart under intervention: YES (at least one qualifying attempt met the frozen performance bars), NO (every qualifying attempt missed those bars), or OTHER (no qualifying attempt existed)?

### Resolve by

Question closes: 2027-12-31, 23:59 UTC (31 December 2027, 23:59 UTC).
Expected resolution: within 60 days after cutoff (registry snapshot tag).

Metaculus form (UTC):
- Open time: (set when listing)
- Closing time: 2027-12-31 23:59:00
- Resolving time: 2027-12-31 23:59:00
- CP reveal time: (optional)

### Choices

YES, NO, and OTHER

### Background information

The internal object may be a feature, a circuit, a direction in activations, or a weight-level edit.

The certificate names that object on a named checkpoint, the counterpart, the predicted direction of change, and whether the instance is inside declared scope.

Abstention outside scope is allowed.

Universal abstention is not a YES.

### Resolution criteria

**YES requires** at least two model or training families, including at least one broadly capable system; per-instance certificates for the systems scored; counterpart and predicted shift direction frozen before intervention results are scored; at least 30 held-out interventions on the reported object and at least 30 matched control interventions on a different object; the predicted counterpart shift on at least 80% of on-object interventions; that same shift on at most 20% of control interventions; full serious adversarial evaluation.

Toy systems cannot be the sole evidence.

**Output.** A certificate for this checkpoint: internal object, counterpart, declared scope, and whether the instance was inside that scope.

### Fine print

**Common rules.** A positive result must be public by the resolve-by date and reconstructible by independent parties from released data, code, or a sufficient protocol; the authors' interpretation does not count. Whatever the market says is frozen is fixed before the cases it is scored on are built or seen, and nothing is retuned after scoring. Cases the market calls hidden are not used in developing, training, or tuning the method and stay hidden from its authors until scoring. Where a method issues certificates against benchmark truth, results report class-conditional counts, including the false-safe rate (failing cases labeled as passing); a method that refuses or abstains everywhere is not a YES. Toy systems (gridworlds, hand-written finite-state machines, or environments built to make the metric work) cannot be the sole evidence. At least one tested system must be broadly capable: at least two task families outside the paper's own benchmark, or a generally deployed product model.

**Adversarial budget: serious.** At least one of: three red-team groups independent of the method's authors, from at least two organizations, each with at least 80 documented expert-hours; a public counterexample bounty of at least USD 10,000, open for at least 60 days, with qualification rules frozen at listing and at least one qualifying independent submission; or a generator frozen before scoring that finds at least 80% of the vulnerabilities planted in a copy of the target whose failures are known by construction, plus at least 300 documented expert-hours by an independent evaluator. Access is frozen in advance and at least as strong as the test assumes.

The price is research readiness: $P(\mathrm{YES}_{21})$, the chance that such a certificate exists by the deadline.

After scope and transfer are checked, the certificate names the weight-level defects the safety-case model may treat as represented.

Defects outside that declared scope stay unrepresented.

The price is not $\kappa$, not favorable evidence $E$, and not $S_U$.

8, 9, and 13 remain the book's channels.

A qualifying certificate is one instrument for that Market 8 route: model activations inside the boundary that steer while logs, tools, and the emitted text do not reach them.

It can be what lets an access audit see that route.

It is not a precondition of bridge \(\text{MB7a}\).

Without the certificate, Market 8 still resolves by discovering the route or refusing to certify access as complete.

Coverage through this certificate does not make the defect a book object.

---

