Source URL: https://www.lesswrong.com/posts/quC3LLPXCashfnKZY/the-open-problems-of-the-ai-alignment-field-and-their-cruxes
Source file: context/The Open Problems of the AI Alignment Field and their Cruxes — LessWrong.pdf (deleted after extract)
Extracted: 2026-11-15 (pypdf text layer; formatting may differ from live LW)

# The Open Problems of the AI Alignment Field and their Cruxes

<!-- page 1 -->

The Open Problems of the AI
Alignment Field and their Cruxes
by Gunnar_Zarncke 6th Aug 2026
Previous: AI Safety Interventions
TL;DR: I made an overview of the open problems of AI alignment that reveals cruxes
within those open problems and missed opportunities for formalization and
collaboration. And CEV  may deserve a second look.
Epistemic status: Trying too much in too little time. I'm confident I have identified
and modeled significant structure within the alignment field, but I urgently need
feedback on specific gaps and this post is largely a call for that. My work was LLM-
assisted, but no part of this post was LLM-written, except for the crux summary and
the Lean code.
Recently, Chi Nguyen and peterbarnett said: PSA: Almost nobody is directly working
on superintelligent alignment . I have been around in the field since the old days of
LW 1.0 and thought: that can't be true. I mean, so many people seem to be working
on it. I thought I was working on it. But was I? The PSA made me think back on what
I was actually working on. It was Steven Byrnes who came up with a research agenda
I could actually contribute to, which led me to founding project aintelope  in 2022
(PS. It is still going). And a while back, I compiled a report on AI Safety Interventions
 for AE Studio, so I thought I was kind of up-to-date on research agendas. Now, is
that superintelligence alignment? Or is that more prosaic normal alignment? Maybe
each individual research is normal, boring, but does all of that research together
actually cover all areas?
So I set out to collect the evidence and find and piece all the research agendas
together, and connect to all of our field's open problems. This involved finding all the
agendas, naming the open problems, and finding the evidence of each agenda for
Agent Foundations AI Control Corrigibility Crux Research Agendas AI World Modeling Frontpage
52

<!-- page 2 -->

each problem. The first was easy, thanks to the people who maintain sites like
aisafety.com (thanks guys for the great map!), my previous work, and other such
resources (and aided by LLM search). The second was the hardest, as it involved
getting a good understanding of the cruxes within the open problems and how they
relate. That took most of the time. I am not reporting on all the details here; I owe
you more posts on that. But once the modeling and structuring was done, putting it
all together was again easy. The result is the pretty big table below (full clickable
version can be found on my website, the tags classify evidence: C conceptual, T
theory, S simulation, P practical, D empirical (software), E empirical (other), O other):

<!-- page 3 -->

This table shows some interesting patterns:
Many cells are empty. In fact, some columns are almost empty.
Some columns are crowded.
Some columns have dominant types of evidence.
There is little practical or applied evidence ("P") that I could find.
And I think you can spot more patterns. Each pattern can have multiple explanations.
For example, a group of empty cells can mean that some areas are genuinely
neglected and more people should work on them. It can mean an open problem or
crux was dissolved, i.e., there is actually no longer a need to work on it, or it isn't
load-bearing anymore. Or it could be a coding error on my side. The open problems
Value Referents (MB3, part of Value Learning), Tiling  (MB5), Acausal Coordination
(MB7d), and CEV (MB8) seem to have little evidence. Is that because matching them
with existing research is hard? Due to a lack of shared terminology? Or is it because
of errors in my modeling? Relatedly, the last row, my work, Towards
Superintelligence Alignment (TSA), appears to span everything, but that is simply
because I know how my work relates, and can easily link it. Also, it is largely of a
different type than the other evidence - no published papers but mostly simulations.
So don't treat that as comprehensive coverage but as advertisement. But it reminds
that visibility of agendas and publication matter for the other cells too. The matrix
doesn't tell why cells are empty and why the patterns are there, but the answer seems
important. It is clear that alignment must cover the columns against a
superintelligent adversary. But the matrix also doesn't tell us yet if each cell delivers.
• • •
The second thing I want to elaborate on a bit more is some structure within the open
problems. As far as I can ascertain, the open problems are Embedded Agency , Value
Learning , Corrigibility , Tiling , Goodhart Selection (the principle behind Gradual
Disempowerment ), Inner Alignment , Acausal Coordination , Extrapolated Volition
, Grounding Drift , Successor Gaming, and Deployment Safety (the crucial part of AI
Control ).
I have done some modeling of the open problems to figure out how they relate. I tried
to reduce each open problem to a proposition that can be true or false. I call these
propositions bridges. Doing so forced splitting Value Learning  into Value Learning
LLM assisted with Cursor Composer Fast: Summary of open problems from my
site (lightly edited)

