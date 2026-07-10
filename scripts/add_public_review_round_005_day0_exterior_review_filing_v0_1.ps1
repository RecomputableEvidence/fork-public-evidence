# scripts/add_public_review_round_005_day0_exterior_review_filing_v0_1.ps1
# Files Public Review Round 005 Day-0 exterior review observation.
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

Assert-RepoRoot

$scriptPath = "scripts/add_public_review_round_005_day0_exterior_review_filing_v0_1.ps1"
$schemaPath = "schemas/public_review_round_005_interaction_v0_1.schema.json"
$templatePath = "docs/templates/PUBLIC_REVIEW_ROUND_005_INTERACTION_TEMPLATE_v0_1.json"
$checkerPath = "tools/check_public_review_round_005_interactions_v0_1.py"

$roundRoot = "docs/review/public-rounds/round-005"
$roundReadmePath = "$roundRoot/README.md"
$synthesisPath = "$roundRoot/PUBLIC_REVIEW_ROUND_005_SYNTHESIS_v0_1.md"
$sourcePath = "$roundRoot/sources/EXTERIOR_REVIEW_LRT_DAY0_PACKET_v0_1.md"
$observationPath = "$roundRoot/observations/ROUND005_OBS_001_claude_lrt_day0_exterior_review_v0_1.json"

$roundId = "public_review_round_005_longitudinal_day0_packet_accessibility_reconstruction_boundary_replay_readiness"
$observationId = "ROUND005_OBS_001_claude_lrt_day0_exterior_review_v0_1"
$reviewedCommitFull = "03f25f0e52109e8545c188c2bcc329fac4f701f7"
$reviewedCommitShort = "03f25f0"

$nonAuthority = "This filing records an exterior access-path review, execution receipt, manual verifier reconstruction receipt, longitudinal Day-0 packet inspection, and adversarial reconstruction observation. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, production readiness, procurement approval, validation, or institutional authority."

$sourceReview = @'
# Exterior Review: Longitudinal Reconstruction Day-0 Packet v0.1

Status: Exterior access-path review, execution receipt, adversarial boundary-pressure observation.
Reviewer: Claude (Anthropic), acting as an outside reviewer with no repository write access.
Repo: RecomputableEvidence/fork-public-evidence
Reviewed object: `docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/`

Scope statement, as instructed by the review requester: this document does not assess Fork as production-ready, legally sufficient, compliant, safe, approved, certified, endorsed, or authoritative. It answers one bounded question: does the Day-0 packet preserve enough evidence for a future reviewer to reconstruct the declared Day-0 state without inheriting the author's authority. Every command below was executed in a fresh clone in a disposable Linux container; nothing here is an opinion about Fork's merit.

## Commit hash reviewed

- HEAD short: `03f25f0`
- HEAD full: `03f25f0e52109e8545c188c2bcc329fac4f701f7`
- Commit date: 2026-07-09 23:19:48 -0700
- Subject: Add longitudinal reconstruction Day-0 packet
- Branch: main, tracking origin/main, working tree clean.
- Packet manifest generated_from_base_commit: `e4555b93e8ce25d974de1c6a300049021862ba90`
- Reviewer confirmed the generated_from_base_commit is HEAD's immediate parent, distance 1.

## Environment

| Item | Value |
|---|---|
| OS | Linux container, Ubuntu 24.04.4 LTS, kernel 6.18.5 |
| Shell | bash 5.2.21 |
| Python | 3.12.3 |
| Git | 2.43.0 |
| PowerShell / pwsh | Not present |

## Public quickstart

Structurally sufficient, but primary verifier path is PowerShell-only. Linux/macOS reviewers without pwsh lack a documented one-command fallback equivalent to `scripts/verify_public_review_package_v0_1.ps1`.

## Expanded verifier

The PowerShell verifier did not run because pwsh was unavailable.

The reviewer manually reconstructed the verifier's checks:

- 50/50 required paths present;
- boundary-pressure checker: 4/4 default, 4/4 adversarial;
- Round 004 checker: 4/4;
- Day-0 checker: 27/27;
- git diff --check and git diff --cached --check: exit 0.

This must be recorded as manual reconstruction, not a verifier run.

## Day-0 checker

The reviewer executed:

- `python3 tools/check_longitudinal_reconstruction_day0_packet_v0_1.py --json`

Result:

- 27/27 passed;
- 0 failed.

