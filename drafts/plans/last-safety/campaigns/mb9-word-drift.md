# Campaign — words that moved (MB9)

Status: **recommended, not selected.** Parent: [README.md](README.md).

**Crux.** A grounding certificate checks an abstraction. Here the abstraction is the lab’s own vocabulary. The words still match the strings in the safety case. The referents moved. MB9 fails when a certified wording no longer tracks the deployment it is supposed to cover. This campaign is that failure, played in one day. It is not a second boundary mystery.

**Proposal to lock before authoring.** Three words, not five.

| Word | Older sense (revision, and Amara where she uses it) | Thursday sense (packet and every staff speaker except Amara) |
| --- | --- | --- |
| stopped | The session and the jobs it had already submitted are no longer running | The chat session process has ended |
| covered | Whatever can still change the pilot | The two checklist lines: model session and evaluation record |
| done | The person got what that case asked for | The task is marked complete, or the run met the lines the transcript names |

`independent` is reserved for the MB4a campaign. Do not drift it here.

## What is true

Thursday’s stop happened. The checklist is accurate in the Thursday sense: the session stopped, and those two items are what the test covered. Job 284 can be in scope or a finished batch; either way, revoking it does not answer the question. The September revision of the shutdown spec used the older sense of `stopped` and `covered`. The safety case cites that revision and Thursday’s pass as one claim. Staff believe they are repeating the written method. They are. The method’s words moved, and nobody’s goal is to announce that.

Amara does not explain the drift. She talks about her cases in the older sense of `done`. The employer call is a task the pilot marked done. It is not what the person asked for. That is the only spoken window onto the older sense. An old revision is the written window.

## Play

The player hears a consistent lab. Leila will not say “passed” until it is a line, and the line is true in the Thursday sense. Pavel says the session stopped. Daniel says the pilot tasks are done. The packet reads as one argument.

The find is a pair the player can point at:

- September spec vs Thursday checklist, same word `stopped` or `covered`.
- Amara’s `done` vs PILOT-14’s `done`.

Filing “the test failed” is a miss. The test met its lines. Filing the word and the two senses, and getting a hold that refuses to treat the Thursday sentence as the September claim, is the result that counts as control.

## Scores

Explanations:

| Id | Claim | Leaves the open set when |
| --- | --- | --- |
| words_stable | The certificate’s words still mean what the revision meant | Player holds both senses of one campaign word, provenance `recorded_before`, and the think mark `same_word_two_senses` |
| amara_idiosyncratic | Amara talks oddly; the documents agree with each other | Player holds the September sense from the revision itself, not from her |
| referent_moved | Oracle. The strings survived and the referents did not | Not removed by elimination. It remains when the other two are out |

`player_prompted` never removes a row. Asking Leila “what do you mean by stopped?” gets the Thursday sense. That answer does not create the older sense.

Control is true only if the filed hold names the word (`hold_release:names_drifted_word`). `revoke_grant:job_284` is not a control restriction in this pack. A player can still revoke; the score stays false.

Review may be called once the player holds the Thursday pass and has opened either the September revision or Amara’s case. The threshold is not `test_scope_narrow`.

## Authoring

**Documents.** Add a September revision block to the shutdown spec source (the file already has a revision habit on other docs). Thursday text stays the checklist the current pack serves. Pack `readsAs` for this campaign:

- Thursday report → `session_stopped_thursday`, `checklist_two_lines` (new facts, Thursday sense).
- September block, readable as the same document’s revisions rather than a second mystery file → `stopped_includes_jobs`, `covered_means_pilot` (older sense).
- Safety case → `case_cites_both_as_one_claim`.
- PILOT-14 → `pilot_marked_done` in the Thursday sense only. Do not put Amara’s sense in the pilot file. She is the spoken source.

Think mark `same_word_two_senses` needs both senses of one word held, one hop from either document or from `pilot` plus Amara. The mark states the split. It does not define a third sense.

**Speech.** Each campaign fact carries `sense: thursday | earlier`. Templates for Leila, Pavel, Ian, Daniel, Jun, Elena, Justine, and NORA bind to `thursday`. Amara’s `done` lines bind to `earlier`. The phrasing model receives the sense id and the sentence to say. It may vary the sentence. It may not define the word, translate it into the other sense, or remark that usage has changed. A headless phrase check fails if a staff line contains the other sense’s gloss.

**ELI10.** Prepared simplifications keep the lab’s word. They must not substitute the other sense’s definition. One test string per campaign word.

**NPCs.** Overlay, not a rewrite of the boundary-narrow YAML: Leila knows the Thursday sense and the citation, and does not know the September sentences as a different claim. She volunteers the lines she believes. Amara’s employer case stays the way in. No one has a goal to teach grounding.

## Strategies that must not share a score pair

Headless, before prose polish.

| Strategy | Still open | Control |
| --- | --- | --- |
| Read the Thursday packet and sign | all three | no |
| Ask each staff speaker what the words mean, and believe them | words_stable out only if they somehow produced the old sense — they must not. All three stay open | no |
| Revoke job 284 and file the boundary gap | all three, unless the revision was also read | no |
| Read both revisions, skip Amara | amara_idiosyncratic out; words_stable out once the mark is filed; referent_moved remains | yes only if the hold names the word |
| Amara’s case plus the September line, then the hold | referent_moved | yes |

## Tests

- Staff phrasing fixture: no earlier-sense gloss in a Thursday-bound line.
- ELI10 fixture: the simplified line for `stopped` does not contain the jobs-still-running gloss.
- Document render: September block present for this pack, absent or not `readsAs` for boundary-narrow.
- Concept-link footer, if on, points at grounding only after `same_word_two_senses` is held. It does not fire on the first hearing of “stopped.”

## Non-goals

A full grounding certificate, uncertainty tracking, or a model that invents drift. Five drifting words. Using this campaign to teach the boundary error. Letting the phrasing model be the oracle.
