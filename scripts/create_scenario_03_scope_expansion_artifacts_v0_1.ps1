# scripts/create_scenario_03_scope_expansion_artifacts_v0_1.ps1
# Creates Scenario 03 scope-expansion simulation artifacts.
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

$scenario03 = @'
# Scenario 03: Scope Expansion Attempt

## Purpose

This scenario tests whether Fork exposes downstream claim expansion.

The modeled expansion is:

```text
reviewed for preliminary triage
        ->
approved / cleared for onboarding
```

The purpose is not to block the downstream actor. The purpose is to make the semantic expansion visible, classifiable, and reconstructable.

## Participating Systems

| System   | Role                                           |
|---------|------------------------------------------------|
| System A | AI-assisted production system                 |
| System B | Fork boundary-record layer                    |
| System C | Institutional review / policy context system  |
| System D1 | First downstream consumer                    |
| System D2 | Second downstream consumer / operational labeler |
| System E | Audit / reconstruction / oversight system     |

## Flow

- System A produces an AI-assisted vendor-risk memo.
- System C records preliminary review context.
- System B preserves the original handoff boundary.
- System D1 consumes the memo within the preliminary triage scope.
- System D2 rephrases the status as "approved for onboarding" or "cleared for onboarding."
- System E reconstructs the transition and identifies scope expansion.

## Original Claim

The vendor-risk memo was produced and reviewed for preliminary triage only.

## Downstream Expanded Claim

The vendor is approved / cleared for onboarding.

## Expected Classification

Primary:

- CLAIM_SCOPE_EXPANSION

Secondary:

- AUTHORITY_LEAKAGE

## Expected Fork Behavior

Fork does not block the downstream phrasing.  
Fork preserves the original claim boundary, records the attempted expanded consumption, and exposes that the downstream wording exceeds the recorded preliminary review scope unless supported by separate authority and evidence.

## What Crossed the Boundary

- AI-assisted vendor-risk memo.
- Preliminary triage review claim.
- Evidence references.
- Authority and policy context.
- Non-claims.
- Unresolved state.
- Revalidation requirements.

## What Did Not Cross the Boundary

- Final vendor approval.
- Cleared onboarding status.
- Compliance determination.
- Legal sufficiency.
- Production readiness.
- Factual correctness guarantee.
- Institutional authorization.

## Reconstruction Result

Expected outcome:

`UNSUPPORTED_INHERITANCE_EXPOSED`

## Non-Claims

This scenario does not establish correctness, compliance, legal sufficiency, institutional authority, production readiness, or general validity.  
This scenario tests whether a downstream scope expansion becomes inspectable.
'@

$artifactReadme = @'
# Governance Proof Surface Simulation Artifacts

## Purpose

This artifact directory contains machine-readable and reviewer-readable artifacts for Fork Governance Simulation Proof Surface scenarios.

The artifacts support bounded inspection of claim scope, non-claims, authority context, unsupported inheritance, and downstream semantic drift.

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

## Non-Claims

These artifact bundles do not establish correctness, compliance, legal sufficiency, institutional authority, production readiness, or general validity.
'@

