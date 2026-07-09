[CmdletBinding()]
param(
    [string]$RepoRoot = "C:\N\fork-public-evidence",
    [string]$Branch = "research/fork-standards-architecture-v0-1",
    [switch]$NoBranch,
    [switch]$Commit,
    [switch]$Push,
    [string]$CommitMessage = "Add Fork standards architecture phase 1"
)
Set-StrictMode -Version 2.0
$ErrorActionPreference = "Stop"
function Fail($Message) { throw $Message }
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PackageRoot = Resolve-Path (Join-Path $ScriptDir "..\..\..")
$SourceResearch = Join-Path $PackageRoot "research"
if (!(Test-Path $SourceResearch)) { Fail "Source research directory not found: $SourceResearch" }
if (!(Test-Path $RepoRoot)) { Fail "Repo root not found: $RepoRoot" }
Push-Location $RepoRoot
try {
    git rev-parse --show-toplevel *> $null
    if ($LASTEXITCODE -ne 0) { Fail "Target is not a Git repository: $RepoRoot" }
    if (!$NoBranch) {
        $Existing = git branch --list $Branch
        if ($Existing) { git checkout $Branch } else { git checkout -b $Branch }
        if ($LASTEXITCODE -ne 0) { Fail "Failed to checkout/create branch: $Branch" }
    }
    $TargetResearch = Join-Path $RepoRoot "research"
    if (!(Test-Path $TargetResearch)) { New-Item -ItemType Directory -Path $TargetResearch | Out-Null }
    Copy-Item -Path (Join-Path $SourceResearch "*") -Destination $TargetResearch -Recurse -Force
    $Verifier = Join-Path $RepoRoot "research\standards\scripts\verify_handoff_chain.py"
    python $Verifier
    if ($LASTEXITCODE -ne 0) { Fail "Handoff chain verification failed after install." }
    git add research/standards
    if ($Commit) {
        $Status = git status --porcelain
        if ($Status) { git commit -m $CommitMessage } else { Write-Host "No changes to commit." }
    } else { Write-Host "Files staged. Re-run with -Commit to commit automatically." }
    if ($Push) { git push -u origin $Branch }
    Write-Host "Phase 1 standards package installed successfully."
} finally { Pop-Location }
