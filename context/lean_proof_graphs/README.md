# Lean proof dependency graphs (book layout)

The full spine is in [`../lean_proof_dependency_graph.dot`](../lean_proof_dependency_graph.dot) (developer reference).

For the book, the spine is split into four sub-diagrams plus one overview:

| File | Content |
|------|---------|
| `01-boundary-measurement.dot` | Boundaries, BIQ ceiling, observation/handle limits, MB7a–b |
| `02-value-transport.dot` | Bundles, bearers, goal transport, laundering counterexamples |
| `03-correction-successors.dot` | Handle correction, CCI/risk, successors, MB7c, MB4–5, MB8 |
| `04-selection-limits.dot` | Selection, cooperation, audit aliasing, normative limits, MB6 |
| `00-overview.dot` | How the four spines compose into layered alignment and P30T |

Render all PNGs:

```bash
./scripts/render_lean_graphs.sh
```

Output: `figures/lean_proof/*.png` (included from Appendix I).
