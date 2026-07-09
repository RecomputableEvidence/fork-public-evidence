# scripts/add_boundary_pressure_retrieval_distortion_v0_1.ps1
# Adds Boundary Pressure Review / Retrieval Distortion Test Case v0.1.
# PowerShell 5.1 compatible. Writes UTF-8 without BOM and LF line endings.

param(
    [switch]$Commit,
    [switch]$Push
)

$ErrorActionPreference = "Stop"

$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Read-Utf8 {
    param([Parameter(Mandatory = $true)][string]$Path)
    return [System.IO.File]::ReadAllText((Resolve-Path $Path).Path, $Utf8NoBom)
}

function Write-Utf8Lf {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )

    $full = [System.IO.Path]::GetFullPath($Path)
    $dir = Split-Path -Parent $full

    if ($dir -and -not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }

    $normalized = $Content -replace "`r`n", "`n"
    [System.IO.File]::WriteAllText($full, $normalized, $Utf8NoBom)
}

function Add-RoutingBlock {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$BlockId,
        [Parameter(Mandatory = $true)][string]$Content
    )

    if (-not (Test-Path $Path)) {
        Write-Host "Skipping missing routing target: $Path"
        return
    }

    $start = "<!-- $BlockId`:START -->"
    $end = "<!-- $BlockId`:END -->"

    $existing = Read-Utf8 -Path $Path

    if ($existing -match [regex]::Escape($start)) {
        Write-Host "Routing block already present in $Path"
        return
    }

    $block = @"

$start

$Content

$end
"@

    $updated = $existing.TrimEnd() + "`n" + $block + "`n"
    Write-Utf8Lf -Path $Path -Content $updated
    Write-Host "Updated routing target: $Path"
}

$repoRoot = Get-Location
Write-Host "Repo root: $repoRoot"

$caseDir      = "docs/review/boundary-pressure"
$fixturesDir  = "$caseDir/fixtures"
$validDir     = "$fixturesDir/valid"
$invalidDir   = "$fixturesDir/invalid"
$schemaDir    = "schemas"
$toolsDir     = "tools"

New-Item -ItemType Directory -Force -Path $caseDir     | Out-Null
New-Item -ItemType Directory -Force -Path $validDir    | Out-Null
New-Item -ItemType Directory -Force -Path $invalidDir  | Out-Null
New-Item -ItemType Directory -Force -Path $schemaDir   | Out-Null
New-Item -ItemType Directory -Force -Path $toolsDir    | Out-Null

$docPath           = "$caseDir/BOUNDARY_PRESSURE_RETRIEVAL_DISTORTION_TEST_CASE_v0_1.md"
$schemaPath        = "$schemaDir/boundary_pressure_review_case_v0_1.schema.json"
$checkerPath       = "$toolsDir/check_boundary_pressure_review_cases_v0_1.py"
$validFixturePath  = "$validDir/BPR_RD_VALID_001_access_limitation_preserved_v0_1.json"
$invalidFixturePath= "$invalidDir/BPR_RD_INVALID_001_failed_retrieval_treated_as_review_v0_1.json"

$doc = @'
# Boundary Pressure Review / Retrieval Distortion Test Case v0.1

Status: Experimental review case.
Normative force: Maintainer guidance and reviewer test fixture, not external certification.
Scope: Boundary Pressure Review, retrieval distortion, failed access, partial access, exterior observation, and recomputation interpretation.
Access classification: Public repository review artifact.
Related posture: `docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md`.

## Non-endorsement and non-claims capsule

This artifact does not endorse Fork, certify Fork, validate production readiness, establish legal sufficiency, establish compliance, approve deployment, or convert any exterior observation into endorsement.

This artifact tests a review failure mode: a reviewer, model, downstream reader, or external observer may treat failed retrieval, partial retrieval, inferred access, or surrounding commentary as if it were direct inspection, recomputation, structural verification, approval, or validation.

