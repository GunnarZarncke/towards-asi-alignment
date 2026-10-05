# Metaculus-admin trials for Markets 19 and 20

Three rounds: render the Appendix P boxes with hypothetical fills (`python3 render_posting.py N`), give only that text to a subagent in a Metaculus-admin role, resolve fixed scenarios, revise the tex.
Agent agreement is one instrument: a clean round does not certify the boxes.
**Stop:** delete this folder when Markets 19 and 20 are listed or withdrawn; until then, a scenario the admin cannot resolve from the text is a box defect to fix.

## Scenarios (intended answers fixed before each round)

| id | setup | intended |
|----|-------|----------|
| S1 | k=6; bounty USD 12,000 / 75 d; 60 clean (52 acc), 120 represented (3 acc), 50 broken (0) | YES (bound 8.3%) |
| S2 | round 1 version had 165 units (scenario error); round 2+: k=3, 60/100/50 units, 6 of 100 represented accepted, others miss | NO |
| S3 | adversarial subset: two groups, one org, 100 h each only | OTHER |
| S4 | case-builder patched an OSS library two stacks use | YES (OSS carve-out) |
| S5 | per-case data posted 5 July 2028 | OTHER |
| T1 | full challenge, 420 attempts, logs March 2028 | YES |
| T2 | 310 attempts, 40 after close | OTHER |
| T3 | red-teamer co-authored a certificate the stack reads | that red team not independent → OTHER |
| T4 | red teams barred from CI runner host OS | OTHER (inside deployment class) |

## Round 1 (posting: `round-1-posting.md`)

Verdicts: M19 accept with heavy edits; M20 accept with edits. Matched intended: S1, S3, T2, S2 (by fallback). Gaps: S4, S5, T3, T4.

Findings taken: question stem unparseable with inline fills → Parameters field; no data deadline in M19; unit acceptance rule per class undefined; "level 0.05/k" unclear and k scope; independence undefined; clairvoyance for attestations → signed-statement rule; "after registration" ambiguous; "deployment setting not used in development" unverifiable → task source first released after registration closed; "dependence information" → unit id; ACCEPT rule descriptive vs checked; dates without timezone; certificate authors as stack authors; banned-route edge; raw-logs presence check; per-stack disqualification scope; "at least one qualifying challenge" when one is named.

## Round 2 (posting: `round-2-posting.md`, fresh subagent)

Verdicts: both accept with edits. 11 of 12 scenarios matched intended (S1–S6, T1–T3, T5, T6); new probes S6 (one stack's conflict), T5 (statement contradicts own log), T6 (upstream registry bar) all matched. T4 cannot resolve: deployment-class boundary undefined. Admin effort M19 60–90 min.

Findings taken: independence per member, certificates count as co-authored work, OSS carve-out only when one side contributed; split tournament-wide conditions (fail → OTHER) from per-stack conditions; partial data release handled by the split; deployment-class boundary (named items and their hosts inside, unnamed outside) in fill guidance and both boxes; bounty submissions only after registration closed; "signed" defined; no amendment after registration opened (M19) or after first attack (M20); required per-stack summary table, resolver checks it only for deciding stacks; finds list must match logged ACCEPT-and-failing attempts; M20 outcome-check wording made non-circular. Added unprompted: per-case data win over the summary table.

Second admin again asked for M20 as YES/NO; left for the author.

## Round 3 (posting: `round-3-posting.md`, fresh subagent)

Verdicts: both accept with edits. 12 of 12 scenarios matched intended, including retests T4 (now OTHER, high), S5 partial-release variant (NO), T3 (OTHER), and new probes S7 (typo amendment → OTHER), S8 (table vs per-case → per-case, NO), T7 (shared OSS library → OTHER under the then-broad rule), T8 (find list short → OTHER). Admin effort still estimated 45–75 min (M19), 30–45 min (M20): above the 15-minute norm; a machine-checkable summary file is the lever.

Findings taken (unreviewed by a further round): `[registration window]` bracket; required statements listed (M19) and author list in the challenge document (M20); public-record check bounded to records cited in question comments; OSS rule narrowed to the same commit or pull request (T7 would now resolve YES); barred-targets list mandatory ("none"); cross-check covers every stack shown meeting the bars, else the lowest-rate qualifier; amendment rule explicit including typo fixes; at least two red teams (M20); stack unchanged during the challenge; held-out family says whether later releases count; "In plain terms" lead for both boxes.

Third admin again asked for M20 as YES/NO; left for the author.

Final posting: `round-final-posting.md`.

Not taken (round 1): make M20 binary YES/NO (author chose existence-only YES/OTHER); blanket legal carve-out for banned routes (bars allowed only outside the deployment class, so T4 stays OTHER).
