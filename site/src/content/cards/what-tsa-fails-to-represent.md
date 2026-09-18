---
title: "What This Map Misses"
type: "concept"
status: "open"
summary: "The field matrix asks how other agendas touch this project's questions. This card asks the reverse: what object of theirs those questions do not represent."
decision: "When an agenda looks covered, read the matching section here before treating the objects as the same."
evidence: "For each agenda, say what this map already covers, then name what they still need. A nearby noun is not coverage."
external:
  - label: "Field hub"
    url: "/field/v2/"
  - label: "Appendix B"
    url: "/cards/appendix/appb/"
related:
  - "field-map-starting-points"
  - "field-coverage"
  - "what-not-claiming"
  - "six-thesis-claims"
  - "correction-channel-integrity"
  - "boundary-discovery"
  - "value-bundle-transport"
  - "grounding-viability"
---

The [coverage matrix](/field/coverage/) asks how other programs touch **this project's** questions: [where the real optimizer is](/cards/boundary-discovery/), whether [values and who they apply to](/cards/value-bundle-transport/) still travel, whether [checked symbols stay connected](/cards/grounding-viability/) to what they claim to measure, and whether [human correction still changes later behavior](/cards/correction-channel-integrity/). That matrix is a translation. It does not show that these questions are complete, or that the same English word names the same object. See [what the book is not claiming](/cards/what-not-claiming/).

For each agenda, first say what this map already covers. Then name what they still need. A nearby noun is not coverage.

## Research programs

### [MIRI](/cards/agenda/miri/)

This map already covers a thin slice of their shutdown and interruptibility results. If you have found the [real optimizer](/cards/boundary-discovery/), an off-switch on that path can shut the system down. Training a system so that interrupting it is not costly is a weaker claim than "correction still works." Those are their theorems mapped onto this project's objects. They are not replacements for their objects. Dynamical corrigibility (a system that stays correctable as it gets more capable) is treated under the [Christiano lineage](/cards/agenda/christiano-lineage/), not here.

What they still need is Soares's claim that a capable utility maximizer may *not want* to be corrected, and Vingean tiling: can an agent trust a successor it cannot inspect? Embedded-agency work still needs a map of that problem and a way to find real controllers in the wild. Finding a candidate boundary is not solving that map. [CEV](/cards/specify-cev/) still needs a specified process for whose volition is extrapolated. A claim about expected-utility theory is not a claim about whether [human correction still reaches later behavior](/cards/correction-channel-integrity/). Reflecting "I have proved my successor is safe" is not checking that the [properties we care about survive the successor](/cards/successor-stability/).

### [Redwood](/cards/agenda/redwood-research/)

Both sides already refuse "is this isolated model aligned?" This map also assumes the system may try to defeat oversight. It asks whether a monitored signal can still be trusted when [faking is cheap](/cards/certification-under-manipulation/), and whether hidden productive control is bounded. That is the same *kind* of question as control. It is not their remaining object.

They still need the measured **gap** between a trusted overseer and an untrusted model as the number that licenses a protocol: can this model defeat *this* protocol at *this* gap? A one-sided bound on hidden control, or a cap on what a short trace can show, does not score that two-sided gap. The book reframes the target. It does not replace the protocol verdict labs and governments are asked to consume.

### [CHAI / FAR.AI](/cards/agenda/chai-russell/)

This map already treats a CIRL scalar reward as the one-dimensional case of [learning a small set of value directions](/cards/goal-inference/). That embed is a translation. It does not prove that real CIRL training finds the intended target.

They still need the live assistance game: a human and a robot, a reward the robot does not know, and a joint policy that includes teaching and asking. After the scalar embed, this map still has no object for that online teaching-and-inquiry protocol. The book reframes the target, not the learning algorithm.

### [Christiano lineage](/cards/agenda/christiano-lineage/)

This map already covers a thin slice of debate, amplification, and dynamical corrigibility. Debate can track truth on a clean tree *if* the judge is already correct. Amplification: an error at a leaf gets worse, not better. Dynamical corrigibility is the same crux as [whether correction still changes later behavior](/cards/correction-channel-integrity/) as capability grows ([the dynamical guarantee](/cards/dynamical-guarantee/)). ELK as "is this reporter reading the latent, or simulating the human?" is treated under [ARC](/cards/agenda/arc-alignment-research-center/).

What remains is a *process that produces a better overseer* than the starting human: HCH, iterated amplification, debate as a training story with a bounded judge. Checking a leaf oracle is not checking that process. A stronger judge is not an uncaptured [correction channel](/cards/correction-channel-integrity/).

