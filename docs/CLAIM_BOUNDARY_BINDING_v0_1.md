# Fork Claim Boundary Binding v0.1

Status: INTERNAL_BINDING_LAYER

Depends on:

- docs/CLAIM_BOUNDARY_CONTRACT_v0_1.md
- docs/CLAIM_BOUNDARY_ENFORCEMENT_PHASE_2.md
- schemas/claim_boundary_v0_1.schema.json
- tools/check_claim_boundary.py
- tools/check_artifact_claim_boundary.py

## 1. Purpose

Claim Boundary Binding moves Fork from artifact-level requirement to emission-time attachment.

Phase 1 made overclaiming fail inside a claim boundary payload.

Phase 2 made the claim_boundary block mandatory for eligible machine-readable artifacts.

Binding v0.1 makes the claim boundary derivable from an approved claim profile and attachable to a verifier or release artifact before it is treated as valid.

## 2. Binding Rule

No Fork verifier output, receipt, release metadata artifact, or machine-readable evidence summary should be emitted as valid unless it is bound to an approved claim profile.

Binding means:

- The source artifact is read.
- An approved claim profile is read.
- A claim_boundary block is derived from that profile.
- The claim_boundary block is attached to the artifact.
- The resulting artifact must pass artifact-level Claim Boundary enforcement.

## 3. Approved Claim Profile

The only approved claim profile in v0.1 is:

- claim_profiles/OBSERVED_WORKFLOW_EVENT_INTEGRITY_ONLY_v0_1.json

It supports the claim type:

- OBSERVED_WORKFLOW_EVENT_INTEGRITY_ONLY

This profile allows only integrity and execution-of-checks claims.

## 4. No Naked PASS Rule

A verifier result that says PASS without a bound claim boundary is structurally incomplete.

A naked PASS invites claim inflation. A bounded PASS states:

- What passed
- What failed
- What was not checked
- What the result does not prove
- Where later human, legal, causal, or institutional judgment must begin

## 5. Existing Claim Boundary Policy

By default, the binding tool refuses to bind an artifact that already contains a claim_boundary block.

This prevents silent overwrites and ad hoc claim mutation.

Replacement requires an explicit flag:

- --replace-existing-claim-boundary

## 6. v0.1 Invariant

No Fork verifier output may be treated as valid unless it carries a claim boundary derived from an approved claim profile and passes artifact-level Claim Boundary enforcement.

## 7. Architectural Position

Evidence packets preserve observable state.

Verification receipts recompute integrity.

Claim profiles define the permissible inference surface.

Claim Boundary Binding attaches that surface to emitted artifacts.

Reconstruction and hypothesis layers must consume bounded evidence rather than inventing claim limits after the fact.