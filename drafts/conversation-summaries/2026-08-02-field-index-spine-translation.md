# Field index: dissolve missing-bridge table

**Date:** 2026-08-02  
**Scope:** After Phase 3 Lean decisions, fold the missing-bridge candidates table into coverage-matrix reading rules.

## Context

User asked whether the **Missing-bridge candidates** table could be dissolved now that every row had a Phase 3 disposition and no new `MB*` column was added.

## Decision

**Yes** — the table was decision debt; the agenda × bridge matrix already holds the durable evidence mapping.

## Changes

- `reference/field-agendas/field-agenda-index.md` — removed `## Missing-bridge candidates`; added **How to read matrix cells (spine translation)** under **Coverage vs book treatment**; updated Kosoy row + catalog ev-133
- `drafts/field-claim-formalization-and-bridge-review-plan.md` — scope note (table dissolved)
- `metadata/TODO.md` — misspec item points at new location
- `drafts/conversation-summaries/HANDOFF.md` — open work trimmed

## Open / next

- App B / matrix prose sync when authorized
- Optional Lean catalog rows for new finite modules (TSA row)

## Verification

- Doc-only; no Lean rebuild required
- Commit: `6f3762a9`
