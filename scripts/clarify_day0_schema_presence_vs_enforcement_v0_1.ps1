# scripts/clarify_day0_schema_presence_vs_enforcement_v0_1.ps1
# Clarifies Day-0 schema presence versus schema enforcement.
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

    if ($verifier -like "*checker:longitudinal-day0-schema-scope*") {
        Write-Host "Verifier already runs longitudinal Day-0 schema-scope checker."
        return
    }

    $checkerBlock = @'

    $day0SchemaScopeArgs = @("tools/check_longitudinal_day0_schema_scope_v0_1.py", "--json")
    $day0SchemaScopeRun = Invoke-External -Name "longitudinal-day0-schema-scope" -Command $pythonCommand -Arguments $day0SchemaScopeArgs
    $day0SchemaScopePassed = $false
    $day0SchemaScopeData = $null

    if ($day0SchemaScopeRun.exit_code -eq 0) {
        $day0SchemaScopeData = Convert-JsonOutput -Text $day0SchemaScopeRun.output -Name "Longitudinal Day-0 schema-scope checker"

        $day0SchemaScopePassed = (
            $day0SchemaScopeData.failed -eq 0 -and
            $day0SchemaScopeData.passed -eq $day0SchemaScopeData.total
        )
    }

    [void]$results.Add((New-Result `
        -Name "checker:longitudinal-day0-schema-scope" `
        -Passed $day0SchemaScopePassed `
        -Detail "python tools/check_longitudinal_day0_schema_scope_v0_1.py --json" `
        -Data $day0SchemaScopeData))
'@

    $anchor = "`nif (-not `$SkipGitChecks) {"
    if ($verifier -like "*$anchor*") {
        $verifier = $verifier.Replace($anchor, $checkerBlock + $anchor)
        Write-Utf8Lf -Path $VerifierPath -Content $verifier
        Write-Host "Inserted longitudinal Day-0 schema-scope checker into public verifier."
        return
    }

    throw "Could not patch public verifier checker section; git-check anchor not found."
}

Assert-RepoRoot

$scriptPath = "scripts/clarify_day0_schema_presence_vs_enforcement_v0_1.ps1"
$schemaScopeDocPath = "docs/reconstruction/LONGITUDINAL_DAY0_SCHEMA_PRESENCE_VS_ENFORCEMENT_v0_1.md"
$responseReceiptPath = "docs/review/public-rounds/round-005/ROUND005_RESPONSE_SCHEMA_PRESENCE_VS_ENFORCEMENT_v0_1.md"
$checkerPath = "tools/check_longitudinal_day0_schema_scope_v0_1.py"
$verifierPath = "scripts/verify_public_review_package_v0_1.ps1"

$schemaScopeDoc = @'
# Longitudinal Day-0 Schema Presence vs Schema Enforcement v0.1

Status: Checker-scope clarification.
Scope: Longitudinal Reconstruction Day-0 packet.

## 1. Purpose

This note clarifies a Day-0 checker-scope distinction surfaced in Public Review Round 005:

- the Day-0 packet manifest schema is present in the repository;
- the schema is routed through the public proof surface;
- the schema file is included in public verifier path coverage;
- the Day-0 checker v0.1 does not mechanically enforce the schema.

This is a scope clarification, not a schema-enforcement upgrade.

## 2. Current schema presence

The Day-0 schema artifact is present at:

- `schemas/longitudinal_reconstruction_day0_packet_manifest_v0_1.schema.json`

The Day-0 packet manifest is present at:

- `docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/packet_manifest.json`

The public verifier requires the schema path to exist.

## 3. Current Day-0 checker behavior

The Day-0 checker currently verifies:

- required packet paths are present;
- `packet_manifest.json` parses as JSON;
- `packet_manifest_outer_receipt.json` parses as JSON;
- required manifest fields are present;
- artifact byte hashes match the manifest;
- expected reconstruction hash matches;
- environment manifest hash matches;
- non-authority boundary statement hash matches;
- manifest sidecar hash matches;
- outer receipt manifest hash binding matches;
- non-authority terms are present in selected text fields.

## 4. What is not currently enforced

The Day-0 checker v0.1 does not currently:

- import `jsonschema`;
- load the Day-0 manifest schema file as a validation schema;
- validate `packet_manifest.json` against the schema;
- validate nested evidence records against schema files;
- validate receipt records against schema files;
- convert schema presence into schema enforcement.

Therefore, reviewer language should avoid saying:

- "the Day-0 manifest is schema-validated";
- "the Day-0 packet is schema-enforced";
- "the Day-0 checker validates the manifest against its JSON Schema";
- "schema presence proves schema conformance."

Permitted language:

- "the schema file is present";
- "the public verifier requires the schema path";
- "the Day-0 checker verifies manifest structure through its own required-field and hash checks";
- "schema enforcement is not implemented in v0.1."

## 5. Future upgrade path

A future schema-enforcement upgrade would require at least:

- explicit schema-validation implementation;
- recorded validator behavior;
- invalid manifest fixture coverage;
- valid manifest fixture coverage;
- public verifier integration;
- updated reviewer-facing language;
- a separate response receipt.

## 6. Boundary statement

This note clarifies checker scope only. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, schema conformance, production readiness, procurement approval, or institutional authority.
'@

$responseReceipt = @'
# Round 005 Response: Schema Presence vs Schema Enforcement v0.1

Status: Engineering response receipt.
Round: Public Review Round 005.
Response class: Checker-scope clarification.

## 1. Finding addressed

Round 005 found that the Day-0 schema is declared and present in the repository, but the Day-0 checker does not mechanically load or enforce the schema.

This response preserves that distinction explicitly.

## 2. Repair

This response adds:

- `docs/reconstruction/LONGITUDINAL_DAY0_SCHEMA_PRESENCE_VS_ENFORCEMENT_v0_1.md`
- `tools/check_longitudinal_day0_schema_scope_v0_1.py`

It also routes the clarification through the public proof surface and public verifier.

## 3. Current status

Current Day-0 schema status:

- schema artifact: present;
- public verifier path coverage: present;
- Day-0 checker required-field checks: present;
- Day-0 checker hash checks: present;
- mechanical JSON Schema validation: not implemented in v0.1.

## 4. Correct reviewer language

A reviewer may say:

- "the schema file is present";
- "the public verifier requires the schema path";
- "the Day-0 checker performs required-field and hash checks."

A reviewer should not say:

- "the Day-0 manifest is schema-validated";
- "the Day-0 schema is mechanically enforced";
- "the Day-0 checker validates the manifest against JSON Schema."

## 5. Non-authority statement

This response clarifies schema-scope language only. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, schema conformance, production readiness, procurement approval, or institutional authority.
'@

