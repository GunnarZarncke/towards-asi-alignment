# Bridge first-use (Ch. 10 gate)

Status: **implemented** (2026-09-01). Manuscript + `\leanspine` placement. Lean modules unchanged.

**Lanes:** Voice (when the word is allowed) · Spine (home-chapter tags). Pointers: [`voice.md`](voice.md), [`spine.md`](spine.md).

**Non-goals:** Discharge any `MB*` on real systems; retitle Appendix B; site/quiz sync (follow-on); adding `\leanspine` in every chapter that mentions a load.

---

## Policy

1. **Genus first-use is Chapter 10** (end of Part II). A *bridge* is a named dependency the argument uses and does not close (empirical or philosophical interface; Lean does not prove it). Three tags from here on: closed step, finite separation, undischarged dependency.
2. **Before Chapter 10:** no Lean, no “proof spine” / `\leanspine` / `{leanbox}`, no `MB*` IDs, no technical use of the word *bridge*. Assumptions, dependencies, and A-\* boxes only.
3. **`\leanspine{bridge}{MBn}` once, in the home chapter only.** Assembly ranges (`MB1--MB9`) in Ch. 42 / 48 stay as *composition* cites, not first-use. Appendix D may keep worked-example pointers; they are not first-use.
4. **MB2 / MB3 do not move into Part II.** Their homes are Parts IV–V. The Part II recap tag is **MB1** (A-004 already states the recovery load in Ch. 7).
5. **Do not treat A-\* boxes as bridges.** Intro already splits them from Lean names; keep that split after the genus exists.

---

## 1. Introduce the concept in Chapter 10

In `chapters/ch10-strategic-opacity.tex`, before or at the existing filter-coverage discussion:

- Short operational definition (genus, not the full MB roster).
- **“We can now formalize…”** looking back at Part II / A-004: `\leanspine{bridge}{MB1}{…}` — estimator soundness; the recovery step used in Ch. 7 is now a named undischarged dependency.
- Local instance: keep `\leanspine{bridge}{MB7b}{…}` (filter-family coverage). Two tags in Ch. 10 is intended (retro MB1 + local MB7b).
- Point forward: later chapters name the matching `MB*` at first need; Appendix G is the skeleton; Appendix B maps to field problems.
- Optional one `{leanbox}` at this site (existing “at most one leanbox per chapter” rule).

Do not lead the definition with MB7b alone. MB1 is the teaching example.

---

## 2. Rewrite before Chapter 10

Keep calibration; drop the undefined genus. No Lean, no proofs-as-spine, no `MB*`.

| Place | Change |
|-------|--------|
| Preface | “field crosswalk” / “assumption–field map”, not “bridge–field crosswalk” |
| Intro | Keep A-\* boxes; drop or defer “proof map” / Appendix G as Lean. Physical-bridge closer may stay (technical term not yet in play) |
| Exec overview | Already mostly clean; do not reintroduce Lean |
| Current status | “Lean checks” is site meta — leave or say “companion-site checks” |
| Ch. 3 | Keep P01 *math* as a template; **drop** `\leanspine` / `{leanbox}`. **Move** P30 / CCI packaging to Ch. 26 or 42 |
| Ch. 4 | Drop “Lean types `ConstitutionalRule`…”. “Later assumption about spec coverage”, not “later bridge (`MB9`)”. “Not a new load-bearing assumption”, not “not a new bridge” |
| Ch. 5 | Keep Q4 regime in A-003 / A-005 / A-012. Drop `MB5`, `MB11`, `{leanbox}` `Safe`. Drop “not as a new bridge” or say “not a new named dependency”. Distinct-instrument claim without App. G cite. **Move** certify⇒`Safe` to Ch. 42 |
| Ch. 6 | Leave (`proof of agency` is ordinary English; “bridge to the rest of the book” is metaphor — optional later cleanup) |
| Ch. 7 | Keep A-004 and identifiability *prose*. Drop `\leanspine`, `{leanbox}`, `MB1`. “Recovery step” / “needed interface”, not “representation/recovery bridge”. P34/P35/CID stay as untagged claims (optional recap macros in Ch. 10, not required) |
| Ch. 8 | **Move** `forgeability_gap` + MB10 box to Ch. 31 (already duplicated). Ch. 8 keeps transport-of-identity without spine tags |
| Ch. 2 footnote / App. B refs | Forward-ref to Appendix B as field map is OK if it does not say “bridge” as a defined term |

