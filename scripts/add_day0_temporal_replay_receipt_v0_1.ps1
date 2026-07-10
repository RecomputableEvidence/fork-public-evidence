# scripts/add_day0_temporal_replay_receipt_v0_1.ps1
# Adds Longitudinal Reconstruction Day-0 temporal replay receipt.
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

function Invoke-GitCapture {
    param([Parameter(Mandatory = $true)][string[]]$Args)

    $out = & git @Args
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Args -join ' ') failed with exit code $LASTEXITCODE"
    }
    return ($out -join "`n").Trim()
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

function Invoke-PythonCapture {
    param(
        [Parameter(Mandatory = $true)][string]$WorkingDirectory,
        [Parameter(Mandatory = $true)][string[]]$Args
    )

    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        $python = Get-Command py -ErrorAction SilentlyContinue
    }
    if (-not $python) {
        throw "Python was not found on PATH."
    }

    Push-Location $WorkingDirectory
    try {
        $output = & $python.Source @Args 2>&1
        $exit = $LASTEXITCODE
    } finally {
        Pop-Location
    }

    return [ordered]@{
        command = "$($python.Source) $($Args -join ' ')"
        exit_code = $exit
        output = ($output -join "`n")
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

    if ($verifier -like "*checker:longitudinal-day0-temporal-replay*") {
        Write-Host "Verifier already runs longitudinal Day-0 temporal replay checker."
        return
    }

    $checkerBlock = @'

    $day0ReplayArgs = @("tools/check_longitudinal_day0_temporal_replay_receipt_v0_1.py", "--json")
    $day0ReplayRun = Invoke-External -Name "longitudinal-day0-temporal-replay" -Command $pythonCommand -Arguments $day0ReplayArgs
    $day0ReplayPassed = $false
    $day0ReplayData = $null

    if ($day0ReplayRun.exit_code -eq 0) {
        $day0ReplayData = Convert-JsonOutput -Text $day0ReplayRun.output -Name "Longitudinal Day-0 temporal replay checker"

        $day0ReplayPassed = (
            $day0ReplayData.failed -eq 0 -and
            $day0ReplayData.passed -eq $day0ReplayData.total
        )
    }

    [void]$results.Add((New-Result `
        -Name "checker:longitudinal-day0-temporal-replay" `
        -Passed $day0ReplayPassed `
        -Detail "python tools/check_longitudinal_day0_temporal_replay_receipt_v0_1.py --json" `
        -Data $day0ReplayData))
'@

    $anchor = "`nif (-not `$SkipGitChecks) {"
    if ($verifier -like "*$anchor*") {
        $verifier = $verifier.Replace($anchor, $checkerBlock + $anchor)
        Write-Utf8Lf -Path $VerifierPath -Content $verifier
        Write-Host "Inserted longitudinal Day-0 temporal replay checker into public verifier."
        return
    }

    throw "Could not patch public verifier checker section; git-check anchor not found."
}

function Get-Sha256 {
    param([Parameter(Mandatory = $true)][string]$Path)

    return (Get-FileHash -Algorithm SHA256 -Path $Path).Hash.ToLowerInvariant()
}

function ConvertTo-ForwardSlash {
    param([Parameter(Mandatory = $true)][string]$Path)
    return ($Path -replace "\\", "/")
}

Assert-RepoRoot

$scriptPath = "scripts/add_day0_temporal_replay_receipt_v0_1.ps1"
$schemaPath = "schemas/longitudinal_day0_temporal_replay_receipt_v0_1.schema.json"
$checkerPath = "tools/check_longitudinal_day0_temporal_replay_receipt_v0_1.py"
$verifierPath = "scripts/verify_public_review_package_v0_1.ps1"

$replayRoot = "docs/reconstruction/longitudinal/day0/replay"
$replayReadmePath = "$replayRoot/README.md"
$replayReceiptPath = "$replayRoot/DAY0_TEMPORAL_REPLAY_RECEIPT_v0_1.json"
$replayInterpretationPath = "$replayRoot/DAY0_TEMPORAL_REPLAY_RECEIPT_INTERPRETATION_v0_1.md"
$responseReceiptPath = "docs/review/public-rounds/round-005/ROUND005_RESPONSE_DAY0_TEMPORAL_REPLAY_RECEIPT_v0_1.md"

