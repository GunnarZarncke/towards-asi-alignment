# 2026-07-17 — Content sync plumbing

## Trigger

User approved the "Content sync plumbing" plan (`~/.cursor/plans/content_sync_plumbing_4f52d78d.plan.md`, not edited) and asked to implement all ten phases without stopping, marking to-dos in progress as work proceeded. This log covers phases 7–10; phases 0–6 (schema, glossary/terminology retirement, bridges, projections, remaining concept kinds, notation) were completed in an earlier segment of the same session.

## Done

- **Phase 7 — releases.** Added `site/scripts/sync-releases.mjs`, which parses `RELEASE_NOTES.md` `## vX.Y.Z — date — title` sections into `release-vX-Y-Z.md` cards plus the `releases-updates` hub card. Fixed two bugs found during verification: the generated title/tag URL were missing the `v` prefix, and the summary picker was grabbing a leading `Commit: ... · Tag: ...` metadata line instead of the first descriptive paragraph (now skips metadata-only paragraphs). Untracked the three hand-written release cards from git (`git rm --cached`) and added them to `site/.gitignore`, matching how the other generated card families were retired earlier in the session.
- **Phase 8 — search index + chapter `related[]`.** Added `site/scripts/build-search-index.mjs`, which writes `site/public/search-index.json` (title/type/summary/url) from every root concept/bridge/projection/release/artifact card, chapter/appendix/frontmatter cards, experiment cards, and notation symbols — reference cards (~380 bibliography entries) are excluded by design. Wired it into `npm run sync` (as `build:search-index`, last step) and into `npm run check:concepts` (`--check` mode, diff-only). Confirmed `sync-chapter-cards.mjs`'s existing `listConceptCards()` already sources `related[]` from the generated root-card frontmatter (itself now generated from `concepts.yml`/`bridges.yml`/`projections.yml`), so no change was needed there — it was already reading "from the roster" once the earlier phases switched the underlying cards to generated output. No search UI was wired up; per the plan this is a deferred follow-up.
- **Phase 9 — claim ledger linking.** Added an optional `claimId` field: `content.config.ts` schema, the `simpleKeys` serialization list in `scripts/lib/concepts-yaml.mjs`, and a `--check`-mode-independent warning (not a hard failure) in `sync-concepts.mjs` if a `claimId` isn't found as a `## Claim ID: C-...` heading in `metadata/claims-ledger.md`. Populated the six claim IDs the ledger already names explicitly (its intro line: "the six named Introduction claims map to claims C-003 ... C-007") onto their corresponding existing concepts: `boundary-discovery` → `C-003`, `value-bundle-transport` → `C-004`, `grounding-viability` → `C-004a`, `correction-channel-integrity` → `C-005`, `successor-stability` → `C-006`, `attractor-control` → `C-007`. Added a small side-panel link on the card page ("Claims ledger: C-XXX") pointing at the GitHub-anchored heading in `claims-ledger.md`, alongside the existing `external` links list. The ledger itself is untouched — it stays the manually maintained audit ground truth.
- **Phase 10 — cleanup + docs.** Confirmed the retired JSON registries (`terminology.md`, `field-subsumptions.json`, `field-subsumption-gems.json`) are already gone from disk from earlier phases; deleted the now-stale one-shot migration script `scripts/export-cards-to-yaml.mjs` (its job was done and it referenced files that no longer exist). Updated `site/README.md`'s content-layout table with the new sync scripts and YAML rosters, and added a short paragraph noting that most root cards are generated and pointing at `npm run check:concepts` for the no-write validation gate. Wrote this log and the `INDEX.md` row.

## Decisions

- Search index entries store a plain root-relative `url` (the site has no `base` path) rather than a bare card id, since `public/search-index.json` is a static asset fetched at runtime by future client-side search code, not something Astro re-resolves through `BASE_URL` at request time.
- `claimId` mismatches only warn, never fail the build or `--check`, per the plan ("validation warnings only") — the claims ledger is deliberately not merged into `concepts.yml` and stays a manually maintained audit artifact.
- Six `claimId` values were populated (not left at zero) because the ledger's own text already names the exact concept-to-claim mapping for those six; the plan's own schema example (`claimId: C-004a` on `grounding-viability`) confirmed the intended pairing. No other concepts were assigned a `claimId` — guessing beyond the ledger's explicit statement would be scope creep.

## Open / next

- No header/command-palette search UI consumes `search-index.json` yet — building one is explicitly deferred in the plan ("Wire header search (separate small task)").
- `npm run check:concepts` is not wired into `.github/workflows/site.yml`; the site build already regenerates all cards fresh on every CI run via `prebuild`, so drift can't reach `main`, but the check script isn't yet a separate fast-fail CI step.
- Only 6 of the ~48 concepts carry a `claimId`; extending coverage would require deciding the mapping for the remaining claims in `metadata/claims-ledger.md`, which the ledger doesn't state explicitly.

## Key paths

- `metadata/concepts.yml`, `metadata/bridges.yml`, `metadata/projections.yml` — YAML rosters (source of truth)
- `metadata/concepts/bodies/*.md` — hand-written card bodies
- `site/scripts/sync-concepts.mjs`, `sync-bridges.mjs`, `sync-projections.mjs`, `sync-notation.mjs`, `sync-releases.mjs`, `build-search-index.mjs` — generators
- `site/scripts/lib/concepts-yaml.mjs` — shared YAML/card-rendering helpers
- `site/public/search-index.json`, `site/src/data/notation.json`, `site/src/data/glossary.json` — generated data files (gitignored)
- `site/src/pages/glossary/index.astro`, `site/src/pages/notation/index.astro`, `site/src/pages/updates/index.astro` — new/updated site routes
- `metadata/claims-ledger.md` — manually maintained claim audit ledger (unchanged, now optionally linked from concepts)

## Commits

- None yet — changes are unstaged in the working tree pending user review.
