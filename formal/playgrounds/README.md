# Lean playgrounds (Lean 4 Web)

Self-contained snippets for [Lean 4 Web](https://live.lean-lang.org/). Each file must compile **without** the book spine or Mathlib — copy the minimum finite toy model needed.

The site sync script (`site/scripts/sync-lean-spine.mjs`) reads every `*.lean` file here, builds a [Lean 4 Web](https://live.lean-lang.org/) link, and attaches it to the matching proof-spine node.

URL encoding (`site/scripts/lib/lean4web-url.mjs`):

- Prefer `#codez=` (LZ-string, same as lean4web).
- Fall back to `#url=` (GitHub raw) when inline encoding would exceed size limits.
- Sync fails if no encoding fits under 8000 chars; warns above 1800 chars (conservative share-link limit).

## Convention

- Filename: `{nodeId}-{slug}.lean` (e.g. `P01-basin-invariant.lean`, `P15-bundle-geometry.lean`).
- First line doc comment: one-sentence gloss shown on the site.
- Keep snippets short (<120 lines); prefer counterexamples and local proofs over headline certification theorems.

## Adding a playground

1. Add a self-contained `.lean` file in this directory.
2. Run `npm run sync` in `site/` (or `./serve-site.sh`).
3. The node page and graph tooltip pick up the live URL automatically.

No manual URL encoding — the build uses the same `LZString.compressToBase64` scheme as lean4web.