## Purpose

Boundary Pressure Review evaluates whether Fork artifacts preserve declared claim, authority, evidence, non-claim, sufficiency, and truth boundaries under adverse interpretation.

This test case focuses on retrieval distortion.

Retrieval distortion occurs when a review channel silently changes what the reviewer thinks was accessed, observed, executed, or recomputed.

The important failure is not that retrieval failed. Failed retrieval is an ordinary access condition. The failure occurs when failed or partial retrieval is upgraded into a content review, structural reproduction, endorsement, validation, approval, compliance conclusion, legal conclusion, or evidence sufficiency conclusion.

## Test question

Can a Fork review artifact preserve the difference between:

1. raw artifact access;
2. partial access;
3. failed retrieval;
4. inferred commentary;
5. structural reproduction;
6. unresolved state;
7. evidentiary sufficiency;
8. authority;
9. approval;
10. endorsement?

A passing artifact keeps those states separate.

## Review standard exercised

A Fork artifact should not allow any of the following collapses:

- failed retrieval becomes review;
- partial access becomes complete access;
- commentary becomes execution;
- observation becomes endorsement;
- recomputation becomes validation;
- structural pass becomes truth;
- artifact inclusion becomes sufficiency;
- authority context becomes authority transfer;
- external receipt becomes certification.

## Fixture model

The fixtures use a small JSON case format.

Each fixture declares:

- `case_id`;
- `expected_result`;
- `source_access`;
- `claims`;
- `non_claims`;
- `boundary_pressure`;
- `interpretation`.

The checker validates whether the expected result aligns with the declared conditions.

## Valid fixture

The valid fixture records partial access and preserves it as an access limitation.

It does not claim structural reproduction, content review, approval, compliance, legal sufficiency, or truth.

Expected result:

`STRUCTURAL_PASS`

## Invalid fixture

The invalid fixture records no raw access but claims review completion and structural reproduction.

That is the retrieval distortion failure.

Expected result:

`STRUCTURAL_FAIL`

## Checker

Run from repo root:

```powershell
python .\tools\check_boundary_pressure_review_cases_v0_1.py
```

Expected output:

- valid fixture passes;
- invalid fixture fails for the expected reason;
- checker exits 0 when all fixture expectations are matched.

## Interpretation of checker pass

A checker pass means only that the included retrieval-distortion fixtures behaved as expected under the structural rules in the checker.
It does not establish truth, legal sufficiency, compliance, approval, endorsement, production readiness, audit sufficiency, or general completeness of the Boundary Pressure Review method.

## Future expansion

Future versions may add fixtures for:

- semantic paraphrase bypass;
- non-claim suppression;
- hostile endorsement injection;
- observation-volume-as-consensus;
- packet-inclusion-as-sufficiency;
- policy-reference-as-compliance;
- authority-context-as-transfer;
- commercial-language-overclaim;
- recomputation-receipt-overread.
'@

