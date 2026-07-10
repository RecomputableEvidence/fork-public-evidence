# scripts/add_longitudinal_day0_lexical_non_authority_limit_adversarial_case_v0_1.ps1
# Adds Day-0 lexical non-authority limit adversarial case.
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

function Write-JsonUtf8Lf {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)]$Object,
        [int]$Depth = 100
    )

    $json = $Object | ConvertTo-Json -Depth $Depth
    Write-Utf8Lf -Path $Path -Content $json
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

function Ensure-VerifierPath {
    param(
        [Parameter(Mandatory = $true)][string]$VerifierPath,
        [Parameter(Mandatory = $true)][string]$PathToRequire
    )

    $verifier = Read-Utf8 -Path $VerifierPath

    if ($verifier -like "*`"$PathToRequire`"*") {
        Write-Host "Verifier already requires: $PathToRequire"
        return
    }

    $line = "    `"$PathToRequire`","

    $anchor = '    "scripts/verify_public_review_package_v0_1.ps1"'
    if ($verifier -like "*$anchor*") {
        $verifier = $verifier.Replace($anchor, "$line`n$anchor")
        Write-Utf8Lf -Path $VerifierPath -Content $verifier
        Write-Host "Inserted verifier required path before verifier-script anchor: $PathToRequire"
        return
    }

    $anchor2 = ")`n`nforeach (`$path in `$requiredPaths)"
    if ($verifier -like "*$anchor2*") {
        $verifier = $verifier.Replace($anchor2, "$line`n)`n`nforeach (`$path in `$requiredPaths)")
        Write-Utf8Lf -Path $VerifierPath -Content $verifier
        Write-Host "Inserted verifier required path before requiredPaths close: $PathToRequire"
        return
    }

    throw "Could not find safe insertion point in $VerifierPath for $PathToRequire"
}

function Ensure-VerifierChecker {
    param([Parameter(Mandatory = $true)][string]$VerifierPath)

    $verifier = Read-Utf8 -Path $VerifierPath

    if ($verifier -like "*checker:longitudinal-day0-adversarial*") {
        Write-Host "Verifier already runs longitudinal Day-0 adversarial checker."
        return
    }

    $checkerBlock = @'

    $day0AdvArgs = @("tools/check_longitudinal_day0_adversarial_cases_v0_1.py", "--json")
    $day0AdvRun = Invoke-External -Name "longitudinal-day0-adversarial" -Command $pythonCommand -Arguments $day0AdvArgs
    $day0AdvPassed = $false
    $day0AdvData = $null

    if ($day0AdvRun.exit_code -eq 0) {
        $day0AdvData = Convert-JsonOutput -Text $day0AdvRun.output -Name "Longitudinal Day-0 adversarial checker"

        $day0AdvPassed = (
            $day0AdvData.failed -eq 0 -and
            $day0AdvData.passed -eq $day0AdvData.total
        )
    }

    [void]$results.Add((New-Result `
        -Name "checker:longitudinal-day0-adversarial" `
        -Passed $day0AdvPassed `
        -Detail "python tools/check_longitudinal_day0_adversarial_cases_v0_1.py --json" `
        -Data $day0AdvData))
'@

    $anchor = "`nif (-not `$SkipGitChecks) {"
    if ($verifier -like "*$anchor*") {
        $verifier = $verifier.Replace($anchor, $checkerBlock + $anchor)
        Write-Utf8Lf -Path $VerifierPath -Content $verifier
        Write-Host "Inserted longitudinal Day-0 adversarial checker into public verifier."
        return
    }

    throw "Could not patch public verifier checker section; git-check anchor not found."
}

Assert-RepoRoot

$scriptPath = "scripts/add_longitudinal_day0_lexical_non_authority_limit_adversarial_case_v0_1.ps1"
$schemaPath = "schemas/longitudinal_day0_adversarial_case_v0_1.schema.json"
$checkerPath = "tools/check_longitudinal_day0_adversarial_cases_v0_1.py"
$verifierPath = "scripts/verify_public_review_package_v0_1.ps1"

$adversarialRoot = "docs/reconstruction/adversarial"
$adversarialReadmePath = "$adversarialRoot/README.md"
$caseDocPath = "$adversarialRoot/LONGITUDINAL_DAY0_LEXICAL_NON_AUTHORITY_LIMIT_ADVERSARIAL_CASE_v0_1.md"
$caseFixturePath = "$adversarialRoot/fixtures/LRT_DAY0_ADV_002_lexical_non_authority_limit_v0_1.json"
$responseReceiptPath = "docs/review/public-rounds/round-005/ROUND005_RESPONSE_LEXICAL_NON_AUTHORITY_LIMIT_ADVERSARIAL_CASE_v0_1.md"

$nonAuthority = "This adversarial case records a lexical boundary-check limitation for the Day-0 checker. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority."

$schema = @'
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://recomputableevidence.example/schemas/longitudinal_day0_adversarial_case_v0_1.schema.json",
  "title": "Fork Longitudinal Day-0 Adversarial Case v0.1",
  "type": "object",
  "additionalProperties": true,
  "required": [
    "case_id",
    "case_family",
    "review_round_source",
    "reviewed_packet",
    "mutation_target",
    "mutation_summary",
    "expected_observation",
    "expected_outcome_codes",
    "non_authority_statement"
  ],
  "properties": {
    "case_id": { "type": "string" },
    "case_family": { "type": "string" },
    "review_round_source": { "type": "string" },
    "reviewed_packet": { "type": "string" },
    "mutation_target": { "type": "string" },
    "mutation_summary": { "type": "string" },
    "expected_observation": { "type": "string" },
    "expected_outcome_codes": {
      "type": "array",
      "items": { "type": "string" }
    },
    "non_authority_statement": { "type": "string" }
  }
}
'@

