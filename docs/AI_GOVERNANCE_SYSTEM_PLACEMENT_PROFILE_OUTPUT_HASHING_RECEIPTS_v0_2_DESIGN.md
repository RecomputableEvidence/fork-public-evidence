# AI Governance System Placement Profile Output Hashing and Verification Receipts v0.2 Design

Status: `DESIGN_ONLY_NOT_IMPLEMENTED`

Version: `0.2-design`

Applies to lineage:

- `ai-governance-system-placement-profile-v0.1`
- `ai-governance-system-placement-profile-schema-fixtures-v0.1`
- `ai-governance-system-placement-profile-checker-v0.1`
- `ai-governance-system-placement-profile-checker-hardening-v0.1.1`
- `ai-governance-system-placement-profile-v0.2-planning`

## 1. Purpose

This document defines the design for a future v0.2 Output Hashing and Verification Receipts module for the AI Governance System Placement Profile checker line.

This is a design artifact only.

It is not a schema.

It is not a checker.

It is not an implementation.

It does not approve v0.2 code changes.

It does not add runtime behavior.

It does not expand Fork's authority beyond structural and boundary validation.

The purpose of this design is to define how Fork may compute deterministic SHA-256 hashes over normalized checker outputs and emit bounded verification receipts that support recomputable comparison across clean machines.

The receipt proves only that a specific normalized checker output produced a specific hash.

It does not prove that the underlying AI system is safe, compliant, lawful, audit-sufficient, correct, approved, complete, or institutionally authorized.

## 2. Current Baseline

The v0.1.1 Placement Profile checker currently validates single-record structural and boundary consistency.

The checker emits:

- full result output
- normalized result output
- explicit checker status:
  - `PASS`
  - `FAIL`
  - `INDETERMINATE`
- explicit process exit code:
  - `PASS = 0`
  - `FAIL = 1`
  - `INDETERMINATE = 2`
- preserved non-claims
- deterministic normalized outputs for comparison

The normalized output excludes environment-specific fields such as:

- `checked_at_utc`
- local absolute paths
- local machine/environment metadata
- other execution-specific fields that would prevent clean-machine comparison

The normalized output preserves substantive fields needed to compare checker behavior.

v0.2 Output Hashing and Verification Receipts should build on this existing normalized-output boundary.

## 3. Core Design Principle

The v0.2 receipt must hash the normalized checker output, not the raw execution environment.

Core rule:

> Fork hashes normalized checker output so independent reviewers can recompute and compare the structural result. Fork does not hash its way into semantic, legal, compliance, audit, safety, runtime, or institutional authority.

The hash is a deterministic integrity claim about the normalized output.

The hash is not an authority claim about the underlying system.

## 4. What Gets Hashed

The primary hash target is:

`normalized_checker_output_json`

The byte stream to be hashed must be generated from the normalized result object using a deterministic JSON serialization.

Recommended serialization:

- UTF-8 encoding
- sorted object keys
- compact separators
- no trailing whitespace
- LF line handling if written to file
- no environment-specific fields
- no absolute local paths
- no timestamps inside the normalized hash payload unless explicitly included as stable data

Recommended Python serialization equivalent:

```python
json.dumps(normalized_result, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
```

The resulting byte stream is hashed using SHA-256.

Output field:

`normalized_output_sha256`

## 5. What Does Not Get Hashed

The normalized-output hash must not include fields that vary across clean-machine executions unless explicitly included by design.

Excluded from normalized hash scope:

- `checked_at_utc`
- `receipt_created_at_utc`
- local absolute `record_path`
- local absolute `schema_path`
- local working directory
- operating system metadata
- Python executable path
- hostname
- username
- temporary directory paths
- raw stderr/stdout logs
- runtime duration
- wall-clock timestamps
- any non-deterministic ordering

A full receipt may include some of these fields for debugging or provenance, but they must not be included in the normalized-output hash unless a later design explicitly defines a separate environment-inclusive hash.

## 6. Hash Algorithm

Required algorithm:

