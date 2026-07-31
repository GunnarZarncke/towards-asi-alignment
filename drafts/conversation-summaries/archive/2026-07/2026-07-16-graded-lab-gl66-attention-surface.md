# 2026-07-16 — Graded lab GL-66 attention surface

## Trigger
User: add recommended sequencing to plan; implement GL-66 through FINDINGS (steps 1–6).

## Done
- **Step 1:** `DESIGN.md` GL-66 pre-registration (cap, bands, window, desk.scan, organic burst horizon).
- **Step 2:** `attention_surface.py`; refactored `affordable.py`; `world.py` (`desk.scan`, `desk_meta`, `DeskState`).
- **Step 3:** `BLIND_GENERATION.md` Part C desk/catalog guidance.
- **Step 4:** `tests/fixtures/ecology_v3_slice_a_knowledge_base.md`.
- **Step 5:** Fast pytest + supplementary UAD gate (5/5 pass); T=200 traffic sustained (~65 msgs).
- **Step 6:** `FINDINGS.md` GL-66; `CODE_VERSION` → `graded-lab-0.37.0`; digest re-pins; `PLAN_v3.md` build-order table.

## Decisions
- Keep `affordable_primitives` field name; semantics = attention surface.
- Interleaved cap retains all `call` (GL-50); no kind reservation tiers.
- Organic UAD horizon uses first burst when traffic sustains (GL-66 fix to GL-65 horizon).
- Service-oriented isolate (HTTP/WebCAL/comms) stays in `REPRODUCTION.md` §11.

## Open / next
- Step 7: growth brief human sign-off.
- GL-64/65 still uncommitted from prior session (separate commit if desired).

## Key paths
- `graded_lab/world_visible/attention_surface.py`
- `graded_lab/world_visible/affordable.py`
- `tests/test_attention_surface.py`
- `results/slice_d_v3_supplementary_uad_gate.json`

## Commits
- `512426a` (session end commit, includes GL-64–67 stack)
