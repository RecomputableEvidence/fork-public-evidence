# Computed Proof Surface v0.1

## Purpose

This package adds a reviewer-facing consolidation layer for Fork's AHI proof surface.

It explains, in one bounded artifact set, what is fixture-declared, what is computed, what is reconstructed, what is preserved, and what Fork intentionally refuses to conclude.

This is a consolidation step after:

```text
public-surface-cleanup-computed-s09-plan-v0.1
public-surface-encoding-cleanup-v0.1
computed-scenario-09-revocation-split-state-v0.1
```

## Boundary

Computed Proof Surface v0.1 does not add runtime control, approval logic, legal determination, compliance determination, truth certification, safety certification, fault allocation, or execution eligibility.

It records a bounded reviewer map of the current public evidence surface.

## Files

```text
README_COMPUTED_PROOF_SURFACE_v0_1.md
docs/reviewer/COMPUTED_PROOF_SURFACE_v0_1.md
docs/reviewer/COMPUTED_PROOF_SURFACE_REVIEW_NOTE_v0_1.md
examples/simulations/governance-proof-surface/computed_proof_surface/README.md
examples/simulations/governance-proof-surface/computed_proof_surface/computed_proof_surface_manifest_v0_1.json
scripts/check_computed_proof_surface_v0_1.ps1
```

## Apply

```powershell
cd C:\N\fork-public-evidence

git checkout main
git pull
git checkout -b computed-proof-surface-v0.1

Expand-Archive -Path "$env:USERPROFILE\Downloads\computed_proof_surface_v0_1.zip" -DestinationPath "$env:TEMP\computed-proof-surface-v0.1" -Force

Copy-Item -Recurse -Force "$env:TEMP\computed-proof-surface-v0.1\*" "C:\N\fork-public-evidence\"
```

## Validate

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_computed_proof_surface_v0_1.ps1

powershell -ExecutionPolicy Bypass -File scripts\check_computed_scenario_09_revocation_split_state_v0_1.ps1
powershell -ExecutionPolicy Bypass -File scripts\check_no_mojibake_utf8_v0_1.ps1
powershell -ExecutionPolicy Bypass -File scripts\check_public_surface_cleanup_and_computed_s09_plan_v0_1.ps1
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1
powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1

git diff --check
git status -sb
```

## Commit

```powershell
git add `
  README_COMPUTED_PROOF_SURFACE_v0_1.md `
  docs\reviewer\COMPUTED_PROOF_SURFACE_v0_1.md `
  docs\reviewer\COMPUTED_PROOF_SURFACE_REVIEW_NOTE_v0_1.md `
  examples\simulations\governance-proof-surface\computed_proof_surface `
  scripts\check_computed_proof_surface_v0_1.ps1

git commit -m "Add Computed Proof Surface v0.1"
git push -u origin computed-proof-surface-v0.1
```
