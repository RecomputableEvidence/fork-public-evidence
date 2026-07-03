# Scenario 09 Integration Patch v0.1

## Purpose

This patch integrates already-committed Scenario 09 artifacts into the active AHI proof surface.

It patches:

- `examples/simulations/governance-proof-surface/scenario_registry.json`
- `scripts/run_ahi_sim_v0_1_checks.ps1`
- `docs/viewer/ahi-viewer-v0_1/data/scenarios_bundle.json`
- `docs/viewer/ahi-viewer-v0_2/data/comparison_pairs.json`, when the v0.2 builder is present

It does not commit, push, or tag.

## Apply

From repo root on the Scenario 09 branch:

```powershell
Expand-Archive -Path "$env:USERPROFILE\Downloads\scenario_09_integration_patch_v0_1.zip" -DestinationPath "$env:TEMP\scenario-09-integration-patch-v0.1" -Force

Copy-Item -Recurse -Force "$env:TEMP\scenario-09-integration-patch-v0.1\*" "C:\N\fork-public-evidence\"

powershell -ExecutionPolicy Bypass -File scripts\apply_scenario_09_revocation_visibility_split_state_v0_1.ps1
```

## Validate

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_scenario_09_revocation_visibility_split_state_v0_1.ps1
powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1
git diff --check
git status -sb
```

After committing this integration patch, run determinism:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1 -CheckDeterminism
```