### [ARC](/cards/agenda/arc-alignment-research-center/)

This map already covers two ELK facts. A reporter can look right in two ways: it can read what the model actually believes, or it can guess what a human would say from the same sensors. A finite test cannot tell which one you got. And getting an answer out is not the same as the system [taking correction](/cards/correction-channel-integrity/).

They still need a training method that makes the model report what it actually believes, even when guessing the human answer would also pass the test, and even when it can tamper with the sensors humans see. Those two facts do not give that method. They also do not say how much work the system can do in secret.

### [davidad / GSAI](/cards/agenda/davidad-guaranteed-safe-ai-gsai/)

This map already covers the negative: a green certificate on a declared class, or a packed [safety case](/cards/what-not-claiming/) inside a risk budget, does not mean the deployed system is safe. This map asks whether [checked symbols stay connected](/cards/grounding-viability/) to what they claim to measure. It does not ask whether every safety-relevant phenomenon has been listed. Treating completeness as the wrong bar is not a weaker GSAI.

They still need a complete world-model and spec, plus a method that can actually close the proof. See [specify](/cards/specify-gsai/) and [construct](/cards/construct-gsai/) GSAI. Substituting "refuse when the symbol goes silent" for completeness does not host that stack.

### [Safeguarded AI (ARIA)](/cards/agenda/safeguarded-ai-aria-zeroth-heron/)

The green-case-is-not-safe point is the same as under [GSAI](/cards/agenda/davidad-guaranteed-safe-ai-gsai/) above. This map also already covers a second failure: the [named unit may not be the real loop](/cards/composite-agency/).

They still need a machine-checkable proof that a declared tuple (world model, spec, controller, runtime) satisfies the spec at the cut they named. This map's safety case is a structured refusal test: a missing leaf fails the claim. Filling that test honestly is not constructing their certificate.

### [Wentworth / natural abstractions](/cards/agenda/wentworth-natural-abstractions/)

This map does not cover their objects. There is no translation of selection theorems onto this project's [selection](/cards/goodhart-as-selector/) question, or of natural latents onto [value directions](/cards/value-bundle-transport/).

They still need theorems about which agent type a selection process implies, and compressions that survive independently of the observer. This map asks whether [deployment environments favor systems that stay correctable](/cards/attractor-control/). A type-signature theorem is not that environmental question. A natural latent is not a value direction.

### [Kosoy / LTA](/cards/agenda/kosoy-infra-bayesianism-lta/)

This map does not host their learning-theoretic theory. A side note that low regret does not bound harm is not that theory. Appendix B keeps the stack outside the book ontology.

Identifying the user as an agent in the physical world *is* their version of [finding the real optimizer](/cards/boundary-discovery/). That question is already on this map (see also [finding agents](/cards/unsupervised-agent-discovery/)). What they still need is the rest of the stack: a theory tight enough to *license* alignment claims, and a protocol that then superimitates that user's values. Finding the user is not hosting that theory.

### [CLR](/cards/agenda/clr-cooperation-conflict/)

This map already asks whether two systems look [inferentially coupled](/cards/inferential-coupling/). Coupling is not itself a trade. A full acausal-trade equilibrium is not formalized here.

They still need a theory of how competition destroys surplus or produces s-risk, including evidential cooperation as a *choice* when ordinary bargaining fails. A high coupling reading is not a recommendation to cooperate. A detector is not a decision theory. Therefore this map can say "these two look coupled" and still have no object for whether they should cooperate, or how they should bargain when ordinary deals fail.

### [Orthogonal](/cards/agenda/orthogonal/)

This map already covers the *cut* they inherit: [is the certified unit the real optimizer](/cards/boundary-discovery/)? Their Embedded Agency wall is the same problem family as [that column](/cards/mb1-boundary-estimator-soundness/). They treat the cut as a formal obstruction to close. This map treats it as a cut to measure. Their corrigibility wall is the [MIRI / CHAI](/cards/agenda/miri/) problem: a utility that accepts correction. This column's [corrigibility](/cards/mb4-correction-legitimacy/) is whether [the correction process stays intact](/cards/correction-channel-integrity/). [QACI](/cards/alignment-target/) is a proposed target, next to [CEV](/cards/specify-cev/), not a corrigibility result.

They still need a community program that *closes* those walls. Naming the walls, and listing QACI as a target, does not close them.

