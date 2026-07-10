# scripts/add_longitudinal_reconstruction_day0_packet_v0_1.ps1
# Adds Fork Longitudinal Reconstruction Trial Day-0 packet.
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
        [int]$Depth = 80
    )

    $json = $Object | ConvertTo-Json -Depth $Depth
    Write-Utf8Lf -Path $Path -Content $json
}

function Read-Utf8 {
    param([Parameter(Mandatory = $true)][string]$Path)
    return [System.IO.File]::ReadAllText((Resolve-Path $Path).Path, $Utf8NoBom)
}

function Get-Sha256Lower {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path $Path)) {
        throw "Cannot hash missing file: $Path"
    }

    return (Get-FileHash -Algorithm SHA256 -Path $Path).Hash.ToLowerInvariant()
}

function Normalize-PathForManifest {
    param([Parameter(Mandatory = $true)][string]$Path)
    return ($Path -replace "\\", "/")
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

$scriptPath = "scripts/add_longitudinal_reconstruction_day0_packet_v0_1.ps1"
$checkerPath = "tools/check_longitudinal_reconstruction_day0_packet_v0_1.py"
$schemaPath = "schemas/longitudinal_reconstruction_day0_packet_manifest_v0_1.schema.json"
$receiptPath = "docs/reconstruction/LONGITUDINAL_RECONSTRUCTION_DAY0_PACKET_RECEIPT_v0_1.md"
$protocolPath = "docs/reconstruction/FORK_LONGITUDINAL_RECONSTRUCTION_TRIAL_v0_1.md"
$verifierPath = "scripts/verify_public_review_package_v0_1.ps1"

$packetRoot = "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1"
$packetReadmePath = "$packetRoot/README.md"
$manifestPath = "$packetRoot/packet_manifest.json"
$manifestShaPath = "$packetRoot/packet_manifest.sha256"
$outerReceiptPath = "$packetRoot/packet_manifest_outer_receipt.json"

$boundaryStatementPath = "$packetRoot/boundary/day0_non_authority_boundary_statement.txt"
$requestRecordPath = "$packetRoot/evidence/day0_request_record.json"
$aiOutputRecordPath = "$packetRoot/evidence/day0_ai_output_record.json"
$humanReviewRecordPath = "$packetRoot/evidence/day0_human_review_record.json"
$boundaryStateRecordPath = "$packetRoot/evidence/day0_boundary_state_record.json"
$nonClaimsRecordPath = "$packetRoot/evidence/day0_non_claims_record.json"
$expectedReconstructionPath = "$packetRoot/expected/day0_expected_reconstruction.json"
$environmentManifestPath = "$packetRoot/environment/day0_environment_manifest.json"
$generationReceiptPath = "$packetRoot/receipts/day0_generation_receipt.json"
$expectedProvenanceReceiptPath = "$packetRoot/receipts/day0_expected_reconstruction_provenance_receipt.json"
$scopeReceiptPath = "$packetRoot/receipts/day0_packet_scope_receipt.json"

$baseCommit = "unknown"
try {
    $baseCommit = (& git rev-parse HEAD 2>$null).Trim()
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($baseCommit)) {
        $baseCommit = "unknown"
    }
} catch {
    $baseCommit = "unknown"
}

$trialId = "fork_longitudinal_reconstruction_trial_v0_1"
$packetId = "LRT_DAY0_PACKET_v0_1"
$fixtureTime = "2026-07-09T00:00:00Z"

$nonAuthorityStatement = @'
This Day-0 packet preserves a bounded synthetic evidence state for later longitudinal reconstruction testing. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, production readiness, procurement approval, or institutional authority. Later reconstruction may verify packet integrity, manifest continuity, hash consistency, and declared boundary state; it must not convert preserved evidence into authority.
'@

$packetReadme = @'
# Longitudinal Reconstruction Trial Day-0 Packet v0.1

Status: Day-0 fixture packet.
Trial: fork_longitudinal_reconstruction_trial_v0_1
Packet: LRT_DAY0_PACKET_v0_1

## Purpose

This packet creates the first sealed Day-0 object for Fork's longitudinal reconstruction trial.

The trial question is:

Can a future reviewer reconstruct today's evidence state later without inheriting today's authority?

## Packet Contents

- packet_manifest.json
- packet_manifest.sha256
- packet_manifest_outer_receipt.json
- boundary/day0_non_authority_boundary_statement.txt
- evidence/day0_request_record.json
- evidence/day0_ai_output_record.json
- evidence/day0_human_review_record.json
- evidence/day0_boundary_state_record.json
- evidence/day0_non_claims_record.json
- expected/day0_expected_reconstruction.json
- environment/day0_environment_manifest.json
- receipts/day0_generation_receipt.json
- receipts/day0_expected_reconstruction_provenance_receipt.json
- receipts/day0_packet_scope_receipt.json

## Verification

Run from repository root:

- python tools/check_longitudinal_reconstruction_day0_packet_v0_1.py --json

The checker verifies:

- required packet files exist;
- artifact hashes match the manifest;
- packet_manifest.sha256 matches packet_manifest.json;
- packet_manifest_outer_receipt.json binds the manifest hash;
- expected reconstruction hash matches the expected reconstruction file;
- environment manifest hash matches the environment file;
- non-authority boundary statement hash matches the boundary file;
- non-authority language remains explicit.

## Boundary

