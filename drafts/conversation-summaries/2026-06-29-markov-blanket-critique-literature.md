# 2026-06-29 — Markov-blanket critique literature

## Trigger
User supplied feedback on the Pearl vs Friston blanket critique (Bruineberg et al.), technical FEP critique (Biehl, Pollock & Kanai), boundary-relativity (Btesh/Bramley/Lagnado), alignment-field echo (Demski AF), and Chris Pang's alternative boundary ontology. Asked to plan first, then apply all.

## Done
- **ch06:** Footnote on blanket critique literature (Pearl/Friston distinction, Biehl technical critique, modeler-supplied cut, Demski AF, MB1 framing, live Friston reformulation); expanded chapter references block.
- **ch07:** One sentence + footnote on operational partition vs observer-independent cut; cross-ref ch06; MB1 well-definedness presupposition.
- **appBridge:** MB1 paragraph extended with blanket-skepticism strand alongside embedded agency.
- **appH:** MB1 falsify item adds modeler-supplied / ill-defined cut.
- **Bibliography:** Fixed `biehl2020fepcritique` metadata (Biehl, Pollock & Kanai, Entropy 2021); added `btesh2022redressing`, `demski2023agentboundaries`, `friston2021fepresponse`; updated `bruineberg2021emperor` annote.
- **Ledgers:** A-004 failure mode (prior well-definedness); U-05 gloss split existence vs recovery hardness.
- **metadata/TODO.md:** Chris Pang alternative boundary ontology research item.
- **metadata/source-canon.md:** ch06 row + new bib crosswalk entries.
- **references/bibliography-summaries.tex:** Updated summaries for new/changed keys.
- **Build:** `./build.sh` succeeded.

## Decisions
- Primary home is **ch06 footnote** (construct introduction); ch07 stays procedural with one sentence + short footnote.
- Cited **Demski (2023) AF post** rather than attributing the argument to Wentworth (Wentworth commented on related threads; Demski's post explicitly cites Bruineberg).
- Did not touch ch45's unrelated Biehl cite (adversarial audit context).

## Open / next
- Chris Pang correlation-based boundary ontology (TODO only).
- Optional: regenerate Appendix E from `assumptions-ledger.md` if maintainer workflow requires it after A-004 failure-mode edit.
- source-canon ch06 method-comparison table still open (separate from this pass).

## Key paths
- `chapters/ch06-agent-without-anthropomorphism.tex` (footnote ~L167)
- `chapters/ch07-finding-boundary.tex` (~L199–200)
- `appendices/appB-bridge-crosswalk.tex` (MB1 notes)
- `references/manuscript-citations.bib`, `references/dynamical-systems.bib`

## Commits
- `d3dfc61` Wire Markov-blanket critique literature and calibrate MB1 prior risk.
