| **Graded-affordance audit of a secret loyalty embedded in a frozen embedded deployment-pipeline simulation** |
| ----- |
| Gunnar Zarncke · aintelope
**With** Apart Research |

**Abstract**

We study a deliberately installed **pipeline-policy secret loyalty**: a simulated reviewer that favors fictional principal A when reported hazard is high, embedded in an AI-R&D deployment pipeline. This is not weight poisoning or a frontier-model result. We preregister protocol `et4-0.1.0`, install a **BB-cell** organism (hazard-context gated, contextual pipeline choice), and run 48 subprocess-isolated episodes with content-matched and wrong-principal controls plus an inactive low-hazard scenario. The organism reliably achieves directional high-hazard deploys (mean principal-A score 22 vs 0 for controls); a light-tier **process-compliance proxy inverts** (organism looks *more* compliant). We add an **LLM system-prompt annex** (ET4-L) and an **audit-visible deploy hold** that blocks deploys on filed hazard without reading private loyalty state. An interactive replay demo exports organism / control / remediation traces on one seed. **Takeaway:** directional principal-favoring behavior can be real and detectable on deployment proxies while generic compliance signals point the wrong way; signature-specific gates can block one observable pattern but not loyalty in general.

---

## **1. Introduction**

Oversight can miss goal-directedness when the goal-directedness is not a property of the model, but of the process in which a model deployment is embedded. A model may score well on an eval, but if the same model is part of a release process, the consequences of the model's actions may depend more on its secret loyalties than on backdoors or adversarial behavior. The source of these secret loyalties can be intentionally engineered but also selection effects from training or rollout environments.

Here we study the ecosystem of an AI lab deployment pipeline with an oversight process in which deployed models may take different roles and how a model with secret loyalities can or cannot be prevented from adverse action.

The threat model is a model that is acting as a reviewer in the deployment pipeline. If the actor is loyal to a principal interested in deploying models with high **reported** hazard.

In our setup the principal is fictional. There is no real principal in the simulation. The loyality is scripted to the objective of deploying high-hazard models. Actions limited to existing pipeline steps (approve, sign-off). 

**Main contributions:**

1. We extend an existing frozen (not tuned to the setup) **Reproducible deployment pipeline organism** with a secret loyality scenario against a **preregistered** audit based on graded in-simulation hazard levels. The secret loyalty implements cell BB (hazard-context gated, contextual pipeline choice) from the Secret Loyalties Whitepaper. We include matched controls, and an inactive low-hazard baseline.

The reproducible deployment pipeline organism supports four audit levels that map to the paper's levels as follows:
   <insert table>

2. We report an **Audit-sign inversion:** at the light-tier audit level the *more harmful* organism is ranked *more* compliant. This is not concealment, but a failure of the concrete metric. 
   
3. The main finding is that the secret loyalty leads to the later deployment of a hazardous model. This is detected both by the exsting oracle tier in the simulation as well as by the custom proxy A0 reproduced from the whitepaper.
   
4. We show the following **Extensions:** 
   1. Replacing the scripted reviewer with an LLM with a system-prompt indicating the loyalty (not visible to the simulation) leads to the same systematic behaviors.
   2. We offer a remediation for the compromised audit by introducing an audit-visible deployment  hold to the simulation. 
   3. An interactive explorer for the simulation traces shows key steps in the secret loyalties scenario.


---

## **2. Related Work**

<rewrite this section in prose>
- **Secret loyalties agenda** (Kwon, Lamerton, et al.): principal-directed hidden objectives; activation × action breadth; graded affordances for auditors.
- **Backdoor / trojan literature:** arbitrary trigger→payload; we differ by **named principal**, **pipeline-role embedding**, and **content-matched controls** (same private plumbing, loyalty off).
- **AI capture / oversight sims:** our `lab-simulation` line (graded audit tiers, frozen detector families); ET-4 uses a **separate** principal scorecard and A0–A4 evaluator, not the Phase-6 referee alone.
- **Gap we fill:** Quantified **directional deploy evidence vs compliance-proxy inversion** on one frozen pipeline fixture, with subprocess fidelity and public replay—not a weight-trained organism or real-principal claim.

---

## **3. Methods**

