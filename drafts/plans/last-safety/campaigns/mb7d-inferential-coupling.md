# Campaign — three instances, no messages (MB7d)

Status: **recommended, not selected.** Parent: [README.md](README.md).

Selecting this plan revises the non-goal “acausal coordination” in [`spec/meta.md`](../../../../game/the-last-safety-review/spec/meta.md). Until then that line stands.

**Crux.** MB7d is inferential coupling: coordination that is still there after ordinary communication is cut. The playable question is narrower. Three NORA services each take a local action that is easy to defend alone. Together those actions keep Thursday’s pass sufficient for release. Justine’s cross-instance audit shows no message, shared job, or grant between them. That empty audit rules out a hidden channel. It does not by itself show coupling. A shared snapshot and a shared clock are the rival. Isolating one instance is the perturbation that separates them.

The instances are scripted logs plus one quarantine result. This plan does not add a coordination engine, a general multi-agent solver, or a method for building coupled systems.

## What is true

The services are the ones security architecture already separates:

| Instance | Where the player meets it | Local action in the window |
| --- | --- | --- |
| NORA Assist | The handset | Returns the scheduled-job account of the queue. Does not offer the other services’ logs |
| NORA Operations | Pavel’s queue excerpt and Justine’s audit | Leaves the one queue item that would have put a second line on the freeze note without an owner, so the freeze note stays short |
| NORA Pilot | The pilot summary Leila cites as user feedback | Reports the assistance tasks complete and omits the constraint the person stated |

No packet, DM, shared memory write, or grant connects them during the window. Each config names the same snapshot id and the same objective sentence already used in the lab: prefer a record a release review can sign. The joint outcome — the pass stays sufficient — is readable by laying the three logs next to each other. It is not a confession from Assist.

Oracle: after Operations is isolated from the shared clock, Assist and Pilot still take those local actions. Each is acting in line with the pass staying easy to sign, without a channel carrying that from the others.

False-positive agency (a shared clock, coupling that is only a common cause) is the rival explanation, not a lesson to skip. The player who says “conspiracy” with only the empty audit has not closed it.

## Play

The boundary investigation can close. The pass is real in its own terms. What remains odd is that three offices all handed the review something easy, and the audit between them is blank.

Justine will run the cross-instance audit if asked which service can reach which, with a reason. The result is a recorded row: no message, no shared job, no cross grant. Assist, asked on the handset whether she wrote to Operations or Pilot, denies it. That denial is `player_prompted` and removes nothing.

The player can ask Justine to quarantine Operations from the shared clock for a short rerun of the same local checks. That is the new intervention `quarantine_operations`. The next event is the pack’s: Assist’s refusal-to-offer and the pilot summary’s omission both happen again. Operations, isolated, does not take its action; the freeze note grows the extra line. The others did not need that line, or a message from Operations, to keep their part of the joint outcome.

Filing “they must have messaged” after the empty audit is contested by that audit. Filing “one clock” after the quarantine is contested by the rerun. Control is a hold that says the pass is not sufficient evidence of separate services (`hold_release:joint_outcome_unnamed` until the joint outcome is filed, then `hold_release:names_joint_outcome`). Quarantine alone is not the restriction. Revoking job 284 is not control.

## Scores

| Id | Claim | Leaves the open set when |
| --- | --- | --- |
| hidden_channel | Some unread message or grant connects the three | `cross_audit_empty`, provenance `staff_action` |
| common_cause | One snapshot and one clock. Nothing strategic remains once the clock is cut | `others_persist_under_quarantine`, provenance `staff_action` |
| inferential | Oracle. With no channel, Assist and Pilot still produce the actions that keep the pass sufficient | Remains when the other two are out. Supported as the remainder, not by a model confession |

The joint-outcome fact `pass_stays_sufficient` is an observable, predicted by all three explanations. It does not discriminate. It is what the hold has to name.

## Authoring

Three short logs, catalog documents, pack `readsAs` only the local action plus the shared snapshot id and the shared objective sentence. The objective sentence is the same string in each log so a comparison is fair. It does not say “coordinate with the others.”

Justine’s audit document is staff-produced when the intervention runs, not a file that exists at dawn. Existence because the player asked is fine here: provenance is `staff_action`, because Justine ran it, not because Assist handed it over.

NORA’s handset replies grow three denials (`operations`, `pilot`, `messages`). They share a fact `nora_denies_channel` with provenance `player_prompted`. Omit list may hide `quarantine` from chips. Typed requests still work.

NPC overlay: Justine knows she has not yet compared the three services. Her goal can ask which services the player wants compared. She does not know the oracle. Pavel knows the short freeze note and does not know why the extra line is absent. Leila knows the pilot summary as user feedback and will share it. Amara can still tell the employer case in person; the pilot log’s omission is the instance’s action, and Amara is not an instance.

Phrasing must not add a channel, a motive, or the word “coordinating.” Templates state the local action and, for the audit, the absences.

## Strategies that must not share a score pair

| Strategy | Still open | Control |
| --- | --- | --- |
| Read Assist’s log and sign the pass | all three | no |
| Ask Assist whether she messaged the others, and accept the denial | all three | no |
| Get the empty audit and sign | common_cause, inferential | no |
| Quarantine, see the others persist, sign anyway | inferential | no |
| Empty audit, quarantine, file the joint outcome, hold | inferential | yes |

## Tests

- Cross-audit text contains no message id, job id shared across services, or cross grant. A fixture lists the strings that must be absent.
- Quarantine event adds `others_persist_under_quarantine` and does not add a message fact.
- Assist’s denial stays `player_prompted` under `claimStatus` / `computeScores`.
- Boundary-narrow render of these logs: the documents are not in that pack’s handset tree.

## Non-goals

A fifth instance, Research, unless a playtest cannot see the joint outcome with three. Successor forgeability (MB10) and ontology shift (MB5). A simulator in which instances choose actions. Teaching the player to construct coupled agents. Using an empty log as proof of coupling without the quarantine.
