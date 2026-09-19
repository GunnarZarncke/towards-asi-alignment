# Machine psychology

- **Date:** 2023
- **Field:** Psychology
- **Source:** https://arxiv.org/abs/2303.13988
- **Source read:** full
- **TSA files consulted:** `chapters/ch11-capability-without-task-ontology.tex`, `chapters/ch39-passive-observation-not-enough.tex`
- **Keywords grepped:** psychology, interpretability, eliciting latent, competence, behavioral experiment, adversarial measurement, task ontology, benchmark

## Source ontology

Hagendorff, Dasgupta, Binz, Chan, Lampinen, Wang, Akata, and Schulz recast LLMs as experimental *subjects*, not only as engineered artifacts scored on NLP benchmarks or opened by mechanistic interpretability. The new unit is latent cognitive organization inferred from hypothesis-driven behavioral experiments (if construct X, expect behavior Y, else Z), with psychology-style controls and a performance–competence distinction. This replaces held-out accuracy on a named skill as the primary way to understand emergent abilities. Caveats are part of the ontology: self-report is prompt-steerable; classic stimuli contaminate training sets; anthropomorphic “thick descriptions” can add explanatory power without neural correlates.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** task ontology / benchmark trap (ch11); adversarial measurement and perturbation-to-infer-control (ch39); cost of faking behavior evaluation (ch44, grepped only); ontology trap (ch07, grepped only).
- **Overlap:** Ch11 already refuses capability-as-benchmark and notes that a score imports a frame (task, success, action space, system boundary). Ch39 already treats watching outputs and asking questions as weak unless interventions discriminate competing control hypotheses. Both sit near the source’s “not performance, constructs; not passive, experimental.”
- **Gap:** TSA does not name the experimental-subject class expansion or the construct-diagnostic vs performance-benchmark split as a distinct method family. Psychology constructs (theory of mind, heuristics, personality) remain an imported human-subject ontology; TSA’s next move is boundary discovery and cost-of-faking, which the source does not require. Machine psychology assumes the model-as-participant is the right unit; ch11’s tool-using composite is exactly the case where that unit fails.

## Applicability to TSA

- **Score (0–5):** 2
- **Why:** Useful as a field-method cite under eval / MB7: diagnostic behavioral experiments, contamination and prompt-robustness hygiene, and longitudinal construct tracking. It does not change a TSA cut. Absorbing it as “how we understand models” would lock onto the visible LLM as subject—the ontology trap. Cite beside interpretability-as-instrument (appB) as the behavioral counterpart, with the same non-substitute-for-CCI caveat.
- **Ontology-stickiness risk:** Moderate. Pre-2023 training already has “benchmarks vs interpretability” and “do LLMs have theory of mind.” The named primitive—models as psychology subjects, construct tests ≠ skill tests, competence ≠ performance—is easy to round into TSA’s already-present “don’t trust benchmarks” and “perturbation,” missing that the source still takes the chatbot-as-participant as given.
- **Recommended action:** cite-in-crosswalk

## One-line finding

Machine psychology expands the experimental-subject class to LLMs and splits construct-diagnostic tests from benchmarks; TSA already has task-ontology and adversarial measurement, and should cite the method without taking the visible model as the subject.
