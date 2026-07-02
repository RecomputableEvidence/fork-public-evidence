# Fork Governance Simulation Proof Surface

## Purpose

This example package contains initial scenarios for the Fork Governance Simulation Proof Surface.

The simulation is a calibration environment for testing claim boundaries, handoff semantics, artifact formats, interface contracts, delegation behavior, and failure modes.

It is not a product demonstration, compliance proof, approval system, or correctness engine.

## Scenario Set

| Scenario | File | Purpose |
|---|---|---|
| 01 | `scenario_01_baseline_unbounded_handoff.md` | Show failure mode without Fork |
| 02 | `scenario_02_fork_preserved_handoff.md` | Show same workflow with Fork-style handoff records |
| 03 | `scenario_03_scope_expansion_attempt.md` | Show downstream claim expansion |
| 04 | `scenario_04_authority_leakage_attempt.md` | Show authority leakage |
| 05 | `scenario_05_policy_reference_laundering_attempt.md` | Show policy reference treated as compliance or approval |
| 06 | `scenario_06_multi_system_distributed_handoff.md` | Show multi-system distributed handoff reconstruction |

## Simulation Standard

Each scenario must answer:

1. What crossed the boundary?
2. What did not cross the boundary?
3. What did the downstream system try to infer?
4. Did Fork preserve enough state to expose the inference?
5. What remains outside Fork's authority?

## Non-Claims

This simulation does not establish correctness, compliance, legal sufficiency, institutional authority, production readiness, or general validity.