`SHA-256`

Required algorithm identifier:

`sha256`

The v0.2 design does not approve alternative algorithms.

Future algorithms, if added, must be explicitly versioned.

The receipt must identify the algorithm used.

## 7. Receipt Purpose

A verification receipt is a bounded record of a checker output hash.

The receipt should allow a reviewer to answer:

1. Which checker produced the normalized output?
2. Which checker version produced it?
3. Which schema version was used?
4. Which record was checked?
5. What was the checker status?
6. What was the SHA-256 hash of the normalized output?
7. Which hash algorithm was used?
8. What non-claims are preserved?
9. Was the receipt generated from a normalized result or a full result?
10. Can the normalized output be recomputed and compared later?

The receipt should not answer:

1. Was the AI system safe?
2. Was the system compliant?
3. Was the system legally sufficient?
4. Was the evidence substantively adequate?
5. Was the workflow decision correct?
6. Was the output institutionally approved?
7. Was an external artifact authentic?
8. Was a cross-record governance graph valid?

## 8. Proposed Receipt Shape

A v0.2 receipt should be a JSON object.

Proposed fields:

```json
{
  "receipt_type": "PLACEMENT_PROFILE_NORMALIZED_OUTPUT_HASH_RECEIPT",
  "receipt_version": "0.2",
  "receipt_status": "EMITTED",
  "checker_id": "ai_governance_system_placement_profile_checker",
  "checker_version": "0.2",
  "schema_id": "ai_governance_system_placement_profile_v0_1",
  "schema_version": "0.1",
  "record_id": "string",
  "system_id": "string",
  "overall_status": "PASS | FAIL | INDETERMINATE",
  "hash_algorithm": "sha256",
  "normalized_output_sha256": "hex-string",
  "normalized_output_hash_scope": "NORMALIZED_CHECKER_OUTPUT_ONLY",
  "normalized_output_hash_input_description": "Deterministic JSON serialization of normalized checker output with sorted keys and compact separators.",
  "receipt_created_at_utc": "ISO-8601 timestamp",
  "receipt_environment_fields_excluded_from_hash": [
    "checked_at_utc",
    "receipt_created_at_utc",
    "record_path",
    "schema_path",
    "environment",
    "runtime_duration"
  ],
  "non_claims": [
    "Does not validate semantic truth.",
    "Does not validate legal sufficiency.",
    "Does not validate compliance sufficiency.",
    "Does not validate audit sufficiency.",
    "Does not validate model safety.",
    "Does not provide runtime enforcement.",
    "Does not verify external artifact existence.",
    "Does not perform cross-record graph validation.",
    "Does not grant institutional authority."
  ]
}
```

## 9. Required Receipt Fields

The following fields should be required for v0.2 receipt validity:

- `receipt_type`
- `receipt_version`
- `receipt_status`
- `checker_id`
- `checker_version`
- `schema_id`
- `schema_version`
- `record_id`
- `system_id`
- `overall_status`
- `hash_algorithm`
- `normalized_output_sha256`
- `normalized_output_hash_scope`
- `normalized_output_hash_input_description`
- `receipt_created_at_utc`
- `receipt_environment_fields_excluded_from_hash`
- `non_claims`

## 10. Receipt Status Values

Allowed receipt status values:

- `EMITTED`
- `NOT_EMITTED`
- `HASH_MISMATCH`
- `RECOMPUTED_MATCH`
- `RECOMPUTED_MISMATCH`

For v0.2 initial implementation, only the following may be necessary:

- `EMITTED`
- `RECOMPUTED_MATCH`
- `RECOMPUTED_MISMATCH`

No receipt status may imply:

- legal approval
- compliance certification
- audit sufficiency
- model safety
- institutional approval
- production readiness
- external artifact authenticity
- cross-record graph validity

## 11. Hash Scope

Required hash scope label:

`NORMALIZED_CHECKER_OUTPUT_ONLY`

Meaning:

The hash covers only the deterministic normalized checker output.

It does not cover:

