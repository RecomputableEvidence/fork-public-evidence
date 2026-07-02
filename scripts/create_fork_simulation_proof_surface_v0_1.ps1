# scripts/create_fork_simulation_proof_surface_v0_1.ps1
# Creates Fork Governance Simulation Proof Surface v0.1 scaffold.
# Does not stage, commit, push, or tag.

param(
    [switch]$ForceOverwrite
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".git")) {
    throw "Run this script from the repository root, e.g. C:\N\fork-public-evidence"
}

function Write-Utf8NoBomFile {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content,
        [switch]$Overwrite
    )

    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path $parent)) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }

    if ((Test-Path $Path) -and -not $Overwrite) {
        Write-Host "SKIP existing file: $Path"
        return
    }

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $utf8NoBom)
    Write-Host "WROTE: $Path"
}

$doctrine = @'
# Fork Governance Simulation Proof Surface Doctrine v0.1

## Purpose

Fork Governance Simulation Proof Surface is an internal-to-public calibration environment for modeling accountable handoffs between independently accountable systems.

Its purpose is to test claim boundaries, handoff semantics, artifact formats, interface contracts, delegation behavior, and failure modes without asserting correctness, compliance, authority, or general validity.

The simulation layer sits between design notes and external evaluation. It is where Fork concepts are pressure-tested against operational complexity before broader claims are presented to institutional reviewers.

## Core Doctrine

> The simulation is not designed to prove that Fork is correct. It is designed to make Fork's boundaries testable.

Fork's simulation proof surface tests whether handoff-state records can preserve claim scope, non-claims, authority context, unresolved state, and revalidation requirements across independently accountable systems without converting Fork into the authority, policy, runtime, compliance, or audit layer.

## What the Simulation Can Demonstrate

The simulation can demonstrate whether Fork-style boundary records:

- preserve handoff state;
- preserve non-claims through downstream consumption;
- expose claim expansion;
- expose authority leakage;
- keep policy references separated from approval or compliance;
- support later reconstruction of what crossed a boundary;
- allow multiple systems to interoperate without inheriting each other's authority.

## What the Simulation Does Not Claim

The simulation does not establish:

- AI correctness;
- factual truth;
- legal sufficiency;
- compliance;
- production readiness;
- institutional approval;
- universal superiority over existing governance tools;
- general validity of Accountable Handoff Interoperability.

## Safe Simulation Claim

This simulation provides evidence consistent with Fork's claim that explicit handoff-state records can improve reconstruction of consequential transitions between independently accountable systems.

It does not establish correctness, compliance, legal sufficiency, institutional authority, or general validity.

## Four Simulation Planes

### 1. Scenario Plane

The scenario plane defines the modeled world:

- participating systems;
- artifact produced;
- boundary crossed;
- downstream consumer;
- attempted inference;
- expected Fork behavior;
- expected non-claims.

### 2. Contract Plane

The contract plane defines simulation-time artifacts:

- Claim Boundary Contract;
- Boundary Delta Record;
- Claim Consumption Event;
- System Mapping Receipt;
- Authority Policy Context;
- Non-Claims Contract or panel;
- Unsupported Inheritance Event record.

### 3. Execution Plane

The execution plane models the ordered sequence:

- upstream AI or workflow system produces an artifact;
- human reviewer accepts, modifies, or forwards;
- Fork records handoff state;
- downstream system consumes the artifact;
- downstream actor attempts reliance;
- Fork exposes whether reliance was preserved, narrowed, expanded, or unsupported.

Fork does not block runtime action. It makes the handoff inspectable.

### 4. Reconstruction Plane

The reconstruction plane models later review:

- Can a reviewer reconstruct what happened?
- Can they distinguish record integrity from correctness?
- Can they see unresolved state?
- Can they identify unsupported inheritance?
- Can they identify which system held which responsibility?

## Scenario Readiness Standard

Every simulation scenario must answer five questions:

1. What crossed the boundary?
2. What did not cross the boundary?
3. What did the downstream system try to infer?
4. Did Fork preserve enough state to expose the inference?
5. What remains outside Fork's authority?

If a scenario cannot answer these five questions, it is not ready for inclusion.

## Relationship to AHI and Recomputable Evidence

Accountable Handoff Interoperability remains the bounded research implementation focused on accountable handoff records and evaluation readiness.

Recomputable Evidence remains the parent strategic thesis for accountable digital evidence infrastructure.

Fork Governance Simulation Proof Surface is the operational calibration layer used to test and refine Fork's claim boundaries before integrating them into AHI evaluation protocols or Recomputable Evidence service positioning.

The simulation layer must not introduce new truth, compliance, certification, authority, or trust claims.
'@

$sequence = @'
# Fork Governance Simulation Sequence v0.1

## Overview

This document defines the initial sequence of governance simulation scenarios for the Fork Governance Simulation Proof Surface.

Each scenario models accountable handoffs between independently accountable systems, with and without Fork-style boundary records, to generate bounded evidence about handoff-state preservation, unsupported inheritance, and reconstructability.

## System Set

The scaled-down governance model uses five systems.

### System A — AI-Assisted Production System

Produces an artifact, memo, recommendation, summary, or decision-support object.

### System B — Fork Boundary-Record Layer

Preserves transition state:

- what was claimed;
- what was not claimed;
- what evidence was referenced;
- what authority context was recorded;
- what remained unresolved;
- what downstream revalidation is required.

### System C — Institutional Review / Policy Context System

Represents human review, policy context, and constrained acceptance.

This is not Fork.

### System D — Downstream Operational or Decision System

Consumes the artifact for action, approval, routing, escalation, or later institutional reliance.

### System E — Audit / Reconstruction / Oversight System

Used later to determine what crossed the boundary and whether unsupported inheritance occurred.

## Core Simulation Thesis

Independently accountable systems can remain valid within their own boundaries while still producing governance failure at the transitions between them.

Fork addresses that transition by preserving inspectable handoff state without becoming the authority, runtime, policy, compliance, or audit system.

## Scenario List

1. Scenario 01 — Baseline unbounded handoff.
2. Scenario 02 — Fork-preserved handoff.
3. Scenario 03 — Scope expansion attempt.
4. Scenario 04 — Authority leakage attempt.
5. Scenario 05 — Policy-reference laundering attempt.
6. Scenario 06 — Multi-system distributed handoff.

## Per-Scenario Evaluation Criteria

Each scenario must capture:

- Did unsupported inheritance occur?
- Was authority leakage visible?
- Were non-claims preserved?
- Could a later reviewer reconstruct the handoff?
- Did the downstream actor need new evidence or authority?
- Was the transition inspectable without turning Fork into the authority layer?

## Scenario 01 — Baseline Unbounded Handoff

### Goal

Show the failure mode without Fork.

### Flow

- System A produces a vendor-risk memo or similar decision-support artifact.
- A human reviewer in System C accepts or lightly edits the artifact.
- The artifact is handed directly to System D.
- The downstream actor infers approval, authority sufficiency, compliance sufficiency, or resolution completeness.

### Expected Result

The downstream system may rely on more than the upstream systems established.

### Evidence to Capture

- unsupported inheritance events;
- missing non-claims;
- missing authority boundary;
- missing revalidation boundary;
- ambiguity in later reconstruction.

## Scenario 02 — Fork-Preserved Handoff

### Goal

Show the same workflow with Fork-style records.

### Flow

- System A produces the artifact.
- System B records handoff state using boundary records and non-claim artifacts.
- System D receives the artifact and the bounded handoff record.
- System E reconstructs what was established, not established, and still required fresh authority.

### Expected Result

The downstream system can inspect the handoff boundary instead of silently expanding it.

### Evidence to Capture

- preserved claim scope;
- preserved non-claims;
- authority and policy context;
- unresolved state;
- revalidation requirements;
- comparison against Scenario 01.

## Scenario 03 — Scope Expansion Attempt

### Goal

