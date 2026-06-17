# Towards Superintelligence Alignments

**Boundaries, Value Bundles, and the Correction of Civilization**

## Thesis

Superintelligence alignment is not mainly the problem of installing a fixed human utility function into a machine; it is the problem of preserving a human-correctable value-update process across capability growth, ontology shift, successor creation, and socio-technical selection pressure.

> This manuscript develops a conceptual and formal framework for superintelligence alignment. It is not a claim that the alignment problem is solved. The book distinguishes between established claims, plausible hypotheses, and open research problems.

## Manuscript status

| Item | Status |
|------|--------|
| Milestone | First (scaffold complete) |
| Chapters | 45 stubs |
| Appendices | 8 stubs |
| Front matter | Title page, executive overview (stub), roadmap |
| Bibliography | Skeleton `.bib` files |
| PDF | Builds from `book.tex` |

Chapter progress is tracked in `metadata/book.yml`. All chapters are currently **stub**.

## Build instructions

Requires a TeX distribution with `latexmk`, `pdflatex`, `biber`, and the `memoir` class.

```bash
./build.sh        # or: make pdf
./clean.sh        # or: make clean
make check        # structure + citation checks
make wordcount    # approximate chapter word counts
make todos        # list [STUB] / TODO markers
```

Output: `dist/pdf/towards-superintelligence-alignments.pdf`

### PDF extracts (source canon)

```bash
python3 scripts/extract_pdf_to_md.py   # regenerate context/extracts/
```

## Folder structure

```text
book.tex              # root LaTeX file
metadata/             # book.yml, ledgers, notation, preamble
frontmatter/          # title page, overview, roadmap
parts/                # 10 part include files
chapters/             # 45 chapter files
appendices/           # 8 appendix files
references/           # BibLaTeX files by source type
tables/               # chapter map, notation, artifacts
figures/              # source, generated, tikz
scripts/              # build, check, wordcount utilities
review/               # reviewer templates
context/              # source PDFs, extracts, messaging notes
INSTRUCTIONS.md       # full agent instructions for the book
AGENTS.md             # agent behavior guidelines
```

## Chapter status

| Part | Chapters | Status |
|------|----------|--------|
| I. The Alignment Problem Reframed | 1–4 | stub |
| II. Agents, Boundaries, and Real Optimizers | 5–9 | stub |
| III. Capability Growth and Competence | 10–13 | stub |
| IV. Human Values as Bundle Geometry | 14–18 | stub |
| V. Goal Inference | 19–22 | stub |
| VI. Correction Channels | 23–26 | stub |
| VII. Successors, Reproduction, and Continuity | 27–30 | stub |
| VIII. Attractor Basins and Socio-Technical Selection | 31–35 | stub |
| IX. Adversarial Measurement and Practical Guarantees | 36–40 | stub |
| X. The Philosophical and Civilizational Limit | 41–45 | stub |

## Contribution and review

- Read `INSTRUCTIONS.md` before large writing tasks.
- Follow `AGENTS.md` for agent behavior and `context/writing-style-gunnar.md` for voice.
- Use `review/reviewer-guide.md` and the review templates for structured feedback.
- Update `metadata/claims-ledger.md`, `assumptions-ledger.md`, and `uncertainty-ledger.md` as chapters mature.

### Git workflow

```text
chapter/chXX-short-name    # one chapter per branch
review/technical           # technical review pass
review/legibility          # policy/legibility pass
```

Conventional commits: `init:`, `chapter:`, `refs:`, `formal:`, `review:`, `build:`

## Citation policy

- Use BibLaTeX (`biblatex` + `biber`); do not manually format references.
- Internal project sources go in `references/internal-project-sources.bib`.
- Body text must introduce concepts from first principles; do not use internal project names (e.g. "UAD") as explanatory shortcuts.
- Every chapter should cite from at least three categories where relevant: alignment, information theory/dynamical systems, and values/governance/philosophy.

## License

MIT — see [LICENSE](LICENSE).

## Known open problems

See `metadata/open-problems.md` and `metadata/uncertainty-ledger.md`. At minimum:

1. Are human values sufficiently low-dimensional?
2. Can bearer maps survive radical ontology shift?
3. Can correction-channel integrity be measured under adversarial conditions?
4. Can successor constraints be enforced before recursive capability growth?
5. Can composite agent boundaries be detected in real deployment systems?

## Next milestone

Second milestone (`INSTRUCTIONS.md` §25): preface, executive overview, roadmap, chapters 1–2, appendices A and F.
