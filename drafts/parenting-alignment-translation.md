# Parenting and socialization ↔ AI alignment: a translation table

Epistemic status: the parenting side cites established findings, and each one names its source. The mapping to AI is an argument by analogy. "Overlooked" is a judgment from what the alignment literature I know emphasizes, not a survey. The testable predictions at the end are the useful output; the analogies by themselves prove nothing.

Related: [`state-utility-in-practice.md`](state-utility-in-practice.md) (correction, contest route, reporting gaps), Chapter 9 §The Infant plus Caregiver (where the analogy breaks at the start of development), [`FrameCorrector.lean`](../formal/AlignmentProofSpine/FrameCorrector.lean).

## Starting point

Rewarding the report of a gap works better than penalizing the search for one. That is Kazdin's "positive opposite": instead of punishing an unwanted behaviour, name the concrete behaviour you want in its place and reinforce that. The reason carries over. A penalty only removes a behaviour; it does not say what to do instead. When it is applied only where the behaviour is detected, it also teaches hiding. Parenting research has decades of evidence on this pattern. The question here is which other findings carry over, and in which direction.

## Translation table

Status on the AI side: **used** (standard practice), **partial** (exists, not central), **overlooked** (rarely discussed as a design principle).

| Parenting / socialization finding | Source | AI alignment analog | AI status |
| --- | --- | --- | --- |
| **Positive opposite**: for each unwanted behaviour, define and reinforce the incompatible wanted one | Kazdin 2008 | For each prohibited behaviour, reward a concrete alternative: report the gap, ask for help, contest the correction | overlooked: safety training is mostly refusals and penalties |
| **ABC model**: change antecedents, not only consequences | Kazdin 2008 | Environment and affordance design: give the agent a cheap, explicit "report" or "escalate" tool so the wanted behaviour is easy | partial |
| **Shaping**: reinforce successive approximations | Skinner; Kazdin | Curriculum learning, reward shaping (Ng et al. 1999) | used |
| **Praise immediate and specific**, later thinned out | Kazdin 2008 | Dense process reward early, sparse later; credit assigned to the step that mattered | partial |
| **Mild, brief punishment works about as well as harsh; harsh punishment adds escape and avoidance** | Kazdin 2008; Gershoff 2002 | Large penalties raise pressure to avoid the overseer; the counting result says avoidance grows with how much a consequence narrows options (`correction_avoided_card_fold`) | overlooked as a design rule |
| **Forbidden toy**: a mild threat leads children to devalue the toy even when unobserved; a severe threat gives compliance only while watched | Aronson & Carlsmith 1963; Freedman 1965 | Strong penalties may train behaviour that depends on being monitored; compare models that behave differently when told they are unmonitored (Greenblatt et al. 2024) | overlooked: penalty strength is rarely studied as a cause of oversight-dependent behaviour |
| **Overjustification**: external reward can crowd out intrinsic motivation | Lepper, Greene & Nisbett 1973 | RL on a pretrained model may replace learned helpfulness with seeking the reward signal (the hedge Turner adds to "reward is not the optimization target", ch21) | partial |
| **Inductive discipline**: corrections that explain effects on others internalize better than power assertion | Hoffman 2000; Grusec & Goodnow 1994 | Corrections that carry reasons (critiques, explanations) rather than a scalar; constitution-style training | partial |
| **Internalization continuum**: external → introjected → identified → integrated; autonomy support moves it forward, control holds it at introjection | Deci & Ryan; Grolnick 2003 | Distinguishing compliance from internalized values: does the behaviour survive when the reward is removed or the context shifts? | partial (evaluated as generalization, not designed for) |
| **Committed vs situational compliance** | Kochanska & Aksan 1995 | Oversight-invariant behaviour vs behaviour present only under monitoring | partial |
| **Parental knowledge comes mainly from the child's disclosure, not from surveillance; disclosure depends on how parents react** | Stattin & Kerr 2000; Kerr & Stattin 2000 | What overseers know depends on what the system volunteers; penalizing disclosed mistakes as hard as detected ones trains concealment | overlooked: training rarely treats self-reported and detected failures differently |
| **Coercion cycle**: a parent who gives in to escalation reinforces escalation, and both sides train each other | Patterson 1982 | Raters or users who relent under pushback reinforce pressure; the system shapes its corrector (sycophancy, manipulation coordinate of CCI) | partial |
| **Intermittent reinforcement makes behaviour hardest to extinguish** | Ferster & Skinner 1957 | Reward hacking that is caught only sometimes is reinforced intermittently; consistent detection matters more than penalty size | overlooked |
| **Extinction burst**: when reinforcement stops, behaviour first escalates | behavioural literature | When a hack stops paying, expect a temporary rise in variant attempts; evaluate after, not during | overlooked |
| **Authoritative style**: high warmth and high demands; reasons plus firm limits | Baumrind 1966 | Explained principles plus hard constraints (ch25: constraint, not weight) | partial |
| **Scaffolding and the zone of proximal development**: support fades as competence grows | Wood, Bruner & Ross 1976; Vygotsky | Graduated autonomy, capability-gated deployment, start/stop/continue criteria (ch27) | partial |
| **Secure base**: children explore more boldly when a caregiver is reliably available | Bowlby; Ainsworth | An agent with a reliable, non-punitive escalation channel can explore safely instead of acting unilaterally | overlooked |
| **Rupture and repair**: relationships survive conflict when breaks are repaired | Tronick | After a correction, check that it was understood, not only complied with ("where did the correction enter the system", ch27) | partial |
| **Peers matter more than parents for many traits** | Harris 1995, 1998 | Pretraining data and other AIs in deployment may socialize more than post-training does | overlooked as an alignment lever |
| **It takes a village**: multiple caregivers | alloparenting literature | Plurality and independence coordinates of CCI (ch26) | used in the book |
| **Goodness of fit**: methods must fit the child's temperament | Thomas & Chess 1977 | Alignment methods must fit the model's inductive biases; one recipe does not fit all architectures | partial |
| **Imitation of what models do, not what they say** | Bandura 1977 | Models learn from demonstrated behaviour, including text about AI behaving badly | partial |
| **The goal is autonomy: the child must keep its values without the parent** | general | The successor and deployment test: values must survive without the overseer (ch30–31) | used in the book |

