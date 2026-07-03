# scripts/apply_scenario_06_structuralization_v0_1.ps1
# Updates registry, main checker, viewer builder, and regenerates the viewer bundle.
# Does not commit, push, or tag.

$ErrorActionPreference = "Stop"
function Write-Utf8NoBom($Path, $Text) { $utf8NoBom = New-Object System.Text.UTF8Encoding($false); [System.IO.File]::WriteAllText((Resolve-Path $Path), $Text, $utf8NoBom) }
if (-not (Test-Path ".git")) { throw "Run this script from the repository root, e.g. C:\N\fork-public-evidence" }
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw "Python was not found on PATH." }

Write-Host "Patching scenario registry..."
$tempPy = Join-Path $env:TEMP "patch_scenario_06_registry_v0_1.py"
$py = @'
import json
from pathlib import Path
path = Path("examples/simulations/governance-proof-surface/scenario_registry.json")
registry = json.loads(path.read_text(encoding="utf-8"))
scenario_id = "SCENARIO_06_MULTI_SYSTEM_DISTRIBUTED_HANDOFF"
artifact_files = [
  "examples/simulations/governance-proof-surface/artifacts/scenario_06_boundary_delta_record.json",
  "examples/simulations/governance-proof-surface/artifacts/scenario_06_claim_boundary_contract.json",
  "examples/simulations/governance-proof-surface/artifacts/scenario_06_claim_consumption_event.json",
  "examples/simulations/governance-proof-surface/artifacts/scenario_06_system_mapping_receipt.json",
  "examples/simulations/governance-proof-surface/artifacts/scenario_06_distributed_authority_failure_event.json",
  "examples/simulations/governance-proof-surface/artifacts/scenario_06_transition_graph.md",
  "examples/simulations/governance-proof-surface/artifacts/scenario_06_non_claims_panel.md"
]
found = False
for scenario in registry.get("scenarios", []):
    if scenario.get("scenario_id") == scenario_id:
        found = True
        scenario["verification_posture"] = "STRUCTURAL"
        scenario["posture_description"] = "Artifact family present; dedicated checker verifies bounded structural classifications for a distributed multi-system handoff. This does not establish truth, approval, authority, compliance, or correctness."
        scenario["primary_category"] = "MULTI_SYSTEM_DISTRIBUTED_HANDOFF"
        scenario["secondary_categories"] = ["DISTRIBUTED_AUTHORITY_INHERITANCE_ATTEMPT", "CLAIM_SCOPE_EXPANSION", "AUTHORITY_CONTEXT_LOSS", "NON_INHERITANCE"]
        scenario["viewer_treatment"] = "Render as an artifact-backed structural distributed-handoff simulation. Show unsupported authority inheritance and required revalidation without implying approval or compliance."
        scenario["artifact_files"] = artifact_files
        scenario["main_checker"] = {"narrative_file_required": True, "artifact_files_required": True, "json_validation": True, "semantic_classification_assertions": True, "dedicated_checker_invoked": True, "overclaim_scan_covered": True}
if not found:
    raise SystemExit(f"Could not find {scenario_id} in {path}")
path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
'@
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($tempPy, $py, $utf8NoBom)
python $tempPy
Remove-Item $tempPy -Force

Write-Host "Patching main AHI checker..."
$mainChecker = "scripts/run_ahi_sim_v0_1_checks.ps1"
$mainText = Get-Content -Raw -Path $mainChecker
$marker = "# Scenario 06 structuralization validation BEGIN"
if ($mainText -notmatch [regex]::Escape($marker)) {
$block = @'

# Scenario 06 structuralization validation BEGIN
Write-Host ""
Write-Host "Checking Scenario 06 multi-system distributed handoff through main AHI checker..."
& powershell -ExecutionPolicy Bypass -File scripts\check_scenario_06_multi_system_distributed_handoff_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    throw "Scenario 06 checker failed."
}
Write-Host "PASS: Scenario 06 validation completed inside main AHI checker."
# Scenario 06 structuralization validation END

'@
$finalPass = 'Write-Host "PASS: ahi-sim-v0.1.x simulation proof-surface checks completed."'
if ($mainText.Contains($finalPass)) { $mainText = $mainText.Replace($finalPass, $block + $finalPass) } else { $mainText = $mainText.TrimEnd() + "`n" + $block }
Write-Utf8NoBom $mainChecker $mainText
} else { Write-Host "Main checker already contains Scenario 06 structuralization block." }

Write-Host "Patching viewer builder artifact labels..."
$builder = "scripts/build_ahi_viewer_data_v0_1.py"
$builderText = Get-Content -Raw -Path $builder
if ($builderText -notmatch "distributed_authority_failure_event") {
    $builderText = $builderText.Replace('        ("suppressed_limitations_event", "SLE"),', '        ("suppressed_limitations_event", "SLE"),
        ("distributed_authority_failure_event", "DAFE"),')
}
$builderText = $builderText.Replace('            elif atype in ("UIE", "SLE"):', '            elif atype in ("UIE", "SLE", "DAFE"):')
Write-Utf8NoBom $builder $builderText

Write-Host "Regenerating viewer bundle..."
powershell -ExecutionPolicy Bypass -File scripts\build_ahi_viewer_data_v0_1.ps1 -ForceOverwrite
Write-Host ""
Write-Host "Scenario 06 structuralization files and patches applied."
