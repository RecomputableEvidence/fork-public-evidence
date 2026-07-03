# Encoding Cleanup Residual Patch v0.1

This package applies a surgical residual cleanup after the allowlisted repair and neutralizer pass.

## Apply

```powershell
Expand-Archive -Path "$env:USERPROFILE\Downloads\encoding_cleanup_residual_patch_v0_1.zip" -DestinationPath "$env:TEMP\encoding-cleanup-residual-v0.1" -Force

Copy-Item -Recurse -Force "$env:TEMP\encoding-cleanup-residual-v0.1\*" "C:\N\fork-public-evidence\"
```

## Run

```powershell
python scripts\patch_encoding_residuals_v0_1.py

powershell -ExecutionPolicy Bypass -File scripts\check_no_mojibake_utf8_v0_1.ps1

powershell -ExecutionPolicy Bypass -File scripts\build_ahi_viewer_data_v0_1.ps1 -ForceOverwrite
powershell -ExecutionPolicy Bypass -File scripts\build_ahi_viewer_comparison_data_v0_2.ps1 -ForceOverwrite

powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1
powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1

git diff --check
git status -sb
```
