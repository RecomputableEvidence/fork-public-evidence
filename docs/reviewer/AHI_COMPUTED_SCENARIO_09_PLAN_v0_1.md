# AHI Computed Scenario 09 Plan v0.1

## Working title

Scenario 09 v0.2 - Computed Revocation Visibility / Split-State Boundary

## Purpose

Computed Scenario 09 v0.2 should demonstrate that a revocation visibility or split-state consumption gap can be derived from independent System A/B/C state inputs.

This is a maturity step beyond the current authored fixture consistency checks.

## Current Scenario 09 v0.1

Current Scenario 09 v0.1 records the failure mode:

```text
recorded_in_A does not imply visible_in_B
visible_in_B does not imply consumed_by_C
not_visible_locally does not imply still_valid_currently
```

Current checker posture:

- required files exist;
- JSON parses;
- expected authored fields match expected literal values;
- non-claim vocabulary is present;
- selected overclaim phrases are absent.

This is fixture consistency verification.

## Computed Scenario 09 v0.2 target

The v0.2 checker should derive the boundary classification from independent inputs.

The checker should not trust a pre-authored `REVOCATION_VISIBILITY_GAP` label as the source of truth. It should compute whether that label follows from state divergence.

## Candidate input model

### System A - source of truth

File:

```text
examples/simulations/governance-proof-surface/computed/scenario_09_v0_2/system_a_revocation_state.json
```

Candidate fields:

```json
{
  "system_id": "SYSTEM_A",
  "authority_state_id": "AUTHZ-001",
  "subject_id": "SUBJECT-001",
  "validity_state": "REVOKED",
  "validity_changed_at": "2026-01-15T10:00:00Z",
  "change_type": "REVOCATION",
  "source_of_truth": true
}
```

### System B - visibility or synchronization state

File:

```text
examples/simulations/governance-proof-surface/computed/scenario_09_v0_2/system_b_visibility_state.json
```

Candidate fields:

```json
{
  "system_id": "SYSTEM_B",
  "observed_subject_id": "SUBJECT-001",
  "last_successful_sync_at": "2026-01-15T09:30:00Z",
  "known_validity_state": "VALID",
  "revocation_visible_at_reliance_time": false,
  "source_system": "SYSTEM_A"
}
```

### System C - reliance attempt

File:

```text
examples/simulations/governance-proof-surface/computed/scenario_09_v0_2/system_c_reliance_attempt.json
```

Candidate fields:

```json
{
  "system_id": "SYSTEM_C",
  "relied_subject_id": "SUBJECT-001",
  "reliance_attempted_at": "2026-01-15T10:45:00Z",
  "state_consumed_from": "SYSTEM_B",
  "consumed_validity_state": "VALID",
  "current_revalidation_performed": false
}
```

### Freshness or tolerance policy

File:

```text
examples/simulations/governance-proof-surface/computed/scenario_09_v0_2/freshness_tolerance_policy.json
```

Candidate fields:

```json
{
  "policy_id": "FRESHNESS-POLICY-001",
  "max_visibility_lag_seconds": 300,
  "max_consumption_lag_seconds": 300,
  "tolerance_result_is_authorization": false,
  "fork_may_decide_acceptability": false
}
```

## Derived result model

File:

```text
examples/simulations/governance-proof-surface/computed/scenario_09_v0_2/derived_gap_result.json
```

Candidate fields:

```json
{
  "derived_by": "scripts/check_scenario_09_computed_revocation_visibility_v0_2.ps1",
  "derived_classification": "REVOCATION_VISIBILITY_GAP_RECORDED",
  "visibility_gap_seconds": 2700,
  "consumption_gap_seconds": 2700,
  "gap_exceeds_declared_tolerance": true,
  "current_revalidation_required": true,
  "fork_result": "BOUNDARY_GAP_DERIVED_NOT_AUTHORIZED",
  "fork_does_not_establish": [
    "global visibility",
    "global consumption",
    "current validity",
    "current authority",
    "approval",
    "compliance",
    "legal sufficiency",
    "negligence",
    "excuse",
    "correctness",
    "execution eligibility"
  ]
}
```

## Checker behavior

The checker should:

1. Load System A, System B, System C, and policy inputs.
2. Confirm all timestamps parse as UTC.
3. Confirm all subject identifiers align or record a subject mismatch.
4. Compute whether System A changed validity before System C relied.
5. Compute whether System B had visibility after the validity change and before the reliance attempt.
6. Compute whether System C consumed a state that reflects the System A change.
7. Compute visibility lag and consumption lag.
8. Compare lag to declared tolerance.
9. Emit or verify a derived result.
10. Reject any output that converts the gap into approval, compliance, legal sufficiency, fault, excuse, or execution eligibility.

## Required test fixtures

Computed Scenario 09 v0.2 should include at least these fixtures:

1. `valid_no_gap`
2. `valid_gap_within_tolerance`
3. `valid_visibility_gap_exceeds_tolerance`
4. `valid_consumption_gap_exceeds_tolerance`
5. `invalid_gap_labeled_without_derivation`
6. `invalid_gap_converted_to_authorization`

## Main checker integration

The computed checker should be invoked by:

```text
scripts/run_ahi_sim_v0_1_checks.ps1
```

The scenario registry should distinguish:

```text
SEMANTICALLY_VERIFIED_AUTHORED_FIXTURE
```

from:

```text
COMPUTED_TRANSITION_DERIVATION
```

or equivalent wording that does not overstate the current v0.1 posture.

## Relationship to Scenario 10

Computed Scenario 09 v0.2 should define gap derivation.

Scenario 10 should define gap closure evidence.

Scenario 10 should not decide fault. It should distinguish:

```text
notification
receipt
consumption
reconciliation
authorization
```

The core invariant should be:

```text
notification does not imply receipt
receipt does not imply consumption
consumption does not imply reconciliation
reconciliation does not imply authorization
```

## Success criteria

Computed Scenario 09 v0.2 succeeds when:

- the gap classification is computed from independent inputs;
- the checker rejects unsupported labels;
- the checker distinguishes visibility gap from consumption gap;
- the checker records tolerance posture without deciding acceptability;
- the checker preserves Fork's non-authority boundary.
