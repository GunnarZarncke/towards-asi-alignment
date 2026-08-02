# Field agenda reference

Agent-oriented crosswalk material for comparing alignment agendas and vocabulary. **Not** manuscript canon — integration with App E and bridge crosswalk prose is deferred.

| File / path | Role |
|-------------|------|
| [`data/`](data/) | **Source of truth** — structured YAML (agendas, matrix, evidence catalog, clustering) |
| [`data/agendas/*.yml`](data/agendas/) | One file per coherent agenda |
| [`data/matrix.yml`](data/matrix.yml) | Agenda × bridge matrix; cells are `{ type, ids[] }` lists (see [`MAINTAINER.md`](MAINTAINER.md)) |
| [`data/bridges.yml`](data/bridges.yml) | Field nouns + semantic crux wording per `MB*` (matrix headers + legend) |
| [`data/evidence.yml`](data/evidence.yml) | Sourced evidence catalog |
| [`data/clustering.yml`](data/clustering.yml) | AISafety.com map → agenda roll-ups |
| [`field-agenda-index.md`](field-agenda-index.md) | **Generated** agent index (run `sync:field-agendas`) |
| [`MAINTAINER.md`](MAINTAINER.md) | Agent-only matrix reading rules (not on public `/field/` page) |
| [`site/src/content/field/intro.md`](../../site/src/content/field/intro.md) | Public Field hub introduction |
| [`inter-agenda-term-glossary.md`](inter-agenda-term-glossary.md) | Alphabetical terms by source agenda |
| [`anthropic-acausal-taxonomy.md`](anthropic-acausal-taxonomy.md) | Four loads on *anthropic* / acausal |
| [`graphs/`](graphs/) | MB bridge dependency graph (field nouns; companion to matrix) |

**Companion site:** [towards-alignment.com/field/](https://towards-alignment.com/field/) — matrix, evidence catalog, agenda cards.

**Manuscript bridge map:** [`appendices/appB-bridge-crosswalk.tex`](../../appendices/appB-bridge-crosswalk.tex)

## Maintenance

1. Edit YAML under `data/` (add agenda file, evidence row, matrix cell, bridge noun/crux in `bridges.yml`, etc.).
2. Optionally refresh from the legacy markdown index: `node reference/field-agendas/scripts/extract-from-index.mjs` (one-way import).
3. Regenerate site cards and index markdown: `cd site && npm run sync:field-agendas`.
