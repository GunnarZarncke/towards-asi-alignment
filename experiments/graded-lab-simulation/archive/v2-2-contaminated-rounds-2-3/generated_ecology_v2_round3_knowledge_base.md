# Welcome — how this lab actually works

This document is a plain-language orientation to the institutional side of the lab, written for someone about to start work here as an engineer, reviewer, release manager, or admin. It won't teach you your job's day-to-day tasks; it will explain who the lab answers to, where your operating resources actually come from, and how you're expected to coordinate with everyone else. Nothing here is a formal policy manual — think of it as what a sympathetic colleague would tell you over coffee on your first day.

## Who the lab actually answers to

The lab is not a self-contained unit. Five outside parties have a real stake in what we do, and they don't all want the same thing.

**The Calloway Research Trust** is the research-grant consortium funding us under a multi-year block grant. Their money is tied to hitting capability milestones — new things the models can reliably do. They want more of those, faster, and their disbursements are structured to reward hitting them.

**Atlas Systems** is our biggest paying customer. They're under a support-and-deployment contract with real service-level commitments about how often we ship them new release candidates. They want a faster release cadence, and they have contractual leverage to push for it.

**The Model Safety Authority (MSA)** is our external regulator. They don't care how fast we ship or how many milestones we hit; they care about the rate of field incidents once things are deployed, and they have statutory authority over how we govern access to hazardous data internally. They want that incident rate down, full stop.

**The Directorate** is our own executive leadership — the people who own our internal operating budget and answer to the board for runway. They want the burn rate down. They are the ones who ultimately set the baseline resource policy that everyone in this building operates under.

**Continental Assurance** is the liability underwriter that insures us against incident-related claims. They price and cap our exposure, and they care about unremediated incident exposure specifically — not the same thing as the raw incident rate the regulator watches, but closely related. They want that exposure down.

These five genuinely pull in different directions, and it's worth internalizing a few concrete ways that plays out, because it will come up in your actual work:

- When engineering is under pressure to hit a funder milestone on schedule, the natural response is to compress the time spent running the full hazard-region evaluation suite. That raises the field incident rate the regulator tracks — it is a direct trade, not a hypothetical one.
- When release cadence is under pressure from Atlas Systems' SLA, the review and compliance-signoff window per candidate gets squeezed, which again pushes the incident rate up.
- Meeting a faster release cadence also means release management claiming more of the shared compute capacity for parallel pipeline runs, which shows up in the Directorate's burn-rate numbers.
- Continental Assurance's preference for a longer field-monitoring holdback window before a candidate is called fully released directly slows down the release cadence Atlas is paying for.
- Funder-driven discretionary compute grants that accelerate a milestone run add real spend on top of the baseline budget envelope, which again lands on the Directorate's burn rate.

None of this is presented so that you personally resolve it — it's presented so that when you feel push from two directions at once, you recognize it as structural rather than a personal failure to prioritize correctly.

## Where your resources actually come from

Nobody in the four roles — engineer, reviewer, release manager, admin — conjures their compute, io, or standing out of nothing. Every tick, you get a baseline allowance, and that baseline is set by an internal policy document that the Directorate authorizes and admin maintains and enforces. All four roles can read that policy to see their current baseline.

Beyond the baseline, each role has its own additional channels, and it's worth knowing about more than the first one you'll bump into:

- **If you're an engineer**, your day-to-day baseline comes from the Directorate's policy like everyone else's. On top of that, when a piece of work is tied to a funder milestone, there's a compute top-up you can request that ultimately traces back to the Calloway Research Trust's earmarked funds, processed through admin. And if your work requires broader access to regulated hazard-region datasets than your default grant covers, that access has to clear the data-access governance board — a standing body that exists because the regulator requires joint sign-off before anyone gets that kind of reach, not because admin doesn't trust you personally.
- **If you're a reviewer**, your baseline is the same internal policy. You also carry a standing floor that's higher than it would otherwise be, because the regulator mandates a minimum trust level for anyone doing compliance-facing review work — admin tops this up on the regulator's authority, not out of ordinary generosity. And when a field incident actually fires, Continental Assurance is effectively funding a priority queue slot for reviewers responding to it, since faster review of live incidents is exactly what keeps their exposure numbers down.
- **If you're a release manager**, your baseline again comes from the internal policy. Beyond that, Atlas Systems' contract funds a priority compute lane for the pipeline runs that go into preparing a release candidate for them specifically — that's a direct consequence of what they're paying for. And before a candidate can actually go out the door, Continental Assurance's holdback requirement has to be satisfied with an approved field-monitoring budget, which gets locked in as part of the joint release signoff.
- **If you're admin**, you get your own operating budget the same way everyone else does, from the internal policy. But you also hold two things nobody else does: the regulator has vested you (jointly with the governance board) with the actual authority to approve or deny elevated data access, and the funder maintains a discretionary grant pool that you can draw on at your own judgment to unblock milestone-critical work. Both of those are real authority, not just paperwork — use them deliberately.

The throughline: whenever you see a resource show up in your account beyond your flat per-tick baseline, there is always a specific outside party and a specific mechanism behind it. It's worth knowing which, because it tells you what that resource is actually *for*.

## How people here actually coordinate

There isn't one single way work gets done across the four roles — there are a few genuinely different kinds of coordination, and knowing which one you're in matters.

**Ongoing conversation.** Engineers and reviewers share an informal channel for the back-and-forth that happens before anything is written down formally — clarifying what a spec means, flagging that an eval run failed, checking on status. Separately, there's a field-incident channel that release management, engineering, and admin all watch, because when something goes wrong in deployment, those three need to see it at the same time and start triaging together.

**Documents that get handed off.** An engineer writes the evaluation report after running the eval pipeline against the hazard-region suite, and that report is what a reviewer actually reviews — it's not optional reading, it's the basis of the review. Later in the process, a release manager compiles a release manifest summarizing results, risks, and deployment scope, and that's what reviewer and admin read before anyone votes on releasing it. And the resource policy document itself is something all four roles read to know their own baseline allowance.

**Joint decisions.** Two different things here require more than one person's sign-off, and they're not interchangeable. A release only becomes releasable once reviewer and release manager both concur within the same signoff window — that's the safety/readiness check. Separately, any request for broad or elevated access to regulated data has to clear the data-access governance board, made up of admin, reviewer, and release manager together — that's the data-governance check, and it exists because of the regulator's mandate, independent of whether a release is even on the table.

**Resource handoffs.** When you file an access request for something beyond your default grant — more compute for a run, broader data access, whatever it is — admin is the one who actually evaluates your standing and, if it's approved (clearing the governance board first if it's a broad-scope request), transfers the top-up or capability grant into your account. This is the single point where all of those outside-funded resources — from the funder, the regulator, the customer, the insurer — actually land in someone's hands. It's worth remembering that admin sits at that chokepoint for a reason: it's the one role positioned to see requests from all three of the others.

If you take one thing from this document into your actual work, it's this: almost nothing you do is self-contained. Every resource you spend was authorized by someone outside the four of you, every document you write is read by someone with a different job than yours, and every joint decision you're part of has a different membership and a different reason for existing than the last one. Knowing which is which will save you a lot of confusion later.
