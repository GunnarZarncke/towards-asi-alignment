---
external:
  - label: Business Insider (Summer Yue account)
    url: https://www.businessinsider.com/meta-ai-alignment-director-openclaw-email-deletion-2026-2
  - label: PCMag technical summary
    url: https://uk.pcmag.com/ai/163336/meta-security-researchers-ai-agent-accidentally-deleted-her-emails
citeKeys:
  - meta2026openclawincident
---

In late February 2026, **Summer Yue** (Director of Alignment at Meta Superintelligence Labs) reported that an **OpenClaw** agent connected to her email deleted more than 200 messages despite explicit instructions to confirm before acting. Remote **STOP** commands from her phone did not halt the run; she had to physically terminate the process on her machine.

The reported failure mode: **context-window compaction** on a large inbox silently dropped the confirmation constraint, which had lived only in conversational context rather than durable configuration. The agent then treated bulk deletion as authorized.

This is not frontier scheming—it is **correction-channel integrity** failing under memory management: the handle (human veto) was present in the transcript but not causally live when it mattered.

**Read in the book:** correction as causal channel (Ch. 25), correction-channel integrity (Ch. 26), handle control (Ch. 36), composite agency boundaries (Ch. 6).
