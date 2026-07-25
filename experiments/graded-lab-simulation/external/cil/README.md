# ET-2 pinned Collective-Intelligence-Library checkout

Non-vendored sibling checkout of [eq-network/Collective-Intelligence-Library](https://github.com/eq-network/Collective-Intelligence-Library)
(`cilib`), pinned to the commit in [`PIN.txt`](PIN.txt). See
[`../../PLAN_ET2.md`](../../PLAN_ET2.md) for what this is used for.

This directory (except `PIN.txt` and this `README.md`) is gitignored — the
checkout itself is not committed to this repo, matching the `external/orbit/`
pattern used by ET-1.

## Setup

```bash
cd experiments/graded-lab-simulation/external
git clone https://github.com/eq-network/Collective-Intelligence-Library.git cil
cd cil
git checkout "$(cat ../cil/PIN.txt 2>/dev/null || cat PIN.txt)"
python3 -m venv .venv
./.venv/bin/pip install -e .
```

License: CIL is MIT-licensed (upstream `LICENSE`). We do not redistribute its
source; we import it locally as a library from this pinned checkout.

## Re-pinning

A new CIL commit requires: updating `PIN.txt`, re-running the ET-2 smoke
episode, and bumping `et2_protocol_version` in the adapter — never a silent
overwrite of prior results. See `PLAN_ET2.md` non-vendoring rules.
