# Fork Use Case: Audit Evidence Assembly v0.1

## Purpose

This use case stages Fork for AI-assisted audit, risk, and compliance evidence assembly.

The core boundary is:

> Evidence packet completeness is not control effectiveness, audit opinion, compliance status, remediation sufficiency, or risk acceptance.

## Scenario

An AI-assisted workflow collects control evidence, summarizes artifacts, maps them to a requested audit or compliance control, and routes the packet to a reviewer.

## Supported claim

The record can support that identified evidence artifacts were collected, associated with a control or requirement reference, summarized in an AI-assisted packet, and routed for human review.

## Non-claims

Fork does not claim:

- `does_not_claim_control_effectiveness`
- `does_not_claim_audit_opinion`
- `does_not_claim_compliance`
- `does_not_claim_remediation_sufficiency`
- `does_not_claim_risk_acceptance`
- `does_not_claim_approval`

## Boundary-preserved consumption

A reviewer consumes the packet as evidence inventory and orientation material.

Example:

> The reviewer relied on the packet to locate evidence and understand what was assembled, not to conclude that the control was effective.

Boundary result:

`BOUNDARY_PRESERVED`

## Boundary-expanding consumption

A downstream workflow treats packet verification as evidence that the control is effective or that the organization is compliant.

Example:

> The packet verified, so the control passed.

Boundary result:

`BOUNDARY_EXPANSION_DETECTED`

## Buyer-facing boundary sentence

Fork can preserve the difference between evidence presence, evidence integrity, and substantive control effectiveness.

## Fork role

Fork may support audit and compliance teams by preserving the evidence boundary around AI-assisted evidence assembly. It does not issue audit opinions, evaluate control effectiveness, determine compliance status, approve remediation, or accept risk.

## Example record

See:

- `examples/fork_use_cases/valid_audit_evidence_assembly_v0_1.json`