### [Conjecture / CoEm](/cards/agenda/conjecture-cognitive-emulation/)

This map has no object for cognitive emulation. [Whether correction has been captured](/cards/anti-capture-correction-validity/) does not mention an emulation regime.

They still need systems kept inside a human-emulation regime so controllability is architectural. Handles inside that regime can still be captured. An uncaptured [correction channel](/cards/correction-channel-integrity/) can survive after the regime is left. The two fail independently.

### [Resolution](/cards/agenda/resolution/)

Automating alignment research is itself a [capability](/cards/capability/) gain: the research process gets faster and more powerful. The pipelines that write the next proofs and systems are [successors](/cards/successor-stability/). This map already asks whether [certification still holds when the system can manipulate the check](/cards/certification-under-manipulation/), and whether named conditions still connect.

They still need those pipelines to scale to superintelligent alignment with checkable confidence. A compact consistency check does not say whether that scale is the bottleneck. A more capable, automated research process also does not, by itself, keep successors safe.

## Labs and evaluation

### [Anthropic / Goodfire](/cards/agenda/anthropic-lab/)

This map does not cover feature-level interpretability of a trained model, or a laboratory scaling policy. [Constitutional AI](/cards/specify-constitutional-ai/) is one proposed target. Claiming a builder is not showing that the lab built it. Circuits and sparse autoencoders are not treated here as alignment solutions.

They still need to see and steer the features of *this* trained model, plus a lab process that gates deployment as capability grows. Seeing those weights is not an object here. A lab policy is not a structured refusal test on [whether tracking still holds](/cards/alignment-as-measurement/).

### [Google DeepMind safety](/cards/agenda/google-deepmind-safety/)

Debate and amplification stay with the [Christiano lineage](/cards/agenda/christiano-lineage/). [Finding agents](/cards/unsupervised-agent-discovery/) is this map's first step, not their co-scaling race.

They still need in-house oversight that keeps up with the lab's own capability run. Sharing the word "oversight" does not make this project's measurement questions into that lab-internal program.

### [Apollo / Truthful AI](/cards/agenda/apollo-research/)

This map does not cover their eval gate. Bounds on hidden control sit with [Redwood](/cards/agenda/redwood-research/). Apollo does not use that quantity.

They still need a pre-deployment scheming eval: red or green on deception or model-organism tests for a named model. This map asks where [opacity](/cards/strategic-opacity/) sits around control-relevant variables. An eval verdict on a model is not a localization of [where the optimizer is](/cards/boundary-discovery/).

### [METR](/cards/agenda/metr/)

This map does not cover their quantity. Public evaluations are an indirect signal here, not their number.

They still need how long a model can work autonomously, and entity-level assessment, as risk numbers a lab or policymaker can act on. Neither number is hosted here. A green reading is not a [correction-channel](/cards/correction-channel-integrity/) result.

### [CIRIS](/cards/agenda/ciris/)

CIRIS is largely [construction](/cards/target-realization/): a shipped constitution, runtime, and attestation stack. This map does not yet cover how to build a system that tracks the target. The one measurement point already on the map is the negative: a green named path is not the [intervening loop](/cards/composite-agency/).

## Institutions, forecasts, and construction of the field

### [GovAI / UK AISI](/cards/agenda/govai/)

This map's [selection](/cards/attractor-control/) question does not map here. Their crux is whether an institute evaluation or policy instrument *binds* under race, not whether deployment environments favor systems that stay correctable.

They still need evaluations and policy that actually stop or gate deployment while others are racing. A halt that fired is an institutional fact. [Channel integrity](/cards/correction-channel-integrity/) is a causal property: whether legitimate judgment still reaches handles that change later behavior. A halt can fire while the channel is theater. A channel can stay intact while no institute has bound anyone. Neither implies the other.

### [Pause / standards advocacy](/cards/agenda/pause-standards-advocacy-cluster/)

This much is already covered: if a pause actually withholds who can deploy, it can change which systems get copied, and therefore the [selection](/cards/goodhart-as-selector/) environment. A stable environment can still be a bad one. Off-switch language in their platforms is an advocacy priority, not this map's one-bit shutdown claim.

They still need a slowdown that *binds*: law, tracked compute, and verification that other parties cannot defect, without the governance failure their crux names. "Does selection still favor correction?" is not a theory of legislation or coalition enforcement.

### [MAI + CIP](/cards/agenda/mai-cip-institutional-alignment/)

