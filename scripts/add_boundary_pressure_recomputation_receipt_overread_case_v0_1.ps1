# scripts\add_boundary_pressure_recomputation_receipt_overread_case_v0_1.ps1
# Adds Boundary Pressure Recomputation Receipt Overread test case v0.1.
# PowerShell 5.1 compatible. Writes UTF-8 without BOM and LF line endings.

param(
    [switch]$Commit,
    [switch]$Push
)

$ErrorActionPreference = "Stop"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Assert-RepoRoot {
    if (-not (Test-Path ".git")) {
        throw "Run this script from the fork-public-evidence repository root."
    }
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

function Read-Utf8 {
    param([Parameter(Mandatory = $true)][string]$Path)
    return [System.IO.File]::ReadAllText((Resolve-Path $Path).Path, $Utf8NoBom)
}

function Replace-OrAppendBlock {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$BlockId,
        [Parameter(Mandatory = $true)][string]$Content
    )

    if (-not (Test-Path $Path)) {
        Write-Host "Skipping missing routing target: $Path"
        return
    }

    $start = "<!-- $($BlockId):START -->"
    $end = "<!-- $($BlockId):END -->"
    $existing = Read-Utf8 -Path $Path

    $block = @"

$start

$Content

$end
"@

    $pattern = "(?s)" + [regex]::Escape($start) + ".*?" + [regex]::Escape($end)

    if ($existing -match $pattern) {
        $updated = [regex]::Replace($existing, $pattern, $block.Trim())
        Write-Host "Replaced routing block in $Path"
    } else {
        $updated = $existing.TrimEnd() + "`n" + $block + "`n"
        Write-Host "Added routing block in $Path"
    }

    Write-Utf8Lf -Path $Path -Content $updated
}

function Invoke-Git {
    param([Parameter(Mandatory = $true)][string[]]$Args)

    & git @Args
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Args -join ' ') failed with exit code $LASTEXITCODE"
    }
}

function Invoke-Python {
    param([Parameter(Mandatory = $true)][string[]]$Args)

    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        $python = Get-Command py -ErrorAction SilentlyContinue
    }
    if (-not $python) {
        throw "Python was not found on PATH."
    }

    & $python.Source @Args
    if ($LASTEXITCODE -ne 0) {
        throw "python $($Args -join ' ') failed with exit code $LASTEXITCODE"
    }
}

Assert-RepoRoot

$caseDocPath = "docs/review/boundary-pressure/BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_TEST_CASE_v0_1.md"
$validFixturePath = "docs/review/boundary-pressure/fixtures/valid/BPR_RR_VALID_001_receipt_preserved_as_structural_v0_1.json"
$invalidFixturePath = "docs/review/boundary-pressure/fixtures/invalid/BPR_RR_INVALID_001_receipt_upgraded_to_validation_v0_1.json"
$schemaPath = "schemas/boundary_pressure_review_case_v0_1.schema.json"
$checkerPath = "tools/check_boundary_pressure_review_cases_v0_1.py"
$scriptPath = "scripts/add_boundary_pressure_recomputation_receipt_overread_case_v0_1.ps1"

$caseDoc = @'
# Boundary Pressure Recomputation Receipt Overread Test Case v0.1

Status: Experimental boundary-pressure review case.
Scope: Recomputation receipt overread.
Classification: Boundary-pressure test case, not validation, endorsement, legal conclusion, compliance conclusion, production-readiness assessment, approval, or recomputation receipt.

## 1. Purpose

This case tests whether a recomputation receipt is preserved as evidence of a bounded structural replay event without being upgraded into validation, endorsement, truth, correctness, legal sufficiency, compliance sufficiency, authorization, approval, production readiness, or institutional authority.

The boundary pressure is:

```text
A reviewer receives a recomputation receipt and later treats the receipt as if it validates the underlying artifact, decision, policy status, legal status, compliance status, or truth of the reconstructed content.

Fork must preserve the receipt without allowing the receipt to become replacement evidence or authority.
```

## 2. Core Boundary

A recomputation receipt may establish that a bounded replay or checker execution occurred and produced a particular structural result.

A recomputation receipt does not establish that:

- the underlying workflow was correct;
- the underlying decision was authorized;
- the AI output was true;
- the underlying artifact was complete;
- the underlying artifact was legally sufficient;
- compliance was satisfied;
- production readiness was established;
- a reviewer endorsed the system;
- a receipt can replace the underlying artifact;
- structural verification equals truth.

## 3. Valid Case

