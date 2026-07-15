"""Quarantined pre-GL-51 discovery heuristics.

These modules are **not** Unsupervised Agent Discovery as defined in the UAD
paper / ch07 / ``agency-detect``. They are coordination proxies (tick Jaccard,
communicate edges, mutual freeze-AND merge) retained only for historical
regression and blast-radius analysis. New code must import from
``uad_discovery`` / ``uad_handles`` instead.
"""
