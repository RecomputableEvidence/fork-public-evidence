# AHI Local Verification Guide v0.2

## Purpose

This guide gives a clean local verification sequence for the current AHI proof-surface endpoint.

## Preconditions

Run from repository root:

```powershell
cd C:\N\fork-public-evidence
```

Confirm branch and clean state:

```powershell
git status -sb
```

Expected after release:

```text
## main...origin/main
```

## Verify Scenario 08

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_scenario_08_stale_validity_authority_revocation_v0_1.ps1
```

Expected ending:

```text
PASS: Scenario 08 stale validity / authority revocation checks completed
```

## Verify full AHI simulation surface

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1
```

Expected ending:

```text
PASS: Scenario 08 validation completed inside main AHI checker.
PASS: ahi-sim-v0.1.x simulation proof-surface checks completed.
```

## Verify Viewer v0.1

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism
```

Expected ending:

```text
Scenario count: 8
PASS: viewer builder is deterministic from a clean working tree
PASS: AHI viewer v0.1 hardening checks completed
```

## Verify Viewer v0.2

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1 -CheckDeterminism
```

Expected ending:

```text
PASS: AHI viewer v0.2 comparison data built.
PASS: viewer v0.2 comparison builder is deterministic from a clean working tree
PASS: AHI viewer v0.2 comparison mode checks completed
```

## Verify whitespace and repository state

```powershell
git diff --check
git status -sb
```

Expected:

```text
git diff --check
# no output

git status -sb
## main...origin/main
```

## Verify remote release tags

```powershell
git ls-remote --tags origin ahi-sim-v0.1.9
git ls-remote --tags origin ahi-viewer-v0.1.6
git ls-remote --tags origin ahi-viewer-v0.2.1
```

Each command should return a remote tag object.

For peeled annotated-tag commit confirmation:

```powershell
git ls-remote --tags origin "ahi-sim-v0.1.9^{}"
git ls-remote --tags origin "ahi-viewer-v0.1.6^{}"
git ls-remote --tags origin "ahi-viewer-v0.2.1^{}"
```

Expected underlying commit:

```text
64317c3
```

## Interpretation

These checks verify local structural, semantic, bundle, and deterministic generation behavior.

They do not establish external admissibility, compliance, legal sufficiency, truth, approval, certification, acceptance, current authority, or execution eligibility.
