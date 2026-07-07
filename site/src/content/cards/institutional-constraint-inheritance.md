---
title: "Constraint Inheritance Across Successors — the GPL"
type: "concept"
status: "framework"
summary: "The GNU General Public License is the clearest existing engineering solution to a narrow successor problem: the constraint travels with the artifact through copyright, a strong distributed enforcement lever, rather than depending on the successor's stated intent."
decision: "Search for AI's equivalent of copyright — compute access, distribution-platform terms, or insurance underwriting — rather than assuming license text alone can bind model weights or behavior; constraint inheritance only works when it rides an existing, strong, distributed lever."
evidence: "Tivoization showed hardware vendors satisfying the license to the letter while removing the user's actual correction handle, fixed by GPLv3 at the cost of the Linux kernel declining to adopt it; the software-as-a-service shift showed the license's 'distribution' trigger surviving in text while its function silently stopped firing, patched only by a new license (AGPL)."
bookChapters: ["appM"]
bookLabels: ["sec:appm-constraint-inheritance"]
citeKeys: ["kelty2008twobits", "weber2004successopensource", "fsf2007gplv3"]
related: ["chapters/appM", "conserved-properties-growth-split-merge", "successor-stability"]
---

The GPL's mechanism is that the constraint travels with the artifact rather than depending on the successor's goodwill: any distributed derivative work must carry the same license, so inheritance is structural rather than voluntary. Enforcement rides an existing, strong, and distributed lever — copyright — so any contributor can enforce it rather than relying on one capturable enforcement office. It has been tested adversarially in court for four decades.

Its two failures are as instructive as its success. First, its trigger, "distribution," was written for an ontology that software-as-a-service made obsolete: providers could modify and serve code without ever legally distributing it, a goal-transport failure later patched by a new license rather than the original text. Second, hardware vendors satisfied the license to the letter while cryptographically preventing users from running any modified version ("tivoization") — the text and nominal freedom survived; the actual correction handle did not. GPLv3 closed the gap, but the Linux kernel, the GPL's largest successor lineage, declined to adopt it: tightening an inheritance constraint can cause the most important lineage to fork away from it. The transferable claim for AI is structural, not textual: the underlying enforcement lever (copyright) may not extend to model weights or behavior, so the search for AI's equivalent lever should look at compute access, distribution terms, and insurance.
