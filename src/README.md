# Chapter demos (experimental)

Interactive mini apps that illustrate ideas from individual manuscript chapters.
These are **research toys**, not part of the LaTeX book build and not linked from
the published PDF.

## Layout

```text
src/
  README.md                 # this file
  serve.py                  # local dev server for all demos
  index.html                # landing page listing demos
  package.json              # shared TypeScript build + tests
  build-demos.mjs           # compiles each demo's main .ts → .js
  demos/
    chNN-short-slug/        # one folder per chapter demo
      README.md             # optional chapter-specific notes
      index.html            # demo page (required)
      *.ts                  # static demos: main module + optional *.test.ts
      *.js                  # esbuild output (committed for Python-only serve)
      app.py                # optional Python backend (FastAPI)
      backend.json          # optional: port + uvicorn module for app.py demos
      requirements.txt      # optional Python deps for backend demos
      tests/                # optional pytest suite for backend demos
```

**Naming:** `chNN-short-slug` matches chapter number and topic, e.g.
`ch09-uad-coalition-board` for Chapter 9 (*The Real Agent May Be Composite*).

Each demo folder must include `index.html`. Static TypeScript demos use either
`app.ts` or a single non-test `*.ts` file. Python backend demos add `app.py`,
`backend.json`, and `requirements.txt`; `serve.py` starts uvicorn for them
automatically on the configured port.

## Run locally

```bash
cd src
python3 serve.py
```

Opens `http://127.0.0.1:8765/` with a demo index. TypeScript is auto-built when
source is newer than output (requires Node.js / `npx`). Use `--no-build` if JS is
already up to date, or `--no-open` to skip the browser tab.

## Develop

```bash
cd src
npm install          # once
npm run build        # compile all demos
npm test             # vitest across demos/**/*.test.ts
```

## Add a new demo

1. Create `demos/chNN-your-slug/` with `index.html`.
2. For a **static** demo, add main `app.ts` (or one named module).
3. For a **Python backend** demo, add `app.py`, `backend.json` (port + module),
   and `requirements.txt`.
4. Add a row to `src/index.html` linking to `demos/chNN-your-slug/`.
5. Run `npm run build` or start `serve.py` to compile static demos.
6. Optional: add `demos/chNN-your-slug/README.md` with scope and limitations.

Do **not** wire demos into `book.tex`, chapter `.tex` files, or the PDF unless
explicitly requested later.

## Current demos

| Folder | Chapter | Summary |
|--------|---------|---------|
| `demos/ch09-uad-coalition-board/` | 9 — The Real Agent May Be Composite | Posting board → manual or dummy UAD coalition discovery |
| `demos/ch16-value-bundle-simulator/` | 16 — The Value-Bundle Model | Ecology sliders → top value salience |
