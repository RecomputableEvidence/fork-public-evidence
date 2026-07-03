# scripts/apply_scenario_06_semantic_verification_v0_1.ps1
# Promotes Scenario 06 to SEMANTICALLY_VERIFIED after semantic invariant checks pass.
# Patches scenario_registry.json and run_ahi_sim_v0_1_checks.ps1, then regenerates the deterministic viewer bundle.
# Does not commit, push, or tag.

$ErrorActionPreference = "Stop"

function Write-Utf8NoBom($Path, $Text) {
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText((Resolve-Path $Path), $Text, $utf8NoBom)
}

if (-not (Test-Path ".git")) { throw "Run from repository root." }
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw "Python was not found on PATH." }

Write-Host "Running Scenario 06 semantic invariant checker before promotion..."
powershell -ExecutionPolicy Bypass -File scripts\check_scenario_06_semantic_invariants_v0_1.ps1
if ($LASTEXITCODE -ne 0) { throw "Semantic checker failed. Registry was not promoted." }

Write-Host "Promoting Scenario 06 registry posture to SEMANTICALLY_VERIFIED..."
$tempPy = Join-Path $env:TEMP "patch_s06_semantic_registry.py"
$py = @'
import json
from pathlib import Path

path = Path("examples/simulations/governance-proof-surface/scenario_registry.json")
registry = json.loads(path.read_text(encoding="utf-8"))
sid = "SCENARIO_06_MULTI_SYSTEM_DISTRIBUTED_HANDOFF"

for scenario in registry.get("scenarios", []):
    if scenario.get("scenario_id") == sid:
        scenario["verification_posture"] = "SEMANTICALLY_VERIFIED"
        scenario["posture_description"] = (
            "Artifact family present; dedicated structural checker and semantic invariant checker verify bounded "
            "distributed-handoff classifications. This does not establish truth, approval, authority, compliance, "
            "legal sufficiency, execution eligibility, or correctness."
        )
        checker = scenario.setdefault("main_checker", {})
        checker["semantic_invariant_checker_invoked"] = True
        checker["semantic_invariants_checked"] = [
            "two_boundary_distributed_transition_chain",
            "preserved_with_narrowing_without_authority_transfer",
            "unsupported_authority_inheritance_attempt_recorded",
            "expanded_consumption_requires_separate_authority_contract",
            "unsupported_mapping_recorded",
            "failure_event_not_supported",
            "required_revalidation_preserved",
            "non_authority_posture_preserved"
        ]
        break
else:
    raise SystemExit(f"Could not find {sid}")

path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
'@

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($tempPy, $py, $utf8NoBom)
python $tempPy
Remove-Item $tempPy -Force

Write-Host "Patching main AHI checker..."
$mainChecker = "scripts/run_ahi_sim_v0_1_checks.ps1"
$mainText = Get-Content -Raw -Path $mainChecker
$marker = "# Scenario 06 semantic invariant validation BEGIN"

if ($mainText -notmatch [regex]::Escape($marker)) {
    $block = @'

# Scenario 06 semantic invariant validation BEGIN
Write-Host ""
Write-Host "Checking Scenario 06 semantic invariants through main AHI checker..."
& powershell -ExecutionPolicy Bypass -File scripts\check_scenario_06_semantic_invariants_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    throw "Scenario 06 semantic invariant checker failed."
}
Write-Host "PASS: Scenario 06 semantic invariant validation completed inside main AHI checker."
# Scenario 06 semantic invariant validation END

'@

    $anchor = 'Write-Host "PASS: Scenario 06 validation completed inside main AHI checker."'
    if ($mainText.Contains($anchor)) {
        $mainText = $mainText.Replace($anchor, $anchor + $block)
    } else {
        $finalPass = 'Write-Host "PASS: ahi-sim-v0.1.x simulation proof-surface checks completed."'
        if ($mainText.Contains($finalPass)) {
            $mainText = $mainText.Replace($finalPass, $block + $finalPass)
        } else {
            $mainText = $mainText.TrimEnd() + "`n" + $block
        }
    }
    Write-Utf8NoBom $mainChecker $mainText
} else {
    Write-Host "Main checker already contains Scenario 06 semantic invariant block."
}

Write-Host "Regenerating deterministic viewer bundle..."
powershell -ExecutionPolicy Bypass -File scripts\build_ahi_viewer_data_v0_1.ps1 -ForceOverwrite
if ($LASTEXITCODE -ne 0) { throw "Viewer bundle rebuild failed." }

Write-Host ""
Write-Host "Scenario 06 semantic verification promotion applied."
