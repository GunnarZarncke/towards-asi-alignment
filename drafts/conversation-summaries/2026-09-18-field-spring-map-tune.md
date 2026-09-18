# 2026-09-18 — Field spring-map layout tune

## Trigger

User asked why many listings sit on both MB6 and MB10 despite no bridge–bridge edge, and to vary spring *stiffness* more than rest length.

## Done

- Spring model: nearly constant rest gap; stiffness ~ \(w^2\) (`weights.ts`).
- Layout/UI from the same demo thread (already in tree): ×1.5 bridge scale, hover tooltip, hover-highlight crux edges, MB4a stacked on MB11’s x.

## Decisions

- MB6–MB10 co-occurrence in the demo is mostly **not** a missing graph edge. Of 40 dual listings, all 40 are `inherited`; 31 are fuzzy-matched onto `christiano-lineage` because clustering label `ARC` is a substring of `research`. Real dual coding remains for Christiano (WFL + amplification), Anthropic, Apollo, METR. Practitioner bundling (eval Goodhart vs forgeable certificates) is a plausible *second* story, not required to explain the map.

## Open / next

- Tighten inherit matching (word-boundary / min key length) so `ARC` does not capture every `*Research*` org.
- Optional: show inherit vs heuristic as a visual filter so cluster-copying is visible.

## Key paths

- `demos/ch05-field-spring-map/weights.ts`
- `demos/ch05-field-spring-map/scripts/build_snapshot.py` (`match_agenda` fuzzy)
