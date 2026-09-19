# Embedded V2 — coupled construction, field dynamics, and bridge cuts

Status: **decisions locked** (2026-09-18). Source memo: [`../../v2/Proposed V2 Extensions_ Embedded Construction, Field Dynamics, and Bridge Cuts.md`](../../v2/Proposed%20V2%20Extensions_%20Embedded%20Construction,%20Field%20Dynamics,%20and%20Bridge%20Cuts.md). Lane checklists: [`construct.md`](construct.md), [`field.md`](../field/field.md), [`spine.md`](../spine/spine.md). **Not** a v1 intro-claim change. **Not** a Lean covering tuple.

## Goal

Treat the memo as a *closure* of objects V2 already has. The 2.0 reader-facing claim (not v1):

> Alignment is a stability — or convergence — property of a coupled socio-technical construction and correction cycle, not only a property of a system at a time. Bridges are interface cuts through that cycle: each one holds only for some class of contexts it currently leaves implicit.

This is an **additional 2.0 intro claim**. It does not become a seventh v1 thesis claim and does not rewrite [`six-thesis-claims`](../../metadata/concepts/bodies/six-thesis-claims.md). v1 claim 6 (basin / selection, C-007) stays the *system-population* attractor. The 2.0 claim is the *process* remaining valid as constructors, evaluators, and selectors are endogenous.

## Locked decisions (2026-09-18)

| Q | Decision |
|---|---------|
| **Q1** | Additional **2.0** intro claim is OK. Not v1. |
| **Q2** | Keep frozen episode-target \(P\) **separate** from joint region \(D_{\mathrm{joint}}\). |
| **Q3** | Lifecycle is a **cycle**. Preserve is a **property** of repeating the cycle (stability or convergence), not a fifth equal stage. |
| **Q4** | Coverage **matrix stays evidential**. Construction / convergence gets a **separate presentation** (lifecycle cycle + preserve property; not `actsOnContextOf` cells). |
| **Q5** | A research-ecology paper may be spun out. **Manuscript prose and Lean must carry the attractor**; the paper is not the only home. |
| **Q6 / Q8** | Do not unify grains in Lean. Map them (below). Path \((G,A)\) and ecology \(z\) are different jobs. |
| **Q7** | Capacity vs structural is an explicit roster field. |

## What already exists (do not re-derive)

| Object | Where | What the memo adds |
|--------|--------|--------------------|
| Endogenous selector; joint \((x,\theta,e)\) | *Alignment Under Selection* | Institutional capture and human correction-channel integrity were **deliberately out of scope** there — 2.0 / manuscript must now carry that remainder, paper optional |
| Selector as state, not external field | *Constructing Alignment Attractors* | Research/deployment ecology as another coupled basin |
| Construction vs constructibility; \(I\) changes \((Q,f,\theta,E)\) | [`construct.md`](construct.md) Families A–D | Institutional \(I\) already in scope; constructor ecology sketched |
| Joint controller–system state \((G,A)\); legal path \(\mathcal{E}\) | Family E; [`papers/path-construction/`](../../papers/path-construction/) | Different grain from \(z\); do not collapse |
| Fail/refuse as method success; Backtest Exp. 4 | Family C | **Act/Refuse** is this object, now a cycle stage |
| `Environment`; `P35_basin_stability_induction` | `Core.lean`, `Certification.lean` | Unary `System` predicates still hide context; Preserve-as-loop is already Lean’s meaning |
| v1 claim 6 basin / selection | C-007; attractor-control card | 2.0 claim generalizes from population basin to cycle-on-\(z\) |

## Four objects (keep separate)

| Object | Question | Must not become |
|--------|----------|-----------------|
| Frozen **\(P\)** (episode target) | Given this \(P_t\), can we build / certify \(A\) that realizes it? | The field’s prestige ontology |
| **Construction** | Named \(I\) changes \((Q,f,\theta,E)\) (or \(z\)) toward realizing \(P_t\) | A catalog of builders |
| **Path** \((G,A)\) | Legal \(\mathcal{E}\)-steps from described \(G_0\) | Successor constraints on \(A\) alone |
| **\(D_{\mathrm{joint}}\)** (cycle property) | Does repeated Specify→…→Act stay in / converge to a region that includes live correction, independent evaluation, and refuse authority? | A conjunct of \(P\) inside `ConstructionCrux` |

Episode-freeze: \(P_t\) is frozen inside a construction–certification episode. A separately specified legitimate process may produce \(P_{t+1}\). \(D_{\mathrm{joint}}\) is not re-frozen that way: it is the invariant (or basin) of the loop.

## Mapping the three grains

