# AHI Viewer Comparison Mode v0.2

## Purpose

Viewer Comparison Mode v0.2 adds a reviewer-facing comparison surface for AHI scenarios.

The viewer is static, repo-local, and read-only. It compares scenario pairs by boundary movement, attempted inference, required revalidation, and Fork non-claims.

## Adds

- `docs/viewer/ahi-viewer-v0_2/README.md`
- `docs/viewer/ahi-viewer-v0_2/index.html`
- `docs/viewer/ahi-viewer-v0_2/app.js`
- `docs/viewer/ahi-viewer-v0_2/styles.css`
- `docs/viewer/ahi-viewer-v0_2/data/comparison_pairs.json`
- `docs/viewer/ahi-viewer-v0_2/schema/comparison_pairs.schema.json`
- `docs/releases/AHI_VIEWER_v0_2_COMPARISON_MODE.md`
- `scripts/build_ahi_viewer_comparison_data_v0_2.ps1`
- `scripts/build_ahi_viewer_comparison_data_v0_2.py`
- `scripts/check_ahi_viewer_v0_2.ps1`

## Non-authority boundary

Viewer v0.2 does not approve, certify, score, authorize, determine compliance, determine admissibility, establish legal sufficiency, decide acceptance, or judge correctness.

It presents bounded comparison data so a reviewer can inspect what crossed, what did not cross, what was inferred, what required revalidation, and what Fork refused to claim.

## Suggested branch

```powershell
git checkout main
git pull
git checkout -b ahi-viewer-comparison-v0.2
```

## Apply

```powershell
Expand-Archive -Path "$env:USERPROFILE\Downloads\ahi_viewer_comparison_mode_v0_2.zip" -DestinationPath "$env:TEMP\ahi-viewer-comparison-v0.2" -Force

Copy-Item -Recurse -Force "$env:TEMP\ahi-viewer-comparison-v0.2\*" "C:\N\fork-public-evidence\"
```

## Build deterministic comparison data

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_ahi_viewer_comparison_data_v0_2.ps1 -ForceOverwrite
```

## Check

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1
```

After committing, run deterministic check:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1 -CheckDeterminism
```
