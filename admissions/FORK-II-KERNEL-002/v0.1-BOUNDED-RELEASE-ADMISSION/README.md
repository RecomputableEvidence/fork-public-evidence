# FORK-II-KERNEL-002 v0.1 — bounded release admission

**Status:** BOUNDED SUCCESSOR RELEASE ADMISSION  
**Date:** 2026-09-23  
**Historical effect:** None on predecessor evidence or earlier successor records

This admission binds the exact repaired successor package, the already-admitted gate-4 execution receipt, the supplied separate recomputation receipt and recomputed raw bytes, and the complete Attempt 001 negative evidence preserved inside the package. Earlier records are not rewritten.

## Exact release package

`FORK-II-KERNEL-002-EXECUTABLE-PROBE-v0.1-POST-REPAIR-20260923.zip`

- SHA-256: `77b7e7691c6f683b43482019e3f90cb6366a21524714255b67a6da3cf33c3108`
- Bytes: `56826`
- Exact package bytes are admitted under `sources/` at this coordinate.

## Gate-4 execution

The primary gate-4 receipt remains at `docs/experiments/FORK-II-KERNEL-002/v0.1-REPAIR/execution/POST_REPAIR_EXECUTION_RECEIPT.json` (Git blob `f58d22305da72f83b9831bae54632ac51c76b540`). It records 22/22 predecessor baseline, 26/26 FII fixtures, 13/13 frozen controls, 39/39 combined, 12/12 predecessor mutants detected, and 8/8 targeted successor faults detected.

## Separate recomputation

The supplied receipt is preserved unchanged under `sources/`. It binds the same package SHA-256 and reports the same bounded result. `sources/recomputed_raw.json` hashes to `5a2f828a3a715d1a8d1d9ff35f71fcb5afbc695536c72b435b9a314688eb4b22` and is byte-identical to the bundled `receipts/raw/combined_execution_raw.json`.

This is a separate execution of the same supplied implementation and frozen inputs. It is not an independently implemented semantic oracle and no stronger independence property is inherited.

## Attempt 001 negative evidence

The admitted ZIP preserves all three raw Attempt 001 records unchanged:

- `FORK-II-KERNEL-002-EXECUTABLE-PROBE-v0.1/receipts/raw/attempt-001-harness-construction/ATTEMPT_DISPOSITION.md` — `873bce361868f0420f4a353a08f07710cbd2d050f9f4755453ad30876281d30a`
- `FORK-II-KERNEL-002-EXECUTABLE-PROBE-v0.1/receipts/raw/attempt-001-harness-construction/unittest_stdout.txt` — `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `FORK-II-KERNEL-002-EXECUTABLE-PROBE-v0.1/receipts/raw/attempt-001-harness-construction/unittest_stderr.txt` — `6eae601c28b789b96fc65fc9317924f32711469a2a3ff4b128e6bede12366281`

Attempt 001 remains a harness-construction failure. It is not normalized into Attempt 002 or promoted to a successful run.

## Admission effect

On merge, this exact package is admitted as the bounded `FORK-II-KERNEL-002 v0.1` research release. The admission is supported by the preserved gate-4 execution and the separate recomputation record.

No later change inherits into this release by adjacency. Further repair, fixture/control/oracle change, or semantic expansion requires a separately identified successor/version or an explicit amendment preserving this coordinate.

## Non-claims

Release admission does not establish general correctness, failure-surface completeness, production readiness, deployment authority, truth, safety, compliance, institutional adoption, or any stronger recomputation-independence property than the evidence separately establishes.
