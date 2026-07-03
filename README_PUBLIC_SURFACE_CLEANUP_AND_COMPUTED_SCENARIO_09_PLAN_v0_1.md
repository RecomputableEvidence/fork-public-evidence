# PUBLIC_SURFACE_CLEANUP_AND_COMPUTED_SCENARIO_09_PLAN_v0_1

This package adds a bounded public-surface cleanup and computed Scenario 09 planning layer.

## Files

```text
docs/reviewer/PUBLIC_SURFACE_CLEANUP_AND_COMPUTED_SCENARIO_09_PLAN_v0_1.md
docs/reviewer/AHI_REVIEWER_PACKET_LIMITATIONS_v0_1.md
docs/reviewer/AHI_COMPUTED_SCENARIO_09_PLAN_v0_1.md
scripts/check_no_mojibake_utf8_v0_1.ps1
scripts/check_public_surface_cleanup_and_computed_s09_plan_v0_1.ps1
```

## Apply

```powershell
cd C:\N\fork-public-evidence

git checkout main
git pull
git checkout -b public-surface-cleanup-computed-s09-plan-v0.1

Expand-Archive -Path "$env:USERPROFILE\Downloads\PUBLIC_SURFACE_CLEANUP_AND_COMPUTED_SCENARIO_09_PLAN_v0_1.zip" -DestinationPath "$env:TEMP\public-surface-cleanup-computed-s09-plan-v0.1" -Force

Copy-Item -Recurse -Force "$env:TEMP\public-surface-cleanup-computed-s09-plan-v0.1\*" "C:\N\fork-public-evidence\"
```

## Validate

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_public_surface_cleanup_and_computed_s09_plan_v0_1.ps1

powershell -ExecutionPolicy Bypass -File scripts\check_no_mojibake_utf8_v0_1.ps1

git diff --check
git status -sb
```

The no-mojibake check may fail until the actual cleanup pass is performed if existing repo files still contain mojibake. That failure is useful because it gives a concrete cleanup target.

## Commit

```powershell
git add `
  docs\reviewer\PUBLIC_SURFACE_CLEANUP_AND_COMPUTED_SCENARIO_09_PLAN_v0_1.md `
  docs\reviewer\AHI_REVIEWER_PACKET_LIMITATIONS_v0_1.md `
  docs\reviewer\AHI_COMPUTED_SCENARIO_09_PLAN_v0_1.md `
  scripts\check_no_mojibake_utf8_v0_1.ps1 `
  scripts\check_public_surface_cleanup_and_computed_s09_plan_v0_1.ps1 `
  README_PUBLIC_SURFACE_CLEANUP_AND_COMPUTED_SCENARIO_09_PLAN_v0_1.md

git commit -m "Add public surface cleanup and computed Scenario 09 plan"
```

## Boundary

This package does not implement computed Scenario 09 v0.2. It creates the public plan, limitation language, and cleanup checks that should precede broader cold review and the next substantive proof-surface step.
