---
title: "AI safety claims registry"
type: external-service
status: framework
summary: "Versioned market contracts, filed attempts, and outcome files that a Metaculus admin reads at a named git snapshot — not crowd judgment on the book site."
related:
  - chapters/appP
  - predictions/overview
  - funding/prediction-evaluation-program
external:
  - label: Registry site
    url: https://ai-safety-claims.com/
  - label: Source (GitHub)
    url: https://github.com/aintelope/ai-safety-claims
  - label: Evaluation workbench
    url: https://github.com/aintelope/ai-safety-claims-workbench
---

**Resolution layer.** Catalog markets 1–13 and 15–18 resolve from outcome files in this registry, not from Appendix H prose or Metaculus crowd judgment alone.

Each market has a frozen contract with numeric bars, reporting rules, and machine checks. Anyone may file a qualifying attempt; the registry maintainer adjudicates what scripts cannot decide. A Metaculus admin reads the published outcome file at a named git tag.

## Outcomes

- **YES**: at least one qualifying attempt met the frozen performance bars.
- **NO**: every qualifying attempt missed the bars.
- **OTHER**: no qualifying attempt existed.

A YES does not discharge any MB* bridge or certify a frontier deployment.

## Scope

Bootstrap snapshot `snapshot-0` is tagged in the registry. Metaculus listing text points admins at the `outcome` field in each `market-outcomes/market-NN-vK.json` file at that tag.

The current host is not independent of the book project; attempts by the book author or aintelope are not accepted until transfer.

Market 14 is outside this registry (YES/NO only, platform-adjudicated from public documents). Markets 19–21 remain in the appendix until Phase 4.
