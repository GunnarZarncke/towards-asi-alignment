# Agent type signatures / selection theorems

- **Date:** 2021-09-28
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/posts/G2Lne2Fi7Qra5Lbuf/selection-theorems-a-program-for-understanding-agents
- **Source read:** full
- **TSA files consulted:** `reference/field-agendas/inter-agenda-term-glossary.md`; `appendices/appB-bridge-crosswalk.tex`
- **Keywords grepped:** selection theorem; type signature; coherence theorem; Good Regulator; selection environment; embedded agency; Wentworth; agent type

## Source ontology

Wentworth replaces the generic object “agent” with a **type signature**: representation (data structures for goals, world models, components), interfaces (inputs/outputs among components and environment), and embedding (how the abstract structure sits in the low-level implementation). A **selection theorem** then constrains which such signatures outer processes—natural selection, ML training, economic profitability—will produce in a broad environment class; existing examples include coherence/Dutch-book theorems, Good(er) Regulator, and Kelly-style results. “Goal” and “world model” cease to be free modeling choices and become predicted structure of inner agents.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** operational agent / ε-boundary discovery (ch07, MB1); selection environment / \(\mathrm{Fit}_E\) (ch34, MB6); Good Regulator as a control citation (ch03, ch07, ch32); field-glossary entries “selection theorems” and “agency as compression”; App. B NAH/shard sibling row (MB2/MB3), not this primitive.
- **Overlap:** Both refuse a stipulated Cartesian agent and care what outer pressure produces. TSA’s embedding question (where is the real optimizer?) overlaps the source’s embedding slot; Good Regulator is already a cited selection-theorem instance; the field glossary already names Wentworth’s program and separates it from \(\mathrm{Fit}_E\).
- **Gap:** Chapters never use “type signature” or “selection theorem.” TSA’s load-bearing “selection” is institutional deployment of *systems* (ch34), not theorems about internal representation/interface types. Boundary discovery measures a cut; it does not ask which data structures for goals or world models selection forces. App. B maps MB1 to MIRI embedded agency and MB6 to socio-technical selection—so the manuscript crosswalk still lacks this unit.

## Applicability to TSA

- **Score (0–5):** 3
- **Why:** The primitive is alignment-relevant (inner agents, value type, embedding) but is not a missing spine claim: TSA already chose measurable boundaries plus deployment handles over type-signature theorems. Absorbing it into ch34 would be a hostile-test rename. The remaining work is a reverse gap: App. B’s “Selection” cluster and the word “selection” in the six claims will be read as answering Wentworth when they do not. Cite the program next to MB1/inner-alignment, with an explicit non-identity to \(\mathrm{Fit}_E\).
- **Ontology-stickiness risk:** High. Pre-2021 models lack the three-part type-signature object. Post-TSA drafting will map “selection theorems” onto ch34/MB6 because of the homograph the glossary already flags. TSA includes a nearby rename, not the primitive.
- **Recommended action:** add-reverse-gap

## One-line finding

Wentworth’s type-signature/selection-theorem unit is adjacent to TSA boundary and selection vocabulary but is a distinct internal-structure question the manuscript still only distinguishes in the field glossary, not in App. B or the chapters.
