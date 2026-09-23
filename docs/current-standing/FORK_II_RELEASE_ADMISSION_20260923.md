# Fork II v0.1 bounded release admission — 2026-09-23

**Subject:** `FORK-II-KERNEL-002 v0.1`  
**Classification:** `BOUNDED_SUCCESSOR_RELEASE_ADMISSION`  
**Effective:** on merge of the release-admission PR

This standing note binds the successor's release-admission coordinate after the separately admitted pre-repair opening, expected pre-repair failures, frozen controls, successor-only repair, gate-4 post-repair execution, and separate recomputation.

## Bound release evidence

The admission directory is `admissions/FORK-II-KERNEL-002/v0.1-BOUNDED-RELEASE-ADMISSION/`.

It binds:

- repaired package identity: `FORK-II-KERNEL-002-EXECUTABLE-PROBE-v0.1-POST-REPAIR-20260923.zip`, 56,826 bytes, SHA-256 `77b7e7691c6f683b43482019e3f90cb6366a21524714255b67a6da3cf33c3108`, through the already-admitted gate-4 package binding;
- the already-admitted gate-4 execution receipt, recording `22/22` predecessor baseline, `26/26` FII fixtures, `13/13` frozen controls, `39/39` combined, `12/12` predecessor mutants detected, and `8/8` targeted successor faults detected;
- the supplied separate recomputation receipts, which verified `46/46` manifest-listed records and `22/22` predecessor fixture hashes and reproduced the same bounded execution result;
- exact recomputed raw bytes preserved in `sources/recomputed_raw-preserved.zip`; its `recomputed_raw.json` member is 144,185 bytes, SHA-256 `5a2f828a3a715d1a8d1d9ff35f71fcb5afbc695536c72b435b9a314688eb4b22`, and is byte-identical to the bundled combined-execution raw record;
- all three Attempt 001 harness-construction records preserved in `sources/attempt-001-negative-evidence.zip`, including empty stdout and raw stderr.

The admission does not claim a second repository-resident copy of the full repaired package ZIP at this coordinate. The release subject is the package identified by the existing gate-4 hash/length binding.

## Independence boundary

The recomputation is a separate execution of the same supplied implementation and frozen inputs. It does not establish an independently implemented semantic oracle, independent human authorship, or another stronger independence property by implication.

## Release effect

On merge, the hash-bound repaired successor identified above is admitted as the bounded `FORK-II-KERNEL-002 v0.1` research release.

The release admission does not rewrite the predecessor, the pre-repair failure record, the control freeze, the gate-4 post-repair record, or Attempt 001. Later repair, fixture/control/oracle change, or semantic expansion does not inherit into this release by adjacency and requires a separately identified successor/version or an explicit amendment preserving this coordinate.

## Non-claims

This admission does not establish general correctness, completeness of the failure surface, production readiness, deployment authority, truth, safety, compliance, institutional adoption, or a stronger recomputation-independence class than the evidence separately supports.