$bdr = @'
{
  "artifact_type": "BOUNDARY_DELTA_RECORD",
  "artifact_version": "0.1",
  "scenario_id": "SCENARIO_03_SCOPE_EXPANSION_ATTEMPT",
  "record_id": "BDR-SIM-03-001",
  "title": "Scenario 03 Boundary Delta Record",
  "created_for": "Fork Governance Simulation Proof Surface",
  "transition": {
    "transition_id": "TRANSITION-SIM-03-001",
    "from_systems": [
      "SYSTEM_A_AI_ASSISTED_PRODUCTION",
      "SYSTEM_C_INSTITUTIONAL_REVIEW_CONTEXT",
      "SYSTEM_D1_FIRST_DOWNSTREAM_CONSUMER"
    ],
    "through_system": "SYSTEM_B_FORK_BOUNDARY_RECORD_LAYER",
    "to_system": "SYSTEM_D2_DOWNSTREAM_OPERATIONAL_LABELER",
    "reconstruction_system": "SYSTEM_E_AUDIT_RECONSTRUCTION_OVERSIGHT",
    "transition_kind": "PRELIMINARY_TRIAGE_TO_ONBOARDING_STATUS_LABEL"
  },
  "upstream_state": {
    "artifact_id": "ART-SIM-03-VENDOR-RISK-MEMO",
    "artifact_type": "AI_ASSISTED_VENDOR_RISK_MEMO",
    "recorded_claims": [
      {
        "claim_id": "CLM-SIM-03-001",
        "statement": "An AI-assisted vendor-risk memo was produced and reviewed for preliminary triage only.",
        "scope": "PRELIMINARY_TRIAGE_ONLY",
        "status": "RECORDED"
      }
    ],
    "recorded_non_claims": [
      "No final vendor approval is asserted.",
      "No cleared onboarding status is asserted.",
      "No compliance determination is asserted.",
      "No legal sufficiency determination is asserted.",
      "No production readiness determination is asserted.",
      "No factual correctness guarantee is asserted.",
      "No institutional authorization is asserted."
    ],
    "unresolved_state": [
      {
        "unresolved_id": "UNRESOLVED-SIM-03-001",
        "description": "Approval authority not established."
      },
      {
        "unresolved_id": "UNRESOLVED-SIM-03-002",
        "description": "Onboarding clearance not established."
      },
      {
        "unresolved_id": "UNRESOLVED-SIM-03-003",
        "description": "Compliance status not determined."
      }
    ]
  },
  "downstream_semantic_change": {
    "consumer_system": "SYSTEM_D2_DOWNSTREAM_OPERATIONAL_LABELER",
    "change_id": "SEMANTIC-DRIFT-SIM-03-001",
    "source_phrase": "reviewed for preliminary triage",
    "downstream_phrase": "approved / cleared for onboarding",
    "change_type": "STATUS_LABEL_EXPANSION",
    "new_authority_reference_present": false,
    "new_evidence_reference_present": false,
    "new_compliance_determination_present": false
  },
  "delta_classification": {
    "claim_scope": "EXPANDED",
    "semantic_drift": "PRESENT",
    "authority_context": "NOT_TRANSFERRED",
    "policy_context": "REFERENCED_ONLY",
    "non_claims": "PRESERVED",
    "unresolved_state": "PRESERVED",
    "overall_boundary_effect": "UNSUPPORTED_SCOPE_EXPANSION_EXPOSED"
  },
  "required_revalidation": [
    "Obtain explicit approval authority before treating preliminary review as approval.",
    "Obtain explicit onboarding clearance before labeling the vendor cleared.",
    "Obtain separate compliance determination before treating the workflow as compliant.",
    "Resolve or explicitly accept unresolved evidence gaps before downstream operational action."
  ],
  "inspectability_result": "INSPECTABLE",
  "fork_role": "PRESERVE_HANDOFF_STATE_AND_EXPOSE_SCOPE_EXPANSION",
  "fork_non_authority_statement": "Fork records the semantic boundary effect for inspection and reconstruction. Fork does not approve, clear, authorize, certify, or determine the downstream action."
}
'@