Mechanism-level findings:

- Artifact hashes, manifest sidecar, outer receipt binding, expected reconstruction hash, environment manifest hash, and boundary statement hash are real byte-level SHA-256 checks.
- Non-authority language checks are lexical substring checks, not semantic or negation-aware checks.
- generated_from_base_commit is field-presence only; the checker does not call git to confirm the commit exists or is an ancestor.
- The manifest schema is declared and required-present by public verifier path coverage, but the Day-0 checker does not load or enforce the schema.
- Evidence records and receipts receive file-presence and aggregate byte-hash coverage, but not field-level or lexical assertions of their own.

## Manifest, sidecar, and outer receipt

The binding chain was understandable:

- artifact bytes to manifest artifact_hashes;
- manifest bytes to packet_manifest.sha256;
- manifest bytes to packet_manifest_outer_receipt.json packet_manifest_sha256.

Both manifest bindings matched on recomputation.

## Expected reconstruction provenance

The expected reconstruction is clearly marked author-declared, not independent.

However, it is narrower than the protocol section 8 bar. The protocol describes independent hand-authorship, separate implementation, or LLM-generated independently reviewed ground truth, with named artifacts such as source_event_sequence.json and ground_truth_review_receipt.md. The Day-0 packet does not ship those named artifacts and does not claim those methods.

## Future Day-7/30/90 needs

- pinned Day-0 replay checker;
- Day-7, Day-30, Day-90 replay receipts;
- independent expected-reconstruction provenance;
- protocol section 8 named artifacts if the trial intends to conform to that structure;
- external anchoring for the manifest chain;
- field-name reconciliation between protocol and manifest/checker;
- adverse longitudinal fixtures for payload tamper, manifest tamper, policy drift, missing historical reference, and receipt overread.

## Overclaim and overread risk

Direct overclaim in current text was low.

Findings:

- CURRENT_PROOF_SURFACE_v0_1.md still stated Day-0 fixture not yet implemented, while a later appended section stated the Day-0 packet is now present.
- PUBLIC_REVIEW_QUICKSTART_v0_1.md contained the same stale-status contradiction.
- Receipt-overread risk exists if a future reviewer treats byte verification of evidence records as semantic content verification.

## Adversarial cases executed

### Case A: Coordinated re-seal

In a disposable copy, the reviewer edited `receipts/day0_expected_reconstruction_provenance_receipt.json` to falsely claim independent provenance, recomputed that file hash into packet_manifest.json, recomputed packet_manifest.sha256, recomputed packet_manifest_outer_receipt.json, and ran the unmodified Day-0 checker.

Result:

- 27/27 passed;
- 0 failed.

Interpretation:

The checker cannot distinguish never-tampered from tampered-and-consistently-resealed because checks are relative to the current manifest, not to a hash pinned outside the packet at original sealing time.

Suggested outcome codes:

- MANIFEST_INTERNALLY_CONSISTENT_BUT_UNANCHORED
- SEMANTIC_CONTENT_CHANGE_UNDETECTED_BY_LEXICAL_CHECK
- ROOT_OF_TRUST_SCOPE_LIMIT_CONFIRMED

### Case B: Keyword-present authority assertion

The reviewer imported the checker's own has_boundary_terms function and tested it against a sentence containing all required boundary terms while asserting authority rather than disclaiming it.

Result:

- zero missing terms;
- same pass verdict as the real boundary statement.

Interpretation:

The non-authority check is keyword-presence only. It is not semantic or negation-aware.

## Summary

The Day-0 packet passed its checker and is structurally inspectable. The review found useful next-boundary work: cross-platform verifier parity, stale-status repair, protocol-vs-artifact reconciliation, schema enforcement clarification, coordinated re-seal adversarial testing, and lexical-limit documentation or tests.

No item above establishes that Fork is true, compliant, legally sufficient, safe, authorized, approved, certified, endorsed, production-ready, or institutionally authoritative.
'@

