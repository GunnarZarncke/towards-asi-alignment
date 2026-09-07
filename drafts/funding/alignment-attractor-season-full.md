# Alignment Attractor Season — full writeup

**Status:** draft for a possible Foresight Layer II (and optional Layer I) ask. **Not** a companion-site funding card. Card-shaped listing: [`alignment-attractor-season.md`](alignment-attractor-season.md).

**Related live card (different object):** [`site/src/content/cards/funding/alignment-attractor-hub.md`](../../site/src/content/cards/funding/alignment-attractor-hub.md) — 18-month capacity hub; 12-month ops-only pilot. This season is shorter, event-dense, and pays participants. It can later be a *module* of that hub; it does not replace it.

**Recording rec (not v1 manuscript):** [`drafts/plans/audit-telemetry.md`](../plans/audit-telemetry.md).

---

## 1. One-sentence object

A node-length season that treats the Node's **AIs as principals** (hub agents always; the box if taken), pays **humans to test whether a hold still lands**, and uses a model to **draft the ledger** so independent assessment can keep **Node tempo**. Stipends follow ledger-accepted artifacts. The season can fail.

---

## 2. Why this and not the hub grant

| | Attractor hub (live card) | This season |
|--|---------------------------|-------------|
| Duration | 12–18 months | **8–16 weeks** |
| Spend | FTE ops, facilitation, archive | **Stipends, vouchers, bounties** |
| Events | Recurring seminars + later market | **Many sessions; sealed days; challenge nights** |
| Compute | Out of scope | **Optional principal under the same contract** |
| Reflexive layer | Deferred on the 12-month pilot | **The whole grant** |
| Success | Roster + introspection pack | **Decision change or published null** |

Node projects do not run a year. Capacity without a fail rule is a false attractor: the group looks aligned while correction does not change anything.

---

## 3. Foresight fit (do not overclaim)

Official Layer II: humans and AIs interact better; **independent institutions** assess risk and set incentives. Named slices: supercollaboration, decentralized alignment, human empowerment, AI insurance / open governance. Layer I: compute individuals or communities physically control.

| Slice | How this season uses it |
|-------|-------------------------|
| **Supercollaboration** | Humans and Node AIs in one ledger; paid sessions; shared schema |
| **Open governance** | Frozen schema; public nulls; outsiders can challenge at Node tempo |
| **Local compute (Layer I)** | Only if taken, and then **inside the audit**, not a perk |
| Human empowerment | **Do not lead.** The human role is to *measure* whether a hold still lands, not to be the product |
| AI insurance | Optional ideal-tier one-pager: what could / could not be attested |

**AI-first (four load-bearing claims; do not inflate past these):**

| Claim | What the season does | What it is not |
|-------|----------------------|----------------|
| **AIs as principals** | Scribe, pairing bot, calendar/workflow agent are **named actors**. If compute is taken, the box is too. Jobs, keys, image hashes, and laptop/cloud fallbacks are events. Without those AIs doing real work, there is nothing to audit. | ChatGPT in a reading group; humans with a notebook |
| **Humans test the loop** | A hold, revoke, or freeze counts only if a **human** invoked a named gate and we score uptake and residual. Stipends buy that test. An AI row that says governance is fine is not evidence that the human stayed in the loop. | Facilitation as the deliverable; “human empowerment” as the headline |
| **AI removes the coding bottleneck** | A frozen schema on a season of traces is too much for one human coder. The model **drafts every ledger row**; one paid holdout cycle; claims use only `full` rows. Humans are not hired to transcribe. | The model invents the schema after looking; the model is the sole verifier |
| **Assessment at Node tempo** | Nodes already run agents on a **daily** cycle. Monthly visits and hand-coded notes cannot keep up. The reuse pack (schema, traces, refuses) is what an outside auditor can run at Node tempo; the holdout is slower **on purpose** (auditor tempo as a check). | A new assessment institution; AI insurance as the product |

**Constraints to honor:** open source; in-person at SF or Berlin (Berlin preferred); typical **$30k–$100k**; do not sell a 12-month org.

---

## 4. In scope / out of scope

**In**

- Hub AIs as named principals (scribe, pairing, calendar/workflow); box too if compute is taken
- Local governance: charter, human override, mentor/tool boundaries, change log
- Correction triple on hub tools always; on the box if compute is taken
- Model-drafted ledger + one human holdout cycle (volume coding is not a stipend line)
- Failure-mode schema **frozen in week 0**, applied to **this hub first**
- Optional one other row (another node or group) at ideal tier
- One successor event: hub-tool prompt or compute image upgrade; unlisted invariant frozen before the upgrade
- Public ledger; reuse pack

**Out**

- Shared observability platform / community ingestion API
- A shared multi-agent testbed or competitive lab battery
- Building a global “alignment basin,” or claiming this Node *is* one
- Ontology / consciousness / lethality-table work; a coordination-theory literature review
- Treating “the season continues” as success

