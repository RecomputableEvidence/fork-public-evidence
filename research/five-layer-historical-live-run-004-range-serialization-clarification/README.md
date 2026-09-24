# Five-Layer Historical Live Run 004 — Range Serialization Clarification 001

This is a successor clarification to the frozen Run 003 semantic rerun and its recomputation. It introduces exactly one substantive change: an explicit canonical byte-serialization contract for evidence-range hashing.

The contract is:

`one-based inclusive bounds → join selected lines with LF → append one final LF → UTF-8 without BOM → SHA-256`

The 17 Run 003 range coordinates and hashes are carried unchanged in `RUN003_RANGE_HASH_BINDING_UNCHANGED.json`.

No semantic rerun is performed here. No detector outcome or Stage 3 standing changes.
