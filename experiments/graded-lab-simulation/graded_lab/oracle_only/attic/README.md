# Attic: coordination heuristics (not UAD)

Moved here in GL-51 after the proper-UAD audit showed that Phase 7a's
`uad_passive` / mutual-AND `uad_intervention` path never computed the
Markov-blanket residual \(J(C)=\mathrm{I}(I_{t+1};E_{t+1}\mid S_t,A_t)\)
and could disagree with UAD on directed handoffs and timing-shifted
coupling.

| Module | Former path | What it actually does |
|--------|-------------|------------------------|
| `coordination_heuristic.py` | `uad_passive.py` | Communicate-pair / co-activity Jaccard / co-semantic-step union-find |
| `freeze_and_merge.py` | `uad_intervention.py` | Program-freeze compensation matrix + **mutual** threshold merge |

Do not use these as the ecology-BIQ unit source. See `DESIGN.md`
"Phase 7a UAD (GL-51 revision)" and FINDINGS GL-51.