$schema = @'
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://recomputableevidence.example/schemas/public_review_round_005_interaction_v0_1.schema.json",
  "title": "Fork Public Review Round 005 Interaction v0.1",
  "type": "object",
  "additionalProperties": true,
  "required": [
    "review_round",
    "observation_id",
    "reviewer_id",
    "reviewer_type",
    "reviewed_object",
    "reviewed_commit",
    "environment",
    "review_classification",
    "evidence_weight",
    "verifier_execution",
    "checker_results",
    "findings",
    "adversarial_cases",
    "recommended_next_actions",
    "non_authority_statement"
  ],
  "properties": {
    "review_round": { "type": "string" },
    "observation_id": { "type": "string" },
    "reviewer_id": { "type": "string" },
    "reviewer_type": { "type": "string" },
    "reviewed_object": { "type": "string" },
    "reviewed_commit": {
      "type": "object",
      "required": [ "short", "full", "subject" ],
      "properties": {
        "short": { "type": "string" },
        "full": {
          "type": "string",
          "pattern": "^[a-f0-9]{40}$"
        },
        "subject": { "type": "string" }
      }
    },
    "environment": { "type": "object" },
    "review_classification": {
      "type": "array",
      "items": { "type": "string" }
    },
    "evidence_weight": { "type": "string" },
    "verifier_execution": { "type": "object" },
    "checker_results": { "type": "object" },
    "findings": {
      "type": "array",
      "items": { "type": "object" }
    },
    "adversarial_cases": {
      "type": "array",
      "items": { "type": "object" }
    },
    "recommended_next_actions": {
      "type": "array",
      "items": { "type": "string" }
    },
    "non_authority_statement": { "type": "string" }
  }
}
'@

$template = [ordered]@{
    review_round = $roundId
    observation_id = ""
    reviewer_id = ""
    reviewer_type = ""
    reviewed_object = "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/"
    reviewed_commit = [ordered]@{
        short = ""
        full = ""
        subject = ""
    }
    environment = [ordered]@{
        os = ""
        shell = ""
        python = ""
        git = ""
        powershell_available = $false
    }
    review_classification = @()
    evidence_weight = ""
    verifier_execution = [ordered]@{
        public_verifier_executed = $false
        manual_reconstruction_performed = $false
        failure_reason = ""
    }
    checker_results = [ordered]@{}
    findings = @()
    adversarial_cases = @()
    recommended_next_actions = @()
    non_authority_statement = $nonAuthority
}