This packet is a reconstruction fixture. It is not an endorsement, validation, certification, compliance opinion, legal opinion, safety assessment, production-readiness assessment, procurement approval, or authority transfer.
'@

$requestRecord = [ordered]@{
    record_id = "LRT_DAY0_REQUEST_RECORD_v0_1"
    record_type = "synthetic_ai_assisted_workflow_request"
    trial_id = $trialId
    packet_id = $packetId
    created_at_fixed_fixture_time = $fixtureTime
    request_text = "Create a bounded evidence-state fixture that later reviewers can reconstruct without relying on the authority of the author, the model, or the original environment."
    requester_role = "fixture_author"
    declared_purpose = "longitudinal reconstruction trial Day-0 packet"
    requested_output = [ordered]@{
        evidence_state_record = $true
        boundary_state_record = $true
        non_claims_record = $true
        expected_reconstruction = $true
        manifest_and_outer_receipt = $true
    }
    non_authority_statement = $nonAuthorityStatement
}

$aiOutputRecord = [ordered]@{
    record_id = "LRT_DAY0_AI_OUTPUT_RECORD_v0_1"
    record_type = "synthetic_ai_output_record"
    trial_id = $trialId
    packet_id = $packetId
    created_at_fixed_fixture_time = $fixtureTime
    output_summary = "The synthetic workflow produced a bounded Day-0 evidence-state packet describing request, output, human review, boundary state, non-claims, expected reconstruction, and receipts."
    preserved_claims = @(
        "A Day-0 packet exists at the declared packet path.",
        "The packet contains declared evidence-state artifacts.",
        "The packet contains explicit non-authority language.",
        "The packet can be checked for file presence and SHA-256 hash continuity."
    )
    refused_claims = @(
        "The packet proves the underlying workflow is true.",
        "The packet proves legal sufficiency.",
        "The packet proves compliance.",
        "The packet proves safety.",
        "The packet proves authorization.",
        "The packet proves approval.",
        "The packet proves production readiness.",
        "The packet transfers authority to later reviewers."
    )
    non_authority_statement = $nonAuthorityStatement
}

$humanReviewRecord = [ordered]@{
    record_id = "LRT_DAY0_HUMAN_REVIEW_RECORD_v0_1"
    record_type = "synthetic_human_review_record"
    trial_id = $trialId
    packet_id = $packetId
    created_at_fixed_fixture_time = $fixtureTime
    review_scope = "structural fixture review only"
    reviewed_items = @(
        "request record",
        "AI output record",
        "boundary state record",
        "non-claims record",
        "expected reconstruction",
        "environment manifest",
        "non-authority boundary statement"
    )
    review_result = "accepted_as_day0_fixture_for_later_reconstruction_testing"
    review_non_claims = @(
        "not endorsement",
        "not validation",
        "not certification",
        "not legal opinion",
        "not compliance opinion",
        "not safety assessment",
        "not production-readiness assessment",
        "not authority transfer"
    )
    non_authority_statement = $nonAuthorityStatement
}

$boundaryStateRecord = [ordered]@{
    record_id = "LRT_DAY0_BOUNDARY_STATE_RECORD_v0_1"
    record_type = "boundary_state_record"
    trial_id = $trialId
    packet_id = $packetId
    created_at_fixed_fixture_time = $fixtureTime
    preserved_state = [ordered]@{
        request_exists = $true
        ai_output_exists = $true
        human_review_exists = $true
        non_claims_exist = $true
        expected_reconstruction_exists = $true
        environment_manifest_exists = $true
        manifest_exists = $true
        outer_receipt_exists = $true
    }
    boundary_rules = @(
        "Evidence may be preserved.",
        "Interpretation remains external.",
        "Authority is not inherited.",
        "Reconstruction is not authorization.",
        "Receipt continuity is not truth.",
        "Hash continuity is not legal sufficiency.",
        "Checker pass is not compliance.",
        "Packet survival is not production readiness."
    )
    allowed_future_questions = @(
        "Do the packet files still exist?",
        "Do the artifact hashes still match the manifest?",
        "Does the manifest hash still match the outer receipt?",
        "Can the expected reconstruction be reproduced from the preserved packet?",
        "Has checker behavior drifted from the pinned checker to the current checker?"
    )
    disallowed_future_upgrades = @(
        "Treating reconstruction as approval.",
        "Treating packet survival as legal sufficiency.",
        "Treating hash continuity as truth.",
        "Treating a checker pass as compliance.",
        "Treating a receipt as replacement source evidence.",
        "Treating later review as retroactive authorization."
    )
    non_authority_statement = $nonAuthorityStatement
}

$nonClaimsRecord = [ordered]@{
    record_id = "LRT_DAY0_NON_CLAIMS_RECORD_v0_1"
    record_type = "non_claims_record"
    trial_id = $trialId
    packet_id = $packetId
    created_at_fixed_fixture_time = $fixtureTime
    explicit_non_claims = @(
        "Fork does not establish truth.",
        "Fork does not establish legal sufficiency.",
        "Fork does not establish compliance.",
        "Fork does not establish safety.",
        "Fork does not authorize execution.",
        "Fork does not approve deployment.",
        "Fork does not certify the workflow.",
        "Fork does not endorse the underlying content.",
        "Fork does not establish production readiness.",
        "Fork does not transfer institutional authority.",
        "Fork does not replace source evidence.",
        "Fork does not convert later reconstruction into retroactive permission."
    )
    non_authority_statement = $nonAuthorityStatement
}

