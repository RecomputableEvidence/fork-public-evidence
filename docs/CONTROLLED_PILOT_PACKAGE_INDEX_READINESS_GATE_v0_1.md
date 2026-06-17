# Controlled Pilot Package Index / Readiness Gate v0.1

## Purpose

The Controlled Pilot Readiness Gate verifies that the controlled-pilot package exists and is structurally coherent before design-partner handoff or pilot-readiness review.

The gate checks required documents, schemas, tools, templates, fixtures, and tests. It also runs integration checks over the nightly batch checker, pilot dry-run harness, and pilot approval artifact checker.

## Package index

Machine-readable package index:

```text
pilot_package/controlled_pilot_package_index_v0_1.json
```

## Schema

```text
schemas/controlled_pilot_readiness_gate_v0_1.schema.json
```

## Checker

```text
tools/check_controlled_pilot_readiness_gate.py
```

## Gate result

The readiness gate may emit:

- `CONTROLLED_PILOT_PACKAGE_STRUCTURALLY_READY`
- `CONTROLLED_PILOT_PACKAGE_STRUCTURALLY_INCOMPLETE`

## Scope

A ready result means the package's required structural artifacts exist and the executable pilot-ingestion checks pass.

It does not authorize live ingestion, certify production readiness, certify source truth, certify legal admissibility, certify HIPAA compliance, certify medical correctness, certify regulatory compliance, or replace institutional approval.

## Readiness non-claims

The readiness receipt preserves non-claims stating that package readiness does not authorize live ingestion, does not certify production readiness, does not certify source truth, and does not replace institutional approval.

## Stakeholder orientation memo

The controlled-pilot package includes a stakeholder orientation memo explaining how legal, compliance, audit, risk, security, clinical, utilization-management, operational, and engineering stakeholders should read Fork controlled-pilot artifacts.

The memo preserves the distinction that controlled-pilot readiness remains inside Fork while live-ingestion authorization remains exclusively with the institution.
