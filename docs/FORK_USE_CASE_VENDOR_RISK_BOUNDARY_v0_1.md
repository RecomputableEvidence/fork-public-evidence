# Fork Use Case: Vendor Risk Boundary v0.1

## Purpose

This use case stages Fork for procurement, vendor risk, third-party due diligence, and vendor approval workflows.

The core boundary is:

> Vendor evidence completeness is not vendor approval, security validation, contract sufficiency, compliance, or risk acceptance.

## Scope and non-scope

Scope: Fork records and checks the structural boundary of this use case, including supported claims, non-claims, evidence references, downstream consumption, unresolved pointers, and added downstream claims.

Non-scope: Fork does not evaluate substantive correctness, safety, compliance, legal sufficiency, approval, risk acceptance, control effectiveness, clinical appropriateness, production readiness, model safety, patient safety, vendor security, or incident closure.

## Scenario

An AI-assisted workflow summarizes vendor questionnaires, SOC reports, insurance certificates, contract exhibits, data-processing terms, security documentation, and unresolved review items.

## Supported claim

The record can support that a vendor-risk packet was assembled from identified evidence references, that the packet contained specific unresolved or resolved items, and that a reviewer consumed the packet.

## Non-claims

Fork does not claim:

- `does_not_claim_vendor_approval`
- `does_not_claim_vendor_security`
- `does_not_claim_contract_sufficiency`
- `does_not_claim_compliance`
- `does_not_claim_risk_acceptance`
- `does_not_claim_approval`

## Boundary-preserved consumption

A procurement, legal, risk, or security reviewer consumes the packet as an evidence inventory and review aid.

Example:

> The reviewer relied on the packet to identify vendor evidence and open questions, not to approve the vendor.

Boundary result:

`BOUNDARY_PRESERVED`

## Boundary-expanding consumption

A downstream actor treats document presence or packet verification as vendor approval.

Example:

> All required documents were present, so the vendor was approved.

Boundary result:

`BOUNDARY_EXPANSION_DETECTED`

## Buyer-facing boundary sentence

Fork can preserve the difference between vendor evidence packet completeness and vendor approval.

## Fork role

Fork may support third-party risk workflows by preserving claim and non-claim boundaries across vendor evidence handoffs. It does not approve vendors, validate vendor security, determine contract sufficiency, determine regulatory compliance, or accept risk.

## Example record

See:

- `examples/fork_use_cases/valid_vendor_risk_boundary_expansion_v0_1.json`