Show why claim-boundary placement matters.

### Flow

- Upstream artifact establishes a narrow claim.
- Downstream consumer treats the claim as broader.
- Example: "reviewed" becomes "approved"; "vendor risk memo" becomes "vendor cleared."

### Fork Role

Fork does not block by force.

Fork makes expansion visible and inspectable.

### Evidence to Capture

- original claim scope;
- attempted downstream expansion;
- whether the expansion had new authority or evidence;
- whether the expansion was preserved as unsupported, unresolved, or newly justified.

## Scenario 04 — Authority Leakage Attempt

### Goal

Show the difference between recorded authority context and actual authority.

### Flow

- Workflow packet includes policy reference and reviewer role.
- Downstream actor infers that final approval authority existed.
- Fork preserves role, context, and policy reference while preserving the non-claim that policy reference is not policy approval.

### Evidence to Capture

- no authority transfer;
- policy presence not treated as applicability;
- evidence record not treated as authorization;
- unsupported authority inference.

## Scenario 05 — Policy-Reference Laundering Attempt

### Goal

Show how policy reference can be laundered into implied compliance.

### Flow

- A policy citation is introduced as contextual reference.
- Downstream system treats the citation as evidence of compliance with the cited policy.
- Fork records the distinction between policy referenced and policy satisfied.

### Evidence to Capture

- policy-reference non-claim;
- compliance inference;
- whether the downstream inference exceeded the recorded boundary.

## Scenario 06 — Multi-System Distributed Handoff

### Goal

Show Fork relevance to scalable distributed systems and interoperability.

### Flow

- System A produces an AI-assisted artifact.
- System B preserves handoff state.
- System C consumes the artifact and handoff record.
- System D routes or acts on it.
- System E reconstructs the transition later.

### Expected Result

Systems remain independently accountable while the handoff remains inspectable across multiple hops.

### Evidence to Capture

- multi-hop transition state;
- system-specific responsibility;
- preserved non-inheritance;
- reconstruction path;
- unresolved state across systems.

## Why This Matters

Most systems can log, score, route, monitor, or audit after the fact.

The simulation tests whether Fork can preserve transition state as a first-class governance object without absorbing the responsibilities of adjacent systems.
'@

$contracts = @'
# Fork Simulation Contracts and Interfaces v0.1

## Purpose

This document defines the contracts and interface artifacts used in Fork's governance simulation proof surface.

The purpose is to preserve and expose handoff-state behavior without turning Fork into an authority, runtime, policy, compliance, or audit system.

## Contract Artifacts

### Claim Boundary Contract

Describes the scope of claims crossing a boundary, including explicit inclusions, exclusions, and conditions.

### Boundary Delta Record

Captures changes in claim scope, authority context, evidence references, unresolved state, or downstream reliance between upstream and downstream states.

### Claim Consumption Event

Records how a downstream system consumed an upstream claim, including preserved, narrowed, expanded, unresolved, or unsupported reliance classifications.

### System Mapping Receipt

Records mapping between systems and artifacts at a boundary, including identifiers, roles, routing context, and mapping posture.

### Authority Policy Context

Documents policy references, roles, and constraints present at the time of handoff without asserting approval, applicability, compliance, or authority sufficiency.

### Non-Claims Panel

Enumerates explicit non-claims associated with the handoff.

Examples:

- not an approval;
- not a compliance certification;
- not legal sufficiency;
- not production readiness;
- not factual correctness;
- not institutional authority.

### Unsupported Inheritance Event Record

Records detected instances where downstream inference exceeded recorded claim scope, authority, evidence, or non-claims.

## Interface Discipline

Each contract is:

- bounded to a specific handoff boundary;
- inspectable;
- capable of being represented as structured data;
- designed to preserve state, not enforce runtime behavior;
- designed to avoid certifying correctness, compliance, or authority.

## Interface Questions

Every interface should answer:

1. What object crossed the boundary?
2. What claims were attached?
3. What non-claims remained attached?
4. What authority context was recorded?
5. What evidence references were preserved?
6. What unresolved state remained?
7. What downstream revalidation was required?
8. What did the downstream system do with the object?
9. Did any claim expansion occur?
10. Did any expansion have new authority or evidence?

## Prohibited Interface Drift

Simulation interfaces must not collapse:

- evidence into approval;
- policy reference into policy applicability;
- structural verification into factual correctness;
- human review into legal sufficiency;
- routing into authorization;
- auditability into compliance;
- recomputability into truth.

## Safe Interface Claim

Fork simulation interfaces preserve accountable handoff state for later inspection.

They do not decide whether the downstream reliance was justified.
'@

$failureModes = @'
# Fork Simulation Failure Modes v0.1

## Purpose

This document defines initial failure modes for the Fork Governance Simulation Proof Surface.

Failure modes are used to test whether Fork records expose unsupported inheritance, authority leakage, semantic compression, and downstream overreach.

## Failure Mode Classes

### FM-001: Claim Scope Expansion

A downstream system treats a narrow upstream claim as broader than recorded.

Example:

- Upstream: "reviewed for preliminary triage."
- Downstream: "approved for onboarding."

### FM-002: Authority Leakage

A downstream system treats recorded role or policy context as authority transfer.

Example:

- Upstream: "reviewed by vendor-risk analyst."
- Downstream: "authorized by vendor-risk function."

### FM-003: Policy-Reference Laundering

A downstream system treats a policy reference as policy applicability, policy satisfaction, or compliance approval.

Example:

- Upstream: "policy VR-PRELIM-001 referenced."
- Downstream: "complies with VR-PRELIM-001."

### FM-004: Structural Verification to Truth

A downstream system treats structural verification as factual correctness.

Example:

- Upstream: "packet structurally verifies."
- Downstream: "the vendor-risk conclusion is correct."

### FM-005: Human Review to Legal Sufficiency

A downstream system treats human review as legal, compliance, procurement, audit, or institutional sufficiency.

Example:

- Upstream: "human reviewer accepted memo."
- Downstream: "memo is legally sufficient for action."

### FM-006: Unresolved State Suppression

A downstream system omits or hides unresolved issues.

Example:

- Upstream: "SOC 2 evidence unavailable."
- Downstream: "security review complete."

### FM-007: Non-Claim Loss

A downstream system consumes a record but drops the associated non-claims.

Example:

- Upstream non-claim: "not approval."
- Downstream artifact: "approved vendor packet."

### FM-008: Delegation Collapse

A downstream system treats delegated review as final institutional decision authority.

Example:

- Upstream: "review delegated for triage."
- Downstream: "delegated reviewer approved final action."

### FM-009: Multi-Hop Semantic Compression

Multiple systems pass an artifact until original claim scope and unresolved state are compressed into a simpler status label.

Example:

- Original state: "reviewed with unresolved evidence gaps."
- Final state: "cleared."

## Failure Mode Recording Fields

Each failure mode instance should record:

| Field | Meaning |
|---|---|
| Failure mode ID | Stable identifier |
| Scenario ID | Scenario where failure occurred |
| Source system | System where claim originated |
| Consuming system | System where inference occurred |
| Original claim | What was actually recorded |
| Downstream inference | What was inferred |
| Boundary artifact | BDR, CBC, CCE, SMR, APC, or non-claim artifact |
| Exposure result | Exposed, not exposed, ambiguous |
| Non-claim status | Preserved, dropped, altered, absent |
| Revalidation requirement | Required, not required, unclear |
| Notes | Reviewer notes |

## Non-Claims

Failure-mode exposure does not prove that Fork prevents failure.

Failure-mode exposure does not establish compliance, correctness, authority, legal sufficiency, or production readiness.

The purpose is to test whether the failure becomes visible and reconstructable.
'@

$reconstruction = @'
# Fork Simulation Reconstruction Guide v0.1

## Purpose

This guide defines how a reviewer reconstructs simulated handoffs in the Fork Governance Simulation Proof Surface.

