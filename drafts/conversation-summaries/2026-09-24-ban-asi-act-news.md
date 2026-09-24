# 2026-09-24 — Ban Artificial Superintelligence Act field news

## Trigger
User asked for a site news entry on the [Ban Artificial Superintelligence Act](https://www.sanders.senate.gov/wp-content/uploads/Ban-Artificial-Superintelligence-Act.pdf), quoting the bill and the book in the usual quote-bridge form.

## Done
- Field-news YAML entry `field-news-ban-asi-act-sep-2026` (`kind: policy`, `eventDate` 2026-09-23, site `date` 2026-09-24).
- Body at `metadata/field-news/bodies/ban-asi-act-sep-2026.md` (quote-bridge: bill red / this book black). Quotes are from the Senate text, not the one-pager.
- News takeaway quiz item; merged quiz drafts (216 questions).
- Quote color `--src-bill` in site tokens and global CSS.
- `cd site && npm run sync:field-news && npm run generate:card-redirects && npm run build:feed`.
- Attic quiz writer `ROOT` now points at the repo (`parents[2]`), so a later regen from `scripts/attic/` writes the real draft.

## Decisions
- Cut: §§9–10 can refuse a release or shut a system down. §8 ends the training pause when the Department is staffed and the Secretary calls the rules clear. The lasting ban still needs a finding that survives a system optimizing against the inspection.
- House sponsor (Casar) is attributed to the 23 September press release. The PDF on the Senate site is Sanders’ text only.
- No manuscript cite or bib key.

## Revision
- Replaced the “Exhibits” heading and the inspection sentence with a direct claim: deceiving the inspector is a banned trait, and a successful deception can look like a clean report.
- Replaced “One statute, and a policy for everywhere else” with “U.S. labs are bound. Other countries are a policy line.” Closing sentence now says the named labs are inside the statute and §15 starts a wider pause that does not yet cover a lab outside U.S. law.

## Open / next
- Optional: bibliography key if the Act should appear in the PDF.
- The bill is not yet numbered (`S. ll` in the draft text).

## Key paths
- `metadata/field-news.yml`
- `metadata/field-news/bodies/ban-asi-act-sep-2026.md`
- `/cards/news/field-news-ban-asi-act-sep-2026/`

## Commits
- `764c572d1` Add field news on Sanders’ Ban Artificial Superintelligence Act.
