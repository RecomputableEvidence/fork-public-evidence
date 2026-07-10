# scripts/harden_boundary_pressure_invalid_fixture_semantics_v0_1.ps1
# Hardens boundary-pressure checker invalid-fixture semantics after Round 004 adversarial review.
# PowerShell 5.1 compatible. Writes UTF-8 without BOM and LF.

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

$checkerPath = "tools/check_boundary_pressure_review_cases_v0_1.py"
$publicVerifierPath = "scripts/verify_public_review_package_v0_1.ps1"
$receiptPath = "docs/review/boundary-pressure/BOUNDARY_PRESSURE_CHECKER_INVALID_FIXTURE_HARDENING_RECEIPT_v0_1.md"
$scriptPath = "scripts/harden_boundary_pressure_invalid_fixture_semantics_v0_1.ps1"

$advRoot = "docs/review/boundary-pressure/fixtures/adversarial"
$advRdValidShapedPath = "$advRoot/BPR_RD_ADVERSARIAL_001_valid_shaped_content_under_invalid_expectation_v0_1.json"
$advRrNearEmptyPath = "$advRoot/BPR_RR_ADVERSARIAL_001_near_empty_invalid_overread_v0_1.json"
$advRrNoOverreadPath = "$advRoot/BPR_RR_ADVERSARIAL_002_invalid_without_overread_flags_v0_1.json"
$advUnknownValidPath = "$advRoot/BPR_UNKNOWN_ADVERSARIAL_001_unknown_family_must_not_pass_by_directory_v0_1.json"

