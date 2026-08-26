# Chapter formulation groundedness (E / G)

**Canonical home** for the 2026-08-25/26 48-chapter reader passes and the v1 preview-formula demotion. Conversation logs are not the source of truth.

**v1 plan status: closed** (2026-08-26). Scores below are a **pre-demotion snapshot**. Do not treat them as current chapter grades.

**Rerun:** TSA 2.0 / Part XI drafting — see [`drafts/plans/construct.md`](../drafts/plans/construct.md) (checklist item). After substantial 2.0 prose, run the **G** pass again (E is optional; it collapsed).

## Why two passes

**Pass 1 (E, establishedness)** mixed “is the diagnosis known?” with “is the book’s object known?” Every chapter’s diagnosis scored high; the apparatus scored low. Results collapsed to **E ∈ [4.20, 5.80]**, mean **4.93**. No chapter reached mixed-established (6.50+). That ranking is almost uninformative for *where to edit*.

**Pass 2 (G, formulation groundedness)** scores only the chapter’s **own bet**: how conservative, constrained, and integrated the formulation is. **G ∈ [4.10, 7.20]**, mean **5.86**. Low G was almost always **n-tuples and covering inventories in result-syntax**, not weak diagnoses.

## Process (how to rerun)

1. One **read-only** subagent per chapter (`generalPurpose`). Same model for all chapters (2026-08 used Grok 4.6 Medium). Do not edit the manuscript in that pass.
2. Shared rubric; return a fixed format (`E_SCORE` / `G_SCORE`, per-dimension scores, one-line bet, band).
3. Rank after all 48 return. Do not mix E and G in one number.
4. **Do not** raise G by inventing tighter early formalisms. If G is low because of a covering list, demote the list; keep the thesis in prose.

### E rubric (Pass 1 — diagnosis-contaminated)

\(E \in [0,10]\) = unweighted mean of D1–D5. Higher = more established.

| Dim | Question |
|-----|----------|
| D1 Diagnosis | Is the *problem* field-standard? |
| D2 Mechanism | Is the *apparatus* standard or novel? |
| D3 Evidence | Proofs / experiments / history vs assertion? Lean `MB*` = assumptions, not proofs. In-repo experiments are tentative. |
| D4 Export | Do conclusions stay at the grain of the support, or jump to ASI? |
| D5 Consensus | Would an informed outsider treat the *main claims* as already known? |

Bands: 8–10 established · 6.50–7.99 mixed-established · 5.00–6.49 mixed · 3.50–4.99 mixed-speculative · 0–3.49 speculative.

### G rubric (Pass 2 — use this for v2)

\(G \in [0,10]\) = unweighted mean of F1–F5. **Ignore diagnosis.** Higher = more conservative / constrained / integrated.

| Dim | High | Low |
|-----|------|-----|
| F1 Distance | Published method with a mapping | New recipe, inventory, or 1−δ metaphor |
| F2 Constraint | Identifiability, separation, or named failure shapes the claim | True-by-construction or unfalsifiable |
| F3 Integration | Same object later chapters actually use | Local tuple unused downstream |
| F4 Replaceability | Operationalization could be swapped without losing the thesis | Thesis *is* the named index |
| F5 Cover | No free \(\theta,\varepsilon\) covering list as a “result” | n-tuple / seven-property vector as ontology |

Suggested bands: 7.50+ conservative-application · 6.00–7.49 natural-operationalization · 4.50–5.99 mixed-assembly · below 4.50 novel-ontology.

## Decision rule (v1 and v2)

- Keep the **thesis** in ordinary language (and field-standard math: viability, set invariance, IRL identifiability, GSN).
- Do **not** give a covering list the syntax of a derived object before its home chapter exists.
- Numbered contrasts that teach (artifact vs deployment vs loop) are fine.
- Named \(n\)-tuples with free \(\varepsilon,\theta\) read as “this is the ontology.”
- Move a named vector only if a later chapter already owns it. Remove it if later chapters do not use it.
- Do not invent a tighter early formalism unless it is a **published method being mapped**.
- **Part I (ch01–ch05)** may `\eqref` only equations defined in Part I (`scripts/check_structure.py`). Later homes: `\ref{ch:…}` / `\ref{sec:…}` only, so the reading DAG stays a closed first pass.

## v1 actions (closed)

Demoted premature covering formulas; theses kept. Then stripped later-home `\eqref` from Part I.

