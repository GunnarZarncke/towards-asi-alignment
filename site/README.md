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

Production builds for GitHub Pages use base path `/towards-asi-alignment`; local serve uses `/` for simpler URLs.

Manual equivalent:

```bash
cd site
npm install
ASTRO_BASE=/ npm run sync
ASTRO_BASE=/ npm run dev
```

`npm run dev` syncs chapter metadata from `metadata/book.yml`, then starts Astro with hot reload. Edit cards under `src/content/cards/` or pages under `src/pages/` and refresh.

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
| `src/pages/` | Routes (Start Here, FAQ, book map, card/path indexes) |
| `src/content/cards/` | Short concept, bridge, artifact, and glossary cards |
| `src/content/paths/` | Fixed audience reading paths |
| `scripts/sync-book-yml.mjs` | Generates `src/data/book.json` from `metadata/book.yml` |
| `astro.config.mjs` | Site URL and GitHub Pages base path |

## Deploy

Pushes to `main` run `.github/workflows/site.yml`, which builds `site/` and pushes `site/dist/` to the `gh-pages` branch.

**One-time GitHub setup** (after the first successful workflow run creates `gh-pages`):

1. **Settings → Pages**
2. **Source:** Deploy from a branch
3. **Branch:** `gh-pages` / `/ (root)`

Live URL: **https://gunnarzarncke.github.io/towards-asi-alignment/**

We use a branch push (`peaceiris/actions-gh-pages`) instead of the GitHub Pages Deployment API because overlapping deploys were stuck in `deployment_queued` for 10 minutes.
