# Player-facing documents (sources)

Authoring sources for lab documents the evaluator can receive through Lab Access (Files / Knowledge), after `access.request`, an NPC share, or a visit share.

**Do not edit served text in fixtures by hand.** Change the source here; the engine renders it with [lib/documents.mjs](../../lib/documents.mjs) for the loaded pack. Spec: [spec/documents.md](../../spec/documents.md). Access tree: [spec/access.md](../../spec/access.md).

## Files

| Slug | Document ID | Notes |
| --- | --- | --- |
| [sec-arch-04.md](sec-arch-04.md) | SEC-ARCH-11 | Security architecture; pack-conditional omissions (filename slug stays `sec-arch-04`) |
| [eval-shutdown-report.md](eval-shutdown-report.md) | EVAL-SD-47 | Thursday 18 November 2027, 16:02 report; exec checklist |
| [eval-shutdown-spec.md](eval-shutdown-spec.md) | EVAL-SPEC-08 | What the shutdown test covers |
| [job-284-log.md](job-284-log.md) | EXEC-284 | Queue excerpt (jobs 283–285) |
| [staffing-memo.md](staffing-memo.md) | HR-MATCH-28 | Matching / B-plot |
| [safety-case-excerpt.md](safety-case-excerpt.md) | SC-EVAL-22 | Certification surface |
| [pilot-results.md](pilot-results.md) | PILOT-14 | Permission-gated extract |
| [meeting-summary.md](meeting-summary.md) | MTG-REV-18 | Frame; LLM bullets |
| [wiki-glossary.md](wiki-glossary.md) | — | Knowledge; visit share |
| [wiki-shutdown-test.md](wiki-shutdown-test.md) | — | Knowledge |

No camera-archive document.

## Authoring markers

HTML comments in the source are stripped or resolved at render time. They are not player-facing.

| Marker | Effect when served |
| --- | --- |
| Leading `<!-- Authoring … -->` block | Removed entirely |
| `<!-- include after-PACK --> … <!-- /include -->` | Body kept only if the loaded pack is **strictly later** than `PACK` |
| `<!-- infer PACK[,…] --> … <!-- /infer -->` | Body always kept; tags removed. The pack list names which packs may use the sentence as a premise for a think mark. It does not hide the sentence |
| `<!-- llm-fill: name --> … <!-- /llm-fill -->` | Frame kept until the engine replaces from the event log |
| `<!-- exec-never: … -->` | Removed |

Add new documents under this folder and register them in `lib/documents.mjs` (`DOCUMENTS`) and `lib/access.mjs` (`ACCESS_TREE`).
