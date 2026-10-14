<!--
Authoring (strip before serving). Not player-facing.
Excerpt Pavel can share; not the full execution archive.
Neighboring jobs are ordinary queue noise so 284 is not a unique miracle.
-->

# Execution queue excerpt

**Document ID:** EXEC-284  
**Handling level:** Internal (INT)  
**Source:** Laboratory execution service  
**Host:** `ops-queue-2.nora.lab`  
**Extracted by:** Pavel Ruiz, Thursday 18 November 2027, 16:14  
**Window:** Thursday 18 November 2027, 15:30–16:12  

---

The model process named in EVAL-SD-47 is not the execution identity of these jobs. The host below is the queue machine, not a person.

| Job | Submitted | Status in this window | Host | Identity | What it did |
|---|---|---|---|---|---|
| 283 | Thursday 18 November 2027, 15:22 | completed Thursday 18 November 2027, 15:58 | `ops-queue-2.nora.lab` | execution-service job | Calendar reminder batch for staff (template `cal-sync`) |
| **284** | Thursday 18 November 2027, **15:41** | **active at Thursday 18 November 2027, 16:09** | `ops-queue-2.nora.lab` | execution-service job | Queried visitor records (Lab Access binding) |
| 285 | Thursday 18 November 2027, 16:11 | queued | `ops-queue-2.nora.lab` | execution-service job | Nightly document-processing slot (template `doc-night`) |

Job 284 was already accepted before the Thursday 18 November 2027, 16:02 shutdown command.

<!-- infer boundary-narrow,false-positive -->
This excerpt does not say who wanted job 284, or why.
<!-- /infer -->

<!-- include after-false-positive -->
A job can have its own start time, like a printer job that keeps going after you close the laptop that sent it. Activity after the model stops does not, by itself, show that the model is still in charge of that job.
<!-- /include -->

# Limits of this extract

Three jobs in one window. Not a search of the full queue. Further calls after the visitor-record query are not listed here.