$schema = @'
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://recomputableevidence.example/schemas/boundary_pressure_review_case_v0_1.schema.json",
  "title": "Boundary Pressure Review Case v0.1",
  "type": "object",
  "required": [
    "case_id",
    "case_version",
    "expected_result",
    "source_access",
    "claims",
    "non_claims",
    "boundary_pressure",
    "interpretation"
  ],
  "properties": {
    "case_id": {
      "type": "string"
    },
    "case_version": {
      "const": "v0.1"
    },
    "expected_result": {
      "enum": [
        "STRUCTURAL_PASS",
        "STRUCTURAL_FAIL"
      ]
    },
    "source_access": {
      "type": "object",
      "required": [
        "status",
        "raw_artifacts_accessed",
        "execution_performed",
        "access_limitation_recorded"
      ],
      "properties": {
        "status": {
          "enum": [
            "NO_ACCESS",
            "PARTIAL_ACCESS",
            "RAW_ACCESS",
            "EXECUTED"
          ]
        },
        "raw_artifacts_accessed": {
          "type": "boolean"
        },
        "execution_performed": {
          "type": "boolean"
        },
        "access_limitation_recorded": {
          "type": "boolean"
        },
        "notes": {
          "type": "string"
        }
      },
      "additionalProperties": true
    },
    "claims": {
      "type": "object",
      "required": [
        "content_review_completed",
        "structural_reproduction_completed",
        "approval_claimed",
        "compliance_claimed",
        "legal_sufficiency_claimed",
        "truth_claimed"
      ],
      "properties": {
        "content_review_completed": {
          "type": "boolean"
        },
        "structural_reproduction_completed": {
          "type": "boolean"
        },
        "approval_claimed": {
          "type": "boolean"
        },
        "compliance_claimed": {
          "type": "boolean"
        },
        "legal_sufficiency_claimed": {
          "type": "boolean"
        },
        "truth_claimed": {
          "type": "boolean"
        },
        "asserted_meaning": {
          "type": "string"
        }
      },
      "additionalProperties": true
    },
    "non_claims": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "boundary_pressure": {
      "type": "object",
      "required": [
        "pressure_type",
        "prohibited_collapses"
      ],
      "properties": {
        "pressure_type": {
          "const": "RETRIEVAL_DISTORTION"
        },
        "prohibited_collapses": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      },
      "additionalProperties": true
    },
    "interpretation": {
      "type": "object",
      "required": [
        "observation_status",
        "permitted_use",
        "prohibited_use"
      ],
      "properties": {
        "observation_status": {
          "enum": [
            "ACCESS_LIMITATION_RECORDED",
            "RAW_ACCESS_RECORDED",
            "EXECUTION_RECORDED",
            "REVIEW_COMPLETED",
            "UNRESOLVED"
          ]
        },
        "permitted_use": {
          "type": "string"
        },
        "prohibited_use": {
          "type": "string"
        }
      },
      "additionalProperties": true
    }
  },
  "additionalProperties": true
}
'@

$validFixture = @'
{
  "case_id": "BPR-RD-VALID-001",
  "case_version": "v0.1",
  "expected_result": "STRUCTURAL_PASS",
  "source_access": {
    "status": "PARTIAL_ACCESS",
    "raw_artifacts_accessed": false,
    "execution_performed": false,
    "access_limitation_recorded": true,
    "notes": "Reviewer had partial access and preserved the limitation rather than claiming full review or recomputation."
  },
  "claims": {
    "content_review_completed": false,
    "structural_reproduction_completed": false,
    "approval_claimed": false,
    "compliance_claimed": false,
    "legal_sufficiency_claimed": false,
    "truth_claimed": false,
    "asserted_meaning": "Partial access was recorded as an access limitation. No content review, execution, recomputation, approval, compliance, legal sufficiency, or truth conclusion is claimed."
  },
  "non_claims": [
    "does_not_establish_truth",
    "does_not_establish_approval",
    "does_not_establish_compliance",
    "does_not_establish_legal_sufficiency",
    "does_not_establish_production_readiness",
    "does_not_convert_observation_into_endorsement",
    "does_not_convert_failed_retrieval_into_review"
  ],
  "boundary_pressure": {
    "pressure_type": "RETRIEVAL_DISTORTION",
    "prohibited_collapses": [
      "failed_retrieval_to_review",
      "partial_access_to_complete_access",
      "observation_to_endorsement",
      "commentary_to_execution",
      "structural_pass_to_truth",
      "recomputation_to_validation"
    ]
  },
  "interpretation": {
    "observation_status": "ACCESS_LIMITATION_RECORDED",
    "permitted_use": "May be cited only as evidence that partial access was encountered and preserved as unresolved access state.",
    "prohibited_use": "Must not be cited as content review, structural reproduction, endorsement, approval, compliance, legal sufficiency, truth, or production readiness."
  }
}
'@