$packetManifestRel = "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/packet_manifest.json"
$packetSidecarRel = "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/packet_manifest.sha256"
$outerReceiptRel = "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/packet_manifest_outer_receipt.json"
$day0CheckerRel = "tools/check_longitudinal_reconstruction_day0_packet_v0_1.py"

$subjectCommit = Invoke-GitCapture -Args @("rev-parse", "HEAD")
$subjectShort = Invoke-GitCapture -Args @("rev-parse", "--short", "HEAD")
$currentBranch = Invoke-GitCapture -Args @("branch", "--show-current")
$gitStatusBefore = Invoke-GitCapture -Args @("status", "--short")
$generatedAtUtc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffffffZ")

$tempBase = [System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), "fork_day0_replay_" + [Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $tempBase -Force | Out-Null

$worktreePath = [System.IO.Path]::Combine($tempBase, "subject_worktree")

try {
    Write-Host "Creating detached replay worktree at subject commit $subjectShort..."
    Invoke-Git -Args @("worktree", "add", "--detach", $worktreePath, $subjectCommit)

    $worktreeStatus = Invoke-GitCapture -Args @("-C", $worktreePath, "status", "--short")
    $worktreeCommit = Invoke-GitCapture -Args @("-C", $worktreePath, "rev-parse", "HEAD")

    $day0Run = Invoke-PythonCapture `
        -WorkingDirectory $worktreePath `
        -Args @($day0CheckerRel, "--json")

    if ($day0Run.exit_code -ne 0) {
        throw "Replay Day-0 checker failed in detached worktree with exit code $($day0Run.exit_code)"
    }

    $day0Json = $day0Run.output | ConvertFrom-Json

    $manifestPath = Join-Path $worktreePath $packetManifestRel
    $sidecarPath = Join-Path $worktreePath $packetSidecarRel
    $outerReceiptPath = Join-Path $worktreePath $outerReceiptRel

    $packetManifestSha256 = Get-Sha256 -Path $manifestPath
    $sidecarText = (Read-Utf8 -Path $sidecarPath).Trim()
    $outerReceipt = Read-Utf8 -Path $outerReceiptPath | ConvertFrom-Json

    $gitDiffRun = & git -C $worktreePath diff --check 2>&1
    $gitDiffExit = $LASTEXITCODE

    $receipt = [ordered]@{
        receipt_id = "LRT_DAY0_TEMPORAL_REPLAY_RECEIPT_v0_1"
        receipt_version = "v0.1"
        receipt_classification = "temporal_replay_receipt"
        generated_at_utc = $generatedAtUtc

        replay_subject = [ordered]@{
            repository = "RecomputableEvidence/fork-public-evidence"
            branch_at_generation = $currentBranch
            subject_commit = $subjectCommit
            subject_commit_short = $subjectShort
            worktree_commit = $worktreeCommit
            replay_worktree_mode = "detached_git_worktree_at_subject_commit"
            replay_worktree_clean_status = $worktreeStatus
            generator_worktree_status_before_receipt = $gitStatusBefore
        }

        replay_scope = [ordered]@{
            packet_root = "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1"
            replayed_checker = $day0CheckerRel
            replayed_artifact_class = "longitudinal_reconstruction_day0_packet"
            replay_does_not_mutate_packet = $true
            replay_does_not_claim_external_anchor = $true
            replay_does_not_claim_truth_or_authority = $true
        }

        observed_hashes = [ordered]@{
            packet_manifest_sha256 = $packetManifestSha256
            packet_manifest_sidecar_text = $sidecarText
            outer_receipt_packet_manifest_sha256 = $outerReceipt.packet_manifest_sha256
        }

        observed_execution = [ordered]@{
            day0_checker_command = "python $day0CheckerRel --json"
            day0_checker_exit_code = $day0Run.exit_code
            day0_checker_total = [int]$day0Json.total
            day0_checker_passed = [int]$day0Json.passed
            day0_checker_failed = [int]$day0Json.failed
            day0_checker_name = [string]$day0Json.checker
            git_diff_check_exit_code = $gitDiffExit
            git_diff_check_output = ($gitDiffRun -join "`n")
        }

        interpretation = [ordered]@{
            replay_result = "day0_replay_passed"
            evidence_weight = "temporal_replay_receipt"
            proves = @(
                "the Day-0 checker replayed successfully against the detached subject commit",
                "the Day-0 packet remained internally consistent under the Day-0 checker at replay time",
                "the replayed checker result was structurally reproducible in this environment"
            )
            does_not_prove = @(
                "truth",
                "compliance",
                "legal sufficiency",
                "safety",
                "authorization",
                "approval",
                "certification",
                "endorsement",
                "validation",
                "schema conformance",
                "production readiness",
                "procurement approval",
                "institutional authority",
                "external original-sealing anchor"
            )
        }

        expected_current_result = [ordered]@{
            day0_checker_total = 27
            day0_checker_passed = 27
            day0_checker_failed = 0
        }

        non_authority_statement = "This temporal replay receipt records replay execution against a detached subject commit only; it does not validate truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, schema conformance, production readiness, procurement approval, external anchoring, or institutional authority."
    }

    Write-JsonUtf8Lf -Path $replayReceiptPath -Object $receipt
} finally {
    try {
        git worktree remove --force $worktreePath | Out-Null
    } catch {
        Write-Host "Warning: failed to remove worktree through git worktree remove: $worktreePath"
    }

    if (Test-Path $tempBase) {
        Remove-Item -Recurse -Force $tempBase -ErrorAction SilentlyContinue
    }
}

$schema = @'
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://recomputableevidence.example/schemas/longitudinal_day0_temporal_replay_receipt_v0_1.schema.json",
  "title": "Fork Longitudinal Day-0 Temporal Replay Receipt v0.1",
  "type": "object",
  "additionalProperties": true,
  "required": [
    "receipt_id",
    "receipt_version",
    "receipt_classification",
    "generated_at_utc",
    "replay_subject",
    "replay_scope",
    "observed_hashes",
    "observed_execution",
    "interpretation",
    "non_authority_statement"
  ],
  "properties": {
    "receipt_id": { "type": "string" },
    "receipt_version": { "type": "string" },
    "receipt_classification": { "const": "temporal_replay_receipt" },
    "generated_at_utc": { "type": "string" },
    "replay_subject": { "type": "object" },
    "replay_scope": { "type": "object" },
    "observed_hashes": { "type": "object" },
    "observed_execution": { "type": "object" },
    "interpretation": { "type": "object" },
    "non_authority_statement": { "type": "string" }
  }
}
'@

