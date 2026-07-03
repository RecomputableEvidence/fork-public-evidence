# Scenario Registry Viewer Consistency Patch v0.1

## Purpose

This patch normalizes the Scenario 06–09 entries in `scenario_registry.json` so the live viewer reflects the verification posture actually present in the repo.

It addresses:

- false checker-coverage badges caused by missing `main_checker` boolean keys;
- stale copied `purpose` text for Scenarios 07–09;
- `artifact_family_present: false` contradictions where artifact families exist;
- unstructured `viewer_treatment` entries that left viewer display groups blank;
- non-zero-padded `scenario_number` values;
- stale copied categories and viewer notes for Scenarios 07–09.

The patch is descriptive. It does not introduce new semantic authority, approval, compliance, admissibility, legal-sufficiency, correctness, negligence, or execution-eligibility claims.

## Apply

From repo root:

```powershell
cd C:\N\fork-public-evidence

git checkout main
git pull
git checkout -b scenario-registry-viewer-consistency-v0.1

Expand-Archive -Path "$env:USERPROFILE\Downloads\scenario_registry_viewer_consistency_patch_v0_1.zip" -DestinationPath "$env:TEMP\scenario-registry-viewer-consistency-v0.1" -Force

Copy-Item -Recurse -Force "$env:TEMP\scenario-registry-viewer-consistency-v0.1\*" "C:\N\fork-public-evidence\"
```

## Verify registry consistency

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_scenario_registry_viewer_consistency_v0_1.ps1
```

## Rebuild viewer bundle

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_ahi_viewer_data_v0_1.ps1 -ForceOverwrite
```

## Validate without determinism first

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1
git diff --check
git status -sb
```

## Commit

```powershell
git add `
  examples\simulations\governance-proof-surface\scenario_registry.json `
  docs\viewer\ahi-viewer-v0_1\data\scenarios_bundle.json `
  scripts\check_scenario_registry_viewer_consistency_v0_1.ps1 `
  README_SCENARIO_REGISTRY_VIEWER_CONSISTENCY_PATCH_v0_1.md

git commit -m "Normalize scenario registry viewer posture fields"
```

## Run determinism after commit

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1 -CheckDeterminism
git status -sb
```
