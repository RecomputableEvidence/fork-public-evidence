# ESAL Independent Reproduction Packet v0.1

**Document ID:** `ESAL_INDEPENDENT_REPRODUCTION_PACKET_v0_1`
**Status:** Draft v0.1
**Intended path:** `docs/ESAL_INDEPENDENT_REPRODUCTION_PACKET_v0_1.md`
**Applies to:** BDR-ESAL v0.1 replay, conformance, and independent reproduction review.
**Primary spec:** `spec/BDR-ESAL-v0.1.md`
**Boundary posture:** Preservation without inheritance.

---

## 1. Purpose

This packet defines what an independent evaluator or second implementer needs in order to reproduce ESAL replay behavior without relying on Fork project self-description or reference implementation internals.

The goal is not to prove that Fork decisions are legally sufficient, compliant, safe, true, approved, or externally authoritative.

The goal is narrower:

> Given the same BDR-ESAL v0.1 specification and the same conformance vectors, can an independent implementation reduce event logs to the same bounded governance-state classifications and fingerprints?

---

## 2. Reproduction target

An independent reproduction attempt SHOULD target the following behavior:

1. Parse BDR-ESAL v0.1 event logs.
2. Canonicalize event order.
3. Apply the ESAL reduction function.
4. Enforce validity monotonicity.
5. Enforce constraint and obligation monotonicity.
6. Preserve lineage and violations.
7. Serialize canonical governance state.
8. Compute SHA-256 state fingerprints.
9. Emit bounded PASS / FAIL conformance results.
10. Preserve non-claims.

A reproduction is successful only within the declared structural scope.

---

## 3. Required inputs

A reproduction packet SHOULD include:

| Input | Required | Purpose |
|---|---:|---|
| `spec/BDR-ESAL-v0.1.md` | Yes | Normative replay specification |
| Canonical positive event logs | Yes | Demonstrate expected successful replay |
| Adversarial event logs | Yes | Demonstrate expected violation or failure behavior |
| Malformed event logs | Yes | Demonstrate parser/schema failure behavior |
| Expected state outputs | Yes | Provide target canonical states |
| Expected fingerprints | Yes | Provide target digest values |
| Expected error classes | Yes | Provide target failure classifications |
| Reference command | Yes | Preserve how the reference result was generated |
| Implementation notes | Optional | Help reviewers understand implementation environment |

---

## 4. Independence requirement

A reproduction SHOULD be considered independent only if the evaluator:

1. Implements replay behavior from the public specification.
2. Does not copy the reference implementation.
3. Does not tune implementation behavior against private project notes.
4. Uses public conformance vectors.
5. Records implementation provenance.
6. Records command, environment, commit, and tool version.
7. Records limitations and non-claims.

Reviewer discussion alone is not independent reproduction.

A second run by the same implementation is repeat execution, not independent reproduction.

---

## 5. Minimum conformance vector classes

A minimally useful reproduction attempt SHOULD include the following vector classes:

| Vector class | Required behavior |
|---|---|
| Basic replay | Valid BDR-created event reduces to expected state |
| Constraint accumulation | Multiple constraints are preserved monotonically |
| Obligation accumulation | Multiple obligations are preserved monotonically |
| Validity false | A validity-affecting event sets validity false and does not restore it |
| Violation preservation | Violations are appended and preserved in order |
| Event reordering | Same event set in different physical order produces the same fingerprint |
| Duplicate event ID | Duplicate event IDs fail |
| Unknown event type | Unknown event types fail under baseline v0.1 |
| Invalid timestamp | Invalid timestamp fails |
| Execution mutation | EXECUTION event attempting state mutation fails |
| Unsupported removal | Constraint or obligation removal fails |

---

## 6. Expected reproduction result shape

A reproduction result SHOULD preserve the following fields:

```json
{
  "reproduction_id": "string",
  "spec_version": "BDR-ESAL-v0.1",
  "profile": "BDR_ESAL_BASELINE_REPLAY_v0_1",
  "implementation_name": "string",
  "implementation_version": "string",
  "implementation_repository": "string",
  "implementation_commit": "string",
  "executor": "string",
  "execution_timestamp": "string",
  "command": "string",
  "input_vectors": [],
  "matched_expected_outputs": true,
  "matched_expected_fingerprints": true,
  "matched_expected_failures": true,
  "result": "REPRODUCED",
  "limitations": [],
  "non_claims": []
}
```

If any expected state, fingerprint, or failure class does not match, the result MUST NOT be `REPRODUCED`.

---

## 7. Result tokens

Permitted reproduction result tokens:

| Token                  | Meaning                                                                                   |
|------------------------|-------------------------------------------------------------------------------------------|
| `REPRODUCED`           | Independent implementation matched expected states, fingerprints, and failure classes    |
| `PARTIALLY_REPRODUCED` | Some vectors matched, but gaps remain                                                     |
| `NOT_REPRODUCED`       | Expected behavior did not reproduce                                                       |
| `INCONCLUSIVE`         | Corpus or execution lacked enough evidence to determine a reproduction result            |

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

## 8. Non-claims

Independent reproduction does not establish:

- Legal sufficiency.
- Regulatory compliance.
- Audit acceptance.
- Safety.
- Truth.
- Approval.
- Runtime authorization.
- External authority.
- Institutional endorsement.
- Host-system conformance.
- Business fitness.
- Claim inheritance.

It establishes only that the replay behavior was independently reproduced under declared conditions.

---

## 9. Current v0.1 status

As of this packet, independent reproduction is not yet established by this document alone.

This packet defines the path to independent reproduction.

The next required artifact is a clean conformance vector index with expected outputs and fingerprints suitable for second implementation review.

---

## 10. Summary

Fork’s next credibility threshold is not another doctrine artifact.

The next threshold is independent reproduction:

> A second implementation, built from the public BDR-ESAL v0.1 specification, produces the same bounded replay results from the same conformance vectors.

That is the evidence threshold this packet prepares.
