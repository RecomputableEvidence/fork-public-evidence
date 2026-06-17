# Pilot Approval Artifact Templates v0.1

## Purpose

This document defines the four named approval artifacts required to support a controlled Fork pilot before live ingestion begins.

These artifacts complete the controlled pilot paper trail:

```text
what Fork may see
→ how Fork hashes it
→ dry-run approval before live ingestion
→ stakeholder acknowledgment of structural posture
```

## Required artifacts

### 1. Redaction Scope Artifact

Defines what Fork may receive in redacted-content mode and what must be removed, masked, excluded, or preserved only by reference.

The institution defines the redaction scope and identifies the approval authority by role or title. Fork does not determine whether redaction is legally, clinically, operationally, or privacy sufficient.

### 2. Pilot Canonicalization Record

Defines the approved hashing and canonicalization or byte-preservation procedure for the pilot.

Fork may provide a reference canonicalization procedure, but the institution-approved Pilot Canonicalization Record controls the pilot implementation.

### 3. Dry-Run Approval Artifact

Records institutional review of the synthetic or redacted dry run before live ingestion begins.

This artifact confirms batch processing, packet creation, hashing or hash-limitation handling, verification, access logging, free-text scope signaling, review routing, and that no unapproved source content was captured during dry-run ingestion.

### 4. Written Orientation Artifact

Records stakeholder acknowledgment that Fork/RGV `PASS`, `FAIL`, and `INDETERMINATE` are structural postures only.

The acknowledgment may be captured by countersignature, approved procurement workflow, written email confirmation, or institution-defined record.

## Machine schema

```text
schemas/pilot_approval_artifacts_v0_1.schema.json
```

## Checker

```text
tools/check_pilot_approval_artifacts.py
```

## Templates

```text
templates/pilot_approval_artifacts/redaction_scope_artifact_v0_1.template.json
templates/pilot_approval_artifacts/pilot_canonicalization_record_v0_1.template.json
templates/pilot_approval_artifacts/dry_run_approval_artifact_v0_1.template.json
templates/pilot_approval_artifacts/written_orientation_artifact_v0_1.template.json
```

## Artifact non-claims

Approval artifacts do not certify:

- source truth;
- legal sufficiency;
- HIPAA compliance;
- medical correctness;
- clinical appropriateness;
- regulatory compliance;
- completeness;
- institutional approval beyond the artifact's stated scope;
- runtime authorization beyond the artifact's stated scope;
- replacement of audit trails, legal holds, discovery processes, regulator-facing documentation, appeal processes, or utilization-management processes.

Fork preserves structural evidence boundaries. The institution remains responsible for legal, privacy, security, clinical, compliance, operational, and records-governance determinations.
