#!/usr/bin/env python3
"""Import bibliography entries from source-map sibling repos.

Reads .bib files referenced by canonical TeX papers in ../agency-detect and
../brain-to-values, deduplicates by citation key, categorizes entries, and
writes references/*.bib for the book.

Chapter-indexed LessWrong references in context/lw-references.md are NOT
imported here; add those to references/*.bib manually (see INSTRUCTIONS.md §7).

Run from repo root: python3 scripts/import_source_map_refs.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENCY = ROOT.parent / "agency-detect" / "docs" / "papers"
BRAIN = ROOT.parent / "brain-to-values" / "papers"
REFS = ROOT / "references"

ENTRY_RE = re.compile(r"@\w+\{[^@]+", re.DOTALL)
KEY_RE = re.compile(r"@(\w+)\{([^,\s]+),")
AUTHOR_RE = re.compile(r"author\s*=\s*\{([^}]+)\}", re.IGNORECASE)
TITLE_RE = re.compile(r"title\s*=\s*\{([^}]+)\}", re.IGNORECASE)

# Canonical .bib paths from metadata/source-canon.md source map
SOURCE_BIBS = [
    AGENCY / "refs.bib",
    AGENCY / "uad-literature-review" / "uad_literature_review.bib",
    BRAIN / "value-bundle-drift" / "value-bundle-drift.bib",
    BRAIN / "unit-of-caring" / "unit-of-caring.bib",
    BRAIN / "loop-hub-control-value" / "lhcv-model-v2.bib",
    BRAIN / "free-energy-loops" / "refs.bib",
    BRAIN / "free-energy-loops" / "refs-supplement.bib",
    BRAIN / "status-regulation-loops" / "status_regulation_as_free_energy_loops.bib",
    BRAIN / "consciousness-agency-backbone" / "refs.bib",
]

# Internal project papers (source map) not always present as standalone .bib entries
INTERNAL_PAPERS = """
@techreport{zarncke2025uad,
  author      = {Zarncke, Gunnar},
  title       = {Foundations of Unsupervised Agent Discovery in Raw Dynamical Systems},
  institution = {AE Studio},
  year        = {2025},
  note        = {Source: ../agency-detect/docs/papers/unsupervised-agent-discovery/; extract: context/extracts/unsupervised-agent-discovery.md},
}

@techreport{zarncke2025biq,
  author      = {Zarncke, Gunnar},
  title       = {Bitwise Intelligence: A Blanket-Information Measure of Competence},
  institution = {AE Studio},
  year        = {2025},
  note        = {Source: ../agency-detect/docs/papers/bitwise-iq/; extract: context/extracts/bitwise-iq.md},
}

@techreport{zarncke2025attractor,
  author      = {Zarncke, Gunnar},
  title       = {Attractor Basins of Cooperation, Privacy, and Parasite Persistence},
  institution = {AE Studio},
  year        = {2025},
  note        = {Source: ../agency-detect/docs/papers/attractor-basins/; extract: context/extracts/attractor-basins.md},
}

@techreport{zarncke2025acausal,
  author      = {Zarncke, Gunnar},
  title       = {A Formalization of Acausal Trade on Top of Unsupervised Agent Discovery},
  institution = {AE Studio},
  year        = {2025},
  note        = {Source: ../agency-detect/docs/papers/acausal-trade-uad-formalization/; extract: context/extracts/acausal-trade-uad-formalization.md},
}

@techreport{zarncke2025endogenized,
  author      = {Zarncke, Gunnar},
  title       = {Endogenized Intentional Stance: Predictive Compression and Goal-Rational Priors},
  institution = {AE Studio},
  year        = {2025},
  note        = {Source: ../agency-detect/docs/papers/endogenized-intentional-stance/; extract: context/extracts/endogenized-intentional-stance.md},
}

@techreport{zarncke2025preference,
  author      = {Zarncke, Gunnar},
  title       = {Preference vs. Capability: Value-Conditioned Prediction and Control Channels},
  institution = {AE Studio},
  year        = {2025},
  note        = {Source: ../agency-detect/docs/papers/preference-capability/; extract: context/extracts/preference-capability.md},
}

@techreport{zarncke2025construction,
  author      = {Zarncke, Gunnar},
  title       = {Construction Without Understanding: Successor Agents and the Limits of Copying},
  institution = {AE Studio},
  year        = {2025},
  note        = {Source: ../agency-detect/docs/papers/construction-without-understanding/; extract: context/extracts/construction-without-understanding.md},
}

