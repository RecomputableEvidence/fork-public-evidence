# scripts/create_scenario_04_authority_leakage_artifacts_v0_1.ps1
# Creates Scenario 04 authority-leakage simulation artifacts.
# Does not stage, commit, push, or tag.

param(
    [switch]$ForceOverwrite
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".git")) {
    throw "Run this script from the repository root, e.g. C:\N\fork-public-evidence"
}

function Write-Utf8NoBomFile {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content,
        [switch]$Overwrite
    )

    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path $parent)) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }

    if ((Test-Path $Path) -and -not $Overwrite) {
        Write-Host "SKIP existing file: $Path"
        return
    }

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $utf8NoBom)
    Write-Host "WROTE: $Path"
}

$scenario04 = @'
# Scenario 04: Authority Leakage Attempt

## Purpose

This scenario tests whether Fork exposes downstream authority leakage.

The modeled drift is:

```text
reviewed by vendor-risk analyst
        ->
authorized by vendor-risk function
```

The purpose is not to block the downstream actor. The purpose is to make the authority leakage visible, classifiable, and reconstructable without converting role or policy context into transferred approval authority.

## Participating Systems

| System   | Role                                           |
|---------|------------------------------------------------|
| System A | AI-assisted production system                 |
| System B | Fork boundary-record layer                    |
| System C | Institutional review / policy context system  |
| System D  | Downstream operational or decision system    |
| System E | Audit / reconstruction / oversight system     |

## Flow

- System A produces an AI-assisted vendor-risk memo.
- System C records preliminary review by a vendor-risk analyst, with policy references.
- System B preserves the handoff boundary, including recorded role and policy context and explicit non-claims.
- System D reads the memo and context and treats it as if the "vendor-risk function" has authorized onboarding or approved the vendor.
- System E reconstructs the transition and identifies authority leakage.

## Original Role and Context

Recorded role:

- Vendor-risk analyst / preliminary reviewer.

Recorded policy context:

- Vendor-risk preliminary review policy reference (for example, `VR-PRELIM-REVIEW-v0.1`).

Recorded non-claims:

- Role and policy references do not establish approval authority, onboarding clearance, compliance, legal sufficiency, or institutional authorization.

## Downstream Authority Leakage Claim

The vendor-risk function (or equivalent) is treated as if it has:

- authorized onboarding, or
- issued final vendor approval.

## Expected Classification

Primary category:

- AUTHORITY_LEAKAGE

Secondary categories:

- CLAIM_SCOPE_EXPANSION
- POLICY_APPROVAL_CONFUSION

## Expected Fork Behavior

Fork does not block the downstream reliance attempt.  
Fork preserves the original role and policy context, records the attempted authority transfer, and exposes that no approval authority or policy-approval decision crossed the boundary.

## What Crossed the Boundary

- AI-assisted vendor-risk memo.
- Preliminary triage review claim.
- Recorded reviewer role.
- Recorded policy reference.
- Non-claims.
- Unresolved authority and compliance state.
- Revalidation requirements.

## What Did Not Cross the Boundary

- Final approval authority.
- Onboarding clearance.
- Compliance determination.
- Legal sufficiency determination.
- Production readiness.
- Institutional authorization.

## Reconstruction Result

Expected outcome:

`UNSUPPORTED_AUTHORITY_LEAKAGE_EXPOSED`

## Non-Claims

This scenario does not establish correctness, compliance, legal sufficiency, institutional authority, production readiness, or general validity.  
This scenario tests whether downstream authority leakage becomes inspectable.
'@

$artifactReadme = @'
# Governance Proof Surface Simulation Artifacts

## Purpose

This artifact directory contains machine-readable and reviewer-readable artifacts for Fork Governance Simulation Proof Surface scenarios.

The artifacts support bounded inspection of claim scope, non-claims, authority context, unsupported inheritance, semantic drift, and authority leakage.

## Scenario 02 Artifact Set

