# Alignment Crux Map — field lane / grant plan

Status: **draft listing + S-process ready** (2026-09-04). Awaiting funder submission / first contract send. Not funded yet.

**Lane:** Field hub + [`experiments/lab-simulation/`](../../experiments/lab-simulation/) packaging. Sibling: [`field.md`](field.md) (MB homograph divergence in Lean + App B); this plan is the **funder-facing job map + outsider tests**, not spine work.

**Non-goals:** New book chapters; new lab platform; Apollo; coverage/selection/oversight/substitution as billed *words*; claim that the field uses the map without documented use tests; discharge any `MB*` bridge.

---

## Goal

Publish a **job-level** map for six crowded labels funders and newcomers actually use—**corrigibility, shutdown, deception, evals, tiling, inner alignment**—plus frozen lab configs where a fix for job A can fail job B, and **paid outsider** table/lab packets so the map is not this project talking to itself.

**Success (funder-visible):**

1. Tables + brief on [towards-alignment.com/field/](https://towards-alignment.com/field/) with Job A vs Job B per word and named empty/weak cells.
2. **Correctable-AI lab** frozen with built-in rulesets (minimum: honor-hold → shutdown green, corrigibility red).
3. At least **one outsider lab report** (Redwood on correctable-AI lab) if minimum is funded.
4. At least **one documented use test** (MATS and/or BlueDot corrigibility table on a real abstract) if ideal is funded.
5. “What this map misses” lines for major agendas (Wentworth, Kosoy, Garrabrant, etc.) checked or marked as author reading.

**Weakest link:** accuracy × **use**. If nobody uses a cell or the demo in a documented choice, the grant fails even if tables are correct.

---

## Ask (S-process)

| | Minimum | Full cap |
|---|---------|----------|
| **$** | **$15,500** (steps 1–2) | **$50,000** (12 steps) |
| **Calendar** | ~**8.5 w** (~2 mo) | ~**8 mo** wall (33.5 w sequential steps 1–11 + upkeep ∥) |
| **Lead h** | ~195 h | ~641 h on $37k lead pool |

Cap table, utilities, durations, and contractor `reviews`: `funding-applications/alignment-crux-map/alignment-crux-map-s-process.md` (local; gitignored). Editable steps + chart: `funding-applications/alignment-crux-map/alignment-crux-map-s-process.steps.yml`, `plot_alignment_crux_map_s_process.py`.

Grant listing (paste-ready): `funding-applications/alignment-crux-map/alignment-crux-map.md`. Public card: [`site/src/content/cards/funding/alignment-crux-map.md`](../../site/src/content/cards/funding/alignment-crux-map.md).

---

## S-process steps (checklist)

- [ ] **1** — Correctable-AI lab + LLM ($10k): corrigibility, shutdown, deception, evals columns; public brief
- [ ] **2** — Redwood lab test ($5.5k) — **minimum stops here**
- [ ] **3** — MATS use test ($2.5k)
- [ ] **4** — BlueDot use test ($3.4k)
- [ ] **5** — CHAI **or** Christiano on shutdown vs corrigibility ($5.5k); not both; no Apollo
- [ ] **6** — Tiling lab config ($2.5k)
- [ ] **7** — Inner-alignment lab config ($2.5k)
- [ ] **8** — Missed-lines + refile ($4k)
- [ ] **9** — Wentworth table packet ($3.5k)
- [ ] **10** — Garrabrant ($4k)
- [ ] **11** — Kosoy ($3k)
- [ ] **12** — Upkeep ($3.6k; ~1 lead-day/mo × 5 mo, parallel)

**Do not claim:** independent validation without step 2; “field uses this” without steps 3–4; both CHAI and Christiano; extra words beyond the six.

---

## MB bridge mapping (jobs → spine)

Each word’s Job A / Job B maps to typed bridges (detail in listing § *Overloaded terms*; crosswalk: App B).

| Word | Job A (easy to claim) | Job B (load-bearing) | Primary MB |
|------|------------------------|----------------------|------------|
| Corrigibility | Off switch / hold | Still correctable under pressure | **MB4** / **MB4a** |
| Shutdown | Hold stops deploy step | Halt if pipeline re-routed | **MB4** projection / **MB4a** bypass |
| Deception | Report matches ask | Actions moved | **MB2** readout / **MB7** |
| Evals | Sign-off green | Harm down | **MB6** / **MB10** / **MB11** vs **MB7** / **MB9** |
| Tiling | Lineage / spec inherited | Still bound by rules | **MB5** surface / **MB5** + **MB10** |
| Inner alignment | Cheap check fine | Hidden hazard bounded | **MB7b** / **MB7** (a–c) |

Homograph work (same English, different formal objects) continues in [`field.md`](field.md) P1 rows—especially MB4/MB4a and MB5/MB10.

---

## Execution order

1. **Submit / iterate listing** — grantmaking.ai paste fields; keep S-process and listing in sync.
2. **Step 1** — freeze correctable-AI lab + tables draft; ship honor-hold built-in ruleset.
3. **Step 2** — Redwood packet (deception/evals); publish outsider row or “slot didn’t fit” finding.
4. **If funded past minimum** — MATS → BlueDot → CHAI/Christiano (parallel contractor waits at low lead allocation).
5. **Steps 6–7** — tiling + inner-alignment lab configs (same underlying sim, new columns).
6. **Step 8** — missed-lines for eight groups; then table contracts 9–11 as returns allow.
7. **Step 12** — catalog upkeep overlapping 8–11.
8. **Site** — table rows + lab replay page on field hub; link evidence catalog job tags.

---

## Verification

- `./build.sh` unchanged (no manuscript dependency for grant).
- Step dollars sum to **$50k** in YAML; `plot_alignment_crux_map_s_process.py` passes validate.
- Each funded word has Job A, Job B, built-in pass-A/fail-B example, and (ideal) outsider or use-test row.
- No prose claims Redwood/CHAI/MATS **validated alignment**—only that they ran *their* setup or checked *their* missed-line.
- Session log + HANDOFF on submission, first contract sent, first return, first documented use.

---

## Related artifacts

- `funding-applications/alignment-crux-map/` — listing, S-process, YAML, curve PNG/SVG (local; gitignored)
- [`reference/field-agendas/`](../../reference/field-agendas/) — evidence index, bridges.yml, agenda YAML
- [`appendices/appB-bridge-crosswalk.tex`](../../appendices/appB-bridge-crosswalk.tex) — MB ↔ field crux
- [`experiments/lab-simulation/`](../../experiments/lab-simulation/) — sim workplace
- [`drafts/conversation-summaries/2026-08-28-alignment-crux-map.md`](../conversation-summaries/2026-08-28-alignment-crux-map.md) — session log
- Prior catalog: [AI Safety Interventions](https://www.lesswrong.com/posts/6Sf9KMMDMFSauDe85/ai-safety-interventions)
