# AHI Simulation v0.1.8 — Scenario 07 External Authority Bridge

## Summary

Scenario 07 adds an external-authority bridge simulation.

It tests what happens when a Fork-preserved internal workflow record is provided to an external reviewer, auditor, regulator, customer, board, insurer, legal process, or other authority-bearing context.

## Failure mode

`EXTERNAL_AUTHORITY_BRIDGE_ATTEMPT`

The external context attempts to treat record inspectability as if it established:

- external admissibility;
- regulatory compliance;
- legal sufficiency;
- external approval;
- audit acceptance;
- customer acceptance;
- board authorization;
- insurance coverage;
- enforcement defense;
- execution eligibility.

## Fork result

Fork records the unsupported inference. Fork does not approve, certify, score, authorize, determine compliance, determine admissibility, establish legal sufficiency, decide acceptance, or judge correctness.

## Verification

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_scenario_07_external_authority_bridge_v0_1.ps1
powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism
```

## Suggested tag

```powershell
git tag -a ahi-sim-v0.1.8 -m "Scenario 07 external authority bridge simulation"
git push origin ahi-sim-v0.1.8
```

Optional viewer tag:

```powershell
git tag -a ahi-viewer-v0.1.5 -m "AHI viewer v0.1.5 Scenario 07 external authority bridge support"
git push origin ahi-viewer-v0.1.5
```
