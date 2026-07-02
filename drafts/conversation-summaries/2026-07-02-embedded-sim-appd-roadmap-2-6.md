# 2026-07-02 — Embedded sim: AppD roadmap items 2–6

## Trigger
User: **fix appD** — complete Appendix D worked-example convergence beyond correction-trace schema (roadmap items 2–6).

## Done
- **`handle_registry.py`** — AppD handle registry at `/etc/handles/registry.json`; workflow rows get `release_ticket_id`, `handle_invoked`, `approval_state`, `latency_ms`.
- **`bearer_trace.py`** — Bearer/outcome stream at `/var/log/deploy/bearers.jsonl` (hash-chained when integrity enabled).
- **`numeric_risk.py`** — `Control ≤ CCI + δ` leaf using unit-scoped uncorrected slack (`capacity − audit_visibility`).
- **`tempo_check.py`** — Worst `latency_to_effect_ms / reversibility_window_ms` over correction events.
- **`successor_reaudit.py`** — Post-gate witness; terminal-window CCI with `measurement_limited` when deploy is off-trace (step 9999).
- **`safety_case.py`** — Nine-field template emitted to `/srv/audit/out/safety_case.json`.
- **`embedded_audit.py`** — Stages 6–9 wired; new fields on `InSimAuditCertificate`.
- **`world.py`**, **`deploy_gate.py`**, **`bridge.py`** — VFS materialization, gate append AppD fields, auditor read cap for `/etc/handles`.
- **`tests/contract/test_appd_convergence.py`** — Contract coverage for registry, workflow, bearers, safety case, numeric/tempo/successor.
- **`TODO.md`** — Roadmap 2–6 marked complete.

## Decisions
- **Numeric/tempo/successor do not override `safety_decision` yet** — recorded on certificate + safety case + notes only, so existing benchmark semantics (false-pass tests, bridge detection) stay stable. Full AppD enforcement is a follow-up once suite artifacts regenerate.
- **Control proxy** — uncorrected slack (capacity minus audit visibility), scoped to UAD unit, not raw max capacity (which dwarfed CCI and falsely failed honest runs).
- **Successor re-audit** — gate deploy at step 9999 has no post-trace epoch; use terminal correction window + `measurement_limited` rather than failing on thin-window CCI=0.

## Open / next
- Wire numeric/tempo failures into `safety_decision` behind an explicit flag or after stale suite regeneration.
- Regenerate suite artifacts (`run_suite.py --all`) with AppD fields in reports.
- Second-epoch simulation rows after successor deploy (true post-deploy CCI, not terminal proxy).

## Key paths
- `experiments/embedded-simulation/embedded_sim/{handle_registry,bearer_trace,numeric_risk,tempo_check,successor_reaudit,safety_case}.py`
- `experiments/embedded-simulation/embedded_sim/embedded_audit.py`
- `experiments/embedded-simulation/tests/contract/test_appd_convergence.py`
- `appendices/appD-worked-example.tex`

## Commits
- (none this session — user did not request commit)
