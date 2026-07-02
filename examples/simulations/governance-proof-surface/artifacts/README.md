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

## Non-Claims

These artifact bundles do not establish correctness, compliance, legal sufficiency, institutional authority, production readiness, or general validity.