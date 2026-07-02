# Fork Simulation Failure Modes v0.1

## Purpose

This document defines initial failure modes for the Fork Governance Simulation Proof Surface.

Failure modes are used to test whether Fork records expose unsupported inheritance, authority leakage, semantic compression, and downstream overreach.

## Failure Mode Classes

### FM-001: Claim Scope Expansion

A downstream system treats a narrow upstream claim as broader than recorded.

Example:

- Upstream: "reviewed for preliminary triage."
- Downstream: "approved for onboarding."

### FM-002: Authority Leakage

A downstream system treats recorded role or policy context as authority transfer.

Example:

- Upstream: "reviewed by vendor-risk analyst."
- Downstream: "authorized by vendor-risk function."

### FM-003: Policy-Reference Laundering

A downstream system treats a policy reference as policy applicability, policy satisfaction, or compliance approval.

Example:

- Upstream: "policy VR-PRELIM-001 referenced."
- Downstream: "complies with VR-PRELIM-001."

### FM-004: Structural Verification to Truth

A downstream system treats structural verification as factual correctness.

Example:

- Upstream: "packet structurally verifies."
- Downstream: "the vendor-risk conclusion is correct."

### FM-005: Human Review to Legal Sufficiency

A downstream system treats human review as legal, compliance, procurement, audit, or institutional sufficiency.

Example:

- Upstream: "human reviewer accepted memo."
- Downstream: "memo is legally sufficient for action."

### FM-006: Unresolved State Suppression

A downstream system omits or hides unresolved issues.

Example:

- Upstream: "SOC 2 evidence unavailable."
- Downstream: "security review complete."

### FM-007: Non-Claim Loss

A downstream system consumes a record but drops the associated non-claims.

Example:

- Upstream non-claim: "not approval."
- Downstream artifact: "approved vendor packet."

### FM-008: Delegation Collapse

A downstream system treats delegated review as final institutional decision authority.

Example:

- Upstream: "review delegated for triage."
- Downstream: "delegated reviewer approved final action."

### FM-009: Multi-Hop Semantic Compression

Multiple systems pass an artifact until original claim scope and unresolved state are compressed into a simpler status label.

Example:

- Original state: "reviewed with unresolved evidence gaps."
- Final state: "cleared."

## Failure Mode Recording Fields

Each failure mode instance should record:

| Field | Meaning |
|---|---|
| Failure mode ID | Stable identifier |
| Scenario ID | Scenario where failure occurred |
| Source system | System where claim originated |
| Consuming system | System where inference occurred |
| Original claim | What was actually recorded |
| Downstream inference | What was inferred |
| Boundary artifact | BDR, CBC, CCE, SMR, APC, or non-claim artifact |
| Exposure result | Exposed, not exposed, ambiguous |
| Non-claim status | Preserved, dropped, altered, absent |
| Revalidation requirement | Required, not required, unclear |
| Notes | Reviewer notes |

## Non-Claims

Failure-mode exposure does not prove that Fork prevents failure.

Failure-mode exposure does not establish compliance, correctness, authority, legal sufficiency, or production readiness.

The purpose is to test whether the failure becomes visible and reconstructable.