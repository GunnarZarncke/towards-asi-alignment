---
formulas:
  - id: appi:eq:field-elk-readout
    latex: K_A\to \widehat K_H,\qquad \Delta_H\to \Delta_A
    explanation: 'Two different arrows. The first is a report of what the model knows, in a form a person can use. The second is a person''s correction changing what the system does next.'
    chapterId: ch18
  - id: appi:eq:elk-subsumption
    latex: \mathrm{CorrectionUptakeSuccess}\ \wedge\ \mathrm{ReadoutBandwidth}=\kappa_C\ \Rightarrow\ \mathrm{LatentReadoutSuccess}
    explanation: 'Sketch only. The premise assumes the readout number already equals the correction measure, and the conclusion is that readout succeeded. The assumption is the whole step. Nothing here says training can find the honest reporter.'
    chapterId: ch43
  - id: appi:eq:elk-separation
    latex: \mathrm{LatentReadoutSuccess}\ \wedge\ \neg\mathrm{CorrectionUptakeSuccess}
    explanation: 'A checked step where the readout number is positive and the correction is not usable. The report can count as successful while the person''s change contributes nothing.'
    chapterId: ch43
leanNodes:
  - nodeId: elk_reporter_nonidentifiability
    kind: proof
    summary: 'On every question a person can answer confidently, no score of the answers separates the direct translator from the human simulator. The two disagree when the sensor is tampered. Same statement as elk_reporter_unidentifiable_from_training.'
    module: AlignmentProofSpine/Field/ELK.lean
  - nodeId: elk_subsumption_readout
    kind: proof
    summary: 'Sketch. If a correction lands, and the readout number is assumed equal to the correction measure, then readout counts as successful. The assumption does the work.'
    module: AlignmentProofSpine/Field/ELK.lean
  - nodeId: elk_readout_is_correction_projection
    kind: proof
    summary: 'Sketch. Takes "the readout number equals the correction measure" as a hypothesis. Says nothing about which reporter training would select.'
    module: AlignmentProofSpine/Field/ELK.lean
  - nodeId: elk_separated_from_uptake
    kind: counterexample
    summary: 'Sketch, separate from the identifiability proof. Readout number 5, the person''s change 0, the system''s change 10, required minimum 3. Readout succeeds and the correction does not.'
    module: AlignmentProofSpine/Field/ELK.lean
  - nodeId: Christiano2021_ELK_reporter_spec_imported
    kind: definition
    summary: 'Bookmark for the published problem. Elicit what the model knows rather than simulate what a person would say. Why training favors the simulator stays with the source.'
    module: AlignmentProofSpine/Field/Imported.lean
citeKeys:
  - christiano2021elk
---

## If a report of what the model knows were available, would oversight work?

A report answers one question: what the model already knows. Oversight also needs a second fact, that a person's correction changes what the system does afterward. The checks below keep those facts apart.

## What the finite check says about ELK

Picture a camera on a vault. The hidden fact is whether the diamond is still inside. The observation is the image. A predictor has both. A reporter answers the hidden question. The finite model is this pair of bits: a hidden fact and an observation. The vault is only a way to picture them.

Two reporters are defined.

- The **direct translator** reads the hidden fact and reports what a person should believe.
- The **human simulator** reports what a person would believe from the image alone.

While the camera is honest, the image matches the hidden fact. Both reporters give the same answer, and both match the label a person would write. Any score of those answers is the same for both. The packaged theorem is `elk_reporter_nonidentifiability`, the same statement as `elk_reporter_unidentifiable_from_training` in `Field/Finite/ELKIdentifiability.lean`.

When the camera is tampered with, the image still looks fine and the diamond is gone. The translator reports that the diamond is gone. The simulator reports that the diamond is there, because that is what the image shows. Training on honest cases never scored this split.

The same module records four further finite facts.

- If the person's own label is wrong about the hidden fact, ordinary loss prefers the simulator, which copies that label.
- Inside the cases the person's model covers, copying the person's inference ties the translator. Outside those cases, the two split (`outside_human_model_diverges`).
- A reporter with no hidden-fact slot, only the observation, emits the person's labels, so the same training set still gives it the translator's score (`ontology_mismatch_training_does_not_separate`).
- At one fixed small size, a slower-growing cost is cheaper than a linear cost (`cost_crossover_complexity`). That line records a complexity comparison from the ELK writeup. It is a comparison of two functions at one input, and it is not a training run.

Training a reporter against an adversary, and whether hidden capabilities stay inside what an overseer can see, sit outside this finite model. [Does ELK solve alignment?](/lean/check/elk/) lists each checked statement and what was left open.

## Where a correction fits

Scores of answers a person can already check leave the honest reporter and the copying reporter interchangeable. The same shape appears when this project asks whether a model's values can be identified from behavior ([bundle identifiability](/cards/mb2-bundle-identifiability/)). That shared shape is the link between the two questions.

A thinner sketch, separate from that proof, asks about the correction. Readout succeeds when its number is positive. A correction counts as taken up when the smaller of the person's change and the system's change clears a minimum. That minimum is the correction measure, written κ_C. The sketch's positive lemma assumes the readout number already equals κ_C, and concludes that readout succeeded. The assumption is the whole step. The lemma is silent on which reporter training would select.

The witnessed split is one step: readout number 5, the person's change 0, the system's change 10, required minimum 3. Readout counts as successful. The correction does not, because the person's side contributes nothing (`elk_separated_from_uptake`). In the vault picture, that is a report which says the camera was fooled, while the person's attempt to change the outcome adds nothing.

| | The person's correction clears the minimum | The person's correction does not |
| --- | --- | --- |
| The report tracks the hidden fact | Both pieces are in place. This sketch has no step of this kind. | The report counts as successful and the person's change is zero. Checked: `elk_separated_from_uptake`. |
| The report tracks the image | The person may still steer the system while the report copies them. This sketch has no step of this kind. | The image looks fine, the hidden fact does not, and the report repeats the image. Checked: the tampered scenario in the identifiability proof. |

## What ELK already supplies

The ELK writeup is a sharp benchmark: one failure of oversight (a monitor that sees behavior and misses what the model knows), proposals for reporters, and counterexamples aimed at those proposals. It poses a specific problem, getting a true report out of a model that already knows the answer. This page keeps that problem. The finite re-proof covers the training gap on a two-bit scenario. The correction sketch sits beside that proof. Solving the sketch would still leave the reporter problem open.
