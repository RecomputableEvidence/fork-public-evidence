<#
.SYNOPSIS
Initialize ESAL v0.1 layout in the existing fork-public-evidence repository
using the existing 'esal-tests' folder as the test corpus root.

.DESCRIPTION
- Creates (if missing):
    spec/
      BDR-ESAL-v0.1.md
      conformance.json
    reference/esal/
      __init__.py
      models.py
      errors.py
      validator.py
      canonicalization.py
      reducer.py
      fingerprint.py
      taxonomy.py
      runner.py
      report.py
    esal-tests/
      canonical/
      adversarial/
      malformed/
      expected/

- Commits the new layout on the specified branch and pushes to GitHub.

- Assumes:
    - You are in an existing clone of
        RecomputableEvidence/fork-public-evidence
    - git is installed and configured
#>

param(
    [Parameter(Mandatory = $false)]
    [string] $Branch = "boundary-delta-record-v0.1"
)

Write-Host "== ESAL v0.1 Layout Initializer (esal-tests) =="

# --- 1. Verify we are in a git repo root ---

if (-not (Test-Path ".git")) {
    Write-Error "This script must be run from the fork-public-evidence repository root (where .git exists)."
    exit 1
}

$repoName = Split-Path (Get-Location) -Leaf
Write-Host "Repository root detected: $repoName"

# --- 2. Ensure branch exists / checkout ---

$currentBranch = (git rev-parse --abbrev-ref HEAD).Trim()

if ($currentBranch -ne $Branch) {
    Write-Host "Current branch: '$currentBranch'"
    Write-Host "Target ESAL branch: '$Branch'"

    $branchExists = git branch --list $Branch
    if ($branchExists) {
        Write-Host "Checking out existing branch '$Branch' ..."
        git checkout $Branch
    } else {
        Write-Host "Creating and checking out new branch '$Branch' from '$currentBranch' ..."
        git checkout -b $Branch
    }

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to checkout/create branch '$Branch'."
        exit 1
    }
} else {
    Write-Host "Already on target branch '$Branch'."
}

$currentBranch = (git rev-parse --abbrev-ref HEAD).Trim()
Write-Host "Working on branch: $currentBranch"

# --- 3. Create ESAL folders (spec, reference, esal-tests) ---

$pathsToCreate = @(
    "spec",
    "reference",
    "reference\esal",
    "esal-tests",
    "esal-tests\canonical",
    "esal-tests\adversarial",
    "esal-tests\malformed",
    "esal-tests\expected",
    "tools"
)

foreach ($p in $pathsToCreate) {
    if (-not (Test-Path $p)) {
        Write-Host "Creating folder: $p"
        New-Item -ItemType Directory -Path $p | Out-Null
    } else {
        Write-Host "Folder already exists: $p"
    }
}

# --- 4. Create spec files with starter content ---

$specFile        = "spec\BDR-ESAL-v0.1.md"
$conformanceFile = "spec\conformance.json"

if (-not (Test-Path $specFile)) {
    Write-Host "Creating $specFile ..."
@"
# Boundary Delta Record (BDR) / ESAL v0.1 — Formal Specification

Status: Draft — Experimental
Attribution: Fork: Recomputable Evidence for AI-Assisted Workflows
Repository: RecomputableEvidence/fork-public-evidence
Branch: $currentBranch

This document defines:
- ESAL system model (E, C, F, H, S₀)
- BDR data model and authority containment
- Constraint model and evaluation semantics
- Canonicalization function C
- Reduction function F
- Fingerprint function H
- ETI-1 / RDC-1 conformance conditions
- Failure taxonomy (S / G / D / A)

(Full spec text to be inserted here.)
"@ | Set-Content $specFile -Encoding UTF8
} else {
    Write-Host "$specFile already exists; not overwriting."
}

if (-not (Test-Path $conformanceFile)) {
    Write-Host "Creating $conformanceFile ..."
@"
{
  "protocol": "BDR-ESAL",
  "version": "0.1",
  "implementation": "reference-oracle",
  "semantics": {
    "canonicalization": "C",
    "reduction": "F",
    "fingerprint": "H"
  },
  "serialization": {
    "format": "canonical-json",
    "hash": "sha256"
  },
  "excluded_capabilities": [
    "external_state",
    "network_access",
    "runtime_policy_resolution",
    "human_review"
  ]
}
"@ | Set-Content $conformanceFile -Encoding UTF8
} else {
    Write-Host "$conformanceFile already exists; not overwriting."
}

