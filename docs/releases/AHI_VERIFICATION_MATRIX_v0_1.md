# AHI Verification Matrix v0.1

## Purpose

This matrix maps each AHI scenario to its failure mode, verification posture, artifacts, checker coverage, viewer visibility, and non-claims boundary.

## Matrix

| Scenario | Failure mode | Verification posture | Artifact family | Dedicated checker | Main checker integration | Viewer-visible | Latest sim tag | Fork verifies | Fork does not verify |
|---:|---|---|---|---|---|---|---|---|---|
| 01 | Baseline unbounded handoff | Baseline / contrast | Scenario narrative | Main simulation surface | `scripts/run_ahi_sim_v0_1_checks.ps1` | Yes | Pre-v0.1.5 surface | Shows the unbounded handoff problem space | Approval, compliance, correctness, authority, legal sufficiency |
| 02 | Preserved handoff | Artifact-backed | BDR, CBC, CCE, SMR, unsupported inheritance event, authority context, non-claims panel | Main simulation surface | `scripts/run_ahi_sim_v0_1_checks.ps1` | Yes | Pre-v0.1.5 surface | Preserved claim boundary and non-claim state | Truth, approval, compliance, authority, correctness |
| 03 | Scope expansion attempt | Artifact-backed | BDR, CBC, CCE, SMR, unsupported inheritance event, authority context, non-claims panel | Main simulation surface | `scripts/run_ahi_sim_v0_1_checks.ps1` | Yes | Pre-v0.1.5 surface | Unsupported downstream scope expansion is visible | Whether expanded claim is true, approved, compliant, or authorized |
| 04 | Authority leakage attempt | Semantically classified | BDR, CBC, CCE, SMR, unsupported inheritance event, authority context, non-claims panel | Main simulation semantic classification checks | `scripts/run_ahi_sim_v0_1_checks.ps1` | Yes | Pre-v0.1.5 surface | Authority-context leakage is bounded and explicit | Whether authority actually exists or was validly exercised |
| 05 | Policy-reference laundering / non-claim suppression | Dedicated checker integrated | BDR, CBC, CCE, SMR, suppressed limitations event, policy context, downstream memo, non-claims panels | `scripts/check_scenario_05_policy_reference_laundering_v0_1.ps1` | `scripts/run_ahi_sim_v0_1_checks.ps1` | Yes | `ahi-sim-v0.1.5` / `ahi-sim-v0.1.5-checker-integrated` | Policy reference and non-claim suppression are detected | Policy satisfaction, compliance, approval, or legal sufficiency |
| 06 | Multi-system distributed handoff | Structural + semantic invariant verification | BDR, CBC, CCE, SMR, distributed authority failure event, transition graph, non-claims panel | `scripts/check_scenario_06_multi_system_distributed_handoff_v0_1.ps1`; `scripts/check_scenario_06_semantic_invariants_v0_1.ps1` | `scripts/run_ahi_sim_v0_1_checks.ps1` | Yes | `ahi-sim-v0.1.6`; `ahi-sim-v0.1.7` | Distributed authority non-inheritance and required revalidation are preserved | Approval authority, policy satisfaction, compliance, execution eligibility, correctness |
| 07 | External authority bridge | Semantically verified | BDR, CBC, CCE, SMR, external authority failure event, external review context, transition graph, non-claims panel | `scripts/check_scenario_07_external_authority_bridge_v0_1.ps1` | `scripts/run_ahi_sim_v0_1_checks.ps1` | Yes | `ahi-sim-v0.1.8` | Unsupported external-authority inference is recorded | External admissibility, regulatory compliance, legal sufficiency, approval, customer/audit/board/insurer acceptance, execution eligibility |

## Checker coverage summary

| Checker | Scope |
|---|---|
| `scripts/run_ahi_sim_v0_1_checks.ps1` | Main simulation proof-surface checker |
| `scripts/check_ahi_viewer_v0_1.ps1` | Viewer bundle, registry alignment, posture enum, referenced paths, selected fields, unsafe JS scan, non-authority posture, deterministic builder behavior |
| `scripts/check_scenario_05_policy_reference_laundering_v0_1.ps1` | Scenario 05 policy-reference laundering and non-claim suppression |
| `scripts/check_scenario_06_multi_system_distributed_handoff_v0_1.ps1` | Scenario 06 structural distributed handoff checks |
| `scripts/check_scenario_06_semantic_invariants_v0_1.ps1` | Scenario 06 semantic invariant checks |
| `scripts/check_scenario_07_external_authority_bridge_v0_1.ps1` | Scenario 07 external authority bridge checks |

## Non-authority invariant

Across all scenarios, Fork remains an evidence-boundary and transition-state preservation surface.

Fork does not approve, certify, score, authorize, determine compliance, determine admissibility, establish legal sufficiency, decide acceptance, or judge correctness.