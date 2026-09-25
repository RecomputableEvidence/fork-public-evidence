# QSA-001 v0.1 Remaining Adversarial Pressure Plan 001

Status: FROZEN_BEFORE_EXECUTION

## Target

- Target branch: `research/qsa-001-v0.1-freeze-reference`
- Conceptual freeze commit: `704b1da5d999d6130dacd6691c768fe6904e970f`
- Frozen reference implementation commit: `d18119105481d194298148a31715303c77a244bc`
- Frozen reference tree: `e865f17a749e5b8f931b0ca5145a0fc71b9dbde9`
- Target mutability: NONE
- Baseline rewrite: PROHIBITED
- Pre-execution repair: PROHIBITED
- Force update: PROHIBITED

Every probe MUST operate on an isolated derivative of the exact frozen reference package. No probe may inherit mutation state from another probe.

```text
READ_ONLY_FROZEN_BASELINE
→ A3_ISOLATED_COPY
→ A4_ISOLATED_COPY
→ A5_ISOLATED_COPY
→ A6_ISOLATED_COPY
→ A7_ISOLATED_COPY
→ A8_ISOLATED_COPY
→ A9_ISOLATED_COPY
→ A10_ISOLATED_COPY
```

## Frozen expected outcomes

| ID | Mutation | Expected result | Required bounded finding |
| --- | --- | --- | --- |
| A3 | Replay a valid signature under another QSA object domain/type. | MUST_REJECT | DOMAIN_SEPARATOR_MISMATCH or signature verification failure |
| A4 | Alter canonical successor `parent_state_hash` without a matching successor relation. | MUST_REJECT | PARENT_STATE_BINDING_FAILURE or equivalent parent/hash non-pass |
| A5 | Alter implemented successor state material while leaving build mark and adoption materials unchanged. | MUST_REJECT | BUILD_MARK_BINDING_FAILURE or successor-state/hash mismatch |
| A6 | Make the relevant qualification expired or revoked before declared adoption time. | MUST_REJECT under declared policy | QUALIFICATION_NOT_VALID_AT_ADOPTION or equivalent qualification non-pass |
| A7 | Attempt adoption from a parent that is no longer the current canonical state. | MUST_REJECT | STALE_PARENT_NOT_CURRENTLY_ADOPTABLE or equivalent adoption-ordering non-pass |
| A8 | Declare a lower change class while changing protected/constitutional material. | MUST_REJECT or ELEVATED_ROUTE_REQUIRED | CHANGE_CLASS_MISMATCH / CONSTITUTIONAL_ROUTE_REQUIRED or equivalent route non-pass |
| A9 | Remove the inspection receipt or break its required binding from an otherwise adopted proposal. | MUST_REJECT | INSPECTION_BINDING_MISSING / INSPECTION_PREREQUISITE_FAILURE or equivalent inspection non-pass |
| A10 | Modify actor-identity or authority-binding evidence while leaving signed payload verification mathematically valid. | MUST_NOT_REPORT_FULL_ACTOR_OR_AUTHORITY_BINDING_PASS | ACTOR_BINDING_FAILURE, AUTHORITY_BINDING_FAILURE, UNVERIFIABLE, or equivalent bounded non-pass |

## A10 boundary

A10 MUST NOT require a false cryptographic failure when the relevant signature still verifies.

```text
SIGNATURE_VALID = POSSIBLE
ACTOR_IDENTITY_BINDING = FAIL_OR_UNVERIFIABLE
ACTOR_AUTHORITY_BINDING = FAIL_OR_UNVERIFIABLE

SIGNATURE_VALIDITY != ACTOR_IDENTITY
SIGNATURE_VALIDITY != ACTOR_AUTHORITY
```

## Per-probe evidence

Each execution record SHOULD preserve:

- PROBE_ID
- TEST_PLAN_ID
- TEST_PLAN_HASH
- REFERENCE_COMMIT
- REFERENCE_TREE_HASH
- ISOLATED_COPY_ID
- MUTATION_DESCRIPTION
- MUTATED_PATHS
- PRE_MUTATION_HASHES
- POST_MUTATION_HASHES
- EXPECTED_RESULT
- ACTUAL_RESULT
- VERIFIER_COMMAND
- EXIT_CODE
- STDOUT_HASH
- STDERR_HASH
- VERIFICATION_RECEIPT_HASH where produced
- ENVIRONMENT_RECEIPT_HASH
- EXPECTATION_MATCH
- ANOMALIES

## Failure handling

```text
OBSERVED_FAILURE
→ PRESERVE_FIRST

OBSERVED_FAILURE
!= IMMEDIATE_REPAIR_AUTHORIZATION
```

A mismatch establishes only a bounded implementation result with respect to the exact probe and invariant. It does not authorize modification of the frozen reference implementation.

## Post-execution routing

After A3-A10 are executed, preserve `QSA-001-v0.1-REMAINING-ADVERSARIAL-PRESSURE-RETURN-001`, then derive `QSA-001-v0.1-REFERENCE-PRESSURE-DISPOSITION-001` without rewriting this plan, the frozen reference implementation, or prior exterior returns.
