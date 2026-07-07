<#
.SYNOPSIS
Runs a local human recomputation pass over the Boundary-State Interop v0.1.1 evidence packet.
#>

param(
  [Parameter(Mandatory = $true)]
  [string]$EvidencePacketZip,

  [string]$WorkDir = ".\_boundary_state_human_recompute_v0_1_1",

  [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

function Fail([string]$Message) {
  throw "[boundary-human-recompute] $Message"
}

function Info([string]$Message) {
  Write-Host "[boundary-human-recompute] $Message"
}

$EvidencePacketZip = [System.IO.Path]::GetFullPath($EvidencePacketZip)
$WorkDir = [System.IO.Path]::GetFullPath($WorkDir)

if (-not (Test-Path $EvidencePacketZip)) {
  Fail "Evidence packet zip does not exist: $EvidencePacketZip"
}

if (Test-Path $WorkDir) {
  Remove-Item $WorkDir -Recurse -Force
}

New-Item -ItemType Directory -Path $WorkDir | Out-Null

Info "Extracting evidence packet"
Expand-Archive -Path $EvidencePacketZip -DestinationPath $WorkDir -Force

$NestedCheckerZip = Get-ChildItem $WorkDir -Recurse -File -Filter "boundary_state_interop_checker_v0_1_1.zip" |
  Select-Object -First 1

if (-not $NestedCheckerZip) {
  Fail "Could not find nested boundary_state_interop_checker_v0_1_1.zip inside extracted evidence packet."
}

Info ("Extracting nested checker: " + $NestedCheckerZip.Name)
$CheckerDir = Join-Path $WorkDir "checker_v0_1_1_from_source_zip"
New-Item -ItemType Directory -Path $CheckerDir | Out-Null
Expand-Archive -Path $NestedCheckerZip.FullName -DestinationPath $CheckerDir -Force

$CheckerScript = Join-Path $CheckerDir "tools\check_boundary_state_interop_v0_1_1.py"
$ProfileDir = Join-Path $CheckerDir "profile_v0_1_4"
$CanonicalFixtures = Join-Path $ProfileDir "fixtures"

$AdversarialPayloads = Join-Path $CheckerDir "adversarial_payload_pack_v0_1_0\payloads"
$ReviewerFixtures = Join-Path $CheckerDir "reviewer_regressions\fixtures"

if (-not (Test-Path $CheckerScript)) { Fail "Checker script not found: $CheckerScript" }
if (-not (Test-Path $ProfileDir)) { Fail "Profile directory not found: $ProfileDir" }
if (-not (Test-Path $CanonicalFixtures)) { Fail "Canonical fixtures not found: $CanonicalFixtures" }
if (-not (Test-Path $AdversarialPayloads)) { Fail "Adversarial payloads not found: $AdversarialPayloads" }
if (-not (Test-Path $ReviewerFixtures)) { Fail "Reviewer regression fixtures not found: $ReviewerFixtures" }

$ReceiptDir = Join-Path $WorkDir "fresh_receipts"
New-Item -ItemType Directory -Path $ReceiptDir | Out-Null

function Run-CheckerSuite {
  param(
    [string]$Name,
    [string]$FixturesDir,
    [string]$ReceiptName
  )

  $ReceiptPath = Join-Path $ReceiptDir $ReceiptName

  Info "Running $Name suite"

  Push-Location $CheckerDir
  try {
    & $Python ".\tools\check_boundary_state_interop_v0_1_1.py" `
      --packet-dir ".\profile_v0_1_4" `
      --fixtures-dir $FixturesDir `
      --receipt-output $ReceiptPath `
      --json

    if ($LASTEXITCODE -ne 0) {
      Fail "Checker command failed for $ReceiptPath"
    }
  }
  finally {
    Pop-Location
  }

  if (-not (Test-Path $ReceiptPath)) {
    Fail "Expected receipt was not written: $ReceiptPath"
  }
}

Run-CheckerSuite `
  -Name "canonical" `
  -FixturesDir ".\profile_v0_1_4\fixtures" `
  -ReceiptName "canonical_run_receipt_v0_1_1.json"

Run-CheckerSuite `
  -Name "adversarial" `
  -FixturesDir ".\adversarial_payload_pack_v0_1_0\payloads" `
  -ReceiptName "adversarial_run_receipt_v0_1_1.json"

Run-CheckerSuite `
  -Name "reviewer regression" `
  -FixturesDir ".\reviewer_regressions\fixtures" `
  -ReceiptName "reviewer_regression_run_receipt_v0_1_1.json"

Info "Fresh receipts written to: $ReceiptDir"
Info "Human recomputation pass completed."