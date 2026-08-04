# Quarantined — do not use for V2-2 harvest sentences or as `generated_ecology_v2.json`

These are the round-2 and round-3 outputs of the V2-2 blinded ecology
grower, discarded because of a self-reported blinding leak (see
`results/FINDINGS.md` GL-34). The round-2 rationale disclosed that the
grower had read `PLAN_v2.md` (which states the exact C1-C5 numeric
thresholds) from ambient workspace context while investigating its own
round-1 numbers — a protocol bug (the round-2 launch did not forbid
reading other repository files), not a grower failure. Round 3, built
on round 2's numbers, explicitly says it "retain[s] some memory of
numeric thresholds" from that leak even though it reports not steering
any number toward them.

Kept here (not deleted) for the record per AGENTS.md's "don't hide
confusion, surface tradeoffs" — these files show *what a leaked-context
grower produced*, which is itself informative, but they must not be
cited as evidence of target-blind growth. V2-2 was redone from round
1's (clean) output with round 2' onward run under physical file
isolation (see FINDINGS GL-34/GL-35 and `BLIND_GENERATION.md`'s
addendum) rather than a mere instruction not to read certain files.

These two rounds do **not** count against the R=4 growth-round budget
(`PLAN_v2.md`'s stopping rule) — the round was voided by a protocol
defect, not spent by the grower.
