# scripts/create_ahi_release_index_v0_1.ps1
# Creates the AHI release index and verification matrix docs.
# Run from repository root: C:\N\fork-public-evidence
#
# This script creates:
# - docs/releases/AHI_RELEASE_INDEX_v0_1.md
# - docs/releases/AHI_VERIFICATION_MATRIX_v0_1.md
# - docs/releases/AHI_SCENARIO_LADDER_v0_1.md
# - docs/releases/AHI_VIEWER_RELEASE_LADDER_v0_1.md
# - docs/releases/AHI_LOCAL_VERIFICATION_GUIDE_v0_1.md

$ErrorActionPreference = "Stop"

function Fail($Message) {
    Write-Host "FAIL: $Message" -ForegroundColor Red
    exit 1
}

function Write-Utf8NoBom {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Path,

        [Parameter(Mandatory = $true)]
        [string] $Text
    )

    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path $parent)) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText((Join-Path (Get-Location) $Path), $Text, $utf8NoBom)

    Write-Host "WROTE: $Path"
}

if (-not (Test-Path ".git")) {
    Fail "Run this script from the repository root, e.g. C:\N\fork-public-evidence"
}

$releaseDir = "docs/releases"
if (-not (Test-Path $releaseDir)) {
    New-Item -ItemType Directory -Force -Path $releaseDir | Out-Null
}

$releaseIndex = @'
# AHI Release Index v0.1

## Purpose

This index is the reviewer-facing entry point for the Fork AHI simulation proof surface.

It maps the current simulation releases, viewer releases, scenario ladder, verification matrix, and local verification commands.

## Current release state

| Surface | Latest tag | Description |
|---|---:|---|
| AHI simulation surface | `ahi-sim-v0.1.8` | Scenario 07 external authority bridge simulation |
| AHI viewer surface | `ahi-viewer-v0.1.5` | Scenario 07 external authority bridge viewer support |

## Current scenario count

```text
7
```

## Current scenario ladder

| Scenario | Title | Primary boundary/failure mode |
|---:|---|---|
| 01 | Baseline unbounded handoff | Unbounded AI-assisted handoff |
| 02 | Fork-preserved handoff | Bounded evidence preservation |
| 03 | Scope expansion attempt | Downstream scope expansion |
| 04 | Authority leakage attempt | Authority-context leakage |
| 05 | Policy-reference laundering / non-claim suppression | Policy reference treated as policy satisfaction |
| 06 | Multi-system distributed handoff | Distributed authority inheritance |
| 07 | External authority bridge | Inspectability treated as external authority |

## Release documents

- `docs/releases/AHI_RELEASE_INDEX_v0_1.md`
- `docs/releases/AHI_VERIFICATION_MATRIX_v0_1.md`
- `docs/releases/AHI_SCENARIO_LADDER_v0_1.md`
- `docs/releases/AHI_VIEWER_RELEASE_LADDER_v0_1.md`
- `docs/releases/AHI_LOCAL_VERIFICATION_GUIDE_v0_1.md`

## Primary verification commands

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1

powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism
```

Expected high-level results:

```text
PASS: ahi-sim-v0.1.x simulation proof-surface checks completed.
PASS: viewer builder is deterministic from a clean working tree
PASS: AHI viewer v0.1 hardening checks completed
```

## Non-authority boundary

Fork records and verifies bounded evidence and transition-state properties.

Fork does not approve, certify, score, authorize, determine compliance, determine admissibility, establish legal sufficiency, decide acceptance, or judge correctness.

## Reviewer route

A cold reviewer should read in this order:

1. `docs/releases/AHI_RELEASE_INDEX_v0_1.md`
2. `docs/releases/AHI_VERIFICATION_MATRIX_v0_1.md`
3. `docs/releases/AHI_SCENARIO_LADDER_v0_1.md`
4. `docs/releases/AHI_LOCAL_VERIFICATION_GUIDE_v0_1.md`
5. `docs/viewer/ahi-viewer-v0_1/README.md`
6. `docs/viewer/ahi-viewer-v0_1/index.html`

## Latest release tags

```text
ahi-sim-v0.1.8
ahi-viewer-v0.1.5
```

## Verification posture summary

The current surface demonstrates that Fork can preserve and check boundary-state records across increasingly complex governance handoffs without becoming an approval, compliance, authority, admissibility, or correctness layer.
'@

$verificationMatrix = @'
# AHI Verification Matrix v0.1

## Purpose

This matrix maps each AHI scenario to its failure mode, verification posture, artifacts, checker coverage, viewer visibility, and non-claims boundary.

## Matrix

| Scenario | Failure mode | Verification posture | Artifact family | Dedicated checker | Main checker integration | Viewer-visible | Latest sim tag | Fork verifies | Fork does not verify |
|---:|---|---|---|---|---|---|---|---|---|
| 01 | Baseline unbounded handoff | Baseline / contrast | Scenario narrative | Main simulation surface | `scripts/run_ahi_sim_v0_1_checks.ps1` | Yes | Pre-v0.1.5 surface | Shows the unbounded handoff problem space | Approval, compliance, correctness, authority, legal sufficiency |
| 02 | Preserved handoff | Artifact-backed | BDR, CBC, CCE, SMR, unsupported inheritance event, authority context, non-claims panel | Main simulation surface | `scripts/run_ahi_sim_v0_1_checks.ps1` | Yes | Pre-v0.1.5 surface | Preserved claim boundary and non-claim state | Truth, approval, compliance, authority, correctness |
| 03 | Scope expansion attempt | Artifact-backed | BDR, CBC, CCE, SMR, unsupported inheritance event, authority context, non-claims panel | Main simulation surface | `scripts/run_ahi_sim_v0_1_checks.ps1` | Yes | Pre-v0.1.5 surface | Unsupported downstream scope expansion is visible | Whether expanded claim is true, approved, compliant, or authorized |
| 04 | Authority leakage attempt | Semantically classified | BDR, CBC, CCE, SMR, unsupported inheritance event, authority context, non-claims panel | Main simulation semantic classification checks | `scripts/run_ahi_sim_v0_1_checks.ps1` | Yes | Pre-v0.1.5 surface | Authority-context leakage is bounded and explicit | Whether authority actually exists or was validly exercised |
| 05 | Policy-reference laundering / non-claim suppression | Dedicated checker integrated | BDR, CBC, CCE, SMR, suppressed limitations event, policy context, downstream memo, non-claims panels | `scripts/check_scenario_05_policy_reference_laundering_v0_1.ps1` | `scripts/run_ahi_sim_v0_1_checks.ps1` | Yes | `ahi-sim-v0.1.5` / `ahi-sim-v0.1.5-checker-integrated` | Policy reference and non-claim suppression are detected | Policy satisfaction, compliance, approval, or legal sufficiency |
| 06 | Multi-system distributed handoff | Structural + semantic invariant verification | BDR, CBC, CCE, SMR, distributed authority failure event, transition graph, non-claims panel | `scripts/check_scenario_06_multi_system_distributed_handoff_v0_1.ps1`; `scripts/check_scenario_06_semantic_invariants_v0_1.ps1` | `scripts/run_ahi_sim_v0_1_checks.ps1` | Yes | `ahi-sim-v0.1.6`; `ahi-sim-v0.1.7` | Distributed authority non-inheritance and required revalidation are preserved | Approval authority, policy satisfaction, compliance, execution eligibility, correctness |
| 07 | External authority bridge | Semantically verified | BDR, CBC, CCE, SMR, external authority failure event, external review context, transition graph, non-claims panel | `scripts/check_scenario_07_external_authority_bridge_v0_1.ps1` | `scripts/run_ahi_sim_v0_1_checks.ps1` | Yes | `ahi-sim-v0.1.8` | Unsupported external-authority inference is recorded | External admissibility, regulatory compliance, legal sufficiency, approval, customer/audit/board/insurer acceptance, execution eligibility |

## Checker coverage summary

| Checker | Scope |
|---|---|
| `scripts/run_ahi_sim_v0_1_checks.ps1` | Main simulation proof-surface checker |
| `scripts/check_ahi_viewer_v0_1.ps1` | Viewer bundle, registry alignment, posture enum, referenced paths, selected fields, unsafe JS scan, non-authority posture, deterministic builder behavior |
| `scripts/check_scenario_05_policy_reference_laundering_v0_1.ps1` | Scenario 05 policy-reference laundering and non-claim suppression |
| `scripts/check_scenario_06_multi_system_distributed_handoff_v0_1.ps1` | Scenario 06 structural distributed handoff checks |
| `scripts/check_scenario_06_semantic_invariants_v0_1.ps1` | Scenario 06 semantic invariant checks |
| `scripts/check_scenario_07_external_authority_bridge_v0_1.ps1` | Scenario 07 external authority bridge checks |

## Non-authority invariant

Across all scenarios, Fork remains an evidence-boundary and transition-state preservation surface.

Fork does not approve, certify, score, authorize, determine compliance, determine admissibility, establish legal sufficiency, decide acceptance, or judge correctness.
'@

$scenarioLadder = @'
# AHI Scenario Ladder v0.1

## Purpose

The AHI scenario ladder shows how the simulation surface progresses from a baseline unbounded handoff to increasingly explicit boundary-failure modes.

Each scenario adds one governance failure mode without allowing Fork to become an authority layer.

## Ladder

### Scenario 01 — Baseline unbounded handoff

Shows the baseline problem: AI-assisted work can move downstream without enough boundary state for later reconstruction.

Primary lesson:

```text
Without explicit boundary records, downstream reliance can inherit more than the upstream artifact actually supports.
```

### Scenario 02 — Fork-preserved handoff

Introduces artifact-backed preservation.

Artifact family:

- Boundary Delta Record
- Claim Boundary Contract
- Claim Consumption Event
- System Mapping Receipt
- Unsupported inheritance event
- Authority/policy context
- Non-claims panel

Primary lesson:

```text
Fork can preserve what crossed, what did not cross, and what must not be inferred.
```

### Scenario 03 — Scope expansion attempt

Tests downstream expansion of a bounded claim.

Primary lesson:

```text
A bounded claim cannot silently become a broader claim merely because it moved downstream.
```

### Scenario 04 — Authority leakage attempt

Tests whether authority context is improperly inherited.

Primary lesson:

```text
Authority possessed and authority exercised are not the same claim.
```

### Scenario 05 — Policy-reference laundering / non-claim suppression

Tests the failure where a policy reference is treated as policy satisfaction, or limitations disappear downstream.

Primary lesson:

```text
Citing a policy does not establish that the policy was satisfied.
```

### Scenario 06 — Multi-system distributed handoff

Tests distributed authority inheritance across multiple independently accountable systems.

Primary lesson:

```text
Individually bounded systems can still create governance failure at the transition between them.
```

Scenario 06 has two major release steps:

- `ahi-sim-v0.1.6`: structural simulation
- `ahi-sim-v0.1.7`: semantic invariant verification

### Scenario 07 — External authority bridge

Tests the external boundary where an internal Fork-preserved record is provided to an external reviewer, auditor, regulator, customer, board, insurer, legal process, or other authority-bearing context.

Primary lesson:

```text
Inspectability does not establish external admissibility, compliance, approval, legal sufficiency, acceptance, or execution eligibility.
```

## Scenario progression

```text
01: Unbounded handoff baseline
02: Boundary preservation
03: Scope expansion detection
04: Authority leakage detection
05: Policy-reference laundering / non-claim suppression
06: Distributed authority non-inheritance
07: External authority bridge non-inheritance
```

## Strategic meaning

The ladder demonstrates that Fork is not a policy engine, runtime control system, compliance oracle, approval system, or legal authority.

Fork preserves bounded evidence and transition state so later reviewers can reconstruct what was claimed, what was not claimed, what was relied on, what was unsupported, and what required revalidation.
'@

$viewerReleaseLadder = @'
# AHI Viewer Release Ladder v0.1

## Purpose

This file maps the AHI viewer release tags to their functional milestones.

The viewer is a static, repo-local evidence viewer. It does not execute workflows, call external systems, approve records, determine compliance, or certify correctness.

## Release ladder

| Tag | Milestone |
|---|---|
| `ahi-viewer-v0.1` | Static AHI Boundary Explorer scaffold |
| `ahi-viewer-v0.1.1` | Deterministic bundle generation |
| `ahi-viewer-v0.1.2` | Viewer hardening checks and schemas |
| `ahi-viewer-v0.1.3` | Scenario 06 structural bundle support |
| `ahi-viewer-v0.1.4` | Scenario 06 semantic verification posture |
| `ahi-viewer-v0.1.5` | Scenario 07 external authority bridge support |

## Current latest viewer tag

```text
ahi-viewer-v0.1.5
```

## Viewer verification command

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism
```

