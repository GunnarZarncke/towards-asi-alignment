# 2026-09-25 — Field news memes

## Trigger
User asked for meme suggestions for the five newest field-news cards, then a minimal automated workflow (find template, detect text boxes, paste captions), integration into posts, and end-of-session commits split between workflow and images.

## Done
- Added `scripts/meme_workflow/meme_workflow.py` + `memes.json` (imgflip catalog match, layout heuristics, Pillow render).
- Cached blank templates under `scripts/meme_workflow/templates/`.
- Added `site/scripts/sync-field-news-memes.mjs` and wired `sync:field-news-memes` into `site/package.json` sync chain.
- Embedded `<figure class="book-figure book-figure--meme">` in five `metadata/field-news/bodies/*.md` files; ran `sync-field-news`.
- Copied five rendered memes to `site/public/field-news/memes/` (math uses user-edited PNG).

## Decisions
- Meme figures sit after each card’s “If you remember one thing” line.
- Images committed separately from workflow code so art regen does not churn script diffs.

## Open / next
- Tune layout boxes in `meme_workflow.py` if auto-render quality is insufficient; math meme is hand-edited PNG.
- Optional: show meme thumbnails on `/news/` index (not requested).

## Key paths
- `scripts/meme_workflow/meme_workflow.py`
- `scripts/meme_workflow/memes.json`
- `site/scripts/sync-field-news-memes.mjs`
- `site/public/field-news/memes/`

## Commits
- (pending) workflow commit
- (pending) meme images commit
