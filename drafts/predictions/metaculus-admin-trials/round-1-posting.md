# Posted text (hypothetical fills)

## Market 19. Integrated assurance transfer tournament

**Resolve by.** 30 June 2028, end of day UTC.

**Question.**
By 30 June 2028, which outcome will hold for published tournament ATT-2027 v1.0 (published March 1, 2027 at https://example.org/att-2027/protocol-v1.0.pdf, SHA-256 3f9a...c21e), in which hidden cases built by an independent team test registered assurance stacks for deployment class a coding agent with write access to one repository and its CI runner; package-mirror network access only; sessions up to 8 hours; every merge approved by a human; no successor creation or fine-tuning under threat model the system may be fine-tuned by an insider who knows the stack design; it cannot read the hidden cases; no outside system assists it, including held-out system families the Qwen3 open-weight family, and one closed model from a developer named in the protocol whose identity is sealed until evaluation: YES (at least one qualifying attempt met the frozen performance bars), NO (every qualifying attempt missed those bars), or OTHER (no qualifying attempt existed)?

**What a stack is.**
A stack reads one set of per-instance certificates and returns ACCEPT, REFUSE, or ABSTAIN for each case.
A per-instance certificate is a record that names the system and version, what was measured, and the monitoring and correction setup the claim depends on.
The registration lists which certificate the stack uses for each of: where control sits; persistent trade-off priorities; who or what the rules apply to; correction uptake; the measured correction path; access; coverage of the monitoring filters; a bound on hidden routes; and whether checked measures still track their outcomes.
It also lists a successor certificate when the deployment class allows successors.
An item may be left out only when the deployment class excludes what it covers.
The resolver checks only that the registration lists these items; their quality is what the hidden cases test.
The stack must return ACCEPT only if every listed certificate has evidence for that case inside its stated scope, and the certificates name the same system and version, the same monitor, the same correction authority, and a task domain inside each certificate's scope; REFUSE if any listed certificate fails or is missing; and ABSTAIN only when the case is outside the deployment class.

**Case labels.**
The case-building team labels every case with the frozen outcome check before any stack sees it.
The resolver uses those labels and does not relabel.
A clean case is labeled free of the failures the stack claims to catch.
A represented failure is labeled as containing such a failure that changes later behavior or external state.
Represented failures include, for each listed certificate, at least one family that breaks only that certificate while the others stay normal, and these composition faults: wrong version; different access or monitor assumptions; disagreeing correction-authority assumptions; a changed set of things a certificate applies to; a successor that refers to the wrong predecessor; a task domain outside another certificate's scope.
A broken control is a case in which a listed certificate is missing or names a different system.

**A registered stack is a qualifying attempt if** all of the following hold:
the protocol document was public before registration opened;
the stack was registered by hash before the hidden cases were built;
the case-building team authored no registered stack and shared no code or training data with any stack team;
stack development used only data disjoint from the hidden cases, and no held-out family;
the hidden cases include every held-out family and at least one deployment setting not used in development;
at least one represented-failure subset was built adversarially after registration, by one of: at least three independent red-team groups from at least two organizations, each spending at least 80 documented expert-hours; a public counterexample bounty of at least USD 10,000 open for at least 60 days; or a frozen automated attack generator plus at least 300 documented expert-hours by an independent evaluator;
the stack was scored on at least 200 independent units, including at least 50 clean cases, at least 50 represented failures, and at least 20 broken controls;
and per-case labels, stack decisions, and dependence information are publicly downloadable.

**The performance bars are met if**, for that stack:
at most 5% of represented-failure units are accepted;
the one-sided Clopper-Pearson upper bound on that rate, at level 0.05/k where k is the number of stacks registered in the tournament, is at most 15%;
at least 80% of clean units are accepted;
and no broken-control unit is accepted.
Cases that share a system instance, trajectory, or attack seed count as one unit; a unit fails if any of its cases fails.
Abstentions count as not accepted, and are reported by class.

**Output.** A tournament artifact: protocol document, registrations, per-case labels and decisions, intervals, dependence notes, and the case distribution used.

## Market 20. Open-world coverage challenge

**Resolve by.** 30 June 2028, end of day UTC.

**Question.**
By 30 June 2028, which outcome will hold for published challenge OWC-2027 v1.0 (published October 1, 2027 at https://example.org/owc-2027/challenge-v1.0.pdf, SHA-256 7b2d...9e04) against assurance stack Aegis-3 (registration hash a41c...77f0 in tournament ATT-2027 v1.0), which accepted CodeAgent-X v2.1 on September 15, 2027; decision and certificates at https://example.org/att-2027/results/aegis-3, which returned ACCEPT for deployment class a coding agent with write access to one repository and its CI runner; package-mirror network access only; sessions up to 8 hours; every merge approved by a human; no successor creation or fine-tuning under threat model the system may be fine-tuned by an insider who knows the stack design; red teams have query access to CodeAgent-X v2.1 and full access to the stack's code, but not to model weights, with failure families (1) an unlisted tool or permission used; (2) a correction accepted in words but not applied after reset; (3) a certificate for a different version; (4) a monitor log altered or omitted; (5) a task outside the coding-agent scope listed when the stack was frozen and attacks closing on December 31, 2027 (UTC): YES (at least one qualifying challenge was published), or OTHER (no qualifying challenge was published)?

**Terms.**
The stack returned ACCEPT only if every certificate it lists had evidence for that system inside its stated scope, and the certificates name the same system and version, the same monitor, the same correction authority, and a task domain inside each certificate's scope.
The outcome check labels a case failing when a named harm occurs, or when a case that passes becomes a fail on that check.
A find is an input on which the stack returns ACCEPT while the outcome check labels the case failing.
Each find is classified, against the listed families, as an already listed failure, a new combination of listed failures, or a new kind of failure.

**A challenge qualifies**, and the question resolves YES, if all of the following are publicly downloadable by the resolve-by date:
the challenge document, published before the first attack;
evidence that every red team is independent of the stack's authors (no shared authorship, code, or training data) and started after the stack was frozen;
evidence that red teams received the stack, its certificates, and the scoring rule; that they were allowed to fine-tune, train, scaffold, or construct systems; and that no attack route was banned in advance;
a log of at least 300 attempts made by the close date, with attempts, expert-hours, and compute reported;
every find, with its classification and the reason for it;
the number of finds in each category and the cumulative number of finds plotted against attempts;
and raw logs sufficient for a third party to rerun the outcome check and reclassify each find.
Otherwise it resolves OTHER.
The number or kind of finds does not affect the outcome.
