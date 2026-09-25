$externalReturn = Get-Clipboard -Raw

if ([string]::IsNullOrWhiteSpace($externalReturn)) {
    throw "Clipboard is empty."
}

$externalReturnPath = Join-Path `
    $objectRoot `
    "01_EXTERIOR_RECOMPUTATION_RETURN.md"

Write-Utf8NoBom `
    $externalReturnPath `
    $externalReturn

Write-Host "Preserved exterior return:"
Write-Host $externalReturnPath