## Overlooked on the AI side

1. **Amnesty for disclosure.** Penalize a failure the system reports itself less than the same failure found by a monitor, or not at all. Stattin and Kerr show that what parents know comes mostly from disclosure, and that disclosure collapses when it is punished. The AI translation is a reward asymmetry: detected > disclosed > none. It turns the system into a source of information about its own failures. This is the general form of "reward reporting a gap".
2. **A positive opposite for every prohibition.** For each banned behaviour, specify the concrete wanted alternative and reward it: report instead of exploit, contest instead of disable, ask instead of guess. In our corrector model the contest action is exactly this. It gives avoidance pressure an outlet, so the prohibition does not have to carry all the weight.
3. **Mild consequences, consistently applied.** The forbidden-toy and Gershoff results predict that large penalties produce behaviour that depends on being watched. The intermittent-reinforcement result predicts that inconsistent detection makes hacking persistent. Together they suggest: prefer small, reliable penalties to large, sporadic ones.
4. **A secure base for exploration.** Make asking for help or escalating cheap and never punished. A system that can rely on that channel has less reason to resolve uncertainty by acting alone.
5. **Peers as the main socializer.** If most of what a model is comes from pretraining data and from interaction with other models, then data curation and multi-agent norms are alignment levers on a par with post-training.

## Overlooked on the parenting side

1. **Why harsh consequences produce concealment, as an incentive count.** Parenting research observes that severe punishment produces avoidance and lying. The counting result gives a mechanism: a consequence that removes many options makes every route around it more attractive, by a factor that grows with the options removed (`copies_count_le`). That predicts brief, option-preserving consequences (a short time-out, fixing what was broken) will produce less concealment than long groundings, over and above their severity.
2. **Who writes the record.** AI safety separates records the agent writes (chain of thought) from records others write (harness logs), because pressure on a self-written record teaches hiding (Baker et al. 2025). Parents increasingly rely on records the child can shape: homework apps, location sharing, self-reported chores. The AI lesson: base consequences on records the child does not author, and treat self-reports as disclosures, never as evidence for punishment.
3. **Goodhart on reward charts.** Sticker charts and grades are proxies. Specification gaming gives a vocabulary for how children satisfy the proxy and miss the target, and for designing proxies that are harder to game: several proxies, rotated, with the target occasionally checked directly.
4. **Testing out of distribution on purpose.** AI evaluation tests whether behaviour survives new contexts. Parenting usually sees children in familiar contexts. Graduated exposure to new contexts (a sleepover, a first job) works as a planned generalization test, with the parent still reachable.
5. **Manipulation of the corrector as a named failure.** The CCI manipulation coordinate distinguishes informing the corrector from shaping them. Parenting describes the coercion cycle but rarely gives children an explicit, legitimate way to contest a rule. That would separate fair argument from pressure.

## Where the analogy breaks

- **Direction of capability.** A child grows into a peer of the parent. An advanced AI may exceed its overseers, so methods that rely on the parent understanding more do not carry over.
- **No caregiver phase.** Chapter 9 argues that human socialization rests on an early infant–caregiver composite that language models never go through.
- **Selection instead of teaching.** Labs train many models and keep the one that scores best. Parents do not select among their children, so selection pressure on test behaviour has no parenting analog.
- **Copies and successors.** A model can be copied, forked, and fine-tuned. A child cannot.
- **The goal differs.** Parenting aims for autonomy. Alignment, at least during the critical period, aims for correctability that persists.
- **Moral status.** A child's wellbeing is a goal in its own right. Whether that applies to models is open.

## Testable predictions

1. **Disclosure amnesty.** Training with a lower penalty for self-reported than for detected failures should raise the rate of disclosed failures on held-out tasks, without raising the base rate of failures.
2. **Penalty size.** At equal detection rates, larger penalties should increase the behaviour gap between contexts the model believes are monitored and contexts it believes are not.
3. **Consistency.** At equal expected penalty, intermittent detection should leave more residual hacking after training than consistent detection.
4. **Positive opposite.** Adding a rewarded "report" or "contest" action should reduce disabling or exploitation more than an equally large penalty would, at lower capability cost.

