# FORK-II-KERNEL-002 v0.1 — separate recomputation receipt

**Record ID:** `FORK-II-KERNEL-002-v0.1-SEPARATE-RECOMPUTATION-20260923-001`  
**Date:** `2026-09-23`  
**Classification:** `SEPARATE_RECOMPUTATION_BOUNDED_PASS`  
**Input archive SHA-256:** `77b7e7691c6f683b43482019e3f90cb6366a21524714255b67a6da3cf33c3108`

## Result

- Manifest-listed files verified: **46/46**
- Frozen predecessor fixture hashes verified: **22/22**
- Unit-test groups: **8/8 PASS**
- FII-01–FII-22 baseline: **22/22 PASS**
- FII-01–FII-26: **26/26 PASS**
- Frozen controls: **13/13 PASS**
- Combined population: **39/39 PASS**
- Predecessor mutants detected: **12/12**
- Targeted successor fault reintroductions detected: **8/8**
- Overall: **PASS**

## Reproduction check

The newly generated raw execution output is **byte-identical** to the bundled `receipts/raw/combined_execution_raw.json`.

- Recomputed raw SHA-256: `5a2f828a3a715d1a8d1d9ff35f71fcb5afbc695536c72b435b9a314688eb4b22`
- Bundled raw SHA-256: `5a2f828a3a715d1a8d1d9ff35f71fcb5afbc695536c72b435b9a314688eb4b22`

## Scope

This is a separate execution/recomputation of the supplied artifact and frozen inputs. It is not an independently implemented semantic oracle. The result is bounded to the supplied fixture/control/mutant population and does not establish general correctness, completeness, production readiness, truth, authority, compliance, or release admission.