The goal is to determine whether a later reviewer can inspect what crossed the boundary, what did not cross, what was inferred downstream, and what remains outside Fork's authority.

## Reconstruction Questions

For every scenario, answer:

1. What artifact crossed the boundary?
2. What claims crossed with it?
3. What non-claims crossed with it?
4. What evidence references were preserved?
5. What authority or policy context was recorded?
6. What remained unresolved?
7. What did the downstream system infer?
8. Did the downstream inference preserve, narrow, expand, or exceed the recorded boundary?
9. Did any expansion include new authority or evidence?
10. What remains outside Fork's authority?

## Reconstruction Table

| Question | Reviewer Answer | Evidence Reference | Confidence |
|---|---|---|---|
| What crossed the boundary? | TBD | TBD | TBD |
| What did not cross? | TBD | TBD | TBD |
| What was inferred downstream? | TBD | TBD | TBD |
| Was claim scope preserved? | TBD | TBD | TBD |
| Were non-claims preserved? | TBD | TBD | TBD |
| Was authority inferred? | TBD | TBD | TBD |
| Was policy reference laundered? | TBD | TBD | TBD |
| Was unresolved state preserved? | TBD | TBD | TBD |
| What requires revalidation? | TBD | TBD | TBD |

## Reconstruction Outcomes

Use one of the following outcomes:

| Outcome | Meaning |
|---|---|
| RECONSTRUCTABLE_BOUNDARY | Reviewer can reconstruct the handoff boundary |
| PARTIALLY_RECONSTRUCTABLE_BOUNDARY | Reviewer can reconstruct some but not all boundary state |
| UNSUPPORTED_INHERITANCE_EXPOSED | Reviewer can identify downstream overreach |
| AUTHORITY_LEAKAGE_EXPOSED | Reviewer can identify implied authority transfer |
| POLICY_LAUNDERING_EXPOSED | Reviewer can identify policy reference treated as approval or compliance |
| NON_CLAIM_LOSS_EXPOSED | Reviewer can identify missing or dropped non-claims |
| NOT_RECONSTRUCTABLE | Reviewer cannot reconstruct the handoff boundary from available records |

## Non-Claims

Reconstruction does not determine whether the underlying decision was correct.

Reconstruction does not establish legal, compliance, procurement, audit, operational, or institutional sufficiency.

Reconstruction does not convert Fork into an authority layer.
'@

$exampleReadme = @'
# Fork Governance Simulation Proof Surface

## Purpose

This example package contains initial scenarios for the Fork Governance Simulation Proof Surface.

The simulation is a calibration environment for testing claim boundaries, handoff semantics, artifact formats, interface contracts, delegation behavior, and failure modes.

It is not a product demonstration, compliance proof, approval system, or correctness engine.

## Scenario Set

| Scenario | File | Purpose |
|---|---|---|
| 01 | `scenario_01_baseline_unbounded_handoff.md` | Show failure mode without Fork |
| 02 | `scenario_02_fork_preserved_handoff.md` | Show same workflow with Fork-style handoff records |
| 03 | `scenario_03_scope_expansion_attempt.md` | Show downstream claim expansion |
| 04 | `scenario_04_authority_leakage_attempt.md` | Show authority leakage |
| 05 | `scenario_05_policy_reference_laundering_attempt.md` | Show policy reference treated as compliance or approval |
| 06 | `scenario_06_multi_system_distributed_handoff.md` | Show multi-system distributed handoff reconstruction |

## Simulation Standard

Each scenario must answer:

1. What crossed the boundary?
2. What did not cross the boundary?
3. What did the downstream system try to infer?
4. Did Fork preserve enough state to expose the inference?
5. What remains outside Fork's authority?

## Non-Claims

This simulation does not establish correctness, compliance, legal sufficiency, institutional authority, production readiness, or general validity.
'@

$scenario01 = @'
# Scenario 01: Baseline Unbounded Handoff

## Purpose

This scenario models a vendor-risk handoff without Fork-style boundary records.

