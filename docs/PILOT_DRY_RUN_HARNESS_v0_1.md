# Pilot Dry-Run Harness v0.1

## Purpose

The Pilot Dry-Run Harness provides the executable gate between the pilot data-handling package and live pilot ingestion.

It processes a synthetic or redacted nightly batch export using the Nightly Batch Export / Append-Only Drop Schema v0.1.1 checker, emits the batch validation receipt, and produces a dry-run summary that can support institutional review before live ingestion is authorized.

The dry-run harness is not a production ingestion service, runtime interceptor, workflow controller, compliance engine, legal authority, clinical reviewer, or audit substitute.

## Inputs

Required inputs:

- nightly batch manifest JSON;
- nightly batch records JSONL;
- Nightly Batch Export / Append-Only Drop Schema v0.1.1;
- approved-source configuration embedded in the manifest;
- pilot approval artifact identifiers embedded in the manifest.

## Outputs

The harness writes two deterministic artifacts:

1. `fork_batch_validation_receipt_<batch_id>.json`

   The receipt emitted by `tools/check_nightly_batch_export.py`.

2. `fork_pilot_dry_run_summary_<batch_id>.json`

   A dry-run summary that reports gate status, counts, limitations, errors, manual-review candidates, non-claims, and whether unapproved source content was detected.

## Gate posture

A dry run may result in:

- `DRY_RUN_GATE_PASSED`
- `DRY_RUN_GATE_PASSED_WITH_LIMITATIONS`
- `DRY_RUN_GATE_FAILED`

A dry-run pass means only that the synthetic or redacted batch satisfied the structural dry-run gate.

A dry-run pass does not authorize live ingestion by itself. Live ingestion remains subject to completion of the Dry-Run Approval Artifact by the institution's technical sponsor and privacy or security sponsor.

## Failure conditions

The dry-run gate fails if:

- the batch validation receipt is `REJECTED_*`;
- the manifest is not a dry-run phase unless live phase is explicitly allowed;
- full source content is included;
- record-level full source content is included;
- schema errors are present;
- unapproved content is detected;
- the receipt cannot be emitted.

## Limitation handling

The dry-run gate may pass with limitations if the batch is accepted with limitations, including:

- missing hash with `hash_not_available_reason`;
- unknown source excluded by checker;
- other checker limitations preserved in the receipt.

Limitations remain structural signals. They do not determine source truth, legal sufficiency, medical correctness, compliance, clinical appropriateness, completeness, lawfulness, or admissibility.

## Manual-review candidates

The dry-run summary may list manual-review candidates derived from receipt limitations and errors.

Fork may surface the structural condition. The institution determines the operational response.

## Non-claims

The dry-run harness does not claim:

- live ingestion authorization;
- production readiness;
- HIPAA compliance certification;
- BAA sufficiency;
- source truth;
- factual completeness;
- legal admissibility;
- lawfulness;
- regulatory compliance;
- medical correctness;
- clinical appropriateness;
- utilization-management sufficiency;
- institutional approval;
- runtime authorization;
- replacement of audit trails;
- replacement of legal holds;
- replacement of discovery processes;
- replacement of regulator-facing documentation;
- replacement of appeal or utilization-management processes.

Fork preserves structural evidence boundaries. The institution remains responsible for legal, privacy, security, clinical, compliance, operational, and records-governance determinations.