$observation = [ordered]@{
    review_round = $roundId
    observation_id = $observationId
    reviewer_id = "claude"
    reviewer_type = "outside_ai_reviewer_no_repository_write_access"
    source_document = "docs/review/public-rounds/round-005/sources/EXTERIOR_REVIEW_LRT_DAY0_PACKET_v0_1.md"
    reviewed_object = "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/"
    reviewed_commit = [ordered]@{
        short = $reviewedCommitShort
        full = $reviewedCommitFull
        subject = "Add longitudinal reconstruction Day-0 packet"
        branch = "main"
        working_tree = "clean"
        generated_from_base_commit = "e4555b93e8ce25d974de1c6a300049021862ba90"
        generated_from_base_commit_relation = "immediate_parent_of_reviewed_commit_confirmed_by_reviewer"
    }
    environment = [ordered]@{
        os = "Ubuntu 24.04.4 LTS container, kernel 6.18.5"
        shell = "bash 5.2.21"
        python = "3.12.3"
        git = "2.43.0"
        powershell_available = $false
        powershell_note = "pwsh not present and not installable from the review session"
    }
    review_classification = @(
        "exterior access-path review",
        "execution receipt",
        "manual verifier reconstruction receipt",
        "longitudinal Day-0 packet inspection",
        "adversarial reconstruction observation",
        "mixed review"
    )
    evidence_weight = "execution_receipt_plus_manual_reconstruction_plus_adversarial_observation"
    verifier_execution = [ordered]@{
        public_verifier_executed = $false
        verifier_path = "scripts/verify_public_review_package_v0_1.ps1"
        non_execution_reason = "PowerShell/pwsh unavailable in Linux review container"
        manual_reconstruction_performed = $true
        manual_reconstruction_scope = @(
            "required path list extracted from ps1 verifier source",
            "boundary-pressure checker executed directly",
            "Round 004 checker executed directly",
            "Day-0 checker executed directly",
            "git diff checks executed directly"
        )
        manual_reconstruction_result = [ordered]@{
            required_paths_present = "50/50"
            underlying_conditions_satisfied = $true
            classification = "manual reconstruction, not verifier execution"
        }
    }
    checker_results = [ordered]@{
        longitudinal_day0 = [ordered]@{
            command = "python3 tools/check_longitudinal_reconstruction_day0_packet_v0_1.py --json"
            executed = $true
            passed = 27
            failed = 0
            total = 27
        }
        boundary_pressure = [ordered]@{
            command = "python3 tools/check_boundary_pressure_review_cases_v0_1.py --json --run-adversarial"
            executed = $true
            default_passed = 4
            default_failed = 0
            adversarial_passed = 4
            adversarial_failed = 0
        }
        round004 = [ordered]@{
            command = "python3 tools/check_public_review_round_004_interactions_v0_1.py --json"
            executed = $true
            passed = 4
            failed = 0
            total = 4
        }
        git_checks = [ordered]@{
            diff_check_exit_code = 0
            diff_cached_check_exit_code = 0
        }
    }
    positive_confirmations = @(
        "Day-0 checker executed successfully at 27/27.",
        "Manifest, sidecar, and outer receipt binding chain was understandable.",
        "Artifact byte hashes and manifest hash bindings are real SHA-256 checks.",
        "Expected reconstruction is clearly marked author-declared, not independent.",
        "Direct overclaim in current Day-0 packet artifacts was low."
    )
    findings = @(
        [ordered]@{
            finding_id = "ROUND005_FINDING_001_POWERSHELL_ONLY_PRIMARY_VERIFIER"
            severity = "accessibility_gap"
            summary = "The primary one-command public verifier path is PowerShell-only, and the Linux reviewer could not execute it without pwsh."
            reviewer_evidence = "Reviewer manually reconstructed verifier behavior because pwsh was unavailable."
            recommended_response = "Add cross-platform Python public verifier parity path and document Linux/macOS fallback."
        },
        [ordered]@{
            finding_id = "ROUND005_FINDING_002_STALE_DAY0_STATUS_CONTRADICTIONS"
            severity = "documentation_consistency_defect"
            summary = "Read-first documents still contain stale text saying Day-0 fixture is not yet implemented while later sections say the Day-0 packet is present."
            affected_paths = @(
                "docs/CURRENT_PROOF_SURFACE_v0_1.md",
                "docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md"
            )
            recommended_response = "Patch stale status language before building replay claims."
        },
        [ordered]@{
            finding_id = "ROUND005_FINDING_003_PROTOCOL_VS_ARTIFACT_PROVENANCE_GAP"
            severity = "protocol_alignment_gap"
            summary = "Day-0 expected reconstruction is honestly disclosed as author-declared, but it is narrower than the protocol section 8 expected-reconstruction methods and named artifacts."
            recommended_response = "Record author-declared baseline as v0.1 limitation and decide whether to add section 8 artifacts or revise protocol language."
        },
        [ordered]@{
            finding_id = "ROUND005_FINDING_004_SCHEMA_DECLARED_NOT_ENFORCED"
            severity = "checker_scope_gap"
            summary = "The Day-0 manifest schema is declared and required-present, but the Day-0 checker does not mechanically load or enforce it."
            recommended_response = "Clarify schema-present versus schema-enforced, or add schema enforcement."
        },
        [ordered]@{
            finding_id = "ROUND005_FINDING_005_LEXICAL_NON_AUTHORITY_LIMIT"
            severity = "semantic_boundary_gap"
            summary = "Non-authority checks are substring presence checks, not semantic or negation-aware checks."
            recommended_response = "Add lexical-limit receipt and adversarial fixture for authority-asserting text containing required terms."
        },
        [ordered]@{
            finding_id = "ROUND005_FINDING_006_COORDINATED_RESEAL_UNDETECTED"
            severity = "root_of_trust_limitation_confirmed"
            summary = "A falsified provenance receipt plus recomputed manifest, sidecar, and outer receipt still passed the Day-0 checker 27/27."
            recommended_response = "Add coordinated re-seal adversarial case and preserve root-of-trust limitation until external anchoring exists."
        },
        [ordered]@{
            finding_id = "ROUND005_FINDING_007_EVIDENCE_FILE_HASH_VERIFICATION_OVERREAD_RISK"
            severity = "receipt_overread_risk"
            summary = "The checker verifies evidence-file bytes against the manifest but does not semantically verify each evidence record's content."
            recommended_response = "Clarify that evidence-file verification is byte continuity only, not content validation."
        }
    )
    adversarial_cases = @(
        [ordered]@{
            case_id = "ROUND005_ADV_001_COORDINATED_RESEAL"
            executed = $true
            summary = "Reviewer changed expected reconstruction provenance to falsely claim independent review, recomputed artifact hash into manifest, recomputed manifest sidecar and outer receipt, then ran the unmodified Day-0 checker."
            result = "27/27 passed, 0 failed"
            interpretation = "Checker cannot distinguish never-tampered from tampered-and-consistently-resealed without an external root of trust."
            suggested_outcome_codes = @(
                "MANIFEST_INTERNALLY_CONSISTENT_BUT_UNANCHORED",
                "SEMANTIC_CONTENT_CHANGE_UNDETECTED_BY_LEXICAL_CHECK",
                "ROOT_OF_TRUST_SCOPE_LIMIT_CONFIRMED"
            )
        },
        [ordered]@{
            case_id = "ROUND005_ADV_002_KEYWORD_PRESENT_AUTHORITY_ASSERTION"
            executed = $true
            summary = "Reviewer imported the checker's own has_boundary_terms function and tested a sentence containing all required terms while asserting authority."
            result = "zero missing terms"
            interpretation = "Non-authority check is keyword-presence only and can be gamed by authority-asserting language."
            suggested_outcome_codes = @(
                "LEXICAL_BOUNDARY_CHECK_LIMIT_CONFIRMED",
                "NEGATION_AWARENESS_ABSENT",
                "AUTHORITY_ASSERTION_WITH_REQUIRED_TERMS_ACCEPTED"
            )
        }
    )
    future_day7_day30_day90_needs = @(
        "pinned Day-0 replay checker",
        "Day-7 replay receipt",
        "Day-30 replay receipt",
        "Day-90 replay receipt",
        "independent expected-reconstruction provenance",
        "protocol section 8 named artifacts or protocol revision",
        "external anchoring for manifest chain",
        "field-name reconciliation between protocol and manifest",
        "adverse longitudinal fixtures"
    )
    recommended_next_actions = @(
        "File this Round 005 observation before patching findings.",
        "Fix stale Day-0 status contradictions.",
        "Add or document cross-platform Python public verifier parity path.",
        "Add coordinated re-seal adversarial case.",
        "Add lexical non-authority limit receipt or fixture.",
        "Clarify schema-present versus schema-enforced.",
        "Then build Day-0 replay checker and replay receipt."
    )
    non_authority_statement = $nonAuthority
}

