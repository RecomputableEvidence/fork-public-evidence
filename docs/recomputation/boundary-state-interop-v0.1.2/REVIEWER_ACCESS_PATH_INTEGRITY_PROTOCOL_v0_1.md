# Reviewer Access Path Integrity / Retrieval Distortion / Interpreter Compatibility Protocol v0.1

## Invariant

Content assessment is permitted only when the declared access state provides the required artifact surface and the interpreter or execution path is compatible with the claimed review action.

The checker treats these as non-content states:

- retrieval failed;
- partial artifact access where the missing scope is material;
- transformed or excerpted access where fidelity is unresolved;
- interpreter incompatibility;
- execution unavailable.

## Prohibited upgrades

The following are invalid:

- failed retrieval -> negative content finding;
- failed retrieval -> positive validation;
- partial artifact -> complete-package assessment;
- interpreter incompatibility -> package failure;
- execution unavailable -> checker failure attributed to the artifact;
- manual reconstruction -> execution of the named verifier;
- structural reproduction -> endorsement, truth, compliance, legal sufficiency, or authority.

## Fixture semantics

Fixtures marked `expected_valid: true` must satisfy the invariant.

Fixtures marked `expected_valid: false` intentionally encode an overread or distortion and must be rejected by the semantic checker.

## Non-claims

The protocol classifies access and interpretation boundaries. It does not decide whether the reviewed content is correct or sufficient.
