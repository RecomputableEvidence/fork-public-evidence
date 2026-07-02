# Fork Governance Simulation Proof Surface

## Purpose

This example package contains initial scenarios for the Fork Governance Simulation Proof Surface.

The simulation is a calibration environment for testing claim boundaries, handoff semantics, artifact formats, interface contracts, delegation behavior, and failure modes.

It is not a product demonstration. It does not establish compliance, approval, or correctness.

## Scenario Set

| Scenario | File | Purpose | Verification Posture |
|---|---|---|---|
| 01 | `scenario_01_baseline_unbounded_handoff.md` | Show failure mode without Fork | BASELINE — control case, not a Fork claim |
| 02 | `scenario_02_fork_preserved_handoff.md` | Show same workflow with Fork-style handoff records | STRUCTURAL — required files + JSON validity enforced by main checker |
| 03 | `scenario_03_scope_expansion_attempt.md` | Show downstream claim expansion | STRUCTURAL — required files + JSON validity enforced by main checker |
| 04 | `scenario_04_authority_leakage_attempt.md` | Show authority leakage | SEMANTICALLY VERIFIED — structural + explicit classification checks enforced by main checker |
| 05 | `scenario_05_policy_reference_laundering_attempt.md` | Show policy reference treated as compliance or approval | SEMANTICALLY VERIFIED — structural + explicit classification checks + dedicated overclaim scan enforced by main checker |
| 06 | `scenario_06_multi_system_distributed_handoff.md` | Show multi-system distributed handoff reconstruction | SCAFFOLD — narrative only, no artifact family, not yet wired into any checker |
## Simulation Standard

Each scenario must answer:

1. What crossed the boundary?
2. What did not cross the boundary?
3. What did the downstream system try to infer?
4. Did Fork preserve enough state to expose the inference?
5. What remains outside Fork's authority?

## Non-Claims

This simulation does not establish correctness, compliance, legal sufficiency, institutional authority, production readiness, or general validity.