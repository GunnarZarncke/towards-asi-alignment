# Edit-attribution outputs

Committed aggregates from `scripts/human_delta.py`. Raw interval rows and prompts stay in gitignored `telemetry/`.

- `YYYY-MM.csv` — monthly line counts (`--month YYYY-MM`)
- `bar-updates.jsonl` — each authorship-bar key change
- `span-ledger.json` — cumulative human/agent lines per `\begin{authbar}` span
- `author-provenance.jsonl` — spans where an agent committed the diff but the text is pre-existing author prose (e.g. LessWrong transfers marked `{GZ}`). Hook intervals may count those lines as `agent_lines`; the declared key and this log take precedence over naive derivation.
