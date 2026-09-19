# v0.1.0 External Assessment Lineage

This directory preserves the external assessment materials that motivated `FORK-HANDOFF-SEMANTIC-CORE-001-v0.1.1`.

The predecessor package is preserved by digest, not rewritten:

- `FORK-HANDOFF-SEMANTIC-CORE-001-v0.1.0.zip`
- SHA-256: `baa112e3260decf707f0ed95578257c0deaa475bc43f30c9c2fc91747b674cf2`

Preserved external observations:

- v0.1.0 semantic behavior reproduced exactly;
- five declared invariants were implemented but lacked direct packaged adversarial fixtures;
- two runtime-generated `.pyc` files were outside the package manifest/checksum closure;
- a structurally valid `TRUTH` claim with `claim_basis: DECLARED` can pass by design, so validator `PASS` must not be promoted to truth established;
- repository admission was not performed by the external executor.

These observations motivate only the bounded repair delta in v0.1.1. They do not confer repository admission, cryptographic integrity, independent witnessing, truth, authority, compliance, production readiness, or generalization.
