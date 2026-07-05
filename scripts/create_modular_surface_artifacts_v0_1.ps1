param(
    [switch]$ForceOverwrite,
    [string]$Root = "."
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path -LiteralPath $Root).Path

$ArtifactDir = Join-Path $RepoRoot "docs\modular-surface"
$ModularSurfacePath = Join-Path $ArtifactDir "FORK_MODULAR_SURFACE_v0_1.md"
$SurfaceContractPath = Join-Path $ArtifactDir "FORK_SURFACE_INTERACTION_CONTRACT_v0_1.md"

function Write-RepoTextFile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [string]$Content
    )

    if ((Test-Path -LiteralPath $Path) -and -not $ForceOverwrite) {
        throw "Refusing to overwrite existing file: $Path. Re-run with -ForceOverwrite if replacement is intended."
    }

    $Parent = Split-Path -Parent $Path
    if (-not (Test-Path -LiteralPath $Parent)) {
        New-Item -ItemType Directory -Path $Parent -Force | Out-Null
    }

    # Normalize to LF for repo hygiene and write UTF-8 without BOM.
    $Normalized = $Content -replace "`r`n", "`n"
    $Normalized = $Normalized -replace "`r", "`n"
    $Normalized = $Normalized.TrimEnd() + "`n"
    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

    [System.IO.File]::WriteAllText(
        [System.IO.Path]::GetFullPath($Path),
        $Normalized,
        $Utf8NoBom
    )
}

$ModularSurfaceContent = @'
# Fork Modular Surface v0.1

## Purpose

Fork has matured from a bounded proof surface into modular evidence-boundary infrastructure.

Its surfaces are separable so each can be inspected, tested, and integrated without transferring authority across them.

The modular surface does not expand Fork's authority. It separates Fork's already-emerged responsibilities so each surface can be understood without collapsing into approval, compliance, runtime control, policy enforcement, admissibility, or truth certification.

## Governing Constraint

Fork's governing constraint is non-absorption of authority.

Fork may preserve, reference, bind, inspect, recompute, and reconstruct evidence-boundary records.

Fork does not convert those records into truth, approval, compliance, admissibility, institutional authority, model correctness, legal sufficiency, or downstream decision correctness.

No surface may cause Fork to inherit authority from another system, reviewer, policy, workflow, model, runtime, or downstream consumer.

## Surface Map

Fork's modular surface consists of six separable surfaces:

1. Evidence Boundary Surface
2. Transition Surface
3. Reliance Surface
4. Interoperability Surface
5. Simulation Surface
6. Commercial Surface

These surfaces are related, but they are not interchangeable.

## 1. Evidence Boundary Surface

The Evidence Boundary Surface is the invariant core of Fork.

It preserves:

- What was claimed.
- What was not claimed.
- What evidence was referenced.
- What exclusions or non-claims constrained interpretation.
- What verifier scope was declared.
- Whether the sealed record still structurally verifies.

This is the only surface where structural verification occurs.

Every other surface may reference the Evidence Boundary Surface, but no other surface may mutate it, reinterpret its semantics, or expand its verification scope.

The Evidence Boundary Surface supports structural verification of the record and its declared boundaries only.

It does not establish that the underlying claim is true, safe, compliant, approved, sufficient, admissible, authoritative, or decision-ready.

## 2. Transition Surface

The Transition Surface inspects boundary deltas.

It does not track workflow flow as such. It reconstructs what changed when an artifact crossed from one context, system, reviewer, or workflow into another.

The Transition Surface may inspect:

- Boundary delta between pre-transition and post-transition state.
- Semantic compression.
- Semantic expansion.
- Dropped exclusions.
- Dropped non-claims.
- Evidence suppression.
- Evidence loss.
- Authority injection attempts.
- Scope reclassification.
- Use-context reclassification.
- Decision-context reclassification.
- Boundary changes requiring revalidation or new authority.

The Transition Surface makes loss visible.

It does not decide the legal, compliance, operational, or institutional consequence of that loss.

## 3. Reliance Surface

The Reliance Surface records decision-context association.

It preserves where, when, by whom, and on what basis an artifact was relied upon.

The Reliance Surface binds reliance to:

- A role.
- A decision point.
- A time.
- An artifact state.
- A referenced Evidence Boundary record.
- Any relevant Transition record.
- Relied claims.
- Preserved non-claims.
- Excluded information.
- Unresolved unknowns.
- Boundary effect.

The Reliance Surface does not decide whether reliance was correct, justified, compliant, authorized, prudent, or legally sufficient.

It preserves enough context for later reconstruction of what reliance occurred.

## 4. Interoperability Surface

The Interoperability Surface defines how external systems interact with Fork without authority absorption.

External systems may contribute:

- Signals.
- Records.
- Manifests.
- Scores.
- Attestations.
- Policy outputs.
- Admission records.
- Execution proofs.
- Seal events.
- Governance receipts.

Fork may preserve and reference those materials as artifacts.

Interop inputs are treated as referenced artifacts, not adopted assertions.

Fork does not internalize external semantics as truth.

A SCQOS admission record, GLM manifest, AnchorStack proof, Verdict seal, policy output, or governance signal may be referenced by Fork without becoming Fork's own authority claim.

The Interoperability Surface exists to prevent semantic inheritance across systems.

## 5. Simulation Surface

The Simulation Surface is Fork's falsifiability engine.

It tests whether boundary conditions, transition constraints, reliance bindings, and interoperability assumptions continue to hold under recomposition, altered conditions, invalid handoffs, or adversarial interpretation.

The Simulation Surface may test:

- Boundary stress cases.
- Transition violations.
- Authority leakage attempts.
- Reliance misbinding.
- Semantic compression failure.
- Claim expansion attempts.
- Invalid interoperability mappings.
- Replay under preserved boundary conditions.
- Replay under altered boundary conditions.

Simulation is not merely illustrative.

It is structurally grounded recomposition under controlled conditions.

The Simulation Surface may reconstruct other surfaces for testing.

It may not redefine them.

## 6. Commercial Surface

The Commercial Surface is derivative.

It translates Fork's existing surfaces into buyer-readable workflow language for vendor risk, audit, compliance, legal, cyber governance, AI oversight, benchmark consumption, and other design-partner contexts.

The Commercial Surface may compose existing surfaces into workflow narratives.

It may not introduce new primitives, verification claims, authority claims, or product capabilities not already present in the underlying surfaces.

Its role is explanation, discovery, and workflow mapping.

It is not an expansion of Fork's architectural scope.

## Illustrative Thread: AI-Assisted Vendor Risk Review

An AI-assisted vendor risk report enters Fork.

The Evidence Boundary Surface preserves the model output, cited benchmarks, declared exclusions, evidence references, reviewer notes, and non-claims.

The Transition Surface records that the artifact was imported into an internal risk system, that benchmark scores were normalized, and that certain exclusions were dropped during handoff.

The Reliance Surface records that an analyst approved the vendor based on the normalized score, at a specific decision point, under a specific role and time context.

The Interoperability Surface references a SCQOS admission record as an external artifact, without adopting the SCQOS result as Fork-native truth or authority.

The Simulation Surface replays the sequence and shows that the approval path changes when the dropped exclusions are preserved.

The Commercial Surface allows an audit, risk, or compliance buyer to understand why this matters: a later reviewer can reconstruct why approval occurred, what was relied upon, what was missing, and where interpretation expanded beyond the original boundary, without Fork asserting that the approval was wrong, unlawful, noncompliant, or invalid.

## Status Boundary

Fork's modular surface is an architectural decomposition of evidence-boundary responsibilities.

It is not a claim that Fork is a runtime governance platform, approval system, compliance oracle, policy engine, model evaluator, legal sufficiency tool, or institutional authority layer.

Fork preserves the structure needed for independent reconstruction.

It does not own the downstream consequence of that reconstruction.
'@

$SurfaceContractContent = @'
# Fork Surface Interaction Contract v0.1

## Purpose

The Fork Surface Interaction Contract defines how Fork's modular surfaces may reference, derive from, reconstruct, and constrain one another.

This document exists to make the modular surface operationally legible for reviewers, design partners, integrators, future tests, fixtures, and checker design.

The contract does not expand Fork's authority. It defines where each surface must stop.

## Contract Scope

This contract governs the interaction of the following surfaces:

1. Evidence Boundary Surface
2. Transition Surface
3. Reliance Surface
4. Interoperability Surface
5. Simulation Surface
6. Commercial Surface

The contract applies to proposed features, integrations, examples, simulations, fixtures, design-partner workflows, and future checkers.

## Core Rules

### Rule 1: Evidence Boundary Immutability

The Evidence Boundary Surface is immutable after sealing.

Other surfaces may reference it.

Other surfaces may not mutate, rewrite, reinterpret, narrow, expand, or replace its sealed semantics.

### Rule 2: Structural Verification Locality

Structural verification occurs only at the Evidence Boundary Surface.

No other surface may claim that Fork has verified truth, approval, compliance, admissibility, safety, legal sufficiency, policy satisfaction, or institutional authority.

### Rule 3: Transition as Delta Inspection

The Transition Surface may compare pre-transition and post-transition states.

It may detect boundary delta, semantic compression, semantic expansion, evidence loss, non-claim loss, exclusion loss, and authority injection attempts.

It may not convert detected change into a policy judgment, compliance judgment, approval judgment, or legal conclusion.

### Rule 4: Reliance as Decision-Context Association

The Reliance Surface may record decision-context association.

It may bind a reliance event to a role, actor, artifact, decision point, time, Evidence Boundary record, and Transition record.

It may not decide whether the reliance was correct, justified, compliant, authorized, prudent, admissible, or legally sufficient.

### Rule 5: Interoperability as Reference, Not Adoption

The Interoperability Surface may preserve and reference external artifacts.

External artifacts may include manifests, admission records, seal events, proofs, scores, policy outputs, attestation records, and governance receipts.

Interop inputs are referenced artifacts, not adopted assertions.

Fork may preserve an external signal without internalizing that signal as Fork-native truth, authority, approval, compliance, or admissibility.

### Rule 6: Simulation as Falsifiability

The Simulation Surface may reconstruct and stress-test surface interactions.

It may model valid and invalid handoffs, authority leakage, semantic loss, claim expansion, reliance misbinding, and altered replay conditions.

It may not redefine the meaning of any surface.

It may not convert a passing simulation into a general approval, compliance, safety, sufficiency, or authority claim.

### Rule 7: Commercial Surface Derivation

The Commercial Surface may compose Fork's existing surfaces into buyer-readable workflow narratives.

It may not introduce new primitives, verification claims, authority claims, product claims, or runtime capabilities not already present in the underlying surfaces.

## Permitted References

The following references are permitted:

- Transition Surface may reference Evidence Boundary records.
- Reliance Surface may reference Evidence Boundary records.
- Reliance Surface may reference Transition records.
- Interoperability Surface may reference external artifacts.
- Interoperability Surface may bind external artifact references to Fork records.
- Simulation Surface may reference all surfaces for recomposition and failure testing.
- Commercial Surface may reference all surfaces for buyer-readable explanation.

A permitted reference does not imply authority transfer.

A permitted reference does not imply semantic adoption.

A permitted reference does not imply claim expansion.

## Prohibited Interactions

The following interactions are prohibited:

- Reliance Surface converting structural verification into approval.
- Reliance Surface converting a reviewer action into institutional correctness.
- Transition Surface converting boundary change into policy judgment.
- Transition Surface treating semantic compression as automatically acceptable.
- Interoperability Surface converting an external signal into Fork-native truth.
- Interoperability Surface importing external authority semantics.
- Simulation Surface converting a passing scenario into general compliance.
- Simulation Surface redefining surface semantics.
- Commercial Surface introducing capabilities absent from the technical surface.
- Any surface compressing non-claims, exclusions, or limitations into an approval signal.
- Any surface treating evidence preservation as evidence sufficiency.
- Any surface treating downstream use as retroactive authorization.

## Non-Absorption Test

Any proposed feature, integration, workflow, example, fixture, or surface extension should be rejected, isolated, or reframed if it answers yes to any of the following questions:

