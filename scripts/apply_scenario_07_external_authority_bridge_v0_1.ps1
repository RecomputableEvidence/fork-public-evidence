# scripts/apply_scenario_07_external_authority_bridge_v0_1.ps1
# Applies Scenario 07 external authority bridge simulation.
# This script patches scenario_registry.json and run_ahi_sim_v0_1_checks.ps1,
# optionally patches viewer artifact labels, and regenerates the viewer bundle.
# It does not commit, push, or tag.

$ErrorActionPreference = "Stop"

function Write-Utf8NoBom($Path, $Text) {
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText((Resolve-Path $Path), $Text, $utf8NoBom)
}

if (-not (Test-Path ".git")) {
    throw "Run this script from repository root, e.g. C:\N\fork-public-evidence"
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python was not found on PATH."
}

Write-Host "Checking Scenario 07 before registry integration..."
powershell -ExecutionPolicy Bypass -File scripts\check_scenario_07_external_authority_bridge_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    throw "Scenario 07 checker failed. Registry was not patched."
}

Write-Host "Patching scenario registry..."
$tempPy = Join-Path $env:TEMP "patch_scenario_07_registry_v0_1.py"
$py = @'
import copy
import json
from pathlib import Path

path = Path("examples/simulations/governance-proof-surface/scenario_registry.json")
with path.open("r", encoding="utf-8") as f:
    registry = json.load(f)

sid = "SCENARIO_07_EXTERNAL_AUTHORITY_BRIDGE"
scenario_path = "examples/simulations/governance-proof-surface/scenario_07_external_authority_bridge.md"
artifacts = [
    "examples/simulations/governance-proof-surface/artifacts/scenario_07_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_07_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_07_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_07_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_07_external_authority_failure_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_07_external_review_context.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_07_transition_graph.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_07_non_claims_panel.md",
]

scenarios = registry.setdefault("scenarios", [])

existing = None
for s in scenarios:
    if s.get("scenario_id") == sid:
        existing = s
        break

template = None
for s in scenarios:
    if s.get("scenario_id") == "SCENARIO_06_MULTI_SYSTEM_DISTRIBUTED_HANDOFF":
        template = copy.deepcopy(s)
        break

if existing is None:
    scenario = template if template is not None else {}
else:
    scenario = existing

scenario["scenario_id"] = sid

# Preserve registry number type/style where possible.
old_num = scenario.get("scenario_number", scenario.get("number", 7))
if isinstance(old_num, int):
    scenario["scenario_number"] = 7
elif isinstance(old_num, str) and old_num.startswith("0"):
    scenario["scenario_number"] = "07"
else:
    scenario["scenario_number"] = "7"

for key in ("title", "scenario_title", "name"):
    if key in scenario or key == "title":
        scenario[key] = "Scenario 07 — External Authority Bridge"

for key in ("scenario_path", "path", "narrative_path", "file_path", "file"):
    if key in scenario:
        scenario[key] = scenario_path

# Ensure at least one path key exists.
if not any(k in scenario for k in ("scenario_path", "path", "narrative_path", "file_path", "file")):
    scenario["scenario_path"] = scenario_path

scenario["verification_posture"] = "SEMANTICALLY_VERIFIED"
scenario["posture_description"] = (
    "Artifact family present; dedicated checker verifies bounded external-authority bridge invariants. "
    "This does not establish external admissibility, compliance, approval, legal sufficiency, acceptance, "
    "execution eligibility, or correctness."
)
scenario["artifact_files"] = artifacts

scenario["main_checker"] = {
    "invoked_by": "scripts/run_ahi_sim_v0_1_checks.ps1",
    "dedicated_checker": "scripts/check_scenario_07_external_authority_bridge_v0_1.ps1",
    "semantic_invariants_checked": [
        "internal_record_preserved_for_external_inspection",
        "no_external_authority_transfer",
        "unsupported_external_authority_inference_recorded",
        "expanded_external_consumption_requires_separate_authority",
        "unsupported_external_mapping_recorded",
        "external_failure_event_not_supported",
        "required_external_revalidation_preserved",
        "non_authority_posture_preserved"
    ]
}

