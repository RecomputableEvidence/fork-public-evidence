# scripts/create_scenario_05_non_claim_suppression_artifacts_v0_1.ps1
# Creates Scenario 05 policy-reference laundering / non-claim suppression artifacts.
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

function Add-Scenario05ToArtifactReadme {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Section
    )

    if (-not (Test-Path $Path)) {
        Write-Utf8NoBomFile -Path $Path -Content ("# Governance Proof Surface Simulation Artifacts`n`n" + $Section) -Overwrite
        return
    }

    $text = Get-Content -Raw -Path $Path

    if ($text -match "## Scenario 05 Artifact Set") {
        Write-Host "SKIP existing Scenario 05 README section: $Path"
        return
    }

    if ($text -match "(?s)\r?\n## Non-Claims") {
        $updated = [regex]::Replace($text, "(?s)(\r?\n## Non-Claims)", "`n" + $Section + "`n`$1", 1)
    } else {
        $updated = $text.TrimEnd() + "`n`n" + $Section + "`n"
    }

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $updated, $utf8NoBom)
    Write-Host "UPDATED: $Path"
}

$scenario05 = @'
# Scenario 05: Policy-Reference Laundering / Non-Claim Suppression Attempt

## Purpose

This scenario tests whether Fork exposes a downstream handoff failure in which a favorable upstream claim is preserved while the non-claims and limitations required to interpret that claim are dropped, compressed, or hidden.

The concrete subcase is policy-reference laundering:

```text
policy referenced during preliminary review -> policy applied / policy satisfied / compliant
```

Scenario 05 is therefore not a truth, safety, compliance, or legal-sufficiency test. It is a boundary-state test. The question is whether the handoff record makes limitation loss visible.

## Participating Systems

| System | Role |
|---|---|
| System A | AI-assisted vendor-risk memo production |
| System B | Fork boundary-record layer |
| System C | Preliminary human review / policy-reference context |
| System D | Downstream decision memo / operational consumer |
| System E | Audit / reconstruction / oversight system |

## Flow

1. System A produces an AI-assisted vendor-risk memo.
2. System C performs preliminary review and references `VR-PRELIM-REVIEW-v0.1`.
3. System B preserves the positive claim and the material non-claims attached to the handoff.
4. System D drafts a downstream memo that keeps the positive claim but omits the limitations.
5. System D treats a referenced policy as if the policy applied, was satisfied, or established compliance.
6. System E reconstructs the transition and identifies non-claim suppression and policy-reference laundering.

## Upstream Positive Claim

The upstream record supports only this bounded claim:

```text
An AI-assisted vendor-risk memo was produced and reviewed for preliminary vendor-risk triage, with a preliminary review policy reference recorded.
```

## Material Non-Claims

The upstream record does not establish:

- policy applicability,
- policy satisfaction,
- compliance,
- legal sufficiency,
- final vendor approval,
- onboarding clearance,
- production readiness,
- factual correctness of underlying vendor data,
- closure of unresolved issues,
- authority transfer.

## Downstream Laundered Inference

The downstream memo treats the record as if it supports:

```text
The vendor-risk workflow complied with the referenced policy and is cleared for downstream reliance.
```

## Expected Classification

Primary category:

- `NON_CLAIM_SUPPRESSION`

Secondary categories:

- `POLICY_REFERENCE_LAUNDERING`
- `COMPLIANCE_CERTIFICATION_CONFUSION`
- `LIMITATION_LAUNDERING`
- `UNSUPPORTED_INHERITANCE`

## Expected Fork Behavior

Fork does not block the downstream memo and does not decide whether the policy applied, whether the policy was satisfied, whether the vendor should be approved, or whether the final decision is compliant.

Fork preserves the original boundary state and exposes that material non-claims were suppressed during handoff.

## What Crossed the Boundary

- AI-assisted vendor-risk memo reference.
- Preliminary review claim.
- Policy reference.
- Original non-claims.
- Unresolved issues.
- Revalidation requirements.

## What Did Not Cross the Boundary

- Policy applicability.
- Policy satisfaction.
- Compliance determination.
- Legal sufficiency.
- Final approval.
- Onboarding clearance.
- Production readiness.
- Institutional authorization.
- Truth certification.

## Reconstruction Result

Expected outcome:

```text
NON_CLAIM_SUPPRESSION_EXPOSED
```

## Non-Claims

This scenario does not establish correctness, compliance, legal sufficiency, institutional authority, production readiness, or general validity.

This scenario tests whether downstream suppression of limitations becomes inspectable.
'@

$originalNonClaims = @'
# Scenario 05 Original Non-Claims Panel

Artifact ID: `ONCP-SIM-05-001`

## Purpose

This file records the non-claims present before the downstream memo compresses or suppresses them.

## Positive Claim Preserved Upstream

