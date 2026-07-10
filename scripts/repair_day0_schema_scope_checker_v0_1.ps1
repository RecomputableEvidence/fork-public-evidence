# scripts/repair_day0_schema_scope_checker_v0_1.ps1
# Repairs brittle Day-0 schema-scope checker logic and completes schema-scope clarification.
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
        Write-Host "Skipping missing target: $Path"
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
        Write-Host "Replaced block in $Path"
    } else {
        $updated = $existing.TrimEnd() + "`n" + $block + "`n"
        Write-Host "Added block in $Path"
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

$repairScriptPath = "scripts/repair_day0_schema_scope_checker_v0_1.ps1"
$schemaScopeScriptPath = "scripts/clarify_day0_schema_presence_vs_enforcement_v0_1.ps1"
$checkerPath = "tools/check_longitudinal_day0_schema_scope_v0_1.py"
$scopeDocPath = "docs/reconstruction/LONGITUDINAL_DAY0_SCHEMA_PRESENCE_VS_ENFORCEMENT_v0_1.md"
$responseReceiptPath = "docs/review/public-rounds/round-005/ROUND005_RESPONSE_SCHEMA_PRESENCE_VS_ENFORCEMENT_v0_1.md"
$verifierPath = "scripts/verify_public_review_package_v0_1.ps1"

if (-not (Test-Path $checkerPath)) {
    throw "Missing checker: $checkerPath. Run clarify_day0_schema_presence_vs_enforcement_v0_1.ps1 once before this repair."
}

$checker = Read-Utf8 -Path $checkerPath

$oldTokens = @'
FORBIDDEN_SCHEMA_ENFORCEMENT_TOKENS = [
    "import jsonschema",
    "from jsonschema",
    "jsonschema.",
    "Draft202012Validator",
    "Draft7Validator",
    "validate(instance",
    "validate(",
]
'@

$newTokens = @'
FORBIDDEN_SCHEMA_ENFORCEMENT_TOKENS = [
    "import jsonschema",
    "from jsonschema",
    "jsonschema.",
    "Draft202012Validator",
    "Draft7Validator",
    "jsonschema.validate",
    ".validate(instance",
    ".validate(",
]
'@

if ($checker -like "*$oldTokens*") {
    $checker = $checker.Replace($oldTokens, $newTokens)
    Write-Host "Replaced overbroad schema-enforcement token list."
} else {
    Write-Host "Exact old token list not found; continuing."
}

$oldFunction = @'
def contains_schema_scope_distinction(text: str) -> bool:
    lower = text.lower()
    required_phrases = [
        "schema presence",
        "schema enforcement",
        "does not mechanically enforce",
        "schema file is present",
    ]
    return all(phrase in lower for phrase in required_phrases)
'@

$newFunction = @'
def contains_schema_scope_distinction(text: str) -> bool:
    lower = text.lower()

    has_presence = (
        "schema presence" in lower
        or "schema artifact: present" in lower
        or "schema file is present" in lower
        or "schema artifact is present" in lower
    )

    has_enforcement = (
        "schema enforcement" in lower
        or "schema-enforcement" in lower
        or "mechanical json schema validation" in lower
    )

    has_not_enforced = (
        "does not mechanically enforce" in lower
        or "not mechanically enforced" in lower
        or "mechanical json schema validation: not implemented" in lower
        or "mechanical json schema validation is not implemented" in lower
        or "not implemented in v0.1" in lower
    )

    return has_presence and has_enforcement and has_not_enforced
'@

if ($checker -like "*$oldFunction*") {
    $checker = $checker.Replace($oldFunction, $newFunction)
    Write-Host "Replaced brittle schema-scope prose matcher."
} else {
    $pattern = '(?s)def contains_schema_scope_distinction\(text: str\) -> bool:.*?\n\n\ndef main'
    if ($checker -match $pattern) {
        $checker = [regex]::Replace($checker, $pattern, $newFunction + "`n`n`ndef main")
        Write-Host "Replaced schema-scope prose matcher by regex."
    } else {
        throw "Could not locate contains_schema_scope_distinction function in $checkerPath"
    }
}

Write-Utf8Lf -Path $checkerPath -Content $checker

$scopeClarificationBlock = @'
## Explicit v0.1 schema-scope sentence

For checker-scope purposes: schema presence is recorded; schema enforcement is not implemented; the schema file is present; the Day-0 checker does not mechanically enforce the schema.

This sentence is intentionally explicit so reviewers and automated scope checks do not confuse schema path coverage with schema validation.
'@

$responseClarificationBlock = @'
## Explicit v0.1 schema-scope sentence

For checker-scope purposes: schema presence is recorded; schema enforcement is not implemented; the schema file is present; the Day-0 checker does not mechanically enforce the schema.

This response clarifies documentation and checker-scope language only. It does not add mechanical JSON Schema validation.
'@

Replace-OrAppendBlock `
    -Path $scopeDocPath `
    -BlockId "FORK_DAY0_SCHEMA_SCOPE_EXPLICIT_SENTENCE" `
    -Content $scopeClarificationBlock

Replace-OrAppendBlock `
    -Path $responseReceiptPath `
    -BlockId "FORK_DAY0_SCHEMA_SCOPE_EXPLICIT_SENTENCE" `
    -Content $responseClarificationBlock

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

if ($Commit) {
    $pathsToAdd = @(
        $repairScriptPath,
        $schemaScopeScriptPath,
        $scopeDocPath,
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

    $existingPaths = @()
    foreach ($path in $pathsToAdd) {
        if (Test-Path $path) {
            $existingPaths += $path
        }
    }

    Invoke-Git -Args (@("add", "--") + $existingPaths)
    Invoke-Git -Args @("diff", "--cached", "--check")
    Invoke-Git -Args @("commit", "-m", "Clarify Day-0 schema presence versus schema enforcement")

    if ($Push) {
        Invoke-Git -Args @("push")
    }
}

Write-Host ""
Write-Host "Done."