# 2026-06-18 — Session end: Part III complete, ch11 draft

## Trigger
User ended session after chapter 11 draft integration.

## Done this session (cumulative)

### Part III — all four chapters drafted
| Ch | File | Title | Lines |
|----|------|-------|-------|
| 11 | `ch11-capability-without-task-ontology.tex` | Measuring Capability Without Task Ontology | ~1,087 |
| 12 | `ch12-boundary-expansion.tex` | Capability Growth Is Boundary Expansion | ~1,242 |
| 13 | `ch13-coordination-bottleneck.tex` | The Coordination Bottleneck | ~1,049 |
| 14 | `ch14-intelligence-deepens-misalignment.tex` | When Intelligence Deepens Misalignment | ~999 |

### Structural fixes
- ch12/ch13 content moved to correct files per `INSTRUCTIONS.md` (was integrated into wrong filenames).
- ch14: added `Why This Matters`, `What Would Change This View`, `Summary` per §10.
- ch11: integrated user draft; `What Would Change This View`, 6-bullet summary, bridges ch10→ch11→ch12.

### Source map & citations
- `metadata/source-canon.md` — deep-research report chapter mapping.
- `references/*.bib` — 16+ new entries; surgical cites in ch03–ch12, ch40; `TODO(deep-research)` in stubs.
- `context/towards-asi-alignment-deep-research-report.md` — untracked.

### Metadata
- `metadata/book.yml`, `tables/chapter-map.tex` — ch11–ch14 status `draft`.

### Build
- `./build.sh` succeeds (405 pages).
- Pre-existing duplicate labels: `sec:self-modeling-transparency`, `sec:example-helpful-assistant`.
- Fixed ch11 `sec:example-firm` → `sec:example-firm-capability`.

## Decisions
- Part III uses Shape B (native narrative) for integrated drafts; required §10 elements added where missing.
- ch11 uses `B_X` and horizon `h` notation; consistent with ch12 downstream.
- No git commit (user did not request).

## Open / next
1. **Part IV** — draft ch15+ (values as compressed control signals).
2. **Duplicate labels** — resolve `sec:self-modeling-transparency`, `sec:example-helpful-assistant`.
3. **WWCTV** — ch12/ch13 lack explicit sections if full §10 parity desired.
4. **Commit** — large unstaged tree; suggest scoped commit: Part III chapters + bib + metadata + logs; exclude LaTeX aux/pdf.

## Key paths
- `chapters/ch11-capability-without-task-ontology.tex`
- `chapters/ch12-boundary-expansion.tex`
- `chapters/ch13-coordination-bottleneck.tex`
- `chapters/ch14-intelligence-deepens-misalignment.tex`
- `metadata/book.yml`, `metadata/source-canon.md`
- `drafts/conversation-summaries/INDEX.md`

## Commits
- (none)
