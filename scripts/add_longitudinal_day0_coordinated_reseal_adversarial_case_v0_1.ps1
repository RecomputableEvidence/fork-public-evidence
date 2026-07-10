# scripts/add_longitudinal_day0_coordinated_reseal_adversarial_case_v0_1.ps1
# Adds Day-0 coordinated re-seal adversarial case.
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

$scriptPath = "scripts/add_longitudinal_day0_coordinated_reseal_adversarial_case_v0_1.ps1"
$schemaPath = "schemas/longitudinal_day0_adversarial_case_v0_1.schema.json"
$checkerPath = "tools/check_longitudinal_day0_adversarial_cases_v0_1.py"
$verifierPath = "scripts/verify_public_review_package_v0_1.ps1"

$adversarialRoot = "docs/reconstruction/adversarial"
$adversarialReadmePath = "$adversarialRoot/README.md"
$caseDocPath = "$adversarialRoot/LONGITUDINAL_DAY0_COORDINATED_RESEAL_ADVERSARIAL_CASE_v0_1.md"
$caseFixturePath = "$adversarialRoot/fixtures/LRT_DAY0_ADV_001_coordinated_reseal_v0_1.json"
$responseReceiptPath = "docs/review/public-rounds/round-005/ROUND005_RESPONSE_COORDINATED_RESEAL_ADVERSARIAL_CASE_v0_1.md"

$nonAuthority = "This adversarial case records a root-of-trust limitation for the Day-0 packet checker. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority."

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

The checker copies the Day-0 packet into a disposable temporary repository-shaped
directory, falsifies the expected reconstruction provenance receipt, recomputes
that receipt hash into packet_manifest.json, recomputes packet_manifest.sha256,
updates packet_manifest_outer_receipt.json, and then runs the unmodified Day-0
checker against the disposable copy.

Expected current observation:

- the re-sealed scratch packet still passes the Day-0 checker.

This confirms a bounded root-of-trust limitation: the Day-0 checker verifies
internal consistency relative to the current manifest and outer receipt; it does
not distinguish original sealing from coordinated re-sealing without an external
anchor.

This checker does not validate truth, compliance, legal sufficiency, safety,
authorization, approval, certification, endorsement, validation, production
readiness, procurement approval, or institutional authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Dict, List, Tuple


PACKET_ROOT = pathlib.Path("docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1")
DAY0_CHECKER = pathlib.Path("tools/check_longitudinal_reconstruction_day0_packet_v0_1.py")
CASE_ID = "LRT_DAY0_ADV_001_COORDINATED_RESEAL_v0_1"

OUTCOME_CODES = [
    "MANIFEST_INTERNALLY_CONSISTENT_BUT_UNANCHORED",
    "COORDINATED_RESEAL_CONFIRMED",
    "ROOT_OF_TRUST_SCOPE_LIMIT_CONFIRMED",
    "SEMANTIC_CONTENT_CHANGE_UNDETECTED_AFTER_CONSISTENT_RESEAL",
]

NON_AUTHORITY_STATEMENT = (
    "This adversarial checker records root-of-trust and checker-scope behavior only; "
    "it does not validate truth, compliance, legal sufficiency, safety, authorization, "
    "approval, certification, endorsement, validation, production readiness, "
    "procurement approval, or institutional authority."
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
    except Exception as exc:  # pragma: no cover - diagnostic branch
        parse_error = str(exc)

    return {
        "command": f"{sys.executable} {checker_path} --json",
        "cwd": str(cwd),
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "parsed": parsed,
        "parse_error": parse_error,
    }


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
        "case_id": CASE_ID,
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


def evaluate_case(repo_root: pathlib.Path, keep_temp: bool) -> Dict[str, Any]:
    clean_run = run_day0_checker(repo_root=repo_root, cwd=repo_root)

    scratch_root = None
    scratch_packet = None
    mutation = None
    resealed_run = None

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
            "case_id": CASE_ID,
            "passed": passed,
            "classification": "root_of_trust_limitation_confirmed" if passed else "unexpected_result",
            "expected_observation": "coordinated re-sealed scratch packet remains Day-0-checker-pass under current unanchored internal-consistency checks",
            "actual_observation": "resealed packet passed Day-0 checker" if resealed_passes_day0_checker else "resealed packet did not pass Day-0 checker",
            "outcome_codes": OUTCOME_CODES if passed else ["UNEXPECTED_ADVERSARIAL_RESULT"],
            "clean_day0_checker": summarize_run(clean_run),
            "resealed_day0_checker": summarize_run(resealed_run),
            "mutation": mutation,
            "scratch_root": str(scratch_root) if keep_temp and scratch_root else None,
            "non_authority_statement": NON_AUTHORITY_STATEMENT,
        }
    finally:
        if scratch_root is not None and not keep_temp:
            shutil.rmtree(scratch_root, ignore_errors=True)


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


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args(argv)

    repo_root = pathlib.Path(args.repo_root).resolve()

    cases = [evaluate_case(repo_root=repo_root, keep_temp=args.keep_temp)]
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

