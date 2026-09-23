# FORK-II-KERNEL-002 control protocol v0.1

**Status:** FROZEN PRE-REPAIR CONTROL PROTOCOL  
**Historical effect:** None  
**Repair performed:** No

## Purpose

This protocol freezes the control population required by ordered gate 3 of `FORK-II-KERNEL-002 v0.1` before any successor implementation repair. Controls are distinct from FII-23–FII-26. They bound expected non-defect, negative, and temporal-boundary behavior so a repair cannot obtain credit merely by rejecting every successor input.

The frozen population contains 13 controls: one profile-identity positive control, four dependency-binding controls, and eight temporal controls. Exact inputs and oracles are in `CONTROL_POPULATION.json`. No oracle may be weakened or rewritten to make a later implementation pass; a changed oracle requires a separately preserved protocol amendment or successor control version.

## Dependency-record byte contract

`CONTROL_POPULATION.json` contains a frozen `dependency_record_corpus`. Each corpus value is exact text. Its dependency-record bytes are exactly `value.encode("utf-8")`; no newline, BOM, parsing, normalization, or reserialization is added.

For `CTRL-BIND-001` through `CTRL-BIND-004`:

1. `dependency_record_bytes.source=DEPENDENCY_RECORD_CORPUS_UTF8` selects that frozen corpus.
2. `include_ids` is the exact set of record bytes supplied to that control.
3. Dependency digests must be lowercase SHA-256 hexadecimal strings matching `^[0-9a-f]{64}$`.
4. Digest verification is `sha256(exact_utf8_record_bytes).hexdigest()` compared exactly with the corresponding `dependency_record_hashes` value.
5. Supplied byte IDs and hash-map IDs must each exactly cover the dependency IDs declared by the snapshot. Missing or extra IDs do not establish binding.
6. CANON-v1 `canonical_payload_hash` and `snapshot_hash` continue to bind snapshot structure; enclosing-hash consistency does not substitute for per-record digest-format and byte verification.

`CTRL-BIND-002` differs from the positive control only by omission of the `EA-001` record bytes. `CTRL-BIND-003` supplies all record bytes but changes the `EA-001` digest to `not-a-hash`, with enclosing CANON-v1 hashes recomputed consistently. `CTRL-BIND-004` supplies all record bytes but changes the `EA-001` digest to 64 lowercase zeroes, again with enclosing hashes recomputed consistently.

## Profile-identity control

`CTRL-ID-001` uses identical referenced and observed profiles, both with `immutable=true`, and the frozen CANON-v1 recorded content hash. Required result: `referent_integrity=ESTABLISHED`, reuse permitted, `current_use_status=CURRENT`. CANON-v1 is not redefined by this freeze; changed meaning-bearing hash inclusion requires a new canonicalization version.

## Temporal contract

For this control population, timestamp syntax is restricted to UTC RFC 3339 `YYYY-MM-DDTHH:MM:SSZ`; parsing is strict and wall clock is not an input. A valid fixed interval is half-open: `effective_from <= evaluation_time < effective_until`. In-range is `CURRENT`; before start is `NOT_YET_EFFECTIVE`; at or after end is `EXPIRED`. Missing or malformed `evaluation_time` leaves period kind `FIXED_TIME` but current use `NOT_ESTABLISHED`. Malformed interval timestamps or `effective_from >= effective_until` yield `EFFECTIVE_PERIOD_NOT_ESTABLISHED` and current use `NOT_ESTABLISHED`. `UNKNOWN` with null end remains `UNKNOWN` and current use `NOT_ESTABLISHED`.

## Freeze boundary

This freeze does not execute controls and does not modify predecessor or successor implementation bytes. It freezes inputs and acceptance oracles before repair. After admission, the next ordered gate is successor-only repair followed by execution against FII-01–FII-26, this frozen control population, and targeted fault reintroductions.

This freeze does not establish general correctness, completeness of the control surface, production readiness, truth, authority, compliance, portability, or correctness of any future repair.
