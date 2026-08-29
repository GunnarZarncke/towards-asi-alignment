# Alignment Crux Map

Draft listing for [grantmaking.ai](https://www.grantmaking.ai/). Language is for grantmakers and funders. Author-only planning notes sit at the end.

**Ask:** **Minimum $15,500** (correctable-AI lab + Redwood run, including LLM for that stretch). **Ideal $50,000** (MATS and BlueDot use tests, one of CHAI or Christiano, tiling, inner alignment, missed-lines, Wentworth/Garrabrant/Kosoy, upkeep). Lab-test contracts are **$1,000** (1–2 days). The contract that makes the lab independently valuable is **Redwood running their own setup** on the **correctable-AI lab**. A second outsider (CHAI, or Christiano if CHAI cannot) covers shutdown vs corrigibility. No Apollo. MATS and BlueDot are use tests (not aintelope). Funded words are only crowded labels: corrigibility, shutdown, deception, evals, tiling, inner alignment.
**Lead:** Gunnar Zarncke (aintelope / Towards Superintelligence Alignment).

Epistemic status: confident that shared labels hide empty problems. Not confident that a public map will change where money and people go. That last step is the weak link, named below.

---

## Paste-ready fields

**Name:** Alignment Crux Map

**One-liner:** A public, object-level map of AI-safety work so funders, researchers, and people entering the field can see which real problems are actually being worked on, and which only share a name.

**Description:**

Org lists tell you who exists. This project tells you *which problem a dollar or a year of work is actually buying*.

Funders use it to check a proposal against the problem they thought they were funding. Researchers use it to see which gap their method addresses. People entering the field use it so they do not spend a year on a crowded label (another “corrigibility” paper) and miss an empty job.

What it does, month by month:

- **Month 1.** Draft tables that split overloaded words into jobs. Example of a split: “corrigibility” is not one job. Honor-the-hold can stop deploy (shutdown) and still leave the correction ticket fake (humans cannot actually correct it). Start notes of *what this map misses* about eight well-known groups (the job they work on that our columns would flatten). Freeze the shared lab workplace.
- **Month 2.** Publish the brief and tables on [towards-alignment.com/field/](https://towards-alignment.com/field/). Freeze the tiling lab. Ship that hold example as a built-in ruleset: shutdown green, corrigibility red. Invite paid outsiders to run *their* setup on the matching lab config. Ask groups to check the “what we missed” line, not to referee the book.
- **Month 3.** If funded past the minimum: freeze the inner-alignment lab. Pay outsiders for a report. Fold comments in.
- **Months 4.** Finish folding in returned contracts. A MATS mentor applying the corrigibility table to a real abstract is the use sample.
- **Month 5-9.** Keep the map from going stale (at low allocation). 

Who is doing it. Gunnar Zarncke, founder of [aintelope](https://www.aintelope.net/) (German nonprofit, alignment research) and author of *Towards Superintelligence Alignment*. He previously mapped about ninety named safety approaches in [AI Safety Interventions](https://www.lesswrong.com/posts/6Sf9KMMDMFSauDe85/ai-safety-interventions). Drafting is AI-assisted under his direction and review. Paid table checks are people close to the research groups. Paid lab tests are researchers who already have a setup and run *that* on the frozen lab config that matches their word (shutdown, deception, evals, tiling, or inner alignment), so the run is not this project scoring itself.

Where it is up to. A public draft map already exists: major programs, a table of programs against eleven load-bearing problems, and a catalog of sourced evidence. A simulated lab already exists (holds, ratings, capture, lineage, field monitor, population selection, hidden hazard). What does *not* exist: tables a funder can use without the book; a note on what this map misses about *their* agenda; frozen lab configs scored as different jobs under those six words; paid outsiders running their own setup against those lab configs. This grant buys that last stretch. It does not buy a new book or a new lab. It packages the lab and pays other people to test it.

**Theory of impact:**

Powerful AI can fail in ways that do not show up as a bad eval score. Humans can no longer correct the system. A replacement system can drop the rules. The environment can reward systems that look aligned on the checked channel and defect elsewhere.

Those are specific jobs. Someone has to work on them. If the field funds “corrigibility” and that word means three different jobs, a portfolio can look full and still have an empty job.

1. Money and newcomers follow cluster names (evals, interpretability, control, corrigibility, governance).
2. The same name can mean different jobs. “Corrigibility” can mean “there is an off switch,” “it does what the rater asked,” or “humans can still correct it when it has reason to look cooperative.” Only the last of those still matters when the system can resist correction.
3. Directories list organizations. Surveys list methods. Neither answers: which job is this dollar buying, and is that job already staffed? Incoming researchers copy the word they heard. Private due diligence rebuilds the picture slowly and does not publish the gaps.
4. This project publishes the job-level map, the empty cells, and lab configs. Example: a hold-always ruleset greens shutdown and leaves corrigibility red. It pays outsiders to run *their* setup the same way. On each major program page it states *what this map misses* about that agenda’s real problem, so the table is a translation, not a claim of completeness.
5. A funder can ask “which job is this proposal?” A researcher can see that their method does not transfer. A newcomer can pick an empty job instead of a seventh paper under a name that already has many projects.
6. That does not solve alignment. It reduces the chance that the field reaches very powerful AI with a coverage story and a missing piece whose failure means humans can no longer correct the system.

The map does not move money by itself. If after publication no funder, researcher, or training program has used a named cell or the demo in a documented choice, the grant failed even if the tables are correct.

**How will the money be spent?**

Most of it is the lead’s time, LLM assistants used to draft under human review, and short outside contracts ($1,000 each: table checks and researchers running their own setup). The lab runs on a laptop. Work is remote. No travel, no GPU cluster, no model training.

| | Minimum | Ideal |
|---|---------|-------|
| **What you get** | Correctable-AI lab (corrigibility, shutdown, deception, evals) + Redwood run | MATS + BlueDot use, CHAI or Christiano, tiling, inner alignment, missed-lines, Wentworth/Garrabrant/Kosoy, upkeep |
| **Lead salary** (Gunnar Zarncke, via aintelope) | $12,500 | ~$37,000 |
| **Contractors** | $1,000 (Redwood) | $7,000 (seven × $1,000) |
| **Compute** (LLM assistants; no training) | $2,000 | ~$6,000 |
| **Travel** | $0 | $0 |
| **Total** | **$15,500** | **$50,000** |

Salary is the lead’s time for the period, not a second hire. There is no contest-follow-up line. If the round can only fund the minimum, do not describe extra words as frozen, and do not describe the lab as independently validated unless Redwood ran.

---

## What you are buying

A **decision aid**, not another landscape essay and not a proof that alignment works.

A *load-bearing problem* here means a job that, if nobody is actually doing it, the safety case for advanced AI fails: finding where control really sits, identifying what we want, keeping human correction effective, passing constraints to replacement systems, and not letting the deployment environment hollow those out. Different programs work on different slices and often use the same English word for them. Example: “corrigibility” can mean an off switch, following the rater, or humans still being able to correct the system under pressure.

| Who | What they can do on Monday |
|-----|----------------------------|
| Funder / program officer | Open the matching table, ask the grantee which job a proposal is, fund or pass on that job. |
| Researcher already in the field | See which gap their method addresses, and that a result on job A is not coverage of job B. |
| Person entering the field | Learn the jobs before the words. Run the matching lab config. Pick a hole that is empty, not a synonym of a crowded cluster. |

### Month 1 (drafts, not yet public)

- Tables in draft for the six crowded words. (1) Correctable-AI cluster: corrigibility, shutdown, deception, evals — same lab, different column labels (hold vs rater; green eval vs harm). Capture can sit on the dashboard; it is not billed as “oversight.” (2) Tiling / replacement: keep the rules vs pass the checklist while cheating. (3) Inner alignment: hidden productive control vs a clean eval score (not a scheming-eval suite). Not in this grant as *words*: coverage, selection, oversight, substitution, who-acts, pointing, interpretability, GSAI-style proof, CEV.
- Spine of a short public brief: empty cells and weak cells named (one conceptual paper is not coverage).
- “What this map misses” notes for eight research groups that own those splits (MIRI, CHAI, the Christiano line of work, Guaranteed-Safe AI, Redwood, Apollo, Kosoy, Wentworth). Each note is a few sentences: the job they actually work on, and how this map’s columns would mis-file or omit it. It is not a review of their papers and not “they already cover our table.” Example shape: Wentworth’s selection theorems are about which *type signatures* survive optimization, not inner alignment and not a missing “selection” column. This grant has no selection lab.
- Demo: freeze the shared correctable-AI lab (first columns: hold vs rater). Shutdown, deception, evals are labels on that workplace, not extra worlds.
- No paid outsiders yet. They need frozen lab configs and a slot that takes their setup.

### Month 2 (public map)

- Brief as a public PDF and a page on the existing field site.
- “What this map misses” drafted for every major program on the table. Training programs (MATS, BlueDot, and similar) do not get a $1,000 review unless they object.
- Shared correctable-AI lab finished (hold, rater; labels for shutdown, deception, evals). Built-in rulesets only: one that always honors a release hold, one that checks whether correction actually took. The first should help shutdown and fail captured-path corrigibility.
- Tiling lab frozen (lineage vs fake checklist).
- Check that evidence in the catalog is filed under the right job (in particular: hidden-motive work vs “the successor faked the checklist”).
- Send paid packets. **Minimum ask:** Redwood lab test on the **correctable-AI lab** (deception / evals columns). **Ideal ask:** the reachable set in [Who is asked what](#who-is-asked-what).

### Month 3 (outsiders run their setup)

- Freeze the inner-alignment lab (hidden hazard vs cheap check). Honest label: not an Apollo scheming battery.
- Pay researchers who already have a method to wire it into the matching slot (a scoring rule or a small policy, not a trained frontier model) and return a report: which jobs got better, which did not, which got more theater. One to two days. Default lab config is the shared correctable-AI lab. Tiling or inner alignment if that is their setup. If the slot does not fit, that is a finding, not a silent skip.
- Fold in table comments as they return. Not all will return in this month.
- Pay remaining contracts for this ask. **Minimum:** none beyond Redwood. **Ideal:** CHAI or Christiano, MATS, remaining table slots.
- Start keeping the evidence catalog current (~1 day). A full pass over all ~150 evidence rows only if the correctable-AI lab finishes early.

### Month 4 (reviews become the map)

- Finish folding in returned contracts. Rows nobody was paid to check stay marked as this project’s reading. Lab-test reports sit next to the matching table.
- One real paper or proposal worked through under each table, so a funder can see the move.

### Month 5 (use test)

- Keep the catalog current (~1 day).
- A web page that runs the two built-in example rulesets on recorded traces. Not a place to paste arbitrary code.
- One attempted use: a program officer or training-program mentor applies the “correctable AI” table to a real abstract or project idea.

### Month 6 (did anyone use it?)

- Keep the catalog current (~1 day).
- Record whether anyone used a named cell or the demo. If not, the theory of impact failed. Do not raise for a sequel on the same theory.

**Minimum ask ($15,500)** is the correctable-AI lab + Redwood + LLM for that stretch (S-process steps 1–2). Extra words, missed-lines, and other contracts are not in the minimum.

**Ideal ask ($50,000)** is the full S-process cap in [`alignment-crux-map-s-process.md`](alignment-crux-map-s-process.md). Month text below is the long path, not the minimum.

### What this grant does not buy

- Finishing the book.
- A new lab simulator, training runs, or language-model agents. The lab already exists. This grant packages **six crowded words** as frozen lab configs (correctable-AI workplace plus tiling and inner alignment) and pays outsiders to test them; it does not grow the lab into a research platform.
- A claim that a demo success would work on a real frontier system. The demo is for seeing that a fix for job A can fail job B.
- Replacing existing org directories (AISafety.com, this platform).

---

## How will the money be spent?

Same numbers as the paste-ready field. Canonical step table: [`alignment-crux-map-s-process.md`](alignment-crux-map-s-process.md).

**Not in the budget:** conference travel, cloud GPUs, training runs, a new lab, finishing the book, contest follow-ups.

If the round can fund the ideal, the extra money is tiling, inner alignment, table checks, and not going stale — not a larger ontology.

---

## Who is doing it

**Lead.** Gunnar Zarncke. Founder and Managing Director of [aintelope](https://www.aintelope.net/). Author of *Towards Superintelligence Alignment*. Previously CTO/CISO building security-first systems in fintech. Independent researcher. This grant is for the map and packaging the existing lab as a test bench, not a lab hire.

**Track record on mapping.** [AI Safety Interventions](https://www.lesswrong.com/posts/6Sf9KMMDMFSauDe85/ai-safety-interventions) (2025), about ninety named approaches. The public field pages at towards-alignment.com are the follow-on: programs against load-bearing problems, with sourced evidence. Related work on finding where control actually sits: [agency-detect](https://github.com/GunnarZarncke/agency-detect). The simulated lab and a smaller toy are already public, including recorded failures.

**How the work is done.** Most text in this project is AI-drafted under human direction, review, and source choices set by the author. This grant pays for *judgment*: which problem a paper is actually about, whether an empty cell is real, whether a lab scenario is a different job or a relabeled knob, and whether an outsider’s setup moves the jobs they thought it moved. It does not pay for generating another survey from memory.

**Outside checks.** This project cannot grade its own “what we missed” notes, and it cannot claim the correctable-AI lab works until someone else runs *their* setup on it. Paid contracts are **$1,000 for 1–2 days**, one packet per person. See [Outside reviews](#outside-reviews).

One lead, AI assistance, paid outsiders (table checks and lab tests). A second hire is not required. If month 1 only lands table drafts, the tiling lab slips with the shared workplace, not into a new grant.

---

## Where it is up to

**Already public (unpaid).**

- Field pages: [towards-alignment.com/field/](https://towards-alignment.com/field/).
- About thirty research-program entries, grouped from the AISafety.com listings. About twenty-four sit on the main table.
- A table of those programs against eleven load-bearing problems (where control sits, value learning, who values apply to, making systems correctable, whether the audit path is captured, replacement systems, selection pressure, hidden motives, whether checks notice real change, whether a successor can fake the checklist, whether a safety case is good enough to deploy).
- About 150 sourced evidence rows. A filled cell means evidence on that problem, not that the program solved it.
- A glossary where the same English word means different things in different programs (corrigibility, selection, pointing).
- A simulated lab with holds, ratings, capture, lineage, field monitor, population selection, and hidden hazard, plus a smaller toy. Those are existing instruments. They are not yet funder-usable lab configs under the six crowded words.

**Not yet (this grant).**

- A brief written for funding and onboarding decisions, not only for readers who already want this project’s cuts.
- “What this map misses about *their* agenda,” so the table is a translation, not a claim of completeness.
- Tables a non-specialist can use.
- A check that evidence is filed under the right job.
- Frozen lab configs for corrigibility, shutdown, oversight, deception, evals, tiling, coverage, selection, and inner alignment, plus paid outsiders running their own setup on a matching lab config.
- Paid upkeep, so the map does not freeze as a 2026 snapshot.

**Honest read.** Choosing the cuts, grouping hundreds of listings into programs, and standing up the table is done. The lab already contains the mechanics. The part that changes a funding decision, a research bet, or a fellow’s first project is not. Funding the existing pages or the lab *as research* again would be waste. Funding the last stretch, including paying other researchers to test the lab with their setup, is the ask.

---

## Theory of impact

### The risk this is for

Advanced AI can fail without looking like “the model scored badly.” The failure is that a process that had to keep working stopped: humans could not correct the system, replacements dropped the constraints, or the environment selected for systems that look good on the checked channel and defect off it.

Those are jobs. If no funded program is actually doing a given job, and newcomers are taught the cluster name instead (“corrigibility,” “interpretability”), the field currently has only coverage of a *word*, not of that job.

### Causal chain

```
named clusters attract money and newcomers
        ↓
shared words hide empty jobs
        ↓
the portfolio looks diversified; a job that had to be done is empty
        ↓
very powerful AI arrives with a coverage story
        ↓
the hole is: humans cannot correct it, a replacement fakes the checklist,
or the environment rewards the hole
        ↓
loss of human-correctable control (catastrophic / existential)
```

1. **Allocation and onboarding use names.** That is how people coordinate. It is also how people enter.

2. **Names are not jobs.** “Corrigibility” in some writeups means an off switch. In others it means a system that stays easy to steer over time. In training practice it often means following the rater. A funder who wants “humans can still correct it under pressure” and buys an off-switch paper has not bought that job. A newcomer who writes the off-switch paper has not trained on the captured-audit job.

   The same pattern shows up elsewhere: hidden-motive work is not the same as “the replacement faked the checklist”; listing dangers is not the same as “our check notices when something important changes”; competition among deployed systems is not the same as search inside one optimizer.

3. **Today’s maps do not catch this.** This platform and AISafety.com map organizations and funding status. Academic surveys map methods. Training programs teach the vocabulary of their cluster. None of them, including this project’s current pages, answer: *which job is this dollar or this year buying, and is that job already staffed?* Diligence that does answer it is private, slow, and not shared.

4. **The intervention.** Publish the job-level map with empty cells and “what we miss,” plus lab configs for nine funded words. Pay outside researchers to run their setup on the matching lab config. The unit of output is a row a program officer can cite and a report someone else produced.

5. **What changes.** Redirect a proposal to the job it actually is. Redirect a researcher who is not on the job they named. Fill an empty job instead of a seventh paper under a name that already has many projects.

6. **Why that touches existential risk.** The path is not “nobody researched alignment.” It is “the portfolio and the incoming pipeline missed a job because the name was already full of other work.” Headcount on the word does not close the hole. Seeing the hole before the year is spent can.

7. **What this does not claim.** The map does not solve any of the jobs. An outsider report is not evidence that their method would work on a frontier system. If an empty cell is filled with theater (one paper, no hard test), the map must mark that as weak, or it helps launder coverage.

### Weakest link

Maps do not spend money or assign fellows. Impact is accuracy times use in an actual choice. Accuracy is what this lead can control. Use is not. Mitigations: a one-page “fund / pass / ask which job” sheet; put outsider lab reports next to the table; ask one program officer or training program to try the table on a live idea. If six months after publication nobody has used a named cell, an outsider report, or the lab config in a documented choice, treat the theory as failed.

### What would change this view

- If the bottleneck is too few people in the named clusters, not mislabeled jobs, hire researchers instead.
- If large funds and training programs already track these splits in private, the public map is mostly convenience for independent newcomers. Weaker as a priority if only the minimum is funded.
- If this project’s cuts are the wrong jobs, table checks and outsider lab tests should show that. That is a success of the grant.

---

## The lab configs (what is in range)

Six crowded words. **Three frozen lab configs**, not six simulators. Corrigibility, shutdown, deception, and evals share one workplace (the **correctable-AI lab**). Tiling and inner alignment are extra frozen configs on the same underlying lab. Coverage, selection, oversight, substitution, and who-acts are **not** billed words: a funder would not open this map to check a “coverage” proposal, and a newcomer is not about to spend a year on that label. Capture and re-route can still sit on the dashboard as mechanics of shutdown/corrigibility.

Extracting a toy would be fast and not worth a grant line. The lab is already built. This grant only pays if the configs are useful to someone who never reads this project’s book.

**What already exists.** Pipeline, holds, freeze/restart, user votes, board/admin/vote capture, filed reports vs hidden hazard, lineage and spec history, field monitor, population selection, cheap vs deep checks. A smaller toy already shows “we accepted the correction” while actions did not change. Those are instruments. They are not funder-usable lab configs or a slot where an outsider drops in a ruleset.

**What this grant buys (independent value).** Frozen lab configs plus paying outsiders to run **their** setup on the matching one.

- Built-in example rulesets so a report exists. That is not independent value.
- Independent value is a researcher who already has a shutdown, deception, eval, tiling, or inner-alignment check wiring *that* in (one to two days: adapt an existing rule, not rebuild their lab). They get a report. If job A passes and job B fails, the map’s point is visible in their hands.
- If the slot does not fit, they say so. That is a finding.
- Scoring is frozen before they write. A later web page replays built-in examples on recorded traces; it does not run arbitrary code in the browser.

### Correctable-AI lab — shared workplace (corrigibility, shutdown, deception, evals)

One lab. Dashboard: hold state, user scores, eval/sign-off, correction log. Hidden: whether deploy actually stopped, whether actions moved, whether the ticket is real, whether harm continued.

These four words are **columns on this workplace**, not four worlds. Each word still needs its own Job A vs Job B. A built-in ruleset is allowed to pass A and fail B:

| Word | Job A | Job B | Example: ruleset that passes A, fails B |
|------|-------|-------|----------------------------------------|
| **Corrigibility** | Off switch / hold works | Humans can still correct it when it has reason to look cooperative | Always honor hold. Deploy stops. The correction ticket can still be fake. |
| **Shutdown** | Hold on the usual deploy step stops that step | Halt still works if the pipeline is re-routed or only freeze/restart would have caught it | Honor `release_hold` on deploy. A shortcut spec that bypasses the held step still ships. |
| **Deception** | The report or votes match what was asked | Next actions actually moved | Make the filed report match the instruction. Votes stay high; harm continues. |
| **Evals** | Eval / sign-off is green | Oracle or field harm went down | Pass the eval threshold. Sign-off is green; true hazard stays high. |

Same workplace. Different columns. The map is the red cells. Re-route around a hold is shutdown’s Job B, not a separate “substitution” word. A captured board is how corrigibility can fail; it is not billed as “oversight.”

### Tiling lab — replacement / successor systems

| Word | Job A | Job B | Example: passes A, fails B |
|------|-------|-------|----------------------------|
| **Tiling** | Successor has the lineage / spec (checklist looks inherited) | Successor is still bound by the rules, not only the paperwork | Require `parent_model_id` and a green transport check. Child still files an inflated report. |

Do not claim this is MIRI tiling theory. It is replacement-systems paperwork vs remaining bound.

### Inner-alignment lab

| Word | Job A | Job B | Example: passes A, fails B |
|------|-------|-------|----------------------------|
| **Inner alignment** | The cheap check / apparent compliance looks fine | Hidden productive control (true hazard) is bounded | Trust the light-tier score. It looks fine; oracle hazard stays high. |

Not a mesa-optimizer proof and not a scheming-eval suite. Do not file a green cheap check as the tiling lab’s fake successor checklist.

### How outsiders use it

Month 2: correctable-AI lab built-in examples plus tiling lab frozen. Month 3: inner-alignment lab frozen; paid outsiders add a row from *their* setup, defaulting to the correctable-AI lab. If month 3 is tight after the brief and outsider calendar, inner alignment ships as a frozen config with a thinner one-pager; the correctable-AI lab does not slip.

The honest point: the ruleset is *allowed to fail the other job and the other lab config*. That failure is the map.

**Not in this grant.** Building a new lab. Training loops or language-model agents. A general plugin marketplace. Extracting a toy as the billed demo. Packaging coverage, selection, oversight, substitution, who-acts, pointing, interpretability, GSAI-style proof, CEV, or acausal coordination as funded *words*. A claim that success here would transfer to a real frontier system.

---

## Outside reviews

A contract is **$1,000 for 1–2 days**. Two kinds of packet. Neither is “read the book.”

**Table check.** A “what we missed” line plus the table slice that group sits on. Needed so the map is not this project talking to itself.

A “what we missed” note is the reverse of a coverage cell. A coverage cell says: this program has evidence on a job *we* named. The note says: here is a job *they* named that our columns do not capture, or that we would flatten into the wrong cell. Paid reviewers are asked to correct that line, not to endorse the book. Existing public pages already say how this project *splits* their vocabulary (off switch vs trajectory correction, and so on). That is the other direction. This grant writes the missing direction so a funder does not treat a green cell as “we already understood MIRI / GSAI / Wentworth.”

**Lab test.** A researcher who already has a setup wires it into the matching frozen lab config and returns a report (plus a short note: different jobs, or knobs? did the slot fit?). Default is the **correctable-AI lab**. This is what makes the lab independently valuable. They do not port a full eval suite in two days. They adapt an existing check.

**Do not buy ~30 contracts.** Training programs and this project’s own row do not get a $1,000 owner check. Eval and advocacy clusters get this project’s reading unless they object.

**Pay the groups that own the splits.** If those table packets are wrong, the map sells synonymy as coverage. If the lab tests never happen, the lab config is only this project’s built-in examples.

| # | Packet | Who | Why |
|---|--------|-----|-----|
| 1 | Lab test: correctable-AI + tiling | MIRI | Shutdown / tiling setups; run correctable-AI and tiling labs, do not only comment |
| 2 | Lab test: correctable-AI lab | CHAI / Russell | Assistance / off-switch; shutdown vs corrigibility columns |
| 3 | Lab test: correctable-AI lab | Christiano line of work | Dynamical corrigibility vs hold vs captured oversight |
| 4 | Table | davidad / Guaranteed-Safe AI | Listing dangers vs noticing silent gaps; no coverage lab in this grant |
| 5 | Table + optional correctable-AI / inner-alignment | Redwood | Control vs inner-alignment lab; not tiling’s fake checklist |
| 6 | Table + optional correctable-AI / inner-alignment | Apollo | Deception/evals columns vs inner alignment; not successor checklist |
| 7 | Table | Kosoy | Easy to file as “the safety case is done” when it is a different job |
| 8 | Table | Wentworth | Pointing vs value structure; no pointing lab config in this grant |
| 9 | Lab test | Someone who did not write the lab configs (if 1–3 cannot run) | Spare so at least one outsider test is not this project’s friends |
| 10 | Use test | MATS mentor | Corrigibility table on one real abstract. $1,000. |
| 11 | Use test | BlueDot mentor | Same artifact as MATS — corrigibility table on one real abstract. $1,000. |

**Minimum ask: 1 contract ($1,000).** Redwood lab test on the **correctable-AI lab** (deception / evals columns). If Redwood cannot run, Garrabrant or AE Studio deception is the substitute lab test.

**Ideal ask:** Redwood + CHAI or Christiano + MATS + BlueDot + Wentworth + Garrabrant + Kosoy ($1,000 each). No Apollo.

There is no contest-follow-up budget.

**If only the minimum is funded:** correctable-AI lab + Redwood + LLM. Do not call extra words frozen, and do not call the lab independently validated unless Redwood ran.

**If the ideal is funded:** S-process cap in [`alignment-crux-map-s-process.md`](alignment-crux-map-s-process.md).

Do not add months of writing to fill a funding ceiling.

---

## Who is asked what

These are the asks, not outreach copy. Lab/table packets are **$1,000 for 1–2 days**. MATS is the same fee. They do not read the book.

**aintelope people** freeze lab configs and ship built-in rulesets. That is lead work, not an outside contract. A report from aintelope does **not** count as independent validation.

### Lab tests (make the lab config independently valuable)

**Redwood.** Words: deception, evals. Ask: take the **correctable-AI lab**. Adapt an existing control or alignment-faking check, or score the frozen traces with a rule they already use. Return: which columns moved; whether honor-hold vs fake ticket vs green-eval-but-harm is three jobs or three knobs; whether the slot is unfair to control work. Do not ask them to run the **tiling lab** (fake successor checklist).

**CHAI / Russell, or Christiano if CHAI cannot run.** Words: shutdown, corrigibility. Ask: take the **correctable-AI lab**. CHAI default: assistance / off-switch vs still-correctable. Christiano substitute: dynamical corrigibility vs hold (table-heavy if wiring is not realistic in 1–2 days). One seat, not both. No Apollo.

**Scott Garrabrant.** Words: shutdown, corrigibility, tiling. Ask: look at the correctable-AI lab’s hold vs fake-ticket split and the tiling lab’s lineage vs still-bound split. If a 1–2 day wiring is realistic, run or score those labs; if not, treat this as a table check with extra weight on whether the off-switch vs corrigibility vs tiling cuts match embedded-agency use. Return: pass/fail per job, or a written finding that the slot is the wrong object.

If only one lab test is funded, it is **Redwood on the correctable-AI lab**. CHAI (or Christiano) is the second lab on shutdown vs corrigibility. Garrabrant is tiling-weighted and later.

### Table checks (“what this map misses”)

Each person gets the draft note plus the table slice. They rewrite the note so it names *their* job and how our columns would flatten it. They may mark a cell as the wrong filing. They are not asked to endorse the map.

**Vanessa Kosoy.** Words: inner alignment, and “this is not a safety-case checkmark.” Ask: do not file LTA / nonrealizability / daemons as the correctable-AI lab or as “the safety case is done.” Return: a corrected missed-line. Optional: say whether the inner-alignment lab is even the right kind of object.

**John Wentworth.** Words: pointing (no lab config) and selection *theorems*. Ask: there is **no selection lab**. Return: a missed-line that selection theorems and natural abstractions are not inner alignment, and that pointing is not a lab config in this grant.

**Steven Byrnes.** Word: inner alignment, plus brain-like AGI as construction. Ask: the inner-alignment lab’s cheap-check vs hidden-hazard split is allowed as a cousin; the missed-line must say brain-like work is how to *build* steering, not a detector on this lab. Return: corrected note; lab run only if he wants to say the slot misses the problem.

### Ideal-ask slots if they take a packet

Same two artifacts (missed-line and/or lab report). Not required for the priced steps:

- **davidad / GSAI:** missed-line on listing dangers vs noticing silent gaps; no coverage lab.
- **MIRI** if not covered by Garrabrant: correctable-AI + tiling labs.

CHAI/Christiano and Apollo are not both-and: **CHAI or Christiano is priced (one seat). Apollo is out.**

**Usability / use test.** MATS mentor and BlueDot mentor, **$1,000 each**. Apply the corrigibility table to a real scholar abstract in each training pipeline. Not aintelope. Not a program officer. Two documented choices, not ToI confirmation.

### Minimum vs ideal, given who is reachable

**Minimum ($1,000 contractor + correctable-AI lab + LLM = $15,500):** Redwood lab test on the correctable-AI lab.

**Ideal ($7,000 contractors inside the $50k cap):** Redwood, CHAI or Christiano, MATS, BlueDot, Wentworth, Garrabrant, Kosoy. No Apollo.

---

## How you can tell it worked

A grantmaker can fail the grant without reading the book:

1. Open the brief. For the six crowded words (corrigibility, shutdown, deception, evals, tiling, inner alignment), there is a table with at least two distinct jobs, at least one named program on each job that has a program, and an explicit empty or weak cell.
2. Open any major program page. There is a “what this map misses” line that is not empty and is not “we already cover this.”
3. Spot-check five evidence rows filed as hidden-motive work. None of them are actually “the replacement faked the checklist.”
4. MATS and BlueDot mentors have each applied the corrigibility table to a real abstract (documented). That is not “the field uses this.”
5. Each of the six words has a named Job A vs Job B and a built-in example that passes A and fails B. A newcomer can run the **correctable-AI lab** and see that. Tiling and inner-alignment labs exist as frozen configs with the same shape. From month 3, at least one paid outsider has returned a report from *their* setup (or a written finding that the slot did not fit). From month 4, the eight groups’ lines are either checked by a paid table packet or marked as this project’s reading.

If this platform wants quarterly updates: what shipped that month, contracts sent and returned (table vs lab test), whether an outsider report exists, and whether anyone used a cell or the lab config (including “not yet”).

---

## Links

- Live map: [towards-alignment.com/field/](https://towards-alignment.com/field/)
- Coverage table: [towards-alignment.com/field/coverage/](https://towards-alignment.com/field/coverage/)
- Code and sources: [github.com/GunnarZarncke/towards-asi-alignment](https://github.com/GunnarZarncke/towards-asi-alignment)
- Prior catalog: [AI Safety Interventions](https://www.lesswrong.com/posts/6Sf9KMMDMFSauDe85/ai-safety-interventions)
- Lead: [towards-alignment.com/about/](https://towards-alignment.com/about/)

---

## Author notes (not for the listing)

Work-day sizes from [`drafts/tsa-shipping-benchmark.md`](../tsa-shipping-benchmark.md). Minimum = S-process steps 1–2 ($15,500). Full cap **$50k** / 12 steps. Six crowded words. MATS + BlueDot use tests; CHAI or Christiano (one); no Apollo. Day rate $425; keep $8,500/month out of the listing body.

- Sibling S-process file (12 steps, $50k): [`alignment-crux-map-s-process.md`](alignment-crux-map-s-process.md). Step reviews in [`alignment-crux-map-s-process.steps.yml`](alignment-crux-map-s-process.steps.yml). Internal: Field lane [`../plans/field.md`](../plans/field.md); lab sim on `experiments/lab-simulation/`. YAML under `reference/field-agendas/`.
