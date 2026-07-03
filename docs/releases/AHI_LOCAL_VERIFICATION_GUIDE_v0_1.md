# AHI Local Verification Guide v0.1

## Purpose

This guide gives a reviewer the local commands needed to verify the AHI simulation and viewer proof surface.

Run all commands from repository root:

```powershell
cd C:\N\fork-public-evidence
```

## 1. Confirm clean state

```powershell
git status -sb
git log --oneline --decorate -8
git tag --points-at HEAD
```

Expected current tags at latest release:

```text
ahi-sim-v0.1.8
ahi-viewer-v0.1.5
```

## 2. Run main AHI simulation checks

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1
```

Expected high-level ending:

```text
PASS: Scenario 06 semantic invariant validation completed inside main AHI checker.
PASS: Scenario 07 validation completed inside main AHI checker.
PASS: ahi-sim-v0.1.x simulation proof-surface checks completed.
```

## 3. Run viewer hardening and determinism checks

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism
```

Expected high-level ending:

```text
PASS: viewer builder is deterministic from a clean working tree
PASS: AHI viewer v0.1 hardening checks completed
```

## 4. Run dedicated Scenario 06 checks

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_scenario_06_multi_system_distributed_handoff_v0_1.ps1

powershell -ExecutionPolicy Bypass -File scripts\check_scenario_06_semantic_invariants_v0_1.ps1
```

Expected endings:

```text
PASS: Scenario 06 multi-system distributed handoff checks completed
PASS: Scenario 06 semantic invariants verified
```

## 5. Run dedicated Scenario 07 checks

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_scenario_07_external_authority_bridge_v0_1.ps1
```

Expected ending:

```text
PASS: Scenario 07 external authority bridge checks completed
```

## 6. Check whitespace and line endings

```powershell
git diff --check
```

Expected: no output.

## 7. Check clean repository state after deterministic viewer rebuild

```powershell
git status -sb
```

Expected:

```text
## main...origin/main
```

## Full verification block

```powershell
cd C:\N\fork-public-evidence

git status -sb

powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1

powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism

powershell -ExecutionPolicy Bypass -File scripts\check_scenario_06_multi_system_distributed_handoff_v0_1.ps1

powershell -ExecutionPolicy Bypass -File scripts\check_scenario_06_semantic_invariants_v0_1.ps1

powershell -ExecutionPolicy Bypass -File scripts\check_scenario_07_external_authority_bridge_v0_1.ps1

git diff --check

git status -sb

git tag --points-at HEAD
```

## Interpretation boundary

Passing these commands means the local proof surface structurally and semantically verifies the bounded AHI scenario records according to the included checkers.

Passing these commands does not mean Fork approves, certifies, scores, authorizes, determines compliance, determines admissibility, establishes legal sufficiency, decides acceptance, or judges correctness.