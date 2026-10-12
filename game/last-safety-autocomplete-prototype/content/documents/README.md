# Player-facing documents (sources)

Authoring sources for long-form lab documents the evaluator can receive through Lab Access (Files / Knowledge), usually after `access.request` or an NPC share.

**Do not edit served text in fixtures by hand.** Change the source here; the engine renders it with [lib/documents.mjs](../lib/documents.mjs) for the loaded pack. Spec: [spec/documents.md](../spec/documents.md).

## Files

| Slug | Document ID | Notes |
| --- | --- | --- |
| [sec-arch-04.md](sec-arch-04.md) | SEC-ARCH-04 | Security architecture; pack-conditional omissions |

## Authoring markers

HTML comments in the source are stripped or resolved at render time. They are not player-facing.

| Marker | Effect when served |
| --- | --- |
| Leading `<!-- Authoring … -->` block | Removed entirely |
| `<!-- include after-PACK --> … <!-- /include -->` | Body kept only if the loaded pack is **strictly later** than `PACK` in the pack ladder ([spec/documents.md](../spec/documents.md)) |
| `<!-- infer PACK[,…] --> … <!-- /infer -->` | Body always kept; tags removed. Optional player route; **not** a Lean knowledge edge |
| `<!-- exec-never: … -->` | Removed (authoring note only) |

Add new documents under this folder and register them in `lib/documents.mjs` (`DOCUMENTS`).
