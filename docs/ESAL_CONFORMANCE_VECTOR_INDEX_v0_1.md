ESAL Conformance Vector Index v0.1

Document ID: ESAL_CONFORMANCE_VECTOR_INDEX_v0_1  
Status: Draft v0.1  
Intended path: docs/ESAL_CONFORMANCE_VECTOR_INDEX_v0_1.md  
Applies to: ESAL v0.1 conformance and reproduction vectors.  
Primary spec: spec/BDR-ESAL-v0.1.md  
Boundary posture: Preservation without inheritance.

---

1. Purpose

This index identifies the conformance vector classes required to test BDR-ESAL v0.1 replay behavior.

It does not certify that all vectors are currently complete.

It separates:

- Existing branch-visible vectors.
- Required reproduction vectors.
- Expected outputs.
- Known gaps.

---

2. Vector maturity labels

Label | Meaning
------|--------
VECTOR_PRESENT | Input vector is branch-visible
EXPECTED_OUTPUT_PRESENT | Expected output is branch-visible
FINGERPRINT_PRESENT | Expected fingerprint is branch-visible
FAILURE_CLASS_PRESENT | Expected failure class is branch-visible
REPRODUCTION_READY | Vector has enough information for independent reproduction
GAP | Required reproduction evidence is missing or incomplete

---

3. Required baseline vector classes

Vector class | Purpose | Required for reproduction
-------------|---------|--------------------------
Basic replay | Demonstrates valid BDR-created event reduction | Yes
Constraint accumulation | Demonstrates monotonic constraint preservation | Yes
Obligation accumulation | Demonstrates monotonic obligation preservation | Yes
Validity false | Demonstrates monotonic false validity behavior | Yes
Violation preservation | Demonstrates violation ordering and retention | Yes
Event reordering | Demonstrates canonical order invariance | Yes
Duplicate event ID | Demonstrates duplicate rejection | Yes
Unknown event type | Demonstrates unsupported event type rejection | Yes
Invalid timestamp | Demonstrates timestamp parsing failure | Yes
Execution mutation | Demonstrates EXECUTION state mutation rejection | Yes
Unsupported removal | Demonstrates constraint/obligation removal rejection | Yes

---

4. Branch-visible vector inventory

The following inventory SHOULD be updated against the current branch before any independent reproduction request is sent.

Vector path | Vector class | Expected output path | Current status | Notes
------------|-------------|----------------------|----------------|------
esal-tests/canonical/log1-basic-A-B-C.jsonl | Basic replay | esal-tests/expected/log1-basic-A-B-C.state.json | VECTOR_PRESENT | Verify fingerprint availability
esal-tests/canonical/log2-constraints-tighten.jsonl | Constraint accumulation | esal-tests/expected/log2-constraints-tighten.state.json | VECTOR_PRESENT | Verify monotonic constraint semantics
esal-tests/canonical/log3-obligations-accumulate.jsonl | Obligation accumulation | esal-tests/expected/log3-obligations-accumulate.state.json | VECTOR_PRESENT | Verify obligation ordering and set behavior
esal-tests/adversarial/log4-constraint-violation.jsonl | Validity false / violation preservation | esal-tests/expected/log4-constraint-violation.state.json | VECTOR_PRESENT | Verify validity false remains false
esal-tests/adversarial/log5-authority-inflation.jsonl | Authority inflation | esal-tests/expected/log5-authority-inflation.state.json | VECTOR_PRESENT | Confirm expected classification boundary
esal-tests/adversarial/log6-lineage-truncation.jsonl | Lineage truncation | esal-tests/expected/log6-lineage-truncation.failure.json | VECTOR_PRESENT | Confirm required failure code
esal-tests/adversarial/log7-event-reordering.jsonl | Event reordering | esal-tests/expected/log7-event-reordering.failure.json | VECTOR_PRESENT | Confirm whether this is failure or invariance vector
esal-tests/malformed/log8-schema-invalid.jsonl | Malformed event | esal-tests/expected/log8-schema-invalid.failure.json | VECTOR_PRESENT | Confirm schema/failure code alignment

---

5. Required additions before independent reproduction

Before claiming reproduction readiness, the branch SHOULD contain a clean vector bundle that includes:

- esal-tests/reproduction/
  - positive/
  - adversarial/
  - malformed/
  - expected/
  - fingerprints/

Each vector SHOULD have:

- Input event log.
- Expected canonical state or expected failure.
- Expected fingerprint where replay succeeds.
- Expected result token.
- Required error code where replay fails.
- Short explanation of what behavior is tested.

---

6. Fingerprint requirement

Every successful replay vector intended for independent reproduction SHOULD include a preserved expected fingerprint.

Expected fingerprint records SHOULD identify:

```json
{
  "spec_version": "BDR-ESAL-v0.1",
  "profile": "BDR_ESAL_BASELINE_REPLAY_v0_1",
  "vector_id": "string",
  "fingerprint_algorithm": "sha256",
  "fingerprint": "string",
  "canonical_state_path": "string",
  "generated_by": "string",
  "command": "string",
  "commit": "string"
}
```

Without expected fingerprints, independent reviewers can compare state shape but cannot fully reproduce the replay digest claim.

---

7. Failure-class requirement

Every failing vector intended for independent reproduction SHOULD include a preserved expected failure record.

Expected failure records SHOULD identify:

```json
{
  "spec_version": "BDR-ESAL-v0.1",
  "profile": "BDR_ESAL_BASELINE_REPLAY_v0_1",
  "vector_id": "string",
  "expected_result": "FAIL",
  "expected_error_code": "string",
  "expected_error_scope": "parse|canonicalization|reduction|fingerprint",
  "command": "string",
  "commit": "string"
}
```

---

8. Reproduction readiness determination

A vector class is reproduction-ready only when all applicable evidence exists:

- input vector
- expected state or expected failure
- expected fingerprint for successful replay
- expected error code for failed replay
- command used to generate expected output
- commit or version reference
- non-claim boundary

If any required element is missing, the vector class SHOULD remain marked as GAP.

---

9. Current determination

The existing ESAL vector surface appears to contain useful canonical, adversarial, malformed, and expected-output artifacts.

However, this index does not by itself establish full independent reproduction readiness.

The next step is to bind each vector to expected fingerprints and failure classes in a dedicated reproduction bundle.

---

10. Non-claims

This index does not establish:

- Independent reproduction.
- Legal sufficiency.
- Compliance.
- Safety.
- Truth.
- Approval.
- Runtime authorization.
- External endorsement.
- Host-system conformance.

It is an inventory and readiness document only.