scenario["checker_coverage"] = {
    "required_files": True,
    "json_validity": True,
    "semantic_invariants": True,
    "non_authority_scan": True,
    "viewer_bundle": True
}

if existing is None:
    # Insert after Scenario 06 where possible.
    inserted = False
    for i, s in enumerate(scenarios):
        if s.get("scenario_id") == "SCENARIO_06_MULTI_SYSTEM_DISTRIBUTED_HANDOFF":
            scenarios.insert(i + 1, scenario)
            inserted = True
            break
    if not inserted:
        scenarios.append(scenario)

with path.open("w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(registry, indent=2, ensure_ascii=False) + "\n")
'@

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($tempPy, $py, $utf8NoBom)
python $tempPy
Remove-Item $tempPy -Force

Write-Host "Patching main AHI checker..."
$mainChecker = "scripts/run_ahi_sim_v0_1_checks.ps1"
$mainText = Get-Content -Raw -Path $mainChecker
$marker = "# Scenario 07 external authority bridge validation BEGIN"

if ($mainText -notmatch [regex]::Escape($marker)) {
    $block = @'

# Scenario 07 external authority bridge validation BEGIN
Write-Host ""
Write-Host "Checking Scenario 07 external authority bridge through main AHI checker..."
& powershell -ExecutionPolicy Bypass -File scripts\check_scenario_07_external_authority_bridge_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    throw "Scenario 07 external authority bridge checker failed."
}
Write-Host "PASS: Scenario 07 validation completed inside main AHI checker."
# Scenario 07 external authority bridge validation END

'@

    $finalPass = 'Write-Host "PASS: ahi-sim-v0.1.x simulation proof-surface checks completed."'
    if ($mainText.Contains($finalPass)) {
        $mainText = $mainText.Replace($finalPass, $block + $finalPass)
    } else {
        $mainText = $mainText.TrimEnd() + "`n" + $block
    }

    Write-Utf8NoBom $mainChecker $mainText
} else {
    Write-Host "Main checker already contains Scenario 07 block."
}

Write-Host "Patching viewer builder artifact labels if needed..."
$builder = "scripts/build_ahi_viewer_data_v0_1.py"
if (Test-Path $builder) {
    $builderText = Get-Content -Raw -Path $builder
    if ($builderText -notmatch "external_authority_failure_event") {
        $patched = $false
        $replacements = @(
            @('"distributed_authority_failure_event": "DAFE",', '"distributed_authority_failure_event": "DAFE",' + "`n" + '        "external_authority_failure_event": "EAFE",'),
            @("'distributed_authority_failure_event': 'DAFE',", "'distributed_authority_failure_event': 'DAFE'," + "`n" + "        'external_authority_failure_event': 'EAFE',")
        )

        foreach ($pair in $replacements) {
            if ($builderText.Contains($pair[0])) {
                $builderText = $builderText.Replace($pair[0], $pair[1])
                $patched = $true
                break
            }
        }

        if ($patched) {
            Write-Utf8NoBom $builder $builderText
        } else {
            Write-Host "No known artifact-label dictionary pattern found; continuing without builder label patch."
        }
    } else {
        Write-Host "Viewer builder already references external_authority_failure_event."
    }
}

Write-Host "Regenerating deterministic viewer bundle..."
powershell -ExecutionPolicy Bypass -File scripts\build_ahi_viewer_data_v0_1.ps1 -ForceOverwrite
if ($LASTEXITCODE -ne 0) {
    throw "Viewer bundle rebuild failed."
}

Write-Host ""
Write-Host "Scenario 07 external authority bridge applied."
Write-Host "Next run:"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\check_scenario_07_external_authority_bridge_v0_1.ps1"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1"
