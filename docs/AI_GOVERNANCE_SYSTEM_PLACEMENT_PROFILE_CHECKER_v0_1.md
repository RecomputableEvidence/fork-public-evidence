# AI Governance System Placement Profile Checker v0.1

Status: Initial bounded checker  
Related doctrine: `docs/AI_GOVERNANCE_SYSTEM_PLACEMENT_PROFILE_v0_1.md`  
Related schema/fixtures: `ai-governance-system-placement-profile-schema-fixtures-v0.1`  
Scope: Structural and boundary validation only

## Purpose

This checker validates AI Governance Mapping Record: System Placement Profile v0.1 records against a narrow structural and boundary contract.

It exists to verify that a placement profile is structurally interpretable, preserves explicit claim/non-claim boundaries, declares local evidence references, and does not leak restricted authority claims into claim-bearing fields.

It does not validate whether the underlying governance system is correct, safe, compliant, legally sufficient, audit sufficient, production ready, or institutionally authorized.

## Checker Statuses

- `PASS`: the placement profile is structurally valid and boundary-consistent under v0.1 checker scope.
- `FAIL`: the placement profile violates required structure or boundary rules under v0.1 checker scope.
- `INDETERMINATE`: the placement profile is structurally interpretable but declares active unresolved unknowns that prevent closure under v0.1 checker scope.

## Implemented Checks

- `SCHEMA_FILE_PRESENT`
- `JSON_PARSE`
- `REQUIRED_FIELDS_PRESENT`
- `PROFILE_VERSION_VALID`
- `ROLE_CLASSIFICATION_VALID`
- `VERIFICATION_STATE_DECLARED`
- `CLAIM_NONCLAIM_ARRAYS_PRESENT`
- `CLAIM_NONCLAIM_DISJOINT`
- `CLAIM_UNKNOWN_DISJOINT`
- `NONCLAIM_UNKNOWN_DISJOINT`
- `RESTRICTED_AUTHORITY_CLAIM_GUARD`
- `UNIQUE_IDS`
- `ID_FORMAT_VALID`
- `CLAIM_EVIDENCE_BASIS_PRESENT`
- `LOCAL_REFERENCE_INTEGRITY`
- `HANDOFF_ROLE_REFERENCES_VALID`
- `UNRESOLVED_UNKNOWNS_STATUS`
- `NON_TRANSITIVE_CLAUSES_PRESENT`

## Boundary

The checker does not perform:

- semantic truth validation;
- legal sufficiency validation;
- compliance sufficiency validation;
- audit sufficiency validation;
- model safety validation;
- runtime enforcement;
- institutional approval;
- external artifact resolution;
- cross-record graph validation.

## Claim-to-Evidence Boundary

The checker verifies that each supported claim references declared local evidence inputs.

This is only local reference validation. It does not prove that the referenced evidence actually substantiates the claim.

## Non-Transitive Claim Boundary

The checker preserves the doctrine that governance claims are non-transitive unless explicitly declared, bounded, evidenced, and handed off.

It checks the structure required for that boundary, but it does not decide whether downstream reliance is appropriate.