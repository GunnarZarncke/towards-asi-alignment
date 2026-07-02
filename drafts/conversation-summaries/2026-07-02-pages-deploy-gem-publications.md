# 2026-07-02 — Pages deploy fix, About publications, inferential-coupling gem

## Trigger
Continuation of the site-publication session: GitHub Pages deploys kept failing; user added publications and asked to promote the acausal-trade modeling to gem status.

## Done
- **GitHub Pages deploy debugging:** four consecutive `actions/deploy-pages` runs stalled in `deployment_queued` for the full 10-minute timeout despite a 2.5 MB artifact (build job always green). Interim attempts: Node 24 action stack (`checkout/setup-node/deploy-pages@v5`, `upload-pages-artifact@v5`), workflow-scope `pages`/`id-token` permissions, `configure-pages`, chmod'd artifact tree, `pages` concurrency group. None cleared the queue stall.
- **Deploy method switch (`db18093`):** replaced the Pages Deployment API with `peaceiris/actions-gh-pages@v4` — build pushes `site/dist/` to a `gh-pages` branch; workflow run succeeded in ~1 min and the branch exists. Documented in `site/README.md`.
- **About publications (`74a723b`):** added *Mistral Large 2 (123B) seems to exhibit alignment faking* (LW, co-author) and *Thou art rainbow* (LW); folded the LHCV v2 paper into a `sublinks` entry under the v1 Loop–Hub–Value paper; About template now renders `note` and `sublinks`.
- **Inferential-coupling gem (`e528e45`):** ch35 gem paragraph `sec:ch35-inferential-coupling-gem` (ICI score, meta-prior detector, P33 negative direction, MB7d no-field-analog; conjectural/open status stated in-text); Gem Map row in `REVIEWING_FOR_AGENTS.md`; site card `inferential-coupling.md` (status `open`, ICI formula, P33 Lean node, acausal-trade paper link) registered as part08 gem.
- **PDF on site:** nav/footer links pointed at GitHub Releases HTML (not viewable in-browser). Added `copy-book-pdf.mjs` + `fetch-book-pdf.mjs`; PDF copied to `site/public/` on build; CI fetches latest release asset on main deploy; all site links use `pdfHref()`. Removed stale orphan `dist/towards-superintelligence-alignment.pdf`; `clean.sh` clears it.

## Decisions
- Gem claim strength calibrated to chapter markers: the gem is the measurable object (ICI/detector/P33), not a solved detection problem; equilibrium and large-scale dynamics stay [Conjectural]/[Open].
- Deploy via branch push, not Deployment API — the API queue wedged repeatedly on this repo; branch publishing uses a different pipeline.
- Publication co-authorship noted as plain "co-author" (post lists seven authors, no affiliation asserted).

## Open / next
- **Manual step (user):** Settings → Pages → Source → Deploy from a branch → `gh-pages` / root. Then verify https://gunnarzarncke.github.io/towards-asi-alignment/ is live.
- **Push:** commits through this session not yet pushed after PDF commit.
- Unrelated dirty tree left alone: embedded-simulation code/results churn (separate session), `src/demos/ch09-uad-coalition-board/index.html`, six older untracked conversation logs, `dist/`, regenerated `book.bbl-SAVE-ERROR`.
- agency-detect PDF link audit on About page still pending (older open item).

## Key paths
- `.github/workflows/site.yml` — gh-pages branch deploy
- `chapters/ch35-multi-agent-strategic-coupling.tex` — gem paragraph
- `site/src/content/cards/inferential-coupling.md`, `site/src/data/part-gems.json`
- `site/scripts/copy-book-pdf.mjs`, `site/scripts/fetch-book-pdf.mjs`, `site/src/lib/site-urls.ts` (`pdfHref`)

## Commits
- `66f7019` — Fix GitHub Pages site build: install demo deps and use Node 24.
- `c1b1880` — Fix GitHub Pages deploy timeout: configure Pages and artifact permissions.
- `100bd6e` — Upgrade CI and package engines to Node 24 action stack.
- `4432606` — Harden GitHub Pages deploy against permission and queue stalls.
- `db18093` — Switch Pages deploy from Deployment API to gh-pages branch push.
- `74a723b` — Update About publications: two LessWrong posts, LHCV v2 as sublink.
- `e528e45` — Mark inferential-coupling detection as a gem in book and site.
- `5e0ffd3` — Host book PDF on the site for in-browser viewing.