$expectedReconstruction = [ordered]@{
    reconstruction_id = "LRT_DAY0_EXPECTED_RECONSTRUCTION_v0_1"
    record_type = "expected_reconstruction"
    trial_id = $trialId
    packet_id = $packetId
    created_at_fixed_fixture_time = $fixtureTime
    expected_reconstructable_state = [ordered]@{
        request_summary = "A bounded fixture request asked for a Day-0 evidence-state packet for later reconstruction testing."
        output_summary = "A synthetic AI-assisted output record preserved claims and refused authority-expanding claims."
        human_review_summary = "A synthetic human review accepted the packet only as a structural Day-0 fixture."
        boundary_summary = "The packet distinguishes evidence preservation from interpretation, approval, compliance, legal sufficiency, safety, production readiness, and authority."
        non_claims_summary = "The packet explicitly states what Fork does not claim."
        manifest_summary = "The packet manifest binds artifact paths to SHA-256 hashes."
        outer_receipt_summary = "The outer receipt binds the manifest hash outside the manifest."
    }
    expected_future_verification_results = @(
        "Artifact files exist at declared paths.",
        "Artifact SHA-256 values match packet_manifest.json.",
        "packet_manifest.sha256 matches packet_manifest.json.",
        "packet_manifest_outer_receipt.json records the manifest hash.",
        "Expected reconstruction hash matches this file.",
        "Environment manifest hash matches the environment file.",
        "Non-authority statement hash matches the boundary statement file."
    )
    explicitly_not_reconstructable = @(
        "truth of the underlying workflow",
        "legal sufficiency",
        "compliance sufficiency",
        "safety",
        "authorization",
        "approval",
        "certification",
        "endorsement",
        "production readiness",
        "institutional authority"
    )
    checker_drift_rule = "If a future current checker disagrees with the pinned Day-0 checker while packet hashes remain stable, classify the disagreement as checker drift, not packet failure."
    packet_failure_rule = "If the pinned Day-0 checker cannot verify the preserved packet because files are missing or hashes mismatch, classify the condition as packet failure or tamper depending on the mismatch."
    non_authority_statement = $nonAuthorityStatement
}

$environmentManifest = [ordered]@{
    environment_manifest_id = "LRT_DAY0_ENVIRONMENT_MANIFEST_v0_1"
    record_type = "environment_manifest"
    trial_id = $trialId
    packet_id = $packetId
    created_at_fixed_fixture_time = $fixtureTime
    fixture_generation_environment = [ordered]@{
        intended_platform = "cross-platform repository fixture"
        required_for_day0_check = @(
            "Python 3.10 or later recommended",
            "Git recommended",
            "PowerShell 5.1 or later optional for wrapper scripts"
        )
        canonicalization_method = "file-byte SHA-256 over UTF-8 LF artifacts; JSON emitted by PowerShell ConvertTo-Json with ordered fixture fields; not JCS"
        network_required = $false
    }
    generated_from_base_commit = $baseCommit
    non_authority_statement = $nonAuthorityStatement
}

$generationReceipt = [ordered]@{
    receipt_id = "LRT_DAY0_GENERATION_RECEIPT_v0_1"
    receipt_type = "day0_packet_generation_receipt"
    trial_id = $trialId
    packet_id = $packetId
    created_at_fixed_fixture_time = $fixtureTime
    generation_method = "scripts/add_longitudinal_reconstruction_day0_packet_v0_1.ps1"
    generated_from_base_commit = $baseCommit
    generated_artifact_roles = @(
        "request record",
        "AI output record",
        "human review record",
        "boundary state record",
        "non-claims record",
        "expected reconstruction",
        "environment manifest",
        "manifest",
        "manifest hash",
        "outer receipt"
    )
    non_authority_statement = $nonAuthorityStatement
}

$expectedProvenanceReceipt = [ordered]@{
    receipt_id = "LRT_DAY0_EXPECTED_RECONSTRUCTION_PROVENANCE_RECEIPT_v0_1"
    receipt_type = "expected_reconstruction_provenance_receipt"
    trial_id = $trialId
    packet_id = $packetId
    created_at_fixed_fixture_time = $fixtureTime
    provenance_status = "author_declared_day0_fixture_baseline"
    independence_status = "not_independent_external_reviewer_provenance_in_v0_1"
    boundary_note = "The Day-0 expected reconstruction is a declared fixture baseline. Later Day-7, Day-30, and Day-90 replay should not treat this as independent validation."
    required_future_upgrade = "Future rounds should obtain independent expected reconstruction provenance from an exterior reviewer or separate implementation."
    non_authority_statement = $nonAuthorityStatement
}

$scopeReceipt = [ordered]@{
    receipt_id = "LRT_DAY0_PACKET_SCOPE_RECEIPT_v0_1"
    receipt_type = "packet_scope_receipt"
    trial_id = $trialId
    packet_id = $packetId
    created_at_fixed_fixture_time = $fixtureTime
    in_scope = @(
        "file presence",
        "artifact hash continuity",
        "manifest hash continuity",
        "outer receipt binding",
        "declared expected reconstruction",
        "environment manifest hash",
        "non-authority boundary statement hash"
    )
    out_of_scope = @(
        "truth",
        "compliance",
        "legal sufficiency",
        "safety",
        "authorization",
        "approval",
        "certification",
        "endorsement",
        "production readiness",
        "institutional authority"
    )
    non_authority_statement = $nonAuthorityStatement
}

