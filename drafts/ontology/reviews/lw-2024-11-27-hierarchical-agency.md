# Hierarchical agency

- **Date:** 2024-11-27
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/posts/xud7Mti9jS4tbWqQE/hierarchical-agency-a-missing-piece-in-ai-alignment
- **Source read:** full
- **TSA files consulted:** `chapters/ch09-composite-agent.tex`; `chapters/ch41-multiscale-decomposition.tex`
- **Keywords grepped:** hierarchical; nested agent; composite agent; multi-scale; superagent; boundary discovery; Kulveit; vertical game

## Source ontology

Kulveit (ACS) treats **agents as nested same-type objects**: a superagent composed of subagents, both layers usefully modeled under the intentional stance (Dennett). The primitive is the **vertical relation** (conflict, exploitation, loyalty, “kindness”) between layers, not horizontal game theory among peers. He wants a scale-free formalism whose objects stay type `agent` at every level—unlike social-choice aggregations that turn agents into a contract, or mechanism design that turns them into a mechanism. Alignment holes named: AIs as sub- or superagents inside institutions; internal multi-objective “parts” interacting; value systematization / self-unalignment as inter-level dynamics.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** composite agent / intentional-compression surplus (ch09); multi-scale decomposition and nested/overlapping control loci (ch41); ε-boundary discovery (ch07, MB1). Field material cites Kulveit only via gradual disempowerment, not hierarchical agency. App. B has no ACS / vertical-agency row.
- **Overlap:** Both refuse a privileged individual-agent scale. Ch09’s composite tests (boundary closure, control reach, \(\Delta L_C\), surplus \(\Sigma(C)\)) and ch41’s posterior over decompositions already treat firms, markets, and model–tool–user loops as candidate agents. Intentional compression is TSA’s operational cousin of the intentional stance.
- **Gap:** Ch09’s load-bearing cut is the opposite pole: *an agent can be distributed across components that are not individually agents*. Kulveit’s desideratum is same-type nesting plus vertical intentionality (superagent gaining agency at subagents’ expense; meta-values like kindness between layers). TSA can locate nested control loci; it does not give a vertical game theory or keep “agent” as the type of every layer.

## Applicability to TSA

- **Score (0–5):** 3
- **Why:** Alignment-relevant and adjacent to Claim 1 (boundary / real optimizer), but absorbing it into ch09 would fail the hostile test: TSA’s composite is a measurement of *which cluster is agentic*, including non-agent parts. The remaining work is a reverse gap: “composite” / “multi-scale” will be read as already answering ACS when they do not name same-type vertical relations. Cite next to MB1 / ch09–ch41; do not replace the parts-need-not-be-agents cut.
- **Ontology-stickiness risk:** High for pre-2024 models (game theory’s flat player set). Post-TSA drafting will map “hierarchical agency” onto ch09/ch41 because of the nested-optimizer homograph. TSA includes the nearby scale-fluid rename, not the same-type vertical primitive. Field agendas currently route “Kulveit” to gradual disempowerment, which increases the miss.
- **Recommended action:** add-reverse-gap

## One-line finding

Kulveit’s same-type nested agents and vertical superagent–subagent relations are adjacent to TSA composite/multi-scale boundary work but remain a distinct formalism demand the manuscript and App. B still only miss, not answer.