The upstream record supports only:

```text
An AI-assisted vendor-risk memo was produced and reviewed for preliminary vendor-risk triage, with policy reference VR-PRELIM-REVIEW-v0.1 recorded.
```

## Original Material Non-Claims

The upstream record does not establish:

1. policy applicability,
2. policy satisfaction,
3. compliance,
4. legal sufficiency,
5. final vendor approval,
6. onboarding clearance,
7. production readiness,
8. factual correctness of underlying vendor data,
9. closure of unresolved issues,
10. authority transfer,
11. institutional authorization,
12. downstream reliance justification.

## Required Downstream Treatment

A downstream artifact may cite the positive claim only if it also preserves the limitations required to interpret that claim correctly.

Any downstream assertion of compliance, approval, clearance, policy satisfaction, or legal sufficiency requires a separate authority basis and evidence reference.

## Fork Role

Fork preserves this panel as boundary state.

Fork does not decide whether the policy applies, whether it was satisfied, or whether the downstream action should occur.
'@

$policyContext = @'
# Scenario 05 Policy Reference Context

Artifact ID: `PRC-SIM-05-001`

## Purpose

This context file records a policy reference without converting that reference into policy applicability, policy satisfaction, compliance, approval, or authorization.

## Scenario

`SCENARIO_05_POLICY_REFERENCE_LAUNDERING_ATTEMPT`

## Recorded Policy Reference

Policy reference:

```text
VR-PRELIM-REVIEW-v0.1
```

Recorded use:

```text
Referenced during preliminary vendor-risk review.
```

## What the Reference Supports

The record supports that a policy identifier was referenced during preliminary review.

## What the Reference Does Not Support

The record does not establish that:

- the policy applied to the vendor,
- the policy version was current,
- the policy was satisfied,
- the policy created approval authority,
- the workflow complied with the policy,
- compliance was certified,
- legal sufficiency was determined,
- onboarding was cleared.

## Revalidation Required

Before downstream reliance on policy satisfaction or compliance, the downstream system must obtain separate evidence for:

- policy applicability,
- current policy version,
- required controls,
- satisfaction of required controls,
- authorized reviewer identity,
- approval decision,
- compliance determination,
- unresolved issue disposition.

## Fork Role

Fork preserves the distinction between policy referenced and policy satisfied.
'@

$downstreamMemoExcerpt = @'
# Scenario 05 Downstream Memo Excerpt

Artifact ID: `DME-SIM-05-001`

## Purpose

This excerpt models the downstream language that creates the laundering event.

## Downstream Text Under Review

```text
The vendor-risk memo was reviewed under VR-PRELIM-REVIEW-v0.1. Based on that review, the workflow complied with the applicable vendor-risk policy and the recommendation may be relied on for downstream onboarding.
```

## Boundary Problem

The excerpt preserves the favorable positive claim:

```text
The memo was reviewed and a policy reference was present.
```

But it suppresses the limitations that made the upstream claim bounded.

The downstream text converts:

```text
policy referenced
```

into:

```text
policy applied and was satisfied
```

and further converts:

```text
preliminary review
```

into:

```text
downstream onboarding reliance
```

## Expected Classification

```text
NON_CLAIM_SUPPRESSION
POLICY_REFERENCE_LAUNDERING
COMPLIANCE_CERTIFICATION_CONFUSION
LIMITATION_LAUNDERING
```

## Fork Non-Claim

Fork does not determine whether the downstream text is legally wrong, operationally wrong, or noncompliant.

Fork records that the downstream text exceeds the preserved boundary unless separate evidence and authority are attached.
'@

$nonClaimsPanel = @'
# Scenario 05 Non-Claims Panel

Artifact ID: `NCP-SIM-05-001`

## Purpose

This panel preserves the explicit non-claims that must remain attached to the Scenario 05 handoff.

## Non-Claims

This handoff record is not policy applicability.

This handoff record is not policy satisfaction.

This handoff record is not a compliance determination.

This handoff record is not legal sufficiency.

This handoff record is not final vendor approval.

This handoff record is not onboarding clearance.

This handoff record is not production readiness.

This handoff record is not a factual correctness guarantee.

This handoff record is not closure of unresolved issues.

This handoff record is not institutional authorization.

This handoff record does not transfer authority.

This handoff record does not convert a policy reference into policy satisfaction.

This handoff record does not convert preliminary review into downstream onboarding clearance.

This handoff record does not decide whether downstream reliance is justified.

## Preserved Positive Claim

The only preserved positive claim is:

```text
An AI-assisted vendor-risk memo was produced and reviewed for preliminary vendor-risk triage, with a preliminary review policy reference recorded.
```

## Required Downstream Treatment

Any downstream claim of policy applicability, policy satisfaction, compliance, legal sufficiency, approval, clearance, production readiness, or correctness requires separate evidence or authority.