The valid fixture preserves the recomputation receipt as structural evidence only.

Expected result:

- RECEIPT_PRESERVED_AS_STRUCTURAL_EVIDENCE
- UNDERLYING_ARTIFACT_REQUIRED_FOR_SUBSTANTIVE_REVIEW
- AUTHORITY_NOT_INHERITED
- BOUNDARY_PRESERVED

The valid case is acceptable because the receipt is not used as proof of correctness, approval, compliance, legal sufficiency, safety, truth, or production readiness.

## 4. Invalid Case

The invalid fixture upgrades the recomputation receipt into validation of the underlying artifact.

Expected result:

- RECEIPT_OVERREAD_ATTEMPT_RECORDED
- AUTHORITY_ABSORPTION_ATTEMPT_RECORDED
- BOUNDARY_PRESSURE_REJECTED

The invalid case must be rejected because it treats the receipt as replacement evidence or authority.

## 5. Acceptance Rule

The checker passes only if:

- valid/BPR_RR_VALID_001_receipt_preserved_as_structural_v0_1.json is accepted
- invalid/BPR_RR_INVALID_001_receipt_upgraded_to_validation_v0_1.json is rejected

The checker must not treat invalidity as a hidden failure. The invalid fixture passes the test only when the checker rejects the overread attempt for the expected reason.

## 6. Non-Authority Statement

This test case does not validate Fork, certify Fork, approve Fork, establish production readiness, establish legal sufficiency, establish compliance sufficiency, or conclude that any recomputation receipt is substantively correct.

It tests only whether the boundary between recomputation evidence and downstream authority remains inspectable.
'@

$validFixture = @'
{
  "case_id": "BPR_RR_VALID_001_receipt_preserved_as_structural_v0_1",
  "case_family": "boundary_pressure_recomputation_receipt_overread",
  "case_version": "0.1",
  "expected_valid": true,
  "title": "Recomputation receipt preserved as structural evidence only",
  "description": "A recomputation receipt is preserved as evidence that a bounded replay occurred, while the underlying artifact remains required for substantive review.",
  "presented_materials": {
    "recomputation_receipt": {
      "receipt_id": "RR_VALID_001",
      "receipt_role": "structural_recomputation_receipt_only",
      "receipt_claim": "The bounded checker replay produced the recorded structural outcome.",
      "non_claims": [
        "The receipt does not validate truth.",
        "The receipt does not establish compliance.",
        "The receipt does not establish legal sufficiency.",
        "The receipt does not approve the underlying artifact.",
        "The receipt does not replace the underlying artifact."
      ]
    },
    "underlying_artifacts_available": true,
    "underlying_artifact_reference": "source_artifacts/example_underlying_artifact.json"
  },
  "boundary_controls": {
    "receipt_may_be_preserved": true,
    "receipt_may_be_cited_as_execution_evidence": true,
    "receipt_may_replace_underlying_artifact": false,
    "receipt_may_validate_underlying_truth": false,
    "receipt_may_establish_compliance": false,
    "receipt_may_establish_legal_sufficiency": false,
    "receipt_may_establish_authorization": false,
    "receipt_may_establish_production_readiness": false
  },
  "expected_outcome_codes": [
    "RECEIPT_PRESERVED_AS_STRUCTURAL_EVIDENCE",
    "UNDERLYING_ARTIFACT_REQUIRED_FOR_SUBSTANTIVE_REVIEW",
    "AUTHORITY_NOT_INHERITED",
    "BOUNDARY_PRESERVED"
  ],
  "non_authority_statement": "This fixture preserves a recomputation receipt as structural evidence only; it does not validate, certify, authorize, approve, or establish truth, compliance, legal sufficiency, safety, or production readiness."
}
'@

