---
external:
  - label: Moon & Varshney, Containment Verification (arXiv:2605.09045)
    url: https://arxiv.org/abs/2605.09045
  - label: HTML (v2)
    url: https://arxiv.org/html/2605.09045v2
  - label: davidad / Guaranteed-Safe AI
    url: /cards/agenda/davidad-guaranteed-safe-ai-gsai/
  - label: Safeguarded AI (ARIA / Zeroth / Heron)
    url: /cards/agenda/safeguarded-ai-aria-zeroth-heron/
  - label: What this map misses
    url: /cards/concept/what-tsa-fails-to-represent/
  - label: Victor Taelin, “you can’t win the game” (X)
    url: https://x.com/Gunnar_Zarncke/status/2097972549665571077
  - label: Winning Is A Bug law (demo writeup)
    url: https://bend2.dev/notes/what-is-bend2/
related:
  - field-agendas/davidad-guaranteed-safe-ai-gsai
  - field-agendas/safeguarded-ai-aria-zeroth-heron
  - what-tsa-fails-to-represent
---

<p class="src-legend" role="note">
  <span class="src-legend-item src-legend-item--openai"><span class="src-legend-swatch" aria-hidden="true"></span>Moon &amp; Varshney (blue)</span>
  <span class="src-legend-item src-legend-item--tsa"><span class="src-legend-swatch" aria-hidden="true"></span>this book (black)</span>
</p>

**If you remember one thing:** a machine-checked gate can say that some *named* actions do not leave the runtime. That is not a statement about the unbounded world those actions can still reach.

On 10 September 2026 I joined Orpheus Lummis's GSAI sequence for Royce Moon presenting [Containment Verification](https://arxiv.org/abs/2605.09045) (with Lav R. Varshney; v2 June 2026). The paper is already on this project's [Safeguarded AI](/cards/agenda/safeguarded-ai-aria-zeroth-heron/) roster. The call was useful because it made the residual sharp: the interesting directions are expressible in a spec, and they are not what the published examples prove.

## Progress

They locate the guarantee in the agentic framework, not in the model. The AI is treated as an unconstrained oracle over a typed action set. Whatever it emits, the verified layer must only produce in-policy boundary events.

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://arxiv.org/abs/2605.09045">Moon &amp; Varshney</a> · abstract</p>
<p>The guarantee is independent of alignment because it quantifies over the framework’s typed action boundary rather than over model behavior.</p>
</blockquote>

That is real progress on a [GSAI](/cards/agenda/davidad-guaranteed-safe-ai-gsai/) bottleneck: you can deductively check the *pipe*, in Dafny, and compile it. To their knowledge this is the first such check of an agentic framework. They are explicit that truthfulness, deception, and persuasion are out of scope. A verified containment layer is not a complete safety solution.

The published instantiation is PocketFlow, a minimal graph runtime, on two small workflows (a file reader and a retrieval flow). The policy they prove is:

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://arxiv.org/html/2605.09045v2">Moon &amp; Varshney</a> · §4.1</p>
<p>Read events are permitted only for paths under the configured workspace root, tool-call events only for allowlisted tools, and step events only while the loop bound has not been exceeded.</p>
</blockquote>

On those examples this is verifying a whitelist, plus a proof that dispatch cannot skip it *inside the model*. The logic of their predicate can mention state, so it is potentially more expressive than set membership. In the artifact, that state is still the runtime’s own registers: paths logged, tool names, a step counter. LangChain and other production frameworks are named, not verified.

## Difficulty

A whitelist on a tiny enum is the easy case. They say so.

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://arxiv.org/html/2605.09045v2">Moon &amp; Varshney</a> · §5</p>
<p>A containment layer that exposes a narrow typed enum yields a strong guarantee, one that exposes a generic shell or eval primitive collapses the guarantee onto the primitive.</p>
</blockquote>

The guarantee also needs every real effect to pass through that enum. If a human clicks Approve, if a tool argument is itself an interpreter, if an allowed tool writes the world in a way the spec never named, the proof does not speak. Their own ablation already shows a related hole: a spec can verify, pass their gates, and still be vacuously true of the actual privileged effect.

<blockquote class="src-quote src-quote--openai">
<p class="src-quote-attr"><a href="https://arxiv.org/html/2605.09045v2">Moon &amp; Varshney</a> · §3.5</p>
<p>A deployed safety failure can therefore arise from three sources. […] Finally, failure can arise from a property-completeness gap where Π<sub>I</sub> does not capture the intended safety policy.</p>
</blockquote>

