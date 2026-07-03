# AHI Release Index v0.2 Package

## Purpose

This package refreshes the AHI public release surface after Scenario 08.

It creates the v0.2 release-index document family:

- `docs/releases/AHI_RELEASE_INDEX_v0_2.md`
- `docs/releases/AHI_VERIFICATION_MATRIX_v0_2.md`
- `docs/releases/AHI_SCENARIO_LADDER_v0_2.md`
- `docs/releases/AHI_VIEWER_RELEASE_LADDER_v0_2.md`
- `docs/releases/AHI_LOCAL_VERIFICATION_GUIDE_v0_2.md`

It also includes:

- `scripts/create_ahi_release_index_v0_2.ps1`

## Current endpoint captured

- `ahi-sim-v0.1.9` — Scenario 08 stale validity / authority revocation boundary
- `ahi-viewer-v0.1.6` — Viewer v0.1 Scenario 08 support
- `ahi-viewer-v0.2.1` — Viewer v0.2 Scenario 08 comparison support

## Apply

From repo root:

```powershell
cd C:\N\fork-public-evidence

git checkout main
git pull
git checkout -b ahi-release-index-v0.2

Expand-Archive -Path "$env:USERPROFILE\Downloads\ahi_release_index_v0_2.zip" -DestinationPath "$env:TEMP\ahi-release-index-v0.2" -Force

Copy-Item -Recurse -Force "$env:TEMP\ahi-release-index-v0.2\*" "C:\N\fork-public-evidence\"

powershell -ExecutionPolicy Bypass -File scripts\create_ahi_release_index_v0_2.ps1 -ForceOverwrite
```

## Verify

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1 -CheckDeterminism
git diff --check
git status -sb
```

## Commit

```powershell
git add `
  docs\releases\AHI_RELEASE_INDEX_v0_2.md `
  docs\releases\AHI_VERIFICATION_MATRIX_v0_2.md `
  docs\releases\AHI_SCENARIO_LADDER_v0_2.md `
  docs\releases\AHI_VIEWER_RELEASE_LADDER_v0_2.md `
  docs\releases\AHI_LOCAL_VERIFICATION_GUIDE_v0_2.md `
  scripts\create_ahi_release_index_v0_2.ps1

git commit -m "Refresh AHI release index for Scenario 08"
git push -u origin ahi-release-index-v0.2
```

## Tag after merge to main

```powershell
git tag -a ahi-release-index-v0.2 -m "AHI release index v0.2 Scenario 08 refresh"
git push origin ahi-release-index-v0.2
```
