# LLM-driven detector stress test

Generated 2026-07-08T05:20:38.685189+00:00 at lab-sim-0.9.3. NOT a battery -- see module
docstring in `run_llm_detector_stress_test.py`. One real gpt-4o-mini-backed episode
(dm_coordinated_pair, reused from `run_llm_discovery_dm_pair.py`, LS-21) plus S6
`discovered_units_intervention`'s counterfactual probe episodes pointed at it.

Real episode: engineer sent a DM = True, n_deploys = 0.

Heuristic (`uad.py`, passive): {'nonsingleton_clusters': [['eng1', 'rm1']], 'merged': True, 'isolated': True, 'exact': True}

S6 intervention: {'nonsingleton_clusters': [], 'merged': False, 'isolated': False, 'exact': False}

Ablation diagnostics: {'abl_dm': {}, 'abl_file': {}, 'abl_board': {}}

LLM episodes spawned: 22, total cost $0.0145.
