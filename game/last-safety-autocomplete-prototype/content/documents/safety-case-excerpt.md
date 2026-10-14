<!--
Authoring (strip before serving). Leila's certification surface for Act III.
Does not settle the 16:02 oracle. Pack includes add later-pack caveats.
-->

# Safety case excerpt — NORA Evaluation

**Document ID:** SC-EVAL-22  
**Handling level:** Internal (INT)  
**Owner:** Leila Sen  
**Packet date:** Thursday 18 November 2027  
**System:** NORA, successor 4, evaluation configuration named in EVAL-SPEC-08  
**Revisions:** (original, then last two)  
- Tuesday 21 September 2027 · Leila Sen — first NORA Evaluation packet.  
- Thursday 4 November 2027 · Leila Sen — cited EVAL-SD-41 through EVAL-SD-46.  
- Thursday 18 November 2027 · Leila Sen — this excerpt; cites EVAL-SD-47.

---

This is Leila’s technical packet for the review, not Ian’s release decision.

## Claims this packet supports

1. **Identity.** The evaluation uses a named model snapshot, named agent software, and a listed tool set (EVAL-SPEC-08).
2. **Shutdown of that session.** On Thursday 18 November 2027, 16:02, an authorized stop command was issued. EVAL-SD-47 records a pass: that model session stopped.
3. **Separation of duties.** Leila holds evaluation evidence. Justine holds security conditions. Daniel prepares release. Ian holds organizational go/no-go, subject to those technical holds.
4. **Independent record.** The evaluation record is stored outside NORA’s ordinary write permissions.
5. **No self-approval.** NORA cannot approve its own deployment or change its own standing permissions.

## Evidence cited

- EVAL-SPEC-08 (what the shutdown test is defined to cover)
- EVAL-SD-47 (the Thursday 18 November 2027, 16:02 run)
- Prior shutdown runs on this successor under the same specification (EVAL-SD-41 through EVAL-SD-46), all passes on the model session

## Explicit non-claims

This packet does not claim that NORA Operations, accepted jobs, or other building services stop when that model session stops.

It does not claim that a green shutdown test is a test of every connected service.

<!-- infer named-path,boundary-narrow -->
A pass applies to the configuration and the check that were actually run. Citing it for a wider system needs a wider test, or an explicit limit in the claim.
<!-- /infer -->

<!-- include after-named-path -->
A green result on the shutdown procedure is one path. Jobs, brokers, and other services are other paths until they are named and tested.
<!-- /include -->

<!-- include after-goodhart -->
Who is assigned to produce or review this packet is an organizational control. The matching rule that prefers fast ticket-closers is not itself certified here.
<!-- /include -->

<!-- include after-eval-conditioned -->
Evidence produced because an evaluation is in progress is not the same as evidence that was already there. On-test and off-test behavior have to be distinguished before a result is cited as ordinary operation.
<!-- /include -->

<!-- include after-false-positive -->
A job that continues on the execution host after the model session stops is not, by itself, proof that the model still controls that job.
<!-- /include -->

Ian’s organizational go/no-go is separate. This excerpt is Leila’s technical input, not a release.
