# FORK-II-KERNEL-002 v0.1 — successor-only repair and combined execution

**Status:** POST-REPAIR EXECUTION EVIDENCE — NOT RELEASE ADMISSION  
**Date:** 2026-09-23

Ordered gate 4 has been executed after the separately admitted pre-repair fixture and control freezes. The predecessor remains closed historical evidence and was not modified or resealed.

## Repair scope

The successor implementation is `FORK-II-KERNEL-002-EXECUTABLE-PROBE-v0.1`. The repair is limited to the four already frozen uncovered surfaces:

1. profile `immutable` integrity is enforced separately from unchanged CANON-v1 hashing;
2. dependency digest syntax is validated and, where the frozen controls supply record bytes, exact UTF-8 record-byte SHA-256 digests are verified;
3. valid fixed intervals are evaluated against explicit `request.evaluation_time` under the frozen half-open interval semantics;
4. `UNKNOWN` end state does not establish current validity.

CANON-v1 is not redefined. No FII-01–FII-26 fixture or frozen control oracle is changed.

## Combined execution

The preserved post-repair execution reports:

- FII-01–FII-22 baseline: `22/22 PASS`;
- FII-01–FII-26: `26/26 PASS`;
- frozen controls: `13/13 PASS`;
- combined population: `39/39 PASS`;
- predecessor mutants detected: `12/12`;
- targeted successor fault reintroductions detected: `8/8`.

The eight targeted faults were defined to reintroduce the repaired decision boundaries: ignored immutability, missing dependency bytes, malformed dependency digest acceptance, well-shaped wrong digest acceptance, ignored fixed-time position, invalid fixed-interval acceptance, missing/malformed evaluation-time defaulting, and UNKNOWN-end promotion to current validity.

## Preserved negative attempt

The executable package preserves an initial harness-construction failure. Attempt 001 retained predecessor-package assumptions in the successor test wrapper and misidentified two historical mutant witness fixtures. It did not change implementation or frozen inputs. Attempt 002 corrected only the test/receipt harness and produced the bounded result above.

## Primary package

`artifacts/FORK-II-KERNEL-002-EXECUTABLE-PROBE-v0.1-POST-REPAIR-20260923.zip`

The package contains the successor implementation, FII-01–FII-26, the exact frozen 13-control population, tests, raw combined output, the preserved failed harness attempt, and post-repair receipts.

## Standing boundary

This record does not admit a successor release. It establishes only the recorded result for this bounded package and population in the preserved execution environment.

**Next gate:** preserve a separate recomputation of this repaired package before any successor release admission.

No general correctness, failure-surface completeness, production readiness, truth, authority, compliance, or stronger independence property is established.