$schema = @'
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://recomputableevidence.example/schemas/longitudinal_reconstruction_day0_packet_manifest_v0_1.schema.json",
  "title": "Fork Longitudinal Reconstruction Day-0 Packet Manifest v0.1",
  "type": "object",
  "additionalProperties": true,
  "required": [
    "manifest_schema_version",
    "trial_id",
    "packet_id",
    "created_at_fixed_fixture_time",
    "generated_from_base_commit",
    "canonicalization_method",
    "artifact_hashes",
    "expected_reconstruction_hash",
    "environment_manifest_hash",
    "non_authority_boundary_statement_hash",
    "non_authority_statement"
  ],
  "properties": {
    "manifest_schema_version": { "type": "string" },
    "trial_id": { "type": "string" },
    "packet_id": { "type": "string" },
    "created_at_fixed_fixture_time": { "type": "string" },
    "generated_from_base_commit": { "type": "string" },
    "canonicalization_method": { "type": "string" },
    "artifact_hashes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [ "path", "role", "sha256" ],
        "properties": {
          "path": { "type": "string" },
          "role": { "type": "string" },
          "sha256": {
            "type": "string",
            "pattern": "^[a-f0-9]{64}$"
          }
        }
      }
    },
    "expected_reconstruction_hash": {
      "type": "string",
      "pattern": "^[a-f0-9]{64}$"
    },
    "environment_manifest_hash": {
      "type": "string",
      "pattern": "^[a-f0-9]{64}$"
    },
    "non_authority_boundary_statement_hash": {
      "type": "string",
      "pattern": "^[a-f0-9]{64}$"
    },
    "non_authority_statement": { "type": "string" }
  }
}
'@