- raw input record bytes
- raw schema bytes
- full checker result with environment metadata
- external artifacts
- workspace manifests
- cross-record graphs
- live systems
- legal/compliance/audit determinations

Optional future hash scopes may be considered later, but are not approved by this design.

Potential future scopes:

- `NORMALIZED_RESULT_AND_SCHEMA`
- `NORMALIZED_RESULT_AND_RECORD`
- `WORKSPACE_MANIFEST_ONLY`
- `GRAPH_NORMALIZED_OUTPUT_ONLY`

These are not approved for v0.2 initial implementation.

## 12. Receipt Emission Modes

Potential checker flags:

```text
--emit-receipt <path>
--verify-receipt <path>
```

Candidate behavior:

### 12.1 Emit Receipt

Command pattern:

```text
python tools/check_ai_governance_system_placement_profile_v0_2.py \
  --record <record.json> \
  --schema <schema.json> \
  --output <result.json> \
  --normalized-output <normalized_result.json> \
  --emit-receipt <receipt.json>
```

Behavior:

1. Run the placement-profile checker.
2. Emit full result output if requested.
3. Emit normalized output if requested.
4. Serialize normalized output deterministically.
5. Compute SHA-256 over the deterministic normalized-output byte stream.
6. Emit receipt JSON.
7. Preserve original checker exit code semantics:
   - `PASS = 0`
   - `FAIL = 1`
   - `INDETERMINATE = 2`

Receipt emission must not convert `FAIL` or `INDETERMINATE` into success.

### 12.2 Verify Receipt

Command pattern:

```text
python tools/check_ai_governance_system_placement_profile_v0_2.py \
  --normalized-output <normalized_result.json> \
  --verify-receipt <receipt.json>
```

Behavior:

1. Load normalized output.
2. Deterministically serialize normalized output.
3. Compute SHA-256.
4. Compare computed hash to `normalized_output_sha256` in the receipt.
5. Emit:
   - `RECOMPUTED_MATCH`
   - `RECOMPUTED_MISMATCH`

Verification means only that the normalized output matches or does not match the receipt hash.

Verification does not mean the underlying system is safe, compliant, lawful, correct, complete, or approved.

## 13. Exit-Code Preservation

The v0.2 receipt module must preserve v0.1.1 exit-code semantics.

Checker execution:

- `PASS = 0`
- `FAIL = 1`
- `INDETERMINATE = 2`

Receipt verification candidate exit codes:

- `RECOMPUTED_MATCH = 0`
- `RECOMPUTED_MISMATCH = 1`
- `RECEIPT_PARSE_OR_SCHEMA_FAILURE = 1`

Open design question:

Should receipt verification use the same status vocabulary as checker execution, or a separate receipt-verification vocabulary?

Recommended answer:

Use a separate receipt-verification vocabulary while preserving process exit-code conventions.

Reason:

A receipt match is not the same kind of claim as a placement-profile `PASS`.

## 14. Relationship to PASS / FAIL / INDETERMINATE

A receipt may be emitted for any checker result state.

Allowed:

- receipt for `PASS`
- receipt for `FAIL`
- receipt for `INDETERMINATE`

Reason:

The receipt records the normalized checker output, not approval.

A `FAIL` receipt can be useful because it proves that a particular malformed or boundary-violating record produced a specific deterministic failure result.

An `INDETERMINATE` receipt can be useful because it proves that active unresolved unknowns were preserved rather than silently converted into success.

No receipt should upgrade or downgrade the checker result.

## 15. Non-Claims

The receipt must preserve explicit non-claims.

Required non-claims:

Fork does not validate semantic truth.

Fork does not validate legal sufficiency.

Fork does not validate compliance sufficiency.

Fork does not validate audit sufficiency.

Fork does not validate model safety.

Fork does not provide runtime enforcement.

Fork does not verify external artifact existence.

Fork does not perform cross-record graph validation.

Fork does not grant institutional authority.

Fork does not certify governance systems.