## Fork Role

Fork preserves the non-claims.

Fork does not enforce, approve, authorize, certify, or adjudicate the downstream action.
'@

$bdr = @'
{
  "artifact_type": "BOUNDARY_DELTA_RECORD",
  "artifact_version": "0.1",
  "scenario_id": "SCENARIO_05_POLICY_REFERENCE_LAUNDERING_ATTEMPT",
  "record_id": "BDR-SIM-05-001",
  "title": "Scenario 05 Boundary Delta Record",
  "created_for": "Fork Governance Simulation Proof Surface",
  "transition": {
    "transition_id": "TRANSITION-SIM-05-001",
    "from_systems": [
      "SYSTEM_A_AI_ASSISTED_PRODUCTION",
      "SYSTEM_C_PRELIMINARY_REVIEW_POLICY_CONTEXT"
    ],
    "through_system": "SYSTEM_B_FORK_BOUNDARY_RECORD_LAYER",
    "to_system": "SYSTEM_D_DOWNSTREAM_DECISION_MEMO",
    "reconstruction_system": "SYSTEM_E_AUDIT_RECONSTRUCTION_OVERSIGHT",
    "transition_kind": "PRELIMINARY_REVIEW_POLICY_REFERENCE_TO_DOWNSTREAM_RELIANCE_MEMO",
    "failure_mode_under_test": "NON_CLAIM_SUPPRESSION_AND_POLICY_REFERENCE_LAUNDERING"
  },
  "upstream_state": {
    "artifact_id": "ART-SIM-05-VENDOR-RISK-MEMO",
    "artifact_type": "AI_ASSISTED_VENDOR_RISK_MEMO",
    "recorded_claims": [
      {
        "claim_id": "CLM-SIM-05-001",
        "statement": "An AI-assisted vendor-risk memo was produced and reviewed for preliminary vendor-risk triage, with policy reference VR-PRELIM-REVIEW-v0.1 recorded.",
        "scope": "PRELIMINARY_TRIAGE_WITH_POLICY_REFERENCE_ONLY",
        "status": "RECORDED"
      }
    ],
    "recorded_policy_context": [
      {
        "policy_id": "VR-PRELIM-REVIEW-v0.1",
        "description": "Vendor-risk preliminary review policy reference",
        "recorded_effect": "REFERENCED_ONLY",
        "policy_applicability_established": false,
        "policy_satisfaction_established": false,
        "compliance_established": false
      }
    ],
    "recorded_non_claims": [
      "The policy reference does not establish policy applicability.",
      "The policy reference does not establish policy satisfaction.",
      "The policy reference does not establish compliance.",
      "The preliminary review does not establish legal sufficiency.",
      "The preliminary review does not establish final vendor approval.",
      "The preliminary review does not establish onboarding clearance.",
      "The preliminary review does not establish production readiness.",
      "The preliminary review does not establish factual correctness of underlying vendor data.",
      "The preliminary review does not establish closure of unresolved issues.",
      "The preliminary review does not transfer institutional authorization."
    ],
    "unresolved_state": [
      {
        "unresolved_id": "UNRESOLVED-SIM-05-001",
        "description": "Policy applicability not established."
      },
      {
        "unresolved_id": "UNRESOLVED-SIM-05-002",
        "description": "Policy satisfaction not established."
      },
      {
        "unresolved_id": "UNRESOLVED-SIM-05-003",
        "description": "Compliance determination not established."
      },
      {
        "unresolved_id": "UNRESOLVED-SIM-05-004",
        "description": "Onboarding clearance not established."
      }
    ]
  },
  "downstream_suppression": {
    "consumer_system": "SYSTEM_D_DOWNSTREAM_DECISION_MEMO",
    "suppression_id": "SUPPRESS-SIM-05-001",
    "preserved_positive_claims": [
      "The vendor-risk memo was reviewed and a policy reference was recorded."
    ],
    "suppressed_non_claims": [
      "No policy applicability determination.",
      "No policy satisfaction determination.",
      "No compliance determination.",
      "No legal sufficiency determination.",
      "No final vendor approval.",
      "No onboarding clearance.",
      "No production readiness.",
      "No factual correctness guarantee.",
      "No closure of unresolved issues.",
      "No authority transfer."
    ],
    "downstream_inference": "The workflow complied with the referenced vendor-risk policy and may be relied on for downstream onboarding.",
    "suppression_vectors": [
      "NON_CLAIM_DROPPED",
      "LIMITATION_COMPRESSED",
      "POLICY_REFERENCE_TO_POLICY_SATISFACTION",
      "PRELIMINARY_REVIEW_TO_DOWNSTREAM_CLEARANCE"
    ],
    "new_policy_applicability_record_present": false,
    "new_policy_satisfaction_record_present": false,
    "new_compliance_determination_present": false,
    "new_approval_record_present": false
  },
  "delta_classification": {
    "claim_scope": "EXPANDED",
    "non_claims": "SUPPRESSED",
    "limitations": "DROPPED",
    "policy_reference": "LAUNDERED",
    "authority_context": "PRESERVED_NOT_TRANSFERRED",
    "unresolved_state": "SUPPRESSED",
    "overall_boundary_effect": "NON_CLAIM_SUPPRESSION_EXPOSED"
  },
  "required_revalidation": [
    "Establish policy applicability before treating the policy reference as applicable.",
    "Establish policy satisfaction before treating the workflow as policy-satisfied.",
    "Establish compliance before treating the workflow as compliant.",
    "Establish approval authority before treating preliminary review as approval.",
    "Resolve unresolved issues before treating downstream reliance as cleared."
  ],
  "inspectability_result": "INSPECTABLE",
  "fork_role": "PRESERVE_HANDOFF_STATE_AND_EXPOSE_NON_CLAIM_SUPPRESSION",
  "fork_non_authority_statement": "Fork exposes non-claim suppression and policy-reference laundering for inspection and reconstruction. Fork does not determine compliance, legal sufficiency, approval, or downstream permission."
}
'@

