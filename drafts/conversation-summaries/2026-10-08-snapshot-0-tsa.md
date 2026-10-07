# 2026-10-08 — snapshot-0 TSA pin

kind: new-work
uptake: status

## Trigger
Pin registry bootstrap tag `snapshot-0` on the TSA side after tagging in `ai-safety-claims` (`3563a88`).

## Done
- content: **`metadata/predictions.yml`** — `snapshotTag: snapshot-0`.
- content: **`appendices/appP-bridge-predictions.tex`** — catalog markets reference tag; per-market authbars note host not independent.
- content: **`site/scripts/sync-predictions.mjs`**, **`site/src/pages/predictions/index.astro`** — cards and hub cite snapshot tag when pinned.
- content: **`drafts/plans/predictions/eval-registry-split.md`** — step 6 next; step 4 tag done.
- bookkeeping: **`npm run sync:predictions`**, **`npm run sync:chapters`** — OK.

## Decisions
- TSA pins tag name only; claims repo owns `resolutionSource` and outcome files.
- Appendix keeps host-independence caveat for attempt acceptance.

## Open / next
- Push `ai-safety-claims` commit and `snapshot-0` tag to origin.
- Metaculus listing (step 6); Zenodo deposit for snapshot-0.

## Commits
- (this session)