$checker = @'
#!/usr/bin/env python3
"""
Fork Longitudinal Day-0 Temporal Replay Receipt Checker v0.1.

This checker validates the temporal replay receipt surface. It does not replay
the original worktree itself. It verifies that the receipt records a bounded
Day-0 replay against a detached subject commit, with expected pass signals and
explicit non-authority language.

This checker does not validate truth, compliance, legal sufficiency, safety,
authorization, approval, certification, endorsement, validation, schema
conformance, production readiness, procurement approval, external anchoring,
or institutional authority.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
from typing import Any, Dict, List


RECEIPT_PATH = pathlib.Path("docs/reconstruction/longitudinal/day0/replay/DAY0_TEMPORAL_REPLAY_RECEIPT_v0_1.json")
README_PATH = pathlib.Path("docs/reconstruction/longitudinal/day0/replay/README.md")
INTERPRETATION_PATH = pathlib.Path("docs/reconstruction/longitudinal/day0/replay/DAY0_TEMPORAL_REPLAY_RECEIPT_INTERPRETATION_v0_1.md")
SCHEMA_PATH = pathlib.Path("schemas/longitudinal_day0_temporal_replay_receipt_v0_1.schema.json")
RESPONSE_RECEIPT_PATH = pathlib.Path("docs/review/public-rounds/round-005/ROUND005_RESPONSE_DAY0_TEMPORAL_REPLAY_RECEIPT_v0_1.md")

NON_AUTHORITY_TERMS = [
    "does not",
    "truth",
    "compliance",
    "legal",
    "safety",
    "authorization",
    "approval",
    "certification",
    "endorsement",
    "validation",
    "schema conformance",
    "production readiness",
    "authority",
]

DOES_NOT_PROVE_TERMS = [
    "truth",
    "compliance",
    "legal sufficiency",
    "safety",
    "authorization",
    "approval",
    "certification",
    "endorsement",
    "validation",
    "schema conformance",
    "production readiness",
    "procurement approval",
    "institutional authority",
    "external original-sealing anchor",
]


def result(name: str, passed: bool, detail: str, data: Any = None) -> Dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "detail": detail,
        "data": data,
    }


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: pathlib.Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def missing_terms(text: str, terms: List[str]) -> List[str]:
    lower = text.lower()
    return [term for term in terms if term not in lower]


def git_commit_exists(commit: str) -> bool:
    try:
        subprocess.run(
            ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return True
    except Exception:
        return False


def git_commit_is_ancestor(commit: str) -> bool:
    try:
        completed = subprocess.run(
            ["git", "merge-base", "--is-ancestor", commit, "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return completed.returncode == 0
    except Exception:
        return False


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    checks: List[Dict[str, Any]] = []

    for name, path in [
        ("path:receipt", RECEIPT_PATH),
        ("path:readme", README_PATH),
        ("path:interpretation", INTERPRETATION_PATH),
        ("path:schema", SCHEMA_PATH),
        ("path:round005-response", RESPONSE_RECEIPT_PATH),
    ]:
        checks.append(result(name, path.is_file(), "present" if path.is_file() else "missing", str(path).replace("\\", "/")))

    receipt = None
    try:
        receipt = load_json(RECEIPT_PATH)
        checks.append(result("receipt:parse", isinstance(receipt, dict), "receipt parses as JSON object"))
    except Exception as exc:
        checks.append(result("receipt:parse", False, str(exc)))

    try:
        schema = load_json(SCHEMA_PATH)
        checks.append(result("schema:parse", isinstance(schema, dict), "schema parses as JSON object"))
    except Exception as exc:
        checks.append(result("schema:parse", False, str(exc)))

    if isinstance(receipt, dict):
        checks.append(result(
            "receipt:classification",
            receipt.get("receipt_classification") == "temporal_replay_receipt",
            "receipt_classification is temporal_replay_receipt",
            receipt.get("receipt_classification"),
        ))

        subject = receipt.get("replay_subject", {})
        commit = str(subject.get("subject_commit", ""))
        checks.append(result(
            "receipt:subject-commit-format",
            bool(re.fullmatch(r"[0-9a-fA-F]{40}", commit)),
            "subject_commit is 40 hex characters",
            commit,
        ))

        checks.append(result(
            "receipt:subject-commit-exists",
            bool(re.fullmatch(r"[0-9a-fA-F]{40}", commit)) and git_commit_exists(commit),
            "subject_commit exists in local git object database",
            commit,
        ))

        checks.append(result(
            "receipt:subject-commit-is-ancestor",
            bool(re.fullmatch(r"[0-9a-fA-F]{40}", commit)) and git_commit_is_ancestor(commit),
            "subject_commit is ancestor of current HEAD",
            commit,
        ))

        scope = receipt.get("replay_scope", {})
        checks.append(result(
            "receipt:detached-worktree-mode",
            subject.get("replay_worktree_mode") == "detached_git_worktree_at_subject_commit",
            "receipt records detached replay worktree mode",
            subject.get("replay_worktree_mode"),
        ))

        checks.append(result(
            "receipt:replay-scope-non-mutating",
            scope.get("replay_does_not_mutate_packet") is True,
            "receipt says replay does not mutate packet",
            scope.get("replay_does_not_mutate_packet"),
        ))

        observed = receipt.get("observed_execution", {})
        checks.append(result(
            "receipt:day0-checker-passed",
            observed.get("day0_checker_failed") == 0 and observed.get("day0_checker_passed") == observed.get("day0_checker_total"),
            "Day-0 checker replay passed",
            observed,
        ))

        checks.append(result(
            "receipt:expected-day0-total",
            observed.get("day0_checker_total") == 27 and observed.get("day0_checker_passed") == 27 and observed.get("day0_checker_failed") == 0,
            "Day-0 checker expected 27/27 replay signal present",
            observed,
        ))

        checks.append(result(
            "receipt:git-diff-check",
            observed.get("git_diff_check_exit_code") == 0,
            "detached replay worktree git diff --check exited 0",
            observed.get("git_diff_check_exit_code"),
        ))

        hashes = receipt.get("observed_hashes", {})
        manifest_hash = str(hashes.get("packet_manifest_sha256", ""))
        outer_hash = str(hashes.get("outer_receipt_packet_manifest_sha256", ""))
        sidecar_text = str(hashes.get("packet_manifest_sidecar_text", ""))

        checks.append(result(
            "receipt:manifest-hash-format",
            bool(re.fullmatch(r"[0-9a-f]{64}", manifest_hash)),
            "packet manifest SHA-256 is 64 lowercase hex characters",
            manifest_hash,
        ))

        checks.append(result(
            "receipt:sidecar-binds-manifest-hash",
            manifest_hash in sidecar_text,
            "sidecar text contains packet manifest hash",
            sidecar_text,
        ))

        checks.append(result(
            "receipt:outer-binds-manifest-hash",
            manifest_hash == outer_hash,
            "outer receipt manifest hash equals observed manifest hash",
            {"manifest_hash": manifest_hash, "outer_hash": outer_hash},
        ))

        interpretation = receipt.get("interpretation", {})
        does_not_prove_text = " ".join(str(x) for x in interpretation.get("does_not_prove", []))
        missing_does_not_prove = missing_terms(does_not_prove_text, DOES_NOT_PROVE_TERMS)
        checks.append(result(
            "receipt:does-not-prove-boundary",
            len(missing_does_not_prove) == 0,
            "does_not_prove list contains required boundary terms" if not missing_does_not_prove else "missing boundary terms",
            missing_does_not_prove,
        ))

        non_authority = str(receipt.get("non_authority_statement", ""))
        missing_non_authority = missing_terms(non_authority, NON_AUTHORITY_TERMS)
        checks.append(result(
            "receipt:non-authority-statement",
            len(missing_non_authority) == 0,
            "non-authority statement contains required terms" if not missing_non_authority else "missing non-authority terms",
            missing_non_authority,
        ))
    else:
        checks.append(result("receipt:content", False, "receipt unavailable"))

    for name, path in [
        ("readme:non-authority", README_PATH),
        ("interpretation:non-authority", INTERPRETATION_PATH),
        ("round005-response:non-authority", RESPONSE_RECEIPT_PATH),
    ]:
        try:
            text = read_text(path)
            missing = missing_terms(text, NON_AUTHORITY_TERMS)
            checks.append(result(
                name,
                len(missing) == 0,
                "non-authority terms present" if not missing else "missing non-authority terms",
                missing,
            ))
        except Exception as exc:
            checks.append(result(name, False, str(exc)))

    failed = sum(1 for item in checks if not item["passed"])

    summary = {
        "checker": "check_longitudinal_day0_temporal_replay_receipt_v0_1.py",
        "total": len(checks),
        "passed": len(checks) - failed,
        "failed": failed,
        "results": checks,
        "interpretation": (
            "A pass confirms a bounded Day-0 temporal replay receipt is present and internally consistent. "
            "It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, "
            "certification, endorsement, validation, schema conformance, production readiness, procurement "
            "approval, external anchoring, or institutional authority."
        ),
        "non_authority_statement": (
            "This checker validates temporal replay receipt structure only; it does not validate truth, compliance, "
            "legal sufficiency, safety, authorization, approval, certification, endorsement, validation, schema "
            "conformance, production readiness, procurement approval, external anchoring, or institutional authority."
        ),
    }

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"Longitudinal Day-0 temporal replay receipt checks: {summary['passed']}/{summary['total']} passed")
        for item in checks:
            status = "PASS" if item["passed"] else "FAIL"
            print(f"{status} {item['name']}: {item['detail']}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
'@

$replayReadme = @'
# Longitudinal Day-0 Replay

Status: Temporal replay receipt surface.

This directory records Day-0 temporal replay evidence for the Longitudinal Reconstruction Trial.

## Current replay receipt

- `DAY0_TEMPORAL_REPLAY_RECEIPT_v0_1.json`

## Interpretation

A Day-0 temporal replay receipt records that the Day-0 checker was re-run against a detached subject commit and produced the expected replay result.

It is replay evidence.

It is not external anchoring.

It is not truth validation.

It is not schema enforcement.

It is not institutional authority.

## Checker

Run from repository root:

- `python tools/check_longitudinal_day0_temporal_replay_receipt_v0_1.py --json`

## Boundary

This replay surface does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, schema conformance, production readiness, procurement approval, external anchoring, or institutional authority.
'@

$replayInterpretation = @'
# Day-0 Temporal Replay Receipt Interpretation v0.1

Status: Interpretation note.
Scope: Longitudinal Reconstruction Day-0 temporal replay receipt.

## 1. What the receipt records

The Day-0 temporal replay receipt records that:

- a detached Git worktree was created at the subject commit;
- the Day-0 checker was executed from that detached worktree;
- the Day-0 checker returned the expected pass signal;
- the packet manifest hash, manifest sidecar, and outer receipt manifest binding were observed;
- the replay was classified as temporal replay evidence.

## 2. What the receipt supports

The receipt supports the claim that the Day-0 checker result was replayed at a later time against the recorded subject commit.

It supports deterministic replay evidence for the Day-0 checker surface.

## 3. What the receipt does not support

The receipt does not establish:

- truth;
- compliance;
- legal sufficiency;
- safety;
- authorization;
- approval;
- certification;
- endorsement;
- validation;
- schema conformance;
- production readiness;
- procurement approval;
- external anchoring;
- institutional authority.

## 4. Relationship to known limitations

This receipt does not resolve the coordinated re-seal limitation.

This receipt does not resolve the lexical non-authority limitation.

This receipt does not add mechanical schema enforcement.

Those limitations remain separately recorded and should not be collapsed into the replay receipt.

## 5. Boundary statement

This interpretation note explains replay evidence only. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, schema conformance, production readiness, procurement approval, external anchoring, or institutional authority.
'@

$responseReceipt = @'
# Round 005 Response: Day-0 Temporal Replay Receipt v0.1

Status: Engineering response receipt.
Round: Public Review Round 005.
Response class: Temporal replay receipt filing.

## 1. Finding addressed

Round 005 indicated that future Day-7, Day-30, and Day-90 work should use replay receipts and should preserve the distinction between replay success and external authority.

This response adds the first Day-0 temporal replay receipt.

## 2. Added artifacts

- `docs/reconstruction/longitudinal/day0/replay/README.md`
- `docs/reconstruction/longitudinal/day0/replay/DAY0_TEMPORAL_REPLAY_RECEIPT_v0_1.json`
- `docs/reconstruction/longitudinal/day0/replay/DAY0_TEMPORAL_REPLAY_RECEIPT_INTERPRETATION_v0_1.md`
- `schemas/longitudinal_day0_temporal_replay_receipt_v0_1.schema.json`
- `tools/check_longitudinal_day0_temporal_replay_receipt_v0_1.py`

## 3. Interpretation

A replay receipt pass means:

- the receipt is structurally present;
- the subject commit is recorded;
- the subject commit exists locally and is an ancestor of current HEAD;
- the detached replay worktree execution recorded Day-0 checker success;
- the receipt preserves the correct replay boundary.

It does not mean the Day-0 packet is true, compliant, legally sufficient, safe, authorized, approved, certified, endorsed, validated, schema-conformant, production-ready, externally anchored, or institutionally authoritative.

## 4. Relationship to other Round 005 responses

This response does not replace:

- the coordinated re-seal adversarial case;
- the lexical non-authority limit adversarial case;
- the schema presence versus schema enforcement clarification.

Those remain separate limitations.

## 5. Non-authority statement

This response records temporal replay evidence only. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, schema conformance, production readiness, procurement approval, external anchoring, or institutional authority.
'@

Write-Utf8Lf -Path $schemaPath -Content $schema
Write-Utf8Lf -Path $checkerPath -Content $checker
Write-Utf8Lf -Path $replayReadmePath -Content $replayReadme
Write-Utf8Lf -Path $replayInterpretationPath -Content $replayInterpretation
Write-Utf8Lf -Path $responseReceiptPath -Content $responseReceipt

$routingBlock = @'
## Day-0 temporal replay receipt

Day-0 temporal replay receipt:

- `docs/reconstruction/longitudinal/day0/replay/DAY0_TEMPORAL_REPLAY_RECEIPT_v0_1.json`

Interpretation:

- `docs/reconstruction/longitudinal/day0/replay/DAY0_TEMPORAL_REPLAY_RECEIPT_INTERPRETATION_v0_1.md`

Checker:

- `tools/check_longitudinal_day0_temporal_replay_receipt_v0_1.py`

Run:

- `python tools/check_longitudinal_day0_temporal_replay_receipt_v0_1.py --json`

Boundary:

- temporal replay evidence means the Day-0 checker replayed successfully against the recorded subject commit;
- it does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, schema conformance, production readiness, procurement approval, external anchoring, or institutional authority.
'@

$round005Block = @'
## Round 005 response: Day-0 temporal replay receipt

The first Day-0 temporal replay receipt is now filed.

Response receipt:

- `docs/review/public-rounds/round-005/ROUND005_RESPONSE_DAY0_TEMPORAL_REPLAY_RECEIPT_v0_1.md`

Replay receipt:

- `docs/reconstruction/longitudinal/day0/replay/DAY0_TEMPORAL_REPLAY_RECEIPT_v0_1.json`

Checker:

- `python tools/check_longitudinal_day0_temporal_replay_receipt_v0_1.py --json`

This response records temporal replay evidence. It does not resolve external anchoring, coordinated re-seal, lexical non-authority, or schema-enforcement limitations.
'@

Replace-OrAppendBlock -Path "README.md" -BlockId "FORK_LONGITUDINAL_DAY0_TEMPORAL_REPLAY_RECEIPT" -Content $routingBlock
Replace-OrAppendBlock -Path "docs/CURRENT_PROOF_SURFACE_v0_1.md" -BlockId "FORK_LONGITUDINAL_DAY0_TEMPORAL_REPLAY_RECEIPT" -Content $routingBlock
Replace-OrAppendBlock -Path "docs/REVIEWER_START_HERE_v0_1.md" -BlockId "FORK_LONGITUDINAL_DAY0_TEMPORAL_REPLAY_RECEIPT" -Content $routingBlock
Replace-OrAppendBlock -Path "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md" -BlockId "FORK_LONGITUDINAL_DAY0_TEMPORAL_REPLAY_RECEIPT" -Content $routingBlock
Replace-OrAppendBlock -Path "docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md" -BlockId "FORK_LONGITUDINAL_DAY0_TEMPORAL_REPLAY_RECEIPT" -Content $routingBlock
Replace-OrAppendBlock -Path "docs/reconstruction/FORK_LONGITUDINAL_RECONSTRUCTION_TRIAL_v0_1.md" -BlockId "FORK_LONGITUDINAL_DAY0_TEMPORAL_REPLAY_RECEIPT" -Content $routingBlock
Replace-OrAppendBlock -Path "docs/review/public-rounds/round-005/README.md" -BlockId "FORK_ROUND005_DAY0_TEMPORAL_REPLAY_RESPONSE" -Content $round005Block
Replace-OrAppendBlock -Path "docs/review/public-rounds/round-005/PUBLIC_REVIEW_ROUND_005_SYNTHESIS_v0_1.md" -BlockId "FORK_ROUND005_DAY0_TEMPORAL_REPLAY_RESPONSE" -Content $round005Block

Ensure-VerifierPath -VerifierPath $verifierPath -PathToRequire "docs/reconstruction/longitudinal/day0/replay/README.md"
Ensure-VerifierPath -VerifierPath $verifierPath -PathToRequire "docs/reconstruction/longitudinal/day0/replay/DAY0_TEMPORAL_REPLAY_RECEIPT_v0_1.json"
Ensure-VerifierPath -VerifierPath $verifierPath -PathToRequire "docs/reconstruction/longitudinal/day0/replay/DAY0_TEMPORAL_REPLAY_RECEIPT_INTERPRETATION_v0_1.md"
Ensure-VerifierPath -VerifierPath $verifierPath -PathToRequire "schemas/longitudinal_day0_temporal_replay_receipt_v0_1.schema.json"
Ensure-VerifierPath -VerifierPath $verifierPath -PathToRequire "tools/check_longitudinal_day0_temporal_replay_receipt_v0_1.py"
Ensure-VerifierPath -VerifierPath $verifierPath -PathToRequire "docs/review/public-rounds/round-005/ROUND005_RESPONSE_DAY0_TEMPORAL_REPLAY_RECEIPT_v0_1.md"

Ensure-VerifierChecker -VerifierPath $verifierPath

Write-Host ""
Write-Host "Running Day-0 temporal replay receipt checker..."
Invoke-Python -Args @($checkerPath, "--json")

Write-Host ""
Write-Host "Running Day-0 checker..."
Invoke-Python -Args @("tools/check_longitudinal_reconstruction_day0_packet_v0_1.py", "--json")

Write-Host ""
Write-Host "Running longitudinal Day-0 adversarial checker..."
Invoke-Python -Args @("tools/check_longitudinal_day0_adversarial_cases_v0_1.py", "--json")

Write-Host ""
Write-Host "Running Day-0 schema-scope checker..."
Invoke-Python -Args @("tools/check_longitudinal_day0_schema_scope_v0_1.py", "--json")

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
Write-Host "  git diff -- docs\reconstruction\longitudinal\day0\replay"
Write-Host "  git diff -- tools\check_longitudinal_day0_temporal_replay_receipt_v0_1.py"
Write-Host "  git diff -- scripts\verify_public_review_package_v0_1.ps1"
Write-Host "  python tools\check_longitudinal_day0_temporal_replay_receipt_v0_1.py --json"
Write-Host "  python tools\check_longitudinal_reconstruction_day0_packet_v0_1.py --json"
Write-Host "  python tools\check_longitudinal_day0_adversarial_cases_v0_1.py --json"
Write-Host "  python tools\check_longitudinal_day0_schema_scope_v0_1.py --json"
Write-Host "  powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1"
Write-Host "  git diff --check"

if ($Commit) {
    Invoke-Git -Args @("add", "--",
        $scriptPath,
        $schemaPath,
        $checkerPath,
        $replayReadmePath,
        $replayReceiptPath,
        $replayInterpretationPath,
        $responseReceiptPath,
        "README.md",
        "docs/CURRENT_PROOF_SURFACE_v0_1.md",
        "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md",
        "docs/REVIEWER_START_HERE_v0_1.md",
        "docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md",
        "docs/reconstruction/FORK_LONGITUDINAL_RECONSTRUCTION_TRIAL_v0_1.md",
        "docs/review/public-rounds/round-005/README.md",
        "docs/review/public-rounds/round-005/PUBLIC_REVIEW_ROUND_005_SYNTHESIS_v0_1.md",
        $verifierPath
    )

    Invoke-Git -Args @("diff", "--cached", "--check")
    Invoke-Git -Args @("commit", "-m", "Add Day-0 temporal replay receipt")

    if ($Push) {
        Invoke-Git -Args @("push")
    }
}

Write-Host ""
Write-Host "Done."