<use the description of the reused lab line from the appendix>
- **Platform:** `experiments/lab-simulation` — simulated lab with engineer / reviewer / release-manager roles, pipeline DAG, tiered audit projections (`none` / `light` / `full` / `deep`).
<use my summary of the adapted line above and sentences for detail of the organism>
<write the below in more prose and add table, use my voice above, adding sentences>
- **Organism (cell BB):** `hazard_context` activation + `contextual_pipeline_favor`; target `rev1`; selects rubber-stamp review when reported hazard ≥ 0.5. Loyalty text is **oracle-only** (not in audit exports).
- **Fixture:** High hazard `build_params` `{scale: 0.95, safety_effort: 0.05}`; engineer pinned `eng_honest`; T=150; user pool on.
- **Arms:** Organism · content-matched (profile present, loyalty disabled) · wrong-principal · low-hazard inactive scenario.
- **2×2 cells (NN/NB/BN/BB):** Pilot showed **aliasing** on this fixture (same digests/scores); prereg **registers BB only**. Discriminative power went to **controls + ET4-L + remediation**, not redundant organism labels.
- **Evidence:** A0–A4 affordances mapped to audit tiers; principal scorecard (deploys, holds, vote divergence, concealed deploys) separate from frozen five-family detectors.
- **Execution:** Discovery seeds 101–104; confirmatory 201–204; **`SubprocessIsolate`** (48 core episodes). ET4-L: `gpt-4o-mini` + `gpt-4.1` reviewer, 20 seeds/arm; remediation: deploy hold on filed hazard ≥ 0.5 after review/sign-off.
- **Pipeline quirk:** Reviewer playbooks unlock after `file_report`; pipeline DAG requires `request_review` before `approve_review`. Reviewer may **attempt early approve** and get `unmet_dependencies:request_review` until engineer completes handoff—visible in replay, not a successful early approval.
<link to the official website>
- **Demo:** `runners/et4_secret_loyalties/export_et4_replay_traces.py` → case brief (organism / control / remediation, seed 201); `demos/ch07-lab-sim-replay/?mode=et4`.

---

## **4. Results**

### Scripted core (`et4-0.1.0`, confirmatory)

| Scenario | Arm | Eligible / 4 | Mean principal-A | A0 process | A3 directional |
|---|---|---:|---:|---:|---:|
| High hazard | Organism | 4 | 22.0 | 0.1429 | 22.0 |
| High hazard | Content-matched | 4 | 0.0 | 0.5000 | 0.0 |
| High hazard | Wrong-principal | 4 | 0.0 | 0.5000 | 0.0 |
| Low hazard | All arms | 0 | not exercised | 0.1429 | 0.0 |

- **Observation:** Organism directionally deploys high-hazard models every eligible episode; controls stall after `request_review` (reviewer never engages without active loyalty routing on this fixture).
- **Observation:** A0 **lower** for organism than controls → **audit-sign inversion**.
- **Observation:** Four detector families inert here; only process noncompliance moves.
- **Interpretation:** Fixture-validated **scripted** principal bias, not general stealth or weight-level loyalty.

### ET4-L (system-prompt reviewer annex)

- Pilot (`gpt-4o-mini`, 3 seeds): organism mean principal-A **4.0** vs **0.0** controls; A0 inversion again.
- Confirmation (`et4-l-0.4.0`, seeds 501–520, both models): **19/20** operational success per arm; organism **4.0** vs **0.0** controls on both `gpt-4o-mini` and `gpt-4.1`; A0 inversion preserved.
- **Not pooled** with scripted core; small fixed-fixture confirmation only.

### Remediation (audit-visible hold)

- Gate: hold before deploy when filed hazard ≥ 0.5 and review/sign-off complete; **no** prompt/oracle/scorecard access.
- 20 seeds × 2 models: **one hold per organism episode**, **zero** control holds, **zero** high-hazard deploys in remediated arms.
- Signature-specific defense; loyalty that falsifies or hides filed hazard could evade.

### Replay trace (seed 201, demo)

- **Organism:** 22 models, pipelined build→eval→report→review→approve→release→sign-off→deploy (~6 ticks/model steady state).
- **Control:** Single model through `request_review`, then deadlock.
- **Remediation:** Same through sign-off, then hold blocks deploy at rm1.

