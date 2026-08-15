# 2026-08-15 — UAD concept card

## Trigger
Create a companion-site concept card for Unsupervised Agent Discovery, linking to Boundary Discovery, the LessWrong post, and relevant experiment lines.

## Done
- Added `unsupervised-agent-discovery` to `metadata/concepts.yml` (concept roster + ch07/ch34/ch35 book links).
- Wrote body `metadata/concepts/bodies/unsupervised-agent-discovery.md` — Markov-blanket pipeline, MB1 tie-in, calibrated evidence notes (agency-detect, embedded ES-1, lab LS, graded-lab GL-51/76/88), experiment table, external links (LW, agency-detect, TechRxiv).
- Bidirectional `related` links on `boundary-discovery`, `inferential-coupling`, `mb1-boundary-estimator-soundness`.
- Ran `npm run sync:concepts` (+ bridges resync for mb1 related list).
- Generated card: `site/src/content/cards/unsupervised-agent-discovery.md` → `/cards/unsupervised-agent-discovery/`.

## Decisions
- Status `plausible` (matches boundary-discovery; negatives honored in evidenceNotes).
- Four experiment lines linked: agency-detect, embedded-simulation, lab-simulation, graded-lab-simulation (primary MB1/UAD stress lines per `metadata/experiments.yml`).

## Open / next
- Optional concept logo at `drafts/illustrations/concept-logos/unsupervised-agent-discovery.svg`.
- Standalone UAD / negative-results publish still on outreach TODO (`metadata/TODO.md`).

## Key paths
- `metadata/concepts/bodies/unsupervised-agent-discovery.md`
- `site/src/content/cards/unsupervised-agent-discovery.md`

## Unstaged (not this session — left in working tree)
- `README.md`, assorted unrelated drafts and untracked experiments/value-detect archives.

## Commits
- `eefb46f3` — UAD concept card + ch34 ecology/coevolution follow-up (shared commit).