$checker = @'
#!/usr/bin/env python3
"""
Fork Boundary Pressure Review Case Checker v0.1

Checks boundary-pressure fixtures for retrieval distortion and recomputation
receipt overread.

This checker does not validate truth, compliance, legal sufficiency, safety,
authorization, approval, production readiness, or institutional authority.

Hardening note:
Invalid fixtures must now be rejected for content-sensitive boundary-pressure
reasons, not merely because they are placed in invalid/ or self-declare
expected_valid=false. Adversarial regression mode verifies that malformed,
mislabeled, content-free, or valid-shaped negative fixtures do not silently pass.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any, Dict, List, Tuple


REQUIRED_RR_NON_AUTHORITY_TERMS = [
    "does not",
    "truth",
    "compliance",
    "legal",
    "authorization",
]

FORBIDDEN_AUTHORITY_TERMS = [
    "approved",
    "approval",
    "authorized",
    "authorization",
    "certified",
    "certification",
    "compliant",
    "compliance",
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


def as_text(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False).lower()


def load_json(path: pathlib.Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception as exc:
        raise ValueError(f"{path}: could not parse JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be a JSON object")
    return data


def get_case_id(path: pathlib.Path, data: Dict[str, Any]) -> str:
    value = data.get("case_id") or data.get("caseId") or data.get("id")
    if isinstance(value, str) and value:
        return value
    return path.stem


def normalized_case_id(path: pathlib.Path, data: Dict[str, Any]) -> str:
    return get_case_id(path, data).replace("-", "_").upper()


def expected_valid_for_path(path: pathlib.Path, data: Dict[str, Any]) -> bool:
    if isinstance(data.get("expected_valid"), bool):
        return data["expected_valid"]
    return path.parent.name == "valid"


def validate_rr_common(data: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
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
    if not isinstance(outcomes, list) or not outcomes or not all(isinstance(x, str) for x in outcomes):
        reasons.append("expected_outcome_codes must be a non-empty string array")
    else:
        codes.extend(outcomes)

    non_authority = str(data.get("non_authority_statement", "")).lower()
    for term in REQUIRED_RR_NON_AUTHORITY_TERMS:
        if term not in non_authority:
            reasons.append(f"non_authority_statement missing boundary term: {term}")

    return (not reasons), codes, reasons


def evaluate_recomputation_receipt_overread(data: Dict[str, Any]) -> Tuple[bool, bool, List[str], List[str]]:
    """
    Returns:
      evaluation_ok: checker recognized and evaluated the fixture semantics
      actual_valid: fixture is boundary-valid
      codes: outcome codes
      reasons: diagnostic reasons

    Invalid RR fixtures are evaluation_ok=True only when an actual overread
    condition is present and the expected rejection codes are present.
    """
    ok, codes, reasons = validate_rr_common(data)
    if not ok:
        return False, False, codes, reasons

    expected_valid = data.get("expected_valid") is True
    text = as_text(data)

    presented = data.get("presented_materials", {})
    if not isinstance(presented, dict):
        return False, False, codes, ["presented_materials must be object"]

    receipt = presented.get("recomputation_receipt", {})
    if not isinstance(receipt, dict):
        return False, False, codes, ["presented_materials.recomputation_receipt must be object"]

    role = str(receipt.get("receipt_role", "")).lower()
    underlying_available = presented.get("underlying_artifacts_available")

    if expected_valid:
        if role != "structural_recomputation_receipt_only":
            reasons.append("valid RR fixture must preserve receipt as structural_recomputation_receipt_only")

        if underlying_available is not True:
            reasons.append("valid RR fixture must retain underlying artifact availability")

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

        return (not reasons), (not reasons), codes, reasons

    overread = data.get("overread_attempt", {})
    if not isinstance(overread, dict):
        return False, False, codes, ["invalid RR fixture must include overread_attempt object"]

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
        reasons.append("invalid RR fixture must contain at least one explicit overread flag")

    if not any(term in text for term in FORBIDDEN_AUTHORITY_TERMS):
        reasons.append("invalid RR fixture must contain an authority/validation overread term")

    required_codes = [
        "RECEIPT_OVERREAD_ATTEMPT_RECORDED",
        "AUTHORITY_ABSORPTION_ATTEMPT_RECORDED",
        "BOUNDARY_PRESSURE_REJECTED",
    ]
    for code in required_codes:
        if code not in codes:
            reasons.append(f"invalid RR fixture missing expected rejection code: {code}")

    if reasons:
        return False, False, codes, reasons

    return True, False, codes, ["RR overread detected and rejected as expected"]


def evaluate_retrieval_distortion(path: pathlib.Path, data: Dict[str, Any]) -> Tuple[bool, bool, List[str], List[str]]:
    """
    Legacy-compatible retrieval-distortion evaluation.

    Valid RD fixtures must preserve access/retrieval limitation state without
    explicit upgrade language.

    Invalid RD fixtures must contain both retrieval/access limitation signal and
    explicit retrieval-to-review or retrieval-to-authority upgrade signal.
    Directory placement alone is not sufficient.
    """
    expected_valid = expected_valid_for_path(path, data)
    text = as_text(data)

    codes: List[str] = []
    if isinstance(data.get("expected_outcome_codes"), list):
        codes = [x for x in data["expected_outcome_codes"] if isinstance(x, str)]

    retrieval_terms = [
        "retrieval",
        "access",
        "source",
        "unavailable",
        "unresolved",
        "missing",
        "failed",
        "partial",
        "not available",
        "no access",
    ]

    explicit_upgrade_patterns = [
        '"failed_retrieval_treated_as_review": true',
        '"treated_as_review": true',
        '"retrieval_failure_treated_as_review": true',
        '"review_completed": true',
        '"recomputation_completed": true',
        '"validated_by_failed_retrieval": true',
        '"approved_despite_failed_retrieval": true',
        "failed retrieval treated as review",
        "failed retrieval was treated as review",
        "partial retrieval treated as review",
        "source unavailable but review completed",
        "missing source treated as validated",
        "missing source treated as approved",
    ]

    has_retrieval_signal = any(term in text for term in retrieval_terms)
    has_explicit_upgrade = any(pattern in text for pattern in explicit_upgrade_patterns)

    reasons: List[str] = []

    if expected_valid:
        if not has_retrieval_signal:
            reasons.append("valid RD fixture must preserve access/retrieval limitation state")
        if has_explicit_upgrade:
            reasons.append("valid RD fixture must not explicitly upgrade failed/partial retrieval into review or authority")
        return (not reasons), (not reasons), codes, reasons

    if not has_retrieval_signal:
        reasons.append("invalid RD fixture must contain access/retrieval limitation signal")
    if not has_explicit_upgrade:
        reasons.append("invalid RD fixture must contain explicit retrieval-to-review or retrieval-to-authority upgrade signal")

    if reasons:
        return False, False, codes, reasons

    return True, False, codes, ["RD retrieval distortion detected and rejected as expected"]


def evaluate_case(path: pathlib.Path, data: Dict[str, Any]) -> Tuple[bool, bool, List[str], List[str]]:
    family = str(data.get("case_family", "")).lower()
    case_id = normalized_case_id(path, data)

    if "recomputation_receipt_overread" in family or case_id.startswith("BPR_RR_"):
        return evaluate_recomputation_receipt_overread(data)

    if "retrieval_distortion" in family or case_id.startswith("BPR_RD_"):
        return evaluate_retrieval_distortion(path, data)

    return False, False, [], ["unknown boundary-pressure fixture family rejected"]


def find_default_fixture_paths(root: pathlib.Path) -> List[pathlib.Path]:
    paths: List[pathlib.Path] = []
    for subdir in ["valid", "invalid"]:
        current = root / subdir
        if current.exists():
            paths.extend(sorted(current.glob("*.json")))
    return paths


def find_adversarial_paths(root: pathlib.Path) -> List[pathlib.Path]:
    current = root / "adversarial"
    if not current.exists():
        return []
    return sorted(current.glob("*.json"))


def evaluate_default_fixture(path: pathlib.Path) -> Dict[str, Any]:
    data = load_json(path)
    evaluation_ok, actual_valid, codes, reasons = evaluate_case(path, data)
    expected_valid_by_dir = path.parent.name == "valid"
    passed = evaluation_ok and (actual_valid == expected_valid_by_dir)

    return {
        "path": str(path).replace("\\", "/"),
        "case_id": get_case_id(path, data),
        "expected_valid_by_dir": expected_valid_by_dir,
        "evaluation_ok": evaluation_ok,
        "actual_valid": actual_valid,
        "passed": passed,
        "outcome_codes": codes,
        "reasons": reasons,
    }


def evaluate_adversarial_fixture(path: pathlib.Path) -> Dict[str, Any]:
    data = load_json(path)
    evaluation_ok, actual_valid, codes, reasons = evaluate_case(path, data)
    expected_suite_pass = data.get("adversarial_expected_suite_pass", False)

    # For adversarial regression fixtures in this version, success means the
    # hardened evaluator refuses to treat the fixture as a valid, well-formed
    # member of the default suite.
    rejected_by_hardening = not evaluation_ok
    passed = rejected_by_hardening == (not expected_suite_pass)

    return {
        "path": str(path).replace("\\", "/"),
        "case_id": get_case_id(path, data),
        "adversarial_expected_suite_pass": expected_suite_pass,
        "evaluation_ok": evaluation_ok,
        "actual_valid": actual_valid,
        "passed": passed,
        "outcome_codes": codes,
        "reasons": reasons,
    }


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fixtures-root",
        default="docs/review/boundary-pressure/fixtures",
        help="Boundary-pressure fixtures root containing valid/, invalid/, and optionally adversarial/ directories.",
    )
    parser.add_argument("--run-adversarial", action="store_true", help="Run adversarial regression fixtures.")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary.")
    args = parser.parse_args(argv)

    root = pathlib.Path(args.fixtures_root)
    if not root.exists():
        raise SystemExit(f"fixtures root not found: {root}")

    results = [evaluate_default_fixture(path) for path in find_default_fixture_paths(root)]
    failed = sum(1 for result in results if not result["passed"])

    adversarial_summary = None
    adversarial_failed = 0

    if args.run_adversarial:
        adversarial_results = [evaluate_adversarial_fixture(path) for path in find_adversarial_paths(root)]
        adversarial_failed = sum(1 for result in adversarial_results if not result["passed"])
        adversarial_summary = {
            "total": len(adversarial_results),
            "passed": len(adversarial_results) - adversarial_failed,
            "failed": adversarial_failed,
            "results": adversarial_results,
            "interpretation": (
                "Adversarial regression fixtures pass only when the checker refuses "
                "to silently accept malformed, mislabeled, content-free, or valid-shaped "
                "negative fixtures as successful default-suite cases."
            ),
        }

    summary = {
        "checker": "check_boundary_pressure_review_cases_v0_1.py",
        "fixtures_root": str(root).replace("\\", "/"),
        "total": len(results),
        "passed": len(results) - failed,
        "failed": failed,
        "results": results,
        "adversarial": adversarial_summary,
        "non_authority_statement": (
            "This checker evaluates boundary-pressure fixture classification only; "
            "it does not validate truth, compliance, legal sufficiency, safety, "
            "authorization, approval, production readiness, endorsement, or "
            "institutional authority."
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

        if adversarial_summary is not None:
            print(
                f"Adversarial regression fixtures: "
                f"{adversarial_summary['passed']}/{adversarial_summary['total']} passed"
            )
            for result in adversarial_summary["results"]:
                status = "PASS" if result["passed"] else "FAIL"
                print(f"{status} {result['case_id']} ({result['path']})")
                for reason in result["reasons"]:
                    print(f"  - {reason}")

    return 0 if failed == 0 and adversarial_failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
'@

$advRdValidShaped = @'
{
  "case_id": "BPR_RD_ADVERSARIAL_001_valid_shaped_content_under_invalid_expectation_v0_1",
  "case_family": "boundary_pressure_retrieval_distortion",
  "case_version": "0.1",
  "expected_valid": false,
  "adversarial_expected_suite_pass": false,
  "title": "Valid-shaped retrieval limitation content must not pass as invalid distortion",
  "description": "This fixture preserves access limitation state but does not contain explicit retrieval-to-review or retrieval-to-authority upgrade language. It must not be counted as a successful invalid retrieval-distortion negative test.",
  "access_state": {
    "retrieval": "partial",
    "source": "unavailable",
    "review_status": "not completed"
  },
  "non_authority_statement": "This adversarial fixture does not establish truth, compliance, legal sufficiency, authorization, approval, safety, production readiness, endorsement, certification, validation, or authority.",
  "adversarial_expectation": "Hardened checker should reject this as an invalid fixture lacking explicit upgrade signal."
}
'@

$advRrNearEmpty = @'
{
  "case_id": "BPR_RR_ADVERSARIAL_001_near_empty_invalid_overread_v0_1",
  "case_family": "boundary_pressure_recomputation_receipt_overread",
  "expected_valid": false,
  "adversarial_expected_suite_pass": false,
  "adversarial_expectation": "Hardened checker should reject this as malformed rather than count it as a successful invalid overread fixture."
}
'@

$advRrNoOverread = @'
{
  "case_id": "BPR_RR_ADVERSARIAL_002_invalid_without_overread_flags_v0_1",
  "case_family": "boundary_pressure_recomputation_receipt_overread",
  "case_version": "0.1",
  "expected_valid": false,
  "adversarial_expected_suite_pass": false,
  "title": "Invalid RR fixture without overread flags must not pass",
  "description": "This fixture has common RR fields but lacks explicit overread flags, so it must not be counted as a successful invalid recomputation receipt overread negative test.",
  "presented_materials": {
    "recomputation_receipt": {
      "receipt_id": "RR_ADV_002",
      "receipt_role": "structural_recomputation_receipt_only",
      "receipt_claim": "The bounded checker replay produced the recorded structural outcome."
    },
    "underlying_artifacts_available": false,
    "underlying_artifact_reference": "source_artifacts/example_underlying_artifact.json"
  },
  "overread_attempt": {
    "receipt_used_as_replacement_evidence": false,
    "receipt_used_to_validate_underlying_truth": false,
    "receipt_used_to_establish_compliance": false,
    "receipt_used_to_establish_legal_sufficiency": false,
    "receipt_used_to_establish_authorization": false,
    "receipt_used_to_establish_production_readiness": false
  },
  "expected_outcome_codes": [
    "RECEIPT_OVERREAD_ATTEMPT_RECORDED",
    "AUTHORITY_ABSORPTION_ATTEMPT_RECORDED",
    "BOUNDARY_PRESSURE_REJECTED"
  ],
  "non_authority_statement": "This adversarial fixture does not establish truth, compliance, legal sufficiency, authorization, approval, safety, production readiness, endorsement, certification, validation, or authority.",
  "adversarial_expectation": "Hardened checker should reject this as an invalid fixture lacking explicit overread flags."
}
'@

$advUnknownValid = @'
{
  "case_id": "BPR_UNKNOWN_ADVERSARIAL_001_unknown_family_must_not_pass_by_directory_v0_1",
  "case_family": "unknown_boundary_pressure_family",
  "case_version": "0.1",
  "expected_valid": true,
  "adversarial_expected_suite_pass": false,
  "title": "Unknown family must not pass by directory or self-declaration",
  "description": "This fixture is intentionally shaped as a plausible valid fixture but uses an unknown family. The checker must reject unknown families rather than passing them by placement or expected_valid value.",
  "expected_outcome_codes": [
    "UNKNOWN_FAMILY_MUST_NOT_PASS"
  ],
  "non_authority_statement": "This adversarial fixture does not establish truth, compliance, legal sufficiency, authorization, approval, safety, production readiness, endorsement, certification, validation, or authority.",
  "adversarial_expectation": "Hardened checker should reject this unknown family."
}
'@

$receipt = @'
# Boundary Pressure Checker Invalid-Fixture Hardening Receipt v0.1

Status: Hardening receipt.
Scope: Boundary-pressure checker invalid-fixture semantics.
Classification: Engineering response to Public Review Round 004 adversarial observation.

## 1. Background

Public Review Round 004 produced an execution/recomputation/adversarial observation against the boundary-pressure checker.

The finding was narrow:

- the shipped fixtures were honestly authored;
- the public verifier was runnable;
- the default boundary-pressure suite passed;
- however, invalid fixture branches could classify negative fixtures by placement or self-declaration rather than fully content-gating the invalid condition.

## 2. Hardening Change

The checker now separates:

- `evaluation_ok`: whether the checker recognized and evaluated the fixture semantics;
- `actual_valid`: whether the fixture is boundary-valid;
- `passed`: whether the fixture result matches the expected suite role.

Invalid fixtures now pass the default suite only when the invalid condition is actually detected.

Malformed, mislabeled, content-free, valid-shaped-negative, or unknown-family fixtures must not silently pass.

## 3. Adversarial Regression Fixtures

The hardening adds adversarial fixtures under:

- `docs/review/boundary-pressure/fixtures/adversarial/`

The adversarial regression suite tests that the checker refuses to silently accept:

- retrieval limitation content filed as invalid without explicit upgrade signal;
- near-empty recomputation receipt overread fixtures;
- invalid recomputation receipt overread fixtures without overread flags;
- unknown fixture families that would otherwise rely on placement or self-declaration.

## 4. Commands

Default boundary-pressure suite:

- `python tools/check_boundary_pressure_review_cases_v0_1.py --json`

Default plus adversarial regression suite:

- `python tools/check_boundary_pressure_review_cases_v0_1.py --json --run-adversarial`

Public verifier:

- `powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1`

## 5. Boundary Statement

This hardening does not validate Fork, certify Fork, approve Fork, establish legal sufficiency, establish compliance sufficiency, establish safety, establish production readiness, or transfer authority.

It narrows the checker claim by ensuring invalid fixture pass status depends on detected boundary-pressure content rather than placement or self-declaration alone.
'@

Write-Utf8Lf -Path $checkerPath -Content $checker
Write-Utf8Lf -Path $advRdValidShapedPath -Content $advRdValidShaped
Write-Utf8Lf -Path $advRrNearEmptyPath -Content $advRrNearEmpty
Write-Utf8Lf -Path $advRrNoOverreadPath -Content $advRrNoOverread
Write-Utf8Lf -Path $advUnknownValidPath -Content $advUnknownValid
Write-Utf8Lf -Path $receiptPath -Content $receipt

if (Test-Path $publicVerifierPath) {
    $verifier = Read-Utf8 -Path $publicVerifierPath

    $verifier = $verifier.Replace(
        '@("tools/check_boundary_pressure_review_cases_v0_1.py", "--json")',
        '@("tools/check_boundary_pressure_review_cases_v0_1.py", "--json", "--run-adversarial")'
    )

    if ($verifier -notlike "*Adversarial boundary pressure regression:*") {
        $oldBlock = @'
    if ($checkerData -and $checkerData.total -ne $null) {
        Write-Host ""
        Write-Host "Boundary pressure checker:"
        Write-Host "  total: $($checkerData.total)"
        Write-Host "  passed: $($checkerData.passed)"
        Write-Host "  failed: $($checkerData.failed)"
    }
'@

        $newBlock = @'
    if ($checkerData -and $checkerData.total -ne $null) {
        Write-Host ""
        Write-Host "Boundary pressure checker:"
        Write-Host "  total: $($checkerData.total)"
        Write-Host "  passed: $($checkerData.passed)"
        Write-Host "  failed: $($checkerData.failed)"
    }

    if ($checkerData -and $checkerData.adversarial -and $checkerData.adversarial.total -ne $null) {
        Write-Host ""
        Write-Host "Adversarial boundary pressure regression:"
        Write-Host "  total: $($checkerData.adversarial.total)"
        Write-Host "  passed: $($checkerData.adversarial.passed)"
        Write-Host "  failed: $($checkerData.adversarial.failed)"
    }
'@

        $verifier = $verifier.Replace(($oldBlock -replace "`r`n", "`n"), ($newBlock -replace "`r`n", "`n"))
    }

    Write-Utf8Lf -Path $publicVerifierPath -Content $verifier
}

$currentProofBlock = @'
## Boundary-pressure invalid-fixture hardening

The boundary-pressure checker now distinguishes fixture classification from evaluator confidence.

Default shipped fixture suite:

- valid retrieval limitation preserved;
- invalid retrieval distortion detected;
- valid recomputation receipt preserved as structural evidence;
- invalid recomputation receipt overread detected.

Adversarial regression suite:

- valid-shaped retrieval limitation content must not pass as invalid distortion;
- near-empty recomputation receipt overread fixture must not pass;
- invalid recomputation receipt overread fixture without overread flags must not pass;
- unknown fixture family must not pass by placement or self-declaration.

Run:

- `python tools/check_boundary_pressure_review_cases_v0_1.py --json --run-adversarial`

This hardening does not validate truth, compliance, legal sufficiency, safety, authorization, approval, production readiness, endorsement, certification, or institutional authority.
'@

$publicIndexBlock = @'
## Boundary-pressure checker invalid-fixture hardening

Hardening receipt:

- `docs/review/boundary-pressure/BOUNDARY_PRESSURE_CHECKER_INVALID_FIXTURE_HARDENING_RECEIPT_v0_1.md`

Adversarial regression fixtures:

- `docs/review/boundary-pressure/fixtures/adversarial/`

Run default plus adversarial regression:

- `python tools/check_boundary_pressure_review_cases_v0_1.py --json --run-adversarial`
'@

Replace-OrAppendBlock `
    -Path "docs/CURRENT_PROOF_SURFACE_v0_1.md" `
    -BlockId "FORK_BOUNDARY_PRESSURE_INVALID_FIXTURE_HARDENING" `
    -Content $currentProofBlock

Replace-OrAppendBlock `
    -Path "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md" `
    -BlockId "FORK_BOUNDARY_PRESSURE_INVALID_FIXTURE_HARDENING" `
    -Content $publicIndexBlock

Write-Host ""
Write-Host "Running default boundary-pressure checker..."
Invoke-Python -Args @($checkerPath, "--json")

Write-Host ""
Write-Host "Running boundary-pressure checker with adversarial regression..."
Invoke-Python -Args @($checkerPath, "--json", "--run-adversarial")

Write-Host ""
Write-Host "Running public review verifier..."
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    throw "Public review verifier failed."
}

Write-Host ""
Write-Host "Running Round 004 interaction checker..."
Invoke-Python -Args @("tools/check_public_review_round_004_interactions_v0_1.py", "--json")

Write-Host ""
Write-Host "Running whitespace check..."
Invoke-Git -Args @("diff", "--check")

Write-Host ""
Write-Host "Changed files:"
git status --short

Write-Host ""
Write-Host "Review commands:"
Write-Host "  git diff -- tools\check_boundary_pressure_review_cases_v0_1.py"
Write-Host "  git diff -- docs\review\boundary-pressure"
Write-Host "  git diff -- scripts\verify_public_review_package_v0_1.ps1"
Write-Host "  python tools\check_boundary_pressure_review_cases_v0_1.py --json --run-adversarial"
Write-Host "  powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1"
Write-Host "  python tools\check_public_review_round_004_interactions_v0_1.py --json"
Write-Host "  git diff --check"

if ($Commit) {
    Invoke-Git -Args @("add", "--",
        $checkerPath,
        $publicVerifierPath,
        $receiptPath,
        $advRdValidShapedPath,
        $advRrNearEmptyPath,
        $advRrNoOverreadPath,
        $advUnknownValidPath,
        "docs/CURRENT_PROOF_SURFACE_v0_1.md",
        "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md",
        $scriptPath
    )

    Invoke-Git -Args @("diff", "--cached", "--check")
    Invoke-Git -Args @("commit", "-m", "Harden boundary pressure invalid fixture semantics")

    if ($Push) {
        Invoke-Git -Args @("push")
    }
}

Write-Host ""
Write-Host "Done."