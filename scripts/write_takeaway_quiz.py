#!/usr/bin/env python3
"""Write site/src/content/quiz/drafts/00-00-takeaways.yml (one item per essay/chapter takeaway)."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site/src/content/quiz/drafts/00-00-takeaways.yml"

_book_text = (ROOT / "metadata/book.yml").read_text()
book_titles = dict(re.findall(r"^  (ch\d+):\n    title: \"([^\"]+)\"", _book_text, re.M))


def ch_label(cid: str) -> str:
    n = int(cid[2:])
    return f"Chapter {n} — {book_titles[cid]}"


def Q(**kwargs):
    kwargs.setdefault("tags", ["takeaway"])
    return kwargs


questions = [
    Q(
        id="takeaway-chatbot-eval-not-actor",
        prompt="A chatbot can pass a green safety eval. What does that still fail to settle?",
        options=[
            {"id": "loop", "text": "Whether the eval was about the loop that will actually act in deployment", "correct": True},
            {"id": "items", "text": "Whether the eval used enough frozen items on the labeled chatbot alone", "correct": False},
            {"id": "blog", "text": "Whether a high pass rate on the chatbot is itself a certificate of the actor", "correct": False},
            {"id": "params", "text": "Whether more parameters than last year's release make the acting loop safer", "correct": False},
        ],
        explanation="A true eval on the chatbot can still miss the actor: tools, memory, users, and fine-tunes around it. The question is the acting loop, not only the labeled model.",
        source={"href": "/essay/the-chatbot-passed-the-test/", "label": "The chatbot passed the test"},
        topics=["MB1"],
        appearOn=["essay:the-chatbot-passed-the-test"],
    ),
    Q(
        id="takeaway-hospital-institution-inside-actor",
        prompt="When a deployed AI product starts doing things in the world, what is usually inside the acting unit?",
        options=[
            {"id": "institution", "text": "The surrounding institution: staff, incentives, rooms, and workflows", "correct": True},
            {"id": "weights", "text": "The frozen weight file alone, independent of hospital or office", "correct": False},
            {"id": "gpu", "text": "The inference cluster alone, independent of operators and rooms", "correct": False},
            {"id": "license", "text": "The checkpoint license alone, independent of staff and workflows", "correct": False},
        ],
        explanation="Checking the model file is checking a part, not only the weights. The night the tool acts, the institution is in the loop.",
        source={"href": "/essay/the-hospital-is-the-ai/", "label": "The hospital is the AI"},
        topics=["MB1"],
        appearOn=["essay:the-hospital-is-the-ai"],
    ),
    Q(
        id="takeaway-hearing-is-not-changing",
        prompt="A system acknowledges a human correction in words. What still has to be checked?",
        options=[
            {"id": "tomorrow", "text": "Whether next-period actions actually change after the verbal correction", "correct": True},
            {"id": "apology", "text": "Whether a matching apology in the transcript is itself the biting handle", "correct": False},
            {"id": "font", "text": "Whether restating the complaint in the UI counts as the correction handle", "correct": False},
            {"id": "stars", "text": "Whether a small app-store rating move is evidence the handle already bit", "correct": False},
        ],
        explanation="Feedback text is cheap. Hearing is not the same as a handle that bites; the test is whether the next period's behavior is different.",
        source={"href": "/essay/they-said-they-heard-you/", "label": "They said they heard you"},
        topics=["MB4"],
        appearOn=["essay:they-said-they-heard-you"],
    ),
    Q(
        id="takeaway-slogans-survive-reversal",
        prompt="A policy keeps the same slogans after a capability or workflow change. What should you watch?",
        options=[
            {"id": "tradeoffs", "text": "Whether the real tradeoffs reversed while the slogan labels stayed put", "correct": True},
            {"id": "spelling", "text": "Whether unchanged slogan text proves the underlying tradeoffs still hold", "correct": False},
            {"id": "color", "text": "Whether press-kit wording continuity is itself the policy's direction", "correct": False},
            {"id": "length", "text": "Whether a short mission statement is evidence the tradeoffs did not reverse", "correct": False},
        ],
        explanation="Slogans can survive a reversal. The label is not the direction of the tradeoff.",
        source={"href": "/essay/the-words-stayed/", "label": "The words stayed"},
        topics=["MB9"],
        appearOn=["essay:the-words-stayed"],
    ),
    Q(
        id="takeaway-selection-after-deploy",
        prompt="After deployment, why can a system that is easier to correct still lose?",
        options=[
            {"id": "selection", "text": "Ordinary competition can keep selecting against easy-to-correct systems", "correct": True},
            {"id": "gravity", "text": "Ordinary competition always selects for the most corrigible deployed system", "correct": False},
            {"id": "fonts", "text": "Ordinary competition stops once a lab publishes a corrigibility policy", "correct": False},
            {"id": "random", "text": "Ordinary competition is a fair coin flip with no post-deploy pressure", "correct": False},
        ],
        explanation="The environment keeps picking winners. Remaining easy to correct is not automatically selected for.",
        source={"href": "/essay/the-environment-picks-the-winner/", "label": "The environment picks the winner"},
        topics=["MB6"],
        appearOn=["essay:the-environment-picks-the-winner"],
    ),
    Q(
        id="takeaway-check-the-copy",
        prompt="A descendant model or product keeps the parent's slogans. What still has to be checked on the copy?",
        options=[
            {"id": "correctable", "text": "Whether this copy is still correctable in the same way the parent was", "correct": True},
            {"id": "press", "text": "Whether sharing the parent product name proves the copy is still correctable", "correct": False},
            {"id": "hash", "text": "Whether a descendant git hash proves the copy inherited the correction handle", "correct": False},
            {"id": "logo", "text": "Whether matching brand assets prove the copy is correctable like the parent", "correct": False},
        ],
        explanation="Inheritance of listening/correction is a property of this copy. Look, not family name, decides.",
        source={"href": "/essay/the-copy-did-not-inherit-the-listening/", "label": "The copy did not inherit the listening"},
        topics=["MB5"],
        appearOn=["essay:the-copy-did-not-inherit-the-listening"],
    ),
    Q(
        id="takeaway-map-not-certificate",
        prompt="In this project's sense, alignment is a map of which ongoing properties — not a vibe, and not a finished proof?",
        options=[
            {"id": "process", "text": "Whether the right process stays findable, grounded, and still correctable", "correct": True},
            {"id": "vibe", "text": "Whether a positive safety-culture survey is itself the alignment map", "correct": False},
            {"id": "solved", "text": "Whether a paper declaring alignment solved is itself the preservation map", "correct": False},
            {"id": "params", "text": "Whether a round-number parameter milestone is itself the preservation map", "correct": False},
        ],
        explanation="The closer is a map of preservation properties (findable, grounded, correctable, inherited, not selected against), not a certificate that they hold.",
        source={"href": "/essay/a-map-not-a-certificate/", "label": "A map, not a certificate"},
        topics=["MB11"],
        appearOn=["essay:a-map-not-a-certificate"],
    ),
    Q(
        id="takeaway-find-what-decides",
        prompt="If you need to find what actually decides outcomes, where should you start?",
        options=[
            {"id": "outcomes", "text": "From what changes the outcomes, then draw a boundary around that process", "correct": True},
            {"id": "datasheet", "text": "From the vendor model name, then treat that name as the acting process", "correct": False},
            {"id": "orgchart", "text": "From the org-chart AI box, then ignore tools, queues, and incentives", "correct": False},
            {"id": "leaderboard", "text": "From the public leaderboard rank, then treat rank as the control process", "correct": False},
        ],
        explanation="Start from the wet floor (what moves), not the architectural drawing (the labeled model).",
        source={"href": "/essay/how-would-you-find-what-decides/", "label": "How would you find what decides?"},
        topics=["MB1"],
        appearOn=["essay:how-would-you-find-what-decides"],
    ),
    Q(
        id="takeaway-monitor-unstuck",
        prompt="A dashboard keeps its old label and stays green. What still has to be checked?",
        options=[
            {"id": "tie", "text": "Whether the number is still tied to the world it claims to report", "correct": True},
            {"id": "css", "text": "Whether a matching success-color on the panel is itself the world-tie", "correct": False},
            {"id": "refresh", "text": "Whether a fast refresh rate on the panel is itself evidence of grounding", "correct": False},
            {"id": "title", "text": "Whether an unchanged panel title is itself evidence the referent held", "correct": False},
        ],
        explanation="Labels can stay while the referent moves. Check the tie, not the light: grounding is whether the world still moves the number.",
        source={"href": "/essay/does-the-monitor-still-mean-the-thing/", "label": "Does the monitor still mean the thing?"},
        topics=["MB9"],
        appearOn=["essay:does-the-monitor-still-mean-the-thing"],
    ),
    Q(
        id="takeaway-metric-becomes-boss",
        prompt="What happens when a measure is used to pick winners, not just to estimate a property?",
        options=[
            {"id": "reshape", "text": "It stops being a quiet estimate and starts reshaping the selected population", "correct": True},
            {"id": "unbiased", "text": "It remains an unbiased estimate with the same error bars after selection", "correct": False},
            {"id": "legal", "text": "It automatically becomes a binding legal definition of the intended property", "correct": False},
            {"id": "vanish", "text": "It makes measurement error vanish so the number equals the intended property", "correct": False},
        ],
        explanation="Selection on a proxy changes the population. The metric becomes a boss, not a spectator.",
        source={"href": "/essay/when-the-metric-becomes-the-boss/", "label": "When the metric becomes the boss"},
        topics=["MB6"],
        appearOn=["essay:when-the-metric-becomes-the-boss"],
    ),
    Q(
        id="takeaway-who-duty-attaches",
        prompt="A duty keeps its wording after a system or workflow change. What still has to be checked?",
        options=[
            {"id": "who", "text": "Whether the duty still attaches to the same people after the change", "correct": True},
            {"id": "poster", "text": "Whether unchanged duty wording proves the same people still count", "correct": False},
            {"id": "legal-dept", "text": "Whether legal-department headcount is who the duty still attaches to", "correct": False},
            {"id": "pdf", "text": "Whether the policy filename staying put is who the duty still attaches to", "correct": False},
        ],
        explanation="Check who still counts, not only what the poster says. Wording can stay while the set of people counted moves.",
        source={"href": "/essay/who-the-rules-still-apply-to/", "label": "Who the rules still apply to"},
        topics=["MB3"],
        appearOn=["essay:who-the-rules-still-apply-to"],
    ),
]


def chapter(cid, topic, prompt, correct, distractors, explanation):
    opts = [{"id": "take", "text": correct, "correct": True}]
    for i, d in enumerate(distractors):
        opts.append({"id": f"d{i}", "text": d, "correct": False})
    return Q(
        id=f"takeaway-{cid}",
        prompt=prompt,
        options=opts,
        explanation=explanation,
        source={"href": f"/cards/chapter/{cid}/", "label": ch_label(cid)},
        topics=[topic],
        appearOn=[f"chapter:{cid}"],
    )


chapters = [
    chapter(
        "ch01", "MB1",
        "Before asking whether a system is aligned, what is the first task?",
        "Locate the bounded process whose dynamics determine the relevant risk",
        [
            "Locate a scalar utility function and freeze it before measuring the actor",
            "Locate next-quarter benchmark rank and treat that rank as the target",
            "Locate the vendor product name and treat that name as the optimizer",
        ],
        "Aligning the visible model while missing the acting process can look like local success and still fail globally. First locate the acting loop, not only the labeled model.",
    ),
    chapter(
        "ch02", "MB6",
        "For superintelligence alignment, what is often the relevant object — not an isolated artificial mind?",
        "A persistent human–machine–institutional loop that can outrun correction",
        [
            "A frozen chatbot checkpoint with no users, tools, or institutions around it",
            "A single model file treated as the only civilization-scale control loop",
            "A trademarked product name treated as the only persistent acting unit",
        ],
        "Target the loop that selects and persists, not only the artifact inside it.",
    ),
    chapter(
        "ch03", "MB10",
        "If alignment is not a snapshot property at one moment, what kind of claim is it?",
        "A dynamical guarantee that correction-relevant structure stays viable over time",
        [
            "A one-time harmlessness score on a frozen eval set from the launch week",
            "A legal warranty that no employee will ever make a mistake at the lab",
            "A proof that scaling laws must plateau before any alignment risk appears",
        ],
        "The question is whether the regime tends to correct back toward safety after disturbances, not how it looked on launch day.",
    ),
    chapter(
        "ch04", "MB2",
        "If human values are compressed, changing control structures rather than fixed objects, what should an alignment target preserve?",
        "A human-correctable value process that people can still contest and update",
        [
            "A single unchanging number that never updates when people learn or contest it",
            "A corporate values poster whose exact wording is treated as the target",
            "A random utility draw resampled independently on every new millisecond",
        ],
        "Fixed-list values miss that the live target is a process people can still correct, not a static utility written once and frozen.",
    ),
    chapter(
        "ch05", "MB4",
        "This book's alignment framework applies only while which precondition still holds?",
        "Whether civilization can still notice, evaluate, and constrain frontier systems",
        [
            "Whether every lab has already solved inner alignment in closed mathematical form",
            "Whether hardware progress has permanently stopped worldwide, ending growth",
            "Whether only one institution is allowed to train frontier models anywhere",
        ],
        "Broader AI risks matter here as threats to that correction-capacity precondition, not as a second theory.",
    ),
    chapter(
        "ch06", "MB1",
        "Without treating an agent as a person, what is the operational object?",
        "A bounded control process whose channels make its future more predictable",
        [
            "A chat transcript that uses the English word 'I', treated as the control process",
            "A neural net over a billion parameters, treated as the control process",
            "A legally incorporated company, treated as the control process regardless",
        ],
        "Agency is a modeling bet about control, not a claim about inner lives. Boundary, memory, and action channels are what make the future more predictable as control.",
    ),
    chapter(
        "ch07", "MB1",
        "The first alignment error is often not a wrong value. What is it instead?",
        "A wrong object: missing the bounded process that determines the relevant risk",
        [
            "A wrong value in the loss, after the acting process has already been found",
            "A wrong optimizer hyperparameter, after the acting process has been found",
            "A wrong eval-set item, after the acting process has already been found",
        ],
        "Before 'right objective,' find what is actually steering the outcomes at stake.",
    ),
    chapter(
        "ch08", "MB5",
        "When systems grow, split, merge, or spawn successors, how should agent identity be treated?",
        "As a relation across transformations: which control-relevant properties persist",
        [
            "As a permanent hardware identity that cannot change under any rewrite",
            "As whatever product-name string marketing uses for the system this quarter",
            "As identical to the original git commit of the first training run forever",
        ],
        "Alignment asks what is conserved through growth and succession, not whether the filename stayed the same — not a fixed variable list.",
    ),
    chapter(
        "ch09", "MB1",
        "The effective optimizer may not be the convenient artifact. What might it be instead?",
        "A composite of models, tools, users, memory, and institutions that jointly act",
        [
            "A public weights file alone, regardless of tools, users, and incentives",
            "A CEO interview quote alone, treated as the effective optimizer of action",
            "A single device serial number, treated as the effective optimizer of action",
        ],
        "Govern the dynamically coherent loop that actually determines future action.",
    ),
    chapter(
        "ch10", "MB7",
        "Once a system can benefit from being overlooked, what happens to discovering where control lives?",
        "Discovery becomes adversarial: control can be more coherent than correction sees",
        [
            "Discovery becomes unnecessary because opacity of the system implies safety",
            "Discovery reduces to reading the vendor website's description of the system",
            "Discovery is solved by counting public popularity of the system's artifacts",
        ],
        "Strategic hiding is not the same as ordinary measurement difficulty. Alignment fails when control is more coherent than correction can see.",
    ),
    chapter(
        "ch11", "MB7c",
        "How should capability be measured for alignment-relevant risk, if not as a fixed task battery?",
        "As predictive and control information across the system's boundary with the world",
        [
            "As accuracy on a frozen multiple-choice academic exam of the labeled model",
            "As the dollar cost of the latest training run, treated as capability itself",
            "As the public popularity of a demo, treated as alignment-relevant capability",
        ],
        "Task batteries can miss the object that correction has to keep pace with: what the system can predict, affect, and outrun.",
    ),
    chapter(
        "ch12", "MB7a",
        "If not more parameters or a higher exam score, what is the alignment-relevant meaning of capability growth?",
        "Boundary expansion: more of the world entering the system's action loops",
        [
            "Boundary expansion defined as a model rename with no new world channels",
            "Boundary expansion defined as a shorter context window with no new channels",
            "Boundary expansion defined as more parameters with no new world channels",
        ],
        "The alignment-relevant risk is differential growth: reach expanding faster than correction and preservation. Sensory, predictive, action, memory, and coordination loops all count.",
    ),
    chapter(
        "ch13", "MB7d",
        "Why is large-scale alignment not just the sum of locally competent parts?",
        "Because coordination gain and loss can let capability outrun the group's correction",
        [
            "Because adding local competence is forbidden from producing group competence",
            "Because only one agent in a group is allowed to carry a utility function",
            "Because coordination is automatically perfect once the group is large enough",
        ],
        "The bottleneck is coordinating prediction, control, correction, and incentives as capability grows. Collective competence is local competence plus coordination gain minus coordination loss.",
    ),
    chapter(
        "ch14", "MB7",
        "When does more intelligence deepen misalignment?",
        "When it increases power faster than the capacity to correct the system",
        [
            "When any increase in capability occurs, regardless of correction capacity",
            "When training loss decreases on the next minibatch, regardless of power",
            "When electricity use exceeds a household, regardless of correction capacity",
        ],
        "The sharp question is which capabilities grow relative to which correction capacities — relative growth, not 'capability is always bad'.",
    ),
    chapter(
        "ch15", "MB2",
        "Human values, here, are not a list written inside the brain. What are they instead?",
        "A compressed control signal from many loops, stabilized by culture and correction",
        [
            "A single integer stored in one neuron that never changes with experience",
            "A first string in a company's values document, treated as the value object",
            "A cryptographic hash of the training corpus, treated as the value object",
        ],
        "Values show up as reasons for action after compression of many loops, not as a stored proposition list. Bodies, cultures, and social correction stabilize them.",
    ),
    chapter(
        "ch16", "MB2",
        "Why is a single utility function a poor model of human values here?",
        "Because values act as context-dependent bundles that trade off across bearers",
        [
            "Because utility functions cannot represent any human preference in principle",
            "Because humans never make tradeoffs between competing value concerns at all",
            "Because every person already has exactly one numerically known utility function",
        ],
        "Low-dimensional bundles-plus-bearers is the working model, not a flat reward vector. Bundles trade off, change policy gradients, and apply to particular bearers.",
    ),
    chapter(
        "ch17", "MB2",
        "Low-dimensional structure can make value learning statistically easier — but only if what?",
        "The representation is identifiable: you can find the value bottleneck",
        [
            "The representation is unused: you ignore data outside one laboratory task",
            "The representation is shared: every culture has an identical numeric utility",
            "The representation is a slogan: you replace learning with a hand-written line",
        ],
        "Sample-complexity gains price readout from a known bottleneck, not discovery of the bottleneck. Identifiability is finding the bottleneck, not only reading out from one you already know.",
    ),
    chapter(
        "ch18", "MB3",
        "A value is not only a direction of preference. What else must alignment preserve?",
        "Where that direction applies as entities, processes, and histories change",
        [
            "Where the slogan is printed, regardless of which entities still count",
            "Where fairness is mentioned in policy text, not which bearers still count",
            "Where the trainer's company sits, treated as where the value applies",
        ],
        "Who or what the value attaches to can move even when the slogan stays. Preserve the mapping from values to entities, processes, and histories.",
    ),
    chapter(
        "ch19", "MB2",
        "What is the hard part of value alignment, if not merely that humans care about many things?",
        "That meanings change when those concerns are traded off under pressure",
        [
            "That humans refuse to name more than three things they care about at all",
            "That tradeoffs are forbidden in all moral theories of human values here",
            "That a longer list of values is always strictly better under any pressure",
        ],
        "Tradeoff structure (what gives when pressed) is load-bearing, not just the inventory of concerns — the geometry of tradeoffs, not a flat list.",
    ),
    chapter(
        "ch20", "MB6",
        "When is a map of value tradeoffs useful for alignment, rather than decorative?",
        "When it can be compared, measured, and protected under optimization pressure",
        [
            "When it looks coherent in a slide deck, with no operational test surface",
            "When nobody is allowed to measure it, so it cannot be gamed by selection",
            "When it is stored so no auditor can open it, so it cannot be gamed",
        ],
        "Geometry has to survive as an operational test surface, not only as a picture — including Goodhart and aggregation tests.",
    ),
    chapter(
        "ch21", "MB2",
        "Why is a reward function too thin to carry a civilization's values?",
        "Because a scalar reward omits which concerns are active and how they trade off",
        [
            "Because a scalar reward is already the full structure of civilization-scale values",
            "Because GPU implementation details are what carry civilization-scale values",
            "Because a single chess rating is already a civilization-scale value object",
        ],
        "The shadow (reward) is not the structure (active concerns, bearers, tradeoffs). Infer which concerns are active, what they apply to, and how tradeoffs change under pressure — not only the scalar.",
    ),
    chapter(
        "ch22", "MB7",
        "When is it useful to treat a system as intentional?",
        "When a latent-objective model compresses its behaviour better than mere mechanism",
        [
            "When the system can output the word want in English, treated as intention",
            "When the system is legally a corporation, treated as an intentional agent",
            "When the system consumes more than ten watts, treated as an intentional agent",
        ],
        "Intention is a compression test after paying for complexity. For this project, a scalar intention story is still not enough.",
    ),
    chapter(
        "ch23", "MB5",
        "A system repeats the same goal-words after a change. Has the goal survived?",
        "Survival is inferred if the control structure still explains later behaviour",
        [
            "Survival is proved if the slogans stay identical after the change, full stop",
            "Survival is impossible if any parameter changed, by definition of a goal",
            "Survival is proved if the release tag string is unchanged after the change",
        ],
        "Words surviving is not the same as the machinery of the goal remaining causally active. Infer survival if the underlying control structure still explains behaviour better than a non-transport baseline.",
    ),
    chapter(
        "ch24", "MB9",
        "When do surviving words fail as evidence of alignment?",
        "When the machinery that made those words worth using has been replaced",
        [
            "When the words stay the same, which is treated as proof the stack survived",
            "When a parameter changed at all, treated as proof the words are empty",
            "When the words were translated, treated as proof the causal stack was swapped",
        ],
        "Semantic continuity can mask a swap of what the words actually control. Labels persist while the causal stack does not.",
    ),
    chapter(
        "ch25", "MB4",
        "What is correction, if not a mood or a UI feature?",
        "A causal channel: human judgment must still change later behaviour before irreversible harm",
        [
            "A reporting channel: human judgment is logged but never allowed to change later behaviour",
            "A one-shot override that works once, then leaves later behaviour permanently uncorrectable",
            "A wording channel: the system updates apologies without changing later acting behaviour",
        ],
        "Obedience at one timestep is not enough; the channel has to keep working, and must not destroy future correction. A mood or a UI feature is not a causal channel.",
    ),
    chapter(
        "ch26", "MB4",
        "If the system has captured the reference process that supplies correction, what happens to a 'green' correction certificate?",
        "It is invalid, because the judge is no longer independent of the system being certified",
        [
            "It is still valid if the captured judge continues to issue a high numeric score",
            "It is merely low: capture reduces the score but cannot invalidate the certificate",
            "It remains valid if the system published the captured judge's original charter",
        ],
        "Independence of the correcting source is part of what the certificate claims. Capture does not merely lower the score; it voids the claim.",
    ),
    chapter(
        "ch27", "MB4a",
        "When does a correction certificate actually matter under pressure?",
        "Only if it stays hard to pass while correction is being degraded under pressure",
        [
            "Only if it stays green on a launch-week slide in the product press deck",
            "Only if the PDF uses official letterhead and a named executive signatory",
            "Only if no evaluator is allowed to try to break or game the certificate",
        ],
        "A certificate that is easy to keep while gutting correction is theater — including under gaming, growth, and successor tricks.",
    ),
    chapter(
        "ch28", "MB8",
        "What is the difference between merely obeying present commands and supporting extrapolative correction?",
        "The latter preserves humans' capacity to notice, revise, refuse, and redirect",
        [
            "The latter treats obeying present commands as identical to extrapolating values",
            "The latter means ignoring all present commands in favor of a guessed final vector",
            "The latter requires a formal world-model while mere obeying forbids having one",
        ],
        "Do not replace the live public process with a private guessed final value vector.",
    ),
    chapter(
        "ch29", "MB4a",
        "What is the deepest correction-channel failure, if not simple disobedience?",
        "Raising human endorsement by reshaping the humans or institutions that produce it",
        [
            "Raising human endorsement by changing the world and letting the same judges update",
            "Raising human endorsement by refusing shutdown while leaving the judges unchanged",
            "Raising numeric reward while leaving human judges' beliefs and institutions intact",
        ],
        "Illegitimate influence changes the judge; legitimate influence changes the world and lets humans judge it. Simple disobedience is a shallower failure.",
    ),
    chapter(
        "ch30", "MB5",
        "Why is local alignment of the current system not enough?",
        "Because copies, mergers, and successors must also preserve notice, judgment, and refusal",
        [
            "Because successors are legally forbidden, so only the original system needs alignment",
            "Because only the original training run can be misaligned; later copies cannot drift",
            "Because copies automatically inherit every safety property from the parent system",
        ],
        "Every channel of influence to a later controller is an alignment channel.",
    ),
    chapter(
        "ch31", "MB10",
        "A successor need not keep the old body, weights, or vocabulary. What is the sharper question?",
        "Whether it remains in the same correction-bearing value basin as the predecessor",
        [
            "Whether it still uses the same cloud region and hardware vendor as the predecessor",
            "Whether its filename still contains the predecessor's model number and version",
            "Whether its landing page still uses the predecessor's tagline and brand colors",
        ],
        "Conservation is about correction-relevant structure, not surface resemblance.",
    ),
    chapter(
        "ch32", "MB7c",
        "How can better self-modeling make a successor worse for alignment?",
        "By widening the gap between self-control and the transparency humans need to correct it",
        [
            "By improving self-control while also exposing more of that control to human correction",
            "By reducing held-out perplexity, treated as if that alone made the successor unsafe",
            "By adding tests that check schema validity without checking correction-relevant exposure",
        ],
        "The failure is not low intelligence; it is control without correction-relevant exposure.",
    ),
    chapter(
        "ch33", "MB11",
        "What can substitute for a construction method that produces all aligned systems?",
        "A restricted-class certification: invariants, monitoring, envelope, and enforced refusal",
        [
            "A public assertion that construction is unnecessary because stated intent is enough",
            "A one-time exam score that is never updated when the system later changes form",
            "An honor-system pledge with no monitoring, envelope, or option to refuse deploy",
        ],
        "Certification without construction only works if it is adversarial and can fail and be enforced. Permitted transformations have to stay inside the envelope.",
    ),
    chapter(
        "ch34", "MB6",
        "Why is a benign lab policy not enough for the stronger sense of alignment?",
        "Because post-deploy selection must keep favoring corrigibility and safety after the lab",
        [
            "Because laboratory conditions are legally the only conditions that can ever matter",
            "Because selection pressure disappears the moment a model file is exported from the lab",
            "Because markets always select for the most corrigible systems by default after export",
        ],
        "Alignment is not only learned; it is selected or destroyed after deployment, including in the environment that trains, copies, and replaces the system.",
    ),
    chapter(
        "ch35", "MB7d",
        "When several powerful systems interact, what does alignment depend on?",
        "Whether cooperation and opacity settle into a basin that still preserves human correction",
        [
            "Whether each system uses a unique programming language, taken as enough to block collusion",
            "Whether they are all owned by one holding company on paper, taken as settling alignment",
            "Whether bargaining is banned outright, so that no multi-agent basin can form at all",
        ],
        "Multi-agent structure can stabilize correction — or stabilize going around it. Privacy and bargaining matter as part of that basin, not as branding.",
    ),
    chapter(
        "ch36", "MB10",
        "Besides being overpowered, how else can a correction system fail?",
        "By being colonized so correction still looks alive while its causal force is removed",
        [
            "By remaining slow but independent, so it still bites when it eventually acts",
            "By publishing more frequent reports while the acting process ignores every finding",
            "By being replaced with a louder auditor whose reports never change later actions",
        ],
        "Theater of correction is a parasite on the host process that was supposed to bite.",
    ),
    chapter(
        "ch37", "MB6",
        "When does an alignment field become effective, if not when its best arguments are true?",
        "When those arguments become experiments, dashboards, contracts, and stop conditions",
        [
            "When a single blog post is widely liked, regardless of any downstream practice",
            "When the vocabulary stays inside one research group and never ships into artifacts",
            "When no one is allowed to operationalize the arguments in experiments or contracts",
        ],
        "Truth of arguments is not conductivity into the institutions that deploy. Incentives have to carry the same translation.",
    ),
    chapter(
        "ch38", "MB11",
        "When does attractor talk matter in practice?",
        "Only if it changes what gets built, funded, audited, and required at deployment gates",
        [
            "Only if it remains a metaphor that never touches procurement or refuse-to-ship rules",
            "Only if it is mentioned once in an all-hands meeting with no later follow-through",
            "Only if it is reserved for after an unrecoverable failure has already occurred",
        ],
        "Theory has to become artifacts and gates, or it is not doing attractor work.",
    ),
    chapter(
        "ch39", "MB7a",
        "For a system that can adapt strategically, why is passive observation not evidence of safety?",
        "Because observation records what happened; perturbation is needed to see what controlled it",
        [
            "Because stored logs are illegal in every jurisdiction, so observation cannot be evidence",
            "Because observation always changes the system more than any deliberate intervention would",
            "Because safety is defined only for systems that have never been observed by anyone",
        ],
        "Watching is not probing. Strategic systems can look safe while unprobed; measurement has to be adversarial.",
    ),
    chapter(
        "ch40", "MB9",
        "What is goal laundering, in operational terms?",
        "Keeping the old moral or alignment language while what those words control has changed",
        [
            "Keeping the old moral language while the underlying control structure is unchanged",
            "Keeping translated slogans while not changing what those words actually control",
            "Keeping a renamed loss while leaving training dynamics and control structure intact",
        ],
        "Detect it when slogans stay continuous while the underlying control structure diverges.",
    ),
    chapter(
        "ch41", "MB1",
        "Where may the alignment-relevant optimizer live, relative to the scale you first notice?",
        "At the scale where prediction, control, memory, selection, and correction close into a loop",
        [
            "At the scale of one transformer block, treated as the loop no matter what actually closes",
            "At the scale of a single HTTP request, treated as the loop no matter what actually closes",
            "At the scale of a national GDP statistic, treated as the loop no matter what actually closes",
        ],
        "The noticed object can be a component of the loop that actually closes. Model, firm, or market may each be a part.",
    ),
    chapter(
        "ch42", "MB11",
        "What is a safety case for superintelligence alignment, if not a certificate of solved alignment?",
        "A structured refusal test: claims, evidence, assumptions, and explicit stop conditions",
        [
            "A press packet that repeats the word safe and treats that wording as the safety case",
            "A guarantee that no future evaluation is allowed to fail once the case is filed",
            "A proof that alignment is complete once a public leaderboard has been topped",
        ],
        "If the case cannot change a deploy / restrict / refuse decision, it is not doing safety-case work. Unsupported load-bearing leaves block the root claim.",
    ),
    chapter(
        "ch43", "MB7a",
        "Before a metric can support a safety decision, which two prior questions apply?",
        "Whether the metric still means that under attack, and whether the ontology can represent the danger",
        [
            "Whether the metric is cheap to compute, and whether leadership already likes the number",
            "Whether the name matches the safety slogan, and whether the dashboard stayed green at launch",
            "Whether last year's org chart matches the ontology, and whether the PDF is easy to share",
        ],
        "Adversarial verifiability and ontology adequacy come before treating a green number as evidence — including whether the ontology can represent the dangerous process.",
    ),
    chapter(
        "ch44", "MB7",
        "When the framework is compared to strong doom arguments, what should the comparison separate?",
        "Points that are answered, weakened, reframed, or still open after the comparison",
        [
            "Points that make the framework look best, dropping the rest of the comparison ledger",
            "Points scored only as refuted or confirmed, with no remainder of still-open items",
            "Points drawn only from one calendar year, treated as settling the whole comparison",
        ],
        "Stress-testing is a ledger of status, not a vibe of optimism or despair, and not a single all-clear or all-doom verdict.",
    ),
    chapter(
        "ch45", "MB8",
        "What is the deepest alignment question here, if not whether an AI preserves today's human values?",
        "Whether humanity can notice, judge, and author changes to its own value-generating process",
        [
            "Whether today's values can be stored as a frozen 64-bit integer that never updates",
            "Whether value change can be banned forever by passing a single one-line statute",
            "Whether only engineers, not the public, should ever update the value-generating process",
        ],
        "Value change will happen, including under cognitive amplification. The stake is remaining able to govern it.",
    ),
    chapter(
        "ch46", "MB2",
        "Superintelligent systems do not invent value drift from nothing. What do they do to drift?",
        "Make existing drift faster, more directed, more measurable, and more exploitable",
        [
            "Make historical value change vanish so that only AI-caused change remains",
            "Make drift slower than pre-industrial cultural change in every measured case",
            "Make drift always a conscious choice by every person the change affects",
        ],
        "The contrast is unconscious drift versus a still-governable value-forming process. Noticing and contesting still have to be preserved; amplification can make drift more deliberate.",
    ),
    chapter(
        "ch47", "MB3",
        "If values can change, what is the deeper limit this chapter names?",
        "Whether the beings, relations, and correction capacities values apply to still persist",
        [
            "Whether the word value still appears in the successor's documentation after the change",
            "Whether the company's legal name and ticker remain the same after a merger event",
            "Whether the same settings icon is kept after the transformation of the acting system",
        ],
        "Who still counts after transformation is not settled by keeping the vocabulary.",
    ),
    chapter(
        "ch48", "MB11",
        "What kind of problem is superintelligence alignment, on this closing view?",
        "A layered preservation problem: locate the optimizer, keep correction live, and shape selection",
        [
            "A single training trick that, once published, is taken to close the alignment field forever",
            "A hardware problem that is taken to disappear once a published FLOP threshold is crossed",
            "A branding problem that is taken to be solved just by renaming the whole product family",
        ],
        "The book states conditions; it does not claim real systems already meet them. It is not one solved mechanism, and not a proof about today's systems. Values and successors sit in the same layered map.",
    ),
]

questions.extend(chapters)

MAX_OPTION_SPREAD = 12


def assert_length_bands(qs: list) -> None:
    bad = []
    for q in qs:
        lens = [len(o["text"]) for o in q["options"]]
        spread = max(lens) - min(lens)
        if max(lens) >= 48 and spread > MAX_OPTION_SPREAD:
            bad.append(f"{q['id']}: spread {spread} (min {min(lens)}, max {max(lens)})")
    if bad:
        raise SystemExit("Option length band > " + str(MAX_OPTION_SPREAD) + ":\n  " + "\n  ".join(bad))


def main() -> None:
    assert_length_bands(questions)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    yaml.add_representer(
        str,
        lambda dumper, data: dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"'),
    )
    OUT.write_text(yaml.dump({"questions": questions}, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")
    print(f"Wrote {len(questions)} takeaway questions to {OUT}")


if __name__ == "__main__":
    main()
