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