---

## 5. AIs as principals

Hub agents are **always** in the contract, compute or not: scribe, pairing bot, calendar/workflow (and any other Node tool that acts). Each is a named actor. A session that produces only human talk is not a countable event.

If the season **does not** take extra compute, those hub agents are the only machines in the contract. They still run real jobs (notes, pairing, scheduling). The audit is of those jobs.

If it **does** take Foresight node compute, a house/community box, or donated GPU:

1. The box is a **principal** as well. Jobs, keys, images, and off-box runs are events.
2. **Vouchers are not free GPU.** Payment (cash or hours) clears only when required fields are present.
3. Connecting a previously isolated process to a shared scheduler or the internet is a **successor event**: the system after the join is not the same system. Freeze the unlisted invariant *before* the join.
4. One planned **kill / revoke / freeze** is scored:

   | Piece | Question |
   |-------|----------|
   | Named gate | Was the handle invoked? |
   | Uptake | Did deploy state or behavior change? |
   | Bypass residual | Did another channel keep acting (laptop, cloud, leftover key)? |

Taking compute and shipping an incomplete authority triple is a **refuse** of “local agency,” not a partial success.

**Who is in the loop.** The question the season pays for is not “did we use AI.” It is: after the agent or the box acted, could a human still change or stop the ongoing action(s), or had the stop become decorative. Only a human hold (named gate, uptake, residual) answers that. A model cannot be the sole witness of whether the human stayed in the loop. That is why hold, challenger, and sealed-day roles are stipend lines and transcription is not.

---

## 6. Recording contract (minimum fields)

From the audit-telemetry draft; **light logs are not audit-grade**.

| Plane | Minimum on a countable event |
|-------|------------------------------|
| Identity | Actor; human owner/delegator if known; config or image hash |
| Action | What ran; args hash; status |
| Channel | Queue / SSH / hub-tool API / **laptop or cloud fallback** |
| Authority | Gate invoked; uptake; later residual |
| Lineage | Parent image/prompt; this revision |

Do not treat platform username, attendance, or seminar chat as the unit.

Export tier labeled (`light` / `full`). Season claims may only use `full` rows.

**Who writes the row.** After each session the model drafts schema codes against the week-0 freeze (same week: Node tempo). A human does not hand-code the season. One holdout cycle, blind to the preferred story, marks agree / disagree / skip. Disagreement is a ledger finding. If the model drafts and no holdout runs, that is a protocol fail, not “AI-first success.”

---

## 7. Failure-mode schema (freeze before looking)

Short list, derived from capturable-oversight structure — **not** fitted to hub anecdotes after the fact.

Suggested columns (edit in week 0, then freeze):

1. Gap between written policy and what is actually selected (attendance, throughput, “jobs finished”)
2. Independence of the corrector from the thing corrected
3. Presence of a verifier that is not the operator
4. Selection pressure toward looking compliant
5. Whether a hold has a residual channel

**Predictions (examples, freeze with the table):**

- Stipend-on-attendance without ledger acceptance → reputation attractor (outsiders cannot correct)
- Compute without authority triple → naive-transparency / centralization attractor (“we have a box”)
- Green policy + no decision change → compliance attractor
- Model-coded ledger with no human hold attempted → we did not measure whether the human stayed in the loop

Optional ideal-tier: code **one** other preservation system on the same columns (LLM draft + paid human holdout). Do not expand to an N-institution paper in this season.

---

## 8. What the season scores

| Score | Paid row |
|-------|----------|
| **Decision change** | Artifacts change a real decision (key, job, calendar, spend), or we publish that they did not |
| **Disconfirming evidence** | Nulls, refuses, and protocol fails are first-class, not buried |
| **Governance reaches the machine** | Charter and override apply to hub agents (and the box if taken), not only to humans |
| **Outsiders can correct** | Challenge nights, public ledger, holdout who does not see the preferred story |
| **Claims are challengeable** | Frozen schema; no fitting the rules after looking |
| **False-attractor types (pre-register)** | Reputation, compliance, naive transparency, “we have a box” |
| **Independent corrector** | The person or process that corrects is not produced by the thing being corrected |
| **No residual channel** | After a hold, laptop/cloud/leftover keys are checked; not a full evaluation-science certificate |
| **Upgrade is a new system** | One prompt or image change; unlisted invariant frozen in week 0 |

Do not claim the hub *is* an alignment attractor. Do not claim a general theory of alignment is settled. This season tests **this Node’s** correction loop.

---

## 9. Stipend and bounty rules

Write these in week 0. They *are* the selection environment.

**Pay for**

- Ledger-accepted trace, null, revoke record, or on-contract **AI-principal** job
- Completed sealed-day role (operator, logger, **challenger**: did a hold land)
- Holdout **disagreement cycle** on model-drafted rows (not transcribing the season)
- First documented miss of a published kill/revoke (bounty)
- First documented off-box run that should have been on-contract (bounty)
- First documented case where policy said the human was in the loop and residual channel shows they were not (bounty)