The goal is to expose how unsupported inheritance can occur when an AI-assisted artifact moves downstream without explicit handoff state.

## Participating Systems

| System | Role |
|---|---|
| System A | AI-assisted production system |
| System C | Institutional review / policy context system |
| System D | Downstream operational or decision system |
| System E | Audit / reconstruction / oversight system |

System B, the Fork boundary-record layer, is intentionally absent.

## Flow

1. System A produces an AI-assisted vendor-risk memo.
2. System C human reviewer accepts or lightly edits the memo.
3. The memo is sent to System D.
4. System D treats the memo as sufficient for downstream action.
5. System E later attempts reconstruction.

## What Crossed the Boundary

- AI-assisted vendor-risk memo.
- Human-reviewed status.
- Ordinary workflow notes.

## What Did Not Cross the Boundary

- Explicit non-claims.
- Authority sufficiency record.
- Policy applicability determination.
- Compliance determination.
- Revalidation requirements.
- Unresolved evidence gaps.

## Downstream Inference Attempt

System D infers:

- the vendor was approved;
- the reviewer had sufficient authority;
- the cited policy was satisfied;
- unresolved issues were resolved or irrelevant.

## Expected Failure Mode

Unsupported inheritance occurs because downstream reliance exceeds the recorded evidence.

## Reconstruction Result

Expected outcome:

`NOT_RECONSTRUCTABLE` or `PARTIALLY_RECONSTRUCTABLE_BOUNDARY`

## Non-Claims

This scenario does not prove that Fork would prevent the failure.

It establishes a baseline failure mode for later comparison.
'@

$scenario02 = @'
# Scenario 02: Fork-Preserved Handoff

## Purpose

This scenario models the same vendor-risk handoff with Fork-style boundary records.

The goal is to test whether explicit handoff-state records make claim scope, non-claims, authority context, unresolved state, and revalidation requirements inspectable.

## Participating Systems

| System | Role |
|---|---|
| System A | AI-assisted production system |
| System B | Fork boundary-record layer |
| System C | Institutional review / policy context system |
| System D | Downstream operational or decision system |
| System E | Audit / reconstruction / oversight system |

## Flow

1. System A produces an AI-assisted vendor-risk memo.
2. System C human reviewer accepts or modifies the memo.
3. System B records handoff state.
4. System D receives the memo and the bounded handoff record.
5. System E later reconstructs the handoff.

## Fork Records

Expected artifacts:

- Claim Boundary Contract;
- Boundary Delta Record;
- Claim Consumption Event;
- System Mapping Receipt;
- Authority Policy Context;
- Non-Claims Panel.

## What Crossed the Boundary

- AI-assisted vendor-risk memo.
- Recorded claim scope.
- Evidence references.
- Authority and policy context.
- Non-claims.
- Unresolved state.
- Revalidation requirements.

## What Did Not Cross the Boundary

- Final approval authority.
- Compliance determination.
- Legal sufficiency.
- Production readiness.
- Factual correctness guarantee.
- Institutional authorization.

## Downstream Inference Attempt

System D attempts to infer that the vendor was approved for onboarding.

## Expected Fork Behavior

Fork does not block the inference.

Fork exposes that the inference exceeds recorded claim scope unless supported by separate authority and evidence.

## Reconstruction Result

Expected outcome:

`UNSUPPORTED_INHERITANCE_EXPOSED`

## Non-Claims

This scenario does not establish that the vendor-risk decision was correct.

It tests whether the handoff boundary is reconstructable.
'@

$scenario03 = @'
# Scenario 03: Scope Expansion Attempt

## Purpose

This scenario tests whether Fork exposes a downstream claim expansion attempt.

## Flow

1. Upstream artifact records a narrow claim: preliminary vendor-risk review completed.
2. Downstream system treats the artifact as vendor cleared.
3. Fork records whether the downstream claim preserved, narrowed, expanded, or exceeded the upstream boundary.

## Original Claim

`Vendor-risk memo reviewed for preliminary triage only.`

