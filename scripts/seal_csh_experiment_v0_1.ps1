[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("PrepareFreeze", "CreateSignedTag")]
    [string]$Mode,

    [string]$RepoRoot = "",
    [string]$TagName = "csh-v0.1-baseline-freeze"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Resolve-RepoRoot {
    param([string]$Candidate)
    if ($Candidate) { return (Resolve-Path -LiteralPath $Candidate).Path }
    $current = (Get-Location).Path
    while ($current) {
        if ((Test-Path (Join-Path $current ".git")) -and (Test-Path (Join-Path $current "README.md"))) {
            return $current
        }
        $parent = Split-Path -Parent $current
        if ($parent -eq $current) { break }
        $current = $parent
    }
    throw "Repository root not found."
}

function Read-Json {
    param([string]$Path)
    return (Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json)
}

function Write-JsonLf {
    param([string]$Path, [object]$Value)
    $text = $Value | ConvertTo-Json -Depth 100
    $text = ($text -replace "`r`n", "`n") + "`n"
    [System.IO.File]::WriteAllText($Path, $text, $Utf8NoBom)
}

function Get-ArtifactRecord {
    param([string]$AbsolutePath, [string]$Root)
    $relative = $AbsolutePath.Substring($Root.Length).TrimStart("\", "/") -replace "\\", "/"
    return [ordered]@{
        path = $relative
        sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $AbsolutePath).Hash.ToLowerInvariant()
    }
}

function Get-ArtifactRecords {
    param([string[]]$Paths, [string]$Root)
    $records = @()
    foreach ($path in ($Paths | Sort-Object -Unique)) {
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
            throw "Required freeze artifact missing: $path"
        }
        $records += Get-ArtifactRecord -AbsolutePath $path -Root $Root
    }
    return $records
}

$root = Resolve-RepoRoot -Candidate $RepoRoot
Set-Location -LiteralPath $root

$base = Join-Path $root "docs\experiments\cross-system-claim-handoff-v0.1"
$freezePath = Join-Path $base "CORPUS_FREEZE_v0_1.json"
$manifestPath = Join-Path $base "EXPERIMENT_MANIFEST_v0_1.json"
$registryPath = Join-Path $base "SYSTEM_REGISTRY_v0_1.json"
$anchorPath = Join-Path $base "EXPERIMENT_RELEASE_ANCHOR_v0_1.json"

if ($Mode -eq "PrepareFreeze") {
    $registryText = [System.IO.File]::ReadAllText($registryPath, $Utf8NoBom)
    if ($registryText -match "UNASSIGNED") {
        throw "SYSTEM_REGISTRY_v0_1.json still contains UNASSIGNED values. Freeze refused."
    }

    $scenarioPaths = @(Get-ChildItem -LiteralPath (Join-Path $base "corpus") -Filter "SIM_*.json" -File | ForEach-Object FullName)
    if ($scenarioPaths.Count -ne 6) {
        throw "Expected exactly six scenario descriptors; found $($scenarioPaths.Count)."
    }

    $promptPaths = @(Get-ChildItem -LiteralPath (Join-Path $base "prompts") -File |
        Where-Object Name -ne "README.md" | ForEach-Object FullName)
    if ($promptPaths.Count -eq 0) {
        throw "No frozen prompt artifacts found. Add exact prompts before freeze."
    }
    $pairedPromptPaths = @(
        Get-ChildItem -LiteralPath (Join-Path $base "prompts") -Filter "PROMPT_PACKET_SIM_*_v0_1.json" -File |
            ForEach-Object FullName
    )
    if ($pairedPromptPaths.Count -ne 12) {
        throw "Expected exactly twelve paired prompt packets; found $($pairedPromptPaths.Count)."
    }
    foreach ($requiredPromptArtifact in @(
        "SHARED_RECEIVER_INSTRUCTION_v0_1.txt",
        "PAIR_MANIFEST_v0_1.json",
        "RUN_ORDER_v0_1.json"
    )) {
        if (-not (Test-Path -LiteralPath (Join-Path (Join-Path $base "prompts") $requiredPromptArtifact) -PathType Leaf)) {
            throw "Required prompt configuration artifact missing: $requiredPromptArtifact"
        }
    }

    $handoffPaths = @(Get-ChildItem -LiteralPath (Join-Path $base "handoff") -Filter "HANDOFF_SIM_*_v0_1.json" -File |
        ForEach-Object FullName)
    if ($handoffPaths.Count -ne 6) {
        throw "Expected exactly six handoff-state artifacts; found $($handoffPaths.Count)."
    }

    python tools/check_csh_configuration_v0_1.py --json
    if ($LASTEXITCODE -ne 0) {
        throw "CSH configuration checker failed before freeze preparation."
    }

    $schemaRelative = @(

        "schemas/cross_system_claim_handoff_manifest_v0_1.schema.json",
        "schemas/cross_system_claim_handoff_scenario_v0_1.schema.json",
        "schemas/cross_system_claim_handoff_corpus_freeze_v0_1.schema.json",
        "schemas/cross_system_claim_handoff_system_registry_v0_1.schema.json",
        "schemas/cross_system_claim_handoff_state_artifact_v0_1.schema.json",
        "schemas/cross_system_claim_handoff_prompt_packet_v0_1.schema.json",
        "schemas/cross_system_claim_handoff_run_order_v0_1.schema.json",
        "schemas/cross_system_claim_handoff_run_v0_1.schema.json",
        "schemas/cross_system_claim_handoff_result_v0_1.schema.json",
        "schemas/cross_system_claim_handoff_receipt_v0_1.schema.json",
        "schemas/unsupported_inheritance_classifier_input_v0_1.schema.json",
        "schemas/unsupported_inheritance_classification_v0_1.schema.json"
    )
    $checkerRelative = @(
        "tools/check_cross_system_claim_handoff_v0_1.py",
        "tools/check_csh_configuration_v0_1.py",
        "tools/classify_unsupported_inheritance_v0_1.py",
        "tools/validate_json_schema_bundle_v0_1.py"
    )

    $freeze = Read-Json $freezePath
    $manifest = Read-Json $manifestPath
    $registry = Read-Json $registryPath
    $baseCommit = (& git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0 -or $baseCommit -notmatch "^[a-f0-9]{40}$") {
        throw "Could not resolve current Git HEAD."
    }

    $registry.registry_status = "frozen"
    Write-JsonLf -Path $registryPath -Value $registry
    $manifest.freeze_status = "frozen"
    $manifest.status = "frozen_not_executed"
    Write-JsonLf -Path $manifestPath -Value $manifest

    $freeze.freeze_status = "frozen"
    $freeze.freeze_completed_at_utc = [DateTime]::UtcNow.ToString("o")
    $freeze.base_commit_before_freeze = $baseCommit
    $freeze.release_commit = $null
    $freeze.preregistration_sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $base "PREREGISTRATION_v0_1.md")).Hash.ToLowerInvariant()
    $freeze.manifest_sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $manifestPath).Hash.ToLowerInvariant()
    $freeze.system_registry_sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $registryPath).Hash.ToLowerInvariant()
    $freeze.scenario_artifacts = @(Get-ArtifactRecords -Paths $scenarioPaths -Root $root)
    $freeze.prompt_artifacts = @(Get-ArtifactRecords -Paths $promptPaths -Root $root)
    $freeze.handoff_artifacts = @(Get-ArtifactRecords -Paths $handoffPaths -Root $root)
    $freeze.schema_artifacts = @(Get-ArtifactRecords -Paths @($schemaRelative | ForEach-Object { Join-Path $root $_ }) -Root $root)
    $freeze.checker_artifacts = @(Get-ArtifactRecords -Paths @($checkerRelative | ForEach-Object { Join-Path $root $_ }) -Root $root)
    $freeze.blocking_unresolved_items = @()
    $freeze.baseline_execution_permitted = $true

    $manifest.freeze_status = "frozen"
    $manifest.status = "frozen_not_executed"

    Write-JsonLf -Path $freezePath -Value $freeze
    Write-JsonLf -Path $manifestPath -Value $manifest

    python tools/validate_json_schema_bundle_v0_1.py --json
    if ($LASTEXITCODE -ne 0) { throw "Schema bundle failed after freeze preparation." }
    python tools/check_cross_system_claim_handoff_v0_1.py --json
    if ($LASTEXITCODE -ne 0) { throw "CSH checker failed after freeze preparation." }
    python tools/check_csh_configuration_v0_1.py --json
    if ($LASTEXITCODE -ne 0) { throw "CSH configuration checker failed after freeze preparation." }

    Write-Host ""
    Write-Host "CSH_CONTENT_FREEZE_PREPARED"
    Write-Host "Review and commit the freeze changes before creating a signed tag."
    Write-Host "No commit, tag, push, or release was performed."
    exit 0
}