Expected result:

```text
PASS: viewer builder is deterministic from a clean working tree
PASS: AHI viewer v0.1 hardening checks completed
```

## Viewer invariants

The viewer checker verifies:

- required viewer files exist;
- bundle and scenario registry parse as JSON;
- bundle header is bounded and deterministic;
- scenario count matches registry;
- scenario postures are in the approved enum;
- scenario IDs and numbers are unique;
- registry scenario IDs are represented in bundle;
- referenced scenario and artifact paths exist;
- selected fields and checker coverage are present;
- viewer JavaScript avoids forbidden runtime primitives;
- non-authority posture language is present;
- prohibited oracle phrases are absent;
- deterministic builder behavior does not dirty the repository.

## Non-authority posture

The viewer is read-only and repo-local.

It does not approve, certify, score, authorize, determine compliance, determine admissibility, establish legal sufficiency, decide acceptance, or judge correctness.
'@

$localVerificationGuide = @'
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
'@

Write-Utf8NoBom "docs/releases/AHI_RELEASE_INDEX_v0_1.md" $releaseIndex
Write-Utf8NoBom "docs/releases/AHI_VERIFICATION_MATRIX_v0_1.md" $verificationMatrix
Write-Utf8NoBom "docs/releases/AHI_SCENARIO_LADDER_v0_1.md" $scenarioLadder
Write-Utf8NoBom "docs/releases/AHI_VIEWER_RELEASE_LADDER_v0_1.md" $viewerReleaseLadder
Write-Utf8NoBom "docs/releases/AHI_LOCAL_VERIFICATION_GUIDE_v0_1.md" $localVerificationGuide

Write-Host ""
Write-Host "PASS: AHI release index and verification matrix docs created."
Write-Host ""
Write-Host "Next suggested commands:"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism"
Write-Host "  git diff --check"