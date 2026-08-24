# Reward vs learned optimization target

- **Date:** 2022-07-25
- **Field:** LessWrong
- **Source:** https://www.lesswrong.com/posts/pdaGN6pQyQarFHXF4/reward-is-not-the-optimization-target
- **Source read:** full
- **TSA files consulted:** `chapters/ch21-reward-to-bundle-inference.tex`, `appendices/appB-bridge-crosswalk.tex`
- **Keywords grepped:** optimization target, reward is not, inner alignment, mesa-optim, training signal, wirehead, reinforcement, shard

## Source ontology

Turner splits “reward” into two objects. The training-time scalar is a **cognition-updater** (reinforcement schedule): it upweights computations that preceded the signal. The trained policy’s **optimization target**, if any, is whatever those computations later steer toward — typically task correlates, not the button. Reward is therefore not a utility function over outcomes, and “we select on reward ⇒ we get a reward optimizer” is locally invalid (evolution/IGF is the analogy). Wireheading and “find a safe outer objective to maximize” inherit the discarded type.

## TSA coverage

- **Status:** already-in-TSA
- **Closest TSA terms/chapters:** reward as evidence / not the optimization target (ch21); value bundle vs scalar \(R\) (ch15–ch17, ch21); shard theory as borderline sibling (App B MB2/MB3; ch21 keeps shard mechanics out of the inference target); inner alignment / mesa-optimization still used as MB7 without this type-split (App B).
- **Overlap:** Ch21 §“Reward as Evidence, Not the Optimization Target” cites this post (`turner2022rewardnotopt`) and restates the schedule-vs-target cut. TSA then uses it as a premise for a further move: IRL/RLHF/CIRL language is kept as a partial question, but the object to infer and preserve is \((B,W,\Phi)\), not scalar \(R\) or the programmer’s ground-truth signal. A footnote already records Turner’s later hedge that pretrained models have a “reward” concept and may seek the signal after all.
- **Gap:** Nothing load-bearing is missing. App B names shard theory, not this type-claim; field inner/outer talk (MB7 row) can still read as if the base objective were the trained agent’s target. Turner’s research implication — stop searching for outer objectives, grow inner cognition — is refused, not underspecified: ch21 keeps outer bundle inference and puts internals out of scope.

## Applicability to TSA

- **Score (0–5):** 2
- **Why:** The primitive is already a named section and bib key; deleting it from TSA would require rewriting ch21’s opening ontology. Remaining purchase is cartographic: App B currently folds “reward chisels cognition” into the shard-theory sibling line, which invites mixing this 2022 type-split with the later mechanistic program (2022-09-04 on the parent list). A one-line MB2 note would keep the type-claim visible where inner-alignment vocabulary is still used.
- **Ontology-stickiness risk:** High in the field, low as a TSA hole. Pre-2022 RL textbooks and Hubinger inner/outer framing treat reward as that-which-is-optimized; models trained on that corpus will regenerate “the agent wants the reward.” TSA already includes and renames the split (evidence channel, not target). The live failure mode is re-importing the old type through MB7 / “outer objective” prose, not failing to see the primitive.
- **Recommended action:** cite-in-crosswalk

## One-line finding

TSA already has Turner’s schedule-vs-target split in ch21; cite it in App B as a type-claim distinct from shard mechanics so inner-alignment language does not collapse it back into reward-as-what-the-agent-wants.