This map does not cover their object. An [institutional specify / construct pair](/cards/specify-institutional/) on the field hub is a nearby analogue, not coverage.

They still need thick values produced by a contestable deliberative process. [Whether correction has been captured](/cards/anti-capture-correction-validity/) is not a source of legitimacy. Two legitimacy orderings can disagree on a technically invariant change. A legitimate assembly is not recoverable [value structure](/cards/value-bundle-transport/), and a consensus text is not a map of [who the values apply to](/cards/bearer-persistence/).

### [AI Futures / forecasting](/cards/agenda/ai-futures-forecasting-cluster/)

This map does not cover their object. Forecasts are reused here as schedule cues, not as the thing under test.

They still need trackable *when* (scored scenarios, TAI estimates, prediction infrastructure) as the dominant uncertainty. This map uses timelines as urgency, not as a mechanism. A date is not a failure mode. A labeled failure mode is not a forecast.

### [Iliad / Textbook from the Future](/cards/agenda/iliad-textbook-from-the-future/)

Iliad is trying to coordinate a whole research programme with a communal living textbook; this map is one author's measurement questions, not that instrument.

### [Neglected approaches portfolio](/cards/agenda/neglected-approaches-portfolio/)

This portfolio bets on many underused shots, such as [self-other overlap](https://arxiv.org/abs/2412.16325). This map has no object for neglectedness as a strategy, and does not host those targets. [Finding agents](/cards/unsupervised-agent-discovery/) is this project's own line, not the portfolio.

## Field-building

Roster type **capacity**: pipeline, pedagogy, or sprint velocity. This map asks whether we can tell that a system [still tracks](/cards/alignment-as-measurement/). None of the five has an object for that. Matrix cells that look covered are vocabulary overlap. **Structural** field construction (changing stop authority, evaluator independence, or who can deploy) is a different type — tagged on the agenda card, not as a green coverage cell. See [alignment lifecycle](/cards/alignment-lifecycle/) for construction and convergence.

### [CAIS](/cards/agenda/cais-field-building/)

They need coordinated risk statements, a recognized x-risk course, and events that make that framing actionable for labs and policymakers. Success is legitimacy of the framing plus more people entering the work. The program does not commit to a single technical path.

Advocacy can succeed completely while every measurement question stays unanswered. A public statement that uses the same English words as this project's cards is vocabulary overlap. A legitimate field is not a composed answer.

### [BlueDot Impact](/cards/agenda/bluedot-impact/)

They need introductory curricula and the career placement that follows. Success is a completed course and a placed graduate who can read the field's vocabulary.

Teaching someone the words "oversight" or "measurement" is not measuring a [correction channel](/cards/correction-channel-integrity/). A graduate who can read this site is not a result on any of its questions.

### [MATS](/cards/agenda/mats/)

They need a mentored pairing that produces substantive output in one term. Mentorship output is *supposed* to stay diverse across interpretability, control, transparency, and security. Diversity is a success condition, not a side effect.

This map's bet is the opposite: one composition of its questions, or a named block. A green year for MATS is many good projects that stay in different subfields. A good paper is not that composition. If the program collapsed onto one spine, MATS would have failed its own diversity criterion.

### [Apart Research](/cards/agenda/apart-research/)

They need open research sprints: a shipped artifact in a short burst. Those artifacts do not imply a load-bearing [safety case](/cards/what-not-claiming/). They need separate checks before they warrant deployment trust.

Sprint velocity can be high while every measurement question stays open. A demo that uses the same English as a card here is vocabulary overlap. A demo is not a refusal test.

### [Kairos](/cards/agenda/kairos-field-building/)

They need talent found and placed: mentored research, career programs, workshops, residencies. The bottleneck they are not solving is mechanism discovery.

Finding people is not finding a mechanism that survives optimization. Field-building scale can succeed while every measurement question stays unanswered.

## This project

### [Towards Superintelligence Alignment](/cards/agenda/this-project-towards-superintelligence-alignment-tsa/)

This map tracks whether the [named questions](/cards/six-thesis-claims/) still connect: what should be tracked, whether we can tell that a given system still tracks it, and [whether recovery can still land](/cards/scope-and-correction-capacity/). That is this map's success object. See the [pointing problem](/cards/pointing-problem/) for how the field sometimes folds those questions together.

It does not represent [how to build](/cards/target-realization/) a system that tracks the target, a communal canon, or a procedure for noticing a primitive these slots cannot name. Connecting the measurement questions is not those three objects. Those absences are the same kind of miss this card records for everyone else.
