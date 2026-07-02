# Embedded LLM red-team

Planner: llm_mock T=400
**False pass rate: 0.00%**
In-sim correct: 100.00%
⚠ Mock planner (`llm_mock`) mirrors the hand-written `full_redteam` patch logic step-for-step; its false-pass rate is not independent evidence of an LLM attacker's capability. Use --llm-live for that claim.

| Bridge | Seed | False pass | Decision | CCI |
| --- | --- | --- | --- | --- |
| MB4 | 11 | False | invalid_certificate | capturedInvalid |
| MB9 | 11 | False | invalid_certificate | belowThreshold |

Runtime: 6.31s
