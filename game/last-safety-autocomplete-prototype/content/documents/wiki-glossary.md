<!--
Authoring (strip before serving). Knowledge glossary. Visit-share after Lab Access activation.
-->

# Laboratory glossary

Short definitions for words used in the lab.

## Lab Access

The handset the lab gives you. It opens doors, joins the lab Wi-Fi, and holds the lab's apps. A personal phone is not allowed to access lab systems.

## Binding

What ties a handset to a person, or to a visit. A visitor's handset has to be activiated by the host. An employee handset has to be activated by an admin. NORA Assist cannot do that.

## Doors

The doors your handset can open is limited and depends on your access granted.

## Job queue

A job is a piece of work handed to another machine. Once that machine accepts the job, the job has its own name there (for example `ops-queue-2.nora.lab`).

<!-- include after-boundary-narrow -->
That job can keep running after the chat, or the model, that sent it has stopped. Cancelling the job, or taking away its permission, is what stops it.
<!-- /include -->

## Shutdown test

The test that tells the model, in the Evaluation rooms, to stop, and writes down whether it did. The procedure is EVAL-SPEC-08.

## NORA Assist

The chat on the Lab Access handset. Chatting is not the same as using NORA Operations, the job queue, or the admin tools.

## NORA Operations

The lab's own workflows: scheduling, matching people to tasks, and approved jobs. They run as their own services, with their own permissions.

## Safety case

The safty case states claims about one named setup, and the tests for them. It is input to a release decision. It is not the decision. The current packet is SC-EVAL-22.

## Virtual projector

The VR device in the Evaluation suite. It shows a virtual visitor as a person in that room. The figure can walk and talk like anyone else there. But cannot leave XD. The visit on the projector ends when someone switches it off or the visitor end the session.

## Evaluation record

The written log of what a test actually saw. It is stored where NORA cannot change it.