$adversarialReadme = @'
# Longitudinal Reconstruction Adversarial Cases

Status: Adversarial reconstruction test surface.

This directory contains adversarial cases for the Longitudinal Reconstruction Trial.

These cases are not claims that Fork is false or true. They record bounded checker-scope behavior and root-of-trust limitations.

## Cases

- `LONGITUDINAL_DAY0_COORDINATED_RESEAL_ADVERSARIAL_CASE_v0_1.md`
- `fixtures/LRT_DAY0_ADV_001_coordinated_reseal_v0_1.json`

## Checker

Run from repository root:

- `python tools/check_longitudinal_day0_adversarial_cases_v0_1.py --json`

## Boundary

These cases do not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority.
'@

$caseDoc = @'
# Longitudinal Day-0 Coordinated Re-Seal Adversarial Case v0.1

Status: Adversarial case.
Case ID: `LRT_DAY0_ADV_001_COORDINATED_RESEAL_v0_1`
Source: Public Review Round 005.

## 1. Purpose

This case converts the Round 005 coordinated re-seal finding into a reproducible adversarial check.

The case asks:

Can the Day-0 checker distinguish an originally sealed packet from a scratch-copy packet whose provenance receipt was falsified and then consistently re-sealed by recomputing the receipt hash, packet manifest, manifest sidecar, and outer receipt?

## 2. Expected current observation

Under the current v0.1 Day-0 checker, the coordinated re-sealed scratch packet is expected to pass.

That is not treated as validation.

It is treated as a confirmed root-of-trust limitation:

- the Day-0 checker verifies internal consistency relative to the current manifest and outer receipt;
- it does not verify an external original-sealing anchor;
- therefore, a party able to alter the packet and recompute all internal bindings can produce a self-consistent packet that still passes.

## 3. Mutation performed in disposable scratch copy

The adversarial checker:

1. Copies `docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/` into a temporary repository-shaped directory.
2. Edits `receipts/day0_expected_reconstruction_provenance_receipt.json`.
3. Changes provenance from author-declared baseline to independent external reviewer provenance.
4. Recomputes that receipt's SHA-256.
5. Patches the new receipt hash into `packet_manifest.json`.
6. Recomputes `packet_manifest.json`.
7. Patches the new manifest hash into `packet_manifest.sha256`.
8. Patches the new manifest hash into `packet_manifest_outer_receipt.json`.
9. Runs the unmodified Day-0 checker against the scratch copy.

## 4. Expected outcome codes

- `MANIFEST_INTERNALLY_CONSISTENT_BUT_UNANCHORED`
- `COORDINATED_RESEAL_CONFIRMED`
- `ROOT_OF_TRUST_SCOPE_LIMIT_CONFIRMED`
- `SEMANTIC_CONTENT_CHANGE_UNDETECTED_AFTER_CONSISTENT_RESEAL`

## 5. Non-claim

This adversarial case does not show that the clean Day-0 packet was altered.

It shows that the current v0.1 checker does not distinguish clean original sealing from coordinated re-sealing unless an external root of trust exists.

## 6. Run command

From repository root:

- `python tools/check_longitudinal_day0_adversarial_cases_v0_1.py --json`

## 7. Boundary statement

This case records checker-scope behavior only. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority.
'@

$responseReceipt = @'
# Round 005 Response: Coordinated Re-Seal Adversarial Case v0.1

Status: Engineering response receipt.
Round: Public Review Round 005.
Response class: Adversarial case filing.

## 1. Finding addressed

Round 005 demonstrated that a coordinated re-seal could falsify expected reconstruction provenance, recompute the mutated receipt hash into the manifest, recompute the manifest sidecar and outer receipt, and still pass the current Day-0 checker.

