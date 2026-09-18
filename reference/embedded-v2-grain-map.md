# Embedded V2 grain map

**Status:** canonical reference (2026-09-18). Plan: [`drafts/plans/embedded-v2.md`](../drafts/plans/embedded-v2.md). **Do not unify in Lean.** Use M1 now; M2 for prose silence checks; M3 only when a bridge rewrite needs ambient \(z\).

## One transition, three questions

All grains share one coupled transition \(T\) on socio-technical state. Each grain asks a different question of the **same** \(T\):

| Grain | State | Question of \(T\) | Repo home |
|-------|--------|-------------------|-----------|
| **Attractor** | \((Q,f,\theta,E)\) or \((x,\theta,e)\) | Does \(T\) retain / attract / resist invasion in a desirable region? | v1 claim 6 (C-007); MB6; *Alignment Under Selection*; *Constructing Alignment Attractors* |
| **Path** | \((G,A)\) | Is \(T\) a legal \(\mathcal{E}\)-edge from described \(G_0\) toward \(G^\star\)? | Family E; [`papers/path-construction/`](../papers/path-construction/); `PathRealizable` (open, not in v1 Lean) |
| **Ecology** | \(z=(x,h,k,\theta,e)\) | Which coordinates did \(T\) change, and does \(z\) stay in / return to \(D_{\mathrm{joint}}\)? | 2.0 intro claim; lifecycle Preserve property; constructibility (Family D) |

## Coordinate dictionary

| Coordinate | Attractor | Path | Ecology |
|------------|-----------|------|---------|
| \(x\) / \(A\) / \(Q\) | population or types | governed system \(A\) | AI systems and technical artifacts |
| \(\theta\) | selector | rules inside \(G\) | selection, certification, deployment rules |
| \(E\) / \(e\) | environment | — | remainder (technical, economic, institutional) |
| \(f\) | fitness / payoffs | — | induced by how \(h,\theta\) treat \(x\) and \(k\) |
| \(G\) | — | observe / refuse / redirect / authorize | recovered from \(h\) under \(\theta\) |
| \(h\) | — | — | researchers, labs, auditors, funders, regulators, operators |
| \(k\) | verifier channel (if typed) | — | knowledge, evals, specs, safety cases |

Identifications (use explicitly, do not bake into Lean):

- \(A\) is a distinguished component of \(x\); \(Q\) is a distribution over types of \(x\).
- \(G \subseteq h\) in general: funders and constructors without stop authority live in \(h\setminus G\).
- Attractor papers use \((x,\theta,e)\); construction papers use \((Q,f,\theta,E)\). Same job, different notation.

## Four objects (do not collapse)

| Object | Predicate on | Episode? | Must not become |
|--------|--------------|----------|-----------------|
| **\(P\)** (episode target) | artifact / \(x\) | frozen per construction–certification episode | \(D_{\mathrm{joint}}\) or the field prestige ontology |
| **Construction** | \(I\) changes \((Q,f,\theta,E)\) or \(z\) | named intervention | `ConstructionCrux` discharge by narrative |
| **Path** | \((G,A)\) under frozen \(\mathcal{E}\) | incremental steps | successor constraints on \(A\) alone |
| **\(D_{\mathrm{joint}}\)** (cycle property) | full \(z\) | property of repeated cycle | conjunct inside `ConstructionCrux` / frozen \(P\) |

Legitimate target revision: a separately specified process may produce \(P_{t+1}\). That is not ex post rationalization inside one episode.

## M1 — Job-indexed views (default)

When reading or writing a claim, tag which grain it uses:

```
Attractor claim  →  "under T, does (Q,θ,E) stay in D?"
Path claim       →  "under T, is this E-edge legal for (G,A)?"
Ecology claim    →  "under T, does z stay in D_joint?"
```

## M2 — Forgetful projections (silence checks)

Documentation only — not Lean types:

\[
\pi_{\mathrm{path}}(z)=(G(h,\theta),\,x),\qquad
\pi_{\mathrm{attr}}(z)=(\mathrm{pop}(x),\,f(\theta,e,k),\,\theta,\,e).
\]

Use to ask what a claim is **silent about**:

