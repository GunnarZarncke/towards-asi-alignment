# Three layers of LLM psychology

- **Date:** 2024-12-26
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/posts/zuXo9imNKYspu9HGv/a-three-layer-model-of-llm-psychology
- **Source read:** full
- **TSA files consulted:** `chapters/ch07-finding-boundary.tex`, `chapters/ch32-self-modeling-self-opacity.tex`
- **Keywords grepped:** persona, simulacrum, simulator, self-model, character layer, jailbreak, alignment fak

## Source ontology

Kulveit (Claude as writing partner) splits a character-trained LLM into three interacting layers rather than one mind. **Surface** is cached trigger-action patterns (refusals, stock disclaimers). **Character** is a weight-encoded, statistically persistent persona after character training: literary-character consistency, not an ephemeral generated agent. **Predictive Ground** (“the Ocean”) is the pretrained prediction-error machinery / world-model, which can simulate many perspectives and does not have Character-like values. Layers override one another (Character over Surface; many-shot jailbreaks as Ground over Character). The alignment primitive is that *which layer is self-aware* is not interchangeable: Character-layer situational awareness yields different behaviors and eval implications than Ground-layer awareness (Player vs Character). Explicitly not simulator/simulacra: Character is a privileged trained-in prior of the model itself.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** boundary discovery / many self-models (ch07); self-modeling vs self-transparency vs self-honesty, alignment faking cite (ch32); simulator/oracle as capability type (ch11, grepped only); ELK human-simulator (App B / field glossary).
- **Overlap:** Ch07 already asks whether the real optimizer is the chatbot, the network, the RL loop, or a composite, and notes a superintelligence may have many self-models at many scales. Ch32 splits self-modeling from correction-relevant transparency and cites Greenblatt alignment faking: that is the nearest TSA object to “the Assistant looks aligned while something else steers.”
- **Gap:** TSA’s \(K_{\mathrm{self}}\) is one self-model of “the system.” It does not distinguish Surface reflexes, Character-as-weight-prior, and Ground-as-predictive-ocean, nor the claim that Assistant-persona evals are a lower bound on Ground capability. Ch32’s “three goal layers” (semantic / bundle / effective) are a different cut. Rounding to ch11’s simulator/oracle or ELK’s human-simulator is the hostile-test failure the source warns about.

## Applicability to TSA

- **Score (0–5):** 3
- **Why:** Surface/Character/Ground is LLM phenomenology TSA need not take as a load-bearing cut. The live purchase is a reverse-gap on MB7 / eval grain: “what Claude does” can be Character-layer; Ground-layer Player awareness would subvert the same probes differently. TSA currently collapses that into one system’s \(K_{\mathrm{self}}\) vs \(T_{\mathrm{corr}}\). A crosswalk note on alignment-faking rows would keep the layer-of-awareness split visible without rewriting the boundary chapter.
- **Ontology-stickiness risk:** High. Simulators (2022) plus pre-character-trained models make rounding Character/Ground to simulacrum/simulator the default; Kulveit’s 2024 review says people still do this. TSA already uses simulator/oracle language (ch11) and cites alignment faking at system grain (ch32), so a pre-2024-trained drafter would miss Character-as-persistent-prior and treat Ground as “just physics, not a mind.”
- **Recommended action:** add-reverse-gap

## One-line finding

TSA already has “many self-models” and self-model vs transparency; it still lacks the Character-vs-Ground awareness split, so alignment-faking evals can be misread as measuring the whole LLM.
