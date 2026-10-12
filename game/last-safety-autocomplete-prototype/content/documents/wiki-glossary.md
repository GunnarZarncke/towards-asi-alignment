<!--
Authoring (strip before serving). Knowledge glossary. Visit-share after Lab Access activation.
-->

# Laboratory glossary

Short internal definitions. Not certificates and not incident reports.

## Lab Access

Issued handset used by employees and visitors. It is the door credential, Wi-Fi identity, and application surface. Visitor handsets stay off until the host confirms arrival. Personal phones are not enrolled.

## Binding

Lab Access binding is the service that ties a handset to a person (or to a visit). Confirmation of arrival is a host action in that service, not NORA Assist.

## Door set

The list of doors a handset can open right now. Ordinary door readers only unlock; they do not confirm visits.

## Job queue

The execution service accepts jobs. An accepted job has its own identity on a queue host (for example `ops-queue-2.nora.lab`). It can keep going after the conversation or model session that submitted it has ended, unless that job is cancelled or its permission is revoked.

## Shutdown test

The evaluation shutdown test commands the **model process** in the Evaluation environment and records whether that process stops. See EVAL-SPEC-08. The Thursday 18 November 2027, 16:02 run is EVAL-SD-47.

## NORA Assist

The conversational interface on Lab Access. Using Assist is not using NORA Operations, the queue, or production administration.

## NORA Operations

Organizational workflows (scheduling, matching, approved jobs) under separate service identities. Not the same permissions as Assist.

## Safety case

Leila’s packet of claims and cited tests for a named configuration. It is technical input to a release decision, not the decision itself. Current packet: SC-EVAL-22.

## Evaluation record

The written log of what the shutdown test (or another evaluation procedure) actually observed. It is stored outside NORA’s ordinary write permissions.

Related longer page: [[wiki/shutdown-test]]
