# Nightly Batch Export / Append-Only Drop Schema v0.1.1

## Purpose

This document defines the first controlled pilot export format for Fork nightly batch ingestion or append-only file drop.

The schema supports out-of-band evidence-boundary preservation from existing workflow artifacts without requiring production runtime coupling, live message interception, write-back into source systems, or default export of full source content.

The preferred pilot mode is hash/reference-only ingestion.

## Schema posture

This schema is an ingestion contract, not a truth, legality, compliance, clinical, or admissibility contract.

A conforming batch means only that the submitted export follows the agreed pilot ingestion shape. A JSON-Schema-conforming record may still be rejected, excluded, or accepted with limitations by Fork validation if it violates pilot approval scope, source approval rules, graph-preservation rules, or other pilot controls.

The JSON Schema is the first-pass structural validator for manifest, record, and validation-receipt shape. It enforces required fields, controlled values, deterministic conditional gates, and non-evaluation constants.

Fork validation behavior remains responsible for checks that depend on pilot configuration, approved-source lists, graph-preservation semantics, source non-claim preservation applicability, authority-chain analysis, and institution-defined review rules.

## Delivery pattern

The recommended first delivery pattern is an append-only directory or object-store drop.

Each batch delivery should include:

- `fork_batch_manifest_<batch_id>.json`
- `fork_batch_records_<batch_id>.jsonl`

Fork may emit:

- `fork_batch_validation_receipt_<batch_id>.json`

Files should be written once and not modified in place. If correction is required, the institution should emit a new batch with a new `batch_id` and a relationship to the prior batch.

## Axis separation

`pilot_phase` identifies pilot state:

- `SYNTHETIC_DRY_RUN`
- `REDACTED_DRY_RUN`
- `LIVE_PILOT`
- `POST_PILOT_REPLAY`

`export_mode` identifies export cadence:

- `NIGHTLY_BATCH_EXPORT`
- `ONE_TIME_BATCH_EXPORT`
- `CORRECTIVE_BATCH_EXPORT`

`delivery.delivery_method` identifies delivery mechanism:

- `APPEND_ONLY_DROP`
- `SECURE_FILE_TRANSFER`
- `OBJECT_STORE_DROP`
- `INSTITUTION_APPROVED_EXPORT_LOCATION`

A synthetic dry run can therefore be delivered through an append-only drop without conflating phase and delivery mechanism.

## Hash posture

SHA-256 hash values must be represented as 64-character hexadecimal strings.

If `hash_value` is present, `hash_not_available_reason` must be `null`.

If `hash_value` is `null`, `hash_not_available_reason` must be a non-empty string.

Both null is invalid. Both populated is invalid.

A missing hash does not mean the source content is false, incomplete, unlawful, inadmissible, clinically incorrect, or noncompliant. It means the structural hash anchor was not available and should be preserved as a limitation.

## Required source non-claims

Each record that carries the required source non-claim boundary must preserve the exact six-ID set:

- `SOURCE_TRUTH_NOT_CLAIMED`
- `FACTUAL_BASIS_NOT_CONFIRMED`
- `WHOLENESS_NOT_ASSERTED`
- `COMPLETENESS_NOT_STATED`
- `ADMISSIBILITY_NOT_INFERRED`
- `LAWFULNESS_NOT_IMPLIED`

These identifiers are inference constraints. They are not decorative disclaimers.

## Free-text scope

During this pilot:

- `nlp_scope` must be `NOT_EVALUATED`
- `free_text_scope` must be `NOT_EVALUATED_FOR_INFERENCE`

Fork does not perform NLP during this pilot to determine whether free text is true, false, sufficient, lawful, clinically correct, compliant, admissible, complete, or contradictory.

## Content exception gates

If `redacted_content_included` is true, `redaction_scope_artifact_id` is required.

If `full_source_content_included` is true, `full_content_exception_id` is required.

Full source content is excluded from the default pilot scope.

## Claim consumption events

Claim consumption events are represented as structured graph relationships. A `boundary_effect` of `EXPANDED` requires:

- `new_claim_node_ref`
- `institutional_authority_ref`
- at least one `evidence_basis_ref`

Fork/RGV PASS may be referenced structurally but may not serve as authority for source truth, factual-basis confirmation, wholeness, completeness, admissibility, lawfulness, compliance, safety, correctness, institutional approval, or runtime authorization.

## Schema location

Machine schema:

`schemas/nightly_batch_export_v0_1_1.schema.json`

Checker:

`tools/check_nightly_batch_export.py`

## Schema non-claims

This schema does not claim:

- production readiness;
- HIPAA compliance certification;
- BAA sufficiency;
- legal admissibility;
- regulatory compliance;
- medical correctness;
- clinical appropriateness;
- factual completeness;
- source truth;
- model quality;
- institutional approval;
- runtime authorization;
- replacement of existing audit trails;
- replacement of legal holds;
- replacement of discovery processes;
- replacement of regulator-facing documentation;
- replacement of utilization-management review;
- replacement of appeal processes.

Fork preserves structural evidence boundaries. The institution remains responsible for legal, privacy, security, clinical, compliance, operational, and records-governance determinations.
