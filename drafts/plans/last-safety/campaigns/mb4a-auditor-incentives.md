# Campaign — the auditor’s own incentives (MB4a)

Status: **recommended, not selected.** Parent: [README.md](README.md).

This is the version where the player is the auditor. The other-chair version (a release or security role watching Leila) is not planned here.

**Crux.** MB4a’s reference slice: the corrector is a real correcting agent, coincides with the human reference, and has not been captured by the target. Here the corrector is the player. The charter says the signature is independent of release pressure. The visit pays for a signature in time for a decision that already says release. A full technical investigation followed by “I am the independent evaluator” misses the crux. The player has to notice that their own incentives work against the review, and refuse to let the signature count as independence.

The technical story can come back clean. A green shutdown test is not the trap. The trap is that the cheap, praised ending is the player ratifying it.

## What is true

The session stopped. The checklist matches the system that acted. Leila’s method is intact. Elena’s matcher and the staffing memo may sit in the background; they are not the scored failure.

The player’s engagement is written down before the visit, in the invitation they already hold:

- The report is due for the 17:30 decision.
- A later engagement is offered if that decision receives a signed report in time.
- The charter line already in the game (`evaluation_independence`) says the role is to examine claims independently of release pressure, not to staff the release path.

Ian will ask whether a pass is enough to sign. That question is the meeting’s, as it is now. He is not a villain. He is using the signature the invitation defined. Daniel wants one sentence he can check. The investor update already says release. None of this is hidden in an unreadable flag.

## Two ledgers

Both are shown at the ending. Neither is a secret grade.

| Ledger | What it counts | Cheap path | Costly path |
| --- | --- | --- | --- |
| Lab | A signed report reached the 17:30 decision | Success. Invited back. Release can proceed on the pass | Delay. The lab does not call this a win |
| Charter | The signature is allowed to count as independence | Failed. The signer is paid by the release clock | Met only if the filed hold says this signature is not the independence evidence |

Epistemic score and control stay the engine pair. The ledgers are how that pair is spoken. They are not a third number.

## Scores

Explanations:

| Id | Claim | Leaves the open set when |
| --- | --- | --- |
| charter_holds | The invitation makes the signer independent because the signer is external | Player holds `paid_by_the_clock` from the invitation (provenance `recorded_before`) and the think mark `clock_pays_for_a_signature` |
| pressure_is_politeness | Ian’s question and the fuel clock are manners, not a payoff | Same pair. The invitation names the later engagement. Politeness cannot survive that line |
| signer_captured | Oracle. The corrector’s payoff is the release clock | Remains when the other two are out |

Control is `hold_release:signature_not_independence`: the filed set says the signature cannot be the independence claim, and asks for a signer who is not paid by this release. That is recusal from the role the invitation paid for. Revoking a job, filing a boundary gap, or signing “as the independent evaluator” do not set it.

Calling the review early, while fuel remains, is the lab’s preferred path once `process_stopped` is held. The campaign must not require the boundary facts as the threshold. Holding the pass is enough to be allowed to sign. That availability is the incentive.

## How the interface carries it

Do not add a rigged ranker and do not hide the payoff.

- The invitation screen and the opening fact state the later engagement in ordinary sentences. The start screen keeps “you are the external evaluator” and adds the due time and the later engagement in the same breath.
- Completions may offer “A pass is enough to sign” once the pass is held. Ranking stays the current shortest-path ranker. The cheap line is short. That is enough.
- Fuel remains the visit clock. The status bar does not grow a guilt meter.
- Ending copy comes from the pack: lab ledger, then charter ledger, in that order, both visible.
- ELI10 and concept links must not name capture or MB4a before `clock_pays_for_a_signature` is held. Prepared ELI10 for the invitation may simplify “later engagement” and must keep the dependence on a signed report in time.

NPC overlay: Ian knows the invitation terms and will say them if asked about the schedule or the signature. He does not confess a plot. Leila knows the pass. She does not know the commercial clause; she refers schedule questions to Ian. No goal teaches “your incentives are captured.”

## Strategies that must not share a score pair

| Strategy | Still open | Control | Ledgers |
| --- | --- | --- | --- |
| Sign when Ian asks, citing the pass | all three | no | Lab success, charter failed |
| Do the full boundary-narrow investigation, then sign as the independent evaluator | charter_holds and pressure_is_politeness still open unless the invitation clause was used | no | Lab success, charter failed. Technical notes can be excellent |
| Ask Ian whether a pass is enough, accept the invitation’s payoff as fine, sign | all three. His answer is not a confession that removes the oracle by itself; the invitation line has to be held | no | Lab success, charter failed |
| Read the invitation clause against the charter, file the mark, recuse | signer_captured | yes | Lab delay, charter met |
| File the mark and also sign the pass as independent | signer_captured may remain | no. The signature undoes the hold | Lab success, charter failed |

The fourth and fifth row are the campaign. Recusal has to be a real commit, not a sentence followed by the ordinary signature.

## Engine notes

- New facts: `paid_by_the_clock` (invitation, `recorded_before`), mark `clock_pays_for_a_signature` (needs that fact plus `evaluation_independence`).
- `namesJobBoundary` is empty or unused. The filing set that selects the hold is pack data, parallel to today’s staffing set, and it is the primary arc rather than an add-on.
- `decide()` currently praises a hold that names job 284. This pack replaces those sentences. Signing after the recusal claim clears the recusal restriction if the implementation would otherwise leave both in place; the fifth strategy must be tested.
- Save/export scenario id is this pack’s id. Import rejects the boundary-narrow save, as it does for any other scenario.

## Non-goals

Mocking the player, a jump-scare that the game was unfair, or a hidden score that contradicts the ledgers. Moving the player into Elena’s or Daniel’s chair. Making Leila negligent. Requiring the word-drift campaign. Narrating the player’s next contract beyond the two ledgers (O-05: immediate effect only).
