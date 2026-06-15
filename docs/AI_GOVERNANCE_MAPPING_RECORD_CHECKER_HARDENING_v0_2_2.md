# AI Governance Mapping Record Checker Hardening v0.2.2

Status: `FINAL_STABILIZATION_PATCH`

This document describes the v0.2.2 stabilization patch for the AI Governance Mapping Record checker.

v0.2.2 is intentionally narrow. It does not expand Fork into a policy engine, legal sufficiency checker, compliance checker, audit substitute, decision validator, runtime controller, cross-record graph compiler, external artifact resolver, or semantic intent engine.

## What v0.2.2 adds

- Static machine-readable error codes on failed checks.
- Local multi-hop safe-handoff dependency cycle detection inside a single record.
- Parser-boundary fixtures for malformed JSON, non-object JSON, empty objects, and malformed escape sequences.
- Performance smoke coverage for large synthetic records.
- Output comparison guidance for normalized verification results.
- A changelog entry tying v0.1, semantic alignment, v0.2, v0.2.1, and v0.2.2 together.
- Documentation-level overclaim language regression coverage.

## Boundary of the local cycle check

`LOCAL_HANDOFF_CYCLE_GUARD` detects cycles declared through `handoff_dependency_ids` among safe handoffs inside one mapping record.

It may detect examples such as:

```text
SAFE_HANDOFF_A -> SAFE_HANDOFF_B -> SAFE_HANDOFF_C -> SAFE_HANDOFF_A
```

This is not a cross-record DAG compiler. It does not verify graph-wide cycle immunity across multiple files, repositories, tenants, workflows, ledgers, or external systems.

## Error-code posture

Each `FAIL` check includes a static `error_code` suitable for deterministic downstream tooling. Error codes are diagnostic labels only. They are not legal conclusions, compliance conclusions, audit findings, or institutional decisions.

Examples:

- `ERR_DUPLICATE_OR_MISSING_ID`
- `ERR_SAFE_HANDOFF_SELF_REFERENCE`
- `ERR_LOCAL_HANDOFF_CYCLE`
- `ERR_SCHEMA_VERSION_MISMATCH`
- `ERR_JSON_PARSE`
- `ERR_SCHEMA_FILE_MISSING`
- `ERR_RESTRICTED_AUTHORITY_CLAIM`

## Parser boundary

Fork uses Python's JSON parser for JSON parsing. Fork's custom logic begins after parse and structural loading. v0.2.2 strengthens the checker behavior around parser-boundary failures, but it does not claim a formal context-free grammar, complete parser hardening, or denial-of-service resistance.

## Unicode-aware lexical guardrail boundary

v0.2.2 preserves Unicode-aware lexical normalization for restricted claim checks, including normalization of combining characters and common hyphen variants. This is not semantic intent detection and not exhaustive homoglyph protection.

## Normalized output comparison

Normalized outputs are intended for cross-environment comparison. They exclude environment-specific fields such as timestamp, absolute paths, platform, Python version, and file sizes. They preserve semantic verification fields such as checker identity, checker version, overall status, hashes, checks, warnings, errors, and indeterminate signals.

## Non-claims preserved

Fork v0.2.2 does not claim:

- legal admissibility;
- compliance satisfaction;
- audit sufficiency;
- AI output correctness;
- decision correctness;
- source completeness;
- runtime control;
- execution permissioning;
- policy authority;
- institutional authority;
- graph-wide cycle immunity;
- external artifact verification;
- semantic intent understanding.

## Public description

Safe public language:

> Fork v0.2.2 is a final stabilization patch for the AI Governance Mapping Record checker. It adds static error codes, local multi-hop safe-handoff cycle detection, parser-boundary coverage, performance smoke coverage, normalized output comparison guidance, and overclaim-language regression checks while preserving Fork's bounded non-claim posture.
