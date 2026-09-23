# Fork II KERNEL-002 v0.1 — pre-repair control freeze — 2026-09-23

Ordered gate 3 of `FORK-II-KERNEL-002 v0.1` is complete at this coordinate: the successor control population is defined and byte-frozen before any implementation repair.

The frozen control object is under `docs/experiments/FORK-II-KERNEL-002/v0.1-PRE-REPAIR/controls/v0.1-FROZEN/` and contains:

- `CONTROL_PROTOCOL.md` — SHA-256 `4c550bd12fdce6ea9e65f64a3158ea67988ed534729d123587eb6e56b12aba23`;
- `CONTROL_POPULATION.json` — SHA-256 `64bfdae05599402fd24fdbbd05b7d3312dc02c0e28f26c3e2685ec36134e4287`;
- `CONTROL_FREEZE_RECORD.json` — SHA-256 `2691ddee11ed3f102c9b2b09d4999eda2f01b884e0f97ad39975f39ea7aa59c5`;
- `SHA256SUMS.txt` binding those three files.

The population contains 13 controls: one unchanged-immutable profile identity positive control; four dependency-binding controls covering fully bound bytes, missing bytes, malformed digest format, and well-shaped incorrect digest; and eight temporal controls covering in-range, exact-end, pre-start, malformed interval, reversed interval, missing evaluation time, malformed evaluation time, and UNKNOWN/null behavior.

The dependency-byte contract is explicit: the frozen corpus values are exact text and their record bytes are exactly UTF-8 encoding of those values, without newline, BOM, parsing, normalization, or reserialization. Per-record digest validation is distinct from CANON-v1 enclosing snapshot hashes.

The temporal contract is explicit: fixed intervals are half-open; the wall clock is not an implicit input; missing or malformed evaluation time cannot establish current use; malformed or reversed intervals cannot establish an effective period; UNKNOWN/null does not establish current validity.

No predecessor or successor implementation byte is changed by this freeze. The controls have not been executed. No repair is claimed. No FII-23–FII-26 oracle is changed.

The next ordered Fork II gate is successor-only repair against the already frozen evidence: preserve FII-01–FII-22 baseline expectations and all 12 predecessor mutant detections; require FII-23–FII-26 plus this 13-control population; and use targeted fault reintroductions to show each new oracle detects its intended behavior.

This standing note is a routing and preservation statement only. It does not establish control-surface completeness, general correctness, production readiness, truth, authority, compliance, portability, or correctness of a future repair.
