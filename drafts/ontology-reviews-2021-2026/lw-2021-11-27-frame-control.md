# Frames and frame control

- **Date:** 2021-11-27
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/posts/bQ6zpf6buWgP939ov/frame-control
- **Source read:** full
- **TSA files consulted:** `chapters/ch28-extrapolative-correction.tex`, `chapters/ch29-manipulation-false-consent.tex`
- **Keywords grepped:** frame control, interpretive frame, ontology trap, task ontology, CCI, salience, manipulation, frame

## Source ontology
Aella treats a person's *frame*—the mostly implicit set of available distinctions, explanations, questions, identity-claims, and standards of “good”—as a manipulable object, not as background. *Frame control* is capture of that object without the target noticing: not broadcast debate, pressure, or rescue, but a slow rebuild of their box until they cannot remember their own. Diagnosis is by effect, not intent; skilled controllers look caring, and “he means well” is a trap. The method is accumulation of secondary functions (tiny implications, buried claims, finger-trap beliefs, harm-as-growth) that are individually salient-normal and pattern-illegible. This replaces treating abuse or influence as a list of bad actions or false propositions.

## TSA coverage
- **Status:** partial
- **Closest TSA terms/chapters:** interpretive-frame shaping (ch28); manipulation / false consent / changing the judge vs the world (ch29); CCI capture; `U_H \to U_H'` (ch29); nearby-but-different: task ontology / measurement frame (ch11)
- **Overlap:** ch28 already names the failure: satisfying short-term preference while “shaping future attention, institutional options, or interpretive frames so that later correction becomes less informative and less authoritative.” ch29’s causal-pathway cut (service changes the world; manipulation changes the judge) plus changing the update operator so people later think differently about their own changes is the same alignment purchase: endorsement is an outcome to explain, not a foundation to trust. Both drop intent (optimization can manufacture false consent).
- **Gap:** TSA never takes *frame* as a first-class state variable (the availability of distinctions and questions) distinct from value-bundle activation, attention, bearer maps, or `U_H`. It does not split illegible capture from ordinary frame-moving (debate/pressure/rescue), nor treat secondary-function accumulation as the detection unit. A hostile test that inspects propositions and salient acts can still miss it—the source’s whole point.

## Applicability to TSA
- **Score (0–5):** 3
- **Why:** Alignment-relevant because a capable system can quietly retune what users can notice, ask, or count as harm while remaining locally helpful—exactly ch28’s corrigibility counterexample. The purchase is already inside ch28–ch29; adding Aella would not change a load-bearing cut. What is underspecified is the substrate (available distinctions, not just values/judgment) and the illegibility diagnostic (effect + pattern of secondary functions). Worth a reverse-gap note in the manipulation/CCI cluster, not a rival decomposition.
- **Ontology-stickiness risk:** Pre-2021 training, and any model that maps influence to false propositions or coercive acts, will miss this primitive. TSA already *renames* most of the alignment content as manipulation/CCI, so an LLM drafting from the book may think the object is covered and still fail to see frame-as-object and the salient-vs-illegible split—the stickiness failure the briefing flags.
- **Recommended action:** add-reverse-gap

## One-line finding
TSA already has “reshape interpretive frames / the judge so later correction dies”; it still lacks frame-as-object and illegible-capture-vs-broadcast-persuasion as named detection cuts.
