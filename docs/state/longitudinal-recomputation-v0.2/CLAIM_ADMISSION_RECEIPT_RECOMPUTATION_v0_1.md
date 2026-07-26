# Claim-Admission Self-Check Receipt Recomputation v0.1

**Correction class:** `MECHANICAL_CURRENT_TREE_RECEIPT_RECOMPUTATION`

## Predecessor condition

At exact branch base
`f955834681d2f2ee257276acbf68afde0ae0e69d`, the committed claim-admission
self-check receipt recorded `tree_entry_count: 1660`. Recomputing after the
longitudinal candidate files were staged produced a different tracked-tree
entry count.

The mismatch was observed by the full regression test
`test_committed_self_check_receipt_matches_current_checker_output`. The
candidate did not reinterpret the failed comparison as a defect in the
claim-admission checker or as an admission failure.

## Successor response

The existing consumer-owned checker regenerates:

- `receipts/claim-admission/FORK_CLAIM_ADMISSION_HARDENING_SELF_CHECK_RECEIPT_v0_1.json`

with `--self-check --write-receipt` after every intended candidate file is
staged. The regenerated receipt remains:

- `REVIEW_ELIGIBLE_NOT_ADMITTED`;
- local self-check only;
- candidate checkout `NONE`;
- candidate code execution `NONE`;
- repository-setting effect `NONE`;
- admission effect limited to the checker's declared structural result.

## Non-effects

This mechanical receipt update does not admit, approve, publish, merge,
authorize, certify, execute, or change Pair-001. It performs zero provider
calls and grants no retry, readiness, or execution authority.
