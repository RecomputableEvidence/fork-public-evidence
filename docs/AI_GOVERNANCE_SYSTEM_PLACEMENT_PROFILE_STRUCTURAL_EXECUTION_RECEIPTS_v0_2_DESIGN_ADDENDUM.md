# AI Governance System Placement Profile Structural Execution Receipts v0.2 Design Addendum

Status: `DESIGN_ADDENDUM_ONLY_NOT_IMPLEMENTED`

Version: `0.2-design-addendum`

Applies to lineage:

- `ai-governance-system-placement-profile-v0.1`
- `ai-governance-system-placement-profile-schema-fixtures-v0.1`
- `ai-governance-system-placement-profile-checker-v0.1`
- `ai-governance-system-placement-profile-checker-hardening-v0.1.1`
- `ai-governance-system-placement-profile-v0.2-planning`
- `ai-governance-system-placement-profile-output-hashing-receipts-v0.2-design`

## 1. Purpose

This addendum refines the v0.2 Output Hashing and Receipts design before implementation.

It addresses two design clarifications from external review:

1. The primary artifact name should avoid implying legal, compliance, safety, or institutional verification.
2. Receipt verification should distinguish simple normalized-output hash comparison from full source-profile recomputation.

This addendum is design-only.

It is not a schema.

It is not a checker.

It is not an implementation.

It does not approve v0.2 code changes.

It does not add runtime behavior.

It does not expand Fork's authority beyond structural and boundary validation.

Final implementation must preserve Fork's existing non-claim posture:

Fork does not validate semantic truth, legal sufficiency, compliance sufficiency, audit sufficiency, model safety, runtime behavior, external artifact authenticity, cross-record graph validity, or institutional authority.

## 2. Terminology Correction

The primary artifact name should be:

`Structural Execution Receipt`

Technical synonym:

`Checker Hash Receipt`

Avoid as primary public name:

`Verification Receipt`

Reason:

The phrase "verification receipt" can be misread by non-technical reviewers as system approval, compliance validation, audit sufficiency, legal sufficiency, model-safety validation, or institutional certification.

The phrase "Structural Execution Receipt" is narrower and more accurate.

It means:

> A bounded receipt showing that a specific checker execution produced a specific deterministic normalized structural output hash.

It does not mean:

- the AI system is verified safe
- the system is legally sufficient
- the system is compliant
- the system is audit-sufficient
- the evidence is substantively adequate
- external artifacts are authentic
- the governance chain is valid
- the institution approved the system

## 3. Receipt Scope

A Structural Execution Receipt is a bounded cryptographic record over a normalized checker output.

The hash scope remains:

`NORMALIZED_CHECKER_OUTPUT_ONLY`

The receipt hash must be computed from the deterministic normalized checker output serialization only.

The hash must not include:

- receipt JSON
- receipt timestamp
- local absolute paths
- local working directory
- user name
- host name
- runtime duration
- stdout/stderr
- raw source profile bytes
- raw schema bytes
- external artifacts
- workspace manifests
- cross-record graphs
- live system state

Required hash algorithm:

`sha256`

The receipt hash proves only that the normalized checker output corresponds to the declared SHA-256 value.

The receipt hash does not prove semantic truth or real-world sufficiency.

## 4. Verification Modes

v0.2 should distinguish two separate verification modes.

### 4.1 Normalized Output Hash Comparison Mode

This mode compares an existing normalized output file against an existing Structural Execution Receipt.

Input:

- normalized checker output
- Structural Execution Receipt

Process:

1. Load normalized checker output.
2. Serialize it deterministically.
3. Compute SHA-256.
4. Compare the computed hash to the receipt hash.

This mode may report:

- `NORMALIZED_OUTPUT_HASH_MATCH`
- `NORMALIZED_OUTPUT_HASH_MISMATCH`

This mode proves only:

> The provided normalized output file matches or does not match the receipt hash.

This mode does not prove:

- the source profile was re-run
- the checker was re-executed
- the schema was used again
- the source profile currently produces the same normalized output

Therefore, this mode must not use the status name `RECOMPUTED_MATCH`.

### 4.2 Full Source Recompute Mode

This mode is the preferred Fork recomputability path.

Input:

- source placement profile record
- schema
- checker
- Structural Execution Receipt

Process:

1. Load the source placement profile record.
2. Load the schema.
3. Re-run the checker.
4. Regenerate the normalized checker output.
5. Serialize the regenerated normalized checker output deterministically.
6. Compute SHA-256.
7. Compare the computed hash to the receipt hash.

This mode may report:

- `FULL_RECOMPUTE_MATCH`
- `FULL_RECOMPUTE_MISMATCH`

This mode proves only:

> Re-running the checker against the source profile and schema produced a normalized output whose SHA-256 hash matched or did not match the receipt hash.

This mode does not prove:

- semantic truth
- legal sufficiency
- compliance sufficiency
- audit sufficiency
- model safety
- runtime behavior
- external artifact authenticity
- cross-record graph validity
- institutional authority

## 5. Status Vocabulary

Receipt status terms must avoid overclaiming.

Recommended emission status:

