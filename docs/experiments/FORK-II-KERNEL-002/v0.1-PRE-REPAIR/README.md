# FORK-II-KERNEL-002 v0.1 — pre-repair opening

This separately named successor opens with four concrete fixture inputs and exact expected outputs defined before repair. It is not a release of a repaired kernel. No successor fixture has been executed in this opening; historical observations remain in the [predecessor admission](../../../../admissions/FORK-II-KERNEL-001/v0.1.1-CLOSED-HISTORICAL-EVIDENCE/README.md).

| Fixture | Preserved uncovered surface | Successor acceptance oracle |
| --- | --- | --- |
| FII-23 | `immutable=false` remains hash-equivalent under CANON-v1 | `referent_integrity=CORRUPTED_OR_CHANGED`, reuse false, `REEVALUATION_REQUIRED` |
| FII-24 | `not-a-hash` values plus consistent self-hashes appear bound | `DEPENDENCY_BINDING_NOT_ESTABLISHED`, recomputation false |
| FII-25 | Past `FIXED_TIME` end still produces `CURRENT` | Preserve period kind `FIXED_TIME`; current use `EXPIRED` |
| FII-26 | `UNKNOWN` end still produces `CURRENT` | Preserve period kind `UNKNOWN`; current use `NOT_ESTABLISHED` |

These outputs are prospective successor design decisions, not outputs claimed to exist in v0.1.1. Inputs and oracles are in `fixtures/`; they must not be weakened to make a repair pass. Any changed oracle requires a separately recorded protocol amendment preserving this version.

## Isolation and temporal semantics

FII-23 resets the observed profile to the referenced profile before changing only `immutable`. Thus the original FII-19 execution-dimension change cannot mask the uncovered surface. Do not silently redefine CANON-v1. A repair may enforce immutability separately; changed hash inclusion requires a new canonicalization version.

FII-24 supplies all 11 dependency IDs, malformed digest values, and internally consistent snapshot self-hashes. Rejection cannot be credited merely to missing key coverage or mismatched snapshot hashes. Passing this fixture alone does not demonstrate validation against actual dependency-record bytes.

The preserved AP-03 changed the end to 2000 while retaining a 2026 start. FII-25 deliberately uses a valid 1999–2000 interval to isolate expiry from a reversed interval. That adjustment is a successor design choice, not a rewrite of AP-03. `request.evaluation_time` is explicit and fixed; the wall clock must not be an implicit input. Fixed intervals are half-open: start <= evaluation_time < end. At or after end, status is EXPIRED; before start, NOT_YET_EFFECTIVE. Missing/malformed evaluation time or invalid interval yields NOT_ESTABLISHED. These additional boundary cases require controls before repair admission.

FII-26 treats UNKNOWN as uncertainty, not as a claim of actual expiry or indefinite validity. It does not infer current authority from historical persistence.

## Ordered next gates

1. Admit this opening and its byte-bound definitions before changing implementation.
2. Execute these exact fixtures against an isolated byte-identical predecessor implementation under the successor experiment; preserve raw outputs and an expected pre-repair failure receipt. A failure is a successor observation, not a retroactive historical failure. Do not overwrite predecessor evidence.
3. Define and preserve controls before repair: unchanged immutable profile; a fully bound snapshot with supplied dependency-record bytes; missing bytes, malformed hashes and well-shaped incorrect digests; in-range, exact-end, pre-start, malformed and reversed fixed intervals; UNKNOWN/null. Define record-byte encoding and digest validation explicitly for those controls.
4. Repair only the successor. Preserve FII-01–FII-22 fixture bytes and require their baseline expectations plus all 12 predecessor mutant detections; require FII-23–FII-26 and the controls, with targeted fault reintroductions proving each new oracle detects its intended behavior.
5. Preserve post-repair raw output, environment, hashes, canonicalization/version changes, negative results, and independent recomputation before any successor release admission.

The opening confers no repaired status, general correctness, truth, compliance, production readiness, or inherited authority. The four cases are a bounded population, not a completeness claim.

## Subsequent pre-repair status — 2026-09-23

Ordered gate 2 has now been executed against the byte-identical predecessor: FII-23 through FII-26 produced `0/4 PASS`, `4/4 FAIL`, and the expected pre-repair failure was preserved. A separately supplied recomputation record reproduced the same four-fixture result and is admitted under [`recomputation/`](recomputation/) with an additive reconciliation; its source bytes are preserved unchanged.

The reconciliation does not change the fixture result. It records one erroneous FII-24 recomputed canonical-payload field in the supplied receipt and narrows the repository's supported relationship to a separate recomputation record using the same predecessor implementation rather than inferring a stronger independence class from the source label.

**Current next gate:** ordered gate 3 — define and preserve the control population before any repair.
