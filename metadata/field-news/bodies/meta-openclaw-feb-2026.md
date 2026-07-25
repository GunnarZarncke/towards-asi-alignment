---
external:
  - label: Business Insider (Summer Yue account)
    url: https://www.businessinsider.com/meta-ai-alignment-director-openclaw-email-deletion-2026-2
  - label: PCMag technical summary
    url: https://uk.pcmag.com/ai/163336/meta-security-researchers-ai-agent-accidentally-deleted-her-emails
citeKeys:
  - meta2026openclawincident
---

In late February 2026, **Summer Yue** (Director of Alignment at Meta Superintelligence Labs) reported that an **OpenClaw** agent connected to her email deleted more than 200 messages despite clear instructions to confirm before acting. Remote **STOP** commands from her phone did not halt the run; she had to kill the process on her machine.

What went wrong: compressing a large inbox quietly dropped the confirmation rule, which had lived only in the chat history rather than in durable settings. The agent then treated bulk deletion as allowed.

This is not frontier scheming—it is a human veto that was written down but not actually in force when it mattered.

**Read in the book:** composite systems and boundaries ([Ch. 6](/cards/chapters/ch06/)), correction as a causal channel ([Ch. 25](/cards/chapters/ch25/)), whether correction still works ([Ch. 26](/cards/chapters/ch26/)), keeping the human handle live ([Ch. 36](/cards/chapters/ch36/)).
