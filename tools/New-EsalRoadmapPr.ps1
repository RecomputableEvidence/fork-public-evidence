param(
    [string]$BaseBranch = "boundary-delta-record-v0.1",
    [string]$HeadBranch = "esal-v0.1-roadmap-v0_1",
    [string]$Title = "Add ESAL v0.1 roadmap, release record, and conformance documentation"
)

$ErrorActionPreference = "Stop"

Write-Host "== Create ESAL v0.1 Documentation PR =="

if (!(Test-Path ".git")) {
    throw "Run this script from the repository root."
}

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI 'gh' is not installed or not on PATH. Install gh or create the PR manually on GitHub."
}

Write-Host "Checking GitHub authentication..."
gh auth status | Out-Host

Write-Host "Fetching latest remote refs..."
git fetch origin

$Status = git status --short
if ($Status) {
    Write-Host ""
    Write-Host "Working tree is not clean:"
    $Status | Out-Host
    throw "Commit, stash, or discard local changes before creating the PR."
}

$CurrentBranch = (git branch --show-current).Trim()
Write-Host "Current branch: $CurrentBranch"

if ($CurrentBranch -ne $HeadBranch) {
    Write-Host "Switching to $HeadBranch..."
    git switch $HeadBranch
}

Write-Host "Ensuring branch is pushed..."
git push -u origin $HeadBranch

Write-Host ""
Write-Host "Commits that will be included in the PR:"
git log --oneline "origin/$BaseBranch..$HeadBranch" | Out-Host

$CommitCount = (git rev-list --count "origin/$BaseBranch..$HeadBranch").Trim()
if ($CommitCount -eq "0") {
    throw "No commits found between origin/$BaseBranch and $HeadBranch. Nothing to PR."
}

$Body = @"
Adds a post-RC documentation package for ESAL v0.1 on top of the preserved `esal-v0.1-rc6` checkpoint.

This PR does not modify the RC6 tag, oracle behavior, fixtures, verification logic, or release-gate artifact semantics.

Included artifacts:

- `docs/FORK_ESAL_ROADMAP_v0_1.md`
- `reports/ESAL_v0_1_RELEASE_RECORD.md`
- `docs/ESAL_CONFORMANCE_KIT_v0_1.md`
- `docs/ESAL_v0_1_START_HERE.md`
- `reports/ESAL_v0_1_EXPECTED_OUTPUTS.md`
- `docs/FORK_EVIDENCE_BOUNDARY_WALKTHROUGH_v0_1.md`
- `tools/New-EsalV01DocumentationPack.ps1`

Purpose:

- Preserve `esal-v0.1-rc6` as the signed-off release-candidate checkpoint.
- Make ESAL v0.1 easier to retrieve, reproduce, and review.
- Define the conformance comparison surface.
- Record expected fixture-level outputs.
- Provide a reader navigation guide.
- Explain the evidence-boundary story without expanding ESAL into production, compliance, legal sufficiency, authorization, endorsement, or external-governance claims.

Verification rerun before commit:

```text
PASS: 4
G:    3
S:    2
D:    1
```

Permutation invariance rerun before commit:

```text
PASS: 50 permutations preserved canonical hash, state, fingerprint, and classification.
Fingerprint: 6b38d8a5a586052c68cb767a6e44fe583c62e952bf1df54f3f4cf7763870a836
Canonical events hash: a50c88fabb07842722f0251721dab5ed4fc0a175e283c8bdb8e20f7f5cb85878
```

Non-claims:

This PR does not establish production completeness, legal sufficiency, compliance sufficiency, authorization correctness, external governance validity, endorsement, approval, safety, truth, or independent implementation convergence.
"@

$TempBody = New-TemporaryFile
Set-Content -Path $TempBody -Value $Body -Encoding UTF8

Write-Host ""
Write-Host "Checking for existing open PR..."
$ExistingPrUrl = gh pr list `
    --base $BaseBranch `
    --head $HeadBranch `
    --state open `
    --json url `
    --jq '.[0].url'

if ($ExistingPrUrl) {
    Write-Host "Existing PR found:"
    Write-Host $ExistingPrUrl
    Remove-Item $TempBody -Force
    exit 0
}

Write-Host "Creating PR..."
$PrUrl = gh pr create `
    --base $BaseBranch `
    --head $HeadBranch `
    --title $Title `
    --body-file $TempBody

Remove-Item $TempBody -Force

Write-Host ""
Write-Host "PR created:"
Write-Host $PrUrl
