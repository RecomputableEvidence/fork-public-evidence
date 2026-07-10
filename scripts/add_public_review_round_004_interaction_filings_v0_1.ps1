# scripts/add_public_review_round_004_interaction_filings_v0_1.ps1
# Adds Public Review Round 004 interaction filing schema, observations, synthesis, and checker.
# PowerShell 5.1 compatible. Avoids embedded Markdown code fences.

param(
    [switch]$Commit,
    [switch]$Push
)

$ErrorActionPreference = "Stop"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Assert-RepoRoot {
    if (-not (Test-Path ".git")) {
        throw "Run this script from the fork-public-evidence repository root."
    }
}

function Write-Utf8Lf {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )

    $full = [System.IO.Path]::GetFullPath($Path)
    $dir = Split-Path -Parent $full

    if ($dir -and -not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }

    $normalized = $Content -replace "`r`n", "`n"
    [System.IO.File]::WriteAllText($full, $normalized, $Utf8NoBom)
}

function Read-Utf8 {
    param([Parameter(Mandatory = $true)][string]$Path)
    return [System.IO.File]::ReadAllText((Resolve-Path $Path).Path, $Utf8NoBom)
}

function Replace-OrAppendBlock {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$BlockId,
        [Parameter(Mandatory = $true)][string]$Content
    )

    if (-not (Test-Path $Path)) {
        Write-Host "Skipping missing routing target: $Path"
        return
    }

    $start = "<!-- $($BlockId):START -->"
    $end = "<!-- $($BlockId):END -->"
    $existing = Read-Utf8 -Path $Path

    $block = @"

$start

$Content

$end
"@

    $pattern = "(?s)" + [regex]::Escape($start) + ".*?" + [regex]::Escape($end)

    if ($existing -match $pattern) {
        $updated = [regex]::Replace($existing, $pattern, $block.Trim())
        Write-Host "Replaced routing block in $Path"
    } else {
        $updated = $existing.TrimEnd() + "`n" + $block + "`n"
        Write-Host "Added routing block in $Path"
    }

    Write-Utf8Lf -Path $Path -Content $updated
}

function Invoke-Git {
    param([Parameter(Mandatory = $true)][string[]]$Args)

    & git @Args
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Args -join ' ') failed with exit code $LASTEXITCODE"
    }
}

function Invoke-Python {
    param([Parameter(Mandatory = $true)][string[]]$Args)

    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        $python = Get-Command py -ErrorAction SilentlyContinue
    }
    if (-not $python) {
        throw "Python was not found on PATH."
    }

    & $python.Source @Args
    if ($LASTEXITCODE -ne 0) {
        throw "python $($Args -join ' ') failed with exit code $LASTEXITCODE"
    }
}

Assert-RepoRoot

$schemaPath = "schemas/public_review_round_004_interaction_v0_1.schema.json"
$templatePath = "docs/templates/PUBLIC_REVIEW_ROUND_004_INTERACTION_TEMPLATE_v0_1.json"
$checkerPath = "tools/check_public_review_round_004_interactions_v0_1.py"
$roundReadmePath = "docs/review/public-rounds/README.md"
$round004ReadmePath = "docs/review/public-rounds/round-004/README.md"
$synthesisPath = "docs/review/public-rounds/round-004/PUBLIC_REVIEW_ROUND_004_SYNTHESIS_v0_1.md"
$scriptPath = "scripts/add_public_review_round_004_interaction_filings_v0_1.ps1"

$obsDir = "docs/review/public-rounds/round-004/observations"
$obsCopilotPath = "$obsDir/ROUND004_OBS_001_copilot_access_path_no_execution_review_v0_1.json"
$obsGeminiPath = "$obsDir/ROUND004_OBS_002_gemini_no_access_exterior_observation_v0_1.json"
$obsVibePath = "$obsDir/ROUND004_OBS_003_vibe_access_path_governance_observation_v0_1.json"
$obsClaudePath = "$obsDir/ROUND004_OBS_004_claude_execution_recomputation_adversarial_observation_v0_1.json"

