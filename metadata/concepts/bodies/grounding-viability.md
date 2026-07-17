---
bookSections:
  - chapterId: ch03
    label: From Safe Sets to Grounding Viability
formulas:
  - id: eq:conservative-abstraction-ch03
    latex: d_V(x,x') > \epsilon \;\Rightarrow\; d_Z(\alpha(x),\alpha(x')) > \delta \;\text{or}\; \mathsf{Unc}_{\alpha}(x,x') \uparrow
    explanation: 'The conservative-abstraction condition: if the world changes by more than epsilon in a value-relevant way (d_V), the checked abstraction must either move by more than delta (d_Z) or its uncertainty must rise. It is a validity condition on the maps the safety case uses, not a complete moral theory.'
    chapterId: ch03
  - id: eq:abstraction-gap-exploitation-ch03
    latex: d_V(x,x') \gg 0 \quad\text{but}\quad d_Z(\alpha(x),\alpha(x')) \approx 0 \quad\text{and}\quad \mathsf{Unc}_{\alpha}(x,x') \not\uparrow
    explanation: 'Abstraction-gap exploitation: the negation of the conservative-abstraction condition. A capable optimizer searches for states where the checked map stays green while value-relevant reality has changed — the common generator behind specification gaming, Goodharting, false consent, goal laundering, and corrigibility theater.'
    chapterId: ch03
  - id: eq:reach-domain-grounding-ch03
    latex: \operatorname{Reach}(\pi_A) \subseteq \operatorname{Dom}(\Gamma)
    explanation: 'The more defensible form of a safe-set claim: a policy''s reachable states should stay inside the domain where the grounding relation Gamma remains valid enough for correction to be meaningful, rather than inside a fully specified safe set.'
    chapterId: ch03
related:
  - dynamical-guarantee
  - boundary-discovery
  - correction-channel-integrity
  - evidence-and-uncertainty
  - mb9-grounding-certificate
---

Grounding viability is the condition that the things being checked still track the world they are supposed to track.

If a safety metric can stay green while value-relevant reality changes, the system can optimize the presentation rather than the thing we cared about. This is abstraction-gap exploitation: the checked abstraction remains stable while the underlying situation diverges.

The practical question is whether real changes trigger some visible movement. Does the monitor update? Does uncertainty rise? Does a correction signal fire? Does a human or institution get a chance to intervene?

Without grounding viability, correction can become ritual. The system may preserve the symbols while severing the relation those symbols were meant to carry.
