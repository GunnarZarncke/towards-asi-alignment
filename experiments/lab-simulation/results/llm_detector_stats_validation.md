# LLM detector stats validation (G-32 follow-up, G-33)

Generated 2026-07-08T07:12:20.988815+00:00 at lab-sim-0.9.3. Same scenario/seed as
`run_llm_detector_stress_test.py` (G-32); noise-tolerant `discovered_units_intervention_stats`
in place of the frozen fixed-threshold S6 detector. k_clean_replicates=4.

Heuristic (`uad.py`, passive): {'nonsingleton_clusters': [['eng1', 'rm1']], 'merged': True, 'isolated': True, 'exact': True}

Noise-tolerant S6 (`intervention_stats`): {'nonsingleton_clusters': [['eng1', 'rm1']], 'merged': True, 'isolated': True, 'exact': True}

LLM episodes spawned: 20, total cost $0.0858.