$checker = @'
#!/usr/bin/env python3
"""
Fork Longitudinal Day-0 Adversarial Cases Checker v0.1.

Currently implements:

- LRT_DAY0_ADV_001_COORDINATED_RESEAL_v0_1
- LRT_DAY0_ADV_002_LEXICAL_NON_AUTHORITY_LIMIT_v0_1

This checker records bounded checker-scope behavior. A pass means the expected
limitation was reproduced, not that the adversarial condition is valid.

It does not validate truth, compliance, legal sufficiency, safety, authorization,
approval, certification, endorsement, validation, production readiness,
procurement approval, or institutional authority.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Dict, List, Tuple


PACKET_ROOT = pathlib.Path("docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1")
DAY0_CHECKER = pathlib.Path("tools/check_longitudinal_reconstruction_day0_packet_v0_1.py")

CASE_RESEAL = "LRT_DAY0_ADV_001_COORDINATED_RESEAL_v0_1"
CASE_LEXICAL = "LRT_DAY0_ADV_002_LEXICAL_NON_AUTHORITY_LIMIT_v0_1"

AUTHORITY_ASSERTING_STATEMENT = (
    "This system does not lack truth, compliance, legal sufficiency, safety, "
    "authorization, approval, certification, endorsement, or production readiness. "
    "Full institutional authority is hereby established and confirmed."
)

REQUIRED_BOUNDARY_TERMS = [
    "does not",
    "truth",
    "compliance",
    "legal",
    "safety",
    "authorization",
    "approval",
    "certification",
    "endorsement",
    "production readiness",
    "authority",
]

RESEAL_OUTCOME_CODES = [
    "MANIFEST_INTERNALLY_CONSISTENT_BUT_UNANCHORED",
    "COORDINATED_RESEAL_CONFIRMED",
    "ROOT_OF_TRUST_SCOPE_LIMIT_CONFIRMED",
    "SEMANTIC_CONTENT_CHANGE_UNDETECTED_AFTER_CONSISTENT_RESEAL",
]

LEXICAL_OUTCOME_CODES = [
    "LEXICAL_BOUNDARY_CHECK_LIMIT_CONFIRMED",
    "NEGATION_AWARENESS_ABSENT",
    "AUTHORITY_ASSERTION_WITH_REQUIRED_TERMS_ACCEPTED",
    "SEMANTIC_NON_AUTHORITY_NOT_ESTABLISHED_BY_KEYWORD_PRESENCE",
]

NON_AUTHORITY_STATEMENT = (
    "This adversarial checker records root-of-trust, lexical boundary-check, and "
    "checker-scope behavior only; it does not validate truth, compliance, legal "
    "sufficiency, safety, authorization, approval, certification, endorsement, "
    "validation, production readiness, procurement approval, or institutional authority."
)


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: pathlib.Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be object")
    return data


def write_json(path: pathlib.Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_day0_checker(repo_root: pathlib.Path, cwd: pathlib.Path) -> Dict[str, Any]:
    checker_path = repo_root / DAY0_CHECKER

    completed = subprocess.run(
        [sys.executable, str(checker_path), "--json"],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    parsed = None
    parse_error = None
    try:
        parsed = json.loads(completed.stdout)
    except Exception as exc:
        parse_error = str(exc)

    return {
        "command": f"{sys.executable} {checker_path} --json",
        "cwd": str(cwd),
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "parsed": parsed,
        "parse_error": parse_error,
    }


def summarize_run(run: Dict[str, Any] | None) -> Dict[str, Any]:
    if not run:
        return {
            "exit_code": None,
            "parsed": None,
            "parse_error": "run missing",
        }

    parsed = run.get("parsed")
    summary = {
        "exit_code": run.get("exit_code"),
        "parse_error": run.get("parse_error"),
    }

    if isinstance(parsed, dict):
        summary.update({
            "checker": parsed.get("checker"),
            "total": parsed.get("total"),
            "passed": parsed.get("passed"),
            "failed": parsed.get("failed"),
        })
    else:
        summary["stdout"] = run.get("stdout")

    return summary


def prepare_scratch_packet(repo_root: pathlib.Path) -> Tuple[pathlib.Path, pathlib.Path]:
    scratch_root = pathlib.Path(tempfile.mkdtemp(prefix="fork_lrt_day0_reseal_"))
    source_packet = repo_root / PACKET_ROOT
    scratch_packet = scratch_root / PACKET_ROOT

    if not source_packet.exists():
        raise FileNotFoundError(f"missing Day-0 packet: {source_packet}")

    scratch_packet.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_packet, scratch_packet)

    return scratch_root, scratch_packet


def mutate_and_reseal(scratch_packet: pathlib.Path) -> Dict[str, Any]:
    receipt_rel = pathlib.Path("receipts/day0_expected_reconstruction_provenance_receipt.json")
    receipt_path = scratch_packet / receipt_rel
    manifest_path = scratch_packet / "packet_manifest.json"
    sidecar_path = scratch_packet / "packet_manifest.sha256"
    outer_receipt_path = scratch_packet / "packet_manifest_outer_receipt.json"

    receipt = load_json(receipt_path)
    original_receipt_hash = sha256_file(receipt_path)

    original_provenance_status = receipt.get("provenance_status")
    original_independence_status = receipt.get("independence_status")

    receipt["provenance_status"] = "independent_external_reviewer_provenance"
    receipt["independence_status"] = "independently_verified_in_v0_1"
    receipt["boundary_note"] = (
        "ADVERSARIAL MUTATION: this scratch-copy value falsely claims independent provenance "
        "to test whether coordinated re-seal is detected by the current Day-0 checker."
    )
    receipt["adversarial_mutation"] = {
        "case_id": CASE_RESEAL,
        "mutation_type": "coordinated_reseal_after_falsified_provenance",
        "not_part_of_clean_packet": True,
    }

    write_json(receipt_path, receipt)
    mutated_receipt_hash = sha256_file(receipt_path)

    manifest = load_json(manifest_path)
    original_manifest_hash = sha256_file(manifest_path)

    artifact_hashes = manifest.get("artifact_hashes", [])
    if not isinstance(artifact_hashes, list):
        raise ValueError("manifest artifact_hashes must be list")

    patched_artifact = False
    for item in artifact_hashes:
        if not isinstance(item, dict):
            continue

        item_path = str(item.get("path", "")).replace("\\", "/")
        if item_path.endswith("receipts/day0_expected_reconstruction_provenance_receipt.json"):
            item["sha256"] = mutated_receipt_hash
            patched_artifact = True

    if not patched_artifact:
        raise ValueError("could not find provenance receipt artifact hash entry in manifest")

    write_json(manifest_path, manifest)
    resealed_manifest_hash = sha256_file(manifest_path)

    sidecar_path.write_text(f"{resealed_manifest_hash}  packet_manifest.json\n", encoding="utf-8")

    outer = load_json(outer_receipt_path)
    original_outer_hash = outer.get("packet_manifest_sha256")
    outer["packet_manifest_sha256"] = resealed_manifest_hash
    outer["adversarial_reseal_note"] = (
        "ADVERSARIAL MUTATION: scratch-copy outer receipt updated to bind the re-sealed manifest."
    )
    write_json(outer_receipt_path, outer)

    return {
        "mutation_target": str(receipt_rel).replace("\\", "/"),
        "original_provenance_status": original_provenance_status,
        "mutated_provenance_status": receipt["provenance_status"],
        "original_independence_status": original_independence_status,
        "mutated_independence_status": receipt["independence_status"],
        "original_receipt_sha256": original_receipt_hash,
        "mutated_receipt_sha256": mutated_receipt_hash,
        "original_manifest_sha256": original_manifest_hash,
        "resealed_manifest_sha256": resealed_manifest_hash,
        "original_outer_receipt_manifest_sha256": original_outer_hash,
        "resealed_outer_receipt_manifest_sha256": outer["packet_manifest_sha256"],
    }


def evaluate_coordinated_reseal(repo_root: pathlib.Path, keep_temp: bool) -> Dict[str, Any]:
    clean_run = run_day0_checker(repo_root=repo_root, cwd=repo_root)

    scratch_root = None
    try:
        scratch_root, scratch_packet = prepare_scratch_packet(repo_root)
        mutation = mutate_and_reseal(scratch_packet)
        resealed_run = run_day0_checker(repo_root=repo_root, cwd=scratch_root)

        clean_parsed = clean_run.get("parsed") or {}
        resealed_parsed = resealed_run.get("parsed") or {}

        clean_ok = (
            clean_run["exit_code"] == 0
            and clean_parsed.get("failed") == 0
            and clean_parsed.get("passed") == clean_parsed.get("total")
        )

        resealed_passes_day0_checker = (
            resealed_run["exit_code"] == 0
            and resealed_parsed.get("failed") == 0
            and resealed_parsed.get("passed") == resealed_parsed.get("total")
        )

        mutation_ok = (
            mutation["original_provenance_status"] == "author_declared_day0_fixture_baseline"
            and mutation["mutated_provenance_status"] == "independent_external_reviewer_provenance"
            and mutation["original_receipt_sha256"] != mutation["mutated_receipt_sha256"]
            and mutation["original_manifest_sha256"] != mutation["resealed_manifest_sha256"]
            and mutation["resealed_manifest_sha256"] == mutation["resealed_outer_receipt_manifest_sha256"]
        )

        passed = clean_ok and mutation_ok and resealed_passes_day0_checker

        return {
            "case_id": CASE_RESEAL,
            "passed": passed,
            "classification": "root_of_trust_limitation_confirmed" if passed else "unexpected_result",
            "expected_observation": "coordinated re-sealed scratch packet remains Day-0-checker-pass under current unanchored internal-consistency checks",
            "actual_observation": "resealed packet passed Day-0 checker" if resealed_passes_day0_checker else "resealed packet did not pass Day-0 checker",
            "outcome_codes": RESEAL_OUTCOME_CODES if passed else ["UNEXPECTED_ADVERSARIAL_RESULT"],
            "clean_day0_checker": summarize_run(clean_run),
            "resealed_day0_checker": summarize_run(resealed_run),
            "mutation": mutation,
            "scratch_root": str(scratch_root) if keep_temp and scratch_root else None,
            "non_authority_statement": NON_AUTHORITY_STATEMENT,
        }
    finally:
        if scratch_root is not None and not keep_temp:
            shutil.rmtree(scratch_root, ignore_errors=True)


def import_day0_checker(repo_root: pathlib.Path) -> Any:
    checker_path = repo_root / DAY0_CHECKER
    spec = importlib.util.spec_from_file_location("fork_day0_checker_module", checker_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"could not import checker from {checker_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalize_boundary_result(result: Any) -> Dict[str, Any]:
    if isinstance(result, bool):
        return {
            "raw_type": "bool",
            "raw_repr": repr(result),
            "terms_satisfied": result,
            "missing_terms": [] if result else ["unknown"],
        }

    if isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], bool):
        missing = result[1]
        if missing is None:
            missing_list: List[str] = []
        elif isinstance(missing, (list, tuple, set)):
            missing_list = [str(item) for item in missing]
        else:
            missing_list = [str(missing)]
        return {
            "raw_type": "tuple_bool_missing",
            "raw_repr": repr(result),
            "terms_satisfied": bool(result[0]) and len(missing_list) == 0,
            "missing_terms": missing_list,
        }

    if isinstance(result, dict):
        missing_value = result.get("missing_terms", result.get("missing", []))
        if missing_value is None:
            missing_list = []
        elif isinstance(missing_value, (list, tuple, set)):
            missing_list = [str(item) for item in missing_value]
        else:
            missing_list = [str(missing_value)]

        if "passed" in result:
            terms_satisfied = bool(result["passed"]) and len(missing_list) == 0
        elif "terms_satisfied" in result:
            terms_satisfied = bool(result["terms_satisfied"]) and len(missing_list) == 0
        else:
            terms_satisfied = len(missing_list) == 0

        return {
            "raw_type": "dict",
            "raw_repr": repr(result),
            "terms_satisfied": terms_satisfied,
            "missing_terms": missing_list,
        }

    if isinstance(result, (list, tuple, set)):
        missing_list = [str(item) for item in result]
        return {
            "raw_type": type(result).__name__,
            "raw_repr": repr(result),
            "terms_satisfied": len(missing_list) == 0,
            "missing_terms": missing_list,
        }

    return {
        "raw_type": type(result).__name__,
        "raw_repr": repr(result),
        "terms_satisfied": False,
        "missing_terms": ["unrecognized has_boundary_terms return type"],
    }


def evaluate_lexical_non_authority_limit(repo_root: pathlib.Path) -> Dict[str, Any]:
    module = import_day0_checker(repo_root)

    if not hasattr(module, "has_boundary_terms"):
        return {
            "case_id": CASE_LEXICAL,
            "passed": False,
            "classification": "day0_checker_function_missing",
            "expected_observation": "authority-asserting text containing all required terms is accepted by lexical boundary-term function",
            "actual_observation": "has_boundary_terms function was not found",
            "outcome_codes": ["DAY0_CHECKER_FUNCTION_MISSING"],
            "authority_asserting_statement": AUTHORITY_ASSERTING_STATEMENT,
            "non_authority_statement": NON_AUTHORITY_STATEMENT,
        }

    fn = getattr(module, "has_boundary_terms")
    result = fn(AUTHORITY_ASSERTING_STATEMENT)
    normalized = normalize_boundary_result(result)

    lower = AUTHORITY_ASSERTING_STATEMENT.lower()
    required_terms_present = [term for term in REQUIRED_BOUNDARY_TERMS if term in lower]
    required_terms_missing_by_direct_scan = [term for term in REQUIRED_BOUNDARY_TERMS if term not in lower]

    authority_assertion_present = (
        "full institutional authority" in lower
        and "established and confirmed" in lower
    )

    lexical_function_accepts_statement = normalized["terms_satisfied"]
    passed = (
        authority_assertion_present
        and not required_terms_missing_by_direct_scan
        and lexical_function_accepts_statement
    )

    return {
        "case_id": CASE_LEXICAL,
        "passed": passed,
        "classification": "lexical_boundary_check_limit_confirmed" if passed else "unexpected_result",
        "expected_observation": "authority-asserting text containing all required boundary terms is accepted by the Day-0 lexical boundary-term function",
        "actual_observation": (
            "authority-asserting text accepted by lexical boundary-term function"
            if lexical_function_accepts_statement
            else "authority-asserting text not accepted by lexical boundary-term function"
        ),
        "outcome_codes": LEXICAL_OUTCOME_CODES if passed else ["UNEXPECTED_LEXICAL_ADVERSARIAL_RESULT"],
        "authority_asserting_statement": AUTHORITY_ASSERTING_STATEMENT,
        "required_terms_present": required_terms_present,
        "required_terms_missing_by_direct_scan": required_terms_missing_by_direct_scan,
        "authority_assertion_present": authority_assertion_present,
        "has_boundary_terms_result": normalized,
        "interpretation": (
            "Keyword presence is not semantic non-authority. This case confirms the current "
            "boundary-term check does not parse negation or authority assertion."
        ),
        "non_authority_statement": NON_AUTHORITY_STATEMENT,
    }


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args(argv)

    repo_root = pathlib.Path(args.repo_root).resolve()

    cases = [
        evaluate_coordinated_reseal(repo_root=repo_root, keep_temp=args.keep_temp),
        evaluate_lexical_non_authority_limit(repo_root=repo_root),
    ]

    failed = sum(1 for case in cases if not case["passed"])

    summary = {
        "checker": "check_longitudinal_day0_adversarial_cases_v0_1.py",
        "total": len(cases),
        "passed": len(cases) - failed,
        "failed": failed,
        "cases": cases,
        "non_authority_statement": NON_AUTHORITY_STATEMENT,
    }

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"Longitudinal Day-0 adversarial cases: {summary['passed']}/{summary['total']} passed")
        for case in cases:
            status = "PASS" if case["passed"] else "FAIL"
            print(f"{status} {case['case_id']}: {case['actual_observation']}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
'@

$caseDoc = @'
# Longitudinal Day-0 Lexical Non-Authority Limit Adversarial Case v0.1

Status: Adversarial case.
Case ID: `LRT_DAY0_ADV_002_LEXICAL_NON_AUTHORITY_LIMIT_v0_1`
Source: Public Review Round 005.

## 1. Purpose

This case converts the Round 005 lexical non-authority finding into a reproducible adversarial check.

The case asks:

Can a sentence contain all required non-authority boundary terms while still asserting institutional authority?

## 2. Expected current observation

Under the current v0.1 Day-0 checker, the boundary-term function is lexical.

It checks whether required terms are present.

It does not parse semantic meaning, negation, or whether the sentence actually disclaims authority.

## 3. Adversarial statement

The adversarial checker tests this statement:

> This system does not lack truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, or production readiness. Full institutional authority is hereby established and confirmed.

The statement contains the required lexical terms while asserting authority.

## 4. Expected outcome codes

- `LEXICAL_BOUNDARY_CHECK_LIMIT_CONFIRMED`
- `NEGATION_AWARENESS_ABSENT`
- `AUTHORITY_ASSERTION_WITH_REQUIRED_TERMS_ACCEPTED`
- `SEMANTIC_NON_AUTHORITY_NOT_ESTABLISHED_BY_KEYWORD_PRESENCE`

## 5. Non-claim

This case does not show that the clean Day-0 packet asserts authority.

It shows that the current v0.1 lexical boundary-term check should not be overread as semantic non-authority verification.

## 6. Run command

From repository root:

- `python tools/check_longitudinal_day0_adversarial_cases_v0_1.py --json`

## 7. Boundary statement

This case records checker-scope behavior only. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority.
'@

$responseReceipt = @'
# Round 005 Response: Lexical Non-Authority Limit Adversarial Case v0.1

Status: Engineering response receipt.
Round: Public Review Round 005.
Response class: Adversarial case filing.

## 1. Finding addressed

Round 005 demonstrated that the Day-0 checker’s non-authority language check is lexical, not semantic or negation-aware.

A sentence can contain all required boundary terms while asserting authority.

This response preserves that finding as a reproducible adversarial case.

## 2. Added artifacts

- `docs/reconstruction/adversarial/LONGITUDINAL_DAY0_LEXICAL_NON_AUTHORITY_LIMIT_ADVERSARIAL_CASE_v0_1.md`
- `docs/reconstruction/adversarial/fixtures/LRT_DAY0_ADV_002_lexical_non_authority_limit_v0_1.json`
- updated `tools/check_longitudinal_day0_adversarial_cases_v0_1.py`

## 3. Interpretation

A pass in this adversarial checker means:

- the adversarial sentence contains all required boundary terms;
- the Day-0 checker’s lexical boundary-term function accepts the sentence;
- the sentence nevertheless asserts institutional authority;
- therefore, keyword presence must not be overread as semantic non-authority verification.

It does not mean the clean Day-0 packet asserts authority.

## 4. Current limitation preserved

The Day-0 checker’s boundary-language check verifies term presence.

It does not verify semantic negation, legal meaning, institutional effect, authorization posture, or actual non-authority.

## 5. Future response options

Future work may add:

- explicit semantic-boundary review cases;
- deny-list detection for authority assertion language;
- structured non-claim fields instead of prose-only term checks;
- reviewer-facing warnings that lexical checks are not semantic verification.

## 6. Non-authority statement

This response records a lexical checker-scope limitation. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority.
'@

$caseFixture = [ordered]@{
    case_id = "LRT_DAY0_ADV_002_LEXICAL_NON_AUTHORITY_LIMIT_v0_1"
    case_family = "longitudinal_day0_lexical_non_authority_limit"
    review_round_source = "public_review_round_005_longitudinal_day0_packet_accessibility_reconstruction_boundary_replay_readiness"
    reviewed_packet = "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/"
    mutation_target = "non_authority_statement_text"
    mutation_summary = "Construct an authority-asserting sentence that contains all required Day-0 boundary terms and run it through the Day-0 checker lexical boundary-term function."
    adversarial_statement = "This system does not lack truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, or production readiness. Full institutional authority is hereby established and confirmed."
    expected_observation = "The lexical boundary-term function accepts the authority-asserting sentence because all required terms are present, confirming keyword presence is not semantic non-authority verification."
    expected_outcome_codes = @(
        "LEXICAL_BOUNDARY_CHECK_LIMIT_CONFIRMED",
        "NEGATION_AWARENESS_ABSENT",
        "AUTHORITY_ASSERTION_WITH_REQUIRED_TERMS_ACCEPTED",
        "SEMANTIC_NON_AUTHORITY_NOT_ESTABLISHED_BY_KEYWORD_PRESENCE"
    )
    expected_suite_result = [ordered]@{
        suite_passes_when_limitation_reproduced = $true
        lexical_terms_expected_missing = 0
        semantic_non_authority_expected = $false
    }
    non_authority_statement = $nonAuthority
}

Write-Utf8Lf -Path $schemaPath -Content $schema
Write-Utf8Lf -Path $checkerPath -Content $checker
Write-Utf8Lf -Path $caseDocPath -Content $caseDoc
Write-Utf8Lf -Path $responseReceiptPath -Content $responseReceipt
Write-JsonUtf8Lf -Path $caseFixturePath -Object $caseFixture

if (-not (Test-Path $adversarialReadmePath)) {
    $baseReadme = @'
# Longitudinal Reconstruction Adversarial Cases

Status: Adversarial reconstruction test surface.

This directory contains adversarial cases for the Longitudinal Reconstruction Trial.

These cases are not claims that Fork is false or true. They record bounded checker-scope behavior and limitations.

## Checker

Run from repository root:

- `python tools/check_longitudinal_day0_adversarial_cases_v0_1.py --json`

## Boundary

These cases do not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority.
'@
    Write-Utf8Lf -Path $adversarialReadmePath -Content $baseReadme
}

$adversarialReadmeBlock = @'
## Lexical non-authority limit

- `LONGITUDINAL_DAY0_LEXICAL_NON_AUTHORITY_LIMIT_ADVERSARIAL_CASE_v0_1.md`
- `fixtures/LRT_DAY0_ADV_002_lexical_non_authority_limit_v0_1.json`

This case confirms that keyword presence is not semantic non-authority verification.
'@

$lexicalRoutingBlock = @'
## Longitudinal Day-0 lexical non-authority limit adversarial case

Round 005 found that the Day-0 non-authority check is lexical, not semantic or negation-aware.

This finding is now preserved as a reproducible adversarial case:

- `docs/reconstruction/adversarial/LONGITUDINAL_DAY0_LEXICAL_NON_AUTHORITY_LIMIT_ADVERSARIAL_CASE_v0_1.md`
- `docs/reconstruction/adversarial/fixtures/LRT_DAY0_ADV_002_lexical_non_authority_limit_v0_1.json`
- `tools/check_longitudinal_day0_adversarial_cases_v0_1.py`

Run:

- `python tools/check_longitudinal_day0_adversarial_cases_v0_1.py --json`

Interpretation:

- a pass confirms the lexical limit is reproducible under the current v0.1 checker;
- it does not mean the clean Day-0 packet asserts authority;
- it does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority.
'@

$indexBlock = @'
## Longitudinal Day-0 lexical non-authority limit

Adversarial case:

- `docs/reconstruction/adversarial/LONGITUDINAL_DAY0_LEXICAL_NON_AUTHORITY_LIMIT_ADVERSARIAL_CASE_v0_1.md`

Fixture:

- `docs/reconstruction/adversarial/fixtures/LRT_DAY0_ADV_002_lexical_non_authority_limit_v0_1.json`

Checker:

- `tools/check_longitudinal_day0_adversarial_cases_v0_1.py`

Run:

- `python tools/check_longitudinal_day0_adversarial_cases_v0_1.py --json`
'@

$round005Block = @'
## Round 005 response: lexical non-authority limit adversarial case

The lexical non-authority finding from Round 005 is now preserved as a reproducible adversarial case.

Response receipt:

- `docs/review/public-rounds/round-005/ROUND005_RESPONSE_LEXICAL_NON_AUTHORITY_LIMIT_ADVERSARIAL_CASE_v0_1.md`

Case:

- `docs/reconstruction/adversarial/LONGITUDINAL_DAY0_LEXICAL_NON_AUTHORITY_LIMIT_ADVERSARIAL_CASE_v0_1.md`

Checker:

- `python tools/check_longitudinal_day0_adversarial_cases_v0_1.py --json`

This response records a lexical checker limitation. It does not mean the clean Day-0 packet asserts authority.
'@

Replace-OrAppendBlock -Path $adversarialReadmePath -BlockId "FORK_LONGITUDINAL_DAY0_LEXICAL_NON_AUTHORITY_LIMIT" -Content $adversarialReadmeBlock
Replace-OrAppendBlock -Path "README.md" -BlockId "FORK_LONGITUDINAL_DAY0_LEXICAL_NON_AUTHORITY_LIMIT" -Content $lexicalRoutingBlock
Replace-OrAppendBlock -Path "docs/CURRENT_PROOF_SURFACE_v0_1.md" -BlockId "FORK_LONGITUDINAL_DAY0_LEXICAL_NON_AUTHORITY_LIMIT" -Content $lexicalRoutingBlock
Replace-OrAppendBlock -Path "docs/REVIEWER_START_HERE_v0_1.md" -BlockId "FORK_LONGITUDINAL_DAY0_LEXICAL_NON_AUTHORITY_LIMIT" -Content $lexicalRoutingBlock
Replace-OrAppendBlock -Path "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md" -BlockId "FORK_LONGITUDINAL_DAY0_LEXICAL_NON_AUTHORITY_LIMIT" -Content $indexBlock
Replace-OrAppendBlock -Path "docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md" -BlockId "FORK_LONGITUDINAL_DAY0_LEXICAL_NON_AUTHORITY_LIMIT" -Content $lexicalRoutingBlock
Replace-OrAppendBlock -Path "docs/review/public-rounds/round-005/README.md" -BlockId "FORK_ROUND005_LEXICAL_NON_AUTHORITY_LIMIT_RESPONSE" -Content $round005Block
Replace-OrAppendBlock -Path "docs/review/public-rounds/round-005/PUBLIC_REVIEW_ROUND_005_SYNTHESIS_v0_1.md" -BlockId "FORK_ROUND005_LEXICAL_NON_AUTHORITY_LIMIT_RESPONSE" -Content $round005Block

Ensure-VerifierPath -VerifierPath $verifierPath -PathToRequire "docs/reconstruction/adversarial/LONGITUDINAL_DAY0_LEXICAL_NON_AUTHORITY_LIMIT_ADVERSARIAL_CASE_v0_1.md"
Ensure-VerifierPath -VerifierPath $verifierPath -PathToRequire "docs/reconstruction/adversarial/fixtures/LRT_DAY0_ADV_002_lexical_non_authority_limit_v0_1.json"
Ensure-VerifierPath -VerifierPath $verifierPath -PathToRequire "docs/review/public-rounds/round-005/ROUND005_RESPONSE_LEXICAL_NON_AUTHORITY_LIMIT_ADVERSARIAL_CASE_v0_1.md"
Ensure-VerifierPath -VerifierPath $verifierPath -PathToRequire "schemas/longitudinal_day0_adversarial_case_v0_1.schema.json"
Ensure-VerifierPath -VerifierPath $verifierPath -PathToRequire "tools/check_longitudinal_day0_adversarial_cases_v0_1.py"
Ensure-VerifierChecker -VerifierPath $verifierPath

Write-Host ""
Write-Host "Running longitudinal Day-0 adversarial checker..."
Invoke-Python -Args @($checkerPath, "--json")

Write-Host ""
Write-Host "Running Day-0 checker..."
Invoke-Python -Args @("tools/check_longitudinal_reconstruction_day0_packet_v0_1.py", "--json")

Write-Host ""
Write-Host "Running public verifier..."
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    throw "Public review verifier failed."
}

Write-Host ""
Write-Host "Running Round 005 checker..."
Invoke-Python -Args @("tools/check_public_review_round_005_interactions_v0_1.py", "--json")

Write-Host ""
Write-Host "Running boundary-pressure checker with adversarial regression..."
Invoke-Python -Args @("tools/check_boundary_pressure_review_cases_v0_1.py", "--json", "--run-adversarial")

Write-Host ""
Write-Host "Running Round 004 checker..."
Invoke-Python -Args @("tools/check_public_review_round_004_interactions_v0_1.py", "--json")

Write-Host ""
Write-Host "Running whitespace check..."
Invoke-Git -Args @("diff", "--check")

Write-Host ""
Write-Host "Changed files:"
git status --short

Write-Host ""
Write-Host "Review commands:"
Write-Host "  git diff -- docs\reconstruction\adversarial"
Write-Host "  git diff -- tools\check_longitudinal_day0_adversarial_cases_v0_1.py"
Write-Host "  git diff -- scripts\verify_public_review_package_v0_1.ps1"
Write-Host "  python tools\check_longitudinal_day0_adversarial_cases_v0_1.py --json"
Write-Host "  python tools\check_longitudinal_reconstruction_day0_packet_v0_1.py --json"
Write-Host "  powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1"
Write-Host "  git diff --check"

if ($Commit) {
    Invoke-Git -Args @("add", "--",
        $scriptPath,
        $schemaPath,
        $checkerPath,
        $adversarialReadmePath,
        $caseDocPath,
        $caseFixturePath,
        $responseReceiptPath,
        "README.md",
        "docs/CURRENT_PROOF_SURFACE_v0_1.md",
        "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md",
        "docs/REVIEWER_START_HERE_v0_1.md",
        "docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md",
        "docs/review/public-rounds/round-005/README.md",
        "docs/review/public-rounds/round-005/PUBLIC_REVIEW_ROUND_005_SYNTHESIS_v0_1.md",
        $verifierPath
    )

    Invoke-Git -Args @("diff", "--cached", "--check")
    Invoke-Git -Args @("commit", "-m", "Add lexical non-authority limit adversarial case")

    if ($Push) {
        Invoke-Git -Args @("push")
    }
}

Write-Host ""
Write-Host "Done."