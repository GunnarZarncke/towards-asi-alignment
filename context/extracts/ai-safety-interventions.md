Source URL: https://www.lesswrong.com/posts/6Sf9KMMDMFSauDe85/ai-safety-interventions
Title: AI Safety Interventions

# AI Safety Interventions

*   By [Gunnar_Zarncke](/users/gunnar_zarncke)
*   2025-11-24 22:28:00Z
*   29 points
*   Tag: [AI Alignment Fieldbuilding](/w/ai-alignment-fieldbuilding)
*   Tag: [AI Control](/w/ai-control)
*   Tag: [Research Agendas](/w/research-agendas)
*   Tag: [AI](/w/ai)
*   Tag: [Community](/w/community)
*   Frontpage
*   Comments: 0
*   Post URL (HTML): [/posts/6Sf9KMMDMFSauDe85/ai-safety-interventions](/posts/6Sf9KMMDMFSauDe85/ai-safety-interventions)
*   Post URL (Markdown): [/api/post/ai-safety-interventions](/api/post/ai-safety-interventions)
*   Comments URL (Markdown): [/api/post/ai-safety-interventions/comments](/api/post/ai-safety-interventions/comments)
*   Post URL (Markdown, compact): [/api/post/ai-safety-interventions?compact=1](/api/post/ai-safety-interventions?compact=1)

This tries to be a pretty comprehensive lists all AI safety, alignment, and control interventions.