| Chapter | What was demoted | What stayed |
|---------|------------------|-------------|
| ch02 | 6-tuple \(X_t\), \(\Pi\), MI/power/\(D_t\) displays | Three-object split; tool-picture list; replicator as illustration |
| ch03 | \(C_A\), \(Z_t\), duplicate pathway displays | Viability / basins / class \(\mathcal{C}\); grounding-viability eqs |
| ch04 | 5-tuple \(V_t\), \(\mathcal{S}_{\mathrm{human-correctable}}\) | \(U_H\) at `eq:human-value-update-ch04` |
| ch08 | \(\Xi\), transport-loss / continuity displays | Growth/split/merge math; seven-property *prose* pointing at ch31 |
| ch10 | Local \(\tau\) / self-control growth eqs | Prose; later home is ch32 |
| ch01, ch06, ch09, ch14 | Duplicate covering displays / later `\eqref` as appropriate | Chapter homes; Part I without later eq numbers |

Also: notation/`\symboldef` only at real homes; no later-home `\symbolref` in early chapters.

## Pass 2 G ranking (snapshot, pre-demotion)

Natural-operationalization (22) · mixed-assembly (25) · novel-ontology (1: ch04).

| G | Ch | Band | Bet (one line) |
|---|----|------|----------------|
| 7.20 | 17 | natural-op | IRL/IB readout vs representation split; identifiability shapes the claim |
| 7.00 | 27 | natural-op | CCI certificate only if hard under degraded correction; Lean separations |
| 6.80 | 7 | natural-op | ε-directed blanket recovery plus identifiability limits |
| 6.60 | 45 | natural-op | Preserve the correction envelope as authorship of value change |
| 6.40 | 20 | natural-op | Jacobian/probe tests of bundle geometry under Goodhart |
| 6.40 | 22 | natural-op | MDL intention test vs mechanistic baseline |
| 6.40 | 25 | natural-op | CCI as a live causal channel |
| 6.40 | 33 | natural-op | Restricted-class certification envelope, not a construction recipe |
| 6.40 | 42 | natural-op | GSN: unsupported leaf fails the root |
| 6.30 | 34 | natural-op | Selection must raise fitness for Π-satisfying systems |
| 6.20 | 9 | natural-op | Composite via blankets, control reach, compression surplus |
| 6.20 | 23 | natural-op | MDL transport: goal survived iff transport model compresses better |
| 6.20 | 26 | natural-op | ValidRef CCI vector; captured reference invalidates the score |
| 6.20 | 29 | natural-op | Evaluator-shaping as mediation bypass |
| 6.20 | 39 | natural-op | Eval must be interventional and adversarial |
| 6.20 | 44 | natural-op | Lethality checklists mapped onto book structures; residue open |
| 6.10 | 36 | natural-op | Correction fails by colonization; audit causal force |
| 6.10 | 43 | natural-op | Fake-cost must outrun surplus |
| 6.00 | 1 | natural-op | COS located by interface, memory, compression |
| 6.00 | 21 | natural-op | Infer \((B,W,\Phi)\) and conserve \(G_B\) rather than a scalar |
| 6.00 | 38 | natural-op | High-conductivity artifacts at deployment gates |
| 6.00 | 48 | natural-op | Layered preservation-and-certification, not one mechanism |
| 5.80 | 10, 30, 35, 37 | mixed-assembly | (opacity / successor closure / coupling / conductivity) |
| 5.70 | 15 | mixed-assembly | Values as compressed control signals |
| 5.60 | 5, 6, 11–14, 16, 18, 24, 28, 31, 32, 41, 47 | mixed-assembly | Named book objects at their homes, still free \(\theta\) / inventories |
| 5.50 | 40, 46 | mixed-assembly | GLI; \(D_V\) product region |
| 5.20 | 19 | mixed-assembly | \(G_B=(J,H,\mathcal{C},\Phi)\) |
| 4.90 | 8 | mixed-assembly | Seven-property \(\Xi\) (preview; later demoted) |
| 4.80 | 2 | mixed-assembly | Civilizational 6-tuple (later demoted) |
| 4.60 | 3 | mixed-assembly | Eight-invariant / \(Z_t\) bundle (later demoted) |
| 4.10 | 4 | novel-ontology | Process-tuple \(V_t\) (later demoted) |

**E vs G flip (why G is the rerun target):** ch07 rose 4.40 → 6.80 (published blanket recovery). ch02 fell 5.80 → 4.80 (standard diagnosis, ad-hoc 6-tuple). ch04 was lowest G (4.10) despite mid E.

Pass 1 E extremes (for archive): highest ch02 5.80, ch09 5.60; lowest ch21 4.20. Full E table lived in the scoring chat; pattern only: D1 high everywhere, D2/D3 pull E down.

## Related

- [`INSTRUCTIONS.md`](../INSTRUCTIONS.md) §11 — covering lists vs later homes
- [`REVIEWING_FOR_AGENTS.md`](../REVIEWING_FOR_AGENTS.md) — anti-pattern
- [`metadata/concept-graph/README.md`](../metadata/concept-graph/README.md) — Part I `\eqref` contract
- [`drafts/conversation-summaries/2026-08-26-early-chapter-demotion.md`](../drafts/conversation-summaries/2026-08-26-early-chapter-demotion.md) — session chronology (may be archived)
