# ESAL Independent Reproduction Execution Artifact v0.1

**Document ID:** `ESAL_INDEPENDENT_REPRODUCTION_EXECUTION_ARTIFACT_v0_1`
**Status:** Draft v0.1
**Intended path:** `docs/ESAL_INDEPENDENT_REPRODUCTION_EXECUTION_ARTIFACT_v0_1.md`
**Primary spec:** `spec/BDR-ESAL-v0.1.md`
**Primary bundle:** `esal-tests/reproduction/manifest_v0_1.json`
**Profile:** `BDR_ESAL_BASELINE_REPLAY_v0_1`
**Boundary posture:** Preservation without inheritance.

---

## 1. Purpose

This document defines the required structure for recording an independent reproduction attempt against the ESAL Reproduction Vector Bundle v0.1.

It does not itself establish independent reproduction.

It defines the evidence that must be preserved when a second implementation, clean-room evaluator, or external reviewer runs the ESAL reproduction bundle and reports whether the expected states, fingerprints, and failure classes were reproduced.

---

## 2. Reproduction target

An independent reproduction attempt targets the following artifacts:

```text
spec/BDR-ESAL-v0.1.md
esal-tests/reproduction/manifest_v0_1.json
esal-tests/reproduction/positive/
esal-tests/reproduction/adversarial/
esal-tests/reproduction/malformed/
esal-tests/reproduction/expected/
esal-tests/reproduction/fingerprints/
esal-tests/reproduction/failures/
```

The evaluator SHOULD implement or execute the BDR-ESAL baseline replay profile using the public specification and bundle.

---

## 3. Independence requirement

A reproduction attempt SHOULD be treated as independent only if the evaluator:

1. Identifies the implementation used.
2. Records the implementation repository or archive reference.
3. Records the implementation commit or version.
4. Records the execution command.
5. Records the execution environment.
6. Records whether the implementation was clean-room, forked, adapted, or reference-derived.
7. Preserves vector-level results.
8. Preserves fingerprint matches and mismatches.
9. Preserves failure-class matches and mismatches.
10. Preserves limitations and non-claims.

Reviewer commentary alone is not independent reproduction.

A first-party rerun of Fork's own implementation is not independent reproduction.

---

## 4. Required result tokens

Permitted result tokens are:

| Token | Meaning |
|---|---|
| `INDEPENDENT_REPRODUCTION_ESTABLISHED_WITH_LIMITATIONS` | Independent implementation reproduced all required state fingerprints and failure expectations, subject to declared limitations |
| `PARTIAL_INDEPENDENT_REPRODUCTION` | Some vectors reproduced, but one or more required expectations did not |
| `INDEPENDENT_REPRODUCTION_NOT_ESTABLISHED` | Reproduction was not attempted or did not produce sufficient evidence |
| `INCONCLUSIVE` | Evidence was insufficient to classify the reproduction attempt |

The following tokens MUST NOT be used as reproduction result tokens:

- `APPROVED`
- `CERTIFIED`
- `COMPLIANT`
- `SAFE`
- `LEGAL`
- `ADMISSIBLE`
- `AUTHORIZED`
- `ENDORSED`
- `TRUSTED`

---

## 5. Required vector result shape

Each vector result SHOULD preserve:

```json
{
  "vector_id": "string",
  "input_path": "string",
  "expected_artifact_path": "string",
  "observed_result": "PASS|FAIL|ERROR",
  "expected_result": "PASS|FAIL",
  "matched_expected_state": true,
  "matched_expected_fingerprint": true,
  "matched_expected_failure_class": true,
  "observed_fingerprint": "string",
  "expected_fingerprint": "string",
  "observed_failure_class": "string",
  "expected_failure_class": "string",
  "notes": []
}
```

Successful replay vectors SHOULD compare canonical state and fingerprint.

Failure vectors SHOULD compare expected failure class, failure scope, or declared review-required marker.

---

## 6. Required artifact-level fields

An independent reproduction execution artifact SHOULD preserve:

- artifact ID
- spec version
- bundle manifest path
- bundle manifest digest
- reproduction profile
- evaluator identity or role
- implementation identity
- implementation repository or archive
- implementation commit or version
- independence basis
- command
- environment
- execution timestamp
- vector result matrix
- aggregate result token
- mismatches
- limitations
- non-claims

---

## 7. Non-claims

An independent reproduction execution artifact does not establish:

- Legal sufficiency.
- Regulatory compliance.
- Audit acceptance.
- Safety.
- Truth.
- Approval.
- Runtime authorization.
- External endorsement.
- Host-system conformance.
- Business fitness.
- Claim inheritance.

Independent reproduction establishes only that a declared implementation reproduced, partially reproduced, failed to reproduce, or inconclusively attempted to reproduce the bounded ESAL replay expectations under declared conditions.

---

## 8. Current v0.1 status

This v0.1 package provides the record shape, schema, pending example, and status report required to receive independent reproduction evidence.

Current status:

```text
INDEPENDENT_REPRODUCTION_NOT_YET_ESTABLISHED
```

Closure requires a real execution artifact from a second implementation or independent evaluator.
