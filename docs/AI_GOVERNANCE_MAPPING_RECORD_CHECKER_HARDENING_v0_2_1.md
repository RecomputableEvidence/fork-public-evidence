# AI Governance Mapping Record Checker Hardening v0.2.1

Status: Precision Hardening Patch  
Version: v0.2.1  
Scope: Edge-case hardening for AI Governance Mapping Record checker v0.2

## Purpose

v0.2.1 is a narrow hardening patch. It does not expand Fork into runtime governance, legal review, compliance certification, audit sufficiency, source-of-record authority, or semantic natural-language understanding.

It responds to v0.2 external pressure-test findings by adding edge-case checks around ID ambiguity, safe-handoff self-reference, combined failure handling, malformed inputs, schema-version mismatch behavior, missing schema behavior, and Unicode-aware lexical restricted-claim detection.

## What v0.2.1 adds

v0.2.1 adds:

- duplicate boundary-item ID detection,
- safe-handoff self-reference detection,
- combined failure-mode fixture coverage,
- schema version mismatch fixture coverage,
- missing schema file graceful failure testing,
- empty object / non-object JSON / malformed JSON tests,
- Unicode-aware lexical normalization for restricted-claim matching,
- v0.2 regression preservation,
- normalized result preservation.

## Clarified boundaries

### Exact disjointness guard

`CLAIM_NONCLAIM_DISJOINT` remains an exact-overlap guard. It checks whether the same normalized statement appears in both supported claims and explicit non-claims.

It is not a semantic paraphrase detector.

### Restricted claim lexical guard

`RESTRICTED_AUTHORITY_CLAIM_GUARD` remains the guard for paraphrased or implied restricted claim leakage. v0.2.1 expands normalization so obvious Unicode, punctuation, hyphenation, and accent variants do not bypass the restricted-claim registry.

This is still lexical hardening, not full natural-language understanding.

### Safe handoff ID integrity

`SAFE_HANDOFF_ID_REFERENCE_INTEGRITY` verifies that safe-handoff references resolve to declared in-record boundary items.

It does not prove external artifact existence, cross-record graph continuity, source-of-record availability, or institutional acceptance.

### Self-reference guard

`SAFE_HANDOFF_SELF_REFERENCE_GUARD` rejects a safe handoff that references its own ID through its reference fields. This prevents an artifact from satisfying its own downstream boundary requirements by circular self-reference.

### Unique ID guard

`UNIQUE_BOUNDARY_ITEM_IDS` rejects duplicate IDs across the record's boundary item arrays. This prevents ambiguous reference resolution.

## Fixtures

v0.2.1 includes:

- `VALID_FORK_MAPPING_RECORD_v0_2_1.json`
- `INVALID_DUPLICATE_ID_v0_2_1.json`
- `INVALID_SAFE_HANDOFF_SELF_REFERENCE_v0_2_1.json`
- `INVALID_COMBINED_FAILURE_MODES_v0_2_1.json`
- `INVALID_SCHEMA_VERSION_MISMATCH_v0_2_1.json`
- `INVALID_UNICODE_RESTRICTED_CLAIM_BYPASS_v0_2_1.json`
- `INDETERMINATE_ACTIVE_UNRESOLVED_UNKNOWN_v0_2_1.json`

## Expected status map

| Fixture | Expected status | Exit code | Primary check |
|---|---:|---:|---|
| `VALID_FORK_MAPPING_RECORD_v0_2_1.json` | PASS | 0 | all required v0.2.1 guards pass |
| `INVALID_DUPLICATE_ID_v0_2_1.json` | FAIL | 1 | `UNIQUE_BOUNDARY_ITEM_IDS` |
| `INVALID_SAFE_HANDOFF_SELF_REFERENCE_v0_2_1.json` | FAIL | 1 | `SAFE_HANDOFF_SELF_REFERENCE_GUARD` |
| `INVALID_COMBINED_FAILURE_MODES_v0_2_1.json` | FAIL | 1 | schema, restricted claim, and safe-handoff reference failures |
| `INVALID_SCHEMA_VERSION_MISMATCH_v0_2_1.json` | FAIL | 1 | `SCHEMA_VERSION_PIN` |
| `INVALID_UNICODE_RESTRICTED_CLAIM_BYPASS_v0_2_1.json` | FAIL | 1 | `RESTRICTED_AUTHORITY_CLAIM_GUARD` |
| `INDETERMINATE_ACTIVE_UNRESOLVED_UNKNOWN_v0_2_1.json` | INDETERMINATE | 2 | `INDETERMINATE_SIGNALS` |

## Non-claims

v0.2.1 does not claim:

- full JSON Schema compliance,
- semantic claim understanding,
- legal admissibility,
- compliance satisfaction,
- audit sufficiency,
- AI output correctness,
- decision correctness,
- source completeness,
- runtime control,
- policy authority,
- institutional authority,
- cross-record graph validation,
- external artifact existence validation,
- production readiness.

## v0.3 candidates intentionally deferred

The following remain out of v0.2.1 scope:

- cross-record DAG validation,
- external artifact/manifest resolution,
- signature verification,
- runtime telemetry bridge,
- semantic/NLP claim inference,
- performance/DoS benchmarking,
- multi-language checker implementations.

## Run

From the repository root:

```powershell
python -m unittest discover -s tests -p "test_ai_governance_mapping_record_v0_2_1.py" -v
python -m unittest discover -s tests -p "test_ai_governance_mapping_record_v0_2.py" -v
python -m unittest discover -s tests -p "test_ai_governance_mapping_record_v0_1.py" -v
python -m unittest discover -s tests -p "test_checker_doctrine_alignment_review_v0_1.py" -v
```

Final intended milestone phrase:

```text
AI_GOVERNANCE_MAPPING_RECORD_CHECKER_HARDENING_V0_2_1_PRECISION_PATCH
```