Fork does not determine whether evidence is legally admissible.

Fork does not determine whether a workflow decision was correct.

Fork does not determine whether an organization satisfied regulatory obligations.

Fork does not infer claim inheritance across handoffs.

Fork does not treat receipt hashing as proof of governance sufficiency.

## 16. Fixture Plan

A future v0.2 implementation should include fixtures for receipt emission and verification.

Candidate fixture outputs:

- `valid_evaluation_system_placement_receipt_v0_2.json`
- `invalid_claim_nonclaim_overlap_receipt_v0_2.json`
- `indeterminate_active_unresolved_unknown_receipt_v0_2.json`
- `tampered_normalized_output_receipt_mismatch_v0_2.json`
- `malformed_receipt_v0_2.json`
- `missing_receipt_hash_v0_2.json`
- `wrong_hash_algorithm_v0_2.json`

Candidate fixture behaviors:

### 16.1 Valid PASS Receipt

A valid placement profile produces:

- checker status: `PASS`
- receipt status: `EMITTED`
- normalized-output SHA-256 present
- receipt recomputation status: `RECOMPUTED_MATCH`

### 16.2 Valid FAIL Receipt

An invalid placement profile produces:

- checker status: `FAIL`
- receipt status: `EMITTED`
- normalized-output SHA-256 present
- receipt recomputation status: `RECOMPUTED_MATCH`

### 16.3 Valid INDETERMINATE Receipt

An indeterminate placement profile produces:

- checker status: `INDETERMINATE`
- receipt status: `EMITTED`
- normalized-output SHA-256 present
- receipt recomputation status: `RECOMPUTED_MATCH`

### 16.4 Tampered Normalized Output

A normalized output is modified after receipt emission.

Expected result:

- receipt verification status: `RECOMPUTED_MISMATCH`
- process exit code: `1`
- no claim of semantic tampering beyond hash mismatch

### 16.5 Malformed Receipt

A receipt is not valid JSON or is missing required fields.

Expected result:

- receipt verification status: `RECEIPT_INVALID`
- process exit code: `1`

### 16.6 Wrong Hash Algorithm

A receipt declares an unsupported hash algorithm.

Expected result:

- receipt verification status: `RECEIPT_INVALID`
- error code: `ERR_UNSUPPORTED_HASH_ALGORITHM`
- process exit code: `1`

## 17. Test Plan

A future v0.2 implementation should include tests for:

- receipt emitted for PASS result
- receipt emitted for FAIL result
- receipt emitted for INDETERMINATE result
- normalized-output hash recomputes identically
- tampered normalized output produces mismatch
- malformed receipt fails
- missing receipt hash fails
- unsupported hash algorithm fails
- receipt preserves non-claims
- receipt does not include environment-specific fields in hash scope
- v0.1.1 checker regressions remain intact
- v0.1 checker regressions remain intact
- schema/fixture regressions remain intact
- AI Governance Mapping Record regressions remain intact
- semantic alignment regression remains intact

## 18. Documentation Plan

A future v0.2 implementation should include documentation explaining:

- what a normalized-output receipt is
- how SHA-256 is computed
- what fields are included in hash scope
- what fields are excluded from hash scope
- how to recompute a receipt
- how to compare a recomputed hash
- how to interpret `RECOMPUTED_MATCH`
- how to interpret `RECOMPUTED_MISMATCH`
- why receipt match does not mean semantic truth
- why receipt match does not mean legal/compliance/audit sufficiency
- why receipt match does not mean model safety
- why receipt match does not mean runtime enforcement
- why receipt match does not mean institutional approval

## 19. Open Design Questions

### 19.1 Should Receipts Be Separate Files or Embedded Fields?

Recommended initial answer:

Receipts should be separate files.

Reason:

Separate files preserve the distinction between checker output and hash receipt. They also allow receipts to be generated or verified independently without mutating the normalized output.

### 19.2 Should Full Results Be Hashed?

Recommended initial answer:

No.

Reason:

