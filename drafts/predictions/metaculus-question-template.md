# Metaculus question template

Listing worksheet for one Appendix P market. Not manuscript canon.
Copy the block at the bottom once per market. Stop: delete this file when Markets 19–21 are listed or withdrawn.

Sources checked 2026-10-05:

- Create form, as pasted from the Metaculus question editor (multiple choice).
- Writing guide: [Question writing and submission guidelines](https://www.metaculus.com/question-writing/). The live page is behind a bot check; the same numbered rules are on the [pandemic mirror](https://pandemic.metaculus.com/question-writing/).
- Field lengths: public models on `main` of [Metaculus/metaculus](https://github.com/Metaculus/metaculus) — `questions/models.py` (`Question`) and `posts/models.py` (`Post`).

## What the writing guide limits

The guide states no character or word caps.

The limit that binds these markets is admin time. The guide says to reject a question that would take more than about 15 minutes of admin effort to resolve, unless the question is important enough to justify more. Three admin-role reviews of Markets 19 and 20 (see `metaculus-admin-trials/`) estimated 45–75 minutes and 30–45 minutes. That is the gap to close, not a missing character budget.

Other rules that shape the fields:

- Resolution criteria should be tight, concrete, and cover edge cases, including a data source that stops being published.
- Only Metaculus admins resolve. The text must not hand the decision to the question author or to another named party.
- The long title must match the resolution conditions.
- Details that are not needed to understand the question go in the fine print.

## What the database limits

| Form field | Stored as | Limit |
|------------|-----------|-------|
| Long title | `Question.title` and `Post.title` | 2000 characters |
| Short title | `Post.short_title` | 2000 characters. The form asks for a shorter version of the long title, ending in a question mark. The database allows the same length as the long title. |
| Background information | `Question.description` | No maximum (`TextField`) |
| Resolution criteria | `Question.resolution_criteria` | No maximum (`TextField`) |
| Fine print | `Question.fine_print` | No maximum (`TextField`) |
| Choices | `Question.options`, each a string | 200 characters per option |
| Group variable | `Question.group_variable` | Unused for a single multiple-choice question. Leave blank. |

Dates on the form are entered in the editor's local timezone. Store them here in UTC, matching the appendix ("end of day UTC").

## Why the TeX boxes were split

There is no Metaculus size limit that forced the split.

`predictionbox` in `metadata/preamble.tex` is a `tcolorbox` with no `breakable` option. Each market box sits inside an `authbar`, and an authbar is an `mdframed` frame. A frame that contains an unbreakable box taller than the text block does not continue on the next page. The build prints `non splittable contents` and opens blank pages until it is killed. That happened on the common-rules box once it grew past about a page (453 words; the largest box in the last commit of the appendix was 354 words). Markets 1, 13, 19, and 20 were in the same range.

Splitting one contract into "part 2 of 5" boxes was a workaround for that page break. It is the wrong structure for a Metaculus question, which is one long title, one background, one resolution section, and one fine print.

## How to lay the fields out (implemented for Markets 19–20)

Four TeX environments, outside the authorship bar (the bar closes before the contract block and reopens for post-contract prose such as closest existing work):

| Environment | Metaculus field | PDF / site |
|-------------|-----------------|------------|
| `predictionbox` | Long title, parameters, choices, resolve-by | Strong orange callout |
| `predictionbackground` | Background information | Lighter orange, breakable |
| `predictionresolution` | Resolution criteria | Lighter orange, breakable |
| `predictionfineprint` | Fine print | Lightest orange, breakable |

The front `predictionbox` stays short (under one page). The three lighter boxes use `mdframed` (page-splittable on TeX Live basic; `breakable` `tcolorbox` needs `pdfcol.sty`, which this build does not have). Do not nest any contract box inside `authbar`.

Markets 1–18 still use a single legacy `predictionbox` until migrated. Do not split one question into several `predictionbox` environments.

If a lighter box still fails to break inside a frame, the fallback is to keep the authbar closed for the whole contract block (already done for Markets 19–20).

## Field map

| Metaculus field | Appendix P today | Notes |
|-----------------|------------------|-------|
| Type | Multiple choice | YES, NO, OTHER. Market 20 lists YES and OTHER. |
| Long title | The Question line | One sentence, ends with a question mark. Put parameters on their own lines under it, not inside the sentence. |
| Short title | The `predictionbox` optional title, rewritten as a question | Example shape: "Assurance stacks pass a hidden-case tournament by June 2028?" |
| Background | Prose before the box: what the tournament or challenge is, how to fill each bracket, closest existing work | Factual. Links to the protocol document once it exists. |
| Resolution criteria | Qualifying-attempt list, performance bars, case labels, the YES/NO/OTHER rule | The specific event, the date, and where the artifact is downloaded. |
| Fine print | Independence, signed statements, unit rule, Clopper-Pearson level, what the resolver does not investigate | The guide's place for the lawyerly detail. |
| Choices | YES, NO, OTHER as defined in the reading rules | Each option must stay under 200 characters. The parenthetical definitions in the current Question line are too long to be the option text; put the definitions in the resolution criteria and keep the options as YES, NO, OTHER. |
| Closing time | Not in the appendix | When forecasting closes. Can equal the resolve-by date. |
| Resolving time | Resolve by | When the outcome is expected to be known. |
| Open time | Not in the appendix | When forecasting opens. |
| CP reveal time | Not in the appendix | Leave at the platform default unless a reason exists to hide the community prediction. |
| Categories | Not in the appendix | Platform tags. Not part of the contract. |
| Group variable | — | Blank. |

## Copy block

```
Market:
Type: Multiple choice

Long title:

Short title:

Background:

Resolution criteria:

Fine print:

Choices:
- YES
- NO
- OTHER

Open time (UTC):
Closing time (UTC):
Resolving time (UTC):
CP reveal time (UTC):

Categories:
Group variable:
```
