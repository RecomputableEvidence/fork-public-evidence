# CCEC Governance Interoperability Profile v0.1 Release Notes

## Release

`ccec-governance-interoperability-profile-v0.1`

## Commit

`d4c6109`

## Summary

This release adds the CCEC Governance Interoperability Profile v0.1.

The profile defines how Claim Consumption Event Contracts may be referenced by surrounding governance systems without being converted into approval, truth, safety, compliance, legal sufficiency, institutional authorization, policy satisfaction, risk acceptance, or authority transfer.

It extends the claim-boundary stack from local claim consumption into bounded institutional interoperability.

## What this release adds

This release introduces:

- `docs/CCEC_GOVERNANCE_INTEROPERABILITY_PROFILE_v0_1.md`
- `schemas/ccec_governance_interoperability_profile_v0_1.schema.json`
- `schemas/ccec_governance_interoperability_checker_output_v0_1.schema.json`
- `examples/ccec_governance_interoperability/valid_grc_register_reference.json`
- `examples/ccec_governance_interoperability/valid_audit_evidence_reference.json`
- `examples/ccec_governance_interoperability/invalid_compliance_oracle_mapping.json`
- `examples/ccec_governance_interoperability/invalid_authority_inheritance.json`
- `tools/check_ccec_governance_interoperability.py`
- `tests/test_ccec_governance_interoperability_v0_1.py`
- `output/ccec_governance_interoperability/valid_grc_register_reference_output.json`
- `output/ccec_governance_interoperability/valid_audit_evidence_reference_output.json`

## Why it matters

A Claim Consumption Event Contract records local reliance behavior.

It can show that a receiving workflow consumed a bounded source artifact, preserved non-claims, retained unresolved gaps, and named a local decision owner.

However, surrounding governance systems still need a safe way to ingest or reference that record.

Without an interoperability profile, a GRC tool, audit register, policy workflow, risk register, legal review queue, or vendor-risk system could collapse a bounded CCEC reference into an approval-like or compliance-like status.

This release prevents that collapse structurally.

## Core doctrine

A CCEC interoperability profile defines what surrounding governance systems may reference from a Claim Consumption Event Contract without inheriting authority, approval, truth, safety, compliance, legal sufficiency, policy satisfaction, or risk acceptance.

Evidence may enter the governance system.

Non-claims and unresolved gaps must enter with it.

Authority remains local.

## Permitted mappings

The profile permits bounded references such as:

- evidence reference;
- boundary record reference;
- local reliance record;
- unresolved gap reference;
- non-claim reference;
- decision owner reference;
- boundary effect reference;
- source artifact reference;
- receiving context reference.

These mappings preserve evidence-boundary structure. They do not create approval, compliance, legal, safety, risk, or authority status.

## Prohibited mappings

The profile prohibits mapping a CCEC into:

- approval status;
- truth status;
- safety status;
- compliance status;
- legal sufficiency status;
- institutional authorization status;
- policy satisfaction status;
- risk acceptance status;
- authority transfer;
- claim expansion by mapping;
- automated control decision.

## Checker behavior

`tools/check_ccec_governance_interoperability.py` validates the profile structurally.

It checks:

- JSON parseability;
- schema conformance;
- required permitted and prohibited mappings;
- mapping-rule consistency;
- forbidden oracle-like target fields;
- authority-inheritance prohibition;
- unresolved-gap preservation;
- machine-readable non-claims;
- checker output contract conformance.

It does not validate:

- truth of the source CCEC;
- correctness of an external governance decision;
- compliance of an external system;
- safety of an external system;
- legal sufficiency of an external decision;
- institutional authority of an external owner;
- policy satisfaction;
- risk acceptance.

## Validation

The release was validated with:

```text
python -m pytest tests/test_ccec_governance_interoperability_v0_1.py tests/test_claim_consumption_event_v0_1.py
```

Result:

```text
16 passed
```

The release tag is present on the remote:

```text
ccec-governance-interoperability-profile-v0.1
```

## Relationship to prior release

This release builds directly on:

```text
claim-consumption-event-contract-v0.1
```

The Claim Consumption Event Contract records receiving-side reliance.
The Governance Interoperability Profile defines how that bounded reliance record may enter surrounding governance systems without becoming an approval, compliance, safety, truth, legal sufficiency, authority transfer, policy satisfaction, or risk acceptance oracle.