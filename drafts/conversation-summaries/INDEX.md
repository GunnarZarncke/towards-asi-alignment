# Conversation log index

**Start here:** [HANDOFF.md](HANDOFF.md) (aggregated themes and open work).

**Recent sessions** (15 newest in this folder). Older: [archive/](archive/README.md).

| Date | Topic | Log |
|------|-------|-----|
| 2026-10-08 | **Prediction background split** — Book `authbar` vs Metaculus `predictionbackground`; trimmed listing titles markets 1–18 except 14. | [2026-10-08-prediction-background-split.md](2026-10-08-prediction-background-split.md) |
| 2026-10-08 | **snapshot-0 TSA pin** — Pin `snapshotTag: snapshot-0` after claims-repo tag; update Appendix P, hub, cards, eval plan. | [2026-10-08-snapshot-0-tsa.md](2026-10-08-snapshot-0-tsa.md) |
| 2026-10-08 | **Predictions registry links** — Versioned claims-registry URLs from `registrySite`; card LaTeX link fixes; Market 14 readability; Markets 19–21 full-box until Phase 4. | [2026-10-08-predictions-registry-links.md](2026-10-08-predictions-registry-links.md) |
| 2026-10-07 | **Ward monitoring news** — Create a field-news card on Francis Rhys Ward’s 7 October 2026 survey of frontier-lab monitoring.... | [2026-10-07-ward-monitoring-news.md](2026-10-07-ward-monitoring-news.md) |
| 2026-10-07 | **v1.7.0 release notes** — User asked to prepare the release. | [2026-10-07-v1-7-0-release-notes.md](2026-10-07-v1-7-0-release-notes.md) |
| 2026-10-07 | **Registry split plan revised** — User: revise eval-registry-split.md and the open questions in the TSA repo. | [2026-10-07-registry-split-revision.md](2026-10-07-registry-split-revision.md) |
| 2026-10-07 | **Maintainer checklists + quiz CI fix** — User: build failed (`make check`, quiz bank); then asked for maintainer doc listing action→follow... | [2026-10-07-maintainer-checklists.md](2026-10-07-maintainer-checklists.md) |
| 2026-10-07 | **Field news summary trim** — Shorten the `summary` field on the last four field-news cards (they were too long for the listing). | [2026-10-07-field-news-summary-trim.md](2026-10-07-field-news-summary-trim.md) |
| 2026-10-07 | **Exercised-bars rule and registry decoupling note** — User (working in sibling repo `ai-safety-claims`): apply the rule that an attempt must exercise e... | [2026-10-07-exercised-bars-rule.md](2026-10-07-exercised-bars-rule.md) |
| 2026-10-07 | **Freeze and copy catalog contracts 2–18 (minus 1, 4, 14)** — User: if ready to freeze, freeze and copy contracts up to 18 (minus 1, 4, 14) and do the needed s... | [2026-10-07-catalog-contract-freeze.md](2026-10-07-catalog-contract-freeze.md) |
| 2026-10-07 | **Appendix P after the split** — User: the registry site is https://aintelope.github.io/ai-safety-claims/ ; do “Appendix P after t... | [2026-10-07-appendix-p-split.md](2026-10-07-appendix-p-split.md) |
| 2026-10-06 | **Python venv for agents** — Agents keep failing on PyYAML because they run bare `python3` instead of the repo `.venv/`. | [2026-10-06-python-venv-agents.md](2026-10-06-python-venv-agents.md) |
| 2026-10-06 | **Market 1 wording** — Clarify four technical phrases in Market 1 (null band, sham intervention, freeze fields, extra na... | [2026-10-06-market-1-wording.md](2026-10-06-market-1-wording.md) |
| 2026-10-06 | **Eval registry scaffold** — Review the eval-registry-split plan against Appendix P; adapt it ("when in doubt choose simplicit... | [2026-10-06-eval-registry-scaffold.md](2026-10-06-eval-registry-scaffold.md) |
| 2026-10-05 | **Safety-case site vocabulary** — Use “safety case” as the public noun on the site; keep the agreed adjectives; use “evidence the c... | [2026-10-05-safety-case-site-vocab.md](2026-10-05-safety-case-site-vocab.md) |
| 2026-10-05 | **Predictions hub panels polish** — Continue predictions hub work: merge external factors into related-forecast panels (Metaculus lin... | [2026-10-05-predictions-hub-panels-polish.md](2026-10-05-predictions-hub-panels-polish.md) |
| 2026-10-05 | **Predictions hub catalog label** — Move related forecasts below the catalog. Fold Metaculus 6509 into that list. Keep underspecifica... | [2026-10-05-predictions-hub-catalog-label.md](2026-10-05-predictions-hub-catalog-label.md) |
| 2026-10-05 | **Market short/long titles and panels** — Metaculus wants a short title and a long title. Hub markets should be panels that later show the ... | [2026-10-05-prediction-market-panels.md](2026-10-05-prediction-market-panels.md) |

## Archive by month

- **2026-10** (15): [2026-10-INDEX.md](archive/2026-10-INDEX.md)
- **2026-09** (101): [2026-09-INDEX.md](archive/2026-09-INDEX.md)
- **2026-08** (194): [2026-08-INDEX.md](archive/2026-08-INDEX.md)
- **2026-07** (264): [2026-07-INDEX.md](archive/2026-07-INDEX.md)
- **2026-06** (202): [2026-06-INDEX.md](archive/2026-06-INDEX.md)

## Maintenance

- Roll older logs: `python3 scripts/archive_conversation_summaries.py` (keeps 15 in root).
- Prune superseded logs: `python3 scripts/prune_superseded_conversation_logs.py --apply`.
- Rules: [README.md](README.md).

