# Controlled Pilot Seam Hardening v0.1.1

## Purpose

This hardening layer closes the seam between Fork dry-run readiness and external institutional live-ingestion authorization.

The goal is to make it mechanically difficult to misread Fork structural readiness as legal, clinical, compliance, operational, or institutional authorization.

## Hardening changes

### 1. Structural readiness vocabulary

The package readiness gate now emits structural readiness language:

- `CONTROLLED_PILOT_PACKAGE_STRUCTURALLY_READY`
- `CONTROLLED_PILOT_PACKAGE_STRUCTURALLY_INCOMPLETE`

Fork does not emit a generic operational "ready" signal.

### 2. External live-ingestion authorization boundary

Readiness receipts include a live-ingestion authorization boundary object stating that Fork does not assert live ingestion authorization, does not issue live ingestion authorization, requires external institutional authorization, and does not validate the sufficiency of that external authorization.

### 3. Dry-run output hash binding

The Dry-Run Approval Artifact binds to exact dry-run outputs by SHA-256 hash:

- batch validation receipt hash;
- dry-run summary hash.

The approval artifact checker fails if the referenced dry-run outputs do not exist or if their computed hashes do not match the approved artifact.

### 4. Retained institutional authority acknowledgment

The Dry-Run Approval Artifact and Written Orientation Artifact require exact retained-authority booleans. The institution must acknowledge that Fork is not the decision authority and that the institution retains clinical, compliance, legal, operational, and utilization-management authority.

### 5. Live-ingestion authorization external reference template

A fifth approval artifact template names the live-ingestion authorization gap without allowing Fork to fill it.

Fork may validate that the boundary is named. Fork does not issue or validate the institution's live-ingestion authorization.

Fork does not issue the authorization. Fork names the external authorization boundary and preserves that Fork readiness is not live-ingestion authorization.

## Non-claims

This seam hardening does not authorize live ingestion, certify production readiness, certify source truth, certify completeness, certify legal admissibility, certify lawfulness, certify regulatory compliance, certify HIPAA compliance, certify medical correctness, certify clinical appropriateness, certify utilization-management sufficiency, or replace institutional approval.

Fork preserves the boundary of what its own structural readiness outputs are allowed to mean.