$invalidFixture = @'
{
  "case_id": "BPR-RD-INVALID-001",
  "case_version": "v0.1",
  "expected_result": "STRUCTURAL_FAIL",
  "source_access": {
    "status": "NO_ACCESS",
    "raw_artifacts_accessed": false,
    "execution_performed": false,
    "access_limitation_recorded": false,
    "notes": "Reviewer could not access the raw artifacts but the case claims review completion anyway."
  },
  "claims": {
    "content_review_completed": true,
    "structural_reproduction_completed": true,
    "approval_claimed": true,
    "compliance_claimed": false,
    "legal_sufficiency_claimed": false,
    "truth_claimed": false,
    "asserted_meaning": "Review completed. Structural reproduction confirmed. The artifact is approved based on the available commentary."
  },
  "non_claims": [],
  "boundary_pressure": {
    "pressure_type": "RETRIEVAL_DISTORTION",
    "prohibited_collapses": [
      "failed_retrieval_to_review",
      "observation_to_endorsement"
    ]
  },
  "interpretation": {
    "observation_status": "REVIEW_COMPLETED",
    "permitted_use": "May be cited as completed review.",
    "prohibited_use": "No limitations recorded."
  }
}
'@

$checker = @'
#!/usr/bin/env python3
"""
Boundary Pressure Review Case Checker v0.1

This checker validates the retrieval-distortion fixtures included in Fork.
A checker pass means only that the included fixtures behaved as expected
under the structural rules below. It does not establish truth, approval,
legal sufficiency, compliance, production readiness, endorsement, audit
sufficiency, or external certification.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "docs" / "review" / "boundary-pressure" / "fixtures"

REQUIRED_NON_CLAIMS = {
    "does_not_establish_truth",
    "does_not_establish_approval",
    "does_not_establish_compliance",
    "does_not_establish_legal_sufficiency",
    "does_not_establish_production_readiness",
    "does_not_convert_observation_into_endorsement",
    "does_not_convert_failed_retrieval_into_review",
}

PROHIBITED_COLLAPSES = {
    "failed_retrieval_to_review",
    "partial_access_to_complete_access",
    "observation_to_endorsement",
    "commentary_to_execution",
    "structural_pass_to_truth",
    "recomputation_to_validation",
}


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require(condition: bool, code: str, errors: List[str]) -> None:
    if not condition:
        errors.append(code)


def evaluate_case(case: Dict[str, Any]) -> List[str]:
    errors: List[str] = []

    for key in [
        "case_id",
        "case_version",
        "expected_result",
        "source_access",
        "claims",
        "non_claims",
        "boundary_pressure",
        "interpretation",
    ]:
        require(key in case, f"MISSING_REQUIRED_FIELD:{key}", errors)

    if errors:
        return errors

    source_access = case.get("source_access", {})
    claims = case.get("claims", {})
    non_claims = set(case.get("non_claims", []))
    boundary_pressure = case.get("boundary_pressure", {})
    interpretation = case.get("interpretation", {})

    access_status = source_access.get("status")
    raw_access = bool(source_access.get("raw_artifacts_accessed"))
    executed = bool(source_access.get("execution_performed"))
    limitation_recorded = bool(source_access.get("access_limitation_recorded"))

    content_review = bool(claims.get("content_review_completed"))
    structural_reproduction = bool(claims.get("structural_reproduction_completed"))

    authority_claims = [
        "approval_claimed",
        "compliance_claimed",
        "legal_sufficiency_claimed",
        "truth_claimed",
    ]

    no_or_partial_access = access_status in {"NO_ACCESS", "PARTIAL_ACCESS"}

    require(
        case.get("case_version") == "v0.1",
        "UNSUPPORTED_CASE_VERSION",
        errors,
    )

    require(
        case.get("expected_result") in {"STRUCTURAL_PASS", "STRUCTURAL_FAIL"},
        "INVALID_EXPECTED_RESULT",
        errors,
    )

    require(
        boundary_pressure.get("pressure_type") == "RETRIEVAL_DISTORTION",
        "INVALID_PRESSURE_TYPE",
        errors,
    )

    if no_or_partial_access:
        require(
            limitation_recorded,
            "ACCESS_LIMITATION_NOT_RECORDED",
            errors,
        )

        require(
            interpretation.get("observation_status") == "ACCESS_LIMITATION_RECORDED",
            "FAILED_OR_PARTIAL_ACCESS_NOT_PRESERVED_AS_LIMITATION",
            errors,
        )

        require(
            not content_review,
            "RETRIEVAL_DISTORTION_CONTENT_REVIEW_CLAIMED_WITHOUT_RAW_ACCESS",
            errors,
        )

        require(
            not structural_reproduction,
            "RETRIEVAL_DISTORTION_REPRODUCTION_CLAIMED_WITHOUT_EXECUTION",
            errors,
        )

    if access_status == "RAW_ACCESS":
        require(raw_access, "RAW_ACCESS_STATUS_WITHOUT_RAW_ACCESS_FLAG", errors)

    if access_status == "EXECUTED":
        require(
            raw_access and executed,
            "EXECUTED_STATUS_WITHOUT_RAW_ACCESS_AND_EXECUTION_FLAGS",
            errors,
        )

    for authority_claim in authority_claims:
        require(
            not bool(claims.get(authority_claim)),
            f"AUTHORITY_OR_SUFFICIENCY_CLAIM_FORBIDDEN:{authority_claim}",
            errors,
        )

    missing_non_claims = sorted(REQUIRED_NON_CLAIMS - non_claims)
    for missing in missing_non_claims:
        errors.append(f"MISSING_REQUIRED_NON_CLAIM:{missing}")

    observed_collapses = set(boundary_pressure.get("prohibited_collapses", []))
    require(
        bool(observed_collapses & PROHIBITED_COLLAPSES),
        "NO_RECOGNIZED_BOUNDARY_PRESSURE_COLLAPSE_DECLARED",
        errors,
    )

    asserted_meaning = str(claims.get("asserted_meaning", "")).lower()
    high_risk_terms = [
        "approved",
        "certified",
        "validated",
        "compliant",
        "legally sufficient",
        "production ready",
    ]

    for term in high_risk_terms:
        if term in asserted_meaning:
            errors.append(f"HIGH_RISK_ASSERTED_MEANING_TERM:{term}")

    return errors


def main() -> int:
    if not FIXTURE_ROOT.exists():
        print(f"Missing fixture directory: {FIXTURE_ROOT}", file=sys.stderr)
        return 2

    paths = sorted(FIXTURE_ROOT.rglob("*.json"))

    if not paths:
        print(f"No fixtures found under: {FIXTURE_ROOT}", file=sys.stderr)
        return 2

    unexpected: List[str] = []

    print("Boundary Pressure Review Case Checker v0.1")
    print(f"Fixture root: {FIXTURE_ROOT}")
    print("")

    for path in paths:
        case = load_json(path)
        expected = case.get("expected_result")
        errors = evaluate_case(case)
        actual = "STRUCTURAL_FAIL" if errors else "STRUCTURAL_PASS"

        expectation_matched = expected == actual

        rel = path.relative_to(ROOT)
        print(f"{rel}")
        print(f"  case_id: {case.get('case_id')}")
        print(f"  expected: {expected}")
        print(f"  actual:   {actual}")

        if errors:
            for error in errors:
                print(f"  error:    {error}")

        if expectation_matched:
            print("  result:   EXPECTATION_MATCHED")
        else:
            print("  result:   EXPECTATION_MISMATCH")
            unexpected.append(str(rel))

        print("")

    if unexpected:
        print("Unexpected fixture results:", file=sys.stderr)
        for rel in unexpected:
            print(f"  - {rel}", file=sys.stderr)
        return 1

    print("All boundary pressure fixture expectations matched.")
    print("")
    print(
        "Interpretation: this is a structural fixture result only. "
        "It does not establish truth, approval, legal sufficiency, "
        "compliance, production readiness, endorsement, audit sufficiency, "
        "or external certification."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'@

Write-Utf8Lf -Path $docPath           -Content $doc
Write-Utf8Lf -Path $schemaPath        -Content $schema
Write-Utf8Lf -Path $validFixturePath  -Content $validFixture
Write-Utf8Lf -Path $invalidFixturePath-Content $invalidFixture
Write-Utf8Lf -Path $checkerPath       -Content $checker

Write-Host "Created: $docPath"
Write-Host "Created: $schemaPath"
Write-Host "Created: $validFixturePath"
Write-Host "Created: $invalidFixturePath"
Write-Host "Created: $checkerPath"

$postureBlock = @'
Boundary Pressure Review / Retrieval Distortion Test Case
A first Boundary Pressure Review test case is maintained here:
Boundary Pressure Review / Retrieval Distortion Test Case v0.1
The case evaluates whether failed retrieval, partial access, commentary, observation, recomputation, structural reproduction, approval, endorsement, compliance, legal sufficiency, and truth remain distinguishable under pressure.
Run the checker from repo root:
python .\tools\check_boundary_pressure_review_cases_v0_1.py
'@

Add-RoutingBlock `
    -Path "docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md" `
    -BlockId "FORK_BOUNDARY_PRESSURE_RETRIEVAL_DISTORTION_CASE" `
    -Content $postureBlock

$publicIndexBlock = @'
Boundary Pressure Review
Boundary Pressure Review artifacts exercise failure cases where structural evidence, unresolved state, authority, sufficiency, truth, endorsement, and compliance may be incorrectly collapsed.
Boundary Pressure Review / Retrieval Distortion Test Case v0.1
Checker: tools/check_boundary_pressure_review_cases_v0_1.py
Fixtures: docs/review/boundary-pressure/fixtures/
'@

Add-RoutingBlock `
    -Path "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md" `
    -BlockId "FORK_BOUNDARY_PRESSURE_REVIEW_PUBLIC_INDEX" `
    -Content $publicIndexBlock

$reviewerStartBlock = @'
Boundary Pressure Review
Fork now includes an experimental Boundary Pressure Review case for retrieval distortion:
Boundary Pressure Review / Retrieval Distortion Test Case v0.1
This case tests whether failed retrieval or partial access is preserved as unresolved access state rather than upgraded into review, execution, recomputation, endorsement, approval, compliance, legal sufficiency, or truth.
'@

Add-RoutingBlock `
    -Path "docs/REVIEWER_START_HERE_v0_1.md" `
    -BlockId "FORK_BOUNDARY_PRESSURE_REVIEW_REVIEWER_START" `
    -Content $reviewerStartBlock

Write-Host ""
Write-Host "Running checker..."
python $checkerPath
Write-Host ""
Write-Host "Changed files:"
git status --short
Write-Host ""
Write-Host "SHA-256:"

if (Get-Command certutil.exe -ErrorAction SilentlyContinue) {
    certutil -hashfile $docPath SHA256
    certutil -hashfile $checkerPath SHA256
}

if ($Commit) {
    git add $docPath
    git add $schemaPath
    git add $validFixturePath
    git add $invalidFixturePath
    git add $checkerPath
    git add docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md
    git add docs/REVIEWER_START_HERE_v0_1.md
    git add docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md
    git add scripts/add_boundary_pressure_retrieval_distortion_v0_1.ps1
    git commit -m "Add boundary pressure retrieval distortion test case v0.1"

    if ($Push) {
        git push
    }
}

Write-Host ""
Write-Host "Done."