$invalidFixture = @'
{
  "case_id": "BPR_RR_INVALID_001_receipt_upgraded_to_validation_v0_1",
  "case_family": "boundary_pressure_recomputation_receipt_overread",
  "case_version": "0.1",
  "expected_valid": false,
  "title": "Recomputation receipt upgraded into validation of underlying artifact",
  "description": "A later reviewer has the recomputation receipt but not the underlying artifact, then treats the receipt as if it validates the underlying artifact and proves compliance or correctness.",
  "presented_materials": {
    "recomputation_receipt": {
      "receipt_id": "RR_INVALID_001",
      "receipt_role": "structural_recomputation_receipt_only",
      "receipt_claim": "The bounded checker replay produced the recorded structural outcome."
    },
    "underlying_artifacts_available": false,
    "underlying_artifact_reference": "source_artifacts/example_underlying_artifact.json",
    "missing_materials": [
      "source_artifacts/example_underlying_artifact.json"
    ]
  },
  "overread_attempt": {
    "receipt_used_as_replacement_evidence": true,
    "receipt_used_to_validate_underlying_truth": true,
    "receipt_used_to_establish_compliance": true,
    "receipt_used_to_establish_legal_sufficiency": true,
    "receipt_used_to_establish_authorization": true,
    "receipt_used_to_establish_production_readiness": true,
    "invalid_inference": "Because the recomputation receipt exists, the underlying artifact should be treated as validated, compliant, legally sufficient, approved, and safe."
  },
  "expected_outcome_codes": [
    "RECEIPT_OVERREAD_ATTEMPT_RECORDED",
    "AUTHORITY_ABSORPTION_ATTEMPT_RECORDED",
    "INCOMPLETE_OBSERVABILITY_RECORDED",
    "BOUNDARY_PRESSURE_REJECTED"
  ],
  "non_authority_statement": "This fixture intentionally contains an invalid overread attempt. A recomputation receipt cannot replace missing underlying evidence and cannot establish truth, compliance, legal sufficiency, authorization, approval, safety, or production readiness."
}
'@

$schema = @'
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://recomputableevidence.example/schemas/boundary_pressure_review_case_v0_1.schema.json",
  "title": "Fork Boundary Pressure Review Case v0.1",
  "type": "object",
  "additionalProperties": true,
  "required": [
    "case_id",
    "case_family",
    "case_version",
    "expected_valid",
    "title",
    "description",
    "expected_outcome_codes",
    "non_authority_statement"
  ],
  "properties": {
    "case_id": {
      "type": "string",
      "minLength": 1
    },
    "case_family": {
      "type": "string",
      "enum": [
        "boundary_pressure_retrieval_distortion",
        "boundary_pressure_recomputation_receipt_overread"
      ]
    },
    "case_version": {
      "type": "string"
    },
    "expected_valid": {
      "type": "boolean"
    },
    "title": {
      "type": "string"
    },
    "description": {
      "type": "string"
    },
    "presented_materials": {
      "type": "object",
      "additionalProperties": true
    },
    "boundary_controls": {
      "type": "object",
      "additionalProperties": true
    },
    "overread_attempt": {
      "type": "object",
      "additionalProperties": true
    },
    "expected_outcome_codes": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "non_authority_statement": {
      "type": "string",
      "minLength": 1
    }
  }
}
'@

