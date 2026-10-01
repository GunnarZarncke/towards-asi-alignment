# 2026-09-29 — App P chapter–bridge connections

kind: feedback
uptake: local

## Trigger
User: Appendix P should not only reference a chapter but also the related bridge and explain the connection.
Prompts: `d6ebff1d-bcce-4797-8105-394491e32a55`

## Done
- content: Catalog table in `appendices/appP-bridge-predictions.tex` now names the chapter and the bridge, with a one-clause connection, for markets 1–18.
- content: Each market opening states what the contract tests about that bridge (MB1–MB7d, MB9, MB10, MB6a/MB6b). Markets 14, 15, 17, and 18 are marked as beside the spine (constructibility, composition, admission, scoped harm), not as new live axioms.
- content: Gunnar adjusted prose in the same file as part of a larger uncommitted edit batch (same pass as LW chapter imports, Market~21 wrapper, math-misalignment field news, and related site/YAML).

## Decisions
- Bridge keys follow `metadata/predictions.yml` `primaryBridge`, worded from Appendix B.
- A YES stays a public artifact by the deadline. The bridge stays an assumption about a later deployment.

## Open / next
- Phase 4 pilot/listing of Markets 19–20 remains gated on funding or an external evaluator.
- Commit when the larger edit batch is ready; nothing committed this session.

## Key paths
- `appendices/appP-bridge-predictions.tex`
- `metadata/predictions.yml`
- `appendices/appB-bridge-crosswalk.tex`

## Commits
- none (end of session; user requested no commit)
