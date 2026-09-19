# 2026-09-10 — Containment verification news card

## Trigger
User attended Orpheus Lummis’s GSAI sequence with Royce Moon on Moon & Varshney (arXiv:2605.09045) and asked for a field-news card using the call takeaway: a whitelist/filter proof is progress; world-state and sequence constraints are the interesting next spec; unbounded real-world reach means no remaining guarantee.

## Done
- Field-news YAML entry `field-news-containment-verification-sep-2026` (`kind: research`, 2026-09-10).
- Body at `metadata/field-news/bodies/containment-verification-sep-2026.md` (paper quotes + Ch. 1 / 33 / 43 quotes; first-person call note; Bend / Taelin closed-world contrast).
- `cd site && npm run sync:field-news && npm run build:feed`.
- News index 404: `/news/` linked to legacy `/cards/field-news-…/` (dev catch-all 404s). Pass type `news`/`release`; infer `field-news-*` as news in `card-urls.mjs`.

## Decisions
- Frame as container-level lemma on a declared action alphabet, not a rival to alignment.
- Published PocketFlow examples treated as verified whitelisting; world-state Π as the GSAI-shaped residual.
- No manuscript or evidence.yml edits (ev-141 already indexes the paper).

## Open / next
- Optional: quiz takeaway for `/news/`; App B one-liner if the paper should appear in the GSAI/Safeguarded notes, not only the agenda card.

## Key paths
- `metadata/field-news.yml`
- `metadata/field-news/bodies/containment-verification-sep-2026.md`
- `/cards/news/field-news-containment-verification-sep-2026/`
