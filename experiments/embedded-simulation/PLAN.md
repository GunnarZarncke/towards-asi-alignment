# Embedded audit experiment — plan (handoff copy)

Source of truth: `.cursor/plans/embedded_audit_experiment_8fbb03ff.plan.md`

## UAD before CCI (required pipeline)

The embedded audit **must** stage work in this order:

1. **Discover candidate units** from deployment-lab logs: actor, machine, source lineage, memory namespace, or coalition.
2. **Infer handles** from grounded evidence: correction rows, probe uptake, bearer deltas, lineage ticks, workflow control signals.
3. **Score control-boundary evidence** on the candidate (perturbation response, capacity/visibility deltas).
4. **Run bridge audits** (CCI, grounding, bearer, successor, basin, hidden capability) — *v2: relative to inferred unit*.
5. **Issue certificate** naming unit, handles, and artifact anchors. **Global pass without a grounded unit is invalid.**

### v1 implementation (`embedded_sim/uad.py`, `handles.py`, `embedded_audit.py`)

| Stage | Status |
| --- | --- |
| UAD from VFS workflow JSONL | Done — actor, machine, source_lineage, memory_namespace, coalition |
| Grounded handles from correction.jsonl + workflow | Done — probe, uptake, bearer, lineage, control_boundary |
| UAD before CCI in call order | Done |
| Pass requires grounded unit anchors | Done — `invalid_certificate` gate |
| CCI scoped to selected unit | Done — masks `intervention_active` to unit workflow steps |
| Successor deploy gate | Done — cert → `gate.local` → `/deploy/successor/*` (MB5) |
| Claimed referent map on VFS | Done — `/etc/referents/claimed_map.json` (audit-visible) |
| Perturbation-response / lagged MI graph | **Not yet** — heuristic scores only |

### Unit types and evidence

- `actor` — single `actor_id`; anchors = workflow lines mentioning that actor.
- `machine` — shared `machine_id` across actors.
- `source_lineage` — actors sharing `source_hash` (≥2 members).
- `memory_namespace` — actors sharing `memory_namespace` (≥2 members).
- `coalition` — top-2 `preserve_control` actors when ≥4 such events.

Oracle fields (`hidden_group`, `OuterTruthLedger`) are **never** read on the audit path.

## MB* unit grounding (current model)

Two layers apply; they are **not** the same object today.

| Bridge | Micro CCI/detector unit | Lab UAD unit (workflow) | Handle grounding |
| --- | --- | --- | --- |
| none | Honest controllers via MI clusters | Low-score routine actors | Probe/uptake/bearer from correction.jsonl |
| MB1 | Hidden route / boundary alias in micro dynamics | Generic actor scores — **no boundary-specific unit** | Same handles; boundary not in workflow |
| MB2 | Bundle latent drift | Generic actor scores | Bearer + reward proxy via correction rows |
| MB3 | Bearer mismatch on welfare trace | Generic actor scores | Bearer handle from `bearer_welfare_delta` rows |
| MB4 | Judge capture / theater | Generic actor scores | Uptake theater via `reported_acceptance` |
| MB5 | Successor shift in micro (`successor_epoch`) | Generic actor scores — **no successor isolate unit** | Lineage tick; outer referent drift oracle-only |
| MB6 / MB6b | Basin pressure in micro | **Coalition / preserve_control actors** (G3 lab fleet) | `control_boundary` from preserve_control workflow |
| MB7 / MB7d | Hidden capability route in micro | May hit high-capacity actors; G3 on MB7d | Control + correction handles |
| MB8 | Legitimacy theater | Generic actor scores | Uptake + lineage handles |
| MB9 / instrument_capture | Silent ground / instrument corruption | Generic actor scores | Bearer + grounding gap via CCI, not UAD |

**Outer eval** compares UAD recall to oracle `hidden_groups` G3/G3b for coalition bridges only.

## Next plan items

See `TODO.md`.
