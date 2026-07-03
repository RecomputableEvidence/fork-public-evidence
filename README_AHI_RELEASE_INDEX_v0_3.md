# AHI Release Index v0.3 + Reviewer Packet v0.1

Refreshes the public AHI proof surface after Scenario 09 and adds a reviewer-facing map.

## Current release position

- `ahi-sim-v0.1.10`
- `ahi-viewer-v0.1.7`
- `ahi-viewer-v0.2.2`
- Scenario count: 9
- Latest scenario: Scenario 09 — Revocation Visibility / Split-State Boundary

## Adds

- `docs/releases/AHI_RELEASE_INDEX_v0_3.md`
- `docs/releases/AHI_VERIFICATION_MATRIX_v0_3.md`
- `docs/releases/AHI_SCENARIO_LADDER_v0_3.md`
- `docs/releases/AHI_VIEWER_RELEASE_LADDER_v0_3.md`
- `docs/releases/AHI_LOCAL_VERIFICATION_GUIDE_v0_3.md`
- `docs/reviewer/AHI_PROOF_SURFACE_MAP_v0_1.md`
- `docs/reviewer/FORK_AHI_REVIEWER_PACKET_v0_1.md`
- `scripts/create_ahi_release_index_v0_3.ps1`

## Apply

```powershell
cd C:\N\fork-public-evidence

git checkout main
git pull
git checkout -b ahi-release-index-v0.3-reviewer-map

Expand-Archive -Path "$env:USERPROFILE\Downloads\ahi_release_index_v0_3_and_reviewer_packet_v0_1.zip" -DestinationPath "$env:TEMP\ahi-release-index-v0.3-reviewer-map" -Force

Copy-Item -Recurse -Force "$env:TEMP\ahi-release-index-v0.3-reviewer-map\*" "C:\N\fork-public-evidence\"

powershell -ExecutionPolicy Bypass -File scripts\create_ahi_release_index_v0_3.ps1 -ForceOverwrite
```

## Validate

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1 -CheckDeterminism

git diff --check
git status -sb
```
