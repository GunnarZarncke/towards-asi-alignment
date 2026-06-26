# Chapter 17 — LHV Learnability Toy

Deterministic synthetic experiment for the learnability/identifiability split in
`chapters/ch17-low-dimensional-value-learning.tex`.

The toy plants six latent hub coordinates inside a 64-dimensional scenario
embedding. Binary judgments are generated from nonlinear hub interactions. The
demo then:

- recovers the embedding dimension count with PCA plus parallel analysis;
- compares held-out prediction from raw embeddings, recovered hub coordinates,
  and oracle hub coordinates;
- reports the weak information lower bound implied by the final held-out
  accuracy.

This is not empirical evidence about human values. It only illustrates the
experimental pattern: low-dimensional hub structure can be recoverable and
predictive in a sample window where arbitrary ambient rewards are under-sampled.
