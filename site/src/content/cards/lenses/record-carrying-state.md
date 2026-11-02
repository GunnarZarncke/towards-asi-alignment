---
title: "Record-carrying state"
type: "lens"
status: "framework"
summary: "The current state plus a record of how it was reached. A utility on it can value routes; a utility on the bare state cannot."
related:
  - "lenses/state-utility"
  - "lenses/history-value"
  - "lenses/cycle-residue"
  - "lenses/lenses-and-frameworks"
external:
  - label: "LessWrong tag: Instrumental convergence"
    url: "https://www.lesswrong.com/w/instrumental-convergence"
---

**Role.** Target. Graph node `hstate`.

> A finite history can be written into an enlarged state, and a state utility on that enlargement can reproduce a history preference.
>
> — Frames relations note

The record can be the full history, a transcript, or a few route bits. Every route reward is exact on records: a step scores the record value after it minus the record value before (`route_exact_on_records`). So the round trip that no bare-state utility can value (`stateCycleIncompat`) has a value here.

The escape works only for what the record sees. If two walks leave the same record and differ in route value, no record utility represents the difference (`unrecorded_route_not_representable`).

Correction is the same. A record utility can accept a correction to a worse outcome by compensating the corrected branch, but then it does not care whether the channel survives (`soares_indifference_no_preservation`). If the record does not see the channel, protecting the channel is the same preference as wanting to be corrected (`hstateCorrectionIncompat`).

Whether the record escapes the instrumental-convergence counting argument depends on what it holds. Over observation records the tendency stays and can get stronger; over action-observation records in a deterministic world it disappears for generic utilities (Turner 2021). What the record always changes is what a chosen utility can express.
