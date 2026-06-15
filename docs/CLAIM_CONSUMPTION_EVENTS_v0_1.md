# Claim Consumption Events v0.1

Status: `DOCTRINE_DRAFT`  
Scope: Use-time boundary discipline for downstream reliance on Claim Boundary Contracts.

Primary dependency:

- `docs/CLAIM_BOUNDARY_CONTRACT_v0_1.md`

## 1. Purpose

Claim Boundary Contracts define creation-time boundary discipline for governance-related claims. Claim Consumption Events define use-time boundary discipline.

A Claim Consumption Event records how a downstream actor, system, workflow, or institution relies on a Claim Boundary Contract, whether the original boundary was preserved, narrowed, ignored, or expanded, and whether any expansion produced a new explicit claim with its own Claim Boundary Contract.

The purpose of this document is to define the doctrine and minimum field sketch for Claim Consumption Events without turning Fork into a policy engine, incentive-design system, legal authority, compliance certifier, or semantic oracle.

## 2. Canonical Definition

A Claim Consumption Event records when a downstream actor, system, workflow, or institution relies on a Claim Boundary Contract; what parts of the bounded claim were relied on; which non-claims were preserved; whether the original boundary was preserved, narrowed, ignored, or expanded; and whether any expansion produced a new explicit claim with its own Claim Boundary Contract.

## 3. Relationship to Claim Boundary Contracts

A Claim Boundary Contract answers creation-time questions:

- What was claimed?
- What was not claimed?
- What evidence supported it?
- What upstream claims were relied on or rejected?
- What known gaps remained?
- What does verification actually mean and what scope does it cover?

A Claim Consumption Event answers use-time questions:

- Who relied on the CBC?
- What did they rely on?
- Which claims, evidence references, and upstream claims were used?
- Were the original non-claims preserved?
- Was the original boundary preserved, narrowed, ignored, or expanded?
- If expanded, who took responsibility for the expansion?
- Did the expansion produce a new explicit claim with its own CBC?

The relationship is:

- CBC = boundary at creation  
- CCE = boundary at consumption  

## 4. Core Doctrine

Claim boundaries prevent silent ambiguity at creation; claim-consumption friction prevents silent expansion at use.

Fork does not solve incentive pressure by pretending people will stop compressing meaning. It makes that compression explicit.

If a downstream actor turns "checked" into "approved," Fork's posture is that the expansion should become a recorded, attributable, recomputable event, not invisible semantic drift.

## 5. Why CCE Exists

A Claim Boundary Contract can preserve what a source system or institution actually claimed. But downstream actors may still compress or reinterpret that claim.

Examples:

- "The system checked this tool call" becomes "the workflow was approved."
- "The model passed this benchmark" becomes "the model is production-ready."
- "Legal reviewed this narrow issue" becomes "legal approved the entire workflow."
- "Risk accepted this condition" becomes "the control environment is sufficient."

CCE exists to prevent those transformations from remaining ambient. It does not prevent humans or institutions from expanding a claim. It requires the expansion to be explicit, attributable, and tied to a new bounded record.

## 6. Minimum Field Sketch

A future CCE schema should consider the following fields.

- `consumption_event_id`  
  Unique identifier for the consumption event.

- `source_claim_boundary_contract_id`  
  Identifier of the CBC being consumed.

- `consumer`  
  The downstream actor, system, workflow, team, or institution relying on the CBC.

- `consumption_context`  
  The workflow, decision, dashboard, report, escalation, approval path, or institutional context in which the CBC was consumed.

- `relied_on_claims`  
  The specific claims or portions of the CBC the consumer relied on.

- `relied_on_evidence_refs`  
  The specific evidence references the consumer treated as relevant.

- `preserved_non_claims`  
  The non-claims from the source CBC that were carried forward.

- `ignored_or_rejected_claims`  
  Claims, evidence references, or upstream claims that the consumer explicitly did not rely on.

- `boundary_action`  
  How the consumer treated the original boundary. Allowed values:

  - `PRESERVED`
  - `NARROWED`
  - `IGNORED`
  - `EXPANDED`

- `boundary_expansion_description`  
  Required when `boundary_action` is `EXPANDED`. Describes what changed, what meaning was broadened, and what additional responsibility was assumed.

- `new_claim_boundary_contract_id`  
  Required when an expansion creates a new explicit claim. Points to the CBC that preserves the expanded claim and its own evidence boundary.

- `human_or_institutional_authority`  
  Identifies the human role, team, institution, or governance authority responsible for the consumption action or expansion.

