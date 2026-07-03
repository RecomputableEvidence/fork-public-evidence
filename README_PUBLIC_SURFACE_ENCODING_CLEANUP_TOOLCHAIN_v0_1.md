# Public Surface Encoding Cleanup Toolchain v0.1

## Purpose

This package creates a strict allowlist-driven encoding cleanup toolchain for the Fork public surface.

It is designed for the dedicated branch:

```powershell
public-surface-encoding-cleanup-v0.1
```

## Boundary

This package does not perform broad repository mutation.

It does not implement computed Scenario 09 v0.2.

It does not approve, certify, authorize, determine compliance, determine admissibility, establish legal sufficiency, decide acceptance, judge correctness, determine negligence, determine excuse, or determine execution eligibility.

## Files

```text
docs/reviewer/CATEGORIZED_ENCODING_REGRESSION_FIX_LIST_v0_1.md
encoding/encoding_cleanup_allowlist_v0_1.txt
scripts/fix_encoding_regression_allowlisted_v0_1.py
scripts/check_encoding_cleanup_allowlist_targets_v0_1.ps1
```

## Apply

```powershell
cd C:\N\fork-public-evidence

git checkout main
git pull
git checkout -b public-surface-encoding-cleanup-v0.1

Expand-Archive -Path "$env:USERPROFILE\Downloads\public_surface_encoding_cleanup_toolchain_v0_1.zip" -DestinationPath "$env:TEMP\public-surface-encoding-cleanup-toolchain-v0.1" -Force

Copy-Item -Recurse -Force "$env:TEMP\public-surface-encoding-cleanup-toolchain-v0.1\*" "C:\N\fork-public-evidence\"
```

## Validate allowlist first

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_encoding_cleanup_allowlist_targets_v0_1.ps1
```

## Dry run

```powershell
python scripts\fix_encoding_regression_allowlisted_v0_1.py --allowlist encoding\encoding_cleanup_allowlist_v0_1.txt
```

Review:

```powershell
Get-Content encoding_repair_manifest.json
Get-Content encoding_manual_review.log
```

## Write repair

Only after reviewing the dry run:

```powershell
python scripts\fix_encoding_regression_allowlisted_v0_1.py --allowlist encoding\encoding_cleanup_allowlist_v0_1.txt --write
```

## Validate cleanup

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_no_mojibake_utf8_v0_1.ps1

powershell -ExecutionPolicy Bypass -File scripts\build_ahi_viewer_data_v0_1.ps1 -ForceOverwrite
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1

powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1

git diff --check
git status -sb
```

## Commit

```powershell
git add `
  docs\reviewer\CATEGORIZED_ENCODING_REGRESSION_FIX_LIST_v0_1.md `
  encoding\encoding_cleanup_allowlist_v0_1.txt `
  scripts\fix_encoding_regression_allowlisted_v0_1.py `
  scripts\check_encoding_cleanup_allowlist_targets_v0_1.ps1 `
  encoding_manual_review.log `
  encoding_repair_manifest.json
```

Then add any repaired files shown by `git status -sb` after validation.

Use:

```powershell
git commit -m "Clean public surface encoding regressions"
```
