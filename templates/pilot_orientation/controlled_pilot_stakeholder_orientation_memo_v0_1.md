# Controlled Pilot Stakeholder Orientation Memo Template v0.1

Pilot name: [INSERT PILOT NAME]
Institution: [INSERT INSTITUTION NAME]
Fork package tag: [INSERT TAG]
Fork package commit: [INSERT COMMIT]
Dry-run receipt reference: [INSERT RECEIPT REF]
Dry-run receipt SHA-256: [INSERT RECEIPT SHA-256]
Dry-run summary reference: [INSERT SUMMARY REF]
Dry-run summary SHA-256: [INSERT SUMMARY SHA-256]
Orientation date: [INSERT DATE]

## Orientation purpose

This orientation explains how stakeholders should read Fork controlled-pilot artifacts.

Fork controlled-pilot artifacts preserve structural evidence boundaries. They do not authorize live ingestion.

## Required boundary statement

Controlled-pilot readiness remains inside Fork.

Live-ingestion authorization remains exclusively with the institution.

Fork may verify that the controlled-pilot package, dry-run outputs, approval artifacts, hash bindings, non-claims, and structural handoff boundaries are coherent.

Fork does not issue, populate, validate, or certify institutional authorization for live ingestion.

## Readiness vocabulary

The controlled-pilot readiness gate may emit:

```text
CONTROLLED_PILOT_PACKAGE_STRUCTURALLY_READY
CONTROLLED_PILOT_PACKAGE_STRUCTURALLY_INCOMPLETE
```

`CONTROLLED_PILOT_PACKAGE_STRUCTURALLY_READY` is structural only.

It is not legal, clinical, compliance, privacy, security, operational, production, or live-ingestion authorization.

## Live-ingestion external reference

`LIVE_INGESTION_AUTHORIZATION_EXTERNAL_REFERENCE` names the external institutional authorization boundary.

The presence of this template or reference has zero authorization valence by itself.

Fork must not issue, populate, validate, or be treated as the system of record for live-ingestion authorization.

## Stakeholder acknowledgment

Each stakeholder should acknowledge:

- I understand that Fork controlled-pilot artifacts preserve structural evidence boundaries only.
- I understand that `CONTROLLED_PILOT_PACKAGE_STRUCTURALLY_READY` is not live-ingestion authorization.
- I understand that Fork does not issue, populate, validate, or certify institutional authorization for live ingestion.
- I understand that the institution retains legal, compliance, privacy, security, clinical or utilization-management, operational, and production-deployment authority.
- I understand that Fork outputs may support institutional review but do not replace institutional approval.

## Stakeholder signatures

| Name | Role | Function | Signature / approval reference | Timestamp |
|------|------|----------|--------------------------------|-----------|
| [INSERT] | Legal        | [INSERT] | [INSERT] | [INSERT] |
| [INSERT] | Compliance   | [INSERT] | [INSERT] | [INSERT] |
| [INSERT] | Privacy / Security | [INSERT] | [INSERT] | [INSERT] |
| [INSERT] | Operations   | [INSERT] | [INSERT] | [INSERT] |
| [INSERT] | Clinical / UM (if applicable) | [INSERT] | [INSERT] | [INSERT] |

## Template non-claims

This template does not authorize live ingestion, certify production readiness, certify source truth, certify completeness, certify legal admissibility, certify lawfulness, certify regulatory compliance, certify HIPAA compliance, certify medical correctness, certify clinical appropriateness, certify utilization-management sufficiency, or replace institutional approval.