- `timestamp`  
  When the consumption event was recorded.

- `verification_status`  
  One of: `PASS`, `FAIL`, `NOT_CHECKED`, `PARTIAL`.

- `verification_scope`  
  What `verification_status` actually applies to. Recommended v0.1 value:

  - `RECORD_INTEGRITY_AND_BOUNDARY_STRUCTURE_ONLY`

## 7. Boundary Actions

### PRESERVED

The downstream consumer relied on the CBC without expanding its meaning and preserved the relevant non-claims.

Example:  
A workflow report states that a tool call was blocked and preserves the original non-claims that no legal sufficiency, compliance sufficiency, or system-wide safety claim was made.

### NARROWED

The downstream consumer relied on a smaller subset of the CBC than the original source claim allowed.

Example:  
A risk reviewer relies only on the evidence that a specific policy check occurred, not on the broader issuer-defined result label.

### IGNORED

The downstream consumer records that the CBC was available but was not relied on.

Example:  
A legal reviewer sees an eval benchmark CBC but does not rely on it because the review concerns contractual sufficiency, not model performance.

### EXPANDED

The downstream consumer broadens the meaning of the CBC beyond its original claim boundary.

Example:  
A dashboard turns "benchmark threshold met" into "approved for deployment."

In this case, the expansion must not remain silent. A new explicit claim should be issued and preserved under a new CBC, with the responsible authority identified.

## 8. Example: Incorrect Silent Expansion

Source CBC:

- `claim_type`: `eval_result.benchmark_pass`
- `positive_claim`: benchmark threshold met
- `non_claim`: no production-readiness claim
- `non_claim`: no legal-sufficiency claim
- `verification_scope`: `RECORD_INTEGRITY_AND_BOUNDARY_STRUCTURE_ONLY`

Downstream dashboard label:

- `approved`

CCE result:

- `boundary_action`: `EXPANDED`
- `boundary_expansion_description`: benchmark-pass claim was broadened into deployment approval
- `new_claim_boundary_contract_id`: required
- `human_or_institutional_authority`: required

This does not forbid the institution from making an approval decision. It requires the approval decision to become a new explicit claim with its own boundary, evidence, authority, and non-claims.

## 9. Example: Correct Narrowing

Source CBC:

- `claim_type`: `runtime_enforcement_event.blocked_tool_call`
- `positive_claim`: specific tool call was blocked
- `non_claim`: no workflow-level legal sufficiency claim
- `non_claim`: no system-wide safety claim

Downstream risk note:

- The tool call block is treated only as evidence that the configured policy engine blocked this event under the referenced policy snapshot. No workflow-level approval or legal sufficiency claim is inferred.

CCE result:

- `boundary_action`: `NARROWED`
- `preserved_non_claims`: source non-claims carried forward
- `new_claim_boundary_contract_id`: not required unless the reviewer issues a new claim

## 10. Fork's Role

Fork may preserve CCEs as evidence-boundary records showing how bounded claims were consumed downstream.

Fork may help answer:

- who relied on a CBC
- what they relied on
- what non-claims traveled forward
- whether the boundary was preserved, narrowed, ignored, or expanded
- whether expansion produced a new explicit CBC
- whether the CCE record still structurally verifies later

Fork does not determine whether the downstream reliance was wise, lawful, compliant, safe, or institutionally sufficient.

## 11. Verification Semantics

CCE verification should follow the same bounded posture as CBC verification.

Example:

```text
verification_status: PASS
verification_scope: RECORD_INTEGRITY_AND_BOUNDARY_STRUCTURE_ONLY
```

This means only that the CCE record and preserved evidentiary structure verified within the declared scope. It does not mean the downstream decision was correct, lawful, safe, compliant, approved, or institutionally sufficient.

## 12. Non-Goals

Claim Consumption Events do not:

- prevent human reinterpretation
- redesign organizational incentives
- decide whether claim expansion is permitted
- approve downstream use
- certify legal sufficiency
- certify compliance
- determine safety
- replace policy engines
- replace runtime enforcement
- replace institutional authority
- convert a local source claim into a valid downstream assurance by themselves

## 13. Future Implementation Path

A future implementation may add:

- `examples/claim_consumption_events/dashboard_checked_to_approved_expansion.json`
- `examples/claim_consumption_events/risk_team_correct_narrowing.json`
- `schemas/claim_consumption_event_v0_1.schema.json`
- `tests/test_claim_consumption_event_v0_1.py`

The doctrine should be stabilized before schema enforcement is introduced.