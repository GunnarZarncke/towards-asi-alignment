# Self-driving laboratory

- **Date:** 2023-01-30
- **Field:** Engineering / chemical and materials science
- **Source:** https://www.nature.com/articles/s44160-022-00231-0
- **Source read:** abstract-only
- **TSA files consulted:** `chapters/ch09-composite-agent.tex`; `metadata/concepts/bodies/composite-agency.md`
- **Keywords grepped:** self-driving; laboratory; closed-loop; experiment; automation; robotics; composite agent; boundary discovery

## Source ontology

Abolhasani & Kumacheva define a self-driving lab (SDL) as a machine-learning-assisted modular experimental platform that iteratively runs experiments *selected by the ML algorithm* to achieve a user-defined objective, integrating ML, lab automation, and robotics. The recarving: “the experiment” is no longer an action the scientist chooses; experiment-selection is an internal action of the ML–robotics–instrumentation loop, which becomes the epistemic agent. The scientist remains as objective-setter, not as trial-chooser. (Abstract and figure captions only; full review paywalled.)

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** composite agency / “the agent is the loop” (ch09, Claim 1); scientist-plus-laboratory as composite discovery system (ch09); lab–benchmark–funding composite (ch09); boundary discovery (ch07, MB1). Nearby: selection environment (ch34); R&D-automation vocabulary in `reference/field-agendas/`.
- **Overlap:** Claim 1 already refuses the named chemist or model as the optimizer. Ch09’s tests (boundary closure, control reach, intentional compression) apply directly: an SDL has a stable instrument interface, high control over synthesis and characterization, and is compressed by the user-defined objective. Composite-agency.md’s target — the smallest dynamically coherent loop of users, tools, memory, and selection — *is* the SDL.
- **Gap:** Ch09’s “scientist plus laboratory” still has the scientist as discovery selector; the lab is apparatus. SDL moves *which experiment runs next* inside the loop. Restating SDL as “scientist+lab composite” fails the hostile test: a composite discovery system can still have humans choosing trials. TSA’s “lab” examples are frontier AI labs (evals, funding, deployment), not closed-loop wet-lab experiment-selectors. TSA can name an SDL only by stretching composite-agency onto a unit whose action space is experiment choice.

## Applicability to TSA

- **Score (0–5):** 2
- **Why:** SDL is a physical existence proof for Claim 1 / ch09, not a missing spine primitive. Treat it as the chemistry/materials instance of a composite whose actions are experiment selections under a user-defined objective. CCI, successor, and selection-environment questions about SDLs are the usual questions asked of any closed loop. App. B need not grow a row; a ch09 example or crosswalk cite is enough. Score is conservative because the source was abstract-only.
- **Ontology-stickiness risk:** Moderate-high. Pre-2023 training has high-throughput screening and lab automation, not “the loop is the epistemic agent.” AI-drafted TSA prose will map SDL onto ch09’s scientist+lab composite and miss that experiment selection moved inside — a rename that looks like coverage. TSA already includes the nearby object; it does not name the experiment-as-internally-selected unit.
- **Recommended action:** absorb-as-special-case

## One-line finding

Self-driving labs are ch09 composite agency operationalized as an experiment-selecting loop; TSA already has the nearby object but will miss the recarving unless SDL is absorbed as the case where trial choice, not just apparatus, sits inside the agent.