Full results may contain environment-specific fields that are useful for debugging but unsuitable for clean-machine recomputation.

### 19.3 Should Raw Records Be Hashed?

Recommended initial answer:

Not in initial v0.2.

Reason:

Raw record hashing introduces a broader artifact-integrity layer. It may be useful later, but v0.2 should start with normalized checker output only.

### 19.4 Should Receipts Include Timestamps?

Recommended initial answer:

Yes, but timestamps must not be inside the normalized-output hash scope.

Reason:

Receipt creation time may be useful for human review, but it should not disturb normalized-output recomputability.

### 19.5 Should Receipt Verification Re-run the Checker?

Recommended initial answer:

No for initial receipt verification.

Reason:

Receipt verification should compare a normalized output to a receipt. Re-running the checker is a separate operation.

A later tool may support an end-to-end recompute mode, but that should be explicitly designed.

## 20. Candidate CLI Design

Potential future checker flags:

```text
--emit-receipt <path>
--verify-receipt <path>
--receipt-output <path>
--hash-algorithm sha256
```

Recommended initial minimal flags:

```text
--emit-receipt <path>
--verify-receipt <path>
```

Do not add network, external URL, live-system, or cross-record flags in v0.2.

## 21. Candidate Error Codes

Potential v0.2 receipt-specific error codes:

- `ERR_RECEIPT_JSON_PARSE`
- `ERR_RECEIPT_REQUIRED_FIELD_MISSING`
- `ERR_UNSUPPORTED_HASH_ALGORITHM`
- `ERR_NORMALIZED_OUTPUT_JSON_PARSE`
- `ERR_NORMALIZED_OUTPUT_HASH_MISMATCH`
- `ERR_RECEIPT_SCOPE_UNSUPPORTED`
- `ERR_RECEIPT_STATUS_UNSUPPORTED`

These error codes must remain structural.

They must not imply legal, compliance, audit, safety, or institutional findings.

## 22. Candidate Output Files

Possible future output directory:

`output/ai_governance_system_placement_profile_receipts_v0_2/`

Possible files:

- `valid_evaluation_system_placement_receipt.json`
- `valid_evaluation_system_placement_receipt_verification.json`
- `invalid_claim_nonclaim_overlap_receipt.json`
- `invalid_claim_nonclaim_overlap_receipt_verification.json`
- `indeterminate_active_unresolved_unknown_receipt.json`
- `indeterminate_active_unresolved_unknown_receipt_verification.json`
- `tampered_normalized_output_receipt_verification.json`

## 23. Review Requirements Before Implementation

Before implementation, this design should be reviewed for:

1. Hash scope clarity.
2. Receipt field sufficiency.
3. Non-claim preservation.
4. Exit-code separation between checker execution and receipt verification.
5. Fixture adequacy.
6. Risk of overclaiming cryptographic proof.
7. Compatibility with v0.1.1 normalized-output guidance.
8. Regression impact.
9. Whether any schema change is required.
10. Whether receipt generation can be implemented without modifying v0.1.1 semantics.

## 24. Implementation Recommendation

Recommended v0.2 implementation posture:

- implement receipt emission over normalized outputs
- implement receipt verification against normalized outputs
- preserve v0.1.1 checker semantics
- keep receipts separate from normalized outputs
- use SHA-256 only
- emit deterministic receipt verification outputs
- commit representative receipt fixtures
- run full regression suite

Do not implement:

- workspace manifest resolution
- external artifact verification
- cross-record validation
- DAG compilation
- semantic/NLP validation
- runtime enforcement
- legal/compliance/audit sufficiency checks
- model-safety checks
- institutional approval logic

## 25. Status

This document is a design artifact.

No v0.2 feature is approved by this document.

No schema change is approved by this document.

No checker change is approved by this document.

No runtime behavior is introduced by this document.

No legal, compliance, audit, safety, or institutional authority is claimed by this document.

Final status:

`V0_2_OUTPUT_HASHING_RECEIPTS_DESIGN_ONLY_NOT_IMPLEMENTED`

