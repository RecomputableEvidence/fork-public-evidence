# Scenario 09 — Revocation Visibility / Split-State Boundary v0.1

## Purpose

Scenario 09 tests a distributed visibility and propagation failure.

Scenario 08 established:

```text
Prior validity does not imply current validity.
```

Scenario 09 extends that into split state:

```text
A validity change that exists in one system is not automatically visible, consumed, or operative in another system.
```

The failure mode is `REVOCATION_VISIBILITY_GAP`.

## Apply

```powershell
cd C:\N\fork-public-evidence
git checkout main
git pull
git checkout -b scenario-09-revocation-visibility-split-state-v0.1

Expand-Archive -Path "$env:USERPROFILE\Downloads\scenario_09_revocation_visibility_split_state_v0_1.zip" -DestinationPath "$env:TEMP\scenario-09-revocation-visibility-split-state-v0.1" -Force
Copy-Item -Recurse -Force "$env:TEMP\scenario-09-revocation-visibility-split-state-v0.1\*" "C:\N\fork-public-evidence\"
```

## Verify local artifacts

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_scenario_09_revocation_visibility_split_state_v0_1.ps1
```