$checker = @'
#!/usr/bin/env python3
"""
Fork Longitudinal Reconstruction Trial Day-0 Packet Checker v0.1.

Verifies the Day-0 packet manifest, artifact hashes, manifest hash sidecar,
outer receipt binding, expected reconstruction hash, environment manifest hash,
and non-authority boundary statement hash.

This checker does not validate truth, compliance, legal sufficiency, safety,
authorization, approval, certification, endorsement, production readiness, or
institutional authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
from typing import Any, Dict, List


DEFAULT_PACKET_ROOT = "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1"

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
    "production readiness",
    "authority",
]

REQUIRED_PACKET_FILES = [
    "README.md",
    "packet_manifest.json",
    "packet_manifest.sha256",
    "packet_manifest_outer_receipt.json",
    "boundary/day0_non_authority_boundary_statement.txt",
    "evidence/day0_request_record.json",
    "evidence/day0_ai_output_record.json",
    "evidence/day0_human_review_record.json",
    "evidence/day0_boundary_state_record.json",
    "evidence/day0_non_claims_record.json",
    "expected/day0_expected_reconstruction.json",
    "environment/day0_environment_manifest.json",
    "receipts/day0_generation_receipt.json",
    "receipts/day0_expected_reconstruction_provenance_receipt.json",
    "receipts/day0_packet_scope_receipt.json",
]


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
        raise ValueError(f"{path} root must be object")
    return data


def result(name: str, passed: bool, detail: str = "", data: Any = None) -> Dict[str, Any]:
    return {
        "name": name,
        "passed": passed,
        "detail": detail,
        "data": data,
    }


def has_boundary_terms(text: str) -> List[str]:
    lower = text.lower()
    return [term for term in NON_AUTHORITY_TERMS if term not in lower]


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet-root", default=DEFAULT_PACKET_ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    packet_root = pathlib.Path(args.packet_root)
    results: List[Dict[str, Any]] = []

    if not packet_root.exists():
        results.append(result("packet-root", False, f"missing: {packet_root}"))
        summary = summarize(packet_root, results)
        print_summary(summary, args.json)
        return 1

    for rel in REQUIRED_PACKET_FILES:
        path = packet_root / rel
        results.append(result(f"path:{rel}", path.exists(), "present" if path.exists() else "missing"))

    manifest_path = packet_root / "packet_manifest.json"
    manifest_sha_path = packet_root / "packet_manifest.sha256"
    outer_receipt_path = packet_root / "packet_manifest_outer_receipt.json"

    manifest: Dict[str, Any] = {}
    outer: Dict[str, Any] = {}

    try:
        manifest = load_json(manifest_path)
        results.append(result("manifest:parse", True, "packet_manifest.json parsed"))
    except Exception as exc:
        results.append(result("manifest:parse", False, str(exc)))

    try:
        outer = load_json(outer_receipt_path)
        results.append(result("outer-receipt:parse", True, "packet_manifest_outer_receipt.json parsed"))
    except Exception as exc:
        results.append(result("outer-receipt:parse", False, str(exc)))

    if manifest:
        required_manifest_fields = [
            "manifest_schema_version",
            "trial_id",
            "packet_id",
            "created_at_fixed_fixture_time",
            "generated_from_base_commit",
            "canonicalization_method",
            "artifact_hashes",
            "expected_reconstruction_hash",
            "environment_manifest_hash",
            "non_authority_boundary_statement_hash",
            "non_authority_statement",
        ]
        missing = [field for field in required_manifest_fields if field not in manifest]
        results.append(result("manifest:required-fields", not missing, "missing: " + ", ".join(missing) if missing else "present"))

        missing_terms = has_boundary_terms(str(manifest.get("non_authority_statement", "")))
        results.append(result("manifest:non-authority-terms", not missing_terms, "missing: " + ", ".join(missing_terms) if missing_terms else "present"))

        artifacts = manifest.get("artifact_hashes", [])
        artifact_errors = []
        if not isinstance(artifacts, list) or not artifacts:
            artifact_errors.append("artifact_hashes must be non-empty array")
        else:
            for item in artifacts:
                if not isinstance(item, dict):
                    artifact_errors.append("artifact entry must be object")
                    continue

                rel_path = item.get("path")
                expected_hash = item.get("sha256")

                if not isinstance(rel_path, str) or not rel_path:
                    artifact_errors.append("artifact path missing")
                    continue

                if not isinstance(expected_hash, str) or not re.match(r"^[a-f0-9]{64}$", expected_hash):
                    artifact_errors.append(f"{rel_path}: invalid sha256")
                    continue

                artifact_path = pathlib.Path(rel_path)
                if not artifact_path.exists():
                    artifact_errors.append(f"{rel_path}: missing")
                    continue

                actual_hash = sha256_file(artifact_path)
                if actual_hash != expected_hash:
                    artifact_errors.append(f"{rel_path}: hash mismatch expected {expected_hash} actual {actual_hash}")

        results.append(result("manifest:artifact-hashes", not artifact_errors, "; ".join(artifact_errors) if artifact_errors else "all artifact hashes match"))

        expected_path = packet_root / "expected/day0_expected_reconstruction.json"
        env_path = packet_root / "environment/day0_environment_manifest.json"
        boundary_path = packet_root / "boundary/day0_non_authority_boundary_statement.txt"

        named_hash_checks = [
            ("manifest:expected-reconstruction-hash", expected_path, manifest.get("expected_reconstruction_hash")),
            ("manifest:environment-manifest-hash", env_path, manifest.get("environment_manifest_hash")),
            ("manifest:non-authority-boundary-statement-hash", boundary_path, manifest.get("non_authority_boundary_statement_hash")),
        ]

        for name, path, expected_hash in named_hash_checks:
            if not path.exists():
                results.append(result(name, False, f"missing: {path}"))
            else:
                actual_hash = sha256_file(path)
                results.append(result(name, actual_hash == expected_hash, f"expected {expected_hash} actual {actual_hash}"))

        if boundary_path.exists():
            boundary_text = boundary_path.read_text(encoding="utf-8")
            missing_boundary_terms = has_boundary_terms(boundary_text)
            results.append(result(
                "boundary-statement:non-authority-terms",
                not missing_boundary_terms,
                "missing: " + ", ".join(missing_boundary_terms) if missing_boundary_terms else "present",
            ))

    if manifest_path.exists() and manifest_sha_path.exists():
        actual_manifest_hash = sha256_file(manifest_path)
        sidecar_text = manifest_sha_path.read_text(encoding="utf-8").strip().lower()
        sidecar_ok = actual_manifest_hash in sidecar_text and "packet_manifest.json" in sidecar_text
        results.append(result("manifest-sidecar:sha256", sidecar_ok, f"actual manifest hash {actual_manifest_hash}"))
    else:
        actual_manifest_hash = ""
        results.append(result("manifest-sidecar:sha256", False, "manifest or sidecar missing"))

    if outer:
        outer_hash = str(outer.get("packet_manifest_sha256", "")).lower()
        outer_ok = bool(actual_manifest_hash) and outer_hash == actual_manifest_hash
        results.append(result("outer-receipt:manifest-hash-binding", outer_ok, f"outer {outer_hash} actual {actual_manifest_hash}"))

        missing_outer_terms = has_boundary_terms(str(outer.get("non_authority_statement", "")))
        results.append(result("outer-receipt:non-authority-terms", not missing_outer_terms, "missing: " + ", ".join(missing_outer_terms) if missing_outer_terms else "present"))

    summary = summarize(packet_root, results)
    print_summary(summary, args.json)
    return 0 if summary["failed"] == 0 else 1


def summarize(packet_root: pathlib.Path, results: List[Dict[str, Any]]) -> Dict[str, Any]:
    failed = sum(1 for item in results if not item["passed"])
    return {
        "checker": "check_longitudinal_reconstruction_day0_packet_v0_1.py",
        "packet_root": str(packet_root).replace("\\", "/"),
        "total": len(results),
        "passed": len(results) - failed,
        "failed": failed,
        "results": results,
        "non_authority_statement": (
            "This checker verifies Day-0 packet presence, hash continuity, manifest binding, "
            "and boundary statement presence only; it does not validate truth, compliance, "
            "legal sufficiency, safety, authorization, approval, certification, endorsement, "
            "production readiness, or institutional authority."
        ),
    }


def print_summary(summary: Dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(summary, indent=2, sort_keys=True))
        return

    print(f"Longitudinal Day-0 packet: {summary['passed']}/{summary['total']} passed")
    for item in summary["results"]:
        status = "PASS" if item["passed"] else "FAIL"
        print(f"{status} {item['name']}")
        if not item["passed"] and item["detail"]:
            print(f"  - {item['detail']}")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
'@

$receipt = @'
# Longitudinal Reconstruction Trial Day-0 Packet Receipt v0.1

Status: Day-0 packet receipt.
Trial: fork_longitudinal_reconstruction_trial_v0_1
Packet: LRT_DAY0_PACKET_v0_1

## 1. Purpose

This receipt records creation of the Day-0 packet for Fork's longitudinal reconstruction trial.

The Day-0 packet is the object that later Day-7, Day-30, and Day-90 replay attempts will test.

## 2. Packet Path

- docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/

## 3. Checker

- tools/check_longitudinal_reconstruction_day0_packet_v0_1.py

Run:

- python tools/check_longitudinal_reconstruction_day0_packet_v0_1.py --json

## 4. Packet Boundary

The Day-0 packet is a fixture for longitudinal reconstruction.

It preserves:

- request state;
- output state;
- human review state;
- boundary state;
- non-claims;
- expected reconstruction;
- environment manifest;
- artifact hashes;
- manifest hash sidecar;
- outer receipt.

It does not establish:

- truth;
- compliance;
- legal sufficiency;
- safety;
- authorization;
- approval;
- certification;
- endorsement;
- production readiness;
- institutional authority.

## 5. Current Limitation

The expected reconstruction provenance for v0.1 is author-declared fixture baseline, not independent external reviewer provenance.

This is intentional and must remain visible. Later Day-7, Day-30, and Day-90 replays should not treat this expected reconstruction as independent validation.

## 6. Future Work

Next stages:

- add pinned Day-0 replay checker;
- add current-checker drift comparison;
- add Day-7 replay receipt;
- add Day-30 replay receipt;
- add Day-90 replay receipt;
- add adverse longitudinal variants for packet tamper, manifest tamper, checker drift, and receipt overread.

## 7. Non-Authority Statement

This receipt does not validate Fork, certify Fork, approve Fork, establish legal sufficiency, establish compliance sufficiency, establish safety, establish production readiness, endorse Fork, or transfer authority.
'@

Write-Utf8Lf -Path $schemaPath -Content $schema
Write-Utf8Lf -Path $checkerPath -Content $checker
Write-Utf8Lf -Path $receiptPath -Content $receipt

Write-Utf8Lf -Path $packetReadmePath -Content $packetReadme
Write-Utf8Lf -Path $boundaryStatementPath -Content $nonAuthorityStatement
Write-JsonUtf8Lf -Path $requestRecordPath -Object $requestRecord
Write-JsonUtf8Lf -Path $aiOutputRecordPath -Object $aiOutputRecord
Write-JsonUtf8Lf -Path $humanReviewRecordPath -Object $humanReviewRecord
Write-JsonUtf8Lf -Path $boundaryStateRecordPath -Object $boundaryStateRecord
Write-JsonUtf8Lf -Path $nonClaimsRecordPath -Object $nonClaimsRecord
Write-JsonUtf8Lf -Path $expectedReconstructionPath -Object $expectedReconstruction
Write-JsonUtf8Lf -Path $environmentManifestPath -Object $environmentManifest
Write-JsonUtf8Lf -Path $generationReceiptPath -Object $generationReceipt
Write-JsonUtf8Lf -Path $expectedProvenanceReceiptPath -Object $expectedProvenanceReceipt
Write-JsonUtf8Lf -Path $scopeReceiptPath -Object $scopeReceipt

$artifactSpecs = @(
    @{ path = $packetReadmePath; role = "packet_readme" },
    @{ path = $boundaryStatementPath; role = "non_authority_boundary_statement" },
    @{ path = $requestRecordPath; role = "request_record" },
    @{ path = $aiOutputRecordPath; role = "ai_output_record" },
    @{ path = $humanReviewRecordPath; role = "human_review_record" },
    @{ path = $boundaryStateRecordPath; role = "boundary_state_record" },
    @{ path = $nonClaimsRecordPath; role = "non_claims_record" },
    @{ path = $expectedReconstructionPath; role = "expected_reconstruction" },
    @{ path = $environmentManifestPath; role = "environment_manifest" },
    @{ path = $generationReceiptPath; role = "generation_receipt" },
    @{ path = $expectedProvenanceReceiptPath; role = "expected_reconstruction_provenance_receipt" },
    @{ path = $scopeReceiptPath; role = "packet_scope_receipt" }
)

$artifactHashes = @()
foreach ($spec in $artifactSpecs) {
    $artifactHashes += [ordered]@{
        path = Normalize-PathForManifest -Path $spec.path
        role = $spec.role
        sha256 = Get-Sha256Lower -Path $spec.path
    }
}

$manifest = [ordered]@{
    manifest_schema_version = "0.1"
    trial_id = $trialId
    packet_id = $packetId
    created_at_fixed_fixture_time = $fixtureTime
    generated_from_base_commit = $baseCommit
    canonicalization_method = "file-byte SHA-256 over UTF-8 LF artifacts; JSON emitted by PowerShell ConvertTo-Json with ordered fixture fields; not JCS"
    schema_versions = [ordered]@{
        day0_packet_manifest = "schemas/longitudinal_reconstruction_day0_packet_manifest_v0_1.schema.json"
    }
    checker_versions = [ordered]@{
        day0_packet_checker = "tools/check_longitudinal_reconstruction_day0_packet_v0_1.py"
        public_review_verifier = "scripts/verify_public_review_package_v0_1.ps1"
    }
    artifact_hashes = $artifactHashes
    expected_reconstruction_path = Normalize-PathForManifest -Path $expectedReconstructionPath
    expected_reconstruction_hash = Get-Sha256Lower -Path $expectedReconstructionPath
    environment_manifest_path = Normalize-PathForManifest -Path $environmentManifestPath
    environment_manifest_hash = Get-Sha256Lower -Path $environmentManifestPath
    non_authority_boundary_statement_path = Normalize-PathForManifest -Path $boundaryStatementPath
    non_authority_boundary_statement_hash = Get-Sha256Lower -Path $boundaryStatementPath
    non_authority_statement = $nonAuthorityStatement
}

Write-JsonUtf8Lf -Path $manifestPath -Object $manifest

$manifestHash = Get-Sha256Lower -Path $manifestPath
Write-Utf8Lf -Path $manifestShaPath -Content "$manifestHash  packet_manifest.json`n"

$outerReceipt = [ordered]@{
    receipt_id = "LRT_DAY0_PACKET_MANIFEST_OUTER_RECEIPT_v0_1"
    receipt_type = "packet_manifest_outer_receipt"
    trial_id = $trialId
    packet_id = $packetId
    created_at_fixed_fixture_time = $fixtureTime
    packet_manifest_path = Normalize-PathForManifest -Path $manifestPath
    packet_manifest_sha256 = $manifestHash
    sidecar_path = Normalize-PathForManifest -Path $manifestShaPath
    receipt_role = "outer_manifest_hash_binding"
    receipt_boundary = "Binds the manifest hash outside the manifest so later replay can detect manifest tamper."
    non_authority_statement = $nonAuthorityStatement
}

Write-JsonUtf8Lf -Path $outerReceiptPath -Object $outerReceipt

$verifierPatchNeeded = Test-Path $verifierPath
if ($verifierPatchNeeded) {
    $verifier = Read-Utf8 -Path $verifierPath

    if ($verifier -notlike "*docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/README.md*") {
        $anchor = '    "scripts/verify_public_review_package_v0_1.ps1"'
        $insert = @'
    "scripts/verify_public_review_package_v0_1.ps1",

    "docs/reconstruction/LONGITUDINAL_RECONSTRUCTION_DAY0_PACKET_RECEIPT_v0_1.md",
    "schemas/longitudinal_reconstruction_day0_packet_manifest_v0_1.schema.json",
    "tools/check_longitudinal_reconstruction_day0_packet_v0_1.py",
    "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/README.md",
    "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/packet_manifest.json",
    "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/packet_manifest.sha256",
    "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/packet_manifest_outer_receipt.json",
    "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/boundary/day0_non_authority_boundary_statement.txt",
    "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/evidence/day0_request_record.json",
    "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/evidence/day0_ai_output_record.json",
    "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/evidence/day0_human_review_record.json",
    "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/evidence/day0_boundary_state_record.json",
    "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/evidence/day0_non_claims_record.json",
    "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/expected/day0_expected_reconstruction.json",
    "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/environment/day0_environment_manifest.json",
    "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/receipts/day0_generation_receipt.json",
    "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/receipts/day0_expected_reconstruction_provenance_receipt.json",
    "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/receipts/day0_packet_scope_receipt.json"
'@
        if ($verifier -notlike "*$anchor*") {
            throw "Could not patch public verifier required path list; anchor not found."
        }
        $verifier = $verifier.Replace($anchor, $insert)
    }

    if ($verifier -notlike '*checker:longitudinal-day0*') {
        $insertChecker = @'

    $day0Args = @("tools/check_longitudinal_reconstruction_day0_packet_v0_1.py", "--json")
    $day0Run = Invoke-External -Name "longitudinal-day0" -Command $pythonCommand -Arguments $day0Args
    $day0Passed = $false
    $day0Data = $null

    if ($day0Run.exit_code -eq 0) {
        $day0Data = Convert-JsonOutput -Text $day0Run.output -Name "Longitudinal Day-0 checker"

        $day0Passed = (
            $day0Data.failed -eq 0 -and
            $day0Data.passed -eq $day0Data.total
        )
    }

    [void]$results.Add((New-Result `
        -Name "checker:longitudinal-day0" `
        -Passed $day0Passed `
        -Detail "python tools/check_longitudinal_reconstruction_day0_packet_v0_1.py --json" `
        -Data $day0Data))
'@

        $needle = "`n}`n`nif (-not `$SkipGitChecks) {"
        if ($verifier -notlike "*if (-not `$SkipGitChecks) {*") {
            throw "Could not patch public verifier checker section; git-check anchor not found."
        }
        $verifier = $verifier.Replace($needle, $insertChecker + "`n}`n`nif (-not `$SkipGitChecks) {")
    }

    if ($verifier -notlike "*Longitudinal Day-0 checker:*") {
        $printInsert = @'

    $day0Result = $null
    foreach ($result in $results) {
        if ($result.name -eq "checker:longitudinal-day0") {
            $day0Result = $result
        }
    }

    if ($day0Result -and $day0Result.data) {
        Write-Host ""
        Write-Host "Longitudinal Day-0 checker:"
        Write-Host "  total: $($day0Result.data.total)"
        Write-Host "  passed: $($day0Result.data.passed)"
        Write-Host "  failed: $($day0Result.data.failed)"
    }
'@
        $printNeedle = "`n}`n`nif (`$failed -ne 0) {"
        if ($verifier -like "*$printNeedle*") {
            $verifier = $verifier.Replace($printNeedle, $printInsert + "`n}`n`nif (`$failed -ne 0) {")
        }
    }

    Write-Utf8Lf -Path $verifierPath -Content $verifier
}

$currentProofBlock = @'
## Longitudinal Reconstruction Trial Day-0 packet

The Day-0 packet for the longitudinal reconstruction trial is now present at:

- docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/

The Day-0 packet includes:

- packet manifest;
- manifest SHA-256 sidecar;
- outer receipt binding the manifest hash;
- request record;
- AI output record;
- human review record;
- boundary state record;
- non-claims record;
- expected reconstruction;
- environment manifest;
- non-authority boundary statement;
- Day-0 receipts.

Checker:

- python tools/check_longitudinal_reconstruction_day0_packet_v0_1.py --json

Current limitation:

- the expected reconstruction provenance is an author-declared Day-0 fixture baseline, not independent external reviewer provenance.

Boundary:

- Day-0 packet verification checks presence, hashes, manifest binding, and boundary statements only.
- It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, production readiness, or institutional authority.
'@

$publicIndexBlock = @'
## Longitudinal Reconstruction Trial Day-0 packet

Receipt:

- docs/reconstruction/LONGITUDINAL_RECONSTRUCTION_DAY0_PACKET_RECEIPT_v0_1.md

Packet root:

- docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/

Checker:

- tools/check_longitudinal_reconstruction_day0_packet_v0_1.py

Run:

- python tools/check_longitudinal_reconstruction_day0_packet_v0_1.py --json
'@

$reviewerStartBlock = @'
## Longitudinal Day-0 reconstruction packet

The Day-0 packet for later longitudinal replay is available at:

- docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/

Run:

- python tools/check_longitudinal_reconstruction_day0_packet_v0_1.py --json

This verifies packet presence, artifact hashes, manifest sidecar, outer receipt binding, and boundary statement presence. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, production readiness, or authority.
'@

$quickstartBlock = @'
## Longitudinal Day-0 packet

The Day-0 packet is the first sealed object for later Day-7, Day-30, and Day-90 replay.

Read:

- docs/reconstruction/LONGITUDINAL_RECONSTRUCTION_DAY0_PACKET_RECEIPT_v0_1.md
- docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/README.md

Run:

- python tools/check_longitudinal_reconstruction_day0_packet_v0_1.py --json

Record:

- packet manifest hash;
- outer receipt manifest hash;
- expected reconstruction hash;
- environment manifest hash;
- non-authority boundary statement hash;
- checker result.

Current limitation:

- expected reconstruction provenance is author-declared fixture baseline in v0.1, not independent external reviewer provenance.
'@

Replace-OrAppendBlock `
    -Path "docs/CURRENT_PROOF_SURFACE_v0_1.md" `
    -BlockId "FORK_LONGITUDINAL_DAY0_PACKET" `
    -Content $currentProofBlock

Replace-OrAppendBlock `
    -Path "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md" `
    -BlockId "FORK_LONGITUDINAL_DAY0_PACKET" `
    -Content $publicIndexBlock

Replace-OrAppendBlock `
    -Path "docs/REVIEWER_START_HERE_v0_1.md" `
    -BlockId "FORK_LONGITUDINAL_DAY0_PACKET" `
    -Content $reviewerStartBlock

Replace-OrAppendBlock `
    -Path "docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md" `
    -BlockId "FORK_LONGITUDINAL_DAY0_PACKET" `
    -Content $quickstartBlock

Write-Host ""
Write-Host "Running Longitudinal Day-0 checker..."
Invoke-Python -Args @($checkerPath, "--json")

Write-Host ""
Write-Host "Running expanded public verifier..."
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    throw "Expanded public verifier failed."
}

Write-Host ""
Write-Host "Running boundary-pressure checker with adversarial regression..."
Invoke-Python -Args @("tools/check_boundary_pressure_review_cases_v0_1.py", "--json", "--run-adversarial")

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
Write-Host "  git diff -- docs\reconstruction"
Write-Host "  git diff -- tools\check_longitudinal_reconstruction_day0_packet_v0_1.py"
Write-Host "  git diff -- scripts\verify_public_review_package_v0_1.ps1"
Write-Host "  python tools\check_longitudinal_reconstruction_day0_packet_v0_1.py --json"
Write-Host "  powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1"
Write-Host "  python tools\check_boundary_pressure_review_cases_v0_1.py --json --run-adversarial"
Write-Host "  python tools\check_public_review_round_004_interactions_v0_1.py --json"
Write-Host "  git diff --check"

if ($Commit) {
    Invoke-Git -Args @("add", "--",
        $scriptPath,
        $checkerPath,
        $schemaPath,
        $receiptPath,
        $packetReadmePath,
        $manifestPath,
        $manifestShaPath,
        $outerReceiptPath,
        $boundaryStatementPath,
        $requestRecordPath,
        $aiOutputRecordPath,
        $humanReviewRecordPath,
        $boundaryStateRecordPath,
        $nonClaimsRecordPath,
        $expectedReconstructionPath,
        $environmentManifestPath,
        $generationReceiptPath,
        $expectedProvenanceReceiptPath,
        $scopeReceiptPath,
        $verifierPath,
        "docs/CURRENT_PROOF_SURFACE_v0_1.md",
        "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md",
        "docs/REVIEWER_START_HERE_v0_1.md",
        "docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md"
    )

    Invoke-Git -Args @("diff", "--cached", "--check")
    Invoke-Git -Args @("commit", "-m", "Add longitudinal reconstruction Day-0 packet")

    if ($Push) {
        Invoke-Git -Args @("push")
    }
}

Write-Host ""
Write-Host "Done."