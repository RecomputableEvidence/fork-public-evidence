# Computed Scenario 09 Revocation Split-State v0.1

## Purpose

This package implements a computed Scenario 09 derivation path.

It moves Scenario 09 from a fixture-declared split-state record toward a deterministic derivation over independent System A, System B, and System C state inputs.

## Boundary

This package does not determine fault allocation, fault, excuse, acceptance, legal sufficiency, compliance status, authority status, correctness, safety, or execution eligibility.

It computes whether the provided fixture states exhibit a revocation visibility gap, a split-state consumption gap, or a closed/revalidated state under the supplied fixture policy.

## Files

```text
README_COMPUTED_SCENARIO_09_REVOCATION_SPLIT_STATE_v0_1.md
docs/reviewer/AHI_COMPUTED_SCENARIO_09_REVOCATION_SPLIT_STATE_v0_1.md
examples/simulations/governance-proof-surface/computed_scenario_09/README.md
examples/simulations/governance-proof-surface/computed_scenario_09/cases/visibility_gap_detected/*.json
examples/simulations/governance-proof-surface/computed_scenario_09/cases/gap_closed_by_revalidation/*.json
scripts/derive_computed_scenario_09_revocation_split_state_v0_1.py
scripts/check_computed_scenario_09_revocation_split_state_v0_1.ps1
```

## Apply

```powershell
cd C:\N\fork-public-evidence

git checkout main
git pull
git checkout -b computed-scenario-09-revocation-split-state-v0.1

Expand-Archive -Path "$env:USERPROFILE\Downloads\computed_scenario_09_revocation_split_state_v0_1.zip" -DestinationPath "$env:TEMP\computed-scenario-09-v0.1" -Force

Copy-Item -Recurse -Force "$env:TEMP\computed-scenario-09-v0.1\*" "C:\N\fork-public-evidence\"
```

## Validate

```powershell
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
  README_COMPUTED_SCENARIO_09_REVOCATION_SPLIT_STATE_v0_1.md `
  docs\reviewer\AHI_COMPUTED_SCENARIO_09_REVOCATION_SPLIT_STATE_v0_1.md `
  examples\simulations\governance-proof-surface\computed_scenario_09 `
  scripts\derive_computed_scenario_09_revocation_split_state_v0_1.py `
  scripts\check_computed_scenario_09_revocation_split_state_v0_1.ps1

git commit -m "Add computed Scenario 09 revocation split-state derivation"
git push -u origin computed-scenario-09-revocation-split-state-v0.1
```
