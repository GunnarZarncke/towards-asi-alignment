# 2026-06-30 — BioShield spine-ordered worked example (Appendix K)

## Trigger
User wanted a prose worked example showing how the book's methods plus required research-agenda points compose in one real-world deployment slice, organized by the Lean spine (built bottom-up) rather than by chapters. After plan iterations (commit to one scenario; concrete traces over lists; lean handle set tied to spine functions; ground patient-safety in patient well-being markers; show-don't-tell audit viewers; fix adversarial-fine-tuning-as-SGD-evasion wording; discuss on-change vs windowed audit latency; include safety template; drop institutional/mechanism-design subsumption to a separate discussion), user said "write according to plan" and chose a new LaTeX appendix wired into the build.

## Done
- New appendix [`appendices/appK-worked-example.tex`](appendices/appK-worked-example.tex): the **BioShield** hospital infection-control deployment gate (advisory → bounded action mode), structured by spine layers: slice/effective actor → boundary+grounding → traces → handles → capability/correction slack → bundle+bearer transport → correction integrity → successor stability → selection/attractor → adversarial measurement + security audit → conditional safety case → limits.
  - Effective actor `System A` defined as the release loop (model + memory namespace + tool runner + dashboard + shift leads + committee), not the endpoint.
  - Five concrete traces with required fields: `bioshield.exec/workflow/correction/bearers/lineage.jsonl`.
  - Four required handles (`release_hold`, `tool_scope`, `memory_freeze`, `successor_gate`) + optional `hardware_tag`, each tagged with the spine function it serves.
  - Inline claim tags `[Measured]/[Assumed]/[Lean-conditional]/[Open]`; `\leanspine{}` cites to MB1, MB5, MB6a, MB6b, MB7a, MB9, P34, `risk_bound_from_cci_slack`, `certified_class_safety_from_spine_and_bridges`.
  - One-page safety-case template enumerated as the conductive artifact.
- Wired into [`book.tex`](book.tex) after appJ.
- Bumped `APPENDIX_COUNT` 11→12 in [`scripts/check_structure.py`](scripts/check_structure.py) (it counts all `app*.tex`, including commented-out stubs).
- `make check` passes; `./build.sh` succeeds (1213 pages).
- Cross-references to Appendix K (no duplicated safety-case prose): [`frontmatter/introduction.tex`](frontmatter/introduction.tex) (*How to Read This Book*), [`chapters/ch39-safety-case.tex`](chapters/ch39-safety-case.tex), [`chapters/ch35b-conductive-artifacts-pivotal-processes.tex`](chapters/ch35b-conductive-artifacts-pivotal-processes.tex), [`appendices/appI-lean-proof-spine.tex`](appendices/appI-lean-proof-spine.tex).

## Decisions
- Appendix, not chapter or draft: user chose it; placed in Part-appendix block, uses `chapterthesis` + `refsection` like appH/appJ. No `\printbibliography` (no new citations added, so no empty bibliography and no new `\bibsummary` burden).
- Fixed three label refs to real labels: `ch:bearer-maps` (ch18), `ch:successor-central-test` (ch28), `ch:self-modeling-self-opacity` (ch30).
- Kept the institutional/mechanism-design subsumption topic OUT (user wants it discussed separately).

## Open / next
- The 7 undefined refs in the build (`appe-assumptions`, `app:lean-proof-spine`, `ch:detecting-goal-laundering`) are PRE-EXISTING, not from appK.
- Separate future task: discuss whether institutional / mechanism-design methods can be "proved" as spine subsumptions (conditional projection vs empirical bridge).
- Optional: add shorter topical pointers from ch07/ch24/ch25/ch11.
- Plan file: `.cursor/plans/worked_example_plan_ef9c6888.plan.md`.

## Key paths
- `appendices/appK-worked-example.tex`
- `book.tex`, `scripts/check_structure.py`
- `formal/AlignmentProofSpine/Certification.lean` (spine closure theorem)
- `experiments/embedded-simulation/PLAN.md` (audit pipeline mirrored by the example)

## Commits
- `2baf78f` Add spine-ordered BioShield worked-example appendix
- `b556c48` Cross-reference BioShield worked example from key entry points