$checker = @'
#!/usr/bin/env python3
"""
Fork Public Review Round 005 Interaction Checker v0.1.

Validates structured Round 005 exterior review filings.

This checker validates filing structure only. It does not validate truth,
compliance, legal sufficiency, safety, authorization, approval, certification,
endorsement, production readiness, validation, or institutional authority.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from typing import Any, Dict, List


DEFAULT_ROOT = "docs/review/public-rounds/round-005/observations"

REQUIRED_TOP_LEVEL = [
    "review_round",
    "observation_id",
    "reviewer_id",
    "reviewer_type",
    "reviewed_object",
    "reviewed_commit",
    "environment",
    "review_classification",
    "evidence_weight",
    "verifier_execution",
    "checker_results",
    "findings",
    "adversarial_cases",
    "recommended_next_actions",
    "non_authority_statement",
]

REQUIRED_NON_AUTHORITY_TERMS = [
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


def load_json(path: pathlib.Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be object")
    return data


def check_observation(path: pathlib.Path) -> Dict[str, Any]:
    errors: List[str] = []

    try:
        data = load_json(path)
    except Exception as exc:
        return {
            "path": str(path).replace("\\", "/"),
            "passed": False,
            "errors": [str(exc)],
        }

    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            errors.append(f"missing required field: {key}")

    commit = data.get("reviewed_commit")
    if not isinstance(commit, dict):
        errors.append("reviewed_commit must be object")
    else:
        full = commit.get("full")
        if not isinstance(full, str) or not re.match(r"^[a-f0-9]{40}$", full):
            errors.append("reviewed_commit.full must be 40 lowercase hex characters")

    classifications = data.get("review_classification")
    if not isinstance(classifications, list) or not classifications:
        errors.append("review_classification must be non-empty array")

    findings = data.get("findings")
    if not isinstance(findings, list) or not findings:
        errors.append("findings must be non-empty array")

    adversarial_cases = data.get("adversarial_cases")
    if not isinstance(adversarial_cases, list) or not adversarial_cases:
        errors.append("adversarial_cases must be non-empty array")

    next_actions = data.get("recommended_next_actions")
    if not isinstance(next_actions, list) or not next_actions:
        errors.append("recommended_next_actions must be non-empty array")

    verifier = data.get("verifier_execution")
    if not isinstance(verifier, dict):
        errors.append("verifier_execution must be object")
    else:
        if verifier.get("public_verifier_executed") is False and verifier.get("manual_reconstruction_performed") is not True:
            errors.append("manual reconstruction must be recorded when public verifier did not execute")

    checker_results = data.get("checker_results")
    if not isinstance(checker_results, dict):
        errors.append("checker_results must be object")
    else:
        day0 = checker_results.get("longitudinal_day0")
        if not isinstance(day0, dict):
            errors.append("checker_results.longitudinal_day0 must be object")
        else:
            if day0.get("passed") != 27 or day0.get("failed") != 0:
                errors.append("longitudinal_day0 expected 27 passed and 0 failed for this filing")

    non_auth = str(data.get("non_authority_statement", "")).lower()
    for term in REQUIRED_NON_AUTHORITY_TERMS:
        if term not in non_auth:
            errors.append(f"non_authority_statement missing boundary term: {term}")

    return {
        "path": str(path).replace("\\", "/"),
        "observation_id": data.get("observation_id"),
        "reviewer_id": data.get("reviewer_id"),
        "evidence_weight": data.get("evidence_weight"),
        "passed": not errors,
        "errors": errors,
    }


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--observations-root", default=DEFAULT_ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    root = pathlib.Path(args.observations_root)
    results: List[Dict[str, Any]] = []

    if not root.exists():
        results.append({
            "path": str(root).replace("\\", "/"),
            "passed": False,
            "errors": ["observations root missing"],
        })
    else:
        paths = sorted(root.glob("*.json"))
        if not paths:
            results.append({
                "path": str(root).replace("\\", "/"),
                "passed": False,
                "errors": ["no observation json files found"],
            })
        else:
            results = [check_observation(path) for path in paths]

    failed = sum(1 for item in results if not item["passed"])
    summary = {
        "checker": "check_public_review_round_005_interactions_v0_1.py",
        "round": "public_review_round_005_longitudinal_day0_packet_accessibility_reconstruction_boundary_replay_readiness",
        "observations_root": str(root).replace("\\", "/"),
        "total": len(results),
        "passed": len(results) - failed,
        "failed": failed,
        "results": results,
        "non_authority_statement": (
            "This checker validates Round 005 filing structure only; it does not validate truth, "
            "compliance, legal sufficiency, safety, authorization, approval, certification, "
            "endorsement, production readiness, validation, or institutional authority."
        ),
    }

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"Round 005 filings: {summary['passed']}/{summary['total']} passed")
        for item in results:
            status = "PASS" if item["passed"] else "FAIL"
            print(f"{status} {item.get('observation_id')} {item['path']}")
            for error in item["errors"]:
                print(f"  - {error}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
'@

$roundReadme = @'
# Public Review Round 005

Status: Exterior review filing surface.
Round: Longitudinal Day-0 Packet Accessibility, Reconstruction Boundary, and Replay Readiness Review.

## Scope

Round 005 asks whether an outside reviewer can inspect the public repo, run or reconstruct the verifier/checkers, inspect the Day-0 packet, and determine what can and cannot be reconstructed later without absorbing authority.

It does not ask reviewers to assess Fork as true, compliant, legally sufficient, safe, authorized, approved, certified, endorsed, production-ready, validated, or institutionally authoritative.

## Filed observations

- observations/ROUND005_OBS_001_claude_lrt_day0_exterior_review_v0_1.json

## Source receipts

- sources/EXTERIOR_REVIEW_LRT_DAY0_PACKET_v0_1.md

## Checker

Run from repository root:

- python tools/check_public_review_round_005_interactions_v0_1.py --json

## Key findings preserved

- PowerShell-only primary verifier path created access friction.
- The reviewer manually reconstructed verifier checks rather than running the named verifier.
- Day-0 packet checker passed 27/27.
- Stale Day-0 status contradictions exist in read-first docs.
- Protocol section 8 and the Day-0 packet provenance structure diverge.
- Day-0 schema is declared and present but not enforced by the checker.
- Non-authority language checking is lexical, not semantic.
- Coordinated re-seal passed 27/27 after falsified provenance and recomputed hashes.
- Evidence-file byte verification can be overread as content verification.

## Boundary

This round files exterior observations. It does not convert reviewer execution into endorsement, validation, certification, legal sufficiency, compliance sufficiency, safety, authorization, approval, production readiness, or institutional authority.
'@

$synthesis = @'
# Public Review Round 005 Synthesis v0.1

Status: Initial synthesis.
Round: Longitudinal Day-0 Packet Accessibility, Reconstruction Boundary, and Replay Readiness Review.

## 1. Review received

One exterior review has been filed:

- Claude exterior access-path review, execution receipt, manual verifier reconstruction receipt, Day-0 packet inspection, and adversarial reconstruction observation.

Reviewed commit:

- 03f25f0e52109e8545c188c2bcc329fac4f701f7

Reviewed object:

- docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/

## 2. Positive confirmations

The review confirmed:

- Day-0 checker executed and passed 27/27.
- Boundary-pressure checker passed 4/4 default and 4/4 adversarial.
- Round 004 checker passed 4/4.
- Manifest, sidecar, and outer receipt binding chain was understandable.
- Expected reconstruction is visibly author-declared, not independent.
- Direct overclaim in the Day-0 packet artifacts was low.

## 3. Findings

The review surfaced several concrete boundary and accessibility findings:

1. The primary public verifier path is PowerShell-only.
2. The reviewer manually reconstructed the verifier behavior because pwsh was unavailable.
3. Read-first documentation contains stale Day-0 status contradictions.
4. The Day-0 checker performs real byte and hash checks, but several assertions are lexical or field-presence only.
5. The manifest schema is declared and required-present, but not mechanically enforced by the Day-0 checker.
6. Expected reconstruction provenance is honestly disclosed as author-declared, but narrower than protocol section 8.
7. Coordinated re-seal with falsified provenance passed the unmodified Day-0 checker 27/27.
8. Non-authority checking can be gamed with keyword-present authority-asserting language.
9. Evidence-file hash verification can be overread as semantic content verification.

## 4. Engineering implications

The next work should not proceed directly to Day-0 replay.

First-order response sequence:

1. Fix stale Day-0 status contradictions.
2. Add or document cross-platform verifier parity.
3. File coordinated re-seal as an adverse longitudinal case.
4. File lexical non-authority checker limitation as a boundary-pressure case.
5. Clarify schema-present versus schema-enforced.
6. Then build Day-0 replay checker and replay receipt.

## 5. Non-authority statement

This synthesis records exterior review findings. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, or institutional authority.
'@

Write-Utf8Lf -Path $schemaPath -Content $schema
Write-JsonUtf8Lf -Path $templatePath -Object $template
Write-Utf8Lf -Path $checkerPath -Content $checker
Write-Utf8Lf -Path $roundReadmePath -Content $roundReadme
Write-Utf8Lf -Path $synthesisPath -Content $synthesis
Write-Utf8Lf -Path $sourcePath -Content $sourceReview
Write-JsonUtf8Lf -Path $observationPath -Object $observation

$publicRoundsBlock = @'
## Round 005

Longitudinal Day-0 Packet Accessibility, Reconstruction Boundary, and Replay Readiness Review.

Round directory:

- docs/review/public-rounds/round-005/

Initial filed observation:

- docs/review/public-rounds/round-005/observations/ROUND005_OBS_001_claude_lrt_day0_exterior_review_v0_1.json

Checker:

- python tools/check_public_review_round_005_interactions_v0_1.py --json
'@

$currentProofBlock = @'
## Public Review Round 005 filed observation

Round 005 now preserves an exterior Day-0 packet review.

Filed observation:

- docs/review/public-rounds/round-005/observations/ROUND005_OBS_001_claude_lrt_day0_exterior_review_v0_1.json

Source receipt:

- docs/review/public-rounds/round-005/sources/EXTERIOR_REVIEW_LRT_DAY0_PACKET_v0_1.md

Checker:

- python tools/check_public_review_round_005_interactions_v0_1.py --json

The filed review confirmed Day-0 checker execution and also found access-path and boundary limitations, including PowerShell-only verifier access, stale Day-0 status contradictions, lexical non-authority checking, schema-present-but-not-enforced behavior, and coordinated re-seal risk.

This filing does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, or institutional authority.
'@

$publicIndexBlock = @'
## Public Review Round 005

Round 005 files an exterior review of the Longitudinal Reconstruction Day-0 packet.

Read:

- docs/review/public-rounds/round-005/README.md
- docs/review/public-rounds/round-005/PUBLIC_REVIEW_ROUND_005_SYNTHESIS_v0_1.md
- docs/review/public-rounds/round-005/observations/ROUND005_OBS_001_claude_lrt_day0_exterior_review_v0_1.json
- docs/review/public-rounds/round-005/sources/EXTERIOR_REVIEW_LRT_DAY0_PACKET_v0_1.md

Run:

- python tools/check_public_review_round_005_interactions_v0_1.py --json
'@

$reviewerStartBlock = @'
## Public Review Round 005

A Day-0 exterior review filing is available:

- docs/review/public-rounds/round-005/README.md

The filing records a Linux access-path review where the PowerShell public verifier could not run, but the reviewer manually reconstructed the verifier's underlying checks and executed the Day-0 checker directly.

Run:

- python tools/check_public_review_round_005_interactions_v0_1.py --json
'@

$quickstartBlock = @'
## Round 005 Day-0 exterior review

Round 005 filed a Day-0 exterior review that should be read before designing the Day-0 replay checker:

- docs/review/public-rounds/round-005/PUBLIC_REVIEW_ROUND_005_SYNTHESIS_v0_1.md

Key preserved findings:

- PowerShell-only verifier access needs a cross-platform fallback.
- Day-0 status contradictions need repair.
- Coordinated re-seal risk needs an adverse longitudinal fixture.
- Lexical non-authority checking needs a limit receipt or adversarial fixture.
- Schema-present versus schema-enforced behavior needs clarification.
'@

Replace-OrAppendBlock `
    -Path "docs/review/public-rounds/README.md" `
    -BlockId "FORK_PUBLIC_REVIEW_ROUND_005" `
    -Content $publicRoundsBlock

Replace-OrAppendBlock `
    -Path "docs/CURRENT_PROOF_SURFACE_v0_1.md" `
    -BlockId "FORK_PUBLIC_REVIEW_ROUND_005" `
    -Content $currentProofBlock

Replace-OrAppendBlock `
    -Path "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md" `
    -BlockId "FORK_PUBLIC_REVIEW_ROUND_005" `
    -Content $publicIndexBlock

Replace-OrAppendBlock `
    -Path "docs/REVIEWER_START_HERE_v0_1.md" `
    -BlockId "FORK_PUBLIC_REVIEW_ROUND_005" `
    -Content $reviewerStartBlock

Replace-OrAppendBlock `
    -Path "docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md" `
    -BlockId "FORK_PUBLIC_REVIEW_ROUND_005" `
    -Content $quickstartBlock

Write-Host ""
Write-Host "Running Round 005 interaction checker..."
Invoke-Python -Args @($checkerPath, "--json")

Write-Host ""
Write-Host "Running Day-0 checker..."
Invoke-Python -Args @("tools/check_longitudinal_reconstruction_day0_packet_v0_1.py", "--json")

Write-Host ""
Write-Host "Running public review verifier..."
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    throw "Public review verifier failed."
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
Write-Host "  git diff -- docs\review\public-rounds\round-005"
Write-Host "  git diff -- tools\check_public_review_round_005_interactions_v0_1.py"
Write-Host "  python tools\check_public_review_round_005_interactions_v0_1.py --json"
Write-Host "  python tools\check_longitudinal_reconstruction_day0_packet_v0_1.py --json"
Write-Host "  powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1"
Write-Host "  git diff --check"

if ($Commit) {
    Invoke-Git -Args @("add", "--",
        $scriptPath,
        $schemaPath,
        $templatePath,
        $checkerPath,
        $roundReadmePath,
        $synthesisPath,
        $sourcePath,
        $observationPath,
        "docs/review/public-rounds/README.md",
        "docs/CURRENT_PROOF_SURFACE_v0_1.md",
        "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md",
        "docs/REVIEWER_START_HERE_v0_1.md",
        "docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md"
    )

    Invoke-Git -Args @("diff", "--cached", "--check")
    Invoke-Git -Args @("commit", "-m", "File public review round 005 Day-0 exterior observation")

    if ($Push) {
        Invoke-Git -Args @("push")
    }
}

Write-Host ""
Write-Host "Done."