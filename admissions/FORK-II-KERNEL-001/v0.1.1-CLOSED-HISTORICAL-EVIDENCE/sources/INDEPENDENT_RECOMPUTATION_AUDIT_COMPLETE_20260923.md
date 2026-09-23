# Independent Recomputation Audit — Complete

**Date:** 2026-09-23  
**Subject:** `FORK-II-KERNEL-001-EXECUTABLE-PROBE-v0.1.1.zip`  
**Disposition:** `FRESH_SUBJECT_EXECUTION_REPRODUCES_RECORDED_RESULTS`

## Direct subject identity

- Archive bytes: **70,171**
- SHA-256: `a9c18311043c505137eaece9db6b72b9b186be33a8970df48d3fe5800d1de760`
- ZIP compressed-data test: **PASS**
- Internal manifest: **63/63 entries verified; 0 mismatches**
- Post-execution manifest: **63/63 still verified; 0 mismatches**
- FII-01..FII-18 identity against preserved v0.1 manifest: **18/18 exact hash/size matches**

## Fresh execution

Environment: **Debian GNU/Linux 13 (trixie)**, kernel `6.18.44`, `x86_64`, **CPython 3.13.5**, glibc **2.41**.

- Baseline harness: **PASS — 22/22 fixtures** (exit 0).
- Unit suite: **PASS — 7/7 tests** (exit 0).
- Baseline with warnings elevated to errors: **PASS** (exit 0, empty stderr).
- Deliberate mutants: **12/12 detected**; every mutant exited non-zero.

### Fresh mutant failure pattern

| Mutant | Fresh result | Failed fixture(s) | Matches preserved comparison |
|---|---:|---|---:|
| `eligibility_authorization` | 21/22 pass; exit 1 | FII-01 | YES |
| `scope_globality` | 21/22 pass; exit 1 | FII-03 | YES |
| `false_negation` | 21/22 pass; exit 1 | FII-04 | YES |
| `automatic_license` | 20/22 pass; exit 1 | FII-05, FII-13 | YES |
| `historical_rewrite` | 20/22 pass; exit 1 | FII-14, FII-16 | YES |
| `authority_infects_evidence` | 21/22 pass; exit 1 | FII-17 | YES |
| `force_total_order` | 21/22 pass; exit 1 | FII-18 | YES |
| `stale_reuse` | 20/22 pass; exit 1 | FII-14, FII-15 | YES |
| `mutable_profile_reference` | 21/22 pass; exit 1 | FII-19 | YES |
| `historical_disposition_promoted_to_correctness` | 21/22 pass; exit 1 | FII-20 | YES |
| `unbound_dependency_snapshot` | 21/22 pass; exit 1 | FII-21 | YES |
| `null_effective_until_promoted_to_indefinite_validity` | 21/22 pass; exit 1 | FII-22 | YES |

The failed-fixture set matches `CROSS-ENVIRONMENT-RECOMPUTATION-COMPARISON-001.json` for **all 12 mutants**.

## Receipt recomputation

- Fresh baseline receipt is **byte-for-byte identical** to the packaged `BASELINE_RECEIPT.json`.
- For **all 12 mutant receipts**, the parsed JSON is identical to the packaged receipt.
- For **all 12 mutant receipts**, the fresh deterministic bytes differ only by one byte: appending a single terminal LF (`0x0A`) makes the fresh bytes exactly equal to the packaged bytes.
- Therefore the previously recorded receipt-serialization asymmetry is independently reproduced from the supplied subject archive.

## Relationship to the preserved comparison record

This fresh run is a new execution instance. Its software-version signature matches the preserved `RECOMPUTATION-CHATGPT-001` environment (Debian 13 / CPython 3.13.5 / glibc 2.41). It also matches the preserved, distinct `RECOMPUTATION-CLAUDE-001` result from Ubuntu 24.04.4 / CPython 3.12.3 / glibc 2.39. Thus the earlier cross-environment observation is now additionally backed by direct access to—and fresh execution of—the frozen subject bytes.

## Claim boundary

This audit independently verifies archive identity/integrity and reproduces the behavior of the supplied reference implementation on its frozen synthetic fixture population. It is **execution-level recomputation of the same implementation**, not an independently written implementation or an external proof of the semantics. It does not establish general correctness, platform independence, completeness of the mutant/failure surface, semantic completeness of CANON-v1, production safety, truth, authority, compliance, or operational safety.
