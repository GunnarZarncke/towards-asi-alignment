# 2026-07-27 — ET-4 replay deployment bundle

## Trigger
User asked to add the ET-4 replay trace to the repository so it can be deployed to the companion site for demoing.

## Done
- Removed the ignore rule for `demos/ch07-lab-sim-replay/data/et4_case_brief.json`.
- Prepared the 7.6 MB ET-4 replay bundle to be tracked with the repository.

## Decisions
- Keep the generated JSON in the repository for now, as requested, rather than changing deployment to regenerate it.

## Open / next
- Stage and commit the authorized replay bundle and ignore-rule change when requested.
- Run the site deployment/build and verify the production URL after deployment.

## Key paths
- `demos/.gitignore`
- `demos/ch07-lab-sim-replay/data/et4_case_brief.json`
- `site/scripts/lib/publish-chapter-demos.mjs`

## Commits
- None.
