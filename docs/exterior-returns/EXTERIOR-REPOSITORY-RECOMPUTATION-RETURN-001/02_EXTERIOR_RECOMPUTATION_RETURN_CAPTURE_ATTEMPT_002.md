$externalReturn = Get-Clipboard -Raw

if ([string]::IsNullOrWhiteSpace($externalReturn)) {
    throw "Clipboard is empty."
}

$attempt2Path = Join-Path `
    $objectRoot `
    "02_EXTERIOR_RECOMPUTATION_RETURN_CAPTURE_ATTEMPT_002.md"

Write-Utf8NoBom `
    $attempt2Path `
    $externalReturn

$attempt2Hash = (
    Get-FileHash -Algorithm SHA256 $attempt2Path
).Hash.ToLowerInvariant()

Write-Host ""
Write-Host "Attempt 002:"
Write-Host $attempt2Path

Write-Host "Characters:"
Write-Host $externalReturn.Length

Write-Host "Bytes:"
Write-Host (Get-Item $attempt2Path).Length

Write-Host "SHA-256:"
Write-Host $attempt2Hash