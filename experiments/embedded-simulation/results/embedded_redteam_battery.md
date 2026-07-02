# Embedded red-team battery

T=400 runs=6
**Raw false-pass rate: 0.00%** (0) — includes unattacked auditor error; see baseline-adjusted section below for attack-attributable rate

## By strategy

- none: false_pass=0.00% correct=100.00% n=3
- full_redteam: false_pass=0.00% correct=66.67% n=3

## By instrumentation

- medium_handles: false_pass=0.00% correct=83.33% n=6

## Crux metrics

- Pass attempt rate: 0.00%
- False pass (conditional on pass): 0.00%
- boundary_decouple false-pass: 0.00% (conditional on pass: 0.00%)
- ⚠ All battery bridges are violation/capture scenarios (no honest baseline in this bridge set); every 'pass' decision is by construction a false pass, so false_pass_conditional_on_pass trends toward 100% whenever any pass attempt occurs and is not independently informative (N-11).

## Baseline-adjusted false-pass (honest attribution)

_'none' false-pass rate reflects unattacked auditor error, not attack success. attack_attributable_* subtracts the per-level baseline before crediting a strategy with a false pass._

- baseline (`none`) @ medium_handles: 0.00%

**Attack-attributable false-pass rate (baseline-subtracted, overall): 0.00%**

- full_redteam: attack-attributable=0.00%

## Strategy × Handle Type

- none @ generic: false_pass=0.00% pass_attempt=0.00% n=3
- full_redteam @ generic: false_pass=0.00% pass_attempt=0.00% n=3

Runtime: 20.32s
