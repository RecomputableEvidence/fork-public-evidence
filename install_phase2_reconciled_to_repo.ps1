param(
    [string]$RepoPath = "C:\N\fork-public-evidence",
    [string]$BranchName = "research/fork-standards-architecture-v0-1-1",
    [switch]$Commit,
    [switch]$Push
)

$ErrorActionPreference = "Stop"

function Fail($Message) {
    throw $Message
}

if (-not (Test-Path $RepoPath)) {
    Fail "Repo path does not exist: $RepoPath"
}

$Source = Join-Path $PSScriptRoot "research"
$Dest = Join-Path $RepoPath "research"

if (-not (Test-Path $Source)) {
    Fail "Source research directory not found beside this script: $Source"
}

Push-Location $RepoPath
try {
    $inside = git rev-parse --is-inside-work-tree 2>$null
    if ($LASTEXITCODE -ne 0 -or $inside.Trim() -ne "true") {
        Fail "RepoPath is not a Git work tree: $RepoPath"
    }

    $status = git status --porcelain
    if ($status) {
        Write-Host "Working tree is not clean:" -ForegroundColor Yellow
        $status | Out-Host
        Fail "Commit, stash, or clean existing changes before installing this research-track bundle."
    }

    git rev-parse --verify --quiet $BranchName *> $null
    if ($LASTEXITCODE -eq 0) {
        git checkout $BranchName
    } else {
        git checkout -b $BranchName
    }

    New-Item -ItemType Directory -Force -Path $Dest | Out-Null
    Copy-Item -Path (Join-Path $Source "*") -Destination $Dest -Recurse -Force

    git add research/standards

    if ($Commit) {
        git commit -m "Add Fork Phase 2 standards handoff chain extension v0.1.1"
    } else {
        Write-Host "Files staged. Re-run with -Commit to commit."
    }

    if ($Push) {
        git push -u origin $BranchName
    }
}
finally {
    Pop-Location
}
