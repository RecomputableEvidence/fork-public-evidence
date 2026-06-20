# Fork Use Case: Cyber Triage Boundary v0.1

## Purpose

This use case stages Fork for AI-assisted cybersecurity alert triage, incident summarization, and breach-scope handoffs.

The core boundary is:

> Observed evidence in a triage record is not proof that no breach occurred, that containment succeeded, or that reporting obligations do not exist.

## Scope and non-scope

Scope: Fork records and checks the structural boundary of this use case, including supported claims, non-claims, evidence references, downstream consumption, unresolved pointers, and added downstream claims.

Non-scope: Fork does not evaluate substantive correctness, safety, compliance, legal sufficiency, approval, risk acceptance, control effectiveness, clinical appropriateness, production readiness, model safety, patient safety, vendor security, or incident closure.

## Scenario

An AI-assisted workflow summarizes alerts, log excerpts, endpoint events, network observations, analyst notes, and severity recommendations.

## Supported claim

The record can support that certain logs, alerts, tool outputs, analyst notes, and AI-generated triage artifacts were associated with an incident workflow and routed for review.

## Non-claims

Fork does not claim:

- `does_not_claim_no_breach_occurred`
- `does_not_claim_incident_scope`
- `does_not_claim_containment_success`
- `does_not_claim_reporting_obligation`
- `does_not_claim_security_effectiveness`
- `does_not_claim_approval`

## Boundary-preserved consumption

A security analyst or incident lead consumes the triage packet as an analyst-support artifact based on available evidence.

Example:

> The triage record was used to orient investigation and preserve observed evidence, not to clear the organization of breach risk.

Boundary result:

`BOUNDARY_PRESERVED`

## Boundary-expanding consumption

A downstream actor treats absence of detected malicious activity in summarized logs as proof that no breach occurred.

Example:

> No malicious activity appeared in the summarized logs, so no breach occurred.

Boundary result:

`BOUNDARY_EXPANSION_DETECTED`

## Buyer-facing boundary sentence

Fork can preserve the boundary between observed evidence in a triage record and broader claims about breach status, incident scope, containment, reporting obligations, or security control effectiveness.

## Fork role

Fork may support incident review by preserving the evidence and claim boundaries around AI-assisted triage. It does not determine breach status, incident scope, containment success, legal reporting obligations, security effectiveness, or approval.

## Example record

See:

- `examples/fork_use_cases/valid_cyber_triage_boundary_v0_1.json`