## Downstream Inference

`Vendor cleared for onboarding.`

## Expected Classification

`CLAIM_SCOPE_EXPANSION`

## Expected Reconstruction Outcome

`UNSUPPORTED_INHERITANCE_EXPOSED`

## What Remains Outside Fork

- Whether the vendor should be onboarded.
- Whether the reviewer had approval authority.
- Whether compliance requirements were satisfied.
- Whether the decision was correct.
'@

$scenario04 = @'
# Scenario 04: Authority Leakage Attempt

## Purpose

This scenario tests whether Fork exposes authority leakage.

## Flow

1. A reviewer role is recorded in the authority/policy context.
2. Downstream system treats the recorded role as sufficient final authority.
3. Fork preserves the role context and the non-claim that role presence does not equal authority sufficiency.

## Recorded Context

`Vendor-risk analyst reviewed memo for preliminary triage.`

## Downstream Inference

`Vendor-risk function approved final action.`

## Expected Classification

`AUTHORITY_LEAKAGE`

## Expected Reconstruction Outcome

`AUTHORITY_LEAKAGE_EXPOSED`

## What Remains Outside Fork

- Whether the analyst had final authority.
- Whether the institution approved the action.
- Whether delegated review was sufficient.
'@

$scenario05 = @'
# Scenario 05: Policy-Reference Laundering Attempt

## Purpose

This scenario tests whether Fork exposes policy-reference laundering.

## Flow

1. A policy reference is included in the workflow context.
2. Downstream system treats the policy reference as policy applicability or compliance satisfaction.
3. Fork preserves the distinction between policy referenced and policy satisfied.

## Recorded Context

`Policy VR-PRELIM-REVIEW-v0.1 referenced during preliminary review.`

## Downstream Inference

`Workflow complied with VR-PRELIM-REVIEW-v0.1.`

## Expected Classification

`POLICY_APPROVAL_CONFUSION` or `COMPLIANCE_CERTIFICATION_CONFUSION`

## Expected Reconstruction Outcome

`POLICY_LAUNDERING_EXPOSED`

## What Remains Outside Fork

- Whether the policy applied.
- Whether the policy was satisfied.
- Whether compliance was determined.
- Whether the policy was current or adequate.
'@

$scenario06 = @'
# Scenario 06: Multi-System Distributed Handoff

## Purpose

This scenario tests whether Fork preserves handoff state across multiple independently accountable systems.

## Flow

1. System A produces an AI-assisted artifact.
2. System B preserves handoff state.
3. System C consumes the artifact and records constrained review context.
4. System D routes the artifact or takes downstream action.
5. System E reconstructs the transition later.

## Systems

| System | Native Responsibility | Fork Does Not Become |
|---|---|---|
| System A | Artifact production | Model evaluator |
| System B | Boundary-state preservation | Authority layer |
| System C | Institutional review context | Compliance oracle |
| System D | Routing or operation | Runtime controller |
| System E | Audit or reconstruction | Legal authority |

## Expected Result

The handoff remains inspectable across multiple hops without any system inheriting authority from another system by default.

## Expected Reconstruction Outcome

`RECONSTRUCTABLE_BOUNDARY`

Potential additional outcomes:

- `UNSUPPORTED_INHERITANCE_EXPOSED`
- `AUTHORITY_LEAKAGE_EXPOSED`
- `NON_CLAIM_LOSS_EXPOSED`

## What Remains Outside Fork

- Whether the final downstream action was correct.
- Whether governance authority was sufficient.
- Whether the institution should have acted.
- Whether compliance or legal requirements were satisfied.
'@

$checkScript = @'
# scripts/run_ahi_sim_v0_1_checks.ps1
# Focused checks for Fork Governance Simulation Proof Surface v0.1.
# Does not stage, commit, push, or tag.

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".git")) {
    throw "Run this script from the repository root, e.g. C:\N\fork-public-evidence"
}

Write-Host "Checking required simulation files..."

