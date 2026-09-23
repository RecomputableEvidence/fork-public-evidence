# FORK-II-KERNEL-002 v0.1 — post-repair combined execution receipt

**Record ID:** `FORK-II-KERNEL-002-v0.1-POST-REPAIR-EXECUTION-001`  
**Date:** `2026-09-23`  
**Classification:** `SUCCESSOR_ONLY_REPAIR_EXECUTED_BOUNDED_PASS`  
**Repair scope:** successor only

## Result

- FII-01–FII-22 baseline: **22/22 PASS**
- FII-01–FII-26: **26/26 PASS**
- frozen controls: **13/13 PASS**
- combined population: **39/39 PASS**
- predecessor mutants detected: **12/12**
- targeted successor fault reintroductions detected: **8/8**
- overall: **PASS**

No predecessor byte, frozen fixture, frozen control, or CANON-v1 definition was changed by the repair.

## Repair branches

1. profile `immutable` integrity is enforced separately from CANON-v1 hashing;
2. dependency hash syntax is validated and supplied frozen record bytes are verified against exact UTF-8 SHA-256 digests;
3. valid fixed intervals are evaluated against explicit `request.evaluation_time` using half-open interval semantics;
4. `UNKNOWN` end state does not establish current validity.

## Targeted fault reintroductions
- `successor_ignore_immutable`: **DETECTED** by FII-23; failed records: FII-23.
- `successor_accept_missing_dependency_bytes`: **DETECTED** by CTRL-BIND-002; failed records: CTRL-BIND-002.
- `successor_accept_malformed_digest`: **DETECTED** by FII-24, CTRL-BIND-003; failed records: FII-24, CTRL-BIND-003.
- `successor_skip_dependency_digest_match`: **DETECTED** by CTRL-BIND-004; failed records: CTRL-BIND-004.
- `successor_ignore_fixed_time_position`: **DETECTED** by FII-25, CTRL-TIME-002, CTRL-TIME-003; failed records: FII-25, CTRL-TIME-002, CTRL-TIME-003.
- `successor_accept_invalid_fixed_interval`: **DETECTED** by CTRL-TIME-004, CTRL-TIME-005; failed records: CTRL-TIME-004, CTRL-TIME-005.
- `successor_default_invalid_evaluation_current`: **DETECTED** by CTRL-TIME-006, CTRL-TIME-007; failed records: CTRL-TIME-006, CTRL-TIME-007.
- `successor_unknown_end_current`: **DETECTED** by FII-26, CTRL-TIME-008; failed records: FII-26, CTRL-TIME-008.

## Historical mutant preservation

All 12 predecessor mutants remain detected by the successor population. Some historical mutants also fail additional successor fixtures/controls; that does not rewrite their predecessor witness population.

## Preserved negative attempt

Attempt 001 is retained as a harness-construction failure. It did not modify the repair implementation or frozen inputs. Attempt 002 changed only the test/receipt harness and produced the result above.

## Next gate

Preserve the repaired package/raw outputs and obtain a separate recomputation before any successor release admission.

## Non-claims

This receipt does not establish general correctness, completeness, production readiness, truth, authority, compliance, or release admission.
