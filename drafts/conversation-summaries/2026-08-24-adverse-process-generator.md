# 2026-08-24 — Adverse process generator

## Trigger
User: new 2021–2026 ontologies do not help much identifying cracks (too specific); maybe existing concepts need to be used more thoroughly. What generates all physically grounded processes that can harm humans despite countermeasures — including boring fire/explosion/pandemic/virus, especially coupled, and spore-like inert reconstitution across layers? Collect, combine, model, completeness/gaps, overall report.

## Done
- Draft folder `drafts/adverse-process-generator/`: README, catalog, hybrid generator, TSA coverage, REPORT, `formalizability.md`, `design-bounds.md`.
- Amendment: finite-word grammar missed continuous incremental change and under-specified iterated sporulation; both now first-class.
- Formalizability: schema completeness was the wrong target. Design-conditioned bounds (ch33 envelope): channel-cut + output-quarantine. Airgap including residual hardware coupling yields in-envelope A4↛A3; internet falsifies the hypothesis; exported constructors are outside the theorem.
- No manuscript, Lean, or site edits. No new spine terms.

## Decisions
- Generator is a **hybrid harm-path grammar** (flow \(F\) + jumps \(G\) + generation kernel \(T^{n}\)), not a new ontology of entity types. Finite words are only the discrete trace.
- Completeness claimed for hybrid executions (schema), not instance lists, not general reachability.
- TSA crack: inert intermediates, non-agent effectors, sub-threshold drift (ch46 covers value geometry only), generation kernels. ch05’s “bugs, viruses, ordinary technical failures out of scope except…” is the book-boundary that hides the causal pattern.
- ch36 “parasite” stays correction-host; biological/firmware spores are a reverse gap, not already covered.
- Formalizability: G1 schema almost tautological; G2 relative to a model; G3 never from the armchair. **Intended reading:** construction-conditioned theorems (airgap stack, freeze, type/iteration caps, typed sinks), not hop-list completeness. Channel-cut lemma vs output-quarantine lemma. Connecting internet is expanding \(\mathcal{E}\) without recertifying \(\mathfrak{E}\).
- Reverse-gap if manuscript moves: ch33 \(\mathcal{E},\mathcal{T}\) must include channel whitelist, residual physics, write sinks, type/iteration caps — not only “the model is boxed.”
- Thoroughness extensions (C=0 and \(T^{n}\); boundary includes drifting \(\Phi\); dead-man; wider parasite host; composition + trend audit) — not a tenth claim.
- Do not add “spore,” nine axes, or HybridHarm to the spine.

## Open / next
- v1 reverse-gap weaves shipped 2026-08-25 (`2026-08-25-harm-path-v1-weave.md`). Schema still drafts-only.
- Instance incompleteness (unknown triggers, published constructors) is not closable by ontology work.

## Key paths
- `drafts/adverse-process-generator/REPORT.md`
- `drafts/adverse-process-generator/generator.md`
- `drafts/adverse-process-generator/design-bounds.md`
- Prior thread: `drafts/ontology-reviews-2021-2026/_synthesis.md`, `_three-tests.md`

## Commits
- `94698b10` Add Construct 2.0 plan and adverse-process generator drafts.
