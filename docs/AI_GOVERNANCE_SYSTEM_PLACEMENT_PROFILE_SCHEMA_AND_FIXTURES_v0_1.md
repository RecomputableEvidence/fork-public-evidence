# AI Governance System Placement Profile Schema and Fixtures v0.1

Status: Initial schema and fixture contract  
Related doctrine: `docs/AI_GOVERNANCE_SYSTEM_PLACEMENT_PROFILE_v0_1.md`  
Scope: Minimal machine-readable schema plus synthetic fixtures  
Not a checker: This artifact set does not validate semantic truth, legal sufficiency, compliance satisfaction, audit sufficiency, model safety, runtime enforcement, or institutional authority.

## Purpose

This artifact set begins the machine-readable implementation path for the AI Governance Mapping Record: System Placement Profile v0.1.

It provides:

- a strict JSON Schema for the minimal placement-profile core;
- three valid synthetic placement records;
- six invalid synthetic records representing future checker failure modes;
- one indeterminate synthetic record representing active unresolved unknowns;
- fixture-integrity tests that verify the fixture set is internally coherent.

The schema and fixtures are intentionally narrow. They are a bridge from doctrine to future checker work, not a full checker.

## Minimal Core

The schema requires:

- `profile_version`
- `system_identity`
- `role_classification`
- `authority_boundary`
- `supported_claims`
- `explicit_non_claims`
- `evidence_inputs`
- `evidence_outputs`
- `handoff_requirements`
- `unresolved_unknowns`
- `verification_state`

The optional `non_transitive_clauses` field is included because non-transitivity is central to the doctrine, but the minimal schema does not yet require complex graph semantics.

## Boundary

This schema/fixture set does not claim production readiness, external standardization, semantic claim understanding, legal admissibility, compliance satisfaction, audit sufficiency, model safety, runtime control, external artifact resolution, cross-record graph validation, or institutional authority.

## Next Step

The next appropriate step is a bounded checker that verifies structural and boundary properties against this schema and fixture set, while preserving the doctrine that governance claims are non-transitive unless explicitly declared, bounded, evidenced, and handed off.