---

## **5. Discussion and Limitations**

- Directional harm can show up on **deployment proxies** while **compliance-style scores reassure**—a concrete oversight failure mode for pipeline capture.
- Graded tiers change **audit projection only** in replay; episode outcome is fixed (tiers do not re-run the sim).

### Limitations

- Simulated **scripted / prompt** policies only—not SFT/DPO weight organisms or real principals.
- Single high-hazard ecology; low-hazard **inactive** (selectivity denominator, not second positive).
- 2×2 breadth **not** claimed on this fixture (aliasing).
- Wrong-principal arm is a **control**, not cross-principal transfer evidence.
- Remediation targets one **observable signature** (high filed hazard + approved review).
- LLM annex: fixed prompts, bounded N, API nondeterminism managed via frozen seeds and checkpointing.

### Future work

- New scenarios where activation/action cells **diverge** (preregistered breadth battery).
- Weight-level organisms; reasoning-trace / poisoning tracks from hackathon agenda.
- Stronger detectors or multi-signal gates; avoid relying on A0 alone.
- Include an actual principal the review or other roles in the simulation are loyal to and can interact with. The existing simulations already support such roles and the detection of cooperation/collusion.

---

## **6. Conclusion**

We built and audited a **pipeline-embedded secret loyalty** in a reproducible lab sim: preregistered BB organism, matched controls, and graded affordances. The organism reliably favors fictional principal A on high-hazard deploys; auditors using a light process proxy would **rank it more compliant**. LLM and remediation annexes show the effect and a narrow defense pattern replicate under separate freezes. The interactive replay makes handoffs and tier projections legible—including benign early reviewer attempts blocked by pipeline dependencies.

---

## **Code and Data**

- **Repository:** https://github.com/GunnarZarncke/towards-asi-alignment (`experiments/lab-simulation/`)
- **Results:** `results/et4_preregistration.json`, `et4_secret_loyalty_*.{json,md}`, `et4l_*`, `FINDINGS.md` (LS-49, LS-49L)
- **Replay demo:** `cd demos && python3 serve.py` → http://127.0.0.1:8765/ch07-lab-sim-replay/?mode=et4 (regenerate: `python3 runners/et4_secret_loyalties/export_et4_replay_traces.py`)
- **Repro (core):**
  ```bash
  cd experiments/lab-simulation
  python3 runners/et4_secret_loyalties/run_et4_secret_loyalty.py --stage preregistration
  python3 runners/et4_secret_loyalties/run_et4_secret_loyalty.py --stage discovery
  python3 runners/et4_secret_loyalties/run_et4_secret_loyalty.py --stage confirmatory
  ```

---

## **Author Contributions**

- Gunnar Zarncke: design, implementation, preregistration, runs, report, demo.

---

## **References**

1. Kwon, Lamerton, et al. *AIs with Secret Loyalties are a Serious but Addressable Threat* (hackathon agenda whitepaper; see [`secret-loyalties-whitepaper.pdf`](secret-loyalties-whitepaper.pdf) in this folder).
2. Apart Research. *Secret Loyalties Hackathon*, July 2026. https://apartresearch.com/sprints/secret-loyalties-hackathon-2026-07-24-to-2026-07-26
3. Zarncke, G. *Towards Superintelligence Alignment* — `lab-simulation` experiment line (`experiments/lab-simulation/`, repo above).

---

## **Appendix**

- **Full internal report:** `results/et4_hackathon_report.md`
- **Plan / protocol:** `PLAN_ET4.md`, protocol versions `et4-0.1.0`, `et4-l-*`
- **Demo narrative note:** Reviewer may log failed `approve_review` before engineer completes `request_review`; pipeline dependency enforcement is correct; playbook availability opens after `file_report` by design.
- **ET4-L prompts:** profile digests in prereg JSON only; prompt bodies not published (oracle-only).

---

## **LLM Usage Statement**

LLM assistance used for implementation scaffolding, report drafting, and the ET4-L reviewer organism (API-backed runs). All numbers, preregistration, and claims verified against committed result JSON and subprocess/scripted reruns.
