---
related:
  - chapters/appM
  - conserved-properties-growth-split-merge
  - successor-stability
citeKeys:
  - kelty2008twobits
  - weber2004successopensource
  - fsf2007gplv3
---

How do you make a rule survive its own author? Most constraints on organizations die when the organization is sold, forked, or succeeded: the new owner simply never agreed to them. The GNU General Public License — the legal foundation of Linux and much of the free-software world — is the clearest existing engineering solution to this problem, and it repays study precisely because it has been stress-tested by motivated adversaries for four decades.

Its mechanism is that the constraint travels *with the artifact* rather than depending on any successor's goodwill: whoever distributes a modified version of GPL software must pass on the same freedoms they received, under the same license. Inheritance is structural, not voluntary. And enforcement rides an existing, strong, *distributed* lever — copyright — meaning any contributor whose code was misused can sue, rather than everyone depending on one central enforcement office that could be captured or defunded. The license has survived real courtroom contact in Germany and the United States.

Its two failures teach as much as its success. First, the license's trigger was the word "distribution," written when software changed hands as copied artifacts. Then the world moved to software-as-a-service: companies could modify GPL code and serve it to millions of users without ever legally *distributing* anything. The constraint's text survived intact while its triggering condition silently stopped firing — the world's ontology shifted out from under the rule. Second, hardware vendors discovered "tivoization": publish the source code exactly as the license demands, but cryptographically lock the device so no modified version will run. The letter of the rule survived; the actual freedom it existed to protect did not. A new license version (GPLv3) closed that gap — whereupon the Linux kernel, the GPL's largest and most consequential lineage, declined to adopt it. Tightening an inheritance constraint can drive your most important successor to fork away rather than comply.

For AI, the transferable lesson is structural, not textual. The GPL does not show that one can license model weights into safety — copyright may not even apply to weights, and behavioral-use licenses lack any comparably strong enforcement lever. What it shows is that constraint inheritance across successors works when, and only when, it rides an existing, strong, distributed enforcement mechanism. The search for AI's equivalent of copyright should look at compute access, distribution-platform terms, and insurance — and should expect both failure modes above: triggers that quietly stop firing as deployment ontology shifts, and letter-compliance that removes the substance.

---

*One of eleven historical case studies in [Institutional Genesis, Memory, and Decay](../chapters/appm/) — see the overview for the full life-cycle map, or [read the complete appendix](../chapters/appm/full/).*