- `EMITTED`

Recommended normalized-output comparison statuses:

- `NORMALIZED_OUTPUT_HASH_MATCH`
- `NORMALIZED_OUTPUT_HASH_MISMATCH`

Recommended full recompute statuses:

- `FULL_RECOMPUTE_MATCH`
- `FULL_RECOMPUTE_MISMATCH`

Reserved or discouraged as generic labels:

- `VERIFIED`
- `VALIDATED`
- `CERTIFIED`
- `APPROVED`
- `COMPLIANT`
- `AUDIT_READY`
- `LEGAL_READY`

The term `RECOMPUTED_MATCH` may be used only if the checker actually re-runs from the source profile and schema.

If implementation supports only existing-normalized-output comparison, it must not call that state `RECOMPUTED_MATCH`.

## 6. Exit-Code Semantics

Checker execution must preserve v0.1.1 semantics:

- `PASS = 0`
- `FAIL = 1`
- `INDETERMINATE = 2`

Receipt emission must preserve the checker result exit code:

- if checker result is `PASS`, receipt emission exits `0`
- if checker result is `FAIL`, receipt emission exits `1`
- if checker result is `INDETERMINATE`, receipt emission exits `2`
- if receipt emission itself fails because of a receipt-writing or hashing error, exit `1`

Receipt comparison mode exit codes:

- `NORMALIZED_OUTPUT_HASH_MATCH = 0`
- `NORMALIZED_OUTPUT_HASH_MISMATCH = 1`
- receipt parse, missing field, unsupported algorithm, or normalized-output parse failure = `1`

Full source recompute mode exit codes:

- `FULL_RECOMPUTE_MATCH = 0`
- `FULL_RECOMPUTE_MISMATCH = 1`
- checker execution failure caused by invalid record boundaries may preserve checker exit code if the recomputed normalized output is still emitted and compared
- receipt parse, missing field, unsupported algorithm, or recompute infrastructure failure = `1`

Open implementation question:

Should full recompute mode preserve a checker `INDETERMINATE = 2` when the recomputed hash matches an `INDETERMINATE` receipt?

Recommended answer:

Yes, if the mode is primarily checker-execution oriented.

Alternative:

Return `0` for `FULL_RECOMPUTE_MATCH` while recording `overall_status = INDETERMINATE` inside the verification output.

This must be decided explicitly before implementation.

## 7. CLI Design Clarification

v0.2 should support separate commands or flag combinations for emission, hash comparison, and full recompute.

### 7.1 Emit Structural Execution Receipt

Candidate command:

```text
python tools/check_ai_governance_system_placement_profile_v0_2.py \
  --record <record.json> \
  --schema <schema.json> \
  --output <result.json> \
  --normalized-output <normalized_result.json> \
  --emit-receipt <structural_execution_receipt.json>
```

Behavior:

- run checker
- emit full output if requested
- emit normalized output if requested
- compute SHA-256 over normalized output
- emit Structural Execution Receipt
- preserve checker exit code

### 7.2 Compare Existing Normalized Output to Receipt

Candidate command:

```text
python tools/check_ai_governance_system_placement_profile_v0_2.py \
  --normalized-output <normalized_result.json> \
  --verify-receipt <structural_execution_receipt.json> \
  --receipt-verification-output <receipt_verification_result.json>
```

Behavior:

- do not re-run checker
- compute hash over provided normalized output
- compare to receipt
- emit `NORMALIZED_OUTPUT_HASH_MATCH` or `NORMALIZED_OUTPUT_HASH_MISMATCH`

### 7.3 Full Source Recompute Against Receipt

Candidate command:

```text
python tools/check_ai_governance_system_placement_profile_v0_2.py \
  --record <record.json> \
  --schema <schema.json> \
  --verify-receipt <structural_execution_receipt.json> \
  --full-recompute \
  --receipt-verification-output <receipt_verification_result.json>
```

Behavior:

- re-run checker from source profile and schema
- regenerate normalized output internally or at a requested path
- compute SHA-256 over regenerated normalized output
- compare to receipt
- emit `FULL_RECOMPUTE_MATCH` or `FULL_RECOMPUTE_MISMATCH`

Do not add:

- network flags
- external URL flags
- live-system flags
- workspace manifest flags
- cross-record graph flags
- runtime enforcement flags

## 8. Receipt Shape Clarification

The receipt should remain small and bounded.

Recommended required fields:

- `receipt_type`
- `receipt_artifact_name`
- `receipt_version`
- `receipt_status`
- `checker_id`
- `checker_version`
- `schema_id`
- `schema_version`
- `record_id`
- `system_id`
- `overall_status`
- `checker_exit_code`
- `hash_algorithm`
- `normalized_output_sha256`
- `normalized_output_hash_scope`
- `normalized_output_hash_input_description`
- `receipt_created_at_utc`
- `receipt_environment_fields_excluded_from_hash`
- `non_claims`

Recommended constants:

```json
{
  "receipt_type": "STRUCTURAL_EXECUTION_RECEIPT",
  "receipt_artifact_name": "Structural Execution Receipt",
  "normalized_output_hash_scope": "NORMALIZED_CHECKER_OUTPUT_ONLY",
  "hash_algorithm": "sha256"
}
```