**Canonical map:** [`reference/embedded-v2-grain-map.md`](../../reference/embedded-v2-grain-map.md) (M1 default; M2 silence checks; M3 per-bridge later). Do not collapse these into one `AlignmentContext` covering tuple.

| Grain | State | Job |
|-------|--------|-----|
| **Attractor** | \((Q,f,\theta,E)\) or \((x,\theta,e)\) | Population / selector / environment basin (v1 C-007; MB6) |
| **Path** | \((G,A)\) | Incremental legal steps from a described present controller (Family E) |
| **Ecology** | \(z=(x,h,k,\theta,e)\) | Constructors, evaluators, artifacts, rules — whether the *process* stays in \(D_{\mathrm{joint}}\) |

### Coordinate dictionary

| Coordinate | Attractor | Path | Ecology |
|------------|-----------|------|---------|
| \(x\) / \(A\) / \(Q\) | population or types | the governed system \(A\) | AI systems and technical artifacts |
| \(\theta\) | selector | part of \(G\)’s rules | selection, certification, deployment rules |
| \(E\) / \(e\) | environment | — | remainder (technical, economic, institutional) |
| \(f\) | fitness / payoffs | — | induced by how \(h,\theta\) treat \(x\) and \(k\) |
| \(G\) | — | who holds observe / refuse / redirect / authorize | recovered from \(h\) under \(\theta\) |
| \(h\) | — | — | researchers, labs, auditors, funders, regulators, operators |
| \(k\) | observational / verifier channel, if present | — | knowledge, evals, specs, safety cases |

\(A\) is a point (or distinguished component) of \(x\); \(Q\) is a distribution over types of \(x\). \(G\) is not all of \(h\): funders and constructors without stop authority sit in \(h\setminus G\).

### M1 — Job-indexed views (use this now)

One coupled transition \(T\). Each grain asks a different question of the **same** \(T\):

- Attractor: does \(T\) retain / attract / resist invasion in a region of \((Q,\theta,E)\)?
- Path: is \(T\) a legal \(\mathcal{E}\)-edge on \((G,A)\)?
- Ecology: which of \((x,h,k,\theta,e)\) did \(T\) change, and does \(z\) stay in or return toward \(D_{\mathrm{joint}}\)?

Independence cells (keep):

| Can hold | while failing |
|----------|----------------|
| Legal path step | Attractor (coup-free walk into a wrong vacuum) |
| Attractor move | Path (geometry improved by an illegal skip of \(G\)) |
| Capacity change in \(h\) | Both \(P\) and \(D_{\mathrm{joint}}\) (more people, same capture) |
| \(D_{\mathrm{joint}}\) | `PathRealizable` (good institutions, no legal first step toward \(G^\star\)) |
| `ConstructionCrux` for this \(P\) | \(D_{\mathrm{joint}}\) (a realizing \(A\) whose surrounding process cannot refuse) |
| Snapshot \(\varepsilon\)-cut at Identify | Named restorer still paying after \(T\) (physics / operator / institution / selected self-repair of \(A\)) |

### M2 — Forgetful projections (documentation, not Lean)

\[
\pi_{\mathrm{path}}(z)=(G(h,\theta),\,x),\qquad
\pi_{\mathrm{attr}}(z)=(\mathrm{pop}(x),\,f(\theta,e,k),\,\theta,\,e).
\]

Both maps lose information. \(k\) is collapsed into \(f\) or dropped. \(h\setminus G\) vanishes from the path. A single \(A\) does not recover \(Q\). There is **no inverse**: reconstructing \(z\) from \((G,A)\) or from \((Q,f,\theta,E)\) is exactly the covering tuple we are not writing. Use these maps in prose to say “this path claim is silent about funders” or “this basin claim is silent about who \(G\) is.”

### M3 — Optional later ambient \(z\) (prose first; Lean only per bridge)

Take ecology as the ambient state. Then:

- \(P\) is a predicate on \(x\) (or a distinguished artifact), frozen per episode.
- \(D_{\mathrm{joint}}\) is a predicate on \(z\).
- Path edges are the subset of \(T\) that also satisfy \(\mathcal{E}\) on \(\pi_{\mathrm{path}}(z)\).
- Attractor dynamics are the induced dynamics on \(\pi_{\mathrm{attr}}(z)\).

Lean order if authorized: **MB6** relative to `Environment`, then joint \(z\); **MB11** as `SafeIn C A`. Recover roles from \(h\) and \(\theta\) when a bridge needs them (equality when one lab builds, evaluates, and deploys). Do not add a five-field `AlignmentContext` record up front.

**v1 certificate layer** (Predictions P0c): extra indices live on *certificates* that collapse onto today’s unary predicates. That is not this M3 rewrite. 2027 markets §16 and §18 may *talk about* selection environment and declared deployment setting in surrounding prose; do not freeze restorer / path-legality / \(D_{\mathrm{joint}}\) as 2027 boxes.