Physical/rhetorical “bridge” (Ch. 3 inspector, Ch. 9 collapse, etc.): out of scope unless it sits next to a deleted `MB*` sentence.

---

## 3. Home-chapter `\leanspine{bridge}` only

One dedicated tag per live ID. Do not tag every split (`MB2a`…) unless that chapter teaches the chain. Do not add a Ch. 7 MB1 tag (Ch. 10 is first-use).

| ID | Home | Notes |
|----|------|--------|
| **MB1** | **Ch. 10** | Recap of Ch. 7 / A-004. “We can now formalize…” |
| **MB2** | Ch. 17 | Identifiability / representation load. Ch. 21 keeps counterexamples; no second `{bridge}{MB2}` |
| **MB3** | Ch. 18 | Bearer transport. Chapter currently has **no** `\leanspine` |
| **MB4** | Ch. 25 | Correction integrity. Not only a table in Ch. 42 |
| **MB4a** | Ch. 26 | Own `{bridge}` tag; do not bury only inside `\leanspine{proof}{P24}` |
| **MB5** | Ch. 30 | Successor / ontology shift. Not Ch. 5 |
| **MB6a** | Ch. 35 | Percolation / cooperation evidence |
| **MB6b** | Ch. 37 | Basin → correction (or Ch. 35 if 37 has no natural site — pick one, not both) |
| **MB7a** | Ch. 10 or 11 | Access-model; first chapter after the gate that states it. Not a third teaching example in the genus paragraph |
| **MB7b** | Ch. 10 | Already present; keep as local instance |
| **MB7c** | Ch. 43 | Cost-of-faking / hidden-BIQ → robustness |
| **MB7d** | Ch. 35 | Inferential coupling |
| **MB8** | Ch. 28 | Gravestone only |
| **MB9** | First **post-Ch. 10** chapter that states the grounding certificate | Not Ch. 3–4. Confirm against A-014 restatement / `book.yml` (candidates after Part II, not App. D) |
| **MB10** | Ch. 31 | Drop or shorten Ch. 48 duplicate; Ch. 8 tag goes away with the move |
| **MB11** | Ch. 42 | Certify ⇒ `Safe`. Not Ch. 5 |

**Keep as assembly, not first-use:** Ch. 42 / 48 `\leanspine{bridge}{MB1--MB9}`; Ch. 43 `\leanspine{bridge}{MB7a--MB7d}` if the letters already have homes.

**App. E glossary:** three-line entry after Ch. 10 exists (bridge vs A-\* vs MB\*). Ch. 44 four-way inequality can stay as sharpness, not first occurrence.

---

## Order of work

1. Freeze + rewrite Ch. 3–8 and frontmatter (section 2), including Ch. 8 → Ch. 31 move and Ch. 3 P30 / Ch. 5 MB11 relocations.
2. Chapter 10 genus + MB1 recap + existing MB7b (section 1).
3. Add missing home tags (section 3) in later chapters; remove extra `{bridge}` tags outside homes.
4. Glossary one-liner; optional site/quiz follow-on (out of this plan unless asked).

## Verification

- Grep `chapters/ch0*.tex` + `frontmatter/*.tex`: no `MB[0-9]`, no `\leanspine`, no `{leanbox}`, no “proof spine”.
- Grep `\leanspine{bridge}{MB`: each live ID has exactly one chapter home (plus allowed assembly ranges and App. D).
- `./build.sh` after `.tex` edits.

## Related

[`metadata/bridges.yml`](../../metadata/bridges.yml) · [`chapters/ch10-strategic-opacity.tex`](../../chapters/ch10-strategic-opacity.tex) · [`chapters/ch07-finding-boundary.tex`](../../chapters/ch07-finding-boundary.tex) (A-004) · [`appendices/appG-lean-proof-spine.tex`](../../appendices/appG-lean-proof-spine.tex) · [`appendices/appB-bridge-crosswalk.tex`](../../appendices/appB-bridge-crosswalk.tex)
