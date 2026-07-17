# Companion site

Static Astro site for *Towards Superintelligence Alignment*. The PDF remains the canonical long-form artifact; this site is an orientation layer (Start Here, cards, paths, FAQ, book map).

## Why not open `dist/index.html` directly?

Built HTML expects a web server. Opening a file in the browser (`file://`) has no server at that path, so CSS and internal links break.

Use a local dev server instead.

## Local development (recommended)

From anywhere (script resolves the repo root):

```bash
/path/to/towards-asi-alignment/serve-site.sh
```

Or from the repo root:

```bash
./serve-site.sh
```

The script stops any previous local Astro server, syncs content, starts the dev server, and prints the URL (default: **http://localhost:4321/**). Example chapter: **http://localhost:4321/book/ch06/**.

Local dev and production both use site root `/` (custom domain **https://towards-alignment.com/**).

Manual equivalent:

```bash
cd site
npm install
npm run sync   # runs generate_manuscript_tex.sh, then syncs chapters/cards
npm run dev
```

After a fresh clone, `npm run sync` regenerates gitignored manuscript `.tex` fragments (`metadata/*-index.tex`, `tables/chapter-map.tex`, etc.) before resolving cross-references. Same step runs in CI (`prebuild`).

`npm run dev` syncs chapter metadata from `metadata/book.yml`, then starts Astro with hot reload. Edit cards under `src/content/cards/` or pages under `src/pages/` and refresh.

Most root-level cards (concept, glossary, bridge, projection, release) are **generated** from `metadata/concepts.yml`, `metadata/bridges.yml`, `metadata/projections.yml`, and `RELEASE_NOTES.md` — edit the YAML roster or body file under `metadata/concepts/bodies/`, not the generated `.md` card, then re-run `npm run sync`. `npm run check:concepts` diffs the roster against the generated output (and the search index) without writing, for CI.

## Preview the production build

To test exactly what GitHub Pages will serve:

```bash
./serve-site.sh --preview
```

Manual equivalent:

```bash
cd site
npm run build
npm run preview
```

## Build only

```bash
cd site
npm run build
```

Output: `site/dist/`

## Content layout

| Path | Purpose |
|------|---------|
| `src/pages/` | Routes (Start Here, FAQ, book map, card/path indexes, `/glossary/`, `/notation/`, `/updates/`) |
| `src/content/cards/` | Short concept, bridge, artifact, glossary, and **release** cards — mostly generated, see below |
| `src/pages/updates/` | Releases & updates — newest version card first (`CardSection` initial count 1) |
| `src/content/reading-paths/` | Fixed audience reading paths (loaded at build/dev time) |
| `metadata/concepts.yml` | Roster for concept/glossary/gem/institutional/objection/standalone-claim cards; bodies in `metadata/concepts/bodies/*.md`; optional `claimId` link to `metadata/claims-ledger.md` |
| `metadata/bridges.yml` | Roster for the `mb1`–`mb10` + `bridge-assumptions` cards; cross-checked against `appendices/appB-bridge-crosswalk.tex` |
| `metadata/projections.yml` | Roster for field-projection cards (external agenda ↔ book invariants; display title `Field projection — ...`) |
| `scripts/sync-concepts.mjs` | Generates cards from `concepts.yml` plus `src/data/{glossary,part-gems,standalone-claims}.json`; `--check` diffs without writing |
| `scripts/sync-bridges.mjs` | Generates bridge cards from `bridges.yml` (+ appB parse); `--check` diffs without writing |
| `scripts/sync-projections.mjs` | Generates projection cards from `projections.yml` plus `src/data/field-projection{,-gems}.json`; `--check` diffs without writing |
| `scripts/sync-notation.mjs` | Generates `src/data/notation.json` for `/notation/` from `metadata/notation.md` (no per-symbol cards) |
| `scripts/sync-releases.mjs` | Generates release cards + the `/updates/` hub card from `RELEASE_NOTES.md` |
| `scripts/build-search-index.mjs` | Generates `public/search-index.json` from concepts, chapter/appendix/experiment cards, and notation (excludes the ~380 reference cards) |
| `scripts/sync-chapter-cards.mjs` | Generates chapter/appendix cards; `overviewOnly` appendices (e.g. `appM`) render as case-study hubs at `/cards/chapters/{id}/` with full synced text at `/full/` |
| `scripts/sync-book-yml.mjs` | Generates `src/data/book.json` from `metadata/book.yml` |
| `scripts/sync-experiments.mjs` | Generates `src/data/experiments.json` and experiment cards from `metadata/experiments.yml` (includes lab-sim **Lean leak-proof** link when `leakProofPath` is set) |
| `astro.config.mjs` | Site URL (`https://towards-alignment.com`), `@astrojs/sitemap`, build options |
| `public/robots.txt` | Crawler rules and sitemap index URL |
| `public/og-image.png` | Default Open Graph / Twitter preview image (1200×630) |
| `src/lib/seo.ts` | Site name, canonical URL helpers, default description |

## Deploy

Pushes to `main` run `.github/workflows/site.yml`, which builds `site/` and pushes `site/dist/` to the `gh-pages` branch via **branch-based** publishing (`peaceiris/actions-gh-pages`).

This is **not** a custom GitHub Actions Pages deployment (the Deployment API). With custom Actions deployments, the domain is configured only in repository settings and a deployed `CNAME` file is ignored. Here, branch publishing applies: the workflow’s `cname: towards-alignment.com` writes `CNAME` on `gh-pages`, which GitHub Pages reads for the custom domain.

**One-time GitHub setup** (after the first successful workflow run creates `gh-pages`):

1. **Settings → Pages**
2. **Source:** Deploy from a branch
3. **Branch:** `gh-pages` / `/ (root)`
4. **Custom domain:** `towards-alignment.com` (DNS must point at GitHub Pages; align with the workflow `cname` value)
5. **Enforce HTTPS** once the certificate is ready

Live URL: **https://towards-alignment.com/**

**Redirect chain** (desired end state):

```text
https://gunnarzarncke.github.io/towards-asi-alignment/<path>
    └── GitHub-managed 301 redirect
          └── https://towards-alignment.com/<path>
```

The Astro build serves at site root (`base` omitted); only the deployment prefix is removed from URLs. After the custom domain is active, verify:

```bash
curl -I https://gunnarzarncke.github.io/towards-asi-alignment/
curl -I https://gunnarzarncke.github.io/towards-asi-alignment/cards/corrigibility/
curl -I https://gunnarzarncke.github.io/towards-asi-alignment/towards-superintelligence-alignment.pdf
```

The book PDF is copied into `site/public/` during build (`npm run copy:pdf`) from `dist/pdf/towards-superintelligence-alignment.pdf` (run `./build.sh` locally) or fetched from the latest GitHub Release in CI. Nav and footer **PDF** links open it directly in the browser.

We use a branch push (`peaceiris/actions-gh-pages`) instead of the GitHub Pages Deployment API because overlapping deploys were stuck in `deployment_queued` for 10 minutes.