<!-- page 4 -->

proper (MB2) and Value Referents (MB3). I had to split Corrigibility  into technical
Corrigibility proper (MB4) and Audit Independence (MB4a). And I pulled Acausal
Coordination  (MB7d) out of Inner Alignment . That means that the column
headers of the matrix name two things: the open problem people are working on and
the matching bridge proposition they have to make hold.
Why did I need to split Corrigibility? Because oversight alignment protocols
like Debate  require a human or judge. They do not get integrity from the protocol
score alone. Let me illustrate this. We know from Irving that Debate tracks
truth if the judge is correct. The Lean code includes his finite claim-tree debate game
with soundness, completeness, and a one-judge-error-flips-certification result. From
that it follows that one judge error flips the outcome, and that leads to false
certification.
We can model that "Debate selects truth" can hold while the judge’s correction
channel (how its judgement actually makes it into the Debate) is compromised.
Thus we know that we need a bridge - MB4 - that assumes (for now) that we can
certify that the judge's judgement is not compromised.
Source: formal/AlignmentProofSpine/Field/Finite/DebateGame.lean / Field/Debate.lean
Source: Correction.lean 
Source: formal/AlignmentProofSpine/Core.lean
You can check it in the repo.
And so it goes for all the open problems. You think of a crux. You find
counterexamples that motivate a split. You need to find a way to model that some
part of the system may be compromised, thus you need to pass data. I (with Fable)
have made some effort to rederive or model existing formalizations in Lean (this
folder in the repo), represent the cruxes, and connect them to the overall proof spine.
Maybe I will write a longer post on the Lean code later. If you work on the above-
[1]
Fable: Lean code for theorem debate _ tracks _ truth
Fable: theorem debate _ truth _ separated _ from _ judge _ correction _ step
Fable: MB4 — correction integrity implies the correction operator is preserved
Shell code to check out the code, compile Lean, and print the axioms on the above
examples.

<!-- page 5 -->

shown Debate, or on CIRL, ELK, shutdown, interruptability, or AUP, you can find
translations of theorems from these into Lean on my Lean overview page. Twelve
derivations where you can prove me wrong.
• • •
Overall, the dependencies between the propositions of the cruxes seem to be as
follows (red edges indicate logical entailment between propositions, black indicates
composition; intermediate steps not shown in this diagram):
If this logical dependency is about a real structure of the alignment problem, then
this would give Chi Nguyen and peterbarnett's ask an angle of attack. It may give you
a hint on what to work on. You may not have to work on "all of it". For example,
working on cruxes further up the dependency tree may unblock, in some sense,
cruxes further down.  It doesn't mean people can't work on all of them at the same[2]

<!-- page 6 -->

time - people clearly do; just look at the matrix above - but this graph may help
clarify which teams should work closer together.
The structure shows that CEV  seems to be an alternative route, and making progress
on it may provide an alternative angle of attack, bypassing five other cruxes. Or it
may be that CEV is unsolvable (after all, it is modeled as a black box and thus has no
inputs), and that's why people have given up on it and the cells are empty.
So after doing this, do I feel I am answering Chi Nguyen and peterbarnett's call? Yes
and no. Yes. I have added structure. But also no: The hard parts are still there. More
people working on the agendas have to look at their cells. And people from other
agendas - or even you - should provide the outside view too and analyse patterns and
gaps. You are welcome to collaborate and contribute to (or fork) the repo with
corrections, additions, and whatever helps improve this overview of the alignment
field. Get in touch.
1. Actually, and maybe more controversially, I had to split Inner Alignment  into three more
elements: Access Model Soundness (MB7a), Filter Coverage (MB7b), and Bounded Hidden
Capability (MB7c), beside the mentioned better-known Acausal Coordination  (MB7d). The
matrix doesn't show this split because it wasn't feasible for me to break down the evidence to
this resolution.
2. Entailment is not tractability. Whether the logical order between the bridge proposition
relates to research order is the kind of thing I'd like you to check.
^
^
Moderation Log