1. Does it assign truth value to an underlying claim?
2. Does it treat structural verification as approval?
3. Does it treat a referenced external artifact as Fork-native authority?
4. Does it imply compliance, admissibility, safety, legal sufficiency, or policy satisfaction?
5. Does it allow downstream reliance to expand the original boundary without a new boundary record?
6. Does it compress non-claims, exclusions, or limitations into a simpler approval signal?
7. Does it make Fork responsible for a decision owned by another workflow, reviewer, policy layer, runtime, institution, or downstream actor?
8. Does it allow interoperability to become semantic adoption?
9. Does it allow simulation success to become generalized assurance?
10. Does it allow commercial framing to introduce a primitive not present in the technical surface?

## Minimal Interaction Model

A surface interaction should be expressible as:

```text
source_surface
target_surface
reference_type
permitted_operation
prohibited_operation
authority_effect
semantic_effect
verification_effect
```

### Field Semantics

`source_surface` identifies the surface initiating the reference or interaction.

`target_surface` identifies the surface or external artifact being referenced.

`reference_type` identifies whether the interaction is a boundary reference, transition reference, reliance reference, external artifact reference, simulation reference, or commercial composition reference.

`permitted_operation` identifies what the source surface may do.

`prohibited_operation` identifies what the source surface must not do.

`authority_effect` must remain `NO_AUTHORITY_TRANSFER` unless a future non-Fork authority layer explicitly records otherwise outside Fork.

`semantic_effect` must remain bounded to reference, preservation, comparison, reconstruction, or composition.

`verification_effect` must not exceed the verification scope declared by the Evidence Boundary Surface.

## Candidate Machine-Readable Constraints

Future checker design may encode the following constraints:

```yaml
surface_interaction_contract_version: "v0.1"
interaction_id: "example-interaction-id"
source_surface: "RELIANCE_SURFACE"
target_surface: "EVIDENCE_BOUNDARY_SURFACE"
reference_type: "BOUNDARY_REFERENCE"
permitted_operations:
  - "REFERENCE"
  - "PRESERVE_CONTEXT"
prohibited_operations:
  - "MUTATE_BOUNDARY"
  - "REINTERPRET_SEMANTICS"
  - "EXPAND_VERIFICATION_SCOPE"
authority_effect: "NO_AUTHORITY_TRANSFER"
semantic_effect: "REFERENCE_ONLY"
verification_effect: "NO_NEW_VERIFICATION"
```

## Candidate Surface Identifiers

Future fixtures and checkers should use stable surface identifiers:

```text
EVIDENCE_BOUNDARY_SURFACE
TRANSITION_SURFACE
RELIANCE_SURFACE
INTEROPERABILITY_SURFACE
SIMULATION_SURFACE
COMMERCIAL_SURFACE
```

## Candidate Authority Effects

Future fixtures and checkers should use explicit authority-effect identifiers:

```text
NO_AUTHORITY_TRANSFER
AUTHORITY_REFERENCE_ONLY
AUTHORITY_EXPANSION_ATTEMPTED
AUTHORITY_BORROWING_ATTEMPTED
AUTHORITY_EFFECT_UNRESOLVED
```

## Candidate Semantic Effects

Future fixtures and checkers should use explicit semantic-effect identifiers:

```text
REFERENCE_ONLY
PRESERVATION_ONLY
DELTA_INSPECTION_ONLY
RECONSTRUCTION_ONLY
WORKFLOW_COMPOSITION_ONLY
SEMANTIC_ADOPTION_ATTEMPTED
SEMANTIC_EXPANSION_ATTEMPTED
SEMANTIC_COMPRESSION_DETECTED
```

## Candidate Verification Effects

Future fixtures and checkers should use explicit verification-effect identifiers:

```text
NO_NEW_VERIFICATION
STRUCTURAL_VERIFICATION_ONLY
VERIFICATION_SCOPE_REFERENCED
VERIFICATION_SCOPE_EXPANSION_ATTEMPTED
TRUTH_VERIFICATION_ATTEMPTED
COMPLIANCE_VERIFICATION_ATTEMPTED
APPROVAL_VERIFICATION_ATTEMPTED
```

## Fixture Classes

Future fixtures should include both valid and invalid interactions.

### Valid Fixture Classes

- Valid Evidence Boundary reference by Transition Surface.
- Valid Evidence Boundary reference by Reliance Surface.
- Valid Transition reference by Reliance Surface.
- Valid external artifact reference by Interoperability Surface.
- Valid recomposition by Simulation Surface.
- Valid buyer-readable composition by Commercial Surface.

