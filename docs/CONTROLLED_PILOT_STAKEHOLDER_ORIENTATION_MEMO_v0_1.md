# Controlled Pilot Stakeholder Orientation Memo v0.1

## Purpose

This memo explains how legal, compliance, audit, risk, security, clinical, utilization-management, operational, and engineering stakeholders should read Fork controlled-pilot artifacts.

The controlled pilot uses Fork as an out-of-band evidence-boundary sidecar. Fork preserves structural records of what was observed, what evidence or artifacts were referenced, what claims were made, what claims were not made, what downstream reliance occurred, and whether the controlled-pilot package structurally verifies.

Fork does not decide whether live ingestion may proceed.

## Core distinction

Controlled-pilot readiness remains inside Fork.

Live-ingestion authorization remains exclusively with the institution.

Fork may verify that the controlled-pilot package, dry-run outputs, approval artifacts, hash bindings, non-claims, and structural handoff boundaries are coherent.

Fork does not issue, populate, validate, or certify institutional authorization for live ingestion.

## How to read Fork readiness

Structural readiness refers only to Fork's schema, hash, receipt, template, package-index, and checker validation. It does not mean workflow readiness, clinical readiness, operational readiness, compliance readiness, production readiness, or live-ingestion authorization.

A Fork readiness result means the controlled-pilot package is structurally coherent within Fork's declared scope.

The current readiness vocabulary is:

```text
CONTROLLED_PILOT_PACKAGE_STRUCTURALLY_READY
CONTROLLED_PILOT_PACKAGE_STRUCTURALLY_INCOMPLETE
```

`CONTROLLED_PILOT_PACKAGE_STRUCTURALLY_READY` means the package passed Fork's structural checks (structural verification only, not operational readiness).
It does not mean the workflow is legally sufficient, clinically appropriate, HIPAA compliant, operationally approved, production ready, complete, safe, lawful, admissible, or authorized for live ingestion.

## How to read dry-run approval

A dry-run approval artifact may bind to exact dry-run outputs by SHA-256 hash.

That binding means the approval artifact refers to the specific dry-run receipt and dry-run summary identified by those hashes.

The binding does not certify that the source material is true, that the dry-run represents all production conditions, that later external state has not changed, or that live ingestion is authorized.

## How to read the live-ingestion external reference

Fork may include or validate a `LIVE_INGESTION_AUTHORIZATION_EXTERNAL_REFERENCE`.

This reference names the external institutional authorization boundary.

The presence of this template or reference confers zero authorization by its mere existence. It has no legal, operational, clinical, compliance, or live-ingestion authorization effect by itself.

Fork must not issue, populate, validate, or be treated as the system of record for live-ingestion authorization.

Only the institution's own governance, change-control, legal, clinical, privacy, security, compliance, operational, and records-management processes may decide whether to start, pause, or stop live ingestion.

## Stakeholder retained authority

The institution retains authority over:

- legal sufficiency;
- compliance sufficiency;
- HIPAA, privacy, and security sufficiency;
- clinical or utilization-management sufficiency, where applicable;
- operational readiness;
- production deployment;
- live-ingestion authorization;
- reviewer judgment;
- source-system truth and completeness;
- appeal, audit, retention, and remediation processes.

Fork does not replace those institutional functions.

## Required reading posture

Stakeholders should read Fork artifacts as structural evidence-boundary records.

They should not read Fork artifacts as:

- legal opinions;
- compliance approvals;
- clinical determinations;
- utilization-management determinations;
- HIPAA certifications;
- operational go-live approvals;
- production-readiness certifications;
- source-truth certifications;
- institutional authorizations;
- replacements for existing audit, appeal, legal, clinical, compliance, or records-governance processes.

## Practical review questions

Before using Fork outputs in a controlled pilot review, stakeholders should ask:

1. What exact package, commit, tag, dry-run receipt, and dry-run summary are being reviewed?
2. Do the approval artifact hashes match the dry-run outputs being discussed?
3. What claims does Fork preserve?
4. What claims does Fork explicitly not make?
5. Which institutional authority owns live-ingestion authorization?
6. Where is the institution's external authorization record, if live ingestion is being considered?
7. Has anyone described structural readiness as legal, clinical, compliance, operational, or production approval?

If the answer to question 7 is yes, that description should be corrected before the package is used in a pilot decision process.

## Canonical orientation statement

Fork structural-readiness receipts may be used as inputs to institutional approval processes.

They must not be used or represented as institutional approval, legal opinion, clinical authorization, compliance authorization, HIPAA certification, operational approval, production-readiness certification, source-truth certification, or live-ingestion authorization.

## Acknowledgment language

A stakeholder acknowledging this memo should confirm:

- I understand that Fork controlled-pilot artifacts preserve structural evidence boundaries only.
- I understand that `CONTROLLED_PILOT_PACKAGE_STRUCTURALLY_READY` is not live-ingestion authorization.
- I understand that Fork does not issue, populate, validate, or certify institutional authorization for live ingestion.
- I understand that the institution retains legal, compliance, privacy, security, clinical or utilization-management, operational, and production-deployment authority.
- I understand that Fork outputs may serve as structural evidence during institutional review, but do not constitute or replace institutional approval.

## Memo non-claims

This memo does not authorize live ingestion, certify production readiness, certify source truth, certify completeness, certify legal admissibility, certify lawfulness, certify regulatory compliance, certify HIPAA compliance, certify medical correctness, certify clinical appropriateness, certify utilization-management sufficiency, or replace institutional approval.

This memo explains how to read Fork controlled-pilot artifacts without expanding Fork's structural readiness outputs into institutional authorization.