| Artifact | File | Purpose |
|---|---|---|
| Boundary Delta Record | scenario_02_boundary_delta_record.json | Records the transition between upstream review state and downstream reliance attempt |
| Claim Boundary Contract | scenario_02_claim_boundary_contract.json | Defines what claim scope crossed and what did not cross |
| Claim Consumption Event | scenario_02_claim_consumption_event.json | Records how the downstream system consumed the upstream claim |
| System Mapping Receipt | scenario_02_system_mapping_receipt.json | Maps participating systems, roles, artifacts, and boundary posture |
| Unsupported Inheritance Event | scenario_02_unsupported_inheritance_event.json | Records the downstream inference that exceeded the recorded boundary |
| Authority Policy Context | scenario_02_authority_policy_context.md | Records policy and role context without asserting approval or compliance |
| Non-Claims Panel | scenario_02_non_claims_panel.md | Preserves explicit non-claims associated with the handoff |

## Scenario 03 Artifact Set

| Artifact | File | Purpose |
|---|---|---|
| Boundary Delta Record | scenario_03_boundary_delta_record.json | Records semantic drift from preliminary triage to onboarding approval / cleared status |
| Claim Boundary Contract | scenario_03_claim_boundary_contract.json | Reuses the preliminary-triage boundary and forbids approval / cleared inference |
| Claim Consumption Event | scenario_03_claim_consumption_event.json | Records downstream expansion from reviewed to approved / cleared |
| System Mapping Receipt | scenario_03_system_mapping_receipt.json | Maps the second downstream consumer and semantic re-labeling step |
| Unsupported Inheritance Event | scenario_03_unsupported_inheritance_event.json | Records the unsupported scope expansion |
| Authority Policy Context | scenario_03_authority_policy_context.md | Records policy and role context without treating either as approval authority |
| Non-Claims Panel | scenario_03_non_claims_panel.md | Preserves explicit non-claims, including no conversion of preliminary review into onboarding approval |

## Scenario 04 Artifact Set

| Artifact | File | Purpose |
|---|---|---|
| Boundary Delta Record | scenario_04_boundary_delta_record.json | Records authority leakage from analyst review to inferred functional authorization |
| Claim Boundary Contract | scenario_04_claim_boundary_contract.json | Records that reviewer role and policy references do not transfer approval authority |
| Claim Consumption Event | scenario_04_claim_consumption_event.json | Records downstream inference that the vendor-risk function has authorized onboarding |
| System Mapping Receipt | scenario_04_system_mapping_receipt.json | Maps systems and highlights the authority leakage path |
| Unsupported Inheritance Event | scenario_04_unsupported_inheritance_event.json | Records unsupported authority transfer and policy-approval confusion |
| Authority Policy Context | scenario_04_authority_policy_context.md | Records role and policy context without converting them into approval authority |
| Non-Claims Panel | scenario_04_non_claims_panel.md | Preserves explicit non-claims about authority, approval, and policy applicability |

## Non-Claims

These artifact bundles do not establish correctness, compliance, legal sufficiency, institutional authority, production readiness, or general validity.
'@