### Invalid Fixture Classes

- Reliance converts structural verification into approval.
- Transition converts semantic loss into policy judgment.
- Interoperability adopts external score as Fork-native truth.
- Simulation treats passing replay as compliance assurance.
- Commercial Surface introduces runtime control capability.
- Any surface drops non-claims during composition.
- Any surface expands authority without a new boundary record.
- Any surface treats downstream reliance as retroactive authorization.

## Candidate Checker Outcomes

Future checkers may return bounded outcomes such as:

```text
SURFACE_INTERACTION_RECORDED
SURFACE_INTERACTION_CONFORMS
SURFACE_INTERACTION_NOT_INSPECTABLE
AUTHORITY_ABSORPTION_ATTEMPTED
SEMANTIC_ADOPTION_ATTEMPTED
VERIFICATION_SCOPE_EXPANSION_ATTEMPTED
COMMERCIAL_SURFACE_EXPANSION_ATTEMPTED
NON_CLAIM_COMPRESSION_DETECTED
```

Checker outcomes should not use generic approval language such as:

```text
APPROVED
COMPLIANT
SAFE
VALIDATED_AS_TRUE
AUTHORIZED
LEGALLY_SUFFICIENT
```

## Example: Reliance References Evidence and Transition

A Reliance Surface record may reference:

- The Evidence Boundary record for the artifact relied upon.
- The Transition record showing what changed before reliance.
- The role and decision point associated with reliance.
- The time reliance occurred.

The Reliance Surface may preserve this context.

It may not conclude that reliance was correct, approved, compliant, authorized, or legally sufficient.

## Example: Interop References SCQOS Without Adoption

An Interoperability Surface record may reference a SCQOS admission record.

Fork may preserve the SCQOS record as an external artifact.

Fork may bind the SCQOS artifact reference to a downstream Evidence Boundary or Reliance record.

Fork may not internalize the SCQOS admission result as Fork-native truth, approval, admissibility, or authority.

## Example: Simulation Replays Dropped Exclusions

A Simulation Surface record may replay a vendor-risk reliance path under two conditions:

1. Exclusions dropped during transition.
2. Exclusions preserved during transition.

The simulation may show that the reliance path changes.

It may not conclude that the vendor approval was unlawful, noncompliant, invalid, or wrong.

## Future Checker Design Notes

A future checker should evaluate whether a proposed surface interaction:

- Uses recognized surface identifiers.
- Uses recognized authority-effect identifiers.
- Uses recognized semantic-effect identifiers.
- Uses recognized verification-effect identifiers.
- Avoids prohibited operations.
- Preserves Evidence Boundary immutability.
- Avoids authority absorption.
- Avoids semantic adoption.
- Avoids verification-scope expansion.
- Keeps commercial claims derivative.

The checker should produce structural outcomes only.

It should not produce approval, compliance, safety, admissibility, legal sufficiency, or truth outcomes.

## Status Boundary

This contract is a v0.1 architectural and design-control artifact.

It is intended to guide reviewer interpretation, integration boundaries, fixture design, and future checker implementation.

It does not itself implement enforcement.

It does not certify any workflow, system, artifact, claim, organization, model, policy, or decision.
'@

Write-RepoTextFile -Path $ModularSurfacePath -Content $ModularSurfaceContent
Write-RepoTextFile -Path $SurfaceContractPath -Content $SurfaceContractContent

Write-Host "Created modular surface artifacts:" -ForegroundColor Green
Write-Host " - $ModularSurfacePath"
Write-Host " - $SurfaceContractPath"

Write-Host ""
Write-Host "SHA256:" -ForegroundColor Cyan
Get-FileHash -Algorithm SHA256 -LiteralPath $ModularSurfacePath, $SurfaceContractPath |
    Format-Table -AutoSize

if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host ""
    Write-Host "Git diff stat:" -ForegroundColor Cyan

    git -C $RepoRoot diff --stat -- `
        "docs/modular-surface/FORK_MODULAR_SURFACE_v0_1.md" `
        "docs/modular-surface/FORK_SURFACE_INTERACTION_CONTRACT_v0_1.md"
}
