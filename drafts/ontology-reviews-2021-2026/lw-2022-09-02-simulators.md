# Simulator / simulacrum

- **Date:** 2022-09-02
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/posts/vJFdjigzmcXMhNTsx/simulators
- **Source read:** full
- **TSA files consulted:** `chapters/ch11-capability-without-task-ontology.tex`, `chapters/ch05-assumptions-scope-failure-coverage.tex`
- **Keywords grepped:** simulacr, pattern-completion, goal-agnostic, self-supervised, janus, simulator theory, apparent agency

## Source ontology
Janus splits self-supervised predictors into two types: the **simulator** (the trained policy as a time-invariant transition law, optimized for the simulation objective of Bayes-optimal next-token prediction) and **simulacra** (agentic or non-agentic processes instantiated by prompting and sampling). Agency, knowledge, corrigibility, and myopia attach to simulacra, not to the law. This replaces the 1:1 policy–agent identification of the RL/agent frame, and also the oracle / tool / genie / behavior-cloning frames, which treat GPT as one specialized system rather than a generator of many contingent ones. Prediction orthogonality: an inner-aligned simulator can roll out agents with any goals (or none).

## TSA coverage
- **Status:** partial
- **Closest TSA terms/chapters:** Boundary discovery (Claim 1; ch06–ch10, especially ch07 finding-boundary and ch09 composite-agent); ch11 “simulator, oracle, or pattern-completion engine whose apparent agency comes from the prompt.” False friend: ch05 table row “Human replacement or simulacra” (Turchin/bearer persistence, not Janus). No hit in `appB-bridge-crosswalk.tex`, `reference/field-agendas/`, or `metadata/concepts/` except ELK’s unrelated “human simulator.”
- **Overlap:** TSA already refuses to identify the visible model with the real optimizer and notes that LM agency can be prompt-contingent (ch11). Composite-agent chapters look *above* the model (model+tools+users). Janus looks *inside* a single predictive policy: law vs phenomena, with multiple simultaneous or ephemeral simulacra.
- **Gap:** TSA cannot currently name simulator/simulacra *nonidentity* as a type distinction without stretching “boundary.” Aligning the simulator (inner alignment to prediction) is a different object from specifying or correcting simulacra. Collapsing Janus into “look past the interface” misses that a standalone autoregressive loop already has two levels.

## Applicability to TSA
- **Score (0–5):** 3
- **Why:** Load-bearing for LLM deconfusion and for Claim 1, but not a rival to TSA’s six cuts. The missing unit is the intra-policy split and the simulation objective as a distinct outer objective, not a new preservation target. `appB` maps ELK’s human-simulator, not Janus. A reverse-crosswalk line (simulator theory → boundary / inner alignment of predictors / simulacra specification) would stop the homonym and the skippable ch11 one-liner from standing in for the ontology.
- **Ontology-stickiness risk:** High. Pre-2022 alignment discourse stuck to agent/oracle/tool/genie; models trained on that corpus miss the two-level split. TSA already includes a compressed rename (ch11) and can *fail to see* the type distinction by folding it into composite-boundary language. Drafting LLMs will likely treat “simulator” as “not agentic” rather than as law vs simulacrum.
- **Recommended action:** add-reverse-gap

## One-line finding
Janus’s simulator/simulacrum split is a special case TSA almost has under boundary discovery, but TSA still lacks the type distinction and currently collides with a Turchin homonym in ch05.
