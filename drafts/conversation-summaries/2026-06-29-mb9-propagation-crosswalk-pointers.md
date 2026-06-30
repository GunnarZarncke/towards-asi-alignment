# 2026-06-29 — MB9 propagation, prominent crosswalk pointers, voice TODO

## Trigger
Follow-ups after the bridges-crosswalk and research-order sessions: (1) "Fix MB9 in the apps"; (2) "where do we point to this appendix prominently?"; (3) add a TODO to check narrative-voice consistency; plus two earlier TODO requests (appendix renumbering, hardcoded table ref).

## Done
- **MB9 propagated into the appendices** (was only in Lean + ledger + crosswalk):
  - appI: new `MB9: grounding certificate soundness` assumption block + equation (`appi:ass:mb9`/`appi:eq:mb9`), matching the `Core.lean` axiom; updated graph-legend and "Reading the Appendix" `MB1`--`MB8` → `MB1`--`MB9`.
  - appH: new Tier-0 `MB9` per-bridge research item (validate/falsify); intro range strings → `MB1`--`MB9`.
  - appE: range string → `MB1`--`MB9` (generated index already carries the MB9 row).
- **Prominent reader-facing pointers to the crosswalk** (previously only in repo/agent docs):
  - `frontmatter/preface.tex`: added to the Appendices roster (terse "bridge--field crosswalk") and to the load-bearing-assumptions sentence.
  - `frontmatter/executive-overview.tex`: extended the assumptions-collation sentence to point at the crosswalk and name the mapped field problems.
  - Shortened a redundancy in the preface per user feedback (roster entry now terse; description kept once).
- **TODOs added** to `metadata/TODO.md`: appendix renumbering / filename↔letter sync; hardcoded `tables/assumptions-table.tex` reference; MB9 propagation (now marked done); **narrative voice consistency** (pick one register — I / we / the book / dialogue / none — and apply book-wide).
- Build green throughout (`./build.sh` exit 0, no undefined refs/citations); `make check` passes (132 cited keys); MB9 labels resolve.

## Decisions
- Did **not** rename appendix files for the crosswalk insertion; followed repo precedent (filenames stable, letters drift, `\ref`-based). Renumbering captured as a TODO instead.
- Kept per-bridge appH/appI items in numeric order; priority is expressed via the new Tier section, not by physically reordering.
- Left `RELEASE_NOTES.md` (untracked, unrelated) out of the commit.

## Open / next
- Optional ch48/ch48/introduction cross-links to the crosswalk (offered, not done).
- Lean dependency-graph figures may not render an MB9 node; regenerate via `scripts/render_lean_graphs.sh` if desired.
- Execute the narrative-voice and appendix-renumbering TODOs.

## Key paths
- `appendices/appB-bridge-crosswalk.tex`, `appendices/appF-research-program.tex`, `appendices/appG-lean-proof-spine.tex`, `appendices/appL-assumptions.tex`
- `frontmatter/preface.tex`, `frontmatter/executive-overview.tex`, `metadata/TODO.md`

## Commits
- (this session — see commit below)