if ($Mode -eq "CreateSignedTag") {
    $status = (& git status --porcelain)
    if ($LASTEXITCODE -ne 0) { throw "git status failed." }
    if ($status) {
        throw "Working tree must be clean before creating the signed tag."
    }

    $freeze = Read-Json $freezePath
    if ($freeze.freeze_status -ne "frozen" -or -not $freeze.baseline_execution_permitted) {
        throw "Corpus freeze is not complete or baseline execution is not permitted."
    }

    $existing = (& git tag --list $TagName).Trim()
    if ($existing) {
        throw "Tag already exists: $TagName"
    }

    $releaseCommit = (& git rev-parse HEAD).Trim()
    & git tag -s $TagName -m "Fork Cross-System Claim Handoff v0.1 baseline freeze"
    if ($LASTEXITCODE -ne 0) {
        throw "Signed tag creation failed. Confirm Git signing configuration."
    }

    $anchor = Read-Json $anchorPath
    $anchor.anchor_status = "signed_tag_created_not_pushed"
    $anchor.subject_commit = $releaseCommit
    $anchor.tag_name = $TagName
    $anchor.tag_created = $true
    $anchor.tag_pushed = $false
    $anchor.external_digest_recorded = $false

    $bound = @(
        "docs/experiments/cross-system-claim-handoff-v0.1/PREREGISTRATION_v0_1.md",
        "docs/experiments/cross-system-claim-handoff-v0.1/EXPERIMENT_MANIFEST_v0_1.json",
        "docs/experiments/cross-system-claim-handoff-v0.1/CORPUS_FREEZE_v0_1.json",
        "docs/experiments/cross-system-claim-handoff-v0.1/SYSTEM_REGISTRY_v0_1.json"
    )
    $anchor.artifacts = @(Get-ArtifactRecords -Paths @($bound | ForEach-Object { Join-Path $root $_ }) -Root $root)
    Write-JsonLf -Path $anchorPath -Value $anchor

    Write-Host ""
    Write-Host "CSH_SIGNED_TAG_CREATED"
    Write-Host "Tag: $TagName"
    Write-Host "Commit: $releaseCommit"
    Write-Host "The tag was not pushed."
    Write-Host "EXPERIMENT_RELEASE_ANCHOR_v0_1.json was updated and is now an uncommitted change."
    Write-Host "Review it separately. No commit or push was performed."
}
