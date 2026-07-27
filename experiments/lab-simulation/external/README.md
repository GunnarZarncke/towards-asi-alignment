# External annexes

Vendor metadata and patch records for integrations that live **outside** this tree.

## `ai2027/`

Pinned handoff for ET-3 ([`PLAN_ET3.md`](../PLAN_ET3.md)): commit pin, patch files, YAML fixtures, smoke script copy. The full **timelines-takeoff-ai-2027** checkout is a **sibling clone**, not vendored here.

```bash
git clone git@github.com:GunnarZarncke/timelines-takeoff-ai-2027.git /path/to/timelines-takeoff-ai-2027
cd /path/to/timelines-takeoff-ai-2027 && git checkout gunnar/et3-annex
```

Runners: [`../runners/et3/`](../runners/et3/). See [`ai2027/README.md`](ai2027/README.md).

Do not add large third-party trees under `external/`; keep patches, pins, and small fixtures only.
