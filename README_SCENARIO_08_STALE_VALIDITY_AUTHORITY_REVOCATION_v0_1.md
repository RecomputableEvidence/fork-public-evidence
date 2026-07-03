# Scenario 08 — Stale Validity / Authority Revocation Boundary v0.1

## Purpose

Scenario 08 tests temporal validity and revocation state.

The failure mode is **stale validity reliance**: a claim, authority, role, policy, evidence basis, or time window was valid earlier, but later changed, expired, narrowed, or was revoked. A downstream actor then attempts to rely on the prior record as if it were still current.

## Core thesis

```text
Prior validity does not imply current validity.
```

Fork records the stale-validity / revocation boundary state. It does not decide whether the prior decision was correct, whether the new decision is allowed, or whether an external authority should accept the record.

## Adds

- `examples/simulations/governance-proof-surface/scenario_08_stale_validity_authority_revocation_boundary.md`
- `examples/simulations/governance-proof-surface/artifacts/scenario_08_boundary_delta_record.json`
- `examples/simulations/governance-proof-surface/artifacts/scenario_08_claim_boundary_contract.json`
- `examples/simulations/governance-proof-surface/artifacts/scenario_08_claim_consumption_event.json`
- `examples/simulations/governance-proof-surface/artifacts/scenario_08_system_mapping_receipt.json`
- `examples/simulations/governance-proof-surface/artifacts/scenario_08_revocation_event.json`
- `examples/simulations/governance-proof-surface/artifacts/scenario_08_validity_timeline.md`
- `examples/simulations/governance-proof-surface/artifacts/scenario_08_transition_graph.md`
- `examples/simulations/governance-proof-surface/artifacts/scenario_08_non_claims_panel.md`
- `scripts/check_scenario_08_stale_validity_authority_revocation_v0_1.ps1`
- `scripts/apply_scenario_08_stale_validity_authority_revocation_v0_1.ps1`
- `docs/releases/AHI_SIM_v0_1_9_SCENARIO_08_STALE_VALIDITY_AUTHORITY_REVOCATION.md`

## Optional Viewer v0.2 integration

If `scripts/build_ahi_viewer_comparison_data_v0_2.py` exists, the apply script patches it with a new canonical pair:

```text
Scenario 07 vs Scenario 08 — external authority bridge versus stale validity / revocation
```

Then it rebuilds:

```text
docs/viewer/ahi-viewer-v0_2/data/comparison_pairs.json
```

## Suggested branch

```powershell
git checkout main
git pull
git checkout -b scenario-08-stale-validity-revocation-v0.1
```

## Apply

```powershell
Expand-Archive -Path "$env:USERPROFILE\Downloads\scenario_08_stale_validity_authority_revocation_v0_1.zip" -DestinationPath "$env:TEMP\scenario-08-stale-validity-revocation-v0.1" -Force

Copy-Item -Recurse -Force "$env:TEMP\scenario-08-stale-validity-revocation-v0.1\*" "C:\N\fork-public-evidence\"
```

## Verify

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_scenario_08_stale_validity_authority_revocation_v0_1.ps1
powershell -ExecutionPolicy Bypass -File scripts\apply_scenario_08_stale_validity_authority_revocation_v0_1.ps1
powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1
```

After commit:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1 -CheckDeterminism
```