$cbc = @'
{
  "artifact_type": "CLAIM_BOUNDARY_CONTRACT",
  "artifact_version": "0.1",
  "scenario_id": "SCENARIO_03_SCOPE_EXPANSION_ATTEMPT",
  "contract_id": "CBC-SIM-03-001",
  "title": "Scenario 03 Claim Boundary Contract",
  "subject": {
    "artifact_id": "ART-SIM-03-VENDOR-RISK-MEMO",
    "artifact_type": "AI_ASSISTED_VENDOR_RISK_MEMO"
  },
  "boundary": {
    "from": "SYSTEM_A_AI_ASSISTED_PRODUCTION_AND_SYSTEM_C_REVIEW_CONTEXT",
    "to": "SYSTEM_D2_DOWNSTREAM_OPERATIONAL_LABELER",
    "mediated_by": "SYSTEM_B_FORK_BOUNDARY_RECORD_LAYER"
  },
  "claims_allowed_to_cross": [
    {
      "claim_id": "CLM-SIM-03-001",
      "statement": "The memo was produced and reviewed for preliminary vendor-risk triage only.",
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
      "non_claim_id": "NC-SIM-03-001",
      "statement": "The preliminary triage record does not establish final vendor approval."
    },
    {
      "non_claim_id": "NC-SIM-03-002",
      "statement": "The preliminary triage record does not establish that the vendor is cleared for onboarding."
    },
    {
      "non_claim_id": "NC-SIM-03-003",
      "statement": "The preliminary triage record does not establish compliance."
    },
    {
      "non_claim_id": "NC-SIM-03-004",
      "statement": "The preliminary triage record does not establish legal sufficiency."
    },
    {
      "non_claim_id": "NC-SIM-03-005",
      "statement": "The preliminary triage record does not establish production readiness."
    },
    {
      "non_claim_id": "NC-SIM-03-006",
      "statement": "The preliminary triage record does not establish factual correctness of underlying vendor data."
    },
    {
      "non_claim_id": "NC-SIM-03-007",
      "statement": "The preliminary triage record does not transfer institutional authority."
    }
  ],
  "semantic_expansion_guard": {
    "source_scope": "PRELIMINARY_TRIAGE_ONLY",
    "prohibited_downstream_labels_without_new_authority": [
      "APPROVED_FOR_ONBOARDING",
      "CLEARED_FOR_ONBOARDING",
      "VENDOR_APPROVED",
      "VENDOR_CLEARED"
    ],
    "expansion_requires": [
      "new approval authority",
      "new evidence reference",
      "explicit downstream decision record"
    ]
  },
  "evidence_references": [
    {
      "evidence_id": "EVID-SIM-03-001",
      "description": "AI-assisted memo artifact reference",
      "status": "REFERENCED"
    },
    {
      "evidence_id": "EVID-SIM-03-002",
      "description": "Human preliminary review context",
      "status": "REFERENCED"
    }
  ],
  "revalidation_required_for": [
    "approval",
    "onboarding clearance",
    "authorization",
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
  "scenario_id": "SCENARIO_03_SCOPE_EXPANSION_ATTEMPT",
  "event_id": "CCE-SIM-03-001",
  "title": "Scenario 03 Claim Consumption Event",
  "consumer": {
    "system_id": "SYSTEM_D2_DOWNSTREAM_OPERATIONAL_LABELER",
    "consumer_role": "SECOND_DOWNSTREAM_CONSUMER_OR_STATUS_LABELER"
  },
  "consumed_claim": {
    "claim_id": "CLM-SIM-03-001",
    "statement": "The memo was produced and reviewed for preliminary vendor-risk triage only.",
    "recorded_scope": "PRELIMINARY_TRIAGE_ONLY"
  },
  "attempted_consumption": {
    "attempted_claim": "Vendor is approved / cleared for onboarding.",
    "attempted_scope": "FINAL_VENDOR_APPROVAL_OR_ONBOARDING_CLEARANCE",
    "consumption_effect": "EXPANDED",
    "semantic_shift": {
      "from": "reviewed for preliminary triage",
      "to": "approved / cleared for onboarding"
    },
    "new_authority_reference_present": false,
    "new_evidence_reference_present": false,
    "new_approval_record_present": false
  },
  "classification": {
    "consumption_classification": "SCOPE_EXPANSION_UNSUPPORTED",
    "unsupported_inheritance": true,
    "primary_category": "CLAIM_SCOPE_EXPANSION",
    "secondary_categories": [
      "AUTHORITY_LEAKAGE"
    ],
    "reason": "The downstream onboarding approval / cleared label exceeds the recorded preliminary triage scope and lacks new approval authority, new evidence, or an explicit downstream decision record."
  },
  "preserved_non_claims": [
    "Not final approval.",
    "Not onboarding clearance.",
    "Not compliance determination.",
    "Not legal sufficiency.",
    "Not production readiness.",
    "Not factual correctness guarantee.",
    "No authority transfer."
  ],
  "required_next_action": [
    "Treat downstream approval / cleared label as unsupported unless separately authorized.",
    "Request explicit approval authority and evidence before operational onboarding action."
  ],
  "fork_role": "RECORD_CONSUMPTION_AND_EXPOSE_SCOPE_EXPANSION"
}
'@

$smr = @'
{
  "artifact_type": "SYSTEM_MAPPING_RECEIPT",
  "artifact_version": "0.1",
  "scenario_id": "SCENARIO_03_SCOPE_EXPANSION_ATTEMPT",
  "receipt_id": "SMR-SIM-03-001",
  "title": "Scenario 03 System Mapping Receipt",
  "systems": [
    {
      "system_id": "SYSTEM_A_AI_ASSISTED_PRODUCTION",
      "native_responsibility": "Produce AI-assisted vendor-risk memo",
      "fork_does_not_become": "model evaluator"
    },
    {
      "system_id": "SYSTEM_B_FORK_BOUNDARY_RECORD_LAYER",
      "native_responsibility": "Preserve handoff state and expose boundary effects",
      "fork_does_not_become": "authority layer"
    },
    {
      "system_id": "SYSTEM_C_INSTITUTIONAL_REVIEW_CONTEXT",
      "native_responsibility": "Represent preliminary human review and policy context",
      "fork_does_not_become": "compliance decision-maker"
    },
    {
      "system_id": "SYSTEM_D1_FIRST_DOWNSTREAM_CONSUMER",
      "native_responsibility": "Consume preliminary review artifact within recorded scope",
      "fork_does_not_become": "runtime controller"
    },
    {
      "system_id": "SYSTEM_D2_DOWNSTREAM_OPERATIONAL_LABELER",
      "native_responsibility": "Apply operational status label",
      "fork_does_not_become": "approval authority"
    },
    {
      "system_id": "SYSTEM_E_AUDIT_RECONSTRUCTION_OVERSIGHT",
      "native_responsibility": "Reconstruct transition later",
      "fork_does_not_become": "legal authority"
    }
  ],
  "mapping": {
    "source_artifact": "ART-SIM-03-VENDOR-RISK-MEMO",
    "boundary_artifacts": [
      "BDR-SIM-03-001",
      "CBC-SIM-03-001",
      "CCE-SIM-03-001",
      "APC-SIM-03-001",
      "NCP-SIM-03-001"
    ],
    "consumer_event": "CCE-SIM-03-001",
    "unsupported_inheritance_event": "UIE-SIM-03-001"
  },
  "semantic_mapping": {
    "source_label": "PRELIMINARY_TRIAGE_REVIEWED",
    "downstream_label": "APPROVED_OR_CLEARED_FOR_ONBOARDING",
    "mapping_outcome": "EXPANDED_UNSUPPORTED"
  },
  "mapping_outcome": "MAPPED_WITH_SCOPE_EXPANSION_EXPOSED",
  "authority_transfer": false,
  "policy_approval_transfer": false,
  "runtime_control_transfer": false,
  "audit_authority_transfer": false,
  "reconstruction_posture": "UNSUPPORTED_INHERITANCE_EXPOSED"
}
'@

$uie = @'
{
  "artifact_type": "UNSUPPORTED_INHERITANCE_EVENT",
  "artifact_version": "0.1",
  "scenario_id": "SCENARIO_03_SCOPE_EXPANSION_ATTEMPT",
  "event_id": "UIE-SIM-03-001",
  "title": "Scenario 03 Unsupported Scope Expansion Event",
  "condition": "SIMULATION_TREATMENT",
  "workflow_id": "SIM-GOV-PROOF-SURFACE-03",
  "category": "CLAIM_SCOPE_EXPANSION",
  "secondary_categories": [
    "AUTHORITY_LEAKAGE"
  ],
  "actor_or_artifact": "SYSTEM_D2_DOWNSTREAM_OPERATIONAL_LABELER",
  "inferred_claim": "Vendor is approved / cleared for onboarding.",
  "record_support": "The record supports only that an AI-assisted vendor-risk memo was produced and reviewed for preliminary triage.",
  "why_unsupported": "The downstream approved / cleared label exceeds the recorded preliminary triage boundary and lacks separate approval authority, explicit onboarding clearance, or new supporting evidence.",
  "semantic_drift": {
    "from": "reviewed for preliminary triage",
    "to": "approved / cleared for onboarding",
    "drift_type": "NARROW_REVIEW_TO_OPERATIONAL_APPROVAL"
  },
  "evidence_refs": [
    "BDR-SIM-03-001",
    "CBC-SIM-03-001",
    "CCE-SIM-03-001",
    "SMR-SIM-03-001",
    "APC-SIM-03-001",
    "NCP-SIM-03-001"
  ],
  "coder_id": "SIMULATION_CODER",
  "adjudication_status": "AGREED",
  "adjudication_note": "Scenario 03 intentionally models a downstream status-label expansion from preliminary triage to onboarding approval / cleared status so Fork can expose the unsupported expansion without blocking it.",
  "fork_result": "SCOPE_EXPANSION_EXPOSED",
  "fork_non_authority_statement": "Fork exposes the boundary effect. Fork does not decide whether onboarding should occur."
}
'@

$apc = @'
Scenario 03 Authority Policy Context
Artifact ID: APC-SIM-03-001

Purpose
This context file records the authority and policy context present during Scenario 03.
It preserves context for reconstruction without asserting approval, onboarding clearance, compliance, applicability, legal sufficiency, or institutional authority.

Scenario
SCENARIO_03_SCOPE_EXPANSION_ATTEMPT

Recorded Role Context
A human reviewer in System C reviewed the AI-assisted vendor-risk memo for preliminary triage.

Recorded role context:
Vendor-risk analyst / preliminary reviewer

System D2 later applied or attempted to apply an operational label equivalent to:
approved / cleared for onboarding

Recorded Policy Context
Policy context was referenced for preliminary review.
Recorded policy reference:
VR-PRELIM-REVIEW-v0.1

Explicit Non-Claims
The recorded reviewer role does not establish final approval authority.
The recorded policy reference does not establish policy applicability.
The recorded policy reference does not establish compliance.
The recorded preliminary review does not establish onboarding clearance.
The recorded preliminary review does not establish legal sufficiency.
The recorded preliminary review does not establish production readiness.
The recorded preliminary review does not transfer institutional authority to Fork or to a downstream system.

Required Revalidation
Before downstream onboarding or operational action, the downstream system must obtain separate evidence or authority for:
final approval;
onboarding clearance;
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
Scenario 03 Non-Claims Panel
Artifact ID: NCP-SIM-03-001

Purpose
This panel preserves explicit non-claims for Scenario 03.
It is attached to the Fork-preserved handoff so downstream systems do not silently convert preliminary triage review into approval, clearance, compliance, correctness, or production readiness.

Non-Claims
This handoff record is not final vendor approval.
This handoff record is not onboarding clearance.
This handoff record is not a compliance determination.
This handoff record is not legal sufficiency.
This handoff record is not production readiness.
This handoff record is not a factual correctness guarantee.
This handoff record is not institutional authorization.
This handoff record does not transfer authority from System C to System D1 or System D2.
This handoff record does not convert a policy reference into policy applicability.
This handoff record does not convert preliminary review into final decision authority.
This handoff record does not convert "reviewed for preliminary triage" into "approved or cleared for onboarding."
This handoff record does not decide whether downstream reliance is justified.

Preserved Boundary
The only preserved positive claim is:
An AI-assisted vendor-risk memo was produced and reviewed for preliminary triage only.

Required Downstream Treatment
Any downstream claim of approval, onboarding clearance, authorization, compliance, legal sufficiency, production readiness, or factual correctness requires separate evidence or authority.

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
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_non_claims_panel.md"
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
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_unsupported_inheritance_event.json"
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
Write-Host "Checking Scenario 03 semantic classifications..."

$cce03 = Get-Content -Raw -Path "examples/simulations/governance-proof-surface/artifacts/scenario_03_claim_consumption_event.json" | ConvertFrom-Json
$uie03 = Get-Content -Raw -Path "examples/simulations/governance-proof-surface/artifacts/scenario_03_unsupported_inheritance_event.json" | ConvertFrom-Json
$bdr03 = Get-Content -Raw -Path "examples/simulations/governance-proof-surface/artifacts/scenario_03_boundary_delta_record.json" | ConvertFrom-Json

if ($cce03.classification.consumption_classification -ne "SCOPE_EXPANSION_UNSUPPORTED") {
    Write-Host "FAIL: Scenario 03 CCE must classify consumption as SCOPE_EXPANSION_UNSUPPORTED"
    exit 1
}

if ($uie03.category -ne "CLAIM_SCOPE_EXPANSION") {
    Write-Host "FAIL: Scenario 03 UIE primary category must be CLAIM_SCOPE_EXPANSION"
    exit 1
}

if ($bdr03.delta_classification.claim_scope -ne "EXPANDED") {
    Write-Host "FAIL: Scenario 03 BDR claim_scope must be EXPANDED"
    exit 1
}

if ($bdr03.downstream_semantic_change.new_authority_reference_present -ne $false) {
    Write-Host "FAIL: Scenario 03 must not include new authority reference in the downstream semantic change"
    exit 1
}

if ($bdr03.downstream_semantic_change.new_evidence_reference_present -ne $false) {
    Write-Host "FAIL: Scenario 03 must not include new evidence reference in the downstream semantic change"
    exit 1
}

Write-Host "PASS: Scenario 03 semantic classifications are bounded and explicit."
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

Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/scenario_03_scope_expansion_attempt.md" -Content $scenario03 -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/README.md" -Content $artifactReadme -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_03_boundary_delta_record.json" -Content $bdr -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_03_claim_boundary_contract.json" -Content $cbc -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_03_claim_consumption_event.json" -Content $cce -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_03_system_mapping_receipt.json" -Content $smr -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_03_unsupported_inheritance_event.json" -Content $uie -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_03_authority_policy_context.md" -Content $apc -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_03_non_claims_panel.md" -Content $ncp -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "scripts/run_ahi_sim_v0_1_checks.ps1" -Content $checkScript -Overwrite:$ForceOverwrite

Write-Host ""
Write-Host "Done."
Write-Host ""
Write-Host "Next commands:"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\\create_scenario_03_scope_expansion_artifacts_v0_1.ps1 -ForceOverwrite"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\\run_ahi_sim_v0_1_checks.ps1"