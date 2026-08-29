# Gate round 1 (2026-08-29)

Scorer instance isolated from drafter. N=3 naive + 1 adversary. Pass criterion as in PROTOCOL.md.

## Predictor bundles (1–5 scales in packet)

| Packet | Result |
|--------|--------|
| bundle-gamma (B6, B7) | FAIL |
| bundle-delta (B1, B8) | FAIL |
| bundle-alpha (B2, B3, B10) | FAIL |
| bundle-beta (B4, B5, B11, B12) | FAIL |

Revision cap remaining: 1 after this round (initial + 2 revisions). Item-level leak: numeric poles plus the continuity/drift cover. **Atomize:** workers collect dated facts only; no 1–5 in the worker envelope. Mapping to ordinal scores is not a worker task.

Hashes of failed packets remain in `packet-hashes-draft.txt` for audit. Do not deploy those bytes.
