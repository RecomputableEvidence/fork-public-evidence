# AHI Simulation v0.1.9 — Scenario 08 Stale Validity / Authority Revocation Boundary

## Summary

Scenario 08 adds temporal validity and revocation-state coverage to the AHI simulation proof surface.

It tests what happens when a prior Fork-preserved record was valid or inspectable in an earlier validity window, but a later authority, policy, role, evidence, purpose, environment, or time-window change occurs and a downstream actor attempts to rely on the old record as if it were still current.

## Failure mode

`STALE_VALIDITY_RELIANCE_ATTEMPT`

The downstream context attempts to treat prior validity as if it established:

- current authority;
- current approval;
- current policy satisfaction;
- current regulatory compliance;
- current legal sufficiency;
- current evidence sufficiency;
- current execution eligibility;
- current external acceptance.

## Fork result

Fork records the unsupported stale-validity inference and preserves required current revalidation.

Fork does not approve, certify, score, authorize, determine compliance, determine admissibility, establish legal sufficiency, decide acceptance, or judge correctness.

## Verification

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_scenario_08_stale_validity_authority_revocation_v0_1.ps1
powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism
```

If Viewer v0.2 is present and patched:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1 -CheckDeterminism
```

## Suggested tags

```powershell
git tag -a ahi-sim-v0.1.9 -m "Scenario 08 stale validity and authority revocation boundary"

git push origin ahi-sim-v0.1.9
```

Optional viewer tags:

```powershell
git tag -a ahi-viewer-v0.1.6 -m "AHI viewer v0.1.6 Scenario 08 stale validity support"

git push origin ahi-viewer-v0.1.6
```

If Viewer v0.2 comparison data is updated:

```powershell
git tag -a ahi-viewer-v0.2.1 -m "AHI viewer v0.2.1 Scenario 08 comparison support"

git push origin ahi-viewer-v0.2.1
```
