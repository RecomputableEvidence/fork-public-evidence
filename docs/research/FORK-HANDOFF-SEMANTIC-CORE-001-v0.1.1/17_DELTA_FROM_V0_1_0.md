# Delta from FORK-HANDOFF-SEMANTIC-CORE-001-v0.1.0

**Successor:** `FORK-HANDOFF-SEMANTIC-CORE-001-v0.1.1`  
**Predecessor ZIP SHA-256:** `baa112e3260decf707f0ed95578257c0deaa475bc43f30c9c2fc91747b674cf2`

v0.1.0 remains preserved unchanged. v0.1.1 is a bounded repair successor motivated by the preserved external assessment under `14_REPAIR_LINEAGE/`.

## Authorized repair delta

1. Remove runtime-generated `__pycache__` / `.pyc` files from the package and add executable closure verification.
2. Add explicit adversarial fixtures for `INV-003`, `INV-004`, `INV-006`, `INV-008`, and `INV-012`, producing direct packaged fixture coverage for 15/15 declared semantic invariants.
3. Add a valid declared-`TRUTH` interpretation fixture and explicit prohibited promotion `VALIDATOR_PASS != TRUTH_ESTABLISHED`.

## Not changed

- predecessor repository commit/tree coordinates;
- typed semantic schema;
- the 15 semantic invariants;
- the reference validator's semantic logic;
- the coordinated re-seal successor target;
- the exclusion of cryptographic integrity and external witnessing from this object.

No repair in v0.1.1 may be interpreted as retroactively changing v0.1.0 or as solving `FORK-EXTERNAL-WITNESS-BINDING-001`.
