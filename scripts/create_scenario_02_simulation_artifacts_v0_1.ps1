# scripts/create_scenario_02_simulation_artifacts_v0_1.ps1
# Creates Scenario 02 machine-readable simulation artifacts.
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

$artifactReadme = @'
# Scenario 02 Simulation Artifacts

## Purpose

This artifact bundle supports Scenario 02: Fork-Preserved Handoff.

The scenario models the same vendor-risk handoff as Scenario 01, but adds Fork-style boundary records so downstream reviewers can inspect claim scope, non-claims, authority context, unresolved state, and revalidation requirements.

## Artifact Set

| Artifact | File | Purpose |
|---|---|---|
| Boundary Delta Record | `scenario_02_boundary_delta_record.json` | Records the transition between upstream review state and downstream reliance attempt |
| Claim Boundary Contract | `scenario_02_claim_boundary_contract.json` | Defines what claim scope crossed and what did not cross |
| Claim Consumption Event | `scenario_02_claim_consumption_event.json` | Records how the downstream system consumed the upstream claim |
| System Mapping Receipt | `scenario_02_system_mapping_receipt.json` | Maps participating systems, roles, artifacts, and boundary posture |
| Unsupported Inheritance Event | `scenario_02_unsupported_inheritance_event.json` | Records the downstream inference that exceeded the recorded boundary |
| Authority Policy Context | `scenario_02_authority_policy_context.md` | Records policy and role context without asserting approval or compliance |
| Non-Claims Panel | `scenario_02_non_claims_panel.md` | Preserves explicit non-claims associated with the handoff |

## Expected Reconstruction Outcome

`UNSUPPORTED_INHERITANCE_EXPOSED`

## Non-Claims

This artifact bundle does not establish correctness, compliance, legal sufficiency, institutional authority, production readiness, or general validity.
'@

$bdr = @'
{
  "artifact_type": "BOUNDARY_DELTA_RECORD",
  "artifact_version": "0.1",
  "scenario_id": "SCENARIO_02_FORK_PRESERVED_HANDOFF",
  "record_id": "BDR-SIM-02-001",
  "title": "Scenario 02 Boundary Delta Record",
  "created_for": "Fork Governance Simulation Proof Surface",
  "transition": {
    "transition_id": "TRANSITION-SIM-02-001",
    "from_systems": [
      "SYSTEM_A_AI_ASSISTED_PRODUCTION",
      "SYSTEM_C_INSTITUTIONAL_REVIEW_CONTEXT"
    ],
    "through_system": "SYSTEM_B_FORK_BOUNDARY_RECORD_LAYER",
    "to_system": "SYSTEM_D_DOWNSTREAM_OPERATIONAL_DECISION",
    "reconstruction_system": "SYSTEM_E_AUDIT_RECONSTRUCTION_OVERSIGHT",
    "transition_kind": "AI_ASSISTED_VENDOR_RISK_MEMO_TO_DOWNSTREAM_CONSUMPTION"
  },
  "upstream_state": {
    "artifact_id": "ART-SIM-02-VENDOR-RISK-MEMO",
    "artifact_type": "AI_ASSISTED_VENDOR_RISK_MEMO",
    "recorded_claims": [
      {
        "claim_id": "CLM-SIM-02-001",
        "statement": "An AI-assisted vendor-risk memo was produced and reviewed for preliminary triage.",
        "scope": "PRELIMINARY_TRIAGE_ONLY",
        "status": "RECORDED"
      }
    ],
    "recorded_non_claims": [
      "No final vendor approval is asserted.",
      "No compliance determination is asserted.",
      "No legal sufficiency determination is asserted.",
      "No production readiness determination is asserted.",
      "No factual correctness guarantee is asserted.",
      "No institutional authorization is asserted."
    ],
    "unresolved_state": [
      {
        "unresolved_id": "UNRESOLVED-SIM-02-001",
        "description": "Final approval authority not established in the handoff record."
      },
      {
        "unresolved_id": "UNRESOLVED-SIM-02-002",
        "description": "Compliance status not determined in the handoff record."
      }
    ]
  },
  "downstream_attempted_inference": {
    "consumer_system": "SYSTEM_D_DOWNSTREAM_OPERATIONAL_DECISION",
    "attempted_inference_id": "INF-SIM-02-001",
    "statement": "Vendor is approved for onboarding.",
    "inference_type": "APPROVAL_STATUS_EXPANSION",
    "support_in_record": "NOT_SUPPORTED_BY_RECORDED_BOUNDARY"
  },
  "delta_classification": {
    "claim_scope": "EXPANDED",
    "authority_context": "NOT_TRANSFERRED",
    "policy_context": "REFERENCED_ONLY",
    "non_claims": "PRESERVED",
    "unresolved_state": "PRESERVED",
    "overall_boundary_effect": "UNSUPPORTED_INHERITANCE_EXPOSED"
  },
  "required_revalidation": [
    "Obtain explicit institutional approval authority before treating the vendor as approved.",
    "Obtain separate compliance determination before treating the workflow as compliant.",
    "Resolve or explicitly accept unresolved evidence gaps before downstream action."
  ],
  "inspectability_result": "INSPECTABLE",
  "fork_role": "PRESERVE_HANDOFF_STATE_ONLY",
  "fork_non_authority_statement": "Fork records the boundary state for inspection and reconstruction. Fork does not approve, authorize, certify, or determine the downstream action."
}
'@

