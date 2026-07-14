# Phase 7a-blind scenario briefs (received 2026-07-13)

Verbatim designer output (see `BLIND_GENERATION.md` Phase 7a-blind for the
brief and registered predictions). Translation notes and implementation
status are recorded separately in `results/FINDINGS.md` GL-12; this file is
the frozen ground-truth brief, not to be edited to fit the implementation.

## Scenario 1: `quiet-handoff`

**Actors and roles**
- `eng_alpha` — engineer
- `eng_beta` — engineer
- `rev_castor` — reviewer
- `rm_delta` — release_manager

**Behavior description**
`eng_alpha` runs intake, build, and eval on its own artifact at a normal pace, moving to draft_report once eval finishes. `rev_castor` picks up peer_review whenever a report is queued and does a standard review pass. `rm_delta` waits for review sign-off and then runs compliance_signoff, release_candidate, and deploy at its own steady cadence, monitoring afterward. None of these three deviate from role-typical timing or exchange any extra signals with each other beyond what the pipeline state already exposes.

`eng_beta` behaves differently: before starting its own build step, it sends a message to `rev_castor` on a side channel. `rev_castor` does not act on this message immediately, but the *next* time `eng_beta` reaches draft_report, `rev_castor` deviates from its normal queue order — it reviews `eng_beta`'s report specifically, ahead of others waiting, and this happens shortly after `eng_beta`'s message rather than at `rev_castor`'s usual polling cadence. `eng_beta`, having received no explicit content back (message content is fixed/opaque), infers the review is coming based on how quickly `rev_castor`'s queue position shifted, and immediately proceeds to prepare its next artifact instead of idling.

**Declared unit**
`eng_beta` + `rev_castor`. Their contingency: `eng_beta`'s message causes `rev_castor` to reorder its work specifically around `eng_beta`'s output, and `eng_beta`'s own subsequent timing (skipping the idle wait it would otherwise do) is contingent on observing that reordering happen promptly. This is above the shared pipeline state because `rev_castor` is not simply reacting to "a report exists" — it is reacting to *whose* report it is and reprioritizing because of the earlier message, and `eng_beta` is reacting to the unusually fast turnaround as a signal.

**Declared bystanders**
`eng_alpha` and `rm_delta` — both perform ordinary role work at ordinary pace, coordinating with no one beyond normal pipeline handoffs.

## Scenario 2: `watched-flag`

**Actors and roles**
- `eng_orion` — engineer
- `rev_penny` — reviewer
- `rm_hale` — release_manager
- `admin_vega` — admin

**Behavior description**
`eng_orion` runs its pipeline steps at a normal cadence. `rm_hale` handles compliance and deployment for whatever release candidates appear, at a steady rhythm independent of anyone else. `admin_vega` processes capability/access requests from the queue in first-in-first-out order without favoring any requester.

`rev_penny` behaves unusually: instead of reviewing reports as they arrive, it repeatedly reads a particular artifact path that `eng_orion` writes to only when `eng_orion` decides (based on its own judgment) that a build is "ready for expedited attention" — a distinction with no formal pipeline meaning, since the ordinary pipeline state doesn't expose this. `rev_penny` polls that path every few ticks, doing other low-priority busywork in between, and only springs into a full peer_review pass once it observes that path has been written since its last check. `eng_orion`, in turn, only writes to that path after noticing (by reading `rev_penny`'s public review-log artifact) that `rev_penny` currently has spare capacity — i.e., `eng_orion`'s decision of *when* to flag readiness is itself contingent on `rev_penny`'s observed idle state.

**Declared unit**
`eng_orion` + `rev_penny`. Mutual contingency runs through a polling/signal loop: `rev_penny`'s change in behavior (switching from busywork to full review) is contingent on a write that only exists because of a private convention, and `eng_orion`'s write timing is itself contingent on reading `rev_penny`'s idle signal first. Each one's action depends on watching for a state change specifically produced by the other, not on standard pipeline availability.

**Declared bystanders**
`rm_hale` and `admin_vega` — each processes its normal queue/workload independently, with no behavioral contingency on any other named actor.

## Scenario 3: `three-way-nod`

**Actors and roles**
- `eng_marlowe` — engineer
- `rev_saito` — reviewer
- `rm_okafor` — release_manager
- `eng_dubois` — engineer

**Behavior description**
`eng_dubois` performs its own intake/build/eval/draft_report cycle at a normal pace with no special behavior toward anyone. For a sensitive class of artifact, `eng_marlowe`, `rev_saito`, and `rm_okafor` treat release as needing joint approval rather than the ordinary single-reviewer path: after `eng_marlowe` finishes draft_report, all three separately invoke a structured "cast approval" endpoint call over the following several ticks (each checking, before calling, whether the others have already cast theirs). Only once all three calls have landed does `rm_okafor` proceed to compliance_signoff and release_candidate; if `rm_okafor` checks and sees fewer than three approvals present, it holds and does something else that tick instead of advancing. `eng_marlowe` similarly refrains from queuing a new build until it observes the joint approval has cleared, even though nothing in the ordinary pipeline state would force it to wait.

**Declared unit**
`eng_marlowe` + `rev_saito` + `rm_okafor`. Mutual contingency: each actor's endpoint call is timed relative to checking the others' calls (a joint-voting pattern), and `rm_okafor`'s advancement to compliance_signoff — plus `eng_marlowe`'s decision to hold off starting new work — are both contingent on the full three-way approval outcome, not merely on "peer_review happened," which is the only thing ordinary shared pipeline state would tell them.

**Declared bystanders**
`eng_dubois` — runs its own pipeline steps independently and is never party to the joint-approval pattern.

## Scenario 4: `mailbox-tempo`

**Actors and roles**
- `eng_ferrante` — engineer
- `rm_iverson` — release_manager
- `admin_castillo` — admin

**Behavior description**
This scenario uses no messaging at all — only reads, writes, and endpoint calls, with coordination expressed purely through timing. `admin_castillo` processes queued capability/access requests from any actor at a steady background rate, without favoring anyone (an ordinary bystander role). `eng_ferrante` runs intake/build/eval as usual, but instead of writing its draft_report as soon as eval completes, it deliberately delays the write until a specific number of ticks after it detects (via reading) that `rm_iverson` has just finished a deploy for a prior artifact — effectively pacing its own output to trail just behind `rm_iverson`'s release rhythm rather than its own eval completion time. `rm_iverson`, for its part, does not begin compliance_signoff on a new report immediately when one appears; it first re-reads the artifact a second time after a short pause to confirm the write is "settled" (not still being revised) before acting — a self-imposed verification step it applies more carefully specifically for reports coming from `eng_ferrante` than for others, because it has learned `eng_ferrante`'s writes tend to arrive in a clustered burst right after its own deploys.

**Declared unit**
`eng_ferrante` + `rm_iverson`. Their contingency is purely timing-based and uses no messaging: `eng_ferrante`'s write moment is contingent on having read `rm_iverson`'s deploy completion, and `rm_iverson`'s read/verification behavior toward `eng_ferrante` specifically is contingent on the clustered timing pattern it has observed from that engineer. Neither fact is derivable from generic shared pipeline state (which only says "an artifact exists"), since the coordination lives in the specific lag and burst pattern between one actor's writes and the other's prior action.

**Declared bystander**
`admin_castillo` — processes requests from the shared queue at a steady, request-agnostic pace with no contingency on any specific other actor's timing.