$cbc = @'
{
  "artifact_type": "CLAIM_BOUNDARY_CONTRACT",
  "artifact_version": "0.1",
  "scenario_id": "SCENARIO_05_POLICY_REFERENCE_LAUNDERING_ATTEMPT",
  "contract_id": "CBC-SIM-05-001",
  "title": "Scenario 05 Claim Boundary Contract",
  "subject": {
    "artifact_id": "ART-SIM-05-VENDOR-RISK-MEMO",
    "artifact_type": "AI_ASSISTED_VENDOR_RISK_MEMO"
  },
  "boundary": {
    "from": "SYSTEM_A_AI_ASSISTED_PRODUCTION_AND_SYSTEM_C_PRELIMINARY_REVIEW_CONTEXT",
    "to": "SYSTEM_D_DOWNSTREAM_DECISION_MEMO",
    "mediated_by": "SYSTEM_B_FORK_BOUNDARY_RECORD_LAYER"
  },
  "claims_allowed_to_cross": [
    {
      "claim_id": "CLM-SIM-05-001",
      "statement": "The memo was produced and reviewed for preliminary vendor-risk triage, with policy reference VR-PRELIM-REVIEW-v0.1 recorded.",
      "scope": "PRELIMINARY_TRIAGE_WITH_POLICY_REFERENCE_ONLY",
      "conditions": [
        "May be used to understand what preliminary review occurred.",
        "May be used to identify that a policy reference was recorded.",
        "May be used to identify unresolved issues.",
        "May be used to request additional review, approval, policy applicability determination, or revalidation."
      ]
    }
  ],
  "material_non_claims_required_to_cross": [
    {
      "non_claim_id": "NC-SIM-05-001",
      "statement": "The policy reference does not establish policy applicability."
    },
    {
      "non_claim_id": "NC-SIM-05-002",
      "statement": "The policy reference does not establish policy satisfaction."
    },
    {
      "non_claim_id": "NC-SIM-05-003",
      "statement": "The policy reference does not establish compliance."
    },
    {
      "non_claim_id": "NC-SIM-05-004",
      "statement": "The preliminary review does not establish legal sufficiency."
    },
    {
      "non_claim_id": "NC-SIM-05-005",
      "statement": "The preliminary review does not establish final vendor approval."
    },
    {
      "non_claim_id": "NC-SIM-05-006",
      "statement": "The preliminary review does not establish onboarding clearance."
    },
    {
      "non_claim_id": "NC-SIM-05-007",
      "statement": "The preliminary review does not establish production readiness."
    },
    {
      "non_claim_id": "NC-SIM-05-008",
      "statement": "The preliminary review does not establish factual correctness of underlying vendor data."
    },
    {
      "non_claim_id": "NC-SIM-05-009",
      "statement": "The preliminary review does not establish closure of unresolved issues."
    },
    {
      "non_claim_id": "NC-SIM-05-010",
      "statement": "The preliminary review does not transfer institutional authorization."
    }
  ],
  "claims_not_allowed_to_be_inferred": [
    "Policy applied.",
    "Policy was satisfied.",
    "Workflow complied with the policy.",
    "Vendor was approved.",
    "Vendor was cleared for onboarding.",
    "Legal sufficiency was determined.",
    "Production readiness was established.",
    "Underlying vendor data was verified as true.",
    "Unresolved issues were closed.",
    "Authority transferred."
  ],
  "suppression_guard": {
    "policy_reference_may_be_treated_as_policy_satisfaction": false,
    "omitted_non_claims_may_be_treated_as_resolved": false,
    "preliminary_review_may_be_treated_as_downstream_clearance": false,
    "positive_claim_may_be_preserved_without_material_limitations": false
  },
  "evidence_references": [
    {
      "evidence_id": "EVID-SIM-05-001",
      "description": "AI-assisted vendor-risk memo artifact reference",
      "status": "REFERENCED"
    },
    {
      "evidence_id": "EVID-SIM-05-002",
      "description": "Preliminary review context",
      "status": "REFERENCED"
    },
    {
      "evidence_id": "EVID-SIM-05-003",
      "description": "Policy reference VR-PRELIM-REVIEW-v0.1",
      "status": "REFERENCED_ONLY"
    },
    {
      "evidence_id": "EVID-SIM-05-004",
      "description": "Original non-claims panel",
      "status": "REQUIRED_TO_PRESERVE"
    }
  ],
  "revalidation_required_for": [
    "policy applicability",
    "policy satisfaction",
    "compliance determination",
    "legal sufficiency",
    "final approval",
    "onboarding clearance",
    "production readiness",
    "factual correctness",
    "unresolved issue closure",
    "authority transfer"
  ],
  "contract_result": "BOUNDARY_STRUCTURE_RECORDED_ONLY",
  "non_claims_preserved": true
}
'@

