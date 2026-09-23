# FORK-II-KERNEL-002 v0.1 — bounded release admission

**Status:** BOUNDED SUCCESSOR RELEASE ADMISSION  
**Date:** 2026-09-23  
**Historical effect:** None on predecessor evidence or earlier successor records

This admission binds the repaired successor package identity, the already-admitted gate-4 execution receipt, the supplied separate recomputation receipt, exact recomputed raw bytes preserved inside a transport ZIP, and the complete Attempt 001 negative evidence preserved inside a second transport ZIP. Earlier records are not rewritten.

## Repaired package identity

`FORK-II-KERNEL-002-EXECUTABLE-PROBE-v0.1-POST-REPAIR-20260923.zip`

- SHA-256: `77b7e7691c6f683b43482019e3f90cb6366a21524714255b67a6da3cf33c3108`
- Bytes: `56826`
- Gate-4 binding: `docs/experiments/FORK-II-KERNEL-002/v0.1-REPAIR/PACKAGE_BINDING.json`

The package identity is admitted by exact hash/length binding to the already-admitted gate-4 record. This release-admission coordinate does not claim a second repository-resident copy of the full repaired ZIP.

## Gate-4 execution

The primary gate-4 receipt remains at `docs/experiments/FORK-II-KERNEL-002/v0.1-REPAIR/execution/POST_REPAIR_EXECUTION_RECEIPT.json` (Git blob `f58d22305da72f83b9831bae54632ac51c76b540`, SHA-256 `9e9b2f74e718486e3b74f9165be61e35508bff3d7832f84236e46f2755470783`). It records 22/22 predecessor baseline, 26/26 FII fixtures, 13/13 frozen controls, 39/39 combined, 12/12 predecessor mutants detected, and 8/8 targeted successor faults detected.

## Separate recomputation

The supplied JSON and Markdown receipts are preserved under `sources/`. They bind the same repaired-package SHA-256 and report the same bounded result.

The exact recomputed raw JSON is preserved as `sources/recomputed_raw-preserved.zip`. The ZIP itself hashes to `c49f4e3c0269fabc1dd2e825b27142741219381bede61374d0d063b503f71f85`; its sole member is `recomputed_raw.json`, 144185 bytes, SHA-256 `5a2f828a3a715d1a8d1d9ff35f71fcb5afbc695536c72b435b9a314688eb4b22`. That member is byte-identical to the bundled `receipts/raw/combined_execution_raw.json` according to the separate recomputation receipt.

This is a separate execution of the same supplied implementation and frozen inputs. It is not an independently implemented semantic oracle and no stronger independence property is inherited.

## Attempt 001 negative evidence

The complete Attempt 001 material is additionally preserved as `sources/attempt-001-negative-evidence.zip`, SHA-256 `ffccefd583ba3124dc7b912a4920c97f2d53282c16be058f0480df9016ead130`.

Its members are the same three negative-evidence records preserved in the repaired package:

- `ATTEMPT_DISPOSITION.md` — 1016 bytes — `873bce361868f0420f4a353a08f07710cbd2d050f9f4755453ad30876281d30a`
- `unittest_stdout.txt` — 0 bytes — `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `unittest_stderr.txt` — 87149 bytes — `6eae601c28b789b96fc65fc9317924f32711469a2a3ff4b128e6bede12366281`

Attempt 001 remains a harness-construction failure. It is not normalized into Attempt 002 or promoted to a successful run.

## Admission effect

On merge, the repaired package identified above is admitted as the bounded `FORK-II-KERNEL-002 v0.1` research release, supported by the preserved gate-4 execution and the separate recomputation record.

No later change inherits into this release by adjacency. Further repair, fixture/control/oracle change, or semantic expansion requires a separately identified successor/version or an explicit amendment preserving this coordinate.

## Non-claims

Release admission does not establish general correctness, failure-surface completeness, production readiness, deployment authority, truth, safety, compliance, institutional adoption, or any stronger recomputation-independence property than the evidence separately establishes.