Do not include:

- local absolute source profile path
- local absolute schema path
- host name
- user name
- working directory
- execution duration
- raw stdout/stderr

If local paths are useful for debugging, place them in the full checker output, not in the Structural Execution Receipt.

## 9. Verification Output Shape

Receipt verification should emit a separate verification-result JSON object.

Candidate fields:

- `verification_type`
- `verification_version`
- `verification_mode`
- `verification_status`
- `receipt_type`
- `receipt_version`
- `checker_id`
- `checker_version`
- `schema_id`
- `schema_version`
- `record_id`
- `system_id`
- `hash_algorithm`
- `expected_normalized_output_sha256`
- `computed_normalized_output_sha256`
- `hash_scope`
- `overall_status_from_receipt`
- `overall_status_from_recomputed_output`
- `non_claims`

For normalized-output comparison mode:

`verification_mode = NORMALIZED_OUTPUT_HASH_COMPARISON`

For full source recompute mode:

`verification_mode = FULL_SOURCE_RECOMPUTE`

## 10. Fixture Updates

The v0.2 fixture plan should include both comparison-mode and full-recompute-mode cases.

Required fixture classes:

1. receipt emitted for `PASS`
2. receipt emitted for `FAIL`
3. receipt emitted for `INDETERMINATE`
4. normalized-output hash comparison match
5. normalized-output hash comparison mismatch
6. full source recompute match
7. full source recompute mismatch caused by source profile modification
8. malformed receipt
9. missing receipt hash
10. unsupported hash algorithm
11. receipt preserves non-claims
12. receipt contains no local absolute paths

## 11. Test Updates

The v0.2 test plan should verify:

- receipt emission for `PASS`
- receipt emission for `FAIL`
- receipt emission for `INDETERMINATE`
- receipt emission preserves checker exit codes
- normalized-output hash comparison match exits `0`
- normalized-output hash comparison mismatch exits `1`
- full source recompute match behavior is defined and tested
- full source recompute mismatch exits `1`
- malformed receipt exits `1`
- missing receipt hash exits `1`
- unsupported hash algorithm exits `1`
- receipt includes required non-claims
- receipt does not include local absolute paths
- receipt does not include environment-specific fields in the hash scope
- receipt verification output distinguishes comparison mode from full recompute mode
- v0.1.1 checker regressions remain intact
- v0.1 checker regressions remain intact
- schema/fixture regressions remain intact
- AI Governance Mapping Record regressions remain intact
- semantic alignment regression remains intact

## 12. Documentation Updates

Documentation should state:

- "Structural Execution Receipt" is the primary artifact name.
- "Checker Hash Receipt" is an acceptable technical shorthand.
- "Verification Receipt" should not be used as the primary artifact name.
- A receipt hash covers normalized checker output only.
- A receipt hash does not cover external artifacts.
- A receipt hash does not prove semantic truth.
- A receipt hash does not prove legal, compliance, audit, safety, runtime, graph, or institutional sufficiency.
- Normalized-output comparison mode is not the same as full source recompute mode.
- Full source recompute mode is the preferred Fork recomputability path.

## 13. Design Decision Summary

Accepted:

- Rename primary artifact to `Structural Execution Receipt`.
- Keep `Checker Hash Receipt` as technical shorthand.
- Keep receipt files separate from normalized outputs.
- Keep hash scope limited to `NORMALIZED_CHECKER_OUTPUT_ONLY`.
- Use SHA-256 only.
- Distinguish normalized-output hash comparison from full source recompute.
- Reserve recompute terminology for actual checker re-execution from source profile and schema.
- Do not change the Placement Profile schema for this feature.

Rejected for v0.2:

- embedded receipt fields in source profiles
- raw source profile hashing
- raw schema hashing
- external artifact hashing
- workspace manifest resolution
- cross-record reference validation
- DAG/topological graph compilation
- semantic/NLP validation
- runtime enforcement
- institutional approval logic

## 14. Implementation Readiness

Implementation may proceed only if it incorporates this addendum.

Minimum implementation acceptance criteria:

1. Structural Execution Receipt terminology is used.
2. Receipt files are separate.
3. Hash scope is `NORMALIZED_CHECKER_OUTPUT_ONLY`.
4. SHA-256 is the only supported algorithm.
5. Normalized-output comparison mode does not claim full recomputation.
6. Full source recompute mode re-runs the checker from source profile and schema.
7. Receipt emission preserves checker exit codes.
8. Receipt verification outputs preserve explicit non-claims.
9. No Placement Profile schema change is introduced.
10. Full regression suite passes.

## 15. Status

This document is a design addendum.

No schema change is approved by this document.

No checker change is approved by this document.

No runtime behavior is introduced by this document.

No legal, compliance, audit, safety, graph, external artifact, or institutional authority is claimed by this document.

Final status:

`V0_2_STRUCTURAL_EXECUTION_RECEIPTS_DESIGN_ADDENDUM_ONLY_NOT_IMPLEMENTED`

