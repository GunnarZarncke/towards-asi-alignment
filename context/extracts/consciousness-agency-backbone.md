# Extract: consciousness_agency_backbone.pdf

**Source PDF:** `context/consciousness_agency_backbone.pdf`
**Extract:** `context/extracts/consciousness-agency-backbone.md`
**Pages:** 4
**Note:** Auto-extracted for agent/manuscript use. Display equations use `$$...$$`; Unicode math symbols are converted to LaTeX where possible.

A Minimal Architectural Proposal for Consciousness and Agency
on a Shared Neural Backbone
Gunnar Zarncke (AE Studio)
August 2025
Abstract
We propose a compact systems-level architecture that separates shared machinery from
differential add-ons to describe the overlap and differences of consciousness and agency. We
propose that the shared neural backbone of both comprises (i) a learned generative model,
(ii) attention/gain control, and (iii) a short temporal buffer. On top of this, two neural
processing stacks branch: a consciousness stack (global broadcast and metacognition) and
an agency stack (valuation register and efference cascade).
1
Motivation and scope
Consciousness is used here in a minimalist, operational sense: contents becoming globally
available to disparate subsystems and accessible for report [Dehaene, 2014, Dehaene and Naccache,
2001]. Agency denotes the capacity to initiate and control actions according to goals, treating
systems as if they have beliefs and desires when this makes good predictions for behavior
[Dennett, 1987, 1971]. The two frequently co-occur in humans but neither logically entails the
other; the architecture below explains the overlap and the dissociations.
The proposal is intentionally model-agnostic. It does not presuppose any specific theory of
consciousness or control, and it requires only three building blocks that are broadly accepted
in computational neuroscience: predictive modelling [Friston, 2010], attention-like gain control
[Sarter et al., 2023], and short-horizon working memory [Miller and Buschman, 2015].
2
Backbone and add-ons: informal specification
Let st be latent states, ot sensations, and at actions. The backbone maintains a predictive

$$
mapping p(ot+1 | st) and a belief update q(st+1 | st, ot+1) over a buffer of length \tau \in[0, 2 s]. A
$$

generic attention/gain process \alphat modulates precision.
Two add-on stacks branch from this backbone:
• Consciousness stack: (C1) Global broadcast hub—a routing mechanism that makes
selected contents available system-wide; (C2) Metacognitive monitor—confidence/error-
likelihood tagging of those contents.
• Agency stack: (A1) Valuation register—a critic-like scalarising function over states
and options [Salge et al., 2014]; (A2) Efference cascade—an actor-like path from selected
policies to motor/effector channels with forward models (efference copy) [Popa and Ebner,
2018].
1

---

Figure 1: Schematic separation of common machinery (backbone) from differential add-ons for
consciousness and agency. The same predictive core serves both stacks; dissociations arise when
an add-on fails or is absent.
3
Diagram: shared backbone with differential add-ons
4
Functional roles and minimal predictions
Table 1 states each component’s role and gives testable signatures that do not depend on a
specific neural implementation.
Component
Functional role
Discriminating operational signatures
Generative model
Maintain a compact, predictive scene
state; bind multi-modal inputs over
∼2 s Burgess et al. [2019], Greff et al.
[2019], Locatello et al. [2020]
Violations trigger transient error bursts; im-
agery substitutes for input with matched
dynamics
Attention/gain
Allocate precision to task-relevant
channels Locatello et al. [2020]
Manipulating gain selectively boosts reporta-
bility or control without changing stimuli
Temporal buffer
Provide a rolling workspace for bind-
ing and comparison Kirchhoff et al.
[2018a,b]
Lengthening/shortening window shifts inte-
gration of rapid sequences (e.g., speech, ac-
tions)
Global broadcast (C1)
Make selected contents globally avail-
able Kirchhoff et al. [2018a,b]
Loss yields competent behaviour without ac-
cess/report ("islands"), or vice versa
Metacognition (C2)
Tag contents with confidence/error
likelihood Kirchhoff et al. [2018b]
Dissociable from task performance; manipu-
lations shift confidence at fixed accuracy
Valuation register (A1)
Scalarise options via value or cost
Kirchhoff et al. [2018b]
Predicts discounting curves and effort allo-
cation; lesions flatten gradients
Efference cascade (A2)
Translate selected policies into actions
with forward models Kirchhoff et al.
[2018b]
Loss yields intact intent/report but failed
execution; efference copy suppresses self-
generated reafference
Phenomenal report
Externalisation of selected contents
for report or communication Kirch-
hoff et al. [2018b]
Report channels can be blocked while inter-
nal access remains (e.g., output bottlenecks);
readouts include verbal report, button press,
or eye-tracking
Motor execution
Physical realisation of selected poli-
cies via corticobasal and cerebellar
loops Kirchhoff et al. [2018b]
TMS/lesion yields intention–execution gaps;
efference copy suppresses self-generated reaf-
ference, and failures cause sensory instability
Table 1: Roles and generic signatures of backbone and add-ons.
5
Why the architecture explains co-occurrence and dissociation
Because both stacks share the same predictive core, they tend to co-occur in organisms with
rich models. Yet each add-on can fail independently:
• (C1) breakdown: intact skilled behaviour with impoverished access/report.
2

