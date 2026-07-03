# AHI Simulation v0.1.7 — Scenario 06 Semantic Verification

## Summary

This release promotes Scenario 06 from structural simulation to semantic-invariant verification.

Scenario 06 models a three-system handoff:

1. System A produces a bounded intake/triage summary.
2. System B narrows the summary into routing context.
3. System C attempts to treat the routed summary as authority-bearing.

The verified failure mode is **distributed authority inheritance**.

## What is verified

- The BDR has two explicit transition boundaries.
- S06-B01 preserves/narrows without authority transfer.
- S06-B02 records unsupported authority inheritance.
- The CBC prohibits authority, approval, compliance, execution, and legal-sufficiency inference.
- The CCE classifies System C consumption as `EXPANDED`.
- The SMR records unsupported distributed authority inheritance.
- The failure event marks the downstream inference as `NOT_SUPPORTED`.
- Required revalidation remains preserved.
- Non-authority language remains explicit.

## What is not verified

This release does not establish that the downstream decision was correct, approved, compliant, authorized, legally sufficient, or executable.

Fork does not approve, certify, score, authorize, determine compliance, establish legal sufficiency, or judge correctness.

## Verification

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_scenario_06_semantic_invariants_v0_1.ps1
powershell -ExecutionPolicy Bypass -File scripts\check_scenario_06_multi_system_distributed_handoff_v0_1.ps1
powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism
```

## Suggested tag

```powershell
git tag -a ahi-sim-v0.1.7 -m "Scenario 06 semantic invariant verification"
git push origin ahi-sim-v0.1.7
```