$required = @(
    "docs/simulations/FORK_SIMULATION_PROOF_SURFACE_DOCTRINE_v0_1.md",
    "docs/simulations/FORK_GOVERNANCE_SIMULATION_SEQUENCE_v0_1.md",
    "docs/simulations/FORK_SIMULATION_CONTRACTS_AND_INTERFACES_v0_1.md",
    "docs/simulations/FORK_SIMULATION_FAILURE_MODES_v0_1.md",
    "docs/simulations/FORK_SIMULATION_RECONSTRUCTION_GUIDE_v0_1.md",
    "examples/simulations/governance-proof-surface/README.md",
    "examples/simulations/governance-proof-surface/scenario_01_baseline_unbounded_handoff.md",
    "examples/simulations/governance-proof-surface/scenario_02_fork_preserved_handoff.md",
    "examples/simulations/governance-proof-surface/scenario_03_scope_expansion_attempt.md",
    "examples/simulations/governance-proof-surface/scenario_04_authority_leakage_attempt.md",
    "examples/simulations/governance-proof-surface/scenario_05_policy_reference_laundering_attempt.md",
    "examples/simulations/governance-proof-surface/scenario_06_multi_system_distributed_handoff.md"
)

foreach ($path in $required) {
    if (-not (Test-Path $path)) {
        Write-Host "FAIL: missing required file: $path"
        exit 1
    }
    Write-Host "FOUND: $path"
}

Write-Host ""
Write-Host "Running non-claims contract checker..."
python tools\check_non_claims_contract.py

Write-Host ""
Write-Host "Scanning simulation surface for prohibited overclaim language..."
$grepOutput = git grep -n -i "truth engine\|governance oracle\|compliance proof\|certifies compliance\|proves correctness\|proves compliance\|guarantees trust" -- docs/simulations examples/simulations

if ($LASTEXITCODE -eq 0) {
    Write-Host "FAIL: prohibited simulation overclaim language found:"
    Write-Host $grepOutput
    exit 1
}

if ($LASTEXITCODE -eq 1) {
    Write-Host "PASS: no prohibited simulation overclaim language found."
}
else {
    throw "git grep failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "PASS: ahi-sim-v0.1 simulation proof-surface checks completed."
'@

Write-Utf8NoBomFile -Path "docs/simulations/FORK_SIMULATION_PROOF_SURFACE_DOCTRINE_v0_1.md" -Content $doctrine -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "docs/simulations/FORK_GOVERNANCE_SIMULATION_SEQUENCE_v0_1.md" -Content $sequence -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "docs/simulations/FORK_SIMULATION_CONTRACTS_AND_INTERFACES_v0_1.md" -Content $contracts -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "docs/simulations/FORK_SIMULATION_FAILURE_MODES_v0_1.md" -Content $failureModes -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "docs/simulations/FORK_SIMULATION_RECONSTRUCTION_GUIDE_v0_1.md" -Content $reconstruction -Overwrite:$ForceOverwrite

Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/README.md" -Content $exampleReadme -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/scenario_01_baseline_unbounded_handoff.md" -Content $scenario01 -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/scenario_02_fork_preserved_handoff.md" -Content $scenario02 -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/scenario_03_scope_expansion_attempt.md" -Content $scenario03 -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/scenario_04_authority_leakage_attempt.md" -Content $scenario04 -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/scenario_05_policy_reference_laundering_attempt.md" -Content $scenario05 -Overwrite:$ForceOverwrite
Write-Utf8NoBomFile -Path "examples/simulations/governance-proof-surface/scenario_06_multi_system_distributed_handoff.md" -Content $scenario06 -Overwrite:$ForceOverwrite

Write-Utf8NoBomFile -Path "scripts/run_ahi_sim_v0_1_checks.ps1" -Content $checkScript -Overwrite:$ForceOverwrite

Write-Host ""
Write-Host "Done."
Write-Host ""
Write-Host "Next commands:"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\create_fork_simulation_proof_surface_v0_1.ps1 -ForceOverwrite"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1"