# 2026-08-04 — Site PDF fetch rate-limit fix

## Trigger
GitHub Actions site build failed on `copy:pdf`: unauthenticated Releases API returned `403 rate limit exceeded` on the first CI run of the day.

## Done
- **`site/scripts/lib/fetch-book-pdf-core.mjs`** — prefer direct release download URL (`/releases/latest/download/…`); fall back to authenticated Releases API when `GITHUB_TOKEN` is set; retry 403/429 with backoff.
- **`metadata/TODO.md`** — optional LaTeX PDF CI compile-gate item (path-filtered `./build.sh`; does not publish to site).
- Verified locally: `CI=true npm run copy:pdf` downloads ~53 MB PDF and copies to `site/public/`.

## Decisions
- **Keep release fetch for site deploy** — site PDF continues to track latest GitHub Release, not HEAD on every push.
- **Skip separate PDF CI workflow for now** — would be compile test only (no site publish); logged as optional TODO rather than implementing.
- **Do not fold `./build.sh` into `site.yml`** — ~1300 pp LaTeX build is slow and biber-flaky; site deploy should stay fast.

## Open / next
- Push commit and re-run failed Site workflow on `main`.
- Optional later: path-filtered `book-pdf.yml` per `metadata/TODO.md` § Build / tooling.

## Key paths
- `site/scripts/lib/fetch-book-pdf-core.mjs`
- `site/scripts/copy-book-pdf.mjs`
- `.github/workflows/site.yml`