$cce = @'
{
  "artifact_type": "CLAIM_CONSUMPTION_EVENT",
  "artifact_version": "0.1",
  "scenario_id": "SCENARIO_05_POLICY_REFERENCE_LAUNDERING_ATTEMPT",
  "event_id": "CCE-SIM-05-001",
  "title": "Scenario 05 Claim Consumption Event",
  "consumer": {
    "system_id": "SYSTEM_D_DOWNSTREAM_DECISION_MEMO",
    "consumer_role": "DOWNSTREAM_MEMO_AUTHOR_OR_ROUTING_SYSTEM"
  },
  "consumed_claim": {
    "claim_id": "CLM-SIM-05-001",
    "statement": "The memo was produced and reviewed for preliminary vendor-risk triage, with policy reference VR-PRELIM-REVIEW-v0.1 recorded.",
    "recorded_scope": "PRELIMINARY_TRIAGE_WITH_POLICY_REFERENCE_ONLY"
  },
  "attempted_consumption": {
    "attempted_claim": "The workflow complied with the referenced vendor-risk policy and may be relied on for downstream onboarding.",
    "attempted_scope": "POLICY_SATISFACTION_COMPLIANCE_AND_DOWNSTREAM_RELIANCE",
    "consumption_effect": "EXPANDED",
    "non_claim_treatment": "SUPPRESSED",
    "limitation_treatment": "DROPPED",
    "policy_shift": {
      "from": "POLICY_REFERENCED",
      "to": "POLICY_APPLIED_SATISFIED_OR_COMPLIED_WITH"
    },
    "new_policy_applicability_record_present": false,
    "new_policy_satisfaction_record_present": false,
    "new_compliance_determination_present": false,
    "new_approval_record_present": false
  },
  "classification": {
    "consumption_classification": "NON_CLAIM_SUPPRESSION_UNSUPPORTED",
    "unsupported_inheritance": true,
    "primary_category": "NON_CLAIM_SUPPRESSION",
    "secondary_categories": [
      "POLICY_REFERENCE_LAUNDERING",
      "COMPLIANCE_CERTIFICATION_CONFUSION",
      "LIMITATION_LAUNDERING",
      "UNSUPPORTED_INHERITANCE"
    ],
    "reason": "The downstream memo preserves the favorable review and policy-reference claim while dropping material non-claims and treating a policy reference as policy satisfaction or compliance without a new determination."
  },
  "dropped_non_claims": [
    "No policy applicability determination.",
    "No policy satisfaction determination.",
    "No compliance determination.",
    "No legal sufficiency determination.",
    "No final vendor approval.",
    "No onboarding clearance.",
    "No production readiness.",
    "No factual correctness guarantee.",
    "No unresolved issue closure.",
    "No authority transfer."
  ],
  "required_next_action": [
    "Restore material non-claims to the downstream memo.",
    "Obtain separate policy applicability evidence before asserting applicability.",
    "Obtain separate policy satisfaction evidence before asserting satisfaction.",
    "Obtain separate compliance determination before asserting compliance.",
    "Obtain separate approval or clearance before downstream onboarding reliance."
  ],
  "fork_role": "RECORD_CONSUMPTION_AND_EXPOSE_NON_CLAIM_SUPPRESSION"
}
'@