@techreport{zarncke2026access,
  author      = {Zarncke, Gunnar},
  title       = {Handles Before Interventions: Access-Model UAD and the Embedded Semantics of Agency Tests},
  institution = {AE Studio},
  year        = {2026},
  note        = {Source: ../agency-detect/docs/papers/access-uad/; extract: context/extracts/access-uad.md},
}

@techreport{zarncke2026smoothing,
  author      = {Zarncke, Gunnar},
  title       = {Recoverability of Smoothed Agent Boundaries in Unsupervised Agent Discovery},
  institution = {AE Studio},
  year        = {2026},
  note        = {Source: ../agency-detect/docs/papers/smooth-uad/; extract: context/extracts/smooth-uad.md},
}

@techreport{zarncke2026stealth,
  author      = {Zarncke, Gunnar},
  title       = {Stealth--Capability Bounds for Multi-Resolution Unsupervised Agent Discovery},
  institution = {AE Studio},
  year        = {2026},
  note        = {Source: ../agency-detect/docs/papers/stealth-capability-bounds/; extract: context/extracts/stealth-capability-bounds.md},
}

@techreport{zarncke2025loop-hub-value,
  author      = {Zarncke, Gunnar},
  title       = {Loop--Hub--Value Model: From Free-Energy Loops to Intrinsic Values},
  institution = {AE Studio},
  year        = {2025},
  note        = {Source: ../brain-to-values/papers/loop-hub-value-model/; extract: context/extracts/loop-hub-value-model.md},
}

@techreport{zarncke2025lhcv,
  author      = {Zarncke, Gunnar},
  title       = {Loop--Hub--Control--Value Model v2},
  institution = {AE Studio},
  year        = {2025},
  note        = {Source: ../brain-to-values/papers/loop-hub-control-value/; extract: context/extracts/lhcv-model-v2.md},
}

@techreport{zarncke2025unit-of-caring,
  author      = {Zarncke, Gunnar},
  title       = {Unit of Caring: Architecture, Suffering, and Cross-Scale Aggregation},
  institution = {AE Studio},
  year        = {2025},
  note        = {Source: ../brain-to-values/papers/unit-of-caring/; extract: context/extracts/unit-of-caring.md},
}

@techreport{zarncke2025value-bundle-drift,
  author      = {Zarncke, Gunnar},
  title       = {Value Bundle Drift},
  institution = {AE Studio},
  year        = {2025},
  note        = {Source: ../brain-to-values/papers/value-bundle-drift/; extract: context/extracts/value-bundle-drift.md},
}

@techreport{zarncke2025status-regulation,
  author      = {Zarncke, Gunnar},
  title       = {Status Regulation as Free-Energy Loops},
  institution = {AE Studio},
  year        = {2025},
  note        = {Source: ../brain-to-values/papers/status-regulation-loops/; extract: context/extracts/status-regulation-as-free-energy-loops.md},
}

@techreport{zarncke2025consciousness-backbone,
  author      = {Zarncke, Gunnar},
  title       = {Consciousness and Agency Backbone: A Minimal Operational Stack},
  institution = {AE Studio},
  year        = {2025},
  note        = {Source: ../brain-to-values/papers/consciousness-agency-backbone/; extract: context/extracts/consciousness-agency-backbone.md},
}

@misc{zarncke2025alignment-attractor,
  author       = {Zarncke, Gunnar},
  title        = {Alignment Attractor: Executive Summary and Platform Framing},
  year         = {2025},
  howpublished = {Internal project note},
  note         = {Source: context/Alignment Attractor.md},
}

@misc{zarncke2025uad-review,
  author       = {Zarncke, Gunnar},
  title        = {UAD Literature Review},
  year         = {2025},
  note         = {Source: ../agency-detect/docs/papers/uad-literature-review/; extract: context/extracts/uad-literature-review.md},
}

@misc{zarncke2026rainbow,
  author = {Zarncke, Gunnar},
  title  = {Rainbow Parameterization: Separable Dimensions of Bandwidth, Opacity, Recursion, and Self-Bottleneck Strength},
  year   = {2026},
  note   = {Manuscript in preparation, companion to this research program}
}

@misc{zarncke2026value-bottleneck,
  author = {Zarncke, Gunnar},
  title  = {Value Learning Needs a Low-Dimensional Bottleneck},
  year   = {2026},
  note   = {Manuscript in preparation, brain-to-values research program}
}
"""

# Manual thebibliography entries from papers without .bib files
MANUAL_ENTRIES = """
@book{dennett1987intentional,
  author    = {Dennett, Daniel C.},
  title     = {The Intentional Stance},
  publisher = {MIT Press},
  address   = {Cambridge, MA},
  year      = {1987},
}

