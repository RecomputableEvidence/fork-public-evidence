# Disposition rules v0.1.1

Precedence is material failure → incomplete → minor defect → success.

## Success
`REPRODUCED_WITHIN_DECLARED_SYNTHETIC_SCOPE`

Exact target identity, frozen integrity, fixtures, tests, and mutation boundaries all pass with no recorded minor defect.

## Success with minor defects
`REPRODUCED_WITHIN_DECLARED_SYNTHETIC_SCOPE_WITH_MINOR_DEFECTS`

Core recomputation passes, but one or more bounded procedural or packaging defects are explicitly recorded and do not alter target identity or computed fixture/test results.

## Incomplete
`EXTERIOR_RECOMPUTATION_INCOMPLETE`

Acquisition, environment, dependency, permission, or reviewer-scope conditions prevent completion. This is not package failure.

## Material failure
`EXTERIOR_RECOMPUTATION_FAILED`

Exact target identity, archive integrity, frozen manifest, required fixture/test results, or declared mutation boundaries fail.

Tool exit codes: success `0`; success with minor defects `2`; incomplete `3`; material failure `1`.
