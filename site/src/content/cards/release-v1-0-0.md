---
title: "v1.0.0 — First official major release"
type: "release"
status: "reviewed"
releasedAt: "2026-06-30"
version: "1.0.0"
summary: "First official manuscript release: freezes sequential chapters ch01–ch48 and appendices A–G so cross-references, tooling, and external links have a stable target."
decision: "External links and citations should target the post-renumber chNN / appendix letters from this release onward."
related: ["releases-updates", "release-v1-1-0"]
external:
  - label: "Full release notes"
    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/RELEASE_NOTES.md#v100--2026-06-30--first-official-major-release"
  - label: "Tag v1.0.0"
    url: "https://github.com/GunnarZarncke/towards-asi-alignment/releases/tag/v1.0.0"
---

Released **2026-06-30**. Commit: `bd8f82f` · Tag: `v1.0.0`.

The first official release freezes a **stable, canonical numbering scheme** for chapters and appendices.

### Highlights

- **Sequential chapters `ch01`–`ch48`.** Temporary split chapters (`ch19b`, `ch25b`, `ch35b`, `ch39b`) absorbed into the main sequence.
- **Appendices A–G** match printed letters (Notation, Bridge Crosswalk, Institutional Translation, Worked Example, Glossary, Research Program, Lean Proof Spine).
- **History preserved** via `git mv` renames so `git log --follow` still works.
- **Manuscript state:** 10 parts, 48 chapters with first drafts; 7 built appendices; ~235 bibliography entries; Lean proof spine; `./build.sh` and `make check` pass.

### Upgrade note

External links should target the new `chNN` / appendix letters. See the [releases hub](/cards/releases-updates/) and the follow-on [v1.1.0](/cards/release-v1-1-0/) companion-site release.