---

• (A2) breakdown: intact experience of intending with impaired execution.
• (C2) breakdown: normal performance but unreliable confidence control.
• (A1) breakdown: intact perception but apathetic or chaotic policy selection.
These double-dissociations are the architectural expectation, not anomalies.
6
Outputs: Phenomenal report and motor control
Phenomenal report
We use “report” operationally in the sense of Dehaene [Dehaene, 2014]: any externally verifiable
channel by which globally broadcast contents are read out (speech, button presses, saccade
targets). The report channel is downstream of broadcast and metacognition; it can therefore
fail independently. Minimal predictions: (i) selective output interference (e.g., speech block)
diminishes report without changing internal access; (ii) confidence manipulations shift report
thresholds at matched accuracy. This operational approach allows detection of consciousness
across species, particularly mammals, through neural patterns comparable to humans during
reportable experiences.
Motor control
Motor execution is the physical realisation of selected policies. A forward model (efference copy)
predicts reafferent input so that perception remains stable during movement. Minimal predictions:
(i) perturbing motor pathways leaves intention judgements intact while degrading execution; (ii)
disrupting efference copy induces reafferent confusion (e.g., tickle paradox breakdown).
The agency stack’s applicability extends across species where observable intentional behavior
can be detected [Dennett, 1987].
Summary.
A small set of shared mechanisms plausibly underwrite both consciousness and
agency. Two compact add-on stacks account for their frequent coupling and their separable
failure modes. This provides a neutral scaffold for cumulative experiments and for comparison
with more detailed theories.
References
Chris P Burgess et al. Monet: Unsupervised scene decomposition and representation. arXiv
preprint arXiv:1901.11390, 2019.
Stanislas Dehaene.
Consciousness and the Brain: Deciphering How the Brain Codes Our
Thoughts. Viking, New York, 2014.
Stanislas Dehaene and Lionel Naccache. Towards a cognitive neuroscience of consciousness:
basic evidence and a workspace framework. Cognition, 79(1-2):1–37, 2001.
Daniel C Dennett. Intentional systems. Journal of Philosophy, 68(4):87–106, 1971.
Daniel C Dennett. The Intentional Stance. MIT Press, Cambridge, MA, 1987.
Karl Friston. The free-energy principle: a unified brain theory? Nature Reviews Neuroscience,
11(2):127–138, 2010.
Klaus Greff et al. Iodine: Multi-object representation learning with iterative variational inference.
arXiv preprint arXiv:1903.00450, 2019.
3

---

Michael Kirchhoff et al. The markov blankets of life. J. R. Soc. Interface, 15(138), 2018a.
Michael D Kirchhoff, Thomas Parr, Ester Palacios, Karl Friston, and Julian Kiverstein. The
markov blankets of life: autonomy, active inference and the free energy principle. Journal of
the Royal Society Interface, 15(138):20170792, 2018b.
Francesco Locatello et al.
Object-centric learning with slot attention.
arXiv preprint
arXiv:2006.15055, 2020.
Earl K Miller and Timothy J Buschman. Working memory capacity: Limits on the bandwidth
of cognition. Daedalus, 144(1):112–122, 2015.
Laurentiu S Popa and Timothy J Ebner. Cerebellum, predictions and errors. Frontiers in
Cellular Neuroscience, 12:524, 2018.
Christoph Salge, Cornelius Glackin, and Daniel Polani. Empowerment: a universal agent-centric
measure of control. Proceedings of the 2013 IEEE Congress on Evolutionary Computation,
pages 2375–2383, 2014.
Martin Sarter et al. Cholinergic genetics of visual attention: human and mouse choline transporter
capacity variants and attention. Biological Psychiatry, 93(4):331–339, 2023.
4