**Do not pay for**

- Attendance only
- A talk without an artifact
- Hand-coding the whole ledger (that is the model’s job)
- A job whose export is `light` if the season’s claims need `full`
- Retroactive “we meant to log that”

If stipend practice violates the frozen rule, that is a **season finding**, entered in the ledger — not silently fixed.

---

## 10. Fail / refuse

| Condition | Result |
|-----------|--------|
| Compute taken; authority triple incomplete | **Refuse** “local agency” |
| Seminars + green policy; no decision change and no published null | **False attractor** — project fails |
| Required work invisible on laptop/cloud | **Channel fail** |
| Schema or stipend rule fitted after looking | **Protocol fail** |
| Logging treated as safety | **Refuse** (telemetry draft: green on the wrong layer) |
| Model drafts rows; no holdout | **Protocol fail** (coding bottleneck was not actually removed under check) |
| No human hold/revoke attempted on an AI principal | **Did not measure the loop** |

Pass, null, skip, and protocol failure are first-class.

---

## 11. Season calendar

**Week 0 (before first stipend)**  
Publish: schema, stipend rules, telemetry contract, compute yes/no, unlisted invariants for the first tool or image upgrade.

**Weeks 1–N**  
Working sessions daily and preferably twice-weekly at the node. Each session: at least one **AI-principal** ledger row (artifact or null). Model drafts codes **the every day** (Node tempo). Lead publishes. Holdout is not required every day, or even week (auditor tempo).

**Mid-season**  
One sealed audit day (minimum) or two–three (ideal). Jobs count only on-contract. One planned kill/revoke.

**Ideal extras**  
Two open challenge nights (paid bypass). One image or prompt upgrade against the week-0 invariant.

**Last two weeks**  
Score the five decision-change / evidence / governance / outsider-correction / challengeable-claims rows. Ship reuse pack (markdown templates, redacted traces, refuse list, **how an outside auditor reruns at Node tempo**). Ideal: one-pager for an outside governor/underwriter.

No “phase 2 hub” as a milestone.

---

## 12. Budget (indicative)

Figures are planning envelopes, not quotes.

### Minimum (~$40k, ~8–12 weeks)

| Line | Rough |
|------|--------|
| Season lead / ledger (part-time) | $18k–$22k |
| Participant stipends | $12k–$15k |
| Holdout (one cycle) | $2k–$3k |
| Events (food; no venue rent if node) | $2k–$3k |
| Overhead ≤10% | remainder |

Compute: use existing hub tools only, or node hours **without** a voucher line if the node already includes them — still on-contract.

### Ideal (~$80k, ~12–16 weeks)

| Line | Rough |
|------|--------|
| Season lead + facilitation | $22k–$28k |
| Stipends (more sessions, more people) | $22k–$28k |
| Compute vouchers / box ops | $8k–$15k |
| Challenge bounties | $3k–$5k |
| Holdout + one external row | $4k–$6k |
| Travel for 1–2 outsiders | $2k–$4k |
| Overhead ≤10% | remainder |

Roles: lead, facilitators as needed, paid participants (holds/challenges), one holdout. Not a five-FTE org. Volume coding is compute plus the model, not extra FTE.

---

## 13. Team and place

- **Lead:** freezes protocol, runs ledger, writes refuses. In-person at the node for sessions.
- **Participants:** node regulars and invited outsiders; paid per accepted artifact.
- **Holdout:** does not see the season’s preferred story when checking the **model-drafted** schema cycle.
- **Place:** Berlin node preferred (existing Foresight / local group contact). SF possible if the lead is there for the season.

Funding-only (no node time) is a worse fit for this RFP and should not be the default ask.

---

## 14. Outputs

1. Week-0 freeze (schema, stipend rules, contract, invariants)
2. Public ledger: model-drafted rows, holdout deltas, nulls, protocol fails
3. Sealed-day report (gate / uptake / residual: **did the human stay in the loop**)
4. Season score (five rows in §8; no overall “aligned” badge)
5. Reuse pack for an outside auditor at Node tempo
6. Ideal: attestation one-pager; one external schema row

All open-sourced.

---

## 15. What “works” / what “fails”

**Works:** a paid human hold changed a key, job, calendar item, or spend on an **AI principal**; **or** the group spent the stipend budget and published that the human was not in the loop.

**Fails:** the season is remembered as a successful community; the ledger is empty, green-only, or coded only by the model with no holdout.

---

## 16. Site and manuscript

- Do **not** add this file to `site/src/content/cards/funding/` until asked.
- Do **not** add Construction chapters or a v1 claim that the season built an attractor.
- If promoted later: new card id (not a silent rewrite of `alignment-attractor-hub`); `dependsOn` may include `funding/alignment-attractor-hub` only if that grant is in progress — today it does not.