@misc{mcgregor2025intentional,
  author        = {McGregor, Sean and others},
  title         = {Formalising the Intentional Stance I: Attributing Goals and Beliefs to Stochastic Processes},
  year          = {2025},
  eprint        = {2405.16490},
  archiveprefix = {arXiv},
  primaryclass  = {cs.AI},
}

@book{vonneumann1966,
  author    = {von Neumann, John},
  title     = {Theory of Self-Reproducing Automata},
  editor    = {Burks, Arthur W.},
  publisher = {University of Illinois Press},
  address   = {Urbana},
  year      = {1966},
}

@incollection{burks1969,
  author    = {Burks, Arthur W.},
  title     = {Von Neumann's Self-Reproducing Automata},
  booktitle = {Essays on Cellular Automata},
  publisher = {University of Illinois Press},
  address   = {Urbana},
  year      = {1969},
}

@article{pesavento1995,
  author  = {Pesavento, Umberto},
  title   = {An Implementation of von Neumann's Self-Reproducing Machine},
  journal = {Artificial Life},
  volume  = {2},
  number  = {4},
  pages   = {337--354},
  year    = {1995},
}

@article{eigen1971,
  author  = {Eigen, Manfred},
  title   = {Selforganization of Matter and the Evolution of Biological Macromolecules},
  journal = {Naturwissenschaften},
  volume  = {58},
  pages   = {465--523},
  year    = {1971},
  doi     = {10.1007/BF00623322},
}

@book{maturana1980,
  author    = {Maturana, Humberto R. and Varela, Francisco J.},
  title     = {Autopoiesis and Cognition: The Realization of the Living},
  publisher = {Reidel},
  address   = {Dordrecht},
  year      = {1980},
}

@article{smithszathmary1995nature,
  author  = {Szathm{\'a}ry, E{\"o}rs and Smith, John Maynard},
  title   = {The Major Evolutionary Transitions},
  journal = {Nature},
  volume  = {374},
  pages   = {227--232},
  year    = {1995},
  doi     = {10.1038/374227a0},
}

@book{smithszathmary1995book,
  author    = {Maynard Smith, John and Szathm{\'a}ry, E{\"o}rs},
  title     = {The Major Transitions in Evolution},
  publisher = {Oxford University Press},
  address   = {Oxford},
  year      = {1995},
}

@incollection{griesemer2000,
  author    = {Griesemer, James R.},
  title     = {Reproduction and the Reduction of Genetics},
  booktitle = {The Concept of the Gene in Development and Evolution},
  publisher = {Cambridge University Press},
  address   = {Cambridge},
  pages     = {240--285},
  year      = {2000},
}

@article{griesemer2016,
  author  = {Griesemer, James R.},
  title   = {Reproduction in Complex Life Cycles: Toward a Developmental Reaction Norms Perspective},
  journal = {Philosophy of Science},
  volume  = {83},
  number  = {5},
  pages   = {803--815},
  year    = {2016},
}

@article{szostak2001,
  author  = {Szostak, Jack W. and Bartel, David P. and Luisi, Pier Luigi},
  title   = {Synthesizing Life},
  journal = {Nature},
  volume  = {409},
  pages   = {387--390},
  year    = {2001},
  doi     = {10.1038/35053176},
}

@article{hordijk2010,
  author  = {Hordijk, Wim and Steel, Mike},
  title   = {Autocatalytic Sets and the Origin of Life},
  journal = {Entropy},
  volume  = {12},
  number  = {7},
  pages   = {1733--1742},
  year    = {2010},
}

@inproceedings{bertschinger2008,
  author    = {Bertschinger, Nils and Olbrich, Eckehard and Ay, Nihat and Jost, J{\"u}rgen},
  title     = {Information and Closure in Systems Theory},
  booktitle = {Explorations in the Complexity of Possible Life},
  year      = {2008},
}

@inproceedings{hadfieldmenell2016,
  author    = {Hadfield-Menell, Dylan and Dragan, Anca and Abbeel, Pieter and Russell, Stuart},
  title     = {Cooperative Inverse Reinforcement Learning},
  booktitle = {Advances in Neural Information Processing Systems},
  year      = {2016},
}

@inproceedings{christiano2017,
  author    = {Christiano, Paul F. and Leike, Jan and Brown, Tom B. and others},
  title     = {Deep Reinforcement Learning from Human Preferences},
  booktitle = {Advances in Neural Information Processing Systems},
  year      = {2017},
}

@misc{rafailov2023,
  author        = {Rafailov, Rafael and Sharma, Archit and Baevski, Alexei and others},
  title         = {Direct Preference Optimization: Your Language Model is Secretly a Reward Model},
  year          = {2023},
  eprint        = {2305.18290},
  archiveprefix = {arXiv},
  primaryclass  = {cs.LG},
}

@misc{yao2023,
  author        = {Yao, Shunyu and Zhao, Jeffrey and Yu, Dian and others},
  title         = {ReAct: Synergizing Reasoning and Acting in Language Models},
  year          = {2023},
  eprint        = {2210.03629},
  archiveprefix = {arXiv},
  primaryclass  = {cs.CL},
}

@misc{schick2023,
  author        = {Schick, Timo and Dwivedi-Yu, Jane and others},
  title         = {Toolformer: Language Models Can Teach Themselves to Use Tools},
  year          = {2023},
  eprint        = {2302.04761},
  archiveprefix = {arXiv},
  primaryclass  = {cs.CL},
}

@misc{nakano2021,
  author        = {Nakano, Reiichiro and Hilton, Jacob and Balaji, Suchir and others},
  title         = {WebGPT: Browser-Assisted Question-Answering with Human Feedback},
  year          = {2021},
  eprint        = {2112.09332},
  archiveprefix = {arXiv},
  primaryclass  = {cs.CL},
}

@misc{ahn2022,
  author        = {Ahn, Michael and Brohan, Anthony and others},
  title         = {Do As I Can, Not As I Say: Grounding Language in Robotic Affordances},
  year          = {2022},
  eprint        = {2204.01691},
  archiveprefix = {arXiv},
  primaryclass  = {cs.RO},
}

@misc{driess2023,
  author        = {Driess, Danny and others},
  title         = {PaLM-E: An Embodied Multimodal Language Model},
  year          = {2023},
  eprint        = {2303.03378},
  archiveprefix = {arXiv},
  primaryclass  = {cs.LG},
}

@misc{levine2018,
  author        = {Levine, Sergey},
  title         = {Reinforcement Learning and Control as Probabilistic Inference: Tutorial and Review},
  year          = {2018},
  eprint        = {1805.00995},
  archiveprefix = {arXiv},
  primaryclass  = {cs.LG},
}

@misc{hafner2019,
  author        = {Hafner, Danijar and Lillicrap, Timothy and Fischer, Ian and others},
  title         = {Learning Latent Dynamics for Planning from Pixels},
  year          = {2019},
  eprint        = {1811.07428},
  archiveprefix = {arXiv},
  primaryclass  = {cs.LG},
}

@misc{hafner2023,
  author        = {Hafner, Danijar and Pasukonis, Jurgis and others},
  title         = {Mastering Diverse Domains through World Models},
  year          = {2023},
  eprint        = {2301.04104},
  archiveprefix = {arXiv},
  primaryclass  = {cs.LG},
}

@inproceedings{jaques2019,
  author    = {Jaques, Natasha and others},
  title     = {Social Influence as Intrinsic Motivation for Multi-Agent Deep Reinforcement Learning},
  booktitle = {International Conference on Machine Learning},
  year      = {2019},
}

@article{salgepolani2014,
  author  = {Salge, Christoph and Polani, Daniel},
  title   = {Empowerment as Replacement for the Three Laws of Robotics},
  journal = {Frontiers in Robotics and AI},
  volume  = {2},
  pages   = {27},
  year    = {2014},
}

% LessWrong / Alignment Forum posts curated in context/lw-references.md.
% Mirror of the manual block in references/external-alignment.bib; kept here so
% regeneration does not drop them. Keep the two copies in sync.

@misc{critch2022boundaries,
  author       = {Critch, Andrew},
  title        = {Boundaries, Part 1: A Key Missing Concept from Utility Theory},
  year         = {2022},
  howpublished = {\\url{https://www.lesswrong.com/posts/8oMF8Lv5jiGaQSFvo/boundaries-part-1-a-key-missing-concept-from-utility-theory}},
  note         = {LessWrong post. Argues that agent/environment boundaries (membranes) are a primitive missing from utility theory and bargaining.}
}

@misc{critch2022boundaries3a,
  author       = {Critch, Andrew},
  title        = {Boundaries, Part 3a: Defining Boundaries as Directed Markov Blankets},
  year         = {2022},
  howpublished = {\\url{https://www.lesswrong.com/posts/HrtqLy46Fx7xqRrMo/boundaries-part-3a-defining-boundaries-as-directed-markov}},
  note         = {LessWrong post. Formalizes boundaries as directed Markov blankets.}
}

@misc{lakin2023boundaries,
  author       = {Lakin, Chris},
  title        = {Formalizing Boundaries with Markov Blankets},
  year         = {2023},
  howpublished = {\\url{https://www.lesswrong.com/posts/z4o4iAFgnmaBmksN2/formalizing-boundaries-with-markov-blankets}},
  note         = {LessWrong post. Compact Markov-blanket formalization of the boundaries idea.}
}

@misc{christiano2019failure,
  author       = {Christiano, Paul},
  title        = {What Failure Looks Like},
  year         = {2019},
  howpublished = {\\url{https://www.lesswrong.com/posts/HBxe6wdjxK239zajf/what-failure-looks-like}},
  note         = {LessWrong post. Gradual, distributed loss of human control with no discrete hostile agent to align.}
}

@misc{critch2021multipolar,
  author       = {Critch, Andrew},
  title        = {What Multipolar Failure Looks Like, and Robust Agent-Agnostic Processes},
  year         = {2021},
  howpublished = {\\url{https://www.lesswrong.com/posts/LpM3EAakwYdS6aRKf/what-multipolar-failure-looks-like-and-robust-agent-agnostic}},
  note         = {LessWrong post. Catastrophe from distributed human-AI systems and robust agent-agnostic processes rather than a single rogue agent.}
}

@misc{shlegeris2023aicontrol,
  author       = {Shlegeris, Buck and Roger, Fabien and Greenblatt, Ryan and Sachan, Kshitij},
  title        = {AI Control: Improving Safety Despite Intentional Subversion},
  year         = {2023},
  howpublished = {\\url{https://www.lesswrong.com/posts/d9FJHawgkiMSPjagR/ai-control-improving-safety-despite-intentional-subversion}},
  note         = {LessWrong post. Seeks safety guarantees under the assumption that the model may intentionally subvert oversight.}
}

@misc{thornley2023shutdown,
  author       = {Thornley, Elliott},
  title        = {The Shutdown Problem: An AI Engineering Puzzle for Decision Theorists},
  year         = {2023},
  howpublished = {\\url{https://www.lesswrong.com/posts/8GWLRMnp55iFZDBbm/the-shutdown-problem-three-theorems}},
  note         = {LessWrong post. Formalizes the tension between shutdownability and competent goal pursuit.}
}

@misc{yudkowsky2009valuefragile,
  author       = {Yudkowsky, Eliezer},
  title        = {Value is Fragile},
  year         = {2009},
  howpublished = {\\url{https://www.lesswrong.com/posts/GNnHHmm8EzePmKzPk/value-is-fragile}},
  note         = {LessWrong post. Futures not shaped by detailed inheritance from human values may contain little of value.}
}

@misc{yudkowsky2007wishes,
  author       = {Yudkowsky, Eliezer},
  title        = {The Hidden Complexity of Wishes},
  year         = {2007},
  howpublished = {\\url{https://www.lesswrong.com/posts/4ARaTpNX62uaL86j6/the-hidden-complexity-of-wishes}},
  note         = {LessWrong post. Apparently simple wishes hide many tacit human value constraints.}
}

@misc{yudkowsky2011cevdynamic,
  author       = {Yudkowsky, Eliezer},
  title        = {In Favour of a Selective CEV Initial Dynamic},
  year         = {2011},
  howpublished = {\\url{https://www.lesswrong.com/posts/u8isNgN7rRYBZ35rQ/in-favour-of-a-selective-cev-initial-dynamic}},
  note         = {LessWrong post. Coherent extrapolated volition as what humanity would want under more knowledge, reflection, and coherence.}
}

@misc{wentworth2020pointers,
  author       = {Wentworth, John},
  title        = {The Pointers Problem: Human Values Are A Function Of Humans' Latent Variables},
  year         = {2020},
  howpublished = {\\url{https://www.lesswrong.com/posts/gQY6LrTWJNkTv8YJR/the-pointers-problem-human-values-are-a-function-of-humans}},
  note         = {LessWrong post. Human values as functions of latent variables inside human world-models rather than low-level physical states.}
}

@misc{wentworth2021selection,
  author       = {Wentworth, John},
  title        = {Selection Theorems: A Program For Understanding Agents},
  year         = {2021},
  howpublished = {\\url{https://www.lesswrong.com/posts/G2Lne2Fi7Qra5Lbuf/selection-theorems-a-program-for-understanding-agents}},
  note         = {LessWrong post. Studies what internal structures selection pressure tends to produce in agents.}
}

@misc{wentworth2022agentstructure,
  author       = {Wentworth, John},
  title        = {Clarifying the Agent-Like Structure Problem},
  year         = {2022},
  howpublished = {\\url{https://www.lesswrong.com/posts/moi3cFY2wpeKGu9TT/clarifying-the-agent-like-structure-problem}},
  note         = {LessWrong post. Distinguishes behavioral equivalence from internal agent-like structure.}
}

@misc{kulveit2025pando,
  author       = {Kulveit, Jan},
  title        = {The Pando Problem: Rethinking AI Individuality},
  year         = {2025},
  howpublished = {\\url{https://www.lesswrong.com/posts/wQKskToGofs4osdJ3/the-pando-problem-rethinking-ai-individuality}},
  note         = {LessWrong post. AI individuality may be fluid, distributed, copied, or clonal rather than unitary.}
}

@misc{hubinger2023modelorganisms,
  author       = {Hubinger, Evan and Schiefer, Nicholas and Denison, Carson and Perez, Ethan},
  title        = {Model Organisms of Misalignment: The Case for a New Pillar of Alignment Research},
  year         = {2023},
  howpublished = {\\url{https://www.lesswrong.com/posts/ChDH335ckdvpxXaXX/model-organisms-of-misalignment-the-case-for-a-new-pillar-of-1}},
  note         = {LessWrong post. Controlled in-vitro demonstrations of misalignment mechanisms such as deceptive alignment.}
}

@misc{yudkowsky2022agiruin,
  author       = {Yudkowsky, Eliezer},
  title        = {AGI Ruin: A List of Lethalities},
  year         = {2022},
  howpublished = {\\url{https://www.lesswrong.com/posts/uMQ3cqWDPHhjtiesc/agi-ruin-a-list-of-lethalities}},
  note         = {LessWrong post. Canonical enumeration of reasons alignment may fail under capability growth.}
}

@misc{soares2022sharpleftturn,
  author       = {Soares, Nate},
  title        = {A Central AI Alignment Problem: Capabilities Generalization, and the Sharp Left Turn},
  year         = {2022},
  howpublished = {\\url{https://www.lesswrong.com/posts/GNhMPAWcfBCASy8e6/a-central-ai-alignment-problem-capabilities-generalization}},
  note         = {LessWrong post. Capabilities may generalize sharply while alignment properties fail to generalize.}
}

@misc{christiano2018corrigibility,
  author       = {Christiano, Paul},
  title        = {Corrigibility},
  year         = {2018},
  howpublished = {\\url{https://www.lesswrong.com/posts/fkLYhTQteAu5SinAc/corrigibility}},
  note         = {LessWrong post. Corrigibility as preserving the ability to correct and manage drift through capability amplification.}
}

@misc{soares2022hardbits,
  author       = {Soares, Nate},
  title        = {On How Various Plans Miss the Hard Bits of the Alignment Challenge},
  year         = {2022},
  howpublished = {\\url{https://www.lesswrong.com/posts/3pinFH3jerMzAvmza/on-how-various-plans-miss-the-hard-bits-of-the-alignment}},
  note         = {LessWrong post. Argues many alignment plans fail because they do not survive the sharp left turn.}
}
"""

# Alias keys used in source papers -> canonical keys in this bibliography
ALIASES = {
    "ZarnckeUAD": "zarncke2025uad",
    "ZarnckeBIQ": "zarncke2025biq",
    "ZarnckeAttractors": "zarncke2025attractor",
    "ZarnckeAcausal": "zarncke2025acausal",
    "uad2025": "zarncke2025uad",
    "biq2025": "zarncke2025biq",
    "eis2025": "zarncke2025endogenized",
    "abc2025": "zarncke2025attractor",
    "ConantAshby1970": "conant1970regulator",
    "Friston2010": "friston2010free",
    "Kirchhoff2018": "kirchhoff2018markov",
    "NgRussell2000": "ng2000irl",
    "Ziebart2008": "ziebart2008maxent",
    "Hamilton1964": "hamilton1964genetical",
    "Tishby2000IB": "tishby2000ib",
    "Bialek2001": "bialek2001predictability",
    "ShaliziCrutchfield2001": "shalizi2001computational",
    "Klyubin2005": "klyubin2005empowerment",
    "SalgePolani2014": "salgepolani2014",
    "HadfieldMenell2016": "hadfieldmenell2016",
    "Christiano2017": "christiano2017",
    "Rafailov2023": "rafailov2023",
    "Yao2023": "yao2023",
    "Schick2023": "schick2023",
    "Nakano2021": "nakano2021",
    "Ahn2022": "ahn2022",
    "Driess2023": "driess2023",
    "Levine2018": "levine2018",
    "Hafner2019": "hafner2019",
    "Hafner2023": "hafner2023",
    "Jaques2019": "jaques2019",
    "Dennett1987": "dennett1987intentional",
    "Dennett1991": "dennett1991consciousness",
    "Dehaene2014": "dehaene2014consciousness",
}

INTERNAL_KEYS = {
    "zarncke2025uad",
    "zarncke2025biq",
    "zarncke2025attractor",
    "zarncke2025acausal",
    "zarncke2025endogenized",
    "zarncke2025preference",
    "zarncke2025construction",
    "zarncke2026access",
    "zarncke2026smoothing",
    "zarncke2026stealth",
    "zarncke2025loop-hub-value",
    "zarncke2025lhcv",
    "zarncke2025unit-of-caring",
    "zarncke2025value-bundle-drift",
    "zarncke2025stratification",
    "zarncke2025status-regulation",
    "zarncke2025consciousness-backbone",
    "zarncke2025alignment-attractor",
    "zarncke2025uad-review",
    "zarncke2026rainbow",
    "zarncke2026value-bottleneck",
}

ALIGNMENT_PATTERNS = re.compile(
    r"alignment|reinforcement learning|inverse reinforcement|decision theory|"
    r"existential safety|human compatible|learned optimization|lethal|"
    r"preference optim|rlhf|cirl|reward model|language model|world model|"
    r"toolformer|react:|webgpt|arch(es)?|yudkowsky|soares|garrabrant|"
    r"functional decision|timeless decision|logical induction|"
    r"deep active inference|alignment problem",
    re.IGNORECASE,
)

NEURO_PATTERNS = re.compile(
    r"pain|suffer|neuro|brain|cortex|dopamin|fmri|qaly|daly|nocicept|"
    r"metacogn|insula|hippocamp|thalam|hypothalam|salience network|"
    r"free.?energy|active inference|predictive cod|homeostas|allostat|"
    r"cholinerg|serotonin|oxytocin|immune|circadian|vestibular|"
    r"working memory|attention|curiosity|mirror.?neuron|status|prestige|"
    r"aggression|trust|rejection hurt|basal ganglia|precuneus|"
    r"neuromodul|glial|metabolic coupling|periaqueductal|"
    r"health outcome|burden of disease|happiness report|iasp|"
    r"empowerment as replacement|warm-sensitive|saccade|"
    r"loop-hub|hub-control|stratification",
    re.IGNORECASE,
)

DYNAMICAL_PATTERNS = re.compile(
    r"markov blanket|information bottleneck|transfer entropy|granger|"
    r"computational mechanics|predictive (state|information|represent)|"
    r"empowerment|inverse reinforcement|pomdp|object-centric|slot attention|"
    r"causal emerg|individuality|semantic information|bayesian mechanics|"
    r"computational mechanics|unsupervised scene|iodine|monet|"
    r"variational agent|discovering agents|agents and devices|"
    r"interpret.*pomdp|interpret.*bayesian|dynamic markov|"
    r"cooperation percolation|collective intelligence|predictability, complexity|"
    r"good regulator|information transfer|synergistic|causal loop|"
    r"autocatalytic|self-reproduc|autopoiesis|major transition|"
    r"information and closure|planning and acting in partially",
    re.IGNORECASE,
)

PHILOSOPHY_PATTERNS = re.compile(
    r"consciousness|intentional stance|intentional systems|illusionism|"
    r"panpsychism|phenomenal|integrated information|hard problem|"
    r"self-model|concept of mind|cartesian|meditations|"
    r"morals and legislation|hedonic|unit of caring|unit of carying|"
    r"ethics of what we eat|realistic monism|being no one|"
    r"social brain|algorithm feels|anosognosia|somatoparaphrenia|"
    r"split-brain|metacognition|reportability|global broadcast|"
    r"free will|autonomy|paternalism|value change|bearers of value|"
    r"formalising the intentional stance|true believers",
    re.IGNORECASE,
)

GOVERNANCE_PATTERNS = re.compile(
    r"governance|institution|regulation|policy|certification|compliance|"
    r"norm compliance|legal|ethical issues and recommendations",
    re.IGNORECASE,
)


def parse_entries(text: str) -> dict[str, str]:
    entries: dict[str, str] = {}
    for block in ENTRY_RE.findall(text):
        m = KEY_RE.match(block.strip())
        if not m:
            continue
        key = m.group(2).strip()
        entries[key] = block.strip() + "\n"
    return entries


def completeness(entry: str) -> int:
    return len(re.findall(r"^\s*\w+\s*=", entry, re.MULTILINE))


def merge_entries(all_texts: list[str]) -> dict[str, str]:
    merged: dict[str, str] = {}
    for text in all_texts:
        for key, entry in parse_entries(text).items():
            if key not in merged or completeness(entry) > completeness(merged[key]):
                merged[key] = entry
    return merged


def entry_text(entry: str) -> str:
    author = (AUTHOR_RE.search(entry) or [None, ""])[1].lower()
    title = (TITLE_RE.search(entry) or [None, ""])[1].lower()
    return f"{author} {title} {entry.lower()}"


def categorize(key: str, entry: str) -> str:
    if key in INTERNAL_KEYS or "zarncke" in entry_text(entry):
        return "internal-project-sources.bib"
    blob = entry_text(entry)
    if GOVERNANCE_PATTERNS.search(blob):
        return "governance-institutions.bib"
    if ALIGNMENT_PATTERNS.search(blob):
        return "external-alignment.bib"
    if PHILOSOPHY_PATTERNS.search(blob):
        return "philosophy.bib"
    if NEURO_PATTERNS.search(blob):
        return "neuroscience-values.bib"
    if DYNAMICAL_PATTERNS.search(blob):
        return "dynamical-systems.bib"
    # Default bucket for uncategorized technical refs
    return "dynamical-systems.bib"


def write_bib(path: Path, header: str, entries: list[str]) -> None:
    body = "\n\n".join(sorted(entries, key=lambda e: KEY_RE.search(e).group(2).lower()))  # type: ignore[union-attr]
    path.write_text(f"{header}\n\n{body}\n", encoding="utf-8")


def main() -> int:
    texts: list[str] = [INTERNAL_PAPERS, MANUAL_ENTRIES]
    missing: list[str] = []
    for bib_path in SOURCE_BIBS:
        if bib_path.is_file():
            texts.append(bib_path.read_text(encoding="utf-8", errors="replace"))
        else:
            missing.append(str(bib_path))

    merged = merge_entries(texts)

    # Drop agency-detect short keys when the book's canonical entry already exists.
    for alias, canonical in ALIASES.items():
        if alias in merged and canonical in merged:
            del merged[alias]

    # Write alias stubs pointing to canonical keys (biblatex crossref)
    for alias, canonical in ALIASES.items():
        if canonical in merged and alias not in merged:
            merged[alias] = (
                f"@misc{{{alias},\n"
                f"  crossref = {{{canonical}}},\n"
                f"  note = {{Alias for {canonical}; see source-map papers.}},\n"
                f"}}\n"
            )

    headers = {
        "internal-project-sources.bib": (
            "% Internal project sources from INSTRUCTIONS.md source map "
            "(../agency-detect, ../brain-to-values, context/)"
        ),
        "external-alignment.bib": "% AI alignment, agent foundations, and ML safety",
        "neuroscience-values.bib": (
            "% Neuroscience, moral psychology, pain/suffering, and human values"
        ),
        "dynamical-systems.bib": (
            "% Dynamical systems, information theory, agency, and representation learning"
        ),
        "governance-institutions.bib": "% Governance, institutions, and norm compliance",
        "philosophy.bib": "% Philosophy of mind, consciousness, and ethics",
    }
    buckets: dict[str, list[str]] = {name: [] for name in headers}

    for key, entry in merged.items():
        target = categorize(key, entry)
        buckets[target].append(entry)

    REFS.mkdir(exist_ok=True)
    for filename, header in headers.items():
        write_bib(REFS / filename, header, buckets[filename])

    # main.bib stays as index comment
    (REFS / "main.bib").write_text(
        "% Unified bibliography index — individual files loaded from book.tex\n"
        "% Regenerate category files: python3 scripts/import_source_map_refs.py\n",
        encoding="utf-8",
    )

    counts = {k: len(v) for k, v in buckets.items()}
    print(f"Imported {len(merged)} unique entries:")
    for name, count in sorted(counts.items()):
        print(f"  {name}: {count}")
    if missing:
        print("Warning: missing source files:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