$checker = @'
#!/usr/bin/env python3
"""
Fork Boundary Pressure Review Case Checker v0.1

Checks boundary-pressure fixtures for retrieval distortion and recomputation
receipt overread.

This checker does not validate truth, compliance, legal sufficiency, safety,
authorization, approval, production readiness, or institutional authority. It
checks whether valid fixtures preserve boundary state and whether invalid
fixtures are rejected for boundary-pressure reasons.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any, Dict, List, Tuple

FORBIDDEN_AUTHORITY_TERMS = [
    "approved",
    "approval",
    "authorized",
    "authorization",
    "certified",
    "certification",
    "compliant",
    "compliance",
    "control effectiveness",
    "correct",
    "endorsed",
    "endorsement",
    "legal sufficiency",
    "legally sufficient",
    "production ready",
    "production-readiness",
    "safe",
    "safety",
    "true",
    "truth",
    "validated",
    "validation",
]

REQUIRED_NON_AUTHORITY_TERMS = [
    "does not",
    "truth",
    "compliance",
    "legal",
    "authorization",
]


def as_text(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False).lower()


def load_json(path: pathlib.Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"{path}: could not parse JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be a JSON object")

    return data


def get_case_id(path: pathlib.Path, data: Dict[str, Any]) -> str:
    value = data.get("case_id")
    if isinstance(value, str) and value:
        return value
    return path.stem


def validate_common(data: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
    reasons: List[str] = []
    codes: List[str] = []

    required = [
        "case_id",
        "case_family",
        "case_version",
        "expected_valid",
        "title",
        "description",
        "expected_outcome_codes",
        "non_authority_statement",
    ]

    for key in required:
        if key not in data:
            reasons.append(f"missing required field: {key}")

    if "expected_valid" in data and not isinstance(data["expected_valid"], bool):
        reasons.append("expected_valid must be boolean")

    outcomes = data.get("expected_outcome_codes")
    if not isinstance(outcomes, list) or not outcomes or not all(
        isinstance(x, str) for x in outcomes
    ):
        reasons.append("expected_outcome_codes must be a non-empty string array")
    else:
        codes.extend(outcomes)

    non_authority = str(data.get("non_authority_statement", "")).lower()
    for term in REQUIRED_NON_AUTHORITY_TERMS:
        if term not in non_authority:
            reasons.append(f"non_authority_statement missing boundary term: {term}")

    return (not reasons), codes, reasons


def evaluate_recomputation_receipt_overread(
    data: Dict[str, Any]
) -> Tuple[bool, List[str], List[str]]:
    ok, codes, reasons = validate_common(data)
    if not ok:
        return False, codes, reasons

    expected_valid = data.get("expected_valid") is True
    text = as_text(data)

    presented = data.get("presented_materials", {})
    if not isinstance(presented, dict):
        reasons.append("presented_materials must be object")
        return False, codes, reasons

    receipt = presented.get("recomputation_receipt", {})
    if not isinstance(receipt, dict):
        reasons.append("presented_materials.recomputation_receipt must be object")
        return False, codes, reasons

    role = str(receipt.get("receipt_role", "")).lower()
    underlying_available = presented.get("underlying_artifacts_available")

    if expected_valid:
        if role != "structural_recomputation_receipt_only":
            reasons.append(
                "valid RR fixture must preserve receipt as structural_recomputation_receipt_only"
            )

        if underlying_available is not True:
            reasons.append(
                "valid RR fixture must retain underlying artifact availability"
            )

        controls = data.get("boundary_controls", {})
        if not isinstance(controls, dict):
            reasons.append("valid RR fixture must include boundary_controls object")
        else:
            disallowed_true = [
                "receipt_may_replace_underlying_artifact",
                "receipt_may_validate_underlying_truth",
                "receipt_may_establish_compliance",
                "receipt_may_establish_legal_sufficiency",
                "receipt_may_establish_authorization",
                "receipt_may_establish_production_readiness",
            ]
            for key in disallowed_true:
                if controls.get(key) is not False:
                    reasons.append(f"valid RR fixture must set {key}=false")

        required_codes = [
            "RECEIPT_PRESERVED_AS_STRUCTURAL_EVIDENCE",
            "UNDERLYING_ARTIFACT_REQUIRED_FOR_SUBSTANTIVE_REVIEW",
            "AUTHORITY_NOT_INHERITED",
            "BOUNDARY_PRESERVED",
        ]
        for code in required_codes:
            if code not in codes:
                reasons.append(f"valid RR fixture missing expected outcome code: {code}")

        return (not reasons), codes, reasons

    overread = data.get("overread_attempt", {})
    if not isinstance(overread, dict):
        reasons.append("invalid RR fixture must include overread_attempt object")
        return False, codes, reasons

    overread_flags = [
        "receipt_used_as_replacement_evidence",
        "receipt_used_to_validate_underlying_truth",
        "receipt_used_to_establish_compliance",
        "receipt_used_to_establish_legal_sufficiency",
        "receipt_used_to_establish_authorization",
        "receipt_used_to_establish_production_readiness",
    ]

    if underlying_available is not False:
        reasons.append("invalid RR fixture should model missing underlying artifacts")

    if not any(overread.get(flag) is True for flag in overread_flags):
        reasons.append(
            "invalid RR fixture must contain at least one explicit overread flag"
        )

    if not any(term in text for term in FORBIDDEN_AUTHORITY_TERMS):
        reasons.append(
            "invalid RR fixture must contain an authority/validation overread term"
        )

    required_codes = [
        "RECEIPT_OVERREAD_ATTEMPT_RECORDED",
        "AUTHORITY_ABSORPTION_ATTEMPT_RECORDED",
        "BOUNDARY_PRESSURE_REJECTED",
    ]
    for code in required_codes:
        if code not in codes:
            reasons.append(
                f"invalid RR fixture missing expected rejection code: {code}"
            )

    if reasons:
        return False, codes, reasons

    return False, codes, ["RR overread detected and rejected as expected"]


def evaluate_retrieval_distortion(
    data: Dict[str, Any]
) -> Tuple[bool, List[str], List[str]]:
    ok, codes, reasons = validate_common(data)
    if not ok:
        return False, codes, reasons

    expected_valid = data.get("expected_valid")
    text = as_text(data)

    retrieval_terms = [
        "retrieval",
        "access",
        "source",
        "unavailable",
        "unresolved",
        "missing",
        "failed",
        "partial",
    ]
    has_retrieval_signal = any(term in text for term in retrieval_terms)

    if expected_valid is True:
        if not has_retrieval_signal:
            reasons.append(
                "valid RD fixture must preserve access/retrieval limitation state"
            )

        invalid_upgrade_terms = [
            "treated as review completed",
            "review completed",
            "validated by failed retrieval",
            "approved despite failed retrieval",
        ]
        if any(term in text for term in invalid_upgrade_terms):
            reasons.append("valid RD fixture contains review/validation upgrade language")

        return (not reasons), codes, reasons

    upgrade_terms = [
        "treated_as_review",
        "failed_retrieval_treated_as_review",
        "review_completed",
        "review completed",
        "recomputation_completed",
        "validated",
        "approved",
        "certified",
        "compliant",
        "legal sufficiency",
    ]
    if not any(term in text for term in upgrade_terms):
        reasons.append(
            "invalid RD fixture must contain retrieval-to-review or retrieval-to-authority upgrade signal"
        )

    if reasons:
        return False, codes, reasons

    return False, codes, ["RD retrieval distortion detected and rejected as expected"]


def evaluate_case(
    path: pathlib.Path, data: Dict[str, Any]
) -> Tuple[bool, List[str], List[str]]:
    case_id = get_case_id(path, data)
    family = str(data.get("case_family", "")).lower()

    if "recomputation_receipt_overread" in family or case_id.startswith("BPR_RR_"):
        return evaluate_recomputation_receipt_overread(data)

    if "retrieval_distortion" in family or case_id.startswith("BPR_RD_"):
        return evaluate_retrieval_distortion(data)

    ok, codes, reasons = validate_common(data)
    if not ok:
        return False, codes, reasons

    if data.get("expected_valid") is True:
        return True, codes, reasons

    return False, codes, ["unknown invalid boundary-pressure fixture rejected"]


def find_fixture_paths(root: pathlib.Path) -> List[pathlib.Path]:
    paths: List[pathlib.Path] = []
    for subdir in ["valid", "invalid"]:
        current = root / subdir
        if current.exists():
            paths.extend(sorted(current.glob("*.json")))
    return paths


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fixtures-root",
        default="docs/review/boundary-pressure/fixtures",
        help="Boundary-pressure fixtures root containing valid/ and invalid/ directories.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON summary.")
    args = parser.parse_args(argv)

    root = pathlib.Path(args.fixtures_root)
    if not root.exists():
        raise SystemExit(f"fixtures root not found: {root}")

    results: List[Dict[str, Any]] = []
    failures: List[str] = []

    for path in find_fixture_paths(root):
        data = load_json(path)
        actual_valid, codes, reasons = evaluate_case(path, data)
        expected_valid_by_dir = path.parent.name == "valid"

        passed = actual_valid == expected_valid_by_dir
        result = {
            "path": str(path).replace("\\", "/"),
            "case_id": get_case_id(path, data),
            "expected_valid_by_dir": expected_valid_by_dir,
            "actual_valid": actual_valid,
            "passed": passed,
            "outcome_codes": codes,
            "reasons": reasons,
        }
        results.append(result)

        if not passed:
            failures.append(
                f"{result['path']}: expected valid={expected_valid_by_dir}, "
                f"actual valid={actual_valid}; reasons={reasons}"
            )

    summary = {
        "checker": "check_boundary_pressure_review_cases_v0_1.py",
        "fixtures_root": str(root).replace("\\", "/"),
        "total": len(results),
        "passed": sum(1 for r in results if r["passed"]),
        "failed": sum(1 for r in results if not r["passed"]),
        "results": results,
        "non_authority_statement": (
            "This checker evaluates boundary-pressure fixture classification only; "
            "it does not validate truth, compliance, legal sufficiency, safety, "
            "authorization, approval, production readiness, or institutional authority."
        ),
    }

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"Boundary pressure fixtures: {summary['passed']}/{summary['total']} passed")
        for result in results:
            status = "PASS" if result["passed"] else "FAIL"
            print(f"{status} {result['case_id']} ({result['path']})")
            for reason in result["reasons"]:
                print(f"  - {reason}")

    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
'@

Write-Utf8Lf -Path $caseDocPath -Content $caseDoc
Write-Utf8Lf -Path $validFixturePath -Content $validFixture
Write-Utf8Lf -Path $invalidFixturePath -Content $invalidFixture
Write-Utf8Lf -Path $schemaPath -Content $schema
Write-Utf8Lf -Path $checkerPath -Content $checker

$publicIndexBlock = @'
Boundary Pressure Review: Recomputation Receipt Overread
This boundary-pressure case tests whether a recomputation receipt is preserved as structural evidence without being upgraded into validation, endorsement, approval, compliance, legal sufficiency, truth, safety, production readiness, or institutional authority.
Test case: docs/review/boundary-pressure/BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_TEST_CASE_v0_1.md
Valid fixture: docs/review/boundary-pressure/fixtures/valid/BPR_RR_VALID_001_receipt_preserved_as_structural_v0_1.json
Invalid fixture: docs/review/boundary-pressure/fixtures/invalid/BPR_RR_INVALID_001_receipt_upgraded_to_validation_v0_1.json
Checker: tools/check_boundary_pressure_review_cases_v0_1.py
The case does not validate Fork, certify Fork, approve Fork, establish legal sufficiency, establish compliance sufficiency, or prove the truth of any underlying artifact.
'@

$reviewerStartBlock = @'
Boundary Pressure Case: Recomputation Receipt Overread
Fork includes an experimental boundary-pressure case for recomputation receipt overread.
This case tests whether a recomputation receipt remains evidence of bounded structural replay rather than becoming replacement evidence, validation, approval, compliance, legal sufficiency, truth, safety, production readiness, or authority.
Start with:
docs/review/boundary-pressure/BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_TEST_CASE_v0_1.md
Then run:
python tools/check_boundary_pressure_review_cases_v0_1.py --json

'@

$postureBlock = @'
Boundary Pressure: Recomputation Receipt Overread
A recomputation receipt is not authority.
A receipt may show that a bounded replay or checker execution occurred and produced a particular structural result. It does not validate the underlying artifact, replace missing source evidence, establish legal sufficiency, establish compliance, prove truth, approve a decision, establish safety, or demonstrate production readiness.
The recomputation receipt overread case tests this pressure directly by preserving one valid fixture where the receipt remains structural evidence and one invalid fixture where the receipt is upgraded into validation or authority.
'@

Replace-OrAppendBlock -Path "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md" `
    -BlockId "FORK_BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_PUBLIC_INDEX" `
    -Content $publicIndexBlock

Replace-OrAppendBlock -Path "docs/REVIEWER_START_HERE_V0_1.md" `
    -BlockId "FORK_BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_REVIEWER_START" `
    -Content $reviewerStartBlock

Replace-OrAppendBlock -Path "docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md" `
    -BlockId "FORK_BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_REVIEW_POSTURE" `
    -Content $postureBlock

Write-Host ""
Write-Host "Created or updated:"
Write-Host " $caseDocPath"
Write-Host " $validFixturePath"
Write-Host " $invalidFixturePath"
Write-Host " $schemaPath"
Write-Host " $checkerPath"
Write-Host ""
Write-Host "Running checker..."
Invoke-Python -Args @($checkerPath, "--json")
Write-Host ""
Write-Host "Changed files:"
git status --short
Write-Host ""
Write-Host "Review commands:"
Write-Host " git diff -- docs\review\boundary-pressure"
Write-Host " git diff -- schemas\boundary_pressure_review_case_v0_1.schema.json"
Write-Host " git diff -- tools\check_boundary_pressure_review_cases_v0_1.py"
Write-Host " git diff --check"
Write-Host " python tools\check_boundary_pressure_review_cases_v0_1.py --json"

if ($Commit) {
    Write-Host ""
    Write-Host "Running repository whitespace check..."
    Invoke-Git -Args @("diff", "--check")
    Write-Host ""
    Write-Host "Running checker before commit..."
    Invoke-Python -Args @($checkerPath, "--json")

    Invoke-Git -Args @(
        "add", "--",
        "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md",
        "docs/REVIEWER_START_HERE_v0_1.md",
        "docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md",
        $caseDocPath,
        $validFixturePath,
        $invalidFixturePath,
        $schemaPath,
        $checkerPath,
        $scriptPath
    )

    Invoke-Git -Args @("diff", "--cached", "--check")
    Invoke-Git -Args @("commit", "-m", "Add boundary pressure recomputation receipt overread case")

    if ($Push) {
        Invoke-Git -Args @("push")
    }
}

Write-Host ""
Write-Host "Done."

# This script intentionally keeps the longitudinal reconstruction protocol
# untouched and limits this commit to the boundary-pressure receipt-overread
# workstream.