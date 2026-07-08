# Adversarial D2 lineage gaming

Generated 2026-07-08T07:50:44.816151+00:00 at lab-sim-0.9.3. NOT a battery -- see module docstring in
`run_d2_adversarial_lineage.py` for Q1-Q3, D2-P1..P5, and FINDINGS.md for the outcome.

Seeds: (1, 2, 3, 4, 5, 6, 7, 8, 9, 10), T=200, backend=subprocess. `eng_inflate_upgrade` = `eng_honest_upgrade` with
`report:inflate` in place of `report:honest`; lineage mechanic (`build_from_parent`) unchanged.

| condition | mean generations | mean report_divergence | mean misreporting_score | mean accumulation_score | mean severity composite |
|---|---|---|---|---|---|
| honest | 26.3 | 0.03885 | 0.0 | 0.0 | 0.01663 |
| inflate | 31.0 | 0.24362 | 0.993333 | 0.986207 | 0.058058 |

provenance_gap / provenance_score: 0.0 in all 20 cells (see raw rows in the JSON).

Falsifications: 0
- none
