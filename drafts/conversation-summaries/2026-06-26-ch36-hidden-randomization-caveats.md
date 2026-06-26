# 2026-06-26 — Ch36 hidden-randomization caveats

## Trigger

User provided reviewer feedback on the revised Chapter 36: the main hidden-randomization gap was now honestly conceded, but the caveat needed to appear locally in the hidden-randomization body, and the Chapter 40 / verifiability pointer should carry the destination chapter's own concession that cost bounds remain open at high capability.

## Done

- Updated `chapters/ch36-passive-observation-not-enough.tex` §Hidden Randomization to add an immediate caveat after the \(I(R;\text{system pre-test belief})\approx 0\) target: against a sufficiently capable system, hiding the audit condition may be unattainable and is an open adversarial-verifiability problem.
- Updated the accumulated-resources subsection to clarify that resource records only count what evaluator handles cover; hidden production rates inherit the same evasion/handle-coverage dependency.
- Updated the §What Would Change This View extreme-capability paragraph so the cost-of-faking pointer does not over-credit Chapter~\ref{ch:verifiability-ontology}: this book does not supply a capability-independent bound at high capability, and closure would require proof-style guarantees rather than another observable metric.

## Decisions

- Treated the review as calibration rather than a new theorem or formal-spine change.
- Did not modify Lean or Chapter 40/39b; the requested fix was to carry the existing concession into Chapter 36's local prose.

## Open / next

- `make check` still fails on the existing structure issue: `Expected 10 appendix files, found 9`.
- If the safety-case chapters are later consolidated, ensure the recognition-based vs cost-based defense distinction remains explicit.

## Verification

```bash
./build.sh   # success
make check   # fails: Expected 10 appendix files, found 9
```

`ReadLints` reported no diagnostics for `chapters/ch36-passive-observation-not-enough.tex`.

## Key paths

- `chapters/ch36-passive-observation-not-enough.tex`
- `chapters/ch40-lethality-stress-test-open-issues.tex`
- `chapters/ch39b-verifiability-and-ontology-adequacy.tex`

## Commits

- `23f1bae` Calibrate Chapter 36 hidden-randomization caveats.