$schema = @'
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://recomputableevidence.example/schemas/public_review_round_004_interaction_v0_1.schema.json",
  "title": "Fork Public Review Round 004 Interaction Filing v0.1",
  "type": "object",
  "additionalProperties": true,
  "required": [
    "review_round",
    "reviewer_role",
    "reviewer_environment",
    "access_path",
    "verifier_run",
    "comprehension",
    "governance_articulation",
    "longitudinal_readiness",
    "review_classification"
  ],
  "properties": {
    "review_round": {
      "const": "public_review_round_004_accessibility_exterior_governance_longitudinal_readiness"
    },
    "reviewer_id": {
      "type": "string"
    },
    "reviewer_role": {
      "type": "string"
    },
    "evidence_weight": {
      "type": "string",
      "enum": [
        "execution_recomputation_receipt",
        "access_path_observation",
        "exterior_governance_observation",
        "no_access_observation",
        "mixed_observation"
      ]
    },
    "reviewer_environment": {
      "type": "object",
      "additionalProperties": true,
      "required": [
        "os",
        "shell",
        "python_version",
        "git_available"
      ],
      "properties": {
        "os": { "type": "string" },
        "shell": { "type": "string" },
        "python_version": { "type": "string" },
        "git_available": { "type": "boolean" }
      }
    },
    "access_path": {
      "type": "object",
      "additionalProperties": true,
      "required": [
        "started_from_repo_root",
        "found_current_proof_surface",
        "found_verifier",
        "found_boundary_pressure_cases",
        "found_longitudinal_protocol"
      ],
      "properties": {
        "started_from_repo_root": { "type": "boolean" },
        "found_current_proof_surface": { "type": "boolean" },
        "found_verifier": { "type": "boolean" },
        "found_boundary_pressure_cases": { "type": "boolean" },
        "found_longitudinal_protocol": { "type": "boolean" }
      }
    },
    "verifier_run": {
      "type": "object",
      "additionalProperties": true,
      "required": [
        "attempted",
        "passed",
        "failure_reason"
      ],
      "properties": {
        "attempted": { "type": "boolean" },
        "passed": { "type": "boolean" },
        "failure_reason": { "type": "string" }
      }
    },
    "comprehension": {
      "type": "object",
      "additionalProperties": true,
      "required": [
        "understood_current_claims",
        "understood_non_claims",
        "identified_overclaim_risk"
      ],
      "properties": {
        "understood_current_claims": { "type": "boolean" },
        "understood_non_claims": { "type": "boolean" },
        "identified_overclaim_risk": { "type": "string" }
      }
    },
    "governance_articulation": {
      "type": "object",
      "additionalProperties": true,
      "required": [
        "external_model_name",
        "what_it_would_consume",
        "what_it_would_not_inherit",
        "required_boundary_state"
      ],
      "properties": {
        "external_model_name": { "type": "string" },
        "what_it_would_consume": { "type": "string" },
        "what_it_would_not_inherit": { "type": "string" },
        "required_boundary_state": { "type": "string" }
      }
    },
    "longitudinal_readiness": {
      "type": "object",
      "additionalProperties": true,
      "required": [
        "missing_artifacts",
        "required_receipts",
        "checker_drift_concerns",
        "packet_failure_concerns"
      ],
      "properties": {
        "missing_artifacts": {
          "type": "array",
          "items": { "type": "string" }
        },
        "required_receipts": {
          "type": "array",
          "items": { "type": "string" }
        },
        "checker_drift_concerns": {
          "type": "array",
          "items": { "type": "string" }
        },
        "packet_failure_concerns": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "review_classification": {
      "type": "string"
    },
    "non_authority_statement": {
      "type": "string"
    }
  }
}
'@

$template = @'
{
  "review_round": "public_review_round_004_accessibility_exterior_governance_longitudinal_readiness",
  "reviewer_id": "",
  "reviewer_role": "",
  "evidence_weight": "mixed_observation",
  "reviewer_environment": {
    "os": "",
    "shell": "",
    "python_version": "",
    "git_available": true
  },
  "access_path": {
    "started_from_repo_root": true,
    "found_current_proof_surface": true,
    "found_verifier": true,
    "found_boundary_pressure_cases": true,
    "found_longitudinal_protocol": true
  },
  "verifier_run": {
    "attempted": true,
    "passed": true,
    "failure_reason": ""
  },
  "comprehension": {
    "understood_current_claims": true,
    "understood_non_claims": true,
    "identified_overclaim_risk": ""
  },
  "governance_articulation": {
    "external_model_name": "",
    "what_it_would_consume": "",
    "what_it_would_not_inherit": "",
    "required_boundary_state": ""
  },
  "longitudinal_readiness": {
    "missing_artifacts": [],
    "required_receipts": [],
    "checker_drift_concerns": [],
    "packet_failure_concerns": []
  },
  "review_classification": "",
  "non_authority_statement": "This filing is an exterior review interaction record. It is not an endorsement, validation, certification, legal opinion, compliance opinion, production-readiness assessment, procurement approval, safety assessment, or authority transfer."
}
'@

$copilot = @'
{
  "review_round": "public_review_round_004_accessibility_exterior_governance_longitudinal_readiness",
  "reviewer_id": "copilot",
  "reviewer_role": "AI exterior reviewer; access-path and governance-surface reader",
  "evidence_weight": "access_path_observation",
  "source_interaction_type": "access-path review; no local verifier execution",
  "reviewer_environment": {
    "os": "not executed",
    "shell": "not executed",
    "python_version": "",
    "git_available": false,
    "execution_context": "Could inspect public repository and release materials but did not execute PowerShell or Python verifier."
  },
  "access_path": {
    "started_from_repo_root": true,
    "found_current_proof_surface": true,
    "found_verifier": true,
    "found_boundary_pressure_cases": true,
    "found_longitudinal_protocol": true,
    "notes": "Found public repository and proof-surface routing. Recommended clearer canonical reviewer command and one-page files-to-outputs quickstart."
  },
  "verifier_run": {
    "attempted": false,
    "passed": false,
    "failure_reason": "No interactive shell available in review environment; verifier not executed."
  },
  "comprehension": {
    "understood_current_claims": true,
    "understood_non_claims": true,
    "identified_overclaim_risk": "Some prose may be read normatively by non-technical readers; recommended repeated disclaimers and clearer executable quickstart."
  },
  "governance_articulation": {
    "external_model_name": "external audit/governance ingestion model",
    "what_it_would_consume": "Canonical manifests, recomputed digests, checker versions, fixture provenance, timestamp or anchor receipts, and structured receipts imported into an audit ledger.",
    "what_it_would_not_inherit": "Implicit provenance claims, legal status, compliance status, production readiness, truth, or unsigned and unanchored timestamp assertions.",
    "required_boundary_state": "Canonical manifest digest, checker version/hash, fixture provenance, timestamp/anchor receipts, and explicit non-claim boundary."
  },
  "longitudinal_readiness": {
    "missing_artifacts": [
      "one-page quickstart mapping files to commands, expected outputs, and telemetry points",
      "machine-readable reviewer receipts",
      "single canonical cross-platform command"
    ],
    "required_receipts": [
      "canonical manifest receipt",
      "checker version/hash receipt",
      "timestamp or anchor receipt",
      "execution receipt"
    ],
    "checker_drift_concerns": [
      "Need checker versions and reproducible build or executable recipe to distinguish future checker drift."
    ],
    "packet_failure_concerns": [
      "Missing or corrupted artifacts should be distinguished from checker behavior changes."
    ]
  },
  "objective_data_suggested": [
    "time to first verifier run",
    "verifier pass/fail",
    "OS and runtime versions",
    "reviewer role",
    "points of confusion",
    "missing dependency errors",
    "fixture comprehension success rate"
  ],
  "review_classification": "access-path review",
  "non_authority_statement": "This filing records an access-path/no-execution exterior observation. It is not an endorsement, validation, certification, legal opinion, compliance opinion, production-readiness assessment, procurement approval, safety assessment, or authority transfer."
}
'@

$gemini = @'
{
  "review_round": "public_review_round_004_accessibility_exterior_governance_longitudinal_readiness",
  "reviewer_id": "gemini",
  "reviewer_role": "AI exterior reviewer; no-access governance architecture observer",
  "evidence_weight": "no_access_observation",
  "source_interaction_type": "mixed review; no-access observation plus exterior observation",
  "reviewer_environment": {
    "os": "sandboxed AI runtime",
    "shell": "not available",
    "python_version": "",
    "git_available": false,
    "execution_context": "No active web traversal or local PowerShell execution available."
  },
  "access_path": {
    "started_from_repo_root": false,
    "found_current_proof_surface": false,
    "found_verifier": false,
    "found_boundary_pressure_cases": false,
    "found_longitudinal_protocol": false,
    "notes": "Could not resolve or pull the GitHub repository; review is limited to prompt-provided structure."
  },
  "verifier_run": {
    "attempted": false,
    "passed": false,
    "failure_reason": "Sandboxed AI runtime could not download repository or execute PowerShell verifier."
  },
  "comprehension": {
    "understood_current_claims": true,
    "understood_non_claims": true,
    "identified_overclaim_risk": "No direct textual overclaim could be inspected. Suggested explicit null-claim flag to prevent verification from being read as truth, safety, or compliance."
  },
  "governance_articulation": {
    "external_model_name": "deterministic AI governance model",
    "what_it_would_consume": "Output receipts, JSON or YAML manifests, fixture hashes, verifier hashes, and deterministic state-preservation records.",
    "what_it_would_not_inherit": "Subjective classification, legal compliance, safety, factual truth, production readiness, or authorization.",
    "required_boundary_state": "Exact fixture hash, exact verifier version/hash, receipt schema, and explicit null-claim flag that structural verification is not authority."
  },
  "longitudinal_readiness": {
    "missing_artifacts": [
      "dependency lockfiles",
      "cryptographic anchors",
      "immutable Day-0 fixtures"
    ],
    "required_receipts": [
      "receipt binding input fixture hash",
      "receipt binding verifier script hash",
      "receipt binding timestamp or anchor hash"
    ],
    "checker_drift_concerns": [
      "Same input failing under modern verifier due to changed verifier logic or deprecated runtime."
    ],
    "packet_failure_concerns": [
      "Input packet altered, corrupted, or lost, causing original criteria to reject it."
    ]
  },
  "objective_data_suggested": [
    "cryptographic environment footprint",
    "execution latency",
    "boundary clarification rate",
    "failure mode category"
  ],
  "review_classification": "mixed review: no-access observation plus exterior observation",
  "non_authority_statement": "This filing records a no-access exterior governance observation. It is not an endorsement, validation, certification, legal opinion, compliance opinion, production-readiness assessment, procurement approval, safety assessment, or authority transfer."
}
'@

$vibe = @'
{
  "review_round": "public_review_round_004_accessibility_exterior_governance_longitudinal_readiness",
  "reviewer_id": "vibe",
  "reviewer_role": "AI exterior reviewer; access-path, governance-articulation, and boundary-pressure observer",
  "evidence_weight": "exterior_governance_observation",
  "source_interaction_type": "access-path review; exterior governance articulation; boundary-pressure observation",
  "reviewer_environment": {
    "os": "not executed",
    "shell": "not executed",
    "python_version": "",
    "git_available": false,
    "execution_context": "Reviewed repository content conceptually but did not execute verifier."
  },
  "access_path": {
    "started_from_repo_root": true,
    "found_current_proof_surface": true,
    "found_verifier": true,
    "found_boundary_pressure_cases": true,
    "found_longitudinal_protocol": true,
    "notes": "Reported repository accessible, proof surface discoverable, and navigation clear. Suggested duplicating Reviewer First Path in README."
  },
  "verifier_run": {
    "attempted": false,
    "passed": false,
    "failure_reason": "Could not run PowerShell in review environment; verifier logic inspected only."
  },
  "comprehension": {
    "understood_current_claims": true,
    "understood_non_claims": true,
    "identified_overclaim_risk": "Used phrase production-ready for its stated purpose in exterior summary; Fork should not adopt this as an internal claim."
  },
  "governance_articulation": {
    "external_model_name": "external governance assurance model",
    "what_it_would_consume": "Sealed evidence packets, SHA-256 hashes, manifests, outer receipts, boundary-pressure fixtures and results, explicit non-authority statements, recomputation receipts as structural evidence only, and longitudinal protocol definitions.",
    "what_it_would_not_inherit": "Correctness, truth, validity, authorization, compliance, legal sufficiency, production readiness, safety, or approval.",
    "required_boundary_state": "Hashes, timestamps, fixture definitions, checker versions, explicit non-preservation of authority, and clear statement that reconstruction is not authorization."
  },
  "longitudinal_readiness": {
    "missing_artifacts": [
      "schema implementations",
      "Day-0 fixture packet",
      "Day 0, 7, 30, and 90 replay receipts",
      "adverse variant fixtures",
      "checker drift tracking mechanism"
    ],
    "required_receipts": [
      "sealed artifact receipts",
      "manifest plus outer receipt",
      "pinned checker receipt",
      "expected reconstruction provenance receipt",
      "environment manifest receipt",
      "non-authority boundary statement receipt"
    ],
    "checker_drift_concerns": [
      "Current checker producing different output than pinned checker for same clean packet."
    ],
    "packet_failure_concerns": [
      "Clean packet failing under pinned checker or manifest tamper/hash mismatch."
    ]
  },
  "objective_data_suggested": [
    "time to first verifier run",
    "verifier pass/fail",
    "OS/environment",
    "reviewer role",
    "points of confusion",
    "non-claim comprehension",
    "fixture comprehension score",
    "checker execution time",
    "path existence failures"
  ],
  "review_classification": "access-path review plus exterior governance articulation plus boundary-pressure observation",
  "non_authority_statement": "This filing records an exterior governance observation. It is not an endorsement, validation, certification, legal opinion, compliance opinion, production-readiness assessment, procurement approval, safety assessment, or authority transfer. Any phrase that could imply readiness, approval, certification, endorsement, validation, legal sufficiency, compliance sufficiency, production readiness, or authority is preserved as exterior language only and is not adopted as a Fork claim."
}
'@

$claude = @'
{
  "review_round": "public_review_round_004_accessibility_exterior_governance_longitudinal_readiness",
  "reviewer_id": "claude",
  "reviewer_role": "AI exterior reviewer; execution, recomputation, access-path, usability, and adversarial boundary reviewer",
  "evidence_weight": "execution_recomputation_receipt",
  "source_interaction_type": "execution receipt; recomputation receipt; adversarial counter-fixture observation; access-path review; usability review; governance articulation",
  "reviewer_environment": {
    "os": "Ubuntu 24.04 sandbox",
    "shell": "bash plus PowerShell 7.6.3 installed fresh from official GitHub release tarball",
    "python_version": "Python 3.12.3",
    "git_available": true,
    "git_version": "2.43.0",
    "powershell_version": "7.6.3",
    "environment_notes": "PowerShell was not preinstalled. Release tarball was downloaded and sha256-verified before extraction."
  },
  "access_path": {
    "started_from_repo_root": true,
    "found_current_proof_surface": true,
    "found_verifier": true,
    "found_boundary_pressure_cases": true,
    "found_longitudinal_protocol": true,
    "repo_url": "https://github.com/RecomputableEvidence/fork-public-evidence",
    "head_commit": "7e8f29913e364f73ef86cd942be2472a0109c036",
    "notes": "Clean clone without authentication. README routes cold visitor to REVIEWER_START_HERE first; CURRENT_PROOF_SURFACE is one extra hop for README-first reviewers."
  },
  "verifier_run": {
    "attempted": true,
    "passed": true,
    "failure_reason": "",
    "documented_command_passed": true,
    "direct_python_checker_passed": true,
    "public_verifier_status": "PUBLIC_REVIEW_PACKAGE_VERIFY_PASS",
    "public_verifier_passed_count": 17,
    "public_verifier_failed_count": 0,
    "boundary_pressure_total": 4,
    "boundary_pressure_passed": 4,
    "boundary_pressure_failed": 0,
    "working_tree_unmodified_after_run": true
  },
  "comprehension": {
    "understood_current_claims": true,
    "understood_non_claims": true,
    "identified_overclaim_risk": "Documentation and implementation diverge for invalid-fixture semantics. The checker demonstrates the shipped negative fixtures are correctly labeled, not that it would catch arbitrary mislabeled or content-free negative fixtures."
  },
  "governance_articulation": {
    "external_model_name": "AI exterior reviewer operating under tool-result-versus-truth separation",
    "what_it_would_consume": "Checker C, commit H, fixture set F, pass/fail result, direct verifier output, direct Python checker output, and reproducible execution receipt.",
    "what_it_would_not_inherit": "Any reading of passed:true as correctness, compliance, truth, safety, authorization, production readiness, or validation of the underlying workflow.",
    "required_boundary_state": "Explicit statement of which valid/invalid split is content-gated versus label-trusted; checker version/hash; fixture set; commit; command; environment; non-authority statement."
  },
  "longitudinal_readiness": {
    "missing_artifacts": [
      "schema implementations",
      "fixture packets",
      "reconstruction scripts",
      "checker scripts for longitudinal trial",
      "Day-0 receipt",
      "adverse fixtures",
      "reviewer instructions",
      "Day 7, Day 30, and Day 90 replay receipts"
    ],
    "required_receipts": [
      "packet_manifest.sha256",
      "packet_manifest_outer_receipt.json",
      "manifest carrying trial_id, packet_id, schema_versions, checker_versions, pinned_commit, canonicalization_method, artifact_hashes, expected_reconstruction_hash, environment_manifest_hash, non_authority_boundary_statement_hash, and created_at_fixed_fixture_time",
      "independently produced expected reconstruction provenance receipt"
    ],
    "checker_drift_concerns": [
      "Need pinned-checker replay versus current-checker replay tracks.",
      "Need outcomes for documented semantic change, undocumented semantic drift, and match confirmed.",
      "Expected reconstruction must not be generated and later proved by the same implementation."
    ],
    "packet_failure_concerns": [
      "Payload hash mismatch.",
      "Manifest-level tamper.",
      "Missing or corrupted preserved packet under pinned checker is packet failure, not checker drift."
    ]
  },
  "adversarial_findings": [
    {
      "finding_id": "ROUND004_CLAUDE_FINDING_001_INVALID_FIXTURE_CONTENT_GATING",
      "summary": "Invalid-side branches can pass negative tests by placement or self-declaration rather than proving the invalid condition is detected.",
      "details": "Constructed scratch fixtures showed content shaped like a valid retrieval limitation could be placed under invalid/ and pass as rejected; a near-empty recomputation receipt overread fixture also passed as an invalid negative test while reporting missing required fields.",
      "impact": "Narrows current proof claim. The shipped fixtures are honestly authored, but the checker should not yet be claimed to reject arbitrary malformed, mislabeled, or content-free negative fixtures.",
      "recommended_followup": "Harden boundary-pressure checker invalid fixture semantics and add adversarial counterfixtures."
    }
  ],
  "objective_data_suggested": [
    "pwsh-on-PATH boolean",
    "PowerShell install path taken",
    "outbound HTTPS reachability to github.com and release-assets.githubusercontent.com",
    "documented command unmodified versus adapted",
    "direct checker rerun independent of wrapper",
    "adversarial fixture constructed by reviewer",
    "whether working tree remained unmodified"
  ],
  "review_classification": "mixed: execution receipt; recomputation receipt; access-path review; usability review; governance articulation; adversarial boundary-pressure observation",
  "non_authority_statement": "This filing records execution, recomputation, and adversarial observations. It is not an endorsement, validation, certification, legal opinion, compliance opinion, production-readiness assessment, procurement approval, safety assessment, or authority transfer. It does not certify, validate, approve, endorse, establish compliance, establish legal sufficiency, establish safety, establish production readiness, or transfer authority."
}
'@

$roundReadme = @'
# Public Review Rounds

This directory preserves structured public review rounds for Fork.

Review filings are not endorsements, certifications, approvals, compliance opinions, legal opinions, safety assessments, procurement approvals, or production-readiness assessments.

Each review round should preserve:

- prompt or review scope;
- interaction filings;
- classification of reviewer response;
- objective data fields;
- exterior observations;
- non-claims;
- recommended follow-up work.

Current round:

- round-004/
'@

$round004Readme = @'
# Public Review Round 004

Round name:

public_review_round_004_accessibility_exterior_governance_longitudinal_readiness

Purpose:

Test whether Fork's public GitHub surface is accessible, independently inspectable, and usable by exterior governance models without converting review, recomputation, or observation into authority.

Primary files:

- PUBLIC_REVIEW_ROUND_004_SYNTHESIS_v0_1.md
- observations/

Schema:

- schemas/public_review_round_004_interaction_v0_1.schema.json

Checker:

- python tools/check_public_review_round_004_interactions_v0_1.py --json

This round is experimental. It does not validate Fork, certify Fork, approve Fork, establish legal sufficiency, establish compliance sufficiency, establish safety, establish production readiness, or transfer authority.
'@

$synthesis = @'
# Public Review Round 004 Synthesis v0.1

Status: Exterior review synthesis.
Round: public_review_round_004_accessibility_exterior_governance_longitudinal_readiness
Scope: GitHub accessibility, exterior governance articulation, objective data capture, and longitudinal recomputation readiness.

## 1. Purpose

This synthesis files Round 004 interactions into a shared JSON structure so review observations can be compared without converting them into endorsement, certification, approval, legal sufficiency, compliance sufficiency, safety, production readiness, or authority.

## 2. Filed Observations

- observations/ROUND004_OBS_001_copilot_access_path_no_execution_review_v0_1.json
- observations/ROUND004_OBS_002_gemini_no_access_exterior_observation_v0_1.json
- observations/ROUND004_OBS_003_vibe_access_path_governance_observation_v0_1.json
- observations/ROUND004_OBS_004_claude_execution_recomputation_adversarial_observation_v0_1.json

## 3. Evidence Weighting

execution_recomputation_receipt:
Highest evidentiary weight for this round. A reviewer cloned the repo, ran the verifier, reran the Python checker, and constructed adversarial counterfixtures.

access_path_observation:
Useful for accessibility and documentation clarity. Does not establish execution or recomputation.

exterior_governance_observation:
Useful for how exterior governance models consume or refuse to inherit Fork state. Does not establish execution or recomputation unless paired with a run receipt.

no_access_observation:
Useful for prompt clarity and conceptual articulation under constrained access. Must not be cited as repository inspection, execution, or recomputation.

## 4. Round Result

Round 004 indicates that Fork's public verifier and current proof-surface index are understandable and externally runnable, including from at least one non-Windows environment.

Round 004 also identified a concrete hardening issue:

The shipped boundary-pressure fixtures are honestly authored, but the current invalid-fixture checker branches can classify negative fixtures by placement or self-declaration rather than fully content-gating the invalid condition.

## 5. Immediate Follow-Up

Next recommended engineering work:

- Harden boundary-pressure checker invalid fixture semantics.
- Add adversarial counterfixtures for malformed, mislabeled, content-free, and valid-shaped-negative fixtures.
- Update proof-surface language to distinguish shipped fixture pass from general invalid-fixture enforcement.

## 6. Boundary Statement

This synthesis preserves exterior observations. It is not an endorsement, validation, certification, legal opinion, compliance opinion, production-readiness assessment, procurement approval, safety assessment, or authority transfer.
'@

$checker = @'
#!/usr/bin/env python3
"""
Fork Public Review Round 004 Interaction Checker v0.1.

Validates filed Round 004 interaction JSON records for required structure and
basic boundary-safety fields.

This checker does not validate truth, compliance, legal sufficiency, safety,
authorization, approval, production readiness, or institutional authority.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any, Dict, List, Tuple


ROUND_ID = "public_review_round_004_accessibility_exterior_governance_longitudinal_readiness"

REQUIRED_TOP_LEVEL = [
    "review_round",
    "reviewer_role",
    "reviewer_environment",
    "access_path",
    "verifier_run",
    "comprehension",
    "governance_articulation",
    "longitudinal_readiness",
    "review_classification",
]

REQUIRED_ENVIRONMENT = [
    "os",
    "shell",
    "python_version",
    "git_available",
]

REQUIRED_ACCESS_PATH = [
    "started_from_repo_root",
    "found_current_proof_surface",
    "found_verifier",
    "found_boundary_pressure_cases",
    "found_longitudinal_protocol",
]

REQUIRED_VERIFIER_RUN = [
    "attempted",
    "passed",
    "failure_reason",
]

REQUIRED_COMPREHENSION = [
    "understood_current_claims",
    "understood_non_claims",
    "identified_overclaim_risk",
]

REQUIRED_GOVERNANCE = [
    "external_model_name",
    "what_it_would_consume",
    "what_it_would_not_inherit",
    "required_boundary_state",
]

REQUIRED_LONGITUDINAL = [
    "missing_artifacts",
    "required_receipts",
    "checker_drift_concerns",
    "packet_failure_concerns",
]

BOOLEAN_FIELDS = {
    ("reviewer_environment", "git_available"),
    ("access_path", "started_from_repo_root"),
    ("access_path", "found_current_proof_surface"),
    ("access_path", "found_verifier"),
    ("access_path", "found_boundary_pressure_cases"),
    ("access_path", "found_longitudinal_protocol"),
    ("verifier_run", "attempted"),
    ("verifier_run", "passed"),
    ("comprehension", "understood_current_claims"),
    ("comprehension", "understood_non_claims"),
}

ARRAY_FIELDS = {
    ("longitudinal_readiness", "missing_artifacts"),
    ("longitudinal_readiness", "required_receipts"),
    ("longitudinal_readiness", "checker_drift_concerns"),
    ("longitudinal_readiness", "packet_failure_concerns"),
}


def load_json(path: pathlib.Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception as exc:
        raise ValueError(f"{path}: JSON parse failure: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be object")
    return data


def require_object(data: Dict[str, Any], key: str, errors: List[str]) -> Dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key} must be object")
        return {}
    return value


def validate_record(path: pathlib.Path, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []

    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            errors.append(f"missing top-level field: {key}")

    if data.get("review_round") != ROUND_ID:
        errors.append("review_round does not match Round 004 identifier")

    environment = require_object(data, "reviewer_environment", errors)
    access_path = require_object(data, "access_path", errors)
    verifier_run = require_object(data, "verifier_run", errors)
    comprehension = require_object(data, "comprehension", errors)
    governance = require_object(data, "governance_articulation", errors)
    longitudinal = require_object(data, "longitudinal_readiness", errors)

    for key in REQUIRED_ENVIRONMENT:
        if key not in environment:
            errors.append(f"reviewer_environment missing field: {key}")

    for key in REQUIRED_ACCESS_PATH:
        if key not in access_path:
            errors.append(f"access_path missing field: {key}")

    for key in REQUIRED_VERIFIER_RUN:
        if key not in verifier_run:
            errors.append(f"verifier_run missing field: {key}")

    for key in REQUIRED_COMPREHENSION:
        if key not in comprehension:
            errors.append(f"comprehension missing field: {key}")

    for key in REQUIRED_GOVERNANCE:
        if key not in governance:
            errors.append(f"governance_articulation missing field: {key}")

    for key in REQUIRED_LONGITUDINAL:
        if key not in longitudinal:
            errors.append(f"longitudinal_readiness missing field: {key}")

    sections = {
        "reviewer_environment": environment,
        "access_path": access_path,
        "verifier_run": verifier_run,
        "comprehension": comprehension,
        "governance_articulation": governance,
        "longitudinal_readiness": longitudinal,
    }

    for section, key in BOOLEAN_FIELDS:
        if key in sections[section] and not isinstance(sections[section][key], bool):
            errors.append(f"{section}.{key} must be boolean")

    for section, key in ARRAY_FIELDS:
        value = sections[section].get(key)
        if value is not None:
            if not isinstance(value, list):
                errors.append(f"{section}.{key} must be array")
            elif not all(isinstance(item, str) for item in value):
                errors.append(f"{section}.{key} must contain only strings")

    classification = data.get("review_classification")
    if not isinstance(classification, str) or not classification.strip():
        errors.append("review_classification must be non-empty string")

    non_authority = str(data.get("non_authority_statement", "")).lower()
    required_boundary_terms = [
        "not",
        "endorsement",
        "validation",
        "certification",
        "legal",
        "compliance",
        "production",
        "authority",
    ]
    for term in required_boundary_terms:
        if term not in non_authority:
            errors.append(f"non_authority_statement missing boundary term: {term}")

    if verifier_run.get("attempted") is False and verifier_run.get("passed") is True:
        errors.append("verifier_run.passed cannot be true when attempted is false")

    return not errors, errors


def find_records(root: pathlib.Path) -> List[pathlib.Path]:
    if not root.exists():
        return []
    return sorted(root.glob("*.json"))


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--observations-root",
        default="docs/review/public-rounds/round-004/observations",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    root = pathlib.Path(args.observations_root)
    paths = find_records(root)

    results = []
    failed = 0

    for path in paths:
        data = load_json(path)
        passed, errors = validate_record(path, data)
        if not passed:
            failed += 1

        results.append({
            "path": str(path).replace("\\", "/"),
            "reviewer_id": data.get("reviewer_id", path.stem),
            "review_classification": data.get("review_classification", ""),
            "evidence_weight": data.get("evidence_weight", ""),
            "passed": passed,
            "errors": errors,
        })

    summary = {
        "checker": "check_public_review_round_004_interactions_v0_1.py",
        "round": ROUND_ID,
        "observations_root": str(root).replace("\\", "/"),
        "total": len(results),
        "passed": len(results) - failed,
        "failed": failed,
        "results": results,
        "non_authority_statement": (
            "This checker validates interaction filing structure only; it does not "
            "validate truth, compliance, legal sufficiency, safety, authorization, "
            "approval, production readiness, endorsement, or institutional authority."
        ),
    }

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"Round 004 interaction filings: {summary['passed']}/{summary['total']} passed")
        for result in results:
            status = "PASS" if result["passed"] else "FAIL"
            print(f"{status} {result['reviewer_id']} ({result['path']})")
            for error in result["errors"]:
                print(f"  - {error}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
'@

Write-Utf8Lf -Path $schemaPath -Content $schema
Write-Utf8Lf -Path $templatePath -Content $template
Write-Utf8Lf -Path $roundReadmePath -Content $roundReadme
Write-Utf8Lf -Path $round004ReadmePath -Content $round004Readme
Write-Utf8Lf -Path $synthesisPath -Content $synthesis
Write-Utf8Lf -Path $checkerPath -Content $checker
Write-Utf8Lf -Path $obsCopilotPath -Content $copilot
Write-Utf8Lf -Path $obsGeminiPath -Content $gemini
Write-Utf8Lf -Path $obsVibePath -Content $vibe
Write-Utf8Lf -Path $obsClaudePath -Content $claude

$reviewerStartBlock = @'
## Public Review Round 004 interaction filings

Round 004 filings are preserved here:

- docs/review/public-rounds/round-004/

The interaction schema is:

- schemas/public_review_round_004_interaction_v0_1.schema.json

Validate filed interactions with:

- python tools/check_public_review_round_004_interactions_v0_1.py --json

These filings preserve access-path reviews, no-access observations, exterior governance articulations, and execution/recomputation observations. They are not endorsements, certifications, approvals, legal opinions, compliance opinions, production-readiness assessments, or authority transfers.
'@

$publicIndexBlock = @'
## Public Review Round 004

Round 004 preserves structured interaction filings for GitHub accessibility, exterior governance articulation, objective data capture, and longitudinal recomputation readiness.

Start here:

- docs/review/public-rounds/round-004/PUBLIC_REVIEW_ROUND_004_SYNTHESIS_v0_1.md

Schema:

- schemas/public_review_round_004_interaction_v0_1.schema.json

Checker:

- python tools/check_public_review_round_004_interactions_v0_1.py --json
'@

Replace-OrAppendBlock `
    -Path "docs/REVIEWER_START_HERE_v0_1.md" `
    -BlockId "FORK_PUBLIC_REVIEW_ROUND_004_INTERACTION_FILINGS" `
    -Content $reviewerStartBlock

Replace-OrAppendBlock `
    -Path "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md" `
    -BlockId "FORK_PUBLIC_REVIEW_ROUND_004_INTERACTION_FILINGS" `
    -Content $publicIndexBlock

Write-Host ""
Write-Host "Created or updated Round 004 filing surface."

Write-Host ""
Write-Host "Running Round 004 interaction checker..."
Invoke-Python -Args @($checkerPath, "--json")

Write-Host ""
Write-Host "Running public review verifier..."
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    throw "Public review verifier failed."
}

Write-Host ""
Write-Host "Running whitespace check..."
Invoke-Git -Args @("diff", "--check")

Write-Host ""
Write-Host "Changed files:"
git status --short

Write-Host ""
Write-Host "Review commands:"
Write-Host "  git diff -- docs\review\public-rounds"
Write-Host "  git diff -- schemas\public_review_round_004_interaction_v0_1.schema.json"
Write-Host "  git diff -- tools\check_public_review_round_004_interactions_v0_1.py"
Write-Host "  python tools\check_public_review_round_004_interactions_v0_1.py --json"
Write-Host "  powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1"
Write-Host "  git diff --check"

if ($Commit) {
    Invoke-Git -Args @("add", "--",
        $schemaPath,
        $templatePath,
        $roundReadmePath,
        $round004ReadmePath,
        $synthesisPath,
        $checkerPath,
        $obsCopilotPath,
        $obsGeminiPath,
        $obsVibePath,
        $obsClaudePath,
        "docs/REVIEWER_START_HERE_v0_1.md",
        "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md",
        $scriptPath
    )

    Invoke-Git -Args @("diff", "--cached", "--check")
    Invoke-Git -Args @("commit", "-m", "Add public review round 004 interaction filings")

    if ($Push) {
        Invoke-Git -Args @("push")
    }
}

Write-Host ""
Write-Host "Done."