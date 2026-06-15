# AI Governance Mapping Record Schema and Checker v0.1

Status: Engineering Artifact  
Version: v0.1  
Scope: Machine-readable claim-boundary mapping records

## Purpose

This artifact turns the AI Governance Mapping System from doctrine into a machine-checkable record format.

The schema and checker exist to verify that a system mapping record declares:

- input assumptions,
- supported claims,
- explicit non-claims,
- emitted artifacts,
- consumable artifacts,
- verification model,
- evaluation boundary,
- authority boundary,
- dependency boundary,
- unknowns,
- failure states,
- safe handoffs,
- prohibited claim inheritance,
- re-verification requirements,
- institutional dependencies.

## Core rule

A mapping record must not allow claims to silently cross a system boundary.

Every safe handoff must preserve:

- claims that may travel,
- claims that must not transfer,
- non-claims that must travel,
- unknowns that must travel,
- re-verification requirements.

## Files

Schema:

- schemas/ai_governance_system_mapping_record_v0_1.schema.json

Checker:

- tools/check_ai_governance_mapping_record_v0_1.py

Fixtures:

- examples/ai_governance_system_mapping/records/VALID_FORK_MAPPING_RECORD_v0_1.json
- examples/ai_governance_system_mapping/records/INVALID_MISSING_NON_CLAIMS_v0_1.json
- examples/ai_governance_system_mapping/records/INVALID_CLAIM_LEAKAGE_v0_1.json
- examples/ai_governance_system_mapping/records/INDETERMINATE_UNRESOLVED_DEPENDENCY_v0_1.json

Tests:

- tests/test_ai_governance_mapping_record_v0_1.py

## Checker status values

PASS means the mapping record satisfies the v0.1 structural and semantic boundary checks.

FAIL means the record violates required structure or boundary rules.

INDETERMINATE means the record is structurally inspectable but contains unresolved dependencies, unknowns, unavailable evidence, or review-required states that prevent clean PASS.

## What this checker verifies

The checker verifies:

- record file exists,
- schema file exists or built-in checks are available,
- JSON parses as an object,
- schema version is pinned,
- required fields are present,
- top-level field types are correct,
- explicit non-claims are present,
- prohibited claim inheritance is present,
- supported claims and explicit non-claims are disjoint,
- unknowns are present,
- unresolved dependencies are surfaced as INDETERMINATE,
- authority boundary is declared,
- restricted authority/correctness/compliance claims are guarded,
- safe handoffs carry non-transfer, non-claim, unknown, and re-verification constraints,
- Fork-specific records preserve Fork's canonical non-claims.

## What this checker does not verify

This checker does not verify:

- AI output correctness,
- decision correctness,
- source completeness,
- legal admissibility,
- compliance satisfaction,
- audit sufficiency,
- market adoption,
- ecosystem consensus,
- institutional authority,
- runtime enforcement,
- production interoperability.

## Run

From the repository root:

    python .\tools\check_ai_governance_mapping_record_v0_1.py --record .\examples\ai_governance_system_mapping\records\VALID_FORK_MAPPING_RECORD_v0_1.json --output .\output\ai_governance_mapping_record_checks\valid_fork_result.json

Expected output:

    AI_GOVERNANCE_MAPPING_RECORD_CHECK_PASS

Run tests:

    python -m unittest discover -s tests -p "test_ai_governance_mapping_record_v0_1.py" -v

## Boundary

This is not a governance platform, compliance engine, legal admissibility framework, or audit substitute.

It is a bounded checker for claim-boundary mapping records.