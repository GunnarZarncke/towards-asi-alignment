# 2026-07-16 — Site custom domain (towards-alignment.com)

## Trigger
Configure the Astro companion site for custom domain `towards-alignment.com`: remove GitHub Pages project-path base, keep page routes stable, and align branch-based peaceiris deploy with GitHub-managed redirects from the old project URL.

## Done
- `site/astro.config.mjs`: `site: "https://towards-alignment.com"`, removed `/towards-asi-alignment` base and `ASTRO_BASE` override.
- `.github/workflows/site.yml`: `cname: towards-alignment.com` on `peaceiris/actions-gh-pages` (branch publish, not Deployment API).
- `serve-site.sh`, `site/package.json`: dropped obsolete `ASTRO_BASE=/` local overrides.
- `site/src/data/author-profile.json`: PDF URL → custom domain.
- `site/README.md`: branch vs custom Actions deploy distinction, redirect chain, curl verification examples.
- Did **not** add `site/public/CNAME` — peaceiris `cname` is authoritative for branch deploy.
- Build verified locally (`npm run build`, 703 pages, root-relative routes).

## Decisions
- Keep internal routes unchanged (`/cards/...`, not `/concepts/...`); migration strips only the deployment prefix.
- `cname` in workflow only (no duplicate `public/CNAME`) after clarifying branch-based vs custom Actions Pages deployments.
- Left root `README.md` / `docs/MANUSCRIPT.md` github.io links unchanged this session.

## Open / next
- GSC: after deploy, submit `sitemap-index.xml`; request indexing on key URLs; Enforce HTTPS.
- Optional: compress `og-image.png` (~1.3 MB).

## Key paths
- `site/astro.config.mjs`
- `.github/workflows/site.yml`
- `site/README.md` (Deploy section)

## Commits
- `0cdad42` Configure Astro site for towards-alignment.com custom domain.
