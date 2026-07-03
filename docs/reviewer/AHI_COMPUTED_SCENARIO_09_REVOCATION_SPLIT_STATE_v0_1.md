# AHI Computed Scenario 09 Revocation Split-State v0.1

## Reviewer purpose

This implementation adds a computed derivation path for Scenario 09.

The reviewer concern was that prior Scenario 09 fixtures recorded the split-state condition, but did not compute the condition from independent system state. This package introduces independent state inputs and a deterministic derivation checker.

## State inputs

Each case contains four independent inputs:

```text
system_a_current_revocation_state.json
system_b_visibility_sync_state.json
system_c_consumption_attempt_state.json
freshness_policy.json
```

The derivation script computes the output and compares it with:

```text
expected_derived_result.json
```

## Case 01: visibility_gap_detected

System A records a current revocation before System C attempts downstream reliance.

System B has not synchronized after the revocation event and does not visibly contain the revocation identifier.

System C attempts to consume the earlier claim while seeing a still-valid local basis.

The derived result records:

```text
COMPUTED_GAP_RECORDED
REVOCATION_VISIBILITY_GAP
SPLIT_STATE_CONSUMPTION_GAP
CURRENT_REVALIDATION_REQUIRED
```

## Case 02: gap_closed_by_revalidation

System B has synchronized after the revocation event and visibly contains the revocation identifier.

System C records revalidation after the synchronized state became available.

The derived result records:

```text
NO_COMPUTED_GAP_RECORDED
```

This is not a safety, compliance status, correctness, or legal conclusion. It only means the supplied fixture state does not exhibit the computed split-state gap under the supplied freshness policy.

## Non-claims

This implementation does not decide:

- whether downstream action is permitted;
- whether reliance has legal sufficiency;
- whether any party had fault;
- whether the underlying claim was true;
- whether a policy was correctly interpreted;
- whether the workflow satisfies a compliance status requirement;
- whether execution should be allowed.

It only computes a bounded state-divergence classification from supplied fixtures.