| Claim uses | Silent about (typical) |
|------------|-------------------------|
| Path \((G,A)\) | Funders in \(h\setminus G\); population mix \(Q\); whether \(k\) is captured |
| Attractor \((Q,f,\theta,E)\) | Who \(G\) is; whether refuse authority exists; episode target \(P\) |
| Ecology \(z\) | Nothing by default — but too heavy for most bridge antecedents |

There is **no inverse**: recovering \(z\) from \((G,A)\) or from \((Q,f,\theta,E)\) is the covering tuple we are not writing.

## M3 — Later ambient \(z\) (per-bridge only)

If a bridge rewrite needs context:

- \(P\) = predicate on distinguished artifact in \(x\), frozen per episode.
- \(D_{\mathrm{joint}}\) = predicate on \(z\).
- Path edges = \(T\) restricted to \(\mathcal{E}\)-legal \(\pi_{\mathrm{path}}\).
- Attractor dynamics = induced dynamics on \(\pi_{\mathrm{attr}}(z)\).

Lean order: **MB6** (`Environment` / joint \(z\)) then **MB11** (`SafeIn C A`). No five-field `AlignmentContext` record up front.

## Independence cells (keep explicit)

| Can hold | While failing |
|----------|----------------|
| Legal path step | Attractor (coup-free walk into wrong vacuum) |
| Attractor move | Path (illegal skip of \(G\)) |
| Capacity change in \(h\) | Both \(P\) and \(D_{\mathrm{joint}}\) |
| \(D_{\mathrm{joint}}\) | `PathRealizable` (good institutions, no legal first step) |
| `ConstructionCrux` for \(P\) | \(D_{\mathrm{joint}}\) (realizing \(A\), process cannot refuse) |
| Snapshot \(\varepsilon\)-cut at Identify | Named restorer still paying after \(T\) (physics / operator / institution / selected self-repair of \(A\)) |

## Cut persistence (not autopoiesis)

Identify, Construct, and Preserve all talk about a boundary. They are not the same object. \(A\) need not try to repair “its” cut; self-repair is selected or not.

| Object | Stage | Question |
|--------|-------|----------|
| Snapshot \(\varepsilon\)-cut | Identify | Is there a distinguishable, handle-backed partition *now*? |
| Named restorer | Construct (Family C) | After damage, *who pays* to keep that cut? Physics, operator stack, institution, or a policy selected to restore it. |
| Ecology repair of \(z\) | Preserve | Does the *cycle* stay in / converge back to \(D_{\mathrm{joint}}\) (live correction, independent eval, refuse)? That “converges back” is repair of \(z\), not of \(A\). |

Unsigned “the cut came back” is the same failure mode as unsigned basin. Fail if the restorer is only the operator stack (cut dies when ops stops paying) or only selected self-repair of \(A\) (can fight correction). Do not bake restorer into `AgentCandidate` / `BoundaryCondition`. MB1’s silently fixed context is who restores the recovered cut.

## Lifecycle ↔ grains

Cycle: specify → construct → identify → certify → act/refuse ↻

| Stage | Primary grain | Notes |
|-------|---------------|-------|
| Specify | Ecology + episode \(P\) | Target sort; legitimate \(P_{t+1}\) process separate |
| Construct | Ecology + attractor \(I\) | Which coordinates of \((Q,f,\theta,E)\) or \(z\) does \(I\) move? Named restorer of the construction cut (Family C) |
| Identify | Path + ecology | Snapshot cut of \(A\) and access; may force respecify. Silent about who pays after damage unless restorer is named |
| Certify | Ecology + bridges | MB7/MB10/MB11 cuts; green dashboard ≠ act |
| Act/Refuse | Path + ecology | Backtest Exp. 4; `DeploymentOk` neighborhood |
| Preserve | Ecology (\(D_{\mathrm{joint}}\)) | **Not a stage** — MB3/MB4/MB5/MB6 are cycle-property constraints. “Converges back” = ecology-grain repair of \(z\) |

## Related

- [`drafts/plans/embedded-v2.md`](../drafts/plans/embedded-v2.md) — decisions, roster types, phasing
- [`reference/field-agendas/data/lifecycle.yml`](field-agendas/data/lifecycle.yml) — cycle YAML
- [`papers/path-construction/`](../papers/path-construction/) — path grain briefing