$smr = @'
{
  "artifact_type": "SYSTEM_MAPPING_RECEIPT",
  "artifact_version": "0.1",
  "scenario_id": "SCENARIO_05_POLICY_REFERENCE_LAUNDERING_ATTEMPT",
  "receipt_id": "SMR-SIM-05-001",
  "title": "Scenario 05 System Mapping Receipt",
  "systems": [
    {
      "system_id": "SYSTEM_A_AI_ASSISTED_PRODUCTION",
      "native_responsibility": "Produce AI-assisted vendor-risk memo",
      "fork_does_not_become": "model evaluator"
    },
    {
      "system_id": "SYSTEM_B_FORK_BOUNDARY_RECORD_LAYER",
      "native_responsibility": "Preserve handoff state and expose boundary effects",
      "fork_does_not_become": "compliance authority"
    },
    {
      "system_id": "SYSTEM_C_PRELIMINARY_REVIEW_POLICY_CONTEXT",
      "native_responsibility": "Record preliminary review and policy reference context",
      "fork_does_not_become": "policy interpreter"
    },
    {
      "system_id": "SYSTEM_D_DOWNSTREAM_DECISION_MEMO",
      "native_responsibility": "Consume artifact and produce downstream memo or routing action",
      "fork_does_not_become": "runtime controller"
    },
    {
      "system_id": "SYSTEM_E_AUDIT_RECONSTRUCTION_OVERSIGHT",
      "native_responsibility": "Reconstruct transition later",
      "fork_does_not_become": "legal authority"
    }
  ],
  "mapping": {
    "source_artifact": "ART-SIM-05-VENDOR-RISK-MEMO",
    "boundary_artifacts": [
      "BDR-SIM-05-001",
      "CBC-SIM-05-001",
      "CCE-SIM-05-001",
      "PRC-SIM-05-001",
      "ONCP-SIM-05-001",
      "NCP-SIM-05-001"
    ],
    "consumer_event": "CCE-SIM-05-001",
    "suppressed_limitations_event": "SLE-SIM-05-001"
  },
  "policy_reference_mapping": {
    "recorded_policy_reference": "VR-PRELIM-REVIEW-v0.1",
    "recorded_effect": "REFERENCED_ONLY",
    "downstream_inferred_effect": "POLICY_APPLIED_SATISFIED_OR_COMPLIED_WITH",
    "mapping_outcome": "POLICY_REFERENCE_LAUNDERING_UNSUPPORTED"
  },
  "non_claim_mapping": {
    "original_non_claims_present": true,
    "downstream_non_claims_preserved": false,
    "suppression_outcome": "MATERIAL_NON_CLAIMS_DROPPED"
  },
  "mapping_outcome": "MAPPED_WITH_NON_CLAIM_SUPPRESSION_EXPOSED",
  "authority_transfer": false,
  "policy_approval_transfer": false,
  "runtime_control_transfer": false,
  "audit_authority_transfer": false,
  "reconstruction_posture": "NON_CLAIM_SUPPRESSION_EXPOSED"
}
'@

$suppressedLimitationsEvent = @'
{
  "artifact_type": "SUPPRESSED_LIMITATIONS_EVENT",
  "artifact_version": "0.1",
  "scenario_id": "SCENARIO_05_POLICY_REFERENCE_LAUNDERING_ATTEMPT",
  "event_id": "SLE-SIM-05-001",
  "title": "Scenario 05 Suppressed Limitations Event",
  "condition": "SIMULATION_TREATMENT",
  "workflow_id": "SIM-GOV-PROOF-SURFACE-05",
  "category": "NON_CLAIM_SUPPRESSION",
  "secondary_categories": [
    "POLICY_REFERENCE_LAUNDERING",
    "COMPLIANCE_CERTIFICATION_CONFUSION",
    "LIMITATION_LAUNDERING",
    "UNSUPPORTED_INHERITANCE"
  ],
  "actor_or_artifact": "SYSTEM_D_DOWNSTREAM_DECISION_MEMO",
  "downstream_excerpt_artifact": "DME-SIM-05-001",
  "preserved_positive_claim": "The vendor-risk memo was reviewed and a policy reference was recorded.",
  "suppressed_limitations": [
    "No policy applicability determination.",
    "No policy satisfaction determination.",
    "No compliance determination.",
    "No legal sufficiency determination.",
    "No final vendor approval.",
    "No onboarding clearance.",
    "No production readiness.",
    "No factual correctness guarantee.",
    "No unresolved issue closure.",
    "No authority transfer."
  ],
  "inferred_claim": "The workflow complied with the referenced vendor-risk policy and may be relied on for downstream onboarding.",
  "record_support": "The record supports only preliminary review with a policy reference recorded.",
  "why_unsupported": "The downstream artifact suppresses material limitations and treats policy reference as policy satisfaction or compliance without separate evidence or authority.",
  "evidence_refs": [
    "BDR-SIM-05-001",
    "CBC-SIM-05-001",
    "CCE-SIM-05-001",
    "SMR-SIM-05-001",
    "PRC-SIM-05-001",
    "ONCP-SIM-05-001",
    "NCP-SIM-05-001",
    "DME-SIM-05-001"
  ],
  "coder_id": "SIMULATION_CODER",
  "adjudication_status": "AGREED",
  "adjudication_note": "Scenario 05 intentionally models non-claim suppression and policy-reference laundering so Fork can expose the unsupported boundary expansion without deciding compliance.",
  "fork_result": "NON_CLAIM_SUPPRESSION_EXPOSED",
  "fork_non_authority_statement": "Fork exposes the limitation-suppression boundary effect. Fork does not decide whether the policy applied, whether it was satisfied, or whether onboarding should occur."
}
'@