# --- 5. Create reference oracle skeleton files ---

$esalFiles = @{
    "__init__.py"       = "# ESAL v0.1 reference oracle package";
    "models.py"         = @"
from dataclasses import dataclass
from typing import FrozenSet, Tuple


@dataclass(frozen=True)
class ViolationRecord:
    constraint_id: str
    event_id: str
    boundary_id: str
    severity: str
    timestamp: int


@dataclass(frozen=True)
class State:
    authority: FrozenSet[str]
    constraints: FrozenSet[str]
    obligations: FrozenSet[str]
    lineage: Tuple[str, ...]
    validity: bool
    violations: Tuple[ViolationRecord, ...]


INITIAL_STATE = State(
    authority=frozenset(),
    constraints=frozenset(),
    obligations=frozenset(),
    lineage=tuple(),
    validity=True,
    violations=tuple(),
)
"@;
    "errors.py"         = @"
class ESALViolation(Exception):
    classification: str | None = None


class StructuralError(ESALViolation):
    classification = "S"


class GovernanceError(ESALViolation):
    classification = "G"


class DeterminismError(ESALViolation):
    classification = "D"
"@;
    "validator.py"      = "# TODO: implement schema and lineage validation for events and BDRs.";
    "canonicalization.py" = "# TODO: implement C(E) canonicalization (normalize + deterministic sort).";
    "reducer.py"        = "# TODO: implement F(S₀, E*) = fold(transition, S₀, E*).";
    "fingerprint.py"    = "# TODO: implement H(S) using canonical JSON + SHA-256.";
    "taxonomy.py"       = "# TODO: implement S/G/D/A classification based on ESALViolation and state.";
    "runner.py"         = "# TODO: wire validator, canonicalization, reducer, fingerprint into replay().";
    "report.py"         = "# TODO: generate JSON and human-readable reports for ETI-1/RDC-1."
}

foreach ($name in $esalFiles.Keys) {
    $path = Join-Path "reference\esal" $name
    if (-not (Test-Path $path)) {
        Write-Host "Creating $path ..."
        $esalFiles[$name] | Set-Content $path -Encoding UTF8
    } else {
        Write-Host "$path already exists; not overwriting."
    }
}

# --- 6. Create minimal esal-tests placeholder files ---

$sampleCanonical = "esal-tests\canonical\C-001-placeholder.jsonl"
if (-not (Test-Path $sampleCanonical)) {
    Write-Host "Creating placeholder canonical log at $sampleCanonical ..."
@"
// TODO: add canonical ESAL event log for C-001 once reference oracle is implemented.
"@ | Set-Content $sampleCanonical -Encoding UTF8
}

# --- 7. Stage, commit, and push to GitHub ---

Write-Host "Staging ESAL files for commit ..."
git add spec reference\esal esal-tests tools\Init-EsalLayout.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Error "git add failed."
    exit 1
}

$commitMessage = "Initialize ESAL v0.1 spec, reference oracle skeleton, and esal-tests layout"
Write-Host "Committing with message: $commitMessage"
git commit -m "$commitMessage"

if ($LASTEXITCODE -ne 0) {
    Write-Error "git commit failed. Resolve any issues and commit manually."
    exit 1
}

Write-Host "Pushing branch '$currentBranch' to origin ..."
git push -u origin $currentBranch

if ($LASTEXITCODE -ne 0) {
    Write-Error "git push failed. Check your Git remote and authentication."
    exit 1
}

Write-Host ""
Write-Host "ESAL v0.1 layout initialized and pushed to branch '$currentBranch'."
Write-Host "Next steps:"
Write-Host "  - Implement canonicalization.py, reducer.py, fingerprint.py, etc. in reference/esal."
Write-Host "  - Populate esal-tests/ with real canonical/adversarial/malformed logs."
Write-Host "  - Use your release script to create a GitHub release for independent verification."