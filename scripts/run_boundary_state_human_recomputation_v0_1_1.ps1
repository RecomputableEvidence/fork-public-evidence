<#
.SYNOPSIS
  Runs a local human recomputation pass over the Boundary-State Interop v0.1.1 evidence packet.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$EvidencePacketZip,
    [string]$WorkDir = ".human-recomputation-work\boundary-state-interop-v0.1.1",
    [string]$Python = "python"
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = "Stop"

function Fail([string]$Message) { throw "[boundary-human-recompute] $Message" }
function Say([string]$Message) { Write-Host "[boundary-human-recompute] $Message" }
function Sha([string]$Path) { return (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant() }
function Utf8NoBom() { return New-Object System.Text.UTF8Encoding($false) }
function WriteJson([string]$Path, [object]$Object) {
    $dir = Split-Path -Parent $Path
    if ($dir -and -not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
    [System.IO.File]::WriteAllText($Path, (($Object | ConvertTo-Json -Depth 80) + "`n"), (Utf8NoBom))
}
function VerifySha256Sums([string]$Root, [string]$ManifestRel) {
    $manifest = Join-Path $Root $ManifestRel
    if (-not (Test-Path -LiteralPath $manifest)) { Fail "SHA256 manifest not found: $manifest" }
    $ok = 0; $bad = 0; $missing = 0
    foreach ($rawLine in (Get-Content -LiteralPath $manifest)) {
        $line = $rawLine.Trim()
        if (-not $line) { continue }
        $parts = $line -split "\s+", 2
        if ($parts.Count -ne 2) { continue }
        $expected = $parts[0].ToLowerInvariant()
        $rel = $parts[1].Trim().TrimStart("*").Replace("/", "\")
        $path = Join-Path $Root $rel
        if (-not (Test-Path -LiteralPath $path)) { $missing = $missing + 1; continue }
        $actual = Sha $path
        if ($actual -eq $expected) { $ok = $ok + 1 } else { $bad = $bad + 1 }
    }
    return [ordered]@{ ok = $ok; bad = $bad; missing = $missing; manifest = $ManifestRel }
}
function CompareReceipt([string]$PacketRoot, [string]$ReceiptRel, [string]$FreshPath) {
    $packaged = Join-Path $PacketRoot $ReceiptRel
    if (-not (Test-Path -LiteralPath $packaged)) {
        return [ordered]@{ packaged_receipt = $ReceiptRel; packaged_found = $false; byte_identical = $false }
    }
    $packagedSha = Sha $packaged
    $freshSha = Sha $FreshPath
    return [ordered]@{
        packaged_receipt = $ReceiptRel
        packaged_found = $true
        packaged_sha256 = $packagedSha
        fresh_sha256 = $freshSha
        byte_identical = ($packagedSha -eq $freshSha)
    }
}
function RunChecker([string]$CheckerRoot, [string[]]$Args, [string]$OutFile) {
    $tool = Join-Path $CheckerRoot "tools\check_boundary_state_interop_v0_1_1.py"
    if (-not (Test-Path -LiteralPath $tool)) { Fail "Checker tool not found: $tool" }
    $psiArgs = @($tool) + $Args + @("--json")
    $outputLines = & $Python @psiArgs
    if ($LASTEXITCODE -ne 0) { Fail "Checker command failed for $OutFile" }
    $text = ($outputLines -join "`n") + "`n"
    [System.IO.File]::WriteAllText($OutFile, $text, (Utf8NoBom))
    return $text | ConvertFrom-Json
}

if (-not (Test-Path -LiteralPath $EvidencePacketZip)) { Fail "Evidence packet zip not found: $EvidencePacketZip" }
if (Test-Path -LiteralPath $WorkDir) { Remove-Item -LiteralPath $WorkDir -Recurse -Force }
New-Item -ItemType Directory -Force -Path $WorkDir | Out-Null

$packetRoot = Join-Path $WorkDir "evidence_packet"
$checkerRoot = Join-Path $WorkDir "checker_v0_1_1"
$outRoot = Join-Path $WorkDir "fresh_receipts"
New-Item -ItemType Directory -Force -Path $outRoot | Out-Null

Say "Extracting evidence packet"
Expand-Archive -LiteralPath $EvidencePacketZip -DestinationPath $packetRoot -Force

$topSha = VerifySha256Sums -Root $packetRoot -ManifestRel "SHA256SUMS.txt"

$checkerZip = Get-ChildItem -LiteralPath $packetRoot -Recurse -File -Filter "boundary_state_interop_checker_v0_1_1.zip" | Select-Object -First 1
if ($null -eq $checkerZip) { Fail "Nested checker source zip not found in evidence packet." }
Say "Extracting nested checker: $($checkerZip.Name)"
Expand-Archive -LiteralPath $checkerZip.FullName -DestinationPath $checkerRoot -Force

# Some zips contain a top-level checker_v0_1_1 directory; normalize root.
$maybeNested = Join-Path $checkerRoot "checker_v0_1_1"
if (Test-Path -LiteralPath $maybeNested) { $checkerRoot = $maybeNested }

$checkerSha = $null
$checkerShaFile = Join-Path $checkerRoot "SHA256SUMS.txt"
if (Test-Path -LiteralPath $checkerShaFile) {
    $checkerSha = VerifySha256Sums -Root $checkerRoot -ManifestRel "SHA256SUMS.txt"
}

$profile = Join-Path $checkerRoot "profile_v0_1_4"
$fixtures = Join-Path $profile "fixtures"
$adversarial = Join-Path $checkerRoot "adversarial_payload_pack_v0_1_0\payloads"
$reviewer = Join-Path $checkerRoot "reviewer_regressions\fixtures"

Say "Running canonical suite"
$canonicalOut = Join-Path $outRoot "canonical_run_receipt_v0_1_1.json"
$canonical = RunChecker -CheckerRoot $checkerRoot -Args @("--packet-dir", $profile, "--fixtures-dir", $fixtures) -OutFile $canonicalOut

Say "Running adversarial suite"
$adversarialOut = Join-Path $outRoot "adversarial_run_receipt_v0_1_1.json"
$adversarialResult = RunChecker -CheckerRoot $checkerRoot -Args @("--packet-dir", $profile, "--fixtures-dir", $adversarial) -OutFile $adversarialOut

Say "Running reviewer regression suite"
$reviewerOut = Join-Path $outRoot "reviewer_regression_run_receipt_v0_1_1.json"
$reviewerResult = RunChecker -CheckerRoot $checkerRoot -Args @("--packet-dir", $profile, "--fixtures-dir", $reviewer) -OutFile $reviewerOut

Say "Running PYTHONHASHSEED determinism probe"
$fixture13 = Join-Path $fixtures "13_invalid_authority_alias_reference_v0_1_4.json"
$seedHashes = @()
foreach ($seed in @(1,2,3)) {
    $env:PYTHONHASHSEED = [string]$seed
    $seedOut = Join-Path $outRoot ("fixture13_seed_{0}.json" -f $seed)
    [void](RunChecker -CheckerRoot $checkerRoot -Args @("--packet-dir", $profile, "--fixture", $fixture13) -OutFile $seedOut)
    $seedHashes += [ordered]@{ seed = $seed; sha256 = (Sha $seedOut) }
}
Remove-Item Env:\PYTHONHASHSEED -ErrorAction SilentlyContinue

$receipt = [ordered]@{
    receipt_id = "HUMAN_RECOMPUTATION_RUN_RECEIPT_BOUNDARY_STATE_INTEROP_v0_1_1"
    generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    evidence_packet_zip = (Resolve-Path -LiteralPath $EvidencePacketZip).Path
    evidence_packet_zip_sha256 = (Sha $EvidencePacketZip)
    top_level_sha256 = $topSha
    checker_sha256 = $checkerSha
    suite_results = [ordered]@{
        canonical = [ordered]@{ fixture_count = $canonical.fixture_count; passed_count = $canonical.passed_count; failed_count = $canonical.failed_count; all_passed = $canonical.all_passed; receipt = $canonicalOut; receipt_sha256 = (Sha $canonicalOut); packaged_comparison = (CompareReceipt -PacketRoot $packetRoot -ReceiptRel "receipts\canonical_run_receipt_v0_1_1.json" -FreshPath $canonicalOut) }
        adversarial = [ordered]@{ fixture_count = $adversarialResult.fixture_count; passed_count = $adversarialResult.passed_count; failed_count = $adversarialResult.failed_count; all_passed = $adversarialResult.all_passed; receipt = $adversarialOut; receipt_sha256 = (Sha $adversarialOut); packaged_comparison = (CompareReceipt -PacketRoot $packetRoot -ReceiptRel "receipts\adversarial_run_receipt_v0_1_1.json" -FreshPath $adversarialOut) }
        reviewer_regression = [ordered]@{ fixture_count = $reviewerResult.fixture_count; passed_count = $reviewerResult.passed_count; failed_count = $reviewerResult.failed_count; all_passed = $reviewerResult.all_passed; receipt = $reviewerOut; receipt_sha256 = (Sha $reviewerOut); packaged_comparison = (CompareReceipt -PacketRoot $packetRoot -ReceiptRel "receipts\reviewer_regression_run_receipt_v0_1_1.json" -FreshPath $reviewerOut) }
    }
    hash_seed_probe = [ordered]@{
        runs = $seedHashes
        deterministic = (($seedHashes | Select-Object -ExpandProperty sha256 -Unique).Count -eq 1)
    }
    non_claims = @(
        "does not establish legal sufficiency",
        "does not establish compliance sufficiency",
        "does not establish safety",
        "does not establish truth or correctness",
        "does not establish production readiness",
        "does not establish reliance sufficiency",
        "does not establish adversarial exhaustiveness"
    )
}
$receiptPath = Join-Path $outRoot "human_recomputation_run_receipt_v0_1_1.json"
WriteJson -Path $receiptPath -Object $receipt
Say "Wrote $receiptPath"
$receipt | ConvertTo-Json -Depth 80