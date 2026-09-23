# Fork II KERNEL-002 v0.1 — pre-repair recomputation reconciliation 001

**Record ID:** `FORK-II-KERNEL-002-v0.1-RECOMPUTATION-RECONCILIATION-001`  
**Date:** `2026-09-23`  
**Treatment:** additive reconciliation; supplied source receipt remains unchanged  
**Repair effect:** none

## Preserved source

The supplied receipt `FORK-II-KERNEL-002-v0.1-INDEPENDENT-RECOMPUTATION-RECEIPT-20260923.json` is preserved without editing, SHA-256 `46f4ef68ce05744435fd27eaa5964ef1ff8be47ed75b34c606c0c54983363b2b`.

It records a separate recomputation of `FORK-II-KERNEL-002-v0.1-PRE-REPAIR-EXECUTION-001` and reports the bounded result `0/4 PASS`, with FII-23 through FII-26 all failing against the byte-verified predecessor. That substantive disposition remains supported.

## Reconciliation A — FII-24 canonical payload hash field

The preserved JSON receipt contains an internal contradiction in FII-24:

- `recorded_canonical_payload_hash` = `02f32c7a9f22635ff6fadfe105f9724751c2bf9f8aa832a4a6edde5adff24cf9`
- `recomputed_canonical_payload_hash` = `77a942a92b8b586891386edbe492812f8916063426ff87f193f287a5a6e1aca9`
- `canonical_payload_hash_matches` = `false`
- the same finding text states that the enclosing canonical payload and snapshot hashes recompute exactly.

Direct recomputation using the frozen predecessor CANON-v1 implementation and unchanged FII-24 fixture yields:

- canonical payload hash = `02f32c7a9f22635ff6fadfe105f9724751c2bf9f8aa832a4a6edde5adff24cf9`
- snapshot hash = `a77be9918525dcddd8348138bef8a1a0d67c50003a68ef4f5d92826bf12b4a5f`
- snapshot binding issues = `[]`

The reconciled interpretation is therefore `canonical_payload_hash_matches=true`. The supplied JSON field is preserved as received and is not overwritten.

This discrepancy does not change the FII-24 fixture disposition. All 11 dependency-record digest values remain malformed (`not-a-hash`), while the predecessor still classifies the snapshot `REPRODUCIBLY_BOUND` and permits recomputation. The preserved failure is a digest-validation gap, not corrupted fixture arithmetic.

## Reconciliation B — independence class

The source filename, `record_type`, execution-phase label, claim-boundary text, and conclusion use unqualified `independent` terminology. Those historical bytes are preserved.

For this repository admission, the supported relationship is narrower:

> A separate recomputation record reproduced the four pre-repair failures from the preserved archive and the same predecessor implementation.

This admission does **not** infer from the source label alone:

- independent implementation recomputation;
- independent human recomputation;
- institutional independence; or
- cross-environment recomputation.

A stronger independence property requires separately preserved evidence for that property.

## Bounded disposition

The following remain supported for the admitted pre-repair population:

- predecessor archive identity: SHA-256 `a9c18311043c505137eaece9db6b72b9b186be33a8970df48d3fe5800d1de760`;
- pre-repair execution archive identity reported by the source: SHA-256 `fff3f3f935808e253bce2be7ffde406eb08f5067f5d3f5519a333d8b83d5dcd7`;
- FII-23: FAIL;
- FII-24: FAIL;
- FII-25: FAIL;
- FII-26: FAIL;
- aggregate result: `0/4 PASS`, `4/4 FAIL`;
- disposition: `EXPECTED_PRE_REPAIR_FAILURE_PRESERVED`.

No repair is authorized or claimed by this reconciliation.

## Next gate

The next substantive gate remains the separately defined control population before repair: unchanged immutable profile; fully bound snapshot with supplied dependency-record bytes; missing bytes, malformed hashes and well-shaped incorrect digests; in-range, exact-end, pre-start, malformed and reversed fixed intervals; and UNKNOWN/null controls, with record-byte encoding and digest validation explicitly defined.

## Non-claims

This reconciliation does not establish general correctness, completeness, production readiness, independent implementation, independent human authorship, institutional independence, cross-environment portability, truth, authority, compliance, or correctness of any future repair.