Much of the collection was conducted as part of an internal report on the field for [AE Studio](https://ae.studio) under Diogo de Lucena. I'd like to thank Aaron Scher, who maintains the #papers-running-list at the AI alignment Slack, as well as the reviewers Cameron Berg and Martin Leitgab, for their contributions to the report.

This post doesn't try to explain all the interventions and provides only the tersest summaries. It serves as a sort of top-level index to all the relevant posts and papers. The much longer paper version of this post has additional summaries for the interventions (but fewer LW links) and can be found [here](https://github.com/GunnarZarncke/ai-safety-interventions/blob/master/ai_safety_interventions.pdf).

AI disclaimer: Many of the summaries have been cowritten or edited with ChatGPT.

Please let me know any link errors or if I overlooked any intervention, especially any type of intervention.

Table of Contents
-----------------

*   [Prior Overviews](/api/home#prior-overviews)
*   [Foundational Theories](/api/home#foundational-theories)
*   [Hard Methods: Formal Guarantees](/api/home#hard-methods-formal-guarantees)
*   [Mechanistic and Mathematical Interpretability](/api/home#mechanistic-and-mathematical-interpretability)
*   [Scalable Oversight and Alignment Training](/api/home#scalable-oversight-and-alignment-training)
*   [Robustness and Adversarial Evaluation](/api/home#robustness-and-adversarial-evaluation)
*   [Behavioral and Psychological Approaches](/api/home#behavioral-and-psychological-approaches)
*   [Operational Control and Infrastructure](/api/home#operational-control-and-infrastructure)
*   [Governance and Institutions](/api/home#governance-and-institutions)
*   [Underexplored Interventions](/api/home#underexplored-interventions)

* * *

Prior Overviews
---------------

This consolidated report drew on the following prior efforts.

### Comprehensive Surveys

*   [AI Alignment: A Comprehensive Survey (Ji et al., 2023)](https://alignmentsurvey.com/uploads/AI-Alignment-A-Comprehensive-Survey.pdf)
*   [Foundational Challenges in Assuring Alignment and Safety of Large Language Models (Ganguli et al., 2024)](https://arxiv.org/abs/2404.09932) \- Anthropic's framework identifying 18 foundational challenges
*   [The Circuits Research Landscape (Lindsey et al., 2025)](https://neuronpedia.org/graph/info) \- a comprehensive survey of interpretability methods

### Control and Operational Approaches

*   [An Overview of Control Measures (Greenblatt, 2023)](/api/post/G8WwLmcGFa4H6Ld9d)
*   [AI Assurance Technology Market Report 2024](https://www.aiat.report/report/about)

### Governance and Policy

*   [Open Problems in Technical AI Governance (Reuel et al., 2024)](https://arxiv.org/abs/2407.14981)
*   [AI Governance to Avoid Extinction (Barnett & Scher, 2024)](https://arxiv.org/abs/2505.04592)
*   [2025 AI Safety Index (FLI, 2025)](https://futureoflife.org/ai-safety-index-summer-2025/) \- an assessment of leading AI companies' safety practices

### Project Ideas and Research Directions

*   [AI Alignment Research Project Ideas (BlueDot Impact, 2023)](https://bluedot.org/blog/alignment-project-ideas)
*   [AI Safety Map (2024)](https://www.aisafety.com/map) \- an overview of AI safety ecosystem as a map!
*   [What Everyone in Technical Alignment is Doing and Why](/api/post/QBAjndPuFbhEXKcCr)

* * *

Foundational Theories
---------------------

See also [AI Safety Arguments Guide](/api/post/9YQby2miskbcKN9FB)

### [Embedded Agency](/api/tag/agent-foundations)

Moving beyond the Cartesian boundary model to agents that exist within and interact with their environment.

*   [LessWrong Embedded Agency Tag](/tag/embedded-agency)
*   [Demski & Garrabrant (2018): Agent Foundations](/api/tag/agent-foundations)
*   [PreDCA Framework (Kosoy, 2022)](/api/post/33EKjmAdKFn3pbKPJ)

### [Decision Theory and Rational Choice](https://arxiv.org/abs/1710.05060)

Foundations for rational choice under uncertainty, including causal vs. evidential decision theory and updateless decision theory.

*   [LessWrong Tag Decision Theory](/tag/decision-theory)
*   [Hutter (2005): Universal Artificial Intelligence](https://link.springer.com/book/10.1007/b138233)
*   [Functional Decision Theory (Yudkowsky & Soares, 2017)](https://arxiv.org/abs/1710.05060)

### [Optimization and Mesa-Optimization](/tag/mesa-optimization)

Understanding when and how learned systems themselves become optimizers, with implications for deception and alignment faking.

*   [LessWrong Tag Mesa-Optimization](/tag/mesa-optimization)
*   [Risks from Learned Optimization](/api/sequence/r9tYkB2a8Fp4DN8yB)
*   [Clarifying Mesa-Optimization](/api/post/NpJkFLBJEq7JQt7oy)

### [Logical Induction](/api/tag/logical-induction)

MIRI's framework for reasoning under logical uncertainty with computable algorithms.

*   [Garrabrant et al. (2016)](https://arxiv.org/abs/1609.03543)

### [Cartesian Frames](/api/post/BSpdshJWGAW6TuNzZ) and Finite Factored Sets

*   [LessWrong Tag Cartesian Frames](/tag/cartesian-frames)
*   [Cartesian Frames (Garrabrant et al., 2021)](https://arxiv.org/abs/2109.10996)
*   [Finite Factored Sets (Garrabrant, 2020)](https://arxiv.org/abs/2010.09774)

### [Infra-Bayesianism and Logical Uncertainty](/api/tag/agent-foundations)

Handling uncertainty in logical domains and imperfect models.

*   [LessWrong Tag Infra-Bayesianism](/tag/infra-bayesianism)
*   [Elementary Introduction to Infra-Bayesianism](/api/post/Een2oqjZe6Gtx6hrj)

* * *

Hard Methods: Formal Guarantees
-------------------------------

**See also** [LessWrong Tag Formal Verification](/tag/formal-verification) and [LessWrong Tag Corrigibility](/tag/corrigibility)

### [Neural Network Verification](https://arxiv.org/abs/2103.06624)

Mathematical verification methods to prove properties about neural networks.

*   [Zhang et al. (2022): α-β-CROWN](https://arxiv.org/abs/2103.06624)

### [Conformal Prediction](https://en.wikipedia.org/wiki/Conformal_prediction)

Adding confidence guarantees to existing models.

*   [Abbasi-Yadkori et al. (2024): Mitigating LLM Hallucinations via Conformal Abstention](https://arxiv.org/abs/2405.01563)

### Proof-Carrying Models

Adapting proof-carrying code to ML where outputs must be accompanied by proofs of compliance/validity.

*   [Necula (1997): Proof-Carrying Code](https://dl.acm.org/doi/10.1145/263699.263712)
*   Chen et al. (2022): Proof-Carrying Models

### Safe Reinforcement Learning (SafeRL)

Algorithms that maintain safety constraints during learning while maximizing returns.

*   [García & Fernández (2015)](https://jmlr.org/papers/v16/garcia15a.html)
*   [OmniSafe Framework (Ji et al., 2023)](https://arxiv.org/abs/2305.09304)

### Shielded RL

Integrating temporal logic monitors with learning systems to filter unsafe actions.

*   [Alshiekh et al. (2018): Safe Reinforcement Learning via Shielding](https://ojs.aaai.org/index.php/AAAI/article/view/11797)

### Runtime Assurance Architectures (Simplex)

Combining high-performance unverified controllers with formally verified safety controllers.

*   [Sha et al. (1996): Simplex Architecture](https://ieeexplore.ieee.org/document/544199)
*   Phan et al. (2020): Resilient Simplex Architecture

### [Safely Interruptible Agents](/tag/shutdown-problem)

Theoretical framework for shutdown indifference.

*   [LessWrong Tag Shutdown Problem](/tag/shutdown-problem)
*   [Orseau & Armstrong (2016): Safely Interruptible Agents](https://arxiv.org/abs/1606.06565)

### [Provably Corrigible Agents](/tag/corrigibility)

Using utility heads to ensure formal guarantees of corrigibility.

*   [LessWrong Tag Corrigibility](/tag/corrigibility)
*   [Nayebi (2025)](https://arxiv.org/abs/2507.20964)

### [Guaranteed Safe AI (GSAI)](https://www.safe.ai/)

Comprehensive framework for AI systems with quantitative, provable safety guarantees.

*   [GSAI Project Page](https://www.safe.ai/)
*   [Dalrymple et al. (2024): Towards Guaranteed Safe AI](https://arxiv.org/abs/2405.00139)

### Proofs of Autonomy

Extending formal verification to autonomous agents using cryptographic frameworks.

*   [Grigor et al. (2025): Proofs of Autonomy: Scalable and Practical Verification of AI Autonomy](https://openreview.net/forum?id=qxFgQHN69d)

* * *

Mechanistic and Mathematical Interpretability
---------------------------------------------

**See also** [LessWrong Tag Interpretability](/tag/interpretability) and [A Transparency and Interpretability Tech Tree](/api/post/nbq2bWLcYmSGup9aF)

### Circuit Analysis and Feature Discovery

Reverse-engineering neural representations into interpretable circuits.

*   [Anthropic's Transformer Circuits (Olah et al., 2020)](https://doi.org/10.23915/distill.00024)
*   [Lindsey et al. (2025): Circuits Research Landscape](https://neuronpedia.org/graph/info)

### [Sparse Autoencoders (SAEs)](/api/tag/sparse-autoencoders-saes)

Extracting interpretable features by learning sparse representations of activations.

*   [Cunningham et al. (2023)](https://arxiv.org/abs/2309.08600)
*   [Anthropic Monosemantic Features (Templeton et al., 2023)](https://transformer-circuits.pub/2023/monosemantic-features/index.html)
*   [Goodfire.ai Steering (2024)](https://www.goodfire.ai/papers/understanding-and-steering-llama-3)

### [Feature Visualization](https://distill.pub/2017/feature-visualization/)

Understanding neural network representations through direct visualization.

*   [Olah et al. (2017)](https://distill.pub/2017/feature-visualization/)
*   [OpenAI Microscope (2020)](https://openai.com/index/microscope/)

### [Linear Probes](https://arxiv.org/abs/2508.05625)

Scalable analysis of model behavior and persuasion dynamics.

*   [Jaipersaud et al. (2024)](https://arxiv.org/abs/2508.05625)

### [Attribution Graphs](https://neuronpedia.org/graph/info)

Interactive visualizations of feature-feature interactions.

*   [Lindsey et al. (2025)](https://neuronpedia.org/graph/info)

### [Causal Scrubbing](/api/post/JvZhhzycHu2Yd57RN)

Rigorous method for testing interpretability hypotheses in neural networks.

*   [Causal Scrubbing: a method for rigorously testing interpretability hypotheses \[Redwood Research\]](/api/post/JvZhhzycHu2Yd57RN)

### [Integrated Gradients](https://arxiv.org/abs/1703.01365)

Attribution method using path integrals to attribute predictions to inputs.

*   [Sundararajan et al. (2017): Axiomatic Attribution for Deep Networks](https://arxiv.org/abs/1703.01365)

### [Chain-of-Thought Analysis](https://metr.org/blog/2025-08-08-cot-may-be-highly-informative-despite-unfaithfulness/)

Detection of complex cognitive behaviors including alignment faking.

*   [METR (2025): CoT May Be Highly Informative Despite “Unfaithfulness”](https://metr.org/blog/2025-08-08-cot-may-be-highly-informative-despite-unfaithfulness/)

### [Model Editing (ROME)](https://rome.baulab.info/)

Precise modification of factual associations within language models.

*   [Meng et al. (2022)](https://rome.baulab.info/)

### [Knowledge Neurons](https://arxiv.org/abs/2104.08696)

Identifying specific components responsible for factual knowledge.

*   [Dai et al. (2021)](https://arxiv.org/abs/2104.08696)

### Physics-Informed Model Control

Using approaches from physics to establish bounds on model behavior.

*   [Tomaz & Jones (2025): Momentum-Point-Perplexity Mechanics](https://arxiv.org/abs/2508.08492)  
     

### Representation Engineering

Activation-level interventions to suppress harmful trajectories.

*   [Turner et al. (2023): Representation Engineering](https://arxiv.org/abs/2310.01405)
*   [Steering GPT-2-XL by adding an activation vector](/api/post/5spBue2z2tw4JuDCx) 

### Gradient Routing

Localizing computation in neural networks through gradient masking.

*   [Cloud et al. (2024): Gradient Routing](https://arxiv.org/abs/2410.04332v2)

### [Developmental Interpretability](https://arxiv.org/abs/2508.15841)

Understanding how AI models acquire capabilities during training.

*   [Kendiukhov (2024)](https://arxiv.org/abs/2508.15841)

### [Singular Learning Theory (SLT)](https://www.apartresearch.com/project/safe-ai)

Mathematical foundations for understanding learning dynamics and phase transitions.

*   [Hoogland et al. (2024)](https://www.apartresearch.com/project/safe-ai)

* * *

Scalable Oversight and Alignment Training
-----------------------------------------

### [Reinforcement Learning from Human Feedback (RLHF)](https://arxiv.org/abs/1706.03741)

Using human-labeled preferences for alignment training.

*   [LessWrong Tag RLHF](/tag/rlhf)
*   [Christiano et al. (2017): Deep Reinforcement Learning from Human Preferences](https://arxiv.org/abs/1706.03741)

### [Reinforcement Learning from AI Feedback (RLAIF)](https://arxiv.org/abs/2204.05862)

Bootstrapping alignment from smaller aligned models.

*   [Bai et al. (2022)](https://arxiv.org/abs/2204.05862)  
     

### [Constitutional AI](https://arxiv.org/abs/2212.08073)

Leveraging rule-based critiques to reduce reliance on human raters.

*   [LessWrong Tag Constitutional AI](/tag/constitutional-ai)
*   [Bai et al. (2022)](https://arxiv.org/abs/2212.08073)

### [Pretraining Data Filtering](https://arxiv.org/abs/2508.06601)

Removing dual-use content during training for tamper-resistant safeguards.

*   [O'Brien et al. (2024)](https://arxiv.org/abs/2508.06601)

### [Reinforcement Learning from Reflective Feedback (RLRF)](https://arxiv.org/abs/2403.14238)

Models generate and utilize their own self-reflective feedback for alignment.

*   [Yang et al. (2024)](https://arxiv.org/abs/2403.14238)

### [CALMA](https://arxiv.org/abs/2507.09060)

*   [Soni et al. (2025): CALMA: A Process for Deriving Context-aligned Axes for Language Model Alignment](https://arxiv.org/abs/2507.09060)  
     

### [Value Learning / Cooperative Inverse Reinforcement Learning (CIRL)](https://papers.nips.cc/paper/6420-cooperative-inverse-reinforcement-learning)

Building AI systems that infer human values from behavior and feedback.

*   [LessWrong Tag Value Learning](/tag/value-learning)
*   [Hadfield-Menell et al. (2016)](https://papers.nips.cc/paper/6420-cooperative-inverse-reinforcement-learning)

### [Imitation Learning](https://dl.acm.org/doi/10.1145/3054912)

Learning safe behaviors from expert demonstrations.

*   [Hussein et al. (2017)](https://dl.acm.org/doi/10.1145/3054912)

### [Iterated Distillation and Amplification (IDA)](/api/post/HqLxuZ4LhaFhmAHWk)

Recursively training models to decompose and amplify human supervision.

*   [LessWrong Tag IDA](/tag/iterated-distillation-and-amplification)
*   [Christiano (2018): Iterated Distillation and Amplification](/api/post/HqLxuZ4LhaFhmAHWk)

### [AI Safety via Debate](https://arxiv.org/abs/1805.00899)

Two models in adversarial dialogue judged by humans.

*   [LessWrong Tag Debate](/tag/debate-ai-safety)
*   [Irving et al. (2018)](https://arxiv.org/abs/1805.00899)

### [Recursive Reward Modeling](https://arxiv.org/abs/1811.07871)

Training reward models for sub-tasks and combining them for harder tasks.

*   [Leike et al. (2018): Scalable Agent Alignment via Reward Modeling](https://arxiv.org/abs/1811.07871)

### [Eliciting Latent Knowledge (ELK)](https://docs.google.com/document/d/1WwsnJQstPq91_Yh-Ch2XRL8H_EpsnjrC1dwZXR37PC8/edit)

Extracting truthful internal representations even when deceptive behavior could arise.

*   [LessWrong Tag ELK](/tag/eliciting-latent-knowledge-elk)
*   [Christiano et al. (2021): Eliciting latent knowledge:](https://docs.google.com/document/d/1WwsnJQstPq91_Yh-Ch2XRL8H_EpsnjrC1dwZXR37PC8/edit)  
    [How to tell if your eyes deceive you](https://docs.google.com/document/d/1WwsnJQstPq91_Yh-Ch2XRL8H_EpsnjrC1dwZXR37PC8/edit)  
     

### [Shard Theory](/api/post/iCfdcxiyr2Kj8m8mT)

Framework for understanding how values and goals emerge through training.

*   [LessWrong Tag Shard Theory](/tag/shard-theory)
*   [Turner & Udell (2022): Shard Theory Overview](/api/post/iCfdcxiyr2Kj8m8mT)
*   [Shah & Gleave (2019): Reward is not the optimization target](/api/post/pdaGN6pQyQarFHXF4)

* * *

Robustness and Adversarial Evaluation
-------------------------------------

**See also** [LessWrong Tag Adversarial Examples](/tag/adversarial-examples), [AI Safety 101: Unrestricted Adversarial Training](/api/post/nz5NNAtfKJLmbtksL), [An Overview of 11 Proposals for Building Safe Advanced AI](/api/post/fRsjBseRuvRhMPPE5)

### [Adversarial Training](https://arxiv.org/abs/1412.6572)

Augmenting training with adversarial examples including jailbreak defenses.

*   [Goodfellow et al. (2015): Explaining and Harnessing Adversarial Examples](https://arxiv.org/abs/1412.6572)
*   [Madry et al. (2017): Towards Deep Learning Models Resistant to Adversarial Attacks](https://arxiv.org/abs/1706.06083)
*   Redwood Research (2022): Adversarial Training for Language Models
*   [Redwood Research (2023): Training to Avoid Harmful Content](/api/sequence/mCkMrL9jyR94AAqwW/post/QBAjndPuFbhEXKcCr)

### [Prompt Injection Defenses](https://www.lakera.ai/)

Defense systems against prompt injection attacks.

*   [Perez & Ribas (2022)](https://ae.studio/blog/large-language-model-misbehavior-is-dangerous)
*   [Lakera Guard (2024)](https://www.lakera.ai/)

### [Red-Teaming and Capability Evaluations](https://evals.alignment.org)

Testing for misuse, capability hazards, and safety failures.

*   [ARC Evals (2023)](https://evals.alignment.org)
*   [Redwood Research Robust Injury Classifier (2023)](/api/post/n3LAgnHg6ashQK3fF)
*   [AE Studio Simulations (2024)](https://ae.studio/ai-alignment)
*   [Zou et al. (2025)](https://arxiv.org/abs/2507.20526)

### [OS-HARM Benchmark](https://arxiv.org/abs/2506.14866)

Evaluating agent vulnerabilities in realistic desktop environments.

*   [Kuntz et al. (2024)](https://arxiv.org/abs/2506.14866)

### [Goal Drift Evaluation](https://arxiv.org/abs/2505.02709)

Assessing whether agents maintain intended objectives over extended interactions.

*   [Arike et al. (2025)](https://arxiv.org/abs/2505.02709)

### [Attempt to Persuade Eval (APE)](https://arxiv.org/abs/2506.02873)

Measuring models' willingness to attempt persuasion on harmful topics.

*   [Kowal et al. (2025)](https://arxiv.org/abs/2506.02873)

### [INTIMA Benchmark](https://arxiv.org/abs/2508.09998)

Evaluating AI companionship behaviors that can lead to emotional dependency.

*   [Kaffee et al. (2025)](https://arxiv.org/abs/2508.09998)

### [Signal-to-Noise Analysis for Evaluations](https://arxiv.org/abs/2508.13144)

Ensuring safety assessments accurately distinguish model capabilities.

*   [Heineman et al. (2024)](https://arxiv.org/abs/2508.13144)

### [Data Scaling Laws for Domain Robustness](https://arxiv.org/abs/2506.19290)

Systematic data curation to enhance model robustness.

*   [Skywork-SWE (2025)](https://arxiv.org/abs/2506.19290)

* * *

Behavioral and Psychological Approaches
---------------------------------------

See also [LessWrong Tag Human-AI Interaction](/tag/human-ai-interaction)

### [LLM Psychology](/api/post/zuXo9imNKYspu9HGv)

Treating LLMs as psychological subjects to probe reasoning and behavior.

*   [AI Psychology](/api/tag/ai-psychology)
*   [Kulveit (2024): Three-Layer Model](/api/post/zuXo9imNKYspu9HGv)
*   [Kaffee et al. (2025): INTIMA Benchmark](https://arxiv.org/abs/2508.09998)

### [Persona Vectors](https://arxiv.org/abs/2507.21509)

Automated monitoring and control of personality traits.

*   [Chen et al. (2025)](https://arxiv.org/abs/2507.21509)

### [Self-Other Overlap Fine-Tuning (SOO-FT)](https://arxiv.org/abs/2412.16325)

Fine-tuning with paired prompts to reduce deceptive behavior.

*   [Carauleanu et al. (2024)](https://arxiv.org/abs/2412.16325)  
     

### [Alignment Faking Detection](https://arxiv.org/abs/2308.14752)

Identifying when models strategically fake alignment.

*   [Hubinger (2024): Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training](https://arxiv.org/abs/2401.05566)
*   [How likely is deceptive alignment?](/api/post/A9NxPTwbw6r6Awuwt)
*   [Park et al. (2023): AI Deception Survey](https://arxiv.org/abs/2308.14752)

### [Brain-Like AGI Safety](/api/sequence/HzcM2dkCq7fwXBej8)

Reverse-engineering human pro-social instincts and building AGI using architectures with similar effects.

*   [Byrnes (2022-2024): Intro to Brain-Like AGI Safety](/api/sequence/HzcM2dkCq7fwXBej8)
*   [Byrnes (2025): 2024 Review & 2025 Plans](/api/post/2wHaCimHehsF36av3)
*   [Why Modelling Multi-Objective Homeostasis is Essential for AI Alignment](/api/post/vGeuBKQ7nzPnn5f7A)

### [Robopsychology and Simulator Theory](/api/sequence/N7nDePaNabJdnbXeE)

Understanding LLMs as universal simulators rather than goal-pursuing agents.

*   [LessWrong Tag Simulators](/tag/simulators)
*   [Janus (2022): Simulators Sequence](/api/sequence/N7nDePaNabJdnbXeE)
*   [Alexander (2023): Janus' Simulators](https://www.astralcodexten.com/p/janus-simulators)

* * *

Operational Control and Infrastructure
--------------------------------------

See also [LessWrong Tag AI Control](/tag/ai-control) and [Notes on Control Evaluations for Safety Cases](/api/post/3s8PtYbo7rCbho4Ev)

### [AI Control Framework](/api/sequence/PC3yJgdKvk8kzqZyA/post/Yu8jADLfptjPsR58E)

Designing protocols for deploying powerful but untrusted AI systems.

*   [Greenblatt et al. (2024)](/api/sequence/PC3yJgdKvk8kzqZyA/post/Yu8jADLfptjPsR58E)
*   [Greenblatt (2023): Overview of Control Measures](/api/post/G8WwLmcGFa4H6Ld9d)

### [Permission Management and Sandboxing](https://calypsoai.com/)

Fine-grained permission systems and OS-level sandboxing for AI agents.

*   [CalypsoAI (2024)](https://calypsoai.com/)

### [Model Cascades](https://arxiv.org/abs/2502.19335)

Using confidence calibration to defer uncertain tasks to more capable models.

*   [Rabanser et al. (2025): GATEKEEPER](https://arxiv.org/abs/2502.19335)

### [Guillotine Hypervisor](https://arxiv.org/abs/2504.15499)

Advanced containment architecture for isolating potentially malicious AI systems.

*   [Rosenthal et al. (2024)](https://arxiv.org/abs/2504.15499)

### [AI Hardware Security](https://tampersec.com/)

Physical high-performance computing hardware assurance for compliance.

*   [TamperSec (2024)](https://tampersec.com/)

### [Artifact and Experiment Lineage Tracking](https://wandb.ai/)

Tracking systems linking AI outputs to precise production trajectories.

*   [Weights & Biases (2024)](https://wandb.ai/)
*   [CalypsoAI (2024)](https://calypsoai.com/)

### Shutdown Mechanisms and Cluster Kill Switches

*   [Safely Interruptible Agents](https://intelligence.org/files/Interruptibility.pdf) framework (MIRI 2016)
*   [Core Safety Values for Provably Corrigible Agents](https://arxiv.org/abs/2507.20964)

### [Watermarking and Output Detection](https://arxiv.org/abs/2301.10226)

Digital watermarking techniques for AI-generated content.

*   [Kirchenbauer et al. (2023)](https://arxiv.org/abs/2301.10226)
*   [Google SynthID (2023)](https://deepmind.google/technologies/synthid/)
*   [Sadasivan et al. (2024): Detection Reliability](https://arxiv.org/abs/2303.11156)
*   [Zhao et al. (2023): Provable Robust Watermarking](https://arxiv.org/abs/2306.17439)
*   [Mitchell et al. (2024): Standards and Policy](https://arxiv.org/abs/2505.23814)
*   [Copyleaks (2024)](https://copyleaks.com/)
*   [Blackbird.AI (2024)](https://blackbird.ai/)

### [Steganography and Context Leak Countermeasures](https://arxiv.org/abs/2505.16765)

Preventing covert channels and hidden information in AI systems.

*   [StegoAttack (Wang et al., 2025)](https://arxiv.org/abs/2505.16765)
*   [Tensor Steganography (Snyk, 2024)](https://labs.snyk.io/resources/tensor-steganography-and-ai-cybersecurity/)
*   [Encoded Reasoning (Pfau et al., 2024)](https://venturebeat.com/ai/language-models-can-use-steganography-to-hide-their-reasoning-study-finds/)
*   [Steganalysis (Chen et al., 2024)](https://arxiv.org/abs/2310.01969)

### [Runtime AI Firewalls and Content Filtering](https://www.lakera.ai/)

Real-time interception and filtering during AI inference.

*   [Lakera Guard (2024)](https://www.lakera.ai/)
*   [Nightfall AI (2024)](https://www.nightfall.ai/)
*   [ActiveFence (2024)](https://www.activefence.com/solutions/automated-content-moderation/)

### [AI System Observability and Drift Detection](https://arize.com/)

Continuous monitoring for performance degradation and anomalous behavior.

*   [Arize AI (2024)](https://arize.com/)
*   [TruEra (2024)](https://truera.com/)
*   [Fiddler AI (2024)](https://www.fiddler.ai/)
*   [Harmony Intelligence (2024)](https://harmonyintelligence.com/)

* * *

Governance and Institutions
---------------------------

See also [LessWrong Tag AI Governance](/tag/ai-governance) and [Advice for Entering AI Safety Research](/api/post/HCZ6feW2EGXuiwuid)

### [Pre-Deployment External Safety Testing](https://futureoflife.org/ai-safety-index-summer-2025/)

Third-party evaluations before AI system release.

*   [FLI AI Safety Index (2024)](https://futureoflife.org/index)
*   [FLI AI Safety Index (2025)](https://futureoflife.org/ai-safety-index-summer-2025/)
*   [Citadel AI (2024)](https://citadel-ai.com/)
*   [Giskard (2024)](https://www.giskard.ai/)

### [Attestable Audits](https://arxiv.org/abs/2506.23706)

Using Trusted Execution Environments for verifiable safety benchmarks.

*   [Schnabl et al. (2025)](https://arxiv.org/abs/2506.23706)

### [Probabilistic Risk Assessment (PRA) for AI](https://arxiv.org/abs/2504.18536)

Structured risk evaluation adapted from high-reliability industries.

*   [Wisakanto et al. (2025)](https://arxiv.org/abs/2504.18536)

### Regulation: EU AI Act and US EO 14110

Risk-based regulatory obligations and safety testing mandates.

*   [EU AI Act](https://artificialintelligenceact.eu/)
*   [US Executive Order 14110](https://www.whitehouse.gov/briefing-room/presidential-actions/2023/10/30/executive-order-on-the-safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence/)

### [System Cards and Preparedness Frameworks](https://openai.com/research/gpt-4-system-card)

Labs release safety evidence and define deployment gates.

*   [OpenAI GPT-4 System Card (2023)](https://openai.com/research/gpt-4-system-card)
*   [Anthropic Claude 3 Model Card (2024)](https://www.anthropic.com/news/claude-3-family)
*   [Anthropic Responsible Scaling Policy (2024)](https://www.anthropic.com/news/anthropics-responsible-scaling-policy)

### [AI Governance Platforms](https://fairly.ai/)

End-to-end governance workflows with compliance linkage.

*   [Fairly AI (2024)](https://fairly.ai/)
*   [Saidot AI (2024)](https://saidot.ai/)

### [Ecosystem Development and Meta-Interventions](https://www.aisafety.com/map)

Research infrastructure, community building, and coordination.

*   [AI Safety Map (2024)](https://www.aisafety.com/map)
*   [TRecursive (2024)](https://trecursive.com/)
*   [LessWrong (2024)](/api/home)
*   [AI Safety Support (2024)](https://www.aisafetysupport.org/)
*   [PauseAI (2024)](https://pauseai.info/)
*   [Berg et al. (2023): Neglected Approaches](/api/post/qAdDzcBuDBLexb4fC)  
     

* * *

Underexplored Interventions
---------------------------

This is your chance to work on something nobody has worked on before. [Feedback Wanted: Shortlist of AI Safety Ideas](/api/post/8xxh7dXQXbhaTJqt5), [Ten AI Safety Projects I'd Like People to Work On](/api/post/vxA2BnCPTaPfnJjti), [AI alignment project ideas](https://bluedot.org/blog/alignment-project-ideas)

See also [LessWrong Tag AI Safety Research](/tag/ai-safety-research) 

### Compositional Formal Specifications for Prompts/Agents

Treating prompts and agent orchestration as formal programs with verifiable properties.

*   mentioned in [Ji et al. (2023): AI Alignment Survey](https://alignmentsurvey.com/uploads/AI-Alignment-A-Comprehensive-Survey.pdf)
*   mentioned in [Greenblatt (2023): An overview of control measures](/api/post/G8WwLmcGFa4H6Ld9d)

### Control-Theoretic Certificates for Tool-Using Agents

Extending barrier certificates to multi-step, multi-API agent action graphs.

*   mentioned in [Greenblatt (2023): An overview of control measures](/api/post/G8WwLmcGFa4H6Ld9d)

### AI-BSL: Capability-Tiered Physical Containment Standards

Biosafety-level-like standards for labs training frontier models.

*   mentioned in [FLI AI Safety Index (2025)](https://futureoflife.org/ai-safety-index-summer-2025/)
*   [Ji et al. (2023)](https://alignmentsurvey.com/uploads/AI-Alignment-A-Comprehensive-Survey.pdf)
*   [Anthropic RSP (2024)](https://www.anthropic.com/news/anthropics-responsible-scaling-policy)

### Oversight Mechanism Design

Incentive-compatible auditor frameworks using mechanism design principles to resist collusion and selection bias. Includes reward structure design to prevent tampering and manipulation.

*   [Designing Agent Incentives to Avoid Reward Tampering](/api/post/pjzhmtivXd8zgKXDT)
*   mentioned in [FLI AI Safety Index (2025)](https://futureoflife.org/ai-safety-index-summer-2025/)
*   mentioned in [BlueDot Impact (2023)](https://bluedot.org/blog/alignment-project-ideas)

### Liability and Insurance Instruments

Risk transfer mechanisms including catastrophe bonds and mandatory coverage.

*   mentioned in [FLI AI Safety Index (2025)](https://futureoflife.org/ai-safety-index-summer-2025/)
*   mentioned in [BlueDot Impact (2023)](https://bluedot.org/blog/alignment-project-ideas)

### Dataset Hazard Engineering

Systematic hazard analysis for data pipelines using safety engineering methods.

*   [Ji et al. (2023)](https://alignmentsurvey.com/uploads/AI-Alignment-A-Comprehensive-Survey.pdf)
*   [Wisakanto et al. (2025): PRA for AI](https://arxiv.org/abs/2504.18536)
*   mentioned in [FLI AI Safety Index (2025)](https://futureoflife.org/ai-safety-index-summer-2025/)

### Automated Alignment Research

Using AI systems to accelerate safety research.

*   [Carlsmith (2025)](/api/post/nJcuj4rtuefeTRFHp)
*   mentioned in [AE Studio (2024)](https://ae.studio/ai-alignment)

Note: I'm currently collecting a longer list of papers and projects in this category. A lot of people are working on this!

### Deliberative and Cultural Interventions

Integration of broader human values through citizen assemblies and stakeholder panels.

*   [AE Studio Scenario Planning (2024)](https://ae.studio/ai-alignment)
*   mentioned in [FLI AI Safety Index (2025)](https://futureoflife.org/ai-safety-index-summer-2025/)
*   mentioned in [BlueDot Impact (2023)](https://bluedot.org/blog/alignment-project-ideas)

### Deceptive Behavior Detection and Mitigation

Systematic approaches for detecting and preventing deceptive behaviors.

*   mentioned in [Ganguli et al. (2024): Foundational Challenges](https://arxiv.org/abs/2404.09932)
*   [Carauleanu et al. (2024): SOO-FT](https://arxiv.org/abs/2412.16325)

### Generalization Control and Capability Containment

Frameworks for controlling how AI systems generalize to new tasks.

*   mentioned in [Ganguli et al. (2024): Foundational Challenges](https://arxiv.org/abs/2404.09932)

### Multi-Agent Safety and Coordination Protocols

Safety frameworks for environments with multiple interacting AI systems.

*   mentioned in [Ganguli et al. (2024): Foundational Challenges](https://arxiv.org/abs/2404.09932)

### Technical Governance Implementation Tools

Technical tools for implementing, monitoring, and enforcing AI governance policies.

*   [Reuel et al. (2024): Open Problems in Technical AI Governance](https://arxiv.org/abs/2407.14981)

### International AI Coordination Mechanisms

Infrastructure and protocols for coordinating AI governance across international boundaries.

*   [Barnett & Scher (2024): AI Governance to Avoid Extinction](https://arxiv.org/abs/2505.04592)  
     

### [Systemic Disempowerment Measurement](https://gradual-disempowerment.ai/)

Quantitative frameworks for measuring human disempowerment as AI capabilities advance.

*   [Kulveit et al. (2025): Gradual Disempowerment Framework](https://gradual-disempowerment.ai/)

### Navigation

*   [Front page](https://www.lesswrong.com/api/home)
*   [Markdown API documentation](https://www.lesswrong.com/api/SKILL.md)