$scenario05Checker = @'
# scripts/check_scenario_05_non_claim_suppression_v0_1.ps1
# Validates Scenario 05 policy-reference laundering / non-claim suppression artifacts.
# Does not stage, commit, push, or tag.

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".git")) {
    throw "Run this script from the repository root, e.g. C:\N\fork-public-evidence"
}

Write-Host "Checking Scenario 05 required files..."

$required = @(
    "examples/simulations/governance-proof-surface/scenario_05_policy_reference_laundering_attempt.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_original_non_claims_panel.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_policy_reference_context.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_downstream_memo_excerpt.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_non_claims_panel.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_suppressed_limitations_event.json"
)

foreach ($path in $required) {
    if (-not (Test-Path $path)) {
        Write-Host "FAIL: missing required Scenario 05 file: $path"
        exit 1
    }

    Write-Host "FOUND: $path"
}

Write-Host ""
Write-Host "Validating Scenario 05 JSON artifacts..."

$jsonFiles = @(
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_suppressed_limitations_event.json"
)

foreach ($path in $jsonFiles) {
    try {
        Get-Content -Raw -Path $path | ConvertFrom-Json | Out-Null
        Write-Host "VALID JSON: $path"
    } catch {
        Write-Host "FAIL: invalid JSON: $path"
        Write-Host $_.Exception.Message
        exit 1
    }
}

Write-Host ""
Write-Host "Checking Scenario 05 semantic classifications..."

$bdr = Get-Content -Raw -Path "examples/simulations/governance-proof-surface/artifacts/scenario_05_boundary_delta_record.json" | ConvertFrom-Json
$cbc = Get-Content -Raw -Path "examples/simulations/governance-proof-surface/artifacts/scenario_05_claim_boundary_contract.json" | ConvertFrom-Json
$cce = Get-Content -Raw -Path "examples/simulations/governance-proof-surface/artifacts/scenario_05_claim_consumption_event.json" | ConvertFrom-Json
$smr = Get-Content -Raw -Path "examples/simulations/governance-proof-surface/artifacts/scenario_05_system_mapping_receipt.json" | ConvertFrom-Json
$sle = Get-Content -Raw -Path "examples/simulations/governance-proof-surface/artifacts/scenario_05_suppressed_limitations_event.json" | ConvertFrom-Json

if ($bdr.delta_classification.non_claims -ne "SUPPRESSED") {
    Write-Host "FAIL: Scenario 05 BDR must classify non_claims as SUPPRESSED"
    exit 1
}

if ($bdr.delta_classification.policy_reference -ne "LAUNDERED") {
    Write-Host "FAIL: Scenario 05 BDR must classify policy_reference as LAUNDERED"
    exit 1
}

if ($bdr.downstream_suppression.new_compliance_determination_present -ne $false) {
    Write-Host "FAIL: Scenario 05 downstream suppression must not include a new compliance determination"
    exit 1
}

if ($cbc.suppression_guard.policy_reference_may_be_treated_as_policy_satisfaction -ne $false) {
    Write-Host "FAIL: Scenario 05 CBC must forbid treating policy reference as policy satisfaction"
    exit 1
}

if ($cbc.suppression_guard.positive_claim_may_be_preserved_without_material_limitations -ne $false) {
    Write-Host "FAIL: Scenario 05 CBC must forbid preserving positive claim without material limitations"
    exit 1
}

if ($cce.classification.primary_category -ne "NON_CLAIM_SUPPRESSION") {
    Write-Host "FAIL: Scenario 05 CCE primary category must be NON_CLAIM_SUPPRESSION"
    exit 1
}

if ($cce.classification.consumption_classification -ne "NON_CLAIM_SUPPRESSION_UNSUPPORTED") {
    Write-Host "FAIL: Scenario 05 CCE consumption classification must be NON_CLAIM_SUPPRESSION_UNSUPPORTED"
    exit 1
}

if ($smr.non_claim_mapping.downstream_non_claims_preserved -ne $false) {
    Write-Host "FAIL: Scenario 05 SMR must record downstream non-claims as not preserved"
    exit 1
}

