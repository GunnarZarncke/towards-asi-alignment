# Six-claims spine plan

Status as of 2026-08-17. Canonical audit artifact: [`drafts/claim-spine.md`](../claim-spine.md).

## Goal

Keep the Introduction's six thesis claims as the reader contract; align safety-case enumerations, part/chapter navigation, ch48 discharge, companion site, and tooling without promoting second-tier ledger claims (C-008–C-011) to intro status.

## Phases

| Phase | Description | Status |
|-------|-------------|--------|
| **0** | Audit artifact (`drafts/claim-spine.md`) | Done |
| **1** | Consistency fixes (ch48 six, C-044, ch30 count, executive-overview order) | Done |
| **2** | Navigational spine (intro labels, `sec:how-claims-unfold`, `tables/claim-spine.tex`) | Done |
| **3** | Dedupe safety-case enumerations (`claim-layer-map.tex`, ch03 shorten) | Done |
| **4** | Part openers + first-chapter epistemic tags | Done |
| **5** | ch48 discharge (status table, C-008–C-011 subsection) | Done |
| **6** | Companion site + `check_claim_spine.py` | Done |

## Phase 6 deliverables

- **`six-thesis-claims` concept card** — `metadata/concepts/bodies/six-thesis-claims.md` + roster entry in `metadata/concepts.yml`
- **Homepage callout** — reader contract vs standalone publishable notes (`site/src/pages/index.astro`)
- **Reading paths** — early step on all four guided paths
- **`llms.txt`** + FAQ entry
- **Cross-link** from `standalone-claims` card
- **`scripts/check_claim_spine.py`** — intro labels, spine tables, concepts roster, part openers; wired into `make check`

## Distinctions

| Artifact | Purpose |
|----------|---------|
| Six thesis claims | Introduction reader contract; discharged in ch48 |
| Standalone claims | Four extractable publishable notes (`site/src/data/standalone-claims.json`) |
| ch03 Claims 0–6 | Dynamical guarantee preview (+ capability, bearer split) |
| ch33 checklist (9) | Deployment certification |
| ch42 layers (8) | Full GSN-style safety case |

## Commits

- `e76251c9` — Phases 0–2 + language pass on intro/part openers
- `16d78603` — Phases 3–5 (layer map, ch03 dedup, chapter tags, ch48 tables)
- *(pending)* — Phase 6 companion site + check script + plan update

## Optional follow-ups

- None required from original plan scope.
- If intro claims change, update `drafts/claim-spine.md`, shared LaTeX tables, `six-thesis-claims` card body, and re-run `make check`.
