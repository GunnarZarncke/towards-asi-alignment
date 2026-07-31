# 2026-07-09 — Byrnes social-drive integration for ch15

## Trigger

User asked to resume after three Sonnet subagents launched for a deeper mapping
of Steven Byrnes's human-like social-drives material appeared to hang. The
subagent transcripts showed all three had actually failed on a monthly usage
limit before returning reports, so the research pass continued directly in the
main session.

## Done

- Recovered and read the core Byrnes materials directly via LessWrong markdown:
  the 2024 social-instincts sketch, 2025 Sympathy Reward and Approval Reward
  posts, act-based approval-directed agents, perils of under- vs over-sculpting
  AGI desires, empowerment/corrigibility ontology, and the "alignment-is-hard"
  Approval Reward post.
- Added `chapters/ch15-values-compressed-control.tex`
  `\subsection{A More Structured Social-Drive Proposal}` after the LHCV model.
  The section frames Byrnes as a finer mechanism inside the \(H\to C\) layer:
  conspecific detection, short-term predictors, attention/learning-rate gates,
  transient empathetic simulation, the friend/enemy bit, and the
  "other is thinking about me" bit.
- The new ch15 text distinguishes Sympathy Reward from Approval Reward and
  maps their distinct failure modes: bearer-map errors, dehumanization,
  anthropomorphization, motivated avoidance, hedonic rescue, sycophancy,
  status games, shallow norm-following, and imagined-evaluator failure.
- Added five Byrnes bibliography entries to `references/neuroscience-values.bib`
  plus matching `\bibsummary` lines in
  `references/bibliography-summaries.tex`.
- Verified `python3 scripts/check_bibliography_summaries.py` passes
  (`410 summaries for 410 bib keys`) and no linter diagnostics were reported
  for the touched files.
- Ran `make check`: structure check, citation check, and bibliography-summary
  check all passed.

## Decisions

- Treat Byrnes's social-drive account as complementary to LHCV, not competing
  with it. LHCV remains the coarse hub/control abstraction; Byrnes adds a
  candidate internal social-circuit generator.
- Kept the claim strength explicitly empirical/speculative. The formal spine
  maps ch15 to `AlignmentProofSpine/Bundles.lean`, but the Lean README says
  empirical value-bundle content is not formalized; this edit does not claim a
  proof.
- Did not add a separate appB/ch44 note in this pass. The immediate gap was in
  ch15's biological generator story; strategic/pivotal-process implications
  can be added later if the user wants a wider Byrnes integration.

## Open / next

- Consider a later `appendices/appB-bridge-crosswalk.tex` note tying Byrnes's
  single-model reward-design problem to MB2/MB3/MB4 and the book's measurement
  tests.
- Consider a ch21/ch22 note on non-behaviorist rewards and under/over-sculpting
  if the single-model installation subproblem needs its own explicit treatment.
- Full PDF build was not run in this pass; `make check` and IDE lints passed.

## Key paths

- `chapters/ch15-values-compressed-control.tex`
- `references/neuroscience-values.bib`
- `references/bibliography-summaries.tex`
- `formal/README.md`
- `appendices/appB-bridge-crosswalk.tex` (possible follow-up)
- `chapters/ch21-reward-to-bundle-inference.tex` and
  `chapters/ch22-compression-test-intention.tex` (possible follow-up)

## Commits

- `52b0dbf` Integrate Byrnes social-drive distinctions into ch15.
