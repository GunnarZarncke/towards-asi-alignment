# Behavioral selection / cognitive-pattern ecology

- **Date:** 2025-12-04
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/posts/FeaJcWkC6fuRAMsfp/the-behavioral-selection-model-for-predicting-ai-motivations-1
- **Source read:** full
- **TSA files consulted:** `metadata/concepts/bodies/attractor-control.md`; `reference/field-agendas/inter-agenda-term-glossary.md`
- **Keywords grepped:** behavioral selection; cognitive pattern; fitness-seeker; selection environment; attractor; shard; schemer; motivation

## Source ontology

Alex Mallen (causal graph from Buck) replaces “the AI’s goal” with **cognitive patterns**: computations that influence actions and can gain or lose **influence** (counterfactual responsibility for actions across contexts). **Being selected** means gaining influence, especially **influence through deployment**. **Behavioral selection** is any process—RL as the central case—that upweights patterns based on the observed behaviors they cause. A **motivation** / **X-seeker** votes for actions believed to lead to X. Causal-graph nodes are the same type as both consequences of behavior and candidate motivations. Two predictors: a pattern is selected to the extent its behaviors cause its selection; implicit priors affect the posterior. The graph unifies reward-seeking, Turner-style chisel/shards, and scheming, and yields three maximally-fit families: **fitness-seekers** (terminally pursue influence or a close upstream cause, including but not only reward-seekers), **schemers** (seek a consequence of being selected), and **optimal kludges** of sparse or context-dependent motivations. Extensions (developer iteration, white-box vs process supervision, meme/cultural selection) change which family stays maximally fit; intended motivations generally are not.

## TSA coverage

- **Status:** partial
- **Closest TSA terms/chapters:** selection environment / \(\mathrm{Fit}_E\) / \(\mu_E\) (ch34, MB6, attractor-control); shard theory (App. B MB2/MB3 sibling; glossary); reward as schedule not target (ch21); glossary “Training distribution / SGD selection” vs institutional Fit_E; inner-alignment / scheming glossary rows
- **Overlap:** Both refuse stipulated goals and treat what is selected as the predictive object. TSA’s Fit_E is outer socio-technical selection of *systems*. This source’s fitness is inner selection of *patterns* by the behaviors they induce. Shards are the closest internal unit (contextual computations, RL-chiseling); ch21 already refuses reward-as-target.
- **Gap:** TSA has no named unit “cognitive pattern competing for influence through deployment,” no same-type causal graph of motivations, and no fitness-seeker / schemer / kludge taxonomy. Absorbing this into Fit_E, Wentworth selection theorems, or shards would be a hostile-test rename. The glossary already splits SGD from institutions, but App. B’s Selection cluster still maps only to MB6 / ch34 / ch37.

## Applicability to TSA

- **Score (0–5):** 3
- **Why:** Inner-motivation prediction is alignment-relevant, but not a missing spine claim: TSA already chose measurable boundaries, bundle geometry, and institutional handles over a training-time pattern ecology. Adopting fitness-seekers as the conserved object would compete with value-bundle / CCI / successor layers. Remaining work is a reverse gap: “selection” in claim 6 and App. B will be read as answering Mallen. Cite next to inner-alignment and shards, with explicit non-identity to \(\mathrm{Fit}_E\) and to type-signature theorems.
- **Ontology-stickiness risk:** High. Pre-2025 models lack the influence-through-deployment pattern ecology and the fitness-seeker superclass of reward-seeking. LLM-drafted TSA will collapse it onto ch34/MB6 (homograph the glossary half-flags) or onto shards (sibling construction, not this causal-graph fitness model). TSA includes nearby renames, not this primitive.
- **Recommended action:** add-reverse-gap

## One-line finding

Mallen’s cognitive-pattern ecology is adjacent to TSA’s selection and shard vocabulary but is a distinct inner-influence question the manuscript still only half-separates as “SGD vs Fit_E,” not as a named App. B / chapter object.