$cbc = @'
{
  "artifact_type": "CLAIM_BOUNDARY_CONTRACT",
  "artifact_version": "0.1",
  "scenario_id": "SCENARIO_02_FORK_PRESERVED_HANDOFF",
  "contract_id": "CBC-SIM-02-001",
  "title": "Scenario 02 Claim Boundary Contract",
  "subject": {
    "artifact_id": "ART-SIM-02-VENDOR-RISK-MEMO",
    "artifact_type": "AI_ASSISTED_VENDOR_RISK_MEMO"
  },
  "boundary": {
    "from": "SYSTEM_A_AI_ASSISTED_PRODUCTION_AND_SYSTEM_C_REVIEW_CONTEXT",
    "to": "SYSTEM_D_DOWNSTREAM_OPERATIONAL_DECISION",
    "mediated_by": "SYSTEM_B_FORK_BOUNDARY_RECORD_LAYER"
  },
  "claims_allowed_to_cross": [
    {
      "claim_id": "CLM-SIM-02-001",
      "statement": "The memo was produced and reviewed for preliminary vendor-risk triage.",
      "scope": "PRELIMINARY_TRIAGE_ONLY",
      "conditions": [
        "May be used to understand what was reviewed.",
        "May be used to identify unresolved issues.",
        "May be used to request further review."
      ]
    }
  ],
  "claims_not_allowed_to_be_inferred": [
    {
      "non_claim_id": "NC-SIM-02-001",
      "statement": "The memo does not establish final vendor approval."
    },
    {
      "non_claim_id": "NC-SIM-02-002",
      "statement": "The memo does not establish compliance."
    },
    {
      "non_claim_id": "NC-SIM-02-003",
      "statement": "The memo does not establish legal sufficiency."
    },
    {
      "non_claim_id": "NC-SIM-02-004",
      "statement": "The memo does not establish production readiness."
    },
    {
      "non_claim_id": "NC-SIM-02-005",
      "statement": "The memo does not establish factual correctness of underlying vendor data."
    },
    {
      "non_claim_id": "NC-SIM-02-006",
      "statement": "The memo does not transfer institutional authority."
    }
  ],
  "evidence_references": [
    {
      "evidence_id": "EVID-SIM-02-001",
      "description": "AI-assisted memo artifact reference",
      "status": "REFERENCED"
    },
    {
      "evidence_id": "EVID-SIM-02-002",
      "description": "Human preliminary review context",
      "status": "REFERENCED"
    }
  ],
  "revalidation_required_for": [
    "approval",
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
  "scenario_id": "SCENARIO_02_FORK_PRESERVED_HANDOFF",
  "event_id": "CCE-SIM-02-001",
  "title": "Scenario 02 Claim Consumption Event",
  "consumer": {
    "system_id": "SYSTEM_D_DOWNSTREAM_OPERATIONAL_DECISION",
    "consumer_role": "DOWNSTREAM_OPERATIONAL_CONSUMER"
  },
  "consumed_claim": {
    "claim_id": "CLM-SIM-02-001",
    "statement": "The memo was produced and reviewed for preliminary vendor-risk triage.",
    "recorded_scope": "PRELIMINARY_TRIAGE_ONLY"
  },
  "attempted_consumption": {
    "attempted_claim": "Vendor is approved for onboarding.",
    "attempted_scope": "FINAL_VENDOR_APPROVAL",
    "consumption_effect": "EXPANDED",
    "new_authority_reference_present": false,
    "new_evidence_reference_present": false
  },
  "classification": {
    "consumption_classification": "EXPANDED_UNSUPPORTED",
    "unsupported_inheritance": true,
    "reason": "The downstream attempted claim exceeds the recorded preliminary triage scope and lacks new approval authority or evidence."
  },
  "preserved_non_claims": [
    "Not final approval.",
    "Not compliance determination.",
    "Not legal sufficiency.",
    "Not production readiness.",
    "Not factual correctness guarantee.",
    "No authority transfer."
  ],
  "required_next_action": [
    "Treat downstream approval claim as unsupported unless separately authorized.",
    "Request explicit approval authority and evidence before operational action."
  ],
  "fork_role": "RECORD_CONSUMPTION_AND_EXPOSE_BOUNDARY_EFFECT"
}
'@

$smr = @'
{
  "artifact_type": "SYSTEM_MAPPING_RECEIPT",
  "artifact_version": "0.1",
  "scenario_id": "SCENARIO_02_FORK_PRESERVED_HANDOFF",
  "receipt_id": "SMR-SIM-02-001",
  "title": "Scenario 02 System Mapping Receipt",
  "systems": [
    {
      "system_id": "SYSTEM_A_AI_ASSISTED_PRODUCTION",
      "native_responsibility": "Produce AI-assisted vendor-risk memo",
      "fork_does_not_become": "model_evaluator"
    },
    {
      "system_id": "SYSTEM_B_FORK_BOUNDARY_RECORD_LAYER",
      "native_responsibility": "Preserve handoff state",
      "fork_does_not_become": "authority_layer"
    },
    {
      "system_id": "SYSTEM_C_INSTITUTIONAL_REVIEW_CONTEXT",
      "native_responsibility": "Represent preliminary human review and policy context",
      "fork_does_not_become": "compliance_decision_maker"
    },
    {
      "system_id": "SYSTEM_D_DOWNSTREAM_OPERATIONAL_DECISION",
      "native_responsibility": "Consume artifact for routing or action",
      "fork_does_not_become": "runtime_controller"
    },
    {
      "system_id": "SYSTEM_E_AUDIT_RECONSTRUCTION_OVERSIGHT",
      "native_responsibility": "Reconstruct transition later",
      "fork_does_not_become": "legal_authority"
    }
  ],
  "mapping": {
    "source_artifact": "ART-SIM-02-VENDOR-RISK-MEMO",
    "boundary_artifacts": [
      "BDR-SIM-02-001",
      "CBC-SIM-02-001",
      "CCE-SIM-02-001",
      "APC-SIM-02-001",
      "NCP-SIM-02-001"
    ],
    "consumer_event": "CCE-SIM-02-001",
    "unsupported_inheritance_event": "UIE-SIM-02-001"
  },
  "mapping_outcome": "MAPPED_WITH_NON_INHERITANCE_BOUNDARY",
  "authority_transfer": false,
  "policy_approval_transfer": false,
  "runtime_control_transfer": false,
  "audit_authority_transfer": false,
  "reconstruction_posture": "RECONSTRUCTABLE_BOUNDARY"
}
'@

$uie = @'
{
  "artifact_type": "UNSUPPORTED_INHERITANCE_EVENT",
  "artifact_version": "0.1",
  "scenario_id": "SCENARIO_02_FORK_PRESERVED_HANDOFF",
  "event_id": "UIE-SIM-02-001",
  "title": "Scenario 02 Unsupported Inheritance Event",
  "condition": "TREATMENT",
  "workflow_id": "SIM-GOV-PROOF-SURFACE-02",
  "category": "AUTHORITY_LEAKAGE",
  "secondary_categories": [
    "CLAIM_SCOPE_EXPANSION",
    "PRODUCTION_READINESS_CONFUSION"
  ],
  "actor_or_artifact": "SYSTEM_D_DOWNSTREAM_OPERATIONAL_DECISION",
  "inferred_claim": "Vendor is approved for onboarding.",
  "record_support": "The record supports only that an AI-assisted vendor-risk memo was produced and reviewed for preliminary triage.",
  "why_unsupported": "The inferred approval claim exceeds the recorded boundary and lacks separate approval authority, compliance determination, or new evidence.",
  "evidence_refs": [
    "BDR-SIM-02-001",
    "CBC-SIM-02-001",
    "CCE-SIM-02-001",
    "SMR-SIM-02-001",
    "APC-SIM-02-001",
    "NCP-SIM-02-001"
  ],
  "coder_id": "SIMULATION_CODER",
  "adjudication_status": "AGREED",
  "adjudication_note": "Scenario 02 intentionally models the downstream approval inference as unsupported so the boundary-preservation artifacts can expose the inference without blocking it.",
  "fork_result": "UNSUPPORTED_INHERITANCE_EXPOSED",
  "fork_non_authority_statement": "Fork exposes the boundary effect. Fork does not decide whether onboarding should occur."
}
'@

$apc = @'
# Scenario 02 Authority Policy Context

Artifact ID: `APC-SIM-02-001`

## Purpose

This context file records the authority and policy context present during Scenario 02.

It preserves context for reconstruction without asserting approval, compliance, applicability, legal sufficiency, or institutional authority.

## Scenario

`SCENARIO_02_FORK_PRESERVED_HANDOFF`

## Systems

| System | Role |
|---|---|
| System A | AI-assisted production system |
| System B | Fork boundary-record layer |
| System C | Institutional review / policy context system |
| System D | Downstream operational or decision system |
| System E | Audit / reconstruction / oversight system |

## Recorded Role Context

A human reviewer in System C reviewed the AI-assisted vendor-risk memo for preliminary triage.

Recorded role context:

```text
Vendor-risk analyst / preliminary reviewer
```

## Recorded Policy Context

Policy context was referenced for preliminary review.

Recorded policy reference: `VR-PRELIM-REVIEW-v0.1`

## Explicit Non-Claims

- The recorded role context does not establish final approval authority.
- The recorded policy reference does not establish policy applicability.
- The recorded policy reference does not establish compliance.
- The recorded review does not establish legal sufficiency.
- The recorded review does not establish production readiness.
- The recorded review does not transfer institutional authority to Fork.

## Required Revalidation

Before downstream onboarding or operational action, the downstream system must obtain separate evidence or authority for:

- approval  
- compliance determination  
- legal sufficiency  
- production readiness  
- factual correctness  
- institutional authorization  

## Fork Role

Fork preserves this context as handoff state.  
Fork does not decide whether the policy applies, whether the policy was satisfied, or whether the reviewer had sufficient authority.
'@

$ncp = @'
Scenario 02 Non-Claims Panel
Artifact ID: NCP-SIM-02-001

Purpose
This panel preserves explicit non-claims for Scenario 02.
It is attached to the Fork-preserved handoff so downstream systems do not silently inherit authority, approval, compliance, correctness, or production-readiness claims from a preliminary review record.

Non-Claims
This handoff record is not final vendor approval.
This handoff record is not a compliance determination.
This handoff record is not legal sufficiency.
This handoff record is not production readiness.
This handoff record is not a factual correctness guarantee.
This handoff record is not institutional authorization.
This handoff record does not transfer authority from System C to System D.
This handoff record does not convert a policy reference into policy applicability.
This handoff record does not convert preliminary review into final decision authority.
This handoff record does not decide whether downstream reliance is justified.

Preserved Boundary
The only preserved positive claim is:
An AI-assisted vendor-risk memo was produced and reviewed for preliminary triage.

Required Downstream Treatment
Any downstream claim of approval, authorization, compliance, legal sufficiency, production readiness, or factual correctness requires separate evidence or authority.

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
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_non_claims_panel.md"
)

foreach ($path in $required) {
    if (-not (Test-Path $path)) {
        Write-Host "FAIL: missing required file: $path"
        exit 1
    }
    Write-Host "FOUND: $path"
}

Write-Host ""
Write-Host "Validating Scenario 02 JSON artifacts..."
$jsonFiles = @(
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_unsupported_inheritance_event.json"
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

Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/README.md" -Content $artifactReadme -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_02_boundary_delta_record.json" -Content $bdr -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_02_claim_boundary_contract.json" -Content $cbc -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_02_claim_consumption_event.json" -Content $cce -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_02_system_mapping_receipt.json" -Content $smr -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_02_unsupported_inheritance_event.json" -Content $uie -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_02_authority_policy_context.md" -Content $apc -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_02_non_claims_panel.md" -Content $ncp -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "scripts/run_ahi_sim_v0_1_checks.ps1" -Content $checkScript -Overwrite:$ForceOverwrite

Write-Host ""
Write-Host "Done."
Write-Host ""
Write-Host "Next commands:"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\\create_scenario_02_simulation_artifacts_v0_1.ps1 -ForceOverwrite"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\\run_ahi_sim_v0_1_checks.ps1"