This book’s first chapter is the same cut from the other side. A language model with tools may include a browser, a scratchpad, credentials, and a human who clicks approve. The named runtime is not automatically the loop.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch01/">this book</a> · Ch. 1</p>
<p>Physical containment is evidence. It is not decisive.</p>
</blockquote>

## What the call marked as interesting

In the room, the live directions were not “is the whitelist formally verified.” They were treated as generally interesting and as things a spec could, in principle, say:

It would be interesting if actions were not just filtered, but constrained by how they affect external state. For example, how many actions may access a file. It would also be interesting to bound the effect: how many bytes are written, how many systems are accessed. Types of *sequences* of actions are often the problem. Small innocent actions can compose into harm. That is specification work. It needs a model of the world the actions touch, not only an allowlist of names.

Those are the first steps from a framework policy toward a GSAI safety specification: the predicate has to constrain states of the *world* affected by the actions.

[Victor Taelin’s Bend demo](https://x.com/Gunnar_Zarncke/status/2097972549665571077) is that shape, on a closed game. One rule: you cannot win. You prompt an AI to change the mechanics and try to reach the flag. Jailbreaks do not matter. A commit is accepted only with a proof that the flag is untouchable, so the funny repairs happen instead: the wall moves to the other side, walls become two tiles thick, WASD moves the flag. The AI never implements a game where you can step on the flag, because that would be a failed proof, not a failed preference.

That is closer to the call’s request than PocketFlow’s whitelist. The law is about *sequences* on a modeled state: no finite action list from the start position yields a win ([writeup](https://bend2.dev/notes/what-is-bend2/)). It is still a finite map. The same writeup notes that the law constrains those transitions; it does not verify the renderer or the compiler. Taelin’s further hope, that the same method will soon block hacks, launched nukes, or designed bioweapons, is the step that leaves the envelope. Those are not a flag on a grid.

## Outlook

If we could make statements about what cannot happen in the world, in the sense of actions, that would be the useful object. If those actions reach the unbounded real world, there are no guarantees we can make.

That is not a dismissal of their lemma. It is the same bound this book already puts on certification.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch33/">this book</a> · Ch. 33</p>
<p>A guarantee over arbitrary superintelligence is almost vacuous unless it is a guarantee of containment by external force. But if the system is already superintelligent in the relevant sense, external force is itself one of the things under contest.</p>
</blockquote>

A useful guarantee is always relative to a certified class of systems, an environment, a monitoring regime, and the transformations still allowed. The risk number is not the load-bearing part.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch33/">this book</a> · Ch. 33</p>
<p>Without those restrictions, the statement is not a safety claim. It is a wish.</p>
</blockquote>

A closed action alphabet can support a universal claim: no modeled event outside the policy. An open world does not support a weaker version of the same claim. It supports a different act: refuse, halt, or recertify under a new envelope. [What this map misses](/cards/concept/what-tsa-fails-to-represent/) already says the matching thing about this cluster: a green certificate on a declared cut is not live safety, and the named unit may not be the real loop.

## Needed work

The paper’s own next engineering test is production frameworks with wider interfaces. That is necessary and not sufficient.

What still has to be written, if this is to sit in a GSAI stack rather than only in a framework audit:

1. A predicate whose state is a variable the action *changes in the world*, not a register in the runtime.
2. Bounds and trace properties (bytes, systems, sequences), not only membership in an allowlist.
3. An exclusive cut: every effect that can matter is in the model, including humans and tool arguments, or the claim is labelled as not covering them.
4. A story for widening the enum later without the update path becoming an unmodeled effect.

This book does not construct those proofs. It names what they would have to be about: boundary closure, correction integrity, successor invariants. GSAI is the external program for turning those targets into proofs rather than dashboards.

<blockquote class="src-quote src-quote--tsa">
<p class="src-quote-attr"><a href="/cards/chapter/ch43/">this book</a> · Ch. 43</p>
<p>The practical statement is therefore: this book supplies the target properties, failure separations, and bridge conditions that any deployment-grade proof or safety case must discharge.</p>
</blockquote>

Containment verification is a container-level lemma for a declared action alphabet. Use it that way. Do not read the title as “alignment is unnecessary.” The authors do not claim that. Alignment, correction, and selection start where the alphabet no longer contains the effects.
