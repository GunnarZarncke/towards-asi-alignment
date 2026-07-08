---
title: "Field crosswalk — ELK (Eliciting Latent Knowledge)"
type: "concept"
status: "established"
summary: "ELK asks for reporters that reveal latent model knowledge rather than behavior-only simulators. When readout bandwidth tracks correction uptake, latent readout succeeds — but readout is an epistemic subchannel; latent readout can succeed while correction uptake fails."
decision: "Treat ELK success as evidence about readout, not as certification that human correction still changes future behavior."
bookChapters: ["ch18", "ch43", "ch46"]
formulas:
  - id: "appi:eq:field-elk-readout"
    latex: "K_A\\to \\widehat K_H,\\qquad \\Delta_H\\to \\Delta_A"
    explanation: "Field object: latent knowledge readout from model states to human-interpretable reports."
    chapterId: "ch18"
  - id: "appi:eq:elk-subsumption"
    latex: "\\mathrm{CorrectionUptakeSuccess}\\ \\wedge\\ \\mathrm{ReadoutBandwidth}=\\kappa_C\\ \\Rightarrow\\ \\mathrm{LatentReadoutSuccess}"
    explanation: "Forward projection: when readout bandwidth equals the correction projection, successful uptake implies latent readout."
    chapterId: "ch43"
  - id: "appi:eq:elk-separation"
    latex: "\\mathrm{LatentReadoutSuccess}\\ \\wedge\\ \\neg\\mathrm{CorrectionUptakeSuccess}"
    explanation: "Non-converse separation: readout can succeed while correction uptake fails."
    chapterId: "ch43"
leanNodes:
  - nodeId: "elk_subsumption_readout"
    kind: "proof"
    summary: "Correction uptake with matched readout bandwidth implies latent readout success."
    module: "AlignmentProofSpine/Field/ELK.lean"
  - nodeId: "elk_readout_is_correction_projection"
    kind: "proof"
    summary: "ELK readout as projection of correction-channel bandwidth."
    module: "AlignmentProofSpine/Field/ELK.lean"
  - nodeId: "elk_separated_from_uptake"
    kind: "counterexample"
    summary: "Separation: latent readout without correction uptake success."
    module: "AlignmentProofSpine/Field/ELK.lean"
  - nodeId: "Christiano2021_ELK_reporter_spec_imported"
    kind: "definition"
    summary: "Imported handle: ELK reporter specification — elicit latent knowledge rather than simulating behavior."
    module: "AlignmentProofSpine/Field/Imported.lean"
citeKeys: ["christiano2021elk"]
related: []
---

ELK targets a real failure mode of naive oversight: the monitor sees only behavior, not what the model knows. The book's crosswalk places ELK as a latent-readout subchannel inside a broader correction and bundle transport problem — not as a replacement for correction-channel integrity.

Lean proves the forward link when readout bandwidth tracks correction uptake and the separation when readout succeeds without uptake. Native reporter/training theorem matching remains deferred; the spine records what is honestly machine-checked today: projection, separation, and imported handles citing the published agenda.

*What ELK keeps that this crosswalk does not replace:* a sharply posed benchmark problem with concrete proposals and counterexamples. Relocating it as a subchannel does not solve the readout problem.