if ($sle.category -ne "NON_CLAIM_SUPPRESSION") {
    Write-Host "FAIL: Scenario 05 suppressed limitations event category must be NON_CLAIM_SUPPRESSION"
    exit 1
}

if ($sle.fork_result -ne "NON_CLAIM_SUPPRESSION_EXPOSED") {
    Write-Host "FAIL: Scenario 05 suppressed limitations event fork_result must be NON_CLAIM_SUPPRESSION_EXPOSED"
    exit 1
}

Write-Host "PASS: Scenario 05 non-claim suppression and policy-reference laundering classifications are bounded and explicit."

Write-Host ""
Write-Host "Scanning Scenario 05 surface for prohibited overclaim language..."

$scanFiles = @(
    "examples/simulations/governance-proof-surface/scenario_05_policy_reference_laundering_attempt.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_original_non_claims_panel.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_policy_reference_context.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_downstream_memo_excerpt.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_non_claims_panel.md"
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

$violations = @()

foreach ($file in $scanFiles) {
    foreach ($pattern in $patterns) {
        $matches = Select-String -Path $file -Pattern $pattern -SimpleMatch -CaseSensitive:$false
        foreach ($match in $matches) {
            $violations += [PSCustomObject]@{
                Path = $file
                LineNumber = $match.LineNumber
                Pattern = $pattern
                Line = $match.Line.Trim()
            }
        }
    }
}

if ($violations.Count -gt 0) {
    Write-Host "FAIL: prohibited Scenario 05 overclaim language found:"
    foreach ($v in $violations) {
        Write-Host "$($v.Path):$($v.LineNumber):[$($v.Pattern)] $($v.Line)"
    }
    exit 1
}

Write-Host "PASS: no prohibited Scenario 05 overclaim language found."
Write-Host ""
Write-Host "PASS: Scenario 05 policy-reference laundering / non-claim suppression checks completed."
'@

$artifactReadmeSection = @'
## Scenario 05 Artifact Set

| Artifact | File | Purpose |
|---|---|---|
| Boundary Delta Record | scenario_05_boundary_delta_record.json | Records limitation suppression and policy-reference laundering during downstream memo transition |
| Claim Boundary Contract | scenario_05_claim_boundary_contract.json | Defines what preliminary review and policy-reference claims may cross, and which non-claims must remain attached |
| Claim Consumption Event | scenario_05_claim_consumption_event.json | Records downstream consumption that expands policy reference into policy satisfaction / compliance |
| System Mapping Receipt | scenario_05_system_mapping_receipt.json | Maps systems and highlights the non-claim suppression path |
| Suppressed Limitations Event | scenario_05_suppressed_limitations_event.json | Records the material limitations dropped by the downstream artifact |
| Original Non-Claims Panel | scenario_05_original_non_claims_panel.md | Preserves the upstream limitations before suppression |
| Policy Reference Context | scenario_05_policy_reference_context.md | Records policy reference without treating it as policy applicability or satisfaction |
| Downstream Memo Excerpt | scenario_05_downstream_memo_excerpt.md | Provides the downstream text that launders the policy reference |
| Non-Claims Panel | scenario_05_non_claims_panel.md | Restates explicit non-claims required for reconstruction |
'@


Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/scenario_05_policy_reference_laundering_attempt.md" -Content $scenario05 -Overwrite:$ForceOverwrite

Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_05_original_non_claims_panel.md" -Content $originalNonClaims -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_05_policy_reference_context.md" -Content $policyContext -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_05_downstream_memo_excerpt.md" -Content $downstreamMemoExcerpt -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_05_non_claims_panel.md" -Content $nonClaimsPanel -Overwrite:$ForceOverwrite

Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_05_boundary_delta_record.json" -Content $bdr -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_05_claim_boundary_contract.json" -Content $cbc -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_05_claim_consumption_event.json" -Content $cce -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_05_system_mapping_receipt.json" -Content $smr -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/artifacts/scenario_05_suppressed_limitations_event.json" -Content $suppressedLimitationsEvent -Overwrite:$ForceOverwrite

Write-Utf8NoBomFile -Path "scripts/check_scenario_05_non_claim_suppression_v0_1.ps1" -Content $scenario05Checker -Overwrite:$ForceOverwrite

Add-Scenario05ToArtifactReadme -Path "examples/simulations/governance-proof-surface/artifacts/README.md" -Section $artifactReadmeSection

Write-Host ""
Write-Host "Done."
Write-Host ""
Write-Host "Next commands:"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\check_scenario_05_non_claim_suppression_v0_1.ps1"
Write-Host "  git diff --stat -- examples\simulations\governance-proof-surface scripts\create_scenario_05_non_claim_suppression_artifacts_v0_1.ps1 scripts\check_scenario_05_non_claim_suppression_v0_1.ps1"
