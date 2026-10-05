# Claim extracts

Exploratory sidecars: one JSONL record per load-bearing (or load-checked) sentence of a chapter, with a light formal rendering and a link to Lean symbols. Pilot: `ch42.jsonl` (Ch. 42, sections Why This Matters, Plain-Language Model, Formal Model up to the layer table). Not manuscript canon.

**Check:** `python3 scripts/check_claim_extract.py` (quote must match the `.tex` lines; every `lean:` name must occur in `formal/`).
**Stop rule:** a failure means the record is stale or wrong. Fix or delete the record; never edit the chapter to fit it. If the chapter has changed enough that more than a handful of quotes fail, delete the extract and redo that chapter. A flag that no record needs any more is removed from the vocabulary.

## Record

| key | meaning |
|-----|---------|
| `id` | `chNN.NNN`, in reading order |
| `lines`, `sec`, `quote` | source span, section title, verbatim substring of those lines |
| `role` | thesis, premise, definition, scope-limit, layer, table-row, example, recap, rhetoric, ... |
| `load` | `bearing` (chapter's argument fails without it), `support`, `framing`, `none` |
| `rule` | argumentative form: implication, conjunction, universal, negated-claim, necessity, possibility, comparison-min, definition, empirical-report, citation, ... |
| `form` | one-line rendering; `->` implication, `and`/`or`/`not`, `forall`/`exists`, `possible(...)` |
| `strength` | `null` = stated flatly; else `{q: raw qualifier, num: null}` (numbers later) |
| `refs` | `lean:Name`, `label:key`, `cite:key`, `concept:slug`, `?:Name` (unresolved referent) |
| `lean.status` | `proved`, `definitional`, `assumed`, `consistent`, `partial`, `diverges`, `by-omission`, `unchecked`, `none` |
| `lean.sym` | Lean names the record rests on |
| `flags` | defect/observation tags (e.g. `PROSE-LEAN-DIVERGENCE`, `ROOT-VARIANTS`, `UNREPRESENTED-IN-LEAN`, `BRIDGE-NOT-CONSUMED`, `UNFORMALIZED-PREDICATE`, `ISOLATED-THEOREM`, `REDUNDANT`, `UNHEDGED`) |
| `note` | what was found; cites record ids, never counts |

`lean.status` values are the extractor's reading of `formal/`, not a Lean check. Anything marked `proved` should be confirmed with `#print axioms` before the book cites it.
