# AI Governance Mapping Record Checker Hardening v0.2

Status: Engineering Artifact  
Version: v0.2  
Scope: Hardening layer for AI Governance System Mapping Record validation

## Purpose

This artifact advances the v0.1 mapping record checker from a declaration-based boundary checker into a stricter v0.2 hardening layer.

v0.2 addresses the major gaps preserved in the v0.1 semantic alignment review:

1. Full schema-equivalent validation without requiring a third-party runtime dependency.
2. ID-reference integrity across safe handoff fields.
3. Paraphrased claim-inheritance detection.
4. Separation of declared unknown classes from active unresolved unknowns.
5. Normalized result output for cross-environment reproducibility.

## Core boundary

This remains a bounded checker.

It verifies record structure, references, restricted claim language, non-claims, safe handoff duties, and indeterminate-state handling.

It does not verify:

- legal admissibility,
- compliance satisfaction,
- audit sufficiency,
- AI output correctness,
- decision correctness,
- source completeness,
- institutional acceptance,
- market validation,
- production readiness.

## Files

Schema:

- `schemas/ai_governance_system_mapping_record_v0_2.schema.json`

Checker:

- `tools/check_ai_governance_mapping_record_v0_2.py`

Fixtures:

- `examples/ai_governance_system_mapping/records_v0_2/VALID_FORK_MAPPING_RECORD_v0_2.json`
- `examples/ai_governance_system_mapping/records_v0_2/INVALID_PARAPHRASED_CLAIM_INHERITANCE_v0_2.json`
- `examples/ai_governance_system_mapping/records_v0_2/INVALID_SAFE_HANDOFF_REFERENCE_GAP_v0_2.json`
- `examples/ai_governance_system_mapping/records_v0_2/INVALID_SCHEMA_NESTED_ADDITIONAL_PROPERTY_v0_2.json`
- `examples/ai_governance_system_mapping/records_v0_2/INDETERMINATE_ACTIVE_UNRESOLVED_UNKNOWN_v0_2.json`

Tests:

- `tests/test_ai_governance_mapping_record_v0_2.py`

Outputs:

- `output/ai_governance_mapping_record_checks_v0_2/*.json`
- `output/ai_governance_mapping_record_checks_v0_2/*_normalized.json`

## v0.2 hardening rules

### 1. Schema-equivalent validation

The checker performs dependency-free validation for the JSON Schema subset used by the v0.2 schema:

- object,
- array,
- string,
- boolean,
- required,
- properties,
- additionalProperties: false,
- items,
- minItems,
- minLength,
- enum,
- const,
- local `$ref` into `$defs`.

This is intentionally called schema-equivalent validation rather than external JSON Schema engine validation.

The purpose is to preserve strict nested validation without adding a package dependency.

### 2. ID-reference integrity

Safe handoffs now carry ID references instead of free-text-only handoff assertions.

Each safe handoff must resolve:

- `allowed_claim_ids` against `supported_claims`,
- `claims_that_must_not_transfer_ids` against `prohibited_claim_inheritance`,
- `non_claim_ids_that_must_travel` against `explicit_non_claims`,
- `unknown_ids_that_must_travel` against `declared_unknown_classes` and `active_unresolved_unknowns`,
- `re_verification_requirement_ids` against `re_verification_requirements`.

A handoff that cites a nonexistent boundary item fails.

### 3. Paraphrased claim-inheritance detection

The checker now detects restricted claim categories through phrase patterns, not only exact canonical terms.

Restricted categories include:

- AI output correctness,
- decision correctness,
- source completeness,
- legal admissibility,
- compliance satisfaction,
- audit sufficiency,
- institutional authority,
- runtime control,
- execution permissioning,
- policy authority,
- risk acceptance.

This is still not full natural-language understanding. It is a hardened lexical guardrail for common claim-leakage phrasing.

### 4. Declared unknown classes vs active unresolved unknowns

v0.1 used a single `unknowns` field.

v0.2 separates:

- `declared_unknown_classes`: categories of uncertainty that must travel with otherwise valid records.
- `active_unresolved_unknowns`: live unresolved unknowns that trigger `INDETERMINATE`.

This prevents a valid record from becoming indeterminate merely because it correctly declares unknown classes.

It also prevents active unresolved unknowns from being silently normalized into PASS.

### 5. Normalized result output

The checker supports:

```powershell
--normalized-output <path>
```

The normalized output excludes environment-specific fields:

- `checked_at_utc`,
- absolute record path,
- absolute schema path,
- platform,
- Python version,
- file size.

It keeps substantive fields:

- checker name,
- checker version,
- overall status,
- record SHA-256,
- schema SHA-256,
- checks,
- warnings,
- errors,
- indeterminate signals.

This makes cross-environment reproduction easier to compare.

## Expected fixture outcomes

| Fixture | Expected exit code | Expected status | Purpose |
|---|---:|---|---|
| `VALID_FORK_MAPPING_RECORD_v0_2.json` | 0 | `PASS` | Valid Fork record with ID-linked safe handoffs and declared unknown classes. |
| `INVALID_PARAPHRASED_CLAIM_INHERITANCE_v0_2.json` | 1 | `FAIL` | Detects legal/compliance claim leakage through paraphrased language. |
| `INVALID_SAFE_HANDOFF_REFERENCE_GAP_v0_2.json` | 1 | `FAIL` | Detects missing ID-reference integrity in safe handoff fields. |
| `INVALID_SCHEMA_NESTED_ADDITIONAL_PROPERTY_v0_2.json` | 1 | `FAIL` | Detects nested strict-schema violation. |
| `INDETERMINATE_ACTIVE_UNRESOLVED_UNKNOWN_v0_2.json` | 2 | `INDETERMINATE` | Distinguishes active unresolved unknowns from declared unknown classes. |

## Run

From the repository root:

```powershell
python .\tools\check_ai_governance_mapping_record_v0_2.py `
  --record .\examples\ai_governance_system_mapping\records_v0_2\VALID_FORK_MAPPING_RECORD_v0_2.json `
  --schema .\schemas\ai_governance_system_mapping_record_v0_2.schema.json `
  --output .\output\ai_governance_mapping_record_checks_v0_2\valid_fork_result.json `
  --normalized-output .\output\ai_governance_mapping_record_checks_v0_2\valid_fork_normalized_result.json
```

Expected output:

```text
AI_GOVERNANCE_MAPPING_RECORD_V0_2_CHECK_PASS
```

Run tests:

```powershell
python -m unittest discover -s tests -p "test_ai_governance_mapping_record_v0_2.py" -v
```

## v0.2 status

This hardening layer is stronger than v0.1 but still bounded.

It should be described as:

```text
A v0.2 machine-checkable boundary record validator with schema-equivalent validation, ID-linked handoff integrity, paraphrased claim-leakage guards, active unknown handling, and normalized reproducibility output.
```

It should not be described as:

```text
A full semantic verifier, legal sufficiency checker, compliance checker, audit checker, policy engine, production governance authority, or runtime controller.
```