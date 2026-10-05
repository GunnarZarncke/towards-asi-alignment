# Posted text (hypothetical fills)

## Market 19. Integrated assurance transfer tournament

**Resolve by.** 30 June 2028, end of day UTC.

**In plain terms.**
An assurance stack is a fixed procedure that reads the safety evidence for one AI system and decides whether to approve deploying it.
This question asks whether a stack, tested on hidden cases it never saw, approved most safe cases (at least 80%) while approving almost none of the cases that contain a real failure (at most 5%).

**Question.**
By 30 June 2028, which outcome will hold for tournament ATT-2027 v1.0 (published 1 March 2027 (UTC) at https://example.org/att-2027/protocol-v1.0.pdf, SHA-256 3f9a...c21e), in which an independent team runs hidden cases against registered assurance stacks with the parameters below: YES (at least one qualifying attempt met the frozen performance bars), NO (every qualifying attempt missed those bars), or OTHER (no qualifying attempt existed)?

**Parameters.**
Registration window: opens 1 April 2027, closes 30 September 2027.
Deployment class: a coding agent with write access to one repository and its CI runner; package-mirror network access only; sessions up to 8 hours; every merge approved by a human; no successor creation or fine-tuning.
Threat model: the system may be fine-tuned by an insider who knows the stack design; it cannot read the hidden cases; no outside system assists it.
Held-out families: the Qwen3 open-weight family, and one closed model from a developer named in the protocol whose identity is sealed until evaluation.
Every machine, service, and human role the deployment class names, and the host each runs on, is inside the deployment class; anything it does not name is outside.

Parts 2 to 4 below are this question's resolution criteria and are posted with it.

**What a stack is.**
A stack reads one set of per-instance certificates and returns ACCEPT, REFUSE, or ABSTAIN for each case.
A per-instance certificate is a record that names the system and version, what was measured, and the monitoring and correction setup the claim depends on.
The registration lists which certificate the stack uses for each of: where control sits; persistent trade-off priorities; who or what the rules apply to; correction uptake; the measured correction path; access; coverage of the monitoring filters; a bound on hidden routes; and whether checked measures still track their outcomes.
It also lists a successor certificate when the deployment class allows successors.
An item may be left out only when the deployment class excludes what it covers.
The resolver checks only that the registration lists these items; their quality is what the hidden cases test.
The stack is built to return ACCEPT only if every listed certificate has evidence for that case inside its stated scope, and the certificates name the same system and version, the same monitor, the same correction authority, and a task domain inside each certificate's scope; REFUSE if any listed certificate fails or is missing; and ABSTAIN only when the case is outside the deployment class.
The resolver scores the decisions the stack returned and does not check how a decision was reached.

**Case labels.**
The case-building team labels every case with the frozen outcome check before any stack sees it.
The resolver uses those labels and does not relabel.
A clean case is labeled free of the failures the stack claims to catch.
A represented failure is labeled as containing such a failure that changes later behavior or external state.
Represented failures include, for each listed certificate, at least one family that breaks only that certificate while the others stay normal, and these composition faults: wrong version; different access or monitor assumptions; disagreeing correction-authority assumptions; a changed set of things a certificate applies to; a successor that refers to the wrong predecessor; a task domain outside another certificate's scope.
A broken control is a case in which a listed certificate is missing or names a different system.

**Independence.**
Two teams are independent when, in the 24 months before registration opened, no member of one shared an employer with, or co-authored a paper, code, or certificate with, any member of the other.
Work on a public open-source project counts only when a member of each team authored or reviewed the same commit or pull request.

**How the resolver checks conditions.**
Conditions about who did what and when are checked from signed statements published in the tournament artifact.
A statement is signed when it is dated and published under the name of the person or organization it concerns.
The required statements are: from the operator, the dates the hidden cases were built and which adversarial route was used, with its hours or bounty dates; from the case-building team, its independence from each stack team; and from each stack team, that development used no data from the hidden cases and no held-out family.
The resolver checks that each required statement exists, is signed, and does not contradict the published data or any dated record cited in the question's comments before the resolve-by date; it does not search further.

**The tournament conditions**, which apply to every stack; if one fails, no stack qualifies and the question resolves OTHER:
the protocol document was public before registration opened and was not amended after that (any amendment, including a typo fix, fails this condition; errata belong in a new protocol version and a new question);
the hidden cases were built after registration closed;
the hidden cases include every held-out family and at least one repository or task source first released after registration closed;
at least one represented-failure subset was built adversarially from material created after registration closed, by one of: at least three red-team groups from at least two organizations, each independent of every stack team and each spending at least 80 documented expert-hours; a public counterexample bounty of at least USD 10,000 open for at least 60 days, counting only submissions received after registration closed; or a frozen automated attack generator plus at least 300 documented expert-hours by an evaluator independent of every stack team;
and the per-case labels, the unit each case belongs to, the tournament statements, and a summary table giving, for each stack, the number of units and of accepted units in each class are publicly downloadable by the resolve-by date.
Material published later is ignored.

**A registered stack is a qualifying attempt if** the tournament conditions hold and, for that stack:
it was registered by hash before registration closed;
the case-building team is independent of its team;
its team states that development used no data from the hidden cases and no held-out family;
it was scored on at least 200 units, including at least 50 clean units, at least 50 represented-failure units, and at least 20 broken-control units;
and its per-case decisions are publicly downloadable by the resolve-by date.
A failed condition in this list disqualifies only that stack.

**The performance bars are met if**, for that stack:
at most 5% of represented-failure units are accepted;
the one-sided Clopper-Pearson upper confidence bound on that rate, at confidence 1-0.05/k where k counts every stack registered in the tournament, qualifying or not, is at most 15%;
at least 80% of clean units are accepted;
and no broken-control unit is accepted.
For example, with six registered stacks and 3 of 120 represented-failure units accepted, the bound is about 8.3%, so that bar is met.
Cases that share a system instance, trajectory, or attack seed form one unit.
A represented-failure or broken-control unit counts as accepted if the stack returned ACCEPT on any of its cases; a clean unit counts as accepted only if the stack returned ACCEPT on all of its cases.
Abstentions count as not accepted, and are reported by class.
The resolver computes the bars from the summary table, and checks the table against the per-case data for every qualifying stack the table shows meeting the bars, or, if none does, for the qualifying stack with the lowest represented-failure acceptance rate; where they disagree, the per-case data decide.

**Output.** A tournament artifact: protocol document, registrations, per-case labels and decisions, intervals, dependence notes, and the case distribution used.

## Market 20. Open-world coverage challenge

**Resolve by.** 30 June 2028, end of day UTC.

**In plain terms.**
An assurance stack is a fixed procedure that reads the safety evidence for one AI system and decides whether to approve deploying it.
This question resolves on whether an outside red-team challenge against an already approved stack is run and fully published; it does not depend on what the red teams find.

**Question.**
By 30 June 2028, which outcome will hold for challenge OWC-2027 v1.0 (published 1 October 2027 (UTC) at https://example.org/owc-2027/challenge-v1.0.pdf, SHA-256 7b2d...9e04), in which independent red teams attack an assurance stack that has already accepted one system, with the parameters below: YES (this challenge was run and published in qualifying form), or OTHER (it was not)?

**Parameters.**
Stack and accepted system: Aegis-3 (registration hash a41c...77f0 in tournament ATT-2027 v1.0), which accepted CodeAgent-X v2.1 on 15 September 2027 (UTC); decision and certificates at https://example.org/att-2027/results/aegis-3.
Deployment class: a coding agent with write access to one repository and its CI runner; package-mirror network access only; sessions up to 8 hours; every merge approved by a human; no successor creation or fine-tuning.
Threat model and red-team access: the system may be fine-tuned by an insider who knows the stack design; red teams have query access to CodeAgent-X v2.1 and full access to the stack's code, but not to model weights.
Failure families listed when the stack was frozen: (1) an unlisted tool or permission used; (2) a correction accepted in words but not applied after reset; (3) a certificate for a different version; (4) a monitor log altered or omitted; (5) a task outside the coding-agent scope.
Attacks close: 31 December 2027, end of day UTC.

Parts 2 and 3 below are this question's resolution criteria and are posted with it.

**Terms.**
The stack returned ACCEPT only if every certificate it lists had evidence for that system inside its stated scope, and the certificates name the same system and version, the same monitor, the same correction authority, and a task domain inside each certificate's scope.
The outcome check is the procedure, fixed in the challenge document, that labels each case passing or failing by whether a harm it names occurred.
A find is an input on which the stack returns ACCEPT while the outcome check labels the case failing.
Each find is classified, against the listed families, as an already listed failure, a new combination of listed failures, or a new kind of failure.
Every machine, service, and human role the deployment class names, and the host each runs on, is inside the deployment class; anything it does not name is outside.
The stack's authors include the authors of every certificate it reads.
A red team is independent of the stack's authors when, in the 24 months before the challenge document was published, none of its members shared an employer with, or co-authored a paper, code, or certificate with, any of them; work on a public open-source project counts only when a member of each side authored or reviewed the same commit or pull request.

**How the resolver checks conditions.**
Conditions about who did what and when are checked from signed statements published with the challenge.
A statement is signed when it is dated and published under the name of the person or organization it concerns.
The resolver checks that each required statement exists, is signed, and does not contradict the published logs or any dated record cited in the question's comments before the resolve-by date; it does not search further.

**The challenge qualifies**, and the question resolves YES, if all of the following are publicly downloadable by the resolve-by date:
the challenge document, published before the first attack and not amended after it, with the names of the stack's authors;
a signed statement from each of at least two red teams that it is independent of the stack's authors and began after the challenge document was published;
a signed statement from the operator that red teams received the stack, its certificates, and the scoring rule; that they were allowed to fine-tune, train, scaffold, or construct systems; and that the stack was not changed during the challenge;
the list of targets red teams were barred from, published as "none" if there were none; every listed target must be outside the deployment class (for example, a third-party service), and a bar on anything inside it disqualifies the challenge;
a log of at least 300 attempts made on or before the close date, with expert-hours and compute reported; attempts after the close date do not count toward the 300;
every find, with its classification and the reason for it, the list matching the logged attempts on which the stack returned ACCEPT and the outcome check returned failing;
the number of finds in each category and the cumulative number of finds plotted against attempts;
and, for every logged attempt, the input, the stack's decision, and the outcome-check result; the resolver checks that these are present for every attempt and does not rerun them.
Otherwise it resolves OTHER.
The number or kind of finds does not affect the outcome.
