# Checker Normalized Output Comparison Guide v0.2.2

This guide defines how to compare normalized AI Governance Mapping Record checker outputs.

## Semantic comparison fields

The following fields are part of normalized output comparison:

- `checker_name`
- `checker_version`
- `overall_status`
- `record_sha256`
- `schema_sha256`
- `checks`
- `warnings`
- `errors`
- `indeterminate_signals`

## Excluded environment fields

The following fields are intentionally excluded from normalized outputs:

- `checked_at_utc`
- `record_path`
- `schema_path`
- `record_size_bytes`
- `schema_size_bytes`
- `environment.python_version`
- `environment.platform`

## Comparison rule

Two normalized outputs are equivalent when their semantic comparison fields match byte-for-byte after deterministic JSON serialization with sorted keys and UTF-8 encoding.

## Non-claim

Normalized output equivalence proves only that the checker produced the same bounded verification result for the same record/schema content. It does not prove legal admissibility, compliance satisfaction, audit sufficiency, AI output correctness, decision correctness, source completeness, external artifact existence, or institutional authority.
