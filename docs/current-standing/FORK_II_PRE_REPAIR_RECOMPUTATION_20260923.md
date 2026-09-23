# Fork II KERNEL-002 pre-repair execution and recomputation — 2026-09-23

FORK-II-KERNEL-002 v0.1 has completed its frozen pre-repair fixture execution against the byte-identical admitted predecessor implementation. FII-23 through FII-26 each failed against their prospective successor oracles, producing `0/4 PASS`, `4/4 FAIL`. No successor repair has been performed.

A separately supplied recomputation receipt reproduced the same bounded four-fixture failure result from the preserved execution archive. The source receipt is preserved unchanged under `docs/experiments/FORK-II-KERNEL-002/v0.1-PRE-REPAIR/recomputation/sources/` and is admitted only with `RECOMPUTATION_RECONCILIATION_001` attached.

The reconciliation preserves two documentary limitations without changing the fixture result:

1. the source JSON contains an erroneous FII-24 `recomputed_canonical_payload_hash` field and `canonical_payload_hash_matches=false`; direct recomputation with the frozen predecessor CANON-v1 implementation yields the recorded `02f32c7a...24cf9` payload hash and `canonical_payload_hash_matches=true`;
2. the source uses unqualified `independent` terminology. Repository standing records only a separate recomputation record using the same predecessor implementation; no stronger implementation, human, institutional, or cross-environment independence class is inferred from the source label alone.

The predecessor remains closed historical evidence. The successor remains pre-repair. The next evidence-bearing gate is to define and preserve the control population specified by the KERNEL-002 opening before any repair begins.

This note is additive current-state routing. It does not revise the predecessor result, expand the four-fixture population, establish a stronger independence class, authorize repair, or establish general correctness, truth, authority, compliance, production readiness, or completeness.
