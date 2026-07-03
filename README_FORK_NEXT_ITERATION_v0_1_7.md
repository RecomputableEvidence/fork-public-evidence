# Fork Next Iteration v0.1.7

This package advances Fork after `ahi-sim-v0.1.6` by adding a semantic-invariant checker for Scenario 06 and release/roadmap notes.

## Adds

- `scripts/check_scenario_06_semantic_invariants_v0_1.ps1`
- `scripts/apply_scenario_06_semantic_verification_v0_1.ps1`
- `docs/releases/AHI_SIM_v0_1_7_SCENARIO_06_SEMANTIC_VERIFICATION.md`
- `docs/roadmap/FORK_NEXT_ITERATION_v0_1_7.md`

## Purpose

Scenario 06 is already artifact-backed and structurally checkable. This iteration promotes it toward `SEMANTICALLY_VERIFIED` by checking explicit invariants:

- System A to System B preserves/narrows without authority transfer.
- System B to System C records unsupported authority inheritance.
- The CCE remains `EXPANDED`.
- The SMR records unsupported distributed authority inheritance.
- The failure event remains `NOT_SUPPORTED`.
- Revalidation remains required for approval authority, policy satisfaction, and execution eligibility.
- Fork's non-authority posture remains explicit.

## Boundary

This package does not approve, certify, score, authorize, determine compliance, establish legal sufficiency, or judge correctness.

## Suggested branch

`scenario-06-semantic-verification-v0.1`