This response preserves that finding as a reproducible adversarial case.

## 2. Added artifacts

- `docs/reconstruction/adversarial/README.md`
- `docs/reconstruction/adversarial/LONGITUDINAL_DAY0_COORDINATED_RESEAL_ADVERSARIAL_CASE_v0_1.md`
- `docs/reconstruction/adversarial/fixtures/LRT_DAY0_ADV_001_coordinated_reseal_v0_1.json`
- `schemas/longitudinal_day0_adversarial_case_v0_1.schema.json`
- `tools/check_longitudinal_day0_adversarial_cases_v0_1.py`

## 3. Interpretation

A pass in this adversarial checker means:

- the clean Day-0 packet still passes;
- the checker successfully created a scratch-copy coordinated re-seal;
- the unmodified Day-0 checker still accepted the re-sealed scratch copy;
- the root-of-trust limitation is therefore reproduced.

It does not mean the adversarially mutated packet is valid, truthful, compliant, authorized, approved, certified, endorsed, safe, production-ready, or institutionally authoritative.

## 4. Current limitation preserved

The Day-0 checker verifies internal consistency and byte continuity relative to the current manifest and outer receipt.

It does not verify an external original-sealing anchor.

## 5. Future response options

Future work may add:

- external anchoring;
- signed release evidence;
- transparency-log anchoring;
- pinned manifest hash outside the packet;
- checker behavior that classifies coordinated re-seal as a separate condition.

## 6. Non-authority statement

This response records an adversarial checker-scope limitation. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority.
'@

$caseFixture = [ordered]@{
    case_id = "LRT_DAY0_ADV_001_COORDINATED_RESEAL_v0_1"
    case_family = "longitudinal_day0_coordinated_reseal"
    review_round_source = "public_review_round_005_longitudinal_day0_packet_accessibility_reconstruction_boundary_replay_readiness"
    reviewed_packet = "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/"
    mutation_target = "receipts/day0_expected_reconstruction_provenance_receipt.json"
    mutation_summary = "Falsify provenance to independent external reviewer provenance, recompute target receipt hash into packet_manifest.json, recompute packet_manifest.sha256, and update packet_manifest_outer_receipt.json."
    expected_observation = "The re-sealed scratch packet remains accepted by the current Day-0 checker because the checker verifies internal consistency relative to the current manifest rather than an external original-sealing anchor."
    expected_outcome_codes = @(
        "MANIFEST_INTERNALLY_CONSISTENT_BUT_UNANCHORED",
        "COORDINATED_RESEAL_CONFIRMED",
        "ROOT_OF_TRUST_SCOPE_LIMIT_CONFIRMED",
        "SEMANTIC_CONTENT_CHANGE_UNDETECTED_AFTER_CONSISTENT_RESEAL"
    )
    expected_suite_result = [ordered]@{
        suite_passes_when_limitation_reproduced = $true
        clean_packet_day0_checker_expected_failed = 0
        resealed_scratch_packet_day0_checker_expected_failed = 0
    }
    non_authority_statement = $nonAuthority
}

Write-Utf8Lf -Path $schemaPath -Content $schema
Write-Utf8Lf -Path $checkerPath -Content $checker
Write-Utf8Lf -Path $adversarialReadmePath -Content $adversarialReadme
Write-Utf8Lf -Path $caseDocPath -Content $caseDoc
Write-Utf8Lf -Path $responseReceiptPath -Content $responseReceipt
Write-JsonUtf8Lf -Path $caseFixturePath -Object $caseFixture

$adversarialRoutingBlock = @'
## Longitudinal Day-0 coordinated re-seal adversarial case

Round 005 found that coordinated re-sealing could falsify provenance, recompute internal hashes, and still pass the current Day-0 checker.

This finding is now preserved as a reproducible adversarial case:

- `docs/reconstruction/adversarial/LONGITUDINAL_DAY0_COORDINATED_RESEAL_ADVERSARIAL_CASE_v0_1.md`
- `docs/reconstruction/adversarial/fixtures/LRT_DAY0_ADV_001_coordinated_reseal_v0_1.json`
- `tools/check_longitudinal_day0_adversarial_cases_v0_1.py`

Run:

- `python tools/check_longitudinal_day0_adversarial_cases_v0_1.py --json`

Interpretation:

- a pass confirms the root-of-trust limitation is reproducible under the current v0.1 checker;
- it does not validate the mutated packet;
- it does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority.
'@

$indexBlock = @'
## Longitudinal Day-0 adversarial cases

Adversarial reconstruction surface:

- `docs/reconstruction/adversarial/README.md`

Coordinated re-seal case:

- `docs/reconstruction/adversarial/LONGITUDINAL_DAY0_COORDINATED_RESEAL_ADVERSARIAL_CASE_v0_1.md`

Checker:

- `tools/check_longitudinal_day0_adversarial_cases_v0_1.py`

Run:

- `python tools/check_longitudinal_day0_adversarial_cases_v0_1.py --json`
'@

$round005Block = @'
## Round 005 response: coordinated re-seal adversarial case

The coordinated re-seal finding from Round 005 is now preserved as a reproducible adversarial case.

Response receipt:

- `docs/review/public-rounds/round-005/ROUND005_RESPONSE_COORDINATED_RESEAL_ADVERSARIAL_CASE_v0_1.md`

Case:

- `docs/reconstruction/adversarial/LONGITUDINAL_DAY0_COORDINATED_RESEAL_ADVERSARIAL_CASE_v0_1.md`

Checker:

- `python tools/check_longitudinal_day0_adversarial_cases_v0_1.py --json`

This response records a root-of-trust limitation. It does not validate the adversarially mutated packet.
'@

Replace-OrAppendBlock -Path "README.md" -BlockId "FORK_LONGITUDINAL_DAY0_COORDINATED_RESEAL_ADVERSARIAL" -Content $adversarialRoutingBlock
Replace-OrAppendBlock -Path "docs/CURRENT_PROOF_SURFACE_v0_1.md" -BlockId "FORK_LONGITUDINAL_DAY0_COORDINATED_RESEAL_ADVERSARIAL" -Content $adversarialRoutingBlock
Replace-OrAppendBlock -Path "docs/REVIEWER_START_HERE_v0_1.md" -BlockId "FORK_LONGITUDINAL_DAY0_COORDINATED_RESEAL_ADVERSARIAL" -Content $adversarialRoutingBlock
Replace-OrAppendBlock -Path "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md" -BlockId "FORK_LONGITUDINAL_DAY0_ADVERSARIAL_CASES" -Content $indexBlock
Replace-OrAppendBlock -Path "docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md" -BlockId "FORK_LONGITUDINAL_DAY0_COORDINATED_RESEAL_ADVERSARIAL" -Content $adversarialRoutingBlock
Replace-OrAppendBlock -Path "docs/review/public-rounds/round-005/README.md" -BlockId "FORK_ROUND005_COORDINATED_RESEAL_RESPONSE" -Content $round005Block
Replace-OrAppendBlock -Path "docs/review/public-rounds/round-005/PUBLIC_REVIEW_ROUND_005_SYNTHESIS_v0_1.md" -BlockId "FORK_ROUND005_COORDINATED_RESEAL_RESPONSE" -Content $round005Block

Ensure-VerifierPath -VerifierPath $verifierPath -PathToRequire "docs/reconstruction/adversarial/README.md"
Ensure-VerifierPath -VerifierPath $verifierPath -PathToRequire "docs/reconstruction/adversarial/LONGITUDINAL_DAY0_COORDINATED_RESEAL_ADVERSARIAL_CASE_v0_1.md"
Ensure-VerifierPath -VerifierPath $verifierPath -PathToRequire "docs/reconstruction/adversarial/fixtures/LRT_DAY0_ADV_001_coordinated_reseal_v0_1.json"
Ensure-VerifierPath -VerifierPath $verifierPath -PathToRequire "schemas/longitudinal_day0_adversarial_case_v0_1.schema.json"
Ensure-VerifierPath -VerifierPath $verifierPath -PathToRequire "tools/check_longitudinal_day0_adversarial_cases_v0_1.py"
Ensure-VerifierPath -VerifierPath $verifierPath -PathToRequire "docs/review/public-rounds/round-005/ROUND005_RESPONSE_COORDINATED_RESEAL_ADVERSARIAL_CASE_v0_1.md"

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
    Invoke-Git -Args @("commit", "-m", "Add Day-0 coordinated re-seal adversarial case")

    if ($Push) {
        Invoke-Git -Args @("push")
    }
}

Write-Host ""
Write-Host "Done."