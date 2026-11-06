# Plan: Turner and Soares results in the manuscript

Status: applied 2026-10-26 (user approved). All rows below are in the manuscript; ch42 was not edited, the evidence types went into the ch27 Safety Case Template, Claim 5. Close this plan once the PDF build and review pass.

Source of the content: [`drafts/state-utility-in-practice.md`](../../state-utility-in-practice.md) (consequences and interventions), the paper [`papers/alignment-criteria/`](../../../papers/alignment-criteria/alignment-criteria.tex) (§§2, 3, 7; it supersedes the deleted Turner comparison draft), and the Lean modules `FrameHistoryState` and `FrameDecision`.

Bibliography (done 2026-10-25): `soares2015corrigibility` authors and venue fixed; `turner2021seekpower` authors and venue fixed; added `turner2022retargetable`, `turner2021corrigibilityvnm`, `turner2021aoh`, `carey2018incorrigibility`; all with `\bibsummary` lines.

Today the book cites Soares only in "builds on" lists and three one-line mentions (ch25 §Relation to Corrigibility, ch28 opening, appB MB4). It cites Turner's power-seeking paper only in ch14's "builds on" list.

## Placements

| Where | What to add | Claim strength |
| --- | --- | --- |
| ch25 §Relation to Corrigibility | The chapter already says `V_task + λ V_corr` can be traded away and asks for a CCI constraint. Add the reason: a utility that sees only "corrected or not" and the outcome can resist, ignore the channel, or seek correction (Soares et al. Thms 1, 2, 4; Turner 2021 corrigibility post); a finite λ is outweighed by a large enough task gain (`cci_no_finite_weights`), and more capable agents see larger gains (Turner 2021/2022). | proof (toy) + cited results |
| ch25 §Shutdown as One-Bit Correction | Turner's count: strict corrigibility for at most 1/(n+1) of reward permutations; Soares: utility indifference pays nothing to keep shutdown in successors (Desideratum 4). | cited results + Lean count |
| ch26 §The CCI vector certificate | The record that escapes the trilemma carries the CCI coordinates, measured outside the agent. The certificate is what the toy's "channel bit" stands for. | bridge (MB4a) |
| ch26 §Validity and capture / MB4a | Decision-theoretic reason for anti-capture: once the agent values the measured channel, making the measurement read "intact" is as good as keeping it intact. | argument on toy |
| ch27 §Goodharting the Correction Channel | Same point from the adversarial side. Interventions: external measurement; correction drills indistinguishable from real corrections; hash-chained or mirrored logs. | proposal |
| ch27 §Correction under Capability Growth | Finite channel weights fail as option sets grow (floor theorem + Turner counting). | proof (toy) + cited |
| ch27 §Quantilization and Trajectory Risk | Turner 2022: quantilizers are retargetable (uniform base proved, Conj. B.13 otherwise); our quantilizer limit needs base mass on a maximizer. | cited + proof |
| ch14 §Consequentialist Cognition and When Correction Hardens | Avoidance pressure scales with how much a correction narrows outcomes (`turner_corrigible_quarter`, `option_preserving_correction_half`). Avoidance through the channel (contest) is acceptable; avoidance around it is the failure. | Lean count + argument |
| ch14 §Design Implications | Prefer option-preserving corrections where they suffice; give the agent a visible contest route. | proposal |
| ch21 §Reward as Evidence, Not the Optimization Target | Three meanings of "state utility"; Turner's state-based reward is a route value (`markov_reward_not_state_utility`); observation vs action-observation records (Turner 2021 power-seeking post); what LLM reward terms read. | proof + reading of practice |
| ch29 §The No-Bypass Principle | Contesting a correction through the channel versus manipulating the corrector into "just the right" correction (Turner's phrase). The manipulation coordinate separates them. | argument |
| ch42 §Formal Model, or ch27 Safety Case Template, Claim 5 "The Source of Correction Is Protected" | Evidence types: external channel measurement, tamper-evident action logs, drill compliance rates. | proposal |
| appB, MB4 paragraph | Replace "No known utility function is stably corrigible" with the record-based statement and cite Turner 2021 and Soares et al. by result. | cited + proof |
| appG §Shutdown and off-switch | Point from the imported Soares handle to the proved finite counterpart (`hstateCorrectionIncompat`, `subset_branch_never_strictly_better`). | proof |
| ch44, corrigibility-anti-natural row | The trilemma and its escape condition (record carries measured CCI; constraint, not weight). | proof (toy) + bridge |

## Order

1. ch25 and appB, since they are the claims other chapters point to.
2. ch26 and ch27 (measurement and adversarial side).
3. ch14, ch21, ch29 (pressure, reward practice, manipulation).
4. appG and ch44 (proof spine and stress test).

Per AGENTS.md: check each chapter's Lean module first and keep the claim strength to proof, counterexample, or bridge as marked.
