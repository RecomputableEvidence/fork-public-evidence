# Independent Recomputation — FORK-II-KERNEL-001 v0.1.1

- Source ZIP SHA-256: `a9c18311043c505137eaece9db6b72b9b186be33a8970df48d3fe5800d1de760`
- Manifest: **63/63** hash and byte-size matches; no manifest mismatch observed.
- FII-01..FII-18 regression identity: **18/18 byte matches** against preserved v0.1 manifest.
- Baseline: **22/22 PASS**.
- Bundled unit tests: **7/7 PASS**.
- Deliberate mutants: **12/12 detected**.
- Fresh baseline receipt equals shipped receipt: **true**.
- Fresh mutant receipts equal shipped receipts: **12/12**.

## Additional adversarial probes reproduced

1. `immutable` can change without changing the CANON-v1 profile hash; with otherwise identical canonical fields the evaluator returns `referent_integrity=ESTABLISHED`, `historical_reuse_permitted=true`, `current_use_status=CURRENT`.
2. Dependency-record hash values can all be the literal `not-a-hash`; after recomputing the snapshot self-hashes, the checker reports no binding issues and classifies the snapshot `REPRODUCIBLY_BOUND`.
3. `FIXED_TIME` with `effective_until=2000-01-01T00:00:00Z` remains `current_use_status=CURRENT`; no evaluation-time comparison is performed.
4. `UNKNOWN` with null end remains `current_use_status=CURRENT`.

## Disposition

**PASS under the frozen v0.1.1 admission boundary.** The four adversarial findings are outside the frozen fixture population and therefore do not falsify the admitted v0.1.1 claim. They are bounded successor-surface candidates.

## Claim boundary

This recomputation establishes deterministic behavior of the supplied synthetic artifact under the documented execution path in this environment. It does not establish general correctness, truth, authority, compliance, production safety, real-workflow representativeness, completeness of the failure surface, or external provenance beyond the supplied archive identity.