## Lifecycle (reader surface)

Cycle stages:

\[
\text{Specify}\to\text{Construct}\to\text{Identify}\to\text{Certify}\to\text{Act/Refuse}
\]

with feedback from every downstream stage to earlier ones (certify can reconstruct; identify can respecify; act can change the measurement regime).

**Preserve** is not a stage. It is the property that repeating the cycle stays in \(D_{\mathrm{joint}}\), or converges back to it. Bridges previously tagged `preserve` (MB3, MB4, MB5, MB6) are **cycle-property** constraints: they must hold of the transition, not of a fifth box. “Converges back” is ecology-grain repair of \(z\), not autopoiesis of \(A\). Snapshot cut, named restorer, and that cycle property are distinct — [`embedded-v2-grain-map.md`](../../reference/embedded-v2-grain-map.md) (cut persistence).

**Act/Refuse** is Backtest Exp. 4 / Family C fail-refuse / Lean `DeploymentOk` neighborhood — certification that does not change a decision does not close the loop.

Source: [`lifecycle.yml`](../../reference/field-agendas/data/lifecycle.yml). Coverage matrix unchanged.

## Field construction types (roster)

`fieldConstruction` on [`roster.yml`](../../reference/field-agendas/data/roster.yml): `none` | `capacity` | `structural` | `mixed`. Missing means `none`.

| Value | Meaning | Matrix |
|-------|---------|--------|
| **none** | Technical / evidential agenda. Not a field-construction org. | May fill cells (`evidenceFor`) |
| **capacity** | People, courses, prestige pipeline. Upstream of bridges. | No green cell because headcount rose |
| **structural** | Changes independence, stop authority, irrevocable access, selection/deployment rules, or role separation. Acts on context of MB4a/MB6/MB7/MB10/MB11. | Not evidence those bridges discharge |
| **mixed** | Evidential and/or capacity work **plus** structural instruments | Matrix cells stay evidential; structural half is the type tag |

First cut (author-editable `because` lines on the roster):

- **capacity:** BlueDot, MATS, Apart, Kairos, CAIS, Iliad
- **structural:** Pause / standards cluster (success = changing who can deploy)
- **mixed:** GovAI / UK AISI (papers/evals in-matrix; institutes meant to bind \(\theta\)); MAI + CIP (institutional specify/construct)
- **none:** remaining research orgs, labs, eval suites, this project, CIRIS (CIRIS is *technical* construction, not field construction)

A structural tag is not a showing that stop authority actually fires.

## Presentation (not the matrix)

Leave [`matrix.yml`](../../reference/field-agendas/data/matrix.yml) as the evidential catalog.

New / updated surfaces for construction and convergence:

1. Field-hub **lifecycle cycle** + Preserve as property (this pass).
2. Specify/construct instance cards (already).
3. Roster **fieldConstruction** on agenda cards (this pass).
4. Later: a construction/convergence panel that lists structural orgs and \(D_{\mathrm{joint}}\) conditions — still not matrix paint.

## Attractor: manuscript carries it; paper optional

*Alignment Under Selection* excluded institutional capture and correction-channel integrity. 2.0 must state that remainder in **chapter prose** (ch34–ch38 neighborhood and Part XI) and in **Lean** (MB6 context-relative, then joint \(z\) if needed). A spin-out paper on the research-ecology basin is allowed as a briefing; it does not replace those homes.

## Phasing

| Phase | Work | Gate |
|-------|------|------|
| **Now** | Decisions in this file; lifecycle cycle on the field hub; roster types; grain map | none |
| **P1** | 2.0 claim wording in construct plan / Part XI outline only; reverse-column note uses roster types | not v1 intro |
| **Lean 2.0** | MB6 then MB11 context-relative; no covering tuple; no new axiom to `Safe` | author; still no `Safe` bypass |
| **Certificate layer (v1)** | Per-system certs onto unary predicates — **not** Lean 2.0 | [`../predictions/prediction-interface.md`](../predictions/prediction-interface.md) |
| **Paper** | Optional research-ecology spin-out **after** manuscript/Lean homes are named | construct |
| **Family B chapters** | still Backtest Exp. 4 | unchanged |

## Related

- [`construct.md`](construct.md) · [`field.md`](field.md) · [`spine.md`](spine.md)
- [`papers/alignment-under-selection/`](../../papers/alignment-under-selection/)
- [`papers/constructing-alignment-attractors/`](../../papers/constructing-alignment-attractors/)
- [`papers/path-construction/`](../../papers/path-construction/)
- Sessions: `2026-09-16-embedded-v2-extensions.md`, `2026-09-18-embedded-v2-decisions.md`
