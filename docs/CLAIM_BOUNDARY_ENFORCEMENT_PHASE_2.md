# Fork Claim Boundary Enforcement Phase 2

Status: INTERNAL_ENFORCEMENT_LAYER

Depends on:

- docs/CLAIM_BOUNDARY_CONTRACT_v0_1.md
- schemas/claim_boundary_v0_1.schema.json
- tools/check_claim_boundary.py

## 1. Purpose

Phase 2 moves Claim Boundaries from payload-level validation into artifact-level enforcement.

A machine-readable Fork receipt, release metadata artifact, or reviewer-facing machine summary is not valid unless it carries a top-level `claim_boundary` block that passes the Claim Boundary checker.

Phase 1 made overclaiming fail inside a claim boundary payload.

Phase 2 makes the claim boundary block mandatory for machine-readable artifacts that declare what a Fork artifact proves.

## 2. Enforcement Rule

Every eligible machine-readable artifact must include a top-level `claim_boundary` object.

The `claim_boundary` object must include:

- `claim_type`
- `claim_statement`
- `allowed_inferences`
- `forbidden_inferences`
- `not_checked`
- `non_claims`

The block must pass:

    python tools/check_claim_boundary.py <claim_boundary_payload>

For full artifacts, the artifact must pass:

    python tools/check_artifact_claim_boundary.py <artifact_json>

## 3. Eligible Artifact Classes

Phase 2 applies to machine-readable artifacts that declare what Fork evidence, receipts, releases, or summaries establish.

Examples:

- Verification receipts
- Coherence receipts
- Future conformance receipts
- Release metadata JSON
- Reviewer-facing machine summaries
- Machine-readable evidence summaries

## 4. v0.1 Artifact-Level Invariant

A machine-readable artifact is invalid if:

- It has no top-level `claim_boundary` block.
- Its `claim_boundary` block is not a JSON object.
- Its `claim_boundary` block fails schema validation.
- Its `claim_boundary` block contains a claim-expanding term in `claim_statement` or `allowed_inferences`.
- Its `claim_type` exceeds the supported v0.1 vocabulary.

## 5. Boundary of Phase 2

Phase 2 does not yet perform repository-wide automatic discovery of every historical JSON artifact.

Instead, it provides the enforcement gate that release scripts and CI must call against every eligible machine-readable receipt or release metadata artifact.

A later phase may add repository-wide discovery rules. Phase 2 is intentionally explicit: artifacts become governed when they are passed through the artifact-level checker.

## 6. Constitutional Rule

No Fork receipt, release metadata artifact, or machine-readable evidence summary should be treated as valid unless it contains a passing claim boundary block.

This is the operational form of the Claim Boundary invariant:

Every Fork evidence artifact must carry its evidentiary perimeter.