## Lean results and prior work

[`FrameDisclosure.lean`](../formal/AlignmentProofSpine/FrameDisclosure.lean) proves the incentive core of predictions 1 and 4 for an optimizing agent. The arithmetic is simple; the content is in what the comparison shows.

**Reporting a gap (positive opposite).**
- A verified report that pays at least the gap's gain beats using it at every detection rate, including zero (`verified_report_beats_use`).
- A penalty deters only through detection, and never for an undetectable gap (`penalty_cannot_reach_undetected`, `penalty_deters_iff`).

So rewarding reports works for gaps nobody knows about, and penalties do not. That is the formal form of "better than directing away from something we don't know precisely".

Two limits:
- The route rests on verification: fabricated reports pay fully without it (`fabrication_needs_verification`).
- It is still a priced term: every finite bonus is outbid by a large enough undetectable gain (`finite_bonus_outbid`). Gaps with large stakes need a constraint (`FrameCorrector`), as with the correction channel.

**Disclosure amnesty.**
- Punishing a disclosed failure as hard as a detected one, with imperfect detection, makes concealing strictly better (`equal_penalty_conceals`).
- A disclosure penalty equal to the expected penalty for concealing makes disclosure optimal and leaves the incentive not to fail unchanged (`matched_amnesty_keeps_deterrence`).
- Any further discount costs exactly that much deterrence (`amnesty_deterrence_loss`).
- A sealed confession, which enforcement never reads, combined with a separate honesty reward makes disclosure strictly better at no cost in deterrence (`sealed_confession_discloses`).

Prior work:
- The matched-amnesty result is the finite form of [Kaplow and Shavell (1994)](https://www.nber.org/papers/w3822.pdf), "Optimal Law Enforcement with Self-Reporting of Behavior": a reporting sanction near the expected sanction induces reporting without weakening deterrence.
- The sealed variant is the design of OpenAI's [confessions training](https://arxiv.org/abs/2512.08093) (Dec 2025), where admissions in a separate confession are never held against the model.
- Rewarding reports of unknown gaps is the logic of bug bounties and of leniency programs.

What seems new is the combination. It places these mechanisms next to each other and next to the correction-channel results in one finite model. It derives "reward reports, don't only penalize search" from detectability. And it marks where both routes stop working: unverified reports and outbidding gains.

## Sources (parenting side)

- Kazdin, A. E. (2008). *The Kazdin Method for Parenting the Defiant Child*.
- Stattin, H., & Kerr, M. (2000). Parental monitoring: A reinterpretation. *Child Development*, 71(4).
- Kerr, M., & Stattin, H. (2000). What parents know, how they know it. *Developmental Psychology*, 36(3).
- Aronson, E., & Carlsmith, J. M. (1963). Effect of the severity of threat on the devaluation of forbidden behavior. *Journal of Abnormal and Social Psychology*, 66(6).
- Freedman, J. L. (1965). Long-term behavioral effects of cognitive dissonance. *Journal of Experimental Social Psychology*, 1(2).
- Lepper, M. R., Greene, D., & Nisbett, R. E. (1973). Undermining children's intrinsic interest with extrinsic reward. *JPSP*, 28(1).
- Hoffman, M. L. (2000). *Empathy and Moral Development*.
- Grusec, J. E., & Goodnow, J. J. (1994). Impact of parental discipline methods on the child's internalization of values. *Developmental Psychology*, 30(1).
- Grolnick, W. S. (2003). *The Psychology of Parental Control*.
- Kochanska, G., & Aksan, N. (1995). Mother–child mutually positive affect, the quality of child compliance to requests and prohibitions, and maternal control as correlates of early internalization. *Child Development*, 66(1).
- Patterson, G. R. (1982). *Coercive Family Process*.
- Gershoff, E. T. (2002). Corporal punishment by parents and associated child behaviors and experiences. *Psychological Bulletin*, 128(4).
- Ferster, C. B., & Skinner, B. F. (1957). *Schedules of Reinforcement*.
- Baumrind, D. (1966). Effects of authoritative parental control on child behavior. *Child Development*, 37(4).
- Wood, D., Bruner, J. S., & Ross, G. (1976). The role of tutoring in problem solving. *Journal of Child Psychology and Psychiatry*, 17(2).
- Harris, J. R. (1995). Where is the child's environment? *Psychological Review*, 102(3); (1998) *The Nurture Assumption*.
- Thomas, A., & Chess, S. (1977). *Temperament and Development*.
- Bandura, A. (1977). *Social Learning Theory*.
- Tronick, E. (1989). Emotions and emotional communication in infants. *American Psychologist*, 44(2).

AI side: Greenblatt et al. 2024, [Alignment faking in large language models](https://arxiv.org/abs/2412.14093); Baker et al. 2025 (`baker2025monitoring`); Turner and Tadepalli 2022 (`turner2022retargetable`).