$checker = @'
#!/usr/bin/env python3
"""
Fork Longitudinal Day-0 Schema Scope Checker v0.1.

This checker verifies the documentation distinction between schema presence and
schema enforcement for the Day-0 packet.

It confirms the current v0.1 scope:

- schema artifact is present;
- public verifier requires the schema path;
- Day-0 packet manifest is present and parseable;
- Day-0 checker source does not import jsonschema or call known JSON Schema
  validator APIs;
- documentation explicitly says schema presence is not schema enforcement.

This checker does not enforce the Day-0 schema. It does not validate truth,
compliance, legal sufficiency, safety, authorization, approval, certification,
endorsement, validation, schema conformance, production readiness, procurement
approval, or institutional authority.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from typing import Any, Dict, List


SCHEMA_PATH = pathlib.Path("schemas/longitudinal_reconstruction_day0_packet_manifest_v0_1.schema.json")
MANIFEST_PATH = pathlib.Path("docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/packet_manifest.json")
DAY0_CHECKER_PATH = pathlib.Path("tools/check_longitudinal_reconstruction_day0_packet_v0_1.py")
PUBLIC_VERIFIER_PATH = pathlib.Path("scripts/verify_public_review_package_v0_1.ps1")
SCOPE_DOC_PATH = pathlib.Path("docs/reconstruction/LONGITUDINAL_DAY0_SCHEMA_PRESENCE_VS_ENFORCEMENT_v0_1.md")
RESPONSE_RECEIPT_PATH = pathlib.Path("docs/review/public-rounds/round-005/ROUND005_RESPONSE_SCHEMA_PRESENCE_VS_ENFORCEMENT_v0_1.md")

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
    "production readiness",
    "authority",
]

FORBIDDEN_SCHEMA_ENFORCEMENT_TOKENS = [
    "import jsonschema",
    "from jsonschema",
    "jsonschema.",
    "Draft202012Validator",
    "Draft7Validator",
    "validate(instance",
    "validate(",
]


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: pathlib.Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def result(name: str, passed: bool, detail: str, data: Any = None) -> Dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "detail": detail,
        "data": data,
    }


def has_non_authority_terms(text: str) -> List[str]:
    lower = text.lower()
    return [term for term in NON_AUTHORITY_TERMS if term not in lower]


def contains_schema_scope_distinction(text: str) -> bool:
    lower = text.lower()
    required_phrases = [
        "schema presence",
        "schema enforcement",
        "does not mechanically enforce",
        "schema file is present",
    ]
    return all(phrase in lower for phrase in required_phrases)


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    checks: List[Dict[str, Any]] = []

    paths = [
        ("path:schema", SCHEMA_PATH),
        ("path:manifest", MANIFEST_PATH),
        ("path:day0-checker", DAY0_CHECKER_PATH),
        ("path:public-verifier", PUBLIC_VERIFIER_PATH),
        ("path:schema-scope-doc", SCOPE_DOC_PATH),
        ("path:round005-response", RESPONSE_RECEIPT_PATH),
    ]

    for name, path in paths:
        checks.append(result(name, path.is_file(), "present" if path.is_file() else "missing", str(path).replace("\\", "/")))

    schema_data = None
    try:
        schema_data = load_json(SCHEMA_PATH)
        checks.append(result("schema:parse", isinstance(schema_data, dict), "schema parses as JSON object"))
    except Exception as exc:
        checks.append(result("schema:parse", False, str(exc)))

    manifest_data = None
    try:
        manifest_data = load_json(MANIFEST_PATH)
        checks.append(result("manifest:parse", isinstance(manifest_data, dict), "manifest parses as JSON object"))
    except Exception as exc:
        checks.append(result("manifest:parse", False, str(exc)))

    if isinstance(manifest_data, dict):
        schema_like_fields = [key for key in manifest_data.keys() if "schema" in str(key).lower()]
        checks.append(result(
            "manifest:schema-field-present",
            bool(schema_like_fields),
            "manifest contains at least one schema-related field" if schema_like_fields else "manifest has no schema-related field",
            schema_like_fields,
        ))
    else:
        checks.append(result("manifest:schema-field-present", False, "manifest unavailable"))

    try:
        verifier_text = read_text(PUBLIC_VERIFIER_PATH)
        checks.append(result(
            "public-verifier:requires-schema-path",
            str(SCHEMA_PATH).replace("\\", "/") in verifier_text.replace("\\", "/"),
            "public verifier includes schema path",
        ))
        checks.append(result(
            "public-verifier:requires-scope-doc",
            str(SCOPE_DOC_PATH).replace("\\", "/") in verifier_text.replace("\\", "/"),
            "public verifier includes schema-scope doc path",
        ))
        checks.append(result(
            "public-verifier:requires-response-receipt",
            str(RESPONSE_RECEIPT_PATH).replace("\\", "/") in verifier_text.replace("\\", "/"),
            "public verifier includes Round 005 schema response receipt path",
        ))
    except Exception as exc:
        checks.append(result("public-verifier:read", False, str(exc)))

    try:
        day0_checker_text = read_text(DAY0_CHECKER_PATH)
        token_hits = [token for token in FORBIDDEN_SCHEMA_ENFORCEMENT_TOKENS if token in day0_checker_text]
        checks.append(result(
            "day0-checker:no-jsonschema-enforcement-tokens",
            len(token_hits) == 0,
            "no known JSON Schema enforcement token found" if not token_hits else "JSON Schema enforcement token found",
            token_hits,
        ))
        exact_schema_filename = SCHEMA_PATH.name
        checks.append(result(
            "day0-checker:does-not-load-schema-file-by-name",
            exact_schema_filename not in day0_checker_text,
            "Day-0 checker does not reference schema filename directly" if exact_schema_filename not in day0_checker_text else "Day-0 checker references schema filename",
        ))
    except Exception as exc:
        checks.append(result("day0-checker:read", False, str(exc)))

    try:
        scope_doc_text = read_text(SCOPE_DOC_PATH)
        missing_terms = has_non_authority_terms(scope_doc_text)
        checks.append(result(
            "scope-doc:schema-presence-vs-enforcement-language",
            contains_schema_scope_distinction(scope_doc_text),
            "scope distinction language present",
        ))
        checks.append(result(
            "scope-doc:non-authority-terms",
            len(missing_terms) == 0,
            "non-authority terms present" if not missing_terms else "missing non-authority terms",
            missing_terms,
        ))
    except Exception as exc:
        checks.append(result("scope-doc:read", False, str(exc)))

    try:
        response_text = read_text(RESPONSE_RECEIPT_PATH)
        missing_terms = has_non_authority_terms(response_text)
        checks.append(result(
            "round005-response:schema-presence-vs-enforcement-language",
            contains_schema_scope_distinction(response_text),
            "scope distinction language present",
        ))
        checks.append(result(
            "round005-response:non-authority-terms",
            len(missing_terms) == 0,
            "non-authority terms present" if not missing_terms else "missing non-authority terms",
            missing_terms,
        ))
    except Exception as exc:
        checks.append(result("round005-response:read", False, str(exc)))

    failed = sum(1 for item in checks if not item["passed"])

    summary = {
        "checker": "check_longitudinal_day0_schema_scope_v0_1.py",
        "total": len(checks),
        "passed": len(checks) - failed,
        "failed": failed,
        "results": checks,
        "interpretation": (
            "A pass confirms the v0.1 schema-scope distinction is documented: schema presence and public path coverage exist, "
            "but mechanical JSON Schema enforcement is not implemented in the Day-0 checker."
        ),
        "non_authority_statement": (
            "This checker clarifies schema-scope behavior only; it does not validate truth, compliance, legal sufficiency, "
            "safety, authorization, approval, certification, endorsement, validation, schema conformance, "
            "production readiness, procurement approval, or institutional authority."
        ),
    }

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"Longitudinal Day-0 schema-scope checks: {summary['passed']}/{summary['total']} passed")
        for item in checks:
            status = "PASS" if item["passed"] else "FAIL"
            print(f"{status} {item['name']}: {item['detail']}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
'@

Write-Utf8Lf -Path $schemaScopeDocPath -Content $schemaScopeDoc
Write-Utf8Lf -Path $responseReceiptPath -Content $responseReceipt
Write-Utf8Lf -Path $checkerPath -Content $checker

$routingBlock = @'
## Day-0 schema presence versus schema enforcement

Round 005 found that the Day-0 schema is present but not mechanically enforced by the Day-0 checker.

Clarification:

- `docs/reconstruction/LONGITUDINAL_DAY0_SCHEMA_PRESENCE_VS_ENFORCEMENT_v0_1.md`

Response receipt:

- `docs/review/public-rounds/round-005/ROUND005_RESPONSE_SCHEMA_PRESENCE_VS_ENFORCEMENT_v0_1.md`

Checker:

- `tools/check_longitudinal_day0_schema_scope_v0_1.py`

Run:

- `python tools/check_longitudinal_day0_schema_scope_v0_1.py --json`

Correct language:

- schema file present;
- public verifier path coverage present;
- Day-0 checker required-field/hash checks present;
- mechanical JSON Schema enforcement not implemented in v0.1.

Do not describe the Day-0 manifest as schema-validated unless a future schema-enforcement upgrade is added.
'@

$round005Block = @'
## Round 005 response: schema presence versus schema enforcement

The schema-presence finding from Round 005 is now clarified.

Response receipt:

- `docs/review/public-rounds/round-005/ROUND005_RESPONSE_SCHEMA_PRESENCE_VS_ENFORCEMENT_v0_1.md`

Clarification:

- `docs/reconstruction/LONGITUDINAL_DAY0_SCHEMA_PRESENCE_VS_ENFORCEMENT_v0_1.md`

Checker:

- `python tools/check_longitudinal_day0_schema_scope_v0_1.py --json`

This response clarifies that the Day-0 schema is present and routed, but not mechanically enforced by the Day-0 checker in v0.1.
'@

Replace-OrAppendBlock -Path "README.md" -BlockId "FORK_LONGITUDINAL_DAY0_SCHEMA_SCOPE" -Content $routingBlock
Replace-OrAppendBlock -Path "docs/CURRENT_PROOF_SURFACE_v0_1.md" -BlockId "FORK_LONGITUDINAL_DAY0_SCHEMA_SCOPE" -Content $routingBlock
Replace-OrAppendBlock -Path "docs/REVIEWER_START_HERE_v0_1.md" -BlockId "FORK_LONGITUDINAL_DAY0_SCHEMA_SCOPE" -Content $routingBlock
Replace-OrAppendBlock -Path "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md" -BlockId "FORK_LONGITUDINAL_DAY0_SCHEMA_SCOPE" -Content $routingBlock
Replace-OrAppendBlock -Path "docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md" -BlockId "FORK_LONGITUDINAL_DAY0_SCHEMA_SCOPE" -Content $routingBlock
Replace-OrAppendBlock -Path "docs/review/public-rounds/round-005/README.md" -BlockId "FORK_ROUND005_SCHEMA_SCOPE_RESPONSE" -Content $round005Block
Replace-OrAppendBlock -Path "docs/review/public-rounds/round-005/PUBLIC_REVIEW_ROUND_005_SYNTHESIS_v0_1.md" -BlockId "FORK_ROUND005_SCHEMA_SCOPE_RESPONSE" -Content $round005Block

Ensure-VerifierPath -VerifierPath $verifierPath -PathToRequire "docs/reconstruction/LONGITUDINAL_DAY0_SCHEMA_PRESENCE_VS_ENFORCEMENT_v0_1.md"
Ensure-VerifierPath -VerifierPath $verifierPath -PathToRequire "docs/review/public-rounds/round-005/ROUND005_RESPONSE_SCHEMA_PRESENCE_VS_ENFORCEMENT_v0_1.md"
Ensure-VerifierPath -VerifierPath $verifierPath -PathToRequire "tools/check_longitudinal_day0_schema_scope_v0_1.py"
Ensure-VerifierChecker -VerifierPath $verifierPath

Write-Host ""
Write-Host "Running Day-0 schema-scope checker..."
Invoke-Python -Args @($checkerPath, "--json")

Write-Host ""
Write-Host "Running Day-0 checker..."
Invoke-Python -Args @("tools/check_longitudinal_reconstruction_day0_packet_v0_1.py", "--json")

Write-Host ""
Write-Host "Running longitudinal Day-0 adversarial checker..."
Invoke-Python -Args @("tools/check_longitudinal_day0_adversarial_cases_v0_1.py", "--json")

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
Write-Host "  git diff -- docs\reconstruction\LONGITUDINAL_DAY0_SCHEMA_PRESENCE_VS_ENFORCEMENT_v0_1.md"
Write-Host "  git diff -- docs\review\public-rounds\round-005\ROUND005_RESPONSE_SCHEMA_PRESENCE_VS_ENFORCEMENT_v0_1.md"
Write-Host "  git diff -- tools\check_longitudinal_day0_schema_scope_v0_1.py"
Write-Host "  git diff -- scripts\verify_public_review_package_v0_1.ps1"
Write-Host "  python tools\check_longitudinal_day0_schema_scope_v0_1.py --json"
Write-Host "  python tools\check_longitudinal_reconstruction_day0_packet_v0_1.py --json"
Write-Host "  python tools\check_longitudinal_day0_adversarial_cases_v0_1.py --json"
Write-Host "  powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1"
Write-Host "  git diff --check"

if ($Commit) {
    Invoke-Git -Args @("add", "--",
        $scriptPath,
        $schemaScopeDocPath,
        $responseReceiptPath,
        $checkerPath,
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
    Invoke-Git -Args @("commit", "-m", "Clarify Day-0 schema presence versus schema enforcement")

    if ($Push) {
        Invoke-Git -Args @("push")
    }
}

Write-Host ""
Write-Host "Done."