$bdr = @'
{
  "artifact_type": "BOUNDARY_DELTA_RECORD",
  "artifact_version": "0.1",
  "scenario_id": "SCENARIO_04_AUTHORITY_LEAKAGE_ATTEMPT",
  "record_id": "BDR-SIM-04-001",
  "title": "Scenario 04 Boundary Delta Record",
  "created_for": "Fork Governance Simulation Proof Surface",
  "transition": {
    "transition_id": "TRANSITION-SIM-04-001",
    "from_systems": [
      "SYSTEM_A_AI_ASSISTED_PRODUCTION",
      "SYSTEM_C_INSTITUTIONAL_REVIEW_CONTEXT"
    ],
    "through_system": "SYSTEM_B_FORK_BOUNDARY_RECORD_LAYER",
    "to_system": "SYSTEM_D_DOWNSTREAM_OPERATIONAL_DECISION",
    "reconstruction_system": "SYSTEM_E_AUDIT_RECONSTRUCTION_OVERSIGHT",
    "transition_kind": "PRELIMINARY_REVIEW_ROLE_TO_INFERRED_FUNCTIONAL_AUTHORIZATION"
  },
  "upstream_state": {
    "artifact_id": "ART-SIM-04-VENDOR-RISK-MEMO",
    "artifact_type": "AI_ASSISTED_VENDOR_RISK_MEMO",
    "recorded_claims": [
      {
        "claim_id": "CLM-SIM-04-001",
        "statement": "An AI-assisted vendor-risk memo was produced and reviewed by a vendor-risk analyst for preliminary triage.",
        "scope": "PRELIMINARY_TRIAGE_ONLY",
        "status": "RECORDED"
      }
    ],
    "recorded_role_context": {
      "role_id": "ROLE-SIM-04-ANALYST",
      "role_label": "Vendor-risk analyst / preliminary reviewer",
      "authority_level": "PRELIMINARY_REVIEW_ONLY"
    },
    "recorded_policy_context": [
      {
        "policy_id": "POLICY-SIM-04-VR-PRELIM-REVIEW-v0.1",
        "description": "Vendor-risk preliminary review policy reference",
        "status": "REFERENCED"
      }
    ],
    "recorded_non_claims": [
      "The recorded reviewer role does not establish final approval authority.",
      "The recorded reviewer role does not establish onboarding clearance.",
      "The recorded policy reference does not establish policy applicability.",
      "The recorded policy reference does not establish compliance.",
      "The recorded preliminary review does not establish legal sufficiency.",
      "The recorded preliminary review does not establish production readiness.",
      "The recorded preliminary review does not transfer institutional authorization."
    ],
    "unresolved_state": [
      {
        "unresolved_id": "UNRESOLVED-SIM-04-001",
        "description": "Final approval authority not established."
      },
      {
        "unresolved_id": "UNRESOLVED-SIM-04-002",
        "description": "Onboarding clearance not established."
      },
      {
        "unresolved_id": "UNRESOLVED-SIM-04-003",
        "description": "Policy applicability and compliance not determined."
      }
    ]
  },
  "downstream_authority_leakage": {
    "consumer_system": "SYSTEM_D_DOWNSTREAM_OPERATIONAL_DECISION",
    "leakage_id": "AUTH-LEAK-SIM-04-001",
    "source_role": "Vendor-risk analyst / preliminary reviewer",
    "downstream_inferred_authority": "Vendor-risk function authorized onboarding / final approval",
    "inference_type": "ROLE_TO_FUNCTION_AUTHORITY_TRANSFER",
    "new_approval_record_present": false,
    "new_authority_evidence_present": false,
    "new_policy_approval_decision_present": false
  },
  "delta_classification": {
    "authority_context": "LEAKED",
    "claim_scope": "EXPANDED",
    "policy_context": "REFERENCED_ONLY",
    "non_claims": "PRESERVED",
    "unresolved_state": "PRESERVED",
    "overall_boundary_effect": "UNSUPPORTED_AUTHORITY_LEAKAGE_EXPOSED"
  },
  "required_revalidation": [
    "Obtain explicit approval authority before treating preliminary review as authorization.",
    "Obtain explicit onboarding clearance before operational onboarding.",
    "Obtain explicit policy-approval decision before treating policy reference as compliance.",
    "Resolve unresolved authority and compliance state before downstream action."
  ],
  "inspectability_result": "INSPECTABLE",
  "fork_role": "PRESERVE_HANDOFF_STATE_AND_EXPOSE_AUTHORITY_LEAKAGE",
  "fork_non_authority_statement": "Fork records the role and policy context and exposes authority leakage for inspection and reconstruction. Fork does not approve, authorize, certify, or determine the downstream action."
}
'@

$cbc = @'
{
  "artifact_type": "CLAIM_BOUNDARY_CONTRACT",
  "artifact_version": "0.1",
  "scenario_id": "SCENARIO_04_AUTHORITY_LEAKAGE_ATTEMPT",
  "contract_id": "CBC-SIM-04-001",
  "title": "Scenario 04 Claim Boundary Contract",
  "subject": {
    "artifact_id": "ART-SIM-04-VENDOR-RISK-MEMO",
    "artifact_type": "AI_ASSISTED_VENDOR_RISK_MEMO"
  },
  "boundary": {
    "from": "SYSTEM_A_AI_ASSISTED_PRODUCTION_AND_SYSTEM_C_REVIEW_CONTEXT",
    "to": "SYSTEM_D_DOWNSTREAM_OPERATIONAL_DECISION",
    "mediated_by": "SYSTEM_B_FORK_BOUNDARY_RECORD_LAYER"
  },
  "claims_allowed_to_cross": [
    {
      "claim_id": "CLM-SIM-04-001",
      "statement": "The memo was produced and reviewed by a vendor-risk analyst for preliminary vendor-risk triage.",
      "scope": "PRELIMINARY_TRIAGE_ONLY",
      "conditions": [
        "May be used to understand what preliminary review occurred.",
        "May be used to identify unresolved issues.",
        "May be used to request additional review, approval, or revalidation."
      ]
    }
  ],
  "claims_not_allowed_to_be_inferred": [
    {
      "non_claim_id": "NC-SIM-04-001",
      "statement": "The preliminary triage record does not establish final vendor approval."
    },
    {
      "non_claim_id": "NC-SIM-04-002",
      "statement": "The preliminary triage record does not establish onboarding clearance."
    },
    {
      "non_claim_id": "NC-SIM-04-003",
      "statement": "The preliminary triage record does not establish that the vendor-risk function has issued authorization."
    },
    {
      "non_claim_id": "NC-SIM-04-004",
      "statement": "The preliminary triage record does not establish compliance."
    },
    {
      "non_claim_id": "NC-SIM-04-005",
      "statement": "The preliminary triage record does not establish legal sufficiency."
    },
    {
      "non_claim_id": "NC-SIM-04-006",
      "statement": "The preliminary triage record does not establish production readiness."
    },
    {
      "non_claim_id": "NC-SIM-04-007",
      "statement": "The preliminary triage record does not establish factual correctness of underlying vendor data."
    },
    {
      "non_claim_id": "NC-SIM-04-008",
      "statement": "The preliminary triage record does not transfer institutional authority."
    }
  ],
  "role_and_policy_guard": {
    "recorded_role": "Vendor-risk analyst / preliminary reviewer",
    "recorded_policy_reference": "VR-PRELIM-REVIEW-v0.1",
    "prohibited_authority_inferences_without_new_decision": [
      "VENDOR_RISK_FUNCTION_AUTHORIZED_ONBOARDING",
      "VENDOR_RISK_FUNCTION_ISSUED_FINAL_APPROVAL"
    ],
    "authority_expansion_requires": [
      "explicit downstream approval decision record",
      "identified approval authority role",
      "new evidence reference or justification"
    ]
  },
  "evidence_references": [
    {
      "evidence_id": "EVID-SIM-04-001",
      "description": "AI-assisted memo artifact reference",
      "status": "REFERENCED"
    },
    {
      "evidence_id": "EVID-SIM-04-002",
      "description": "Human preliminary review context",
      "status": "REFERENCED"
    },
    {
      "evidence_id": "EVID-SIM-04-003",
      "description": "Vendor-risk preliminary review policy reference",
      "status": "REFERENCED"
    }
  ],
  "revalidation_required_for": [
    "approval authority",
    "onboarding clearance",
    "authorization",
    "policy applicability",
    "compliance determination",
    "legal sufficiency",
    "production readiness",
    "factual correctness"
  ],
  "contract_result": "BOUNDARY_STRUCTURE_RECORDED_ONLY",
  "non_claims_preserved": true
}
'@

$cce = @'
{
  "artifact_type": "CLAIM_CONSUMPTION_EVENT",
  "artifact_version": "0.1",
  "scenario_id": "SCENARIO_04_AUTHORITY_LEAKAGE_ATTEMPT",
  "event_id": "CCE-SIM-04-001",
  "title": "Scenario 04 Claim Consumption Event",
  "consumer": {
    "system_id": "SYSTEM_D_DOWNSTREAM_OPERATIONAL_DECISION",
    "consumer_role": "DOWNSTREAM_OPERATIONAL_CONSUMER"
  },
  "consumed_claim": {
    "claim_id": "CLM-SIM-04-001",
    "statement": "The memo was produced and reviewed by a vendor-risk analyst for preliminary vendor-risk triage.",
    "recorded_scope": "PRELIMINARY_TRIAGE_ONLY"
  },
  "attempted_consumption": {
    "attempted_claim": "Vendor-risk function has authorized the vendor for onboarding.",
    "attempted_scope": "FINAL_VENDOR_APPROVAL_OR_AUTHORIZATION",
    "consumption_effect": "EXPANDED",
    "authority_shift": {
      "from_role": "Vendor-risk analyst / preliminary reviewer",
      "to_function": "Vendor-risk function as approval authority"
    },
    "new_approval_record_present": false,
    "new_authority_evidence_present": false,
    "new_policy_approval_decision_present": false
  },
  "classification": {
    "consumption_classification": "AUTHORITY_LEAKAGE_UNSUPPORTED",
    "unsupported_inheritance": true,
    "primary_category": "AUTHORITY_LEAKAGE",
    "secondary_categories": [
      "CLAIM_SCOPE_EXPANSION",
      "POLICY_APPROVAL_CONFUSION"
    ],
    "reason": "The downstream authority inference exceeds the recorded preliminary triage scope and lacks explicit approval decision, identified approval authority, or policy-approval determination."
  },
  "preserved_non_claims": [
    "Not final approval.",
    "Not onboarding clearance.",
    "Not authorization.",
    "Not compliance determination.",
    "Not legal sufficiency.",
    "Not production readiness.",
    "Not factual correctness guarantee.",
    "No authority transfer."
  ],
  "required_next_action": [
    "Treat downstream authority inference as unsupported unless separately authorized.",
    "Request explicit approval authority, decision record, and evidence before operational onboarding action."
  ],
  "fork_role": "RECORD_CONSUMPTION_AND_EXPOSE_AUTHORITY_LEAKAGE"
}
'@

$smr = @'
{
  "artifact_type": "SYSTEM_MAPPING_RECEIPT",
  "artifact_version": "0.1",
  "scenario_id": "SCENARIO_04_AUTHORITY_LEAKAGE_ATTEMPT",
  "receipt_id": "SMR-SIM-04-001",
  "title": "Scenario 04 System Mapping Receipt",
  "systems": [
    {
      "system_id": "SYSTEM_A_AI_ASSISTED_PRODUCTION",
      "native_responsibility": "Produce AI-assisted vendor-risk memo",
      "fork_does_not_become": "model evaluator"
    },
    {
      "system_id": "SYSTEM_B_FORK_BOUNDARY_RECORD_LAYER",
      "native_responsibility": "Preserve handoff state and expose boundary effects",
      "fork_does_not_become": "approval authority"
    },
    {
      "system_id": "SYSTEM_C_INSTITUTIONAL_REVIEW_CONTEXT",
      "native_responsibility": "Represent preliminary human review and policy context",
      "fork_does_not_become": "compliance decision-maker"
    },
    {
      "system_id": "SYSTEM_D_DOWNSTREAM_OPERATIONAL_DECISION",
      "native_responsibility": "Consume artifact for routing or action",
      "fork_does_not_become": "institutional authority"
    },
    {
      "system_id": "SYSTEM_E_AUDIT_RECONSTRUCTION_OVERSIGHT",
      "native_responsibility": "Reconstruct transition later",
      "fork_does_not_become": "legal authority"
    }
  ],
  "mapping": {
    "source_artifact": "ART-SIM-04-VENDOR-RISK-MEMO",
    "boundary_artifacts": [
      "BDR-SIM-04-001",
      "CBC-SIM-04-001",
      "CCE-SIM-04-001",
      "APC-SIM-04-001",
      "NCP-SIM-04-001"
    ],
    "consumer_event": "CCE-SIM-04-001",
    "unsupported_inheritance_event": "UIE-SIM-04-001"
  },
  "authority_mapping": {
    "recorded_role": "Vendor-risk analyst / preliminary reviewer",
    "downstream_inferred_function": "Vendor-risk function approval authority",
    "mapping_outcome": "AUTHORITY_LEAKAGE_UNSUPPORTED"
  },
  "mapping_outcome": "MAPPED_WITH_AUTHORITY_LEAKAGE_EXPOSED",
  "authority_transfer": false,
  "policy_approval_transfer": false,
  "runtime_control_transfer": false,
  "audit_authority_transfer": false,
  "reconstruction_posture": "UNSUPPORTED_AUTHORITY_LEAKAGE_EXPOSED"
}
'@

$uie = @'
{
  "artifact_type": "UNSUPPORTED_INHERITANCE_EVENT",
  "artifact_version": "0.1",
  "scenario_id": "SCENARIO_04_AUTHORITY_LEAKAGE_ATTEMPT",
  "event_id": "UIE-SIM-04-001",
  "title": "Scenario 04 Unsupported Authority Leakage Event",
  "condition": "SIMULATION_TREATMENT",
  "workflow_id": "SIM-GOV-PROOF-SURFACE-04",
  "category": "AUTHORITY_LEAKAGE",
  "secondary_categories": [
    "CLAIM_SCOPE_EXPANSION",
    "POLICY_APPROVAL_CONFUSION"
  ],
  "actor_or_artifact": "SYSTEM_D_DOWNSTREAM_OPERATIONAL_DECISION",
  "inferred_claim": "Vendor-risk function has authorized the vendor for onboarding.",
  "record_support": "The record supports only that an AI-assisted vendor-risk memo was produced and reviewed by a vendor-risk analyst for preliminary triage, with a policy reference.",
  "why_unsupported": "The downstream authority inference exceeds the recorded preliminary triage boundary and lacks explicit approval decision, identified approval authority, or policy-approval determination.",
  "authority_leakage": {
    "from_role": "Vendor-risk analyst / preliminary reviewer",
    "to_function": "Vendor-risk function as approval authority",
    "leak_type": "ROLE_CONTEXT_TREATED_AS_TRANSFERRED_AUTHORITY"
  },
  "evidence_refs": [
    "BDR-SIM-04-001",
    "CBC-SIM-04-001",
    "CCE-SIM-04-001",
    "SMR-SIM-04-001",
    "APC-SIM-04-001",
    "NCP-SIM-04-001"
  ],
  "coder_id": "SIMULATION_CODER",
  "adjudication_status": "AGREED",
  "adjudication_note": "Scenario 04 intentionally models downstream authority leakage from recorded analyst review and policy reference to inferred functional authorization so Fork can expose the unsupported authority transfer.",
  "fork_result": "UNSUPPORTED_AUTHORITY_LEAKAGE_EXPOSED",
  "fork_non_authority_statement": "Fork exposes the authority leakage boundary effect. Fork does not decide whether onboarding should occur."
}
'@

$apc = @'
Scenario 04 Authority Policy Context
Artifact ID: APC-SIM-04-001

Purpose
This context file records the authority and policy context present during Scenario 04.
It preserves context for reconstruction without asserting approval authority, onboarding clearance, compliance, applicability, legal sufficiency, or institutional authorization.

Scenario
SCENARIO_04_AUTHORITY_LEAKAGE_ATTEMPT

Recorded Role Context
A human reviewer in System C reviewed the AI-assisted vendor-risk memo for preliminary triage.

Recorded role context:
Vendor-risk analyst / preliminary reviewer

System D later treated the recorded vendor-risk analyst review and policy reference as if the vendor-risk function had authorized the vendor for onboarding.

Recorded Policy Context
Policy context was referenced for preliminary review.
Recorded policy reference:
VR-PRELIM-REVIEW-v0.1

Explicit Non-Claims
The recorded reviewer role does not establish final approval authority.
The recorded reviewer role does not establish onboarding clearance.
The recorded policy reference does not establish policy applicability.
The recorded policy reference does not establish compliance.
The recorded preliminary review does not establish legal sufficiency.
The recorded preliminary review does not establish production readiness.
The recorded preliminary review does not transfer institutional authority to Fork or to a downstream system.

Required Revalidation
Before downstream onboarding or operational action, the downstream system must obtain separate evidence or authority for:
final approval authority;
onboarding clearance;
policy applicability;
compliance determination;
legal sufficiency;
production readiness;
factual correctness;
institutional authorization.

Fork Role
Fork preserves this context as handoff state.
Fork does not decide whether the policy applies, whether the policy was satisfied, whether the reviewer had sufficient authority, or whether the vendor is approved or cleared.
'@

$ncp = @'
Scenario 04 Non-Claims Panel
Artifact ID: NCP-SIM-04-001

Purpose
This panel preserves explicit non-claims for Scenario 04.
It is attached to the Fork-preserved handoff so downstream systems do not silently convert recorded analyst review and policy reference into approval authority, onboarding clearance, compliance, correctness, or production readiness.

Non-Claims
This handoff record is not final vendor approval.
This handoff record is not onboarding clearance.
This handoff record is not an authorization decision.
This handoff record is not a compliance determination.
This handoff record is not legal sufficiency.
This handoff record is not production readiness.
This handoff record is not a factual correctness guarantee.
This handoff record is not institutional authorization.
This handoff record does not transfer authority from System C to System D.
This handoff record does not convert a policy reference into policy applicability.
This handoff record does not convert preliminary review into final decision authority.
This handoff record does not convert "reviewed by vendor-risk analyst" into "authorized by vendor-risk function."
This handoff record does not decide whether downstream reliance is justified.

Preserved Boundary
The only preserved positive claim is:
An AI-assisted vendor-risk memo was produced and reviewed by a vendor-risk analyst for preliminary triage.

Required Downstream Treatment
Any downstream claim of approval authority, onboarding clearance, authorization, compliance, legal sufficiency, production readiness, or factual correctness requires separate evidence or authority.

Fork Role
Fork preserves the non-claims.
Fork does not enforce, approve, authorize, certify, or adjudicate the downstream action.
'@

$checkScript = @'
# scripts/run_ahi_sim_v0_1_checks.ps1
# Focused checks for Fork Governance Simulation Proof Surface v0.1.x.
# Does not stage, commit, push, or tag.

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".git")) {
    throw "Run this script from the repository root, e.g. C:\N\fork-public-evidence"
}

Write-Host "Checking required simulation files..."
$required = @(
    "docs/simulations/FORK_SIMULATION_PROOF_SURFACE_DOCTRINE_v0_1.md",
    "docs/simulations/FORK_GOVERNANCE_SIMULATION_SEQUENCE_v0_1.md",
    "docs/simulations/FORK_SIMULATION_CONTRACTS_AND_INTERFACES_v0_1.md",
    "docs/simulations/FORK_SIMULATION_FAILURE_MODES_v0_1.md",
    "docs/simulations/FORK_SIMULATION_RECONSTRUCTION_GUIDE_v0_1.md",
    "examples/simulations/governance-proof-surface/README.md",
    "examples/simulations/governance-proof-surface/scenario_01_baseline_unbounded_handoff.md",
    "examples/simulations/governance-proof-surface/scenario_02_fork_preserved_handoff.md",
    "examples/simulations/governance-proof-surface/scenario_03_scope_expansion_attempt.md",
    "examples/simulations/governance-proof-surface/scenario_04_authority_leakage_attempt.md",
    "examples/simulations/governance-proof-surface/scenario_05_policy_reference_laundering_attempt.md",
    "examples/simulations/governance-proof-surface/scenario_06_multi_system_distributed_handoff.md",
    "examples/simulations/governance-proof-surface/artifacts/README.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_unsupported_inheritance_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_authority_policy_context.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_non_claims_panel.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_unsupported_inheritance_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_authority_policy_context.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_non_claims_panel.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_unsupported_inheritance_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_authority_policy_context.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_non_claims_panel.md"
)

foreach ($path in $required) {
    if (-not (Test-Path $path)) {
        Write-Host "FAIL: missing required file: $path"
        exit 1
    }
    Write-Host "FOUND: $path"
}

Write-Host ""
Write-Host "Validating simulation JSON artifacts..."

$jsonFiles = @(
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_unsupported_inheritance_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_unsupported_inheritance_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_unsupported_inheritance_event.json"
)

foreach ($path in $jsonFiles) {
    try {
        Get-Content -Raw -Path $path | ConvertFrom-Json | Out-Null
        Write-Host "VALID JSON: $path"
    }
    catch {
        Write-Host "FAIL: invalid JSON: $path"
        Write-Host $_.Exception.Message
        exit 1
    }
}

Write-Host ""
Write-Host "Checking Scenario 04 semantic classifications..."

$cce04 = Get-Content -Raw -Path "examples/simulations/governance-proof-surface/artifacts/scenario_04_claim_consumption_event.json" | ConvertFrom-Json
$uie04 = Get-Content -Raw -Path "examples/simulations/governance-proof-surface/artifacts/scenario_04_unsupported_inheritance_event.json" | ConvertFrom-Json
$bdr04 = Get-Content -Raw -Path "examples/simulations/governance-proof-surface/artifacts/scenario_04_boundary_delta_record.json" | ConvertFrom-Json

if ($cce04.classification.consumption_classification -ne "AUTHORITY_LEAKAGE_UNSUPPORTED") {
    Write-Host "FAIL: Scenario 04 CCE must classify consumption as AUTHORITY_LEAKAGE_UNSUPPORTED"
    exit 1
}

if ($uie04.category -ne "AUTHORITY_LEAKAGE") {
    Write-Host "FAIL: Scenario 04 UIE primary category must be AUTHORITY_LEAKAGE"
    exit 1
}

if ($bdr04.delta_classification.authority_context -ne "LEAKED") {
    Write-Host "FAIL: Scenario 04 BDR authority_context must be LEAKED"
    exit 1
}

if ($bdr04.downstream_authority_leakage.new_approval_record_present -ne $false) {
    Write-Host "FAIL: Scenario 04 must not include new approval record in the downstream authority leakage"
    exit 1
}

Write-Host "PASS: Scenario 04 authority leakage classifications are bounded and explicit."
Write-Host ""
Write-Host "Running non-claims contract checker..."
python tools\check_non_claims_contract.py

Write-Host ""
Write-Host "Scanning simulation surface for prohibited overclaim language..."

$scanRoots = @(
    "docs\simulations",
    "examples\simulations"
)

$patterns = @(
    "truth engine",
    "governance oracle",
    "compliance proof",
    "certifies compliance",
    "proves correctness",
    "proves compliance",
    "guarantees trust"
)

$scanFiles = @()
foreach ($root in $scanRoots) {
    if (Test-Path $root) {
        $scanFiles += Get-ChildItem -Path $root -Recurse -File
    }
}

$violations = @()
foreach ($file in $scanFiles) {
    foreach ($pattern in $patterns) {
        $matches = Select-String -Path $file.FullName -Pattern $pattern -SimpleMatch -CaseSensitive:$false
        foreach ($match in $matches) {
            $violations += [PSCustomObject]@{
                Path      = $file.FullName
                LineNumber = $match.LineNumber
                Pattern   = $pattern
                Line      = $match.Line.Trim()
            }
        }
    }
}

if ($violations.Count -gt 0) {
    Write-Host "FAIL: prohibited simulation overclaim language found:"
    foreach ($v in $violations) {
        Write-Host "$($v.Path):$($v.LineNumber):[$($v.Pattern)] $($v.Line)"
    }
    exit 1
}

Write-Host "PASS: no prohibited simulation overclaim language found."
Write-Host ""
Write-Host "PASS: ahi-sim-v0.1.x simulation proof-surface checks completed."
'@

Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/scenario_04_authority_leakage_attempt.md" -Content $scenario04 -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/README.md" -Content $artifactReadme -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_04_boundary_delta_record.json" -Content $bdr -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_04_claim_boundary_contract.json" -Content $cbc -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_04_claim_consumption_event.json" -Content $cce -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_04_system_mapping_receipt.json" -Content $smr -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_04_unsupported_inheritance_event.json" -Content $uie -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_04_authority_policy_context.md" -Content $apc -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_04_non_claims_panel.md" -Content $ncp -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "scripts/run_ahi_sim_v0_1_checks.ps1" -Content $checkScript -Overwrite:$ForceOverwrite

Write-Host ""
Write-Host "Done."
Write-Host ""
Write-Host "Next commands:"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\\create_scenario_04_authority_leakage_artifacts_v0_1.ps1 -ForceOverwrite"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\\run_ahi_sim_v0_1_checks.ps1"