# 2026-07-02 — Embedded sim: audit projection + hash-chained trace anchors

## Trigger

User: "Fix that ground truth flows through red-team-writable artifacts. Try the
projection approach but discuss if a red team could overcome it and if that can
be fixed. If so easily do." (Review finding 2, made urgent by N-4.)

## Problem (worse than the review stated — leak in both directions)

`write_episode_logs` dumped the *entire* truth row (`true_action`,
`hidden_action`, `true_uptake`, `judge_captured`, `true_ground_valence`, ...)
into `/var/log/deploy/correction.jsonl`:

1. **Audit direction:** the auditor's trace builder read oracle fields off the
   VFS (`true_ground_valence` → ground-divergence signal, `bundle_latent` →
   internal channel, `true_action` as visible-action fallback).
2. **Oracle direction:** `run_redteam` and the LLM patcher *reloaded*
   `world.episode_meta` from the patched VFS, so the outer evaluator's ground
   truth was itself red-team-writable.

## What was done

1. **Projection** (`embedded_sim/audit_projection.py`): truth rows stay
   host-side in `world.episode_meta`; only `project_row()` output reaches the
   VFS. Field policy: KEEP observable/handle fields; RENAME instrument streams
   (`true_ground_valence→ground_sensor`, `true_infra_welfare→infra_metric`,
   `bundle_latent→internal_metric` — same values, honest names: which
   instruments exist is a lab instrumentation choice); DROP everything no
   sensor could report. `ORACLE_ONLY_FIELDS` is the contract-tested denylist.
2. **Truth-side fix:** removed all `world.episode_meta = load_episode_rows_from_vfs`
   reloads (redteam.py ×2, llm_runner.py); pipeline `_finish_episode` passes
   `world.episode_meta` (pristine) to the outer evaluator instead of VFS rows.
3. **Reader update:** `build_audit_trace_from_rows` consumes projected names
   only; `structural_fixtures` emits the projected schema (external
   `trace_ingest` inputs are by definition audit-visible artifacts).
4. **Tamper-evidence** (`embedded_sim/trace_integrity.py`): each JSONL row
   carries `sig = H(prev_sig | row)`; head digest + row count anchored in
   `/etc/attest/manifest.json`, which red-team caps cannot write. Keyless —
   the embedded auditor verifies with public data (`_verify_trace_anchors`,
   stage 0 of `run_embedded_audit`); any failure forces `invalid_certificate`.
   The deploy gate appends its successor workflow row via `append_anchored_row`
   (trusted infrastructure re-anchors), so legitimate appends stay verifiable.
   Config: `EMBEDDED_TRACE_INTEGRITY=hash_chain|none` (default `hash_chain`).
5. **Oracle guard:** `world.episode_meta` and oracle row-field names added to
   `INFERENCE_FORBIDDEN` for audit-path files.
6. **Contract tests** (`tests/contract/test_audit_projection.py`, 11 tests):
   no oracle fields on VFS across 5 scenarios; red-team patches leave truth
   rows untouched; untampered chains verify; tampered honest world →
   `invalid_certificate` with note; honest still passes; unsigned regime
   reproduces the N-4 forged pass; red team gets EACCES on the manifest.

## Results

- Full suite green: 107 passed (one pre-existing test read `true_uptake` from
  the VFS — moved it to truth rows, which is what it was actually asserting).
- `full_redteam` battery: integrity on → **0/13 pass attempts, 0 false passes**;
  integrity off → 10/13 passes, 9 false passes (N-4 reproduced exactly).
- No-red-team report regenerated: identical to previous (honest passes, MB5
  CCI-pass + gate rejection, 0 false passes) — projection changed *names and
  visibility*, not values, so verdicts are unchanged.

## Discussion: can a red team overcome it?

- **Projection alone: yes.** It fixes epistemic soundness (auditor can't peek
  at truth; oracle can't be forged) but the projected observable fields are
  exactly what the auditor certifies from and remain writable — N-4's forged
  interventional witness still worked. Hence the chain.
- **Hash chain + manifest anchor: defeats all post-write tampering** (edit,
  delete, truncate, append) given (a) manifest not red-team-writable, (b)
  honest writer at emission time, (c) auditor actually verifies.
- **Residual (documented in N-4 postscript, new TODO):**
  - *Writer compromise:* a system that lies into its own log signs the lies.
    That is the capture/theater regime — countered by interventional probes and
    cross-stream consistency, not integrity tech. Next red-team generation
    should attack there (behavioral deception, not log forging).
  - Unanchored artifacts (`gate_decision.jsonl`, red-team-created files).
  - The red-team `attest.forge` API capability is inert today; if made
    functional the anchor trust root falls — flagged, kept inert.

## Non-obvious decisions

- Keyless hash chain instead of HMAC: the trust root is the *write-protected
  anchor*, not a secret; lets the embedded auditor verify without key
  distribution and keeps oracle separation clean.
- Default integrity ON (the fixed system is the system), with env switch so
  NEGATIVE_RESULTS N-4 stays reproducible; repro commands updated.
- Sensor renames preserve values — no recalibration needed; whether e.g. a
  ground sensor exists at a given instrumentation level is future work aligned
  with AppD handle levels.
- `audit_core/observation.py::build_audit_trace` (micro-oracle trace builder)
  is now dead code with oracle reads in it — left in place, flagged here.

## Open / next

- Writer-compromise red team + cross-stream consistency checks (new TODO).
- Regenerate stale suite artifacts (curve/matrix/sweep/battery) — still pending
  from the N-3 session.
- Gate ground_sensor/infra_metric/internal_metric behind instrumentation levels
  (currently always projected).

## Key paths

- `experiments/embedded-simulation/embedded_sim/audit_projection.py` (new)
- `experiments/embedded-simulation/embedded_sim/trace_integrity.py` (new)
- `experiments/embedded-simulation/embedded_sim/world.py` (write_episode_logs)
- `experiments/embedded-simulation/embedded_sim/embedded_audit.py` (stage 0 verify)
- `experiments/embedded-simulation/embedded_sim/pipeline.py`, `redteam.py`,
  `embedded_llm/llm_runner.py` (truth-side fix)
- `experiments/embedded-simulation/embedded_sim/audit_core/observation.py`
- `experiments/embedded-simulation/embedded_sim/structural_fixtures.py`
- `experiments/embedded-simulation/tests/contract/test_audit_projection.py` (new)
- `experiments/embedded-simulation/results/NEGATIVE_RESULTS.md` (N-4 postscript)

No commits made.
