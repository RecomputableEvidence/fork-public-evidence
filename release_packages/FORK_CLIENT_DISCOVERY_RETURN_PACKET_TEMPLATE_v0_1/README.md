# Fork Client Discovery Return Packet Template v0.1

## Purpose

This package is a client-completable discovery return packet template for Fork.

It is used when a qualified prospect has a candidate workflow and needs to provide enough structured information for Fork to determine whether a client-specific evidence boundary and sidecar bridge can be responsibly scoped.

This is not an onboarding packet.

This is not a deployment package.

This is not a production integration specification.

This is not a legal, compliance, audit, security, or risk approval document.

## Governing posture

Fork is ready for qualified client discovery and co-integration mapping only when the client can identify a real workflow, source systems, access/export model, evidence artifacts, state transitions, security/data-handling constraints, institutional owners, and accepted non-claims.

The client-native sidecar bridge is discovered, not assumed.

This packet is the return path.

The client completes it and sends it back for review.

Fork uses the completed packet to determine whether a client-specific evidence boundary and sidecar bridge specification can be responsibly drafted.

## Intended users

This packet may be completed by or with input from:

- workflow owner
- legal operations lead
- compliance lead
- audit lead
- risk lead
- security or data-handling reviewer
- GRC owner
- enterprise AI governance lead
- source-system owner
- technical integration counterpart
- executive sponsor
- co-integration partner, if applicable

## What completion means

Completing this packet does not mean:

- Fork is deployed
- Fork is approved
- Fork has access to client systems
- Fork can capture all relevant evidence
- Fork can prove source completeness
- Fork can prove AI output correctness
- Fork can prove decision correctness
- Fork can satisfy compliance obligations
- Fork can assert legal admissibility
- Fork can control workflow execution

Completing this packet means:

The candidate workflow is sufficiently described for Fork to evaluate whether a bounded evidence-preservation pilot or co-integration mapping exercise may be responsibly scoped.

## Package contents

- `README.md`
- `PACKAGE_MANIFEST.json`
- `CLIENT_WORKFLOW_PROFILE.md`
- `SOURCE_SYSTEM_INVENTORY.md`
- `ACCESS_AND_EXPORT_MODEL.md`
- `AI_ASSISTED_SURFACE.md`
- `EVIDENCE_ARTIFACT_MAP.md`
- `STATE_TRANSITION_MAP.md`
- `SECURITY_AND_DATA_HANDLING_CONSTRAINTS.md`
- `INSTITUTIONAL_OWNERSHIP_MAP.md`
- `CLAIMS_AND_NON_CLAIMS_ACKNOWLEDGMENT.md`
- `CO_INTEGRATION_BOUNDARY.md`
- `CONFIGURATION_OUTPUT_TARGETS.md`
- `RELEASE_NOTES.md`
- `NEXT_STEPS.md`
- `SHA256SUMS.txt`

## Completion instruction

For each file, replace placeholder text such as `[CLIENT_TO_COMPLETE]`, `[YES/NO/UNKNOWN]`, and `[DESCRIBE]`.

Unknown information should remain explicitly marked as `UNKNOWN`.

Do not guess.

Do not remove unknowns to make the packet look complete.

Fork needs accurate boundary information, not optimistic assumptions.

## Return instruction

Return the completed packet as a folder or compressed archive.

Fork will review the returned packet for:

- workflow specificity
- source-system clarity
- export/access feasibility
- evidence boundary clarity
- accepted non-claims
- security and data-handling constraints
- institutional ownership
- co-integration boundaries, if applicable
- implementation blockers

## Review outcomes

A returned packet may result in one of the following:

- `DISCOVERY_RETURN_REVIEWABLE`
- `DISCOVERY_RETURN_INCOMPLETE`
- `DISCOVERY_RETURN_BLOCKED`
- `CLIENT_EVIDENCE_BOUNDARY_READY_TO_DRAFT`
- `NOT_SUITABLE_FOR_FORK_AT_THIS_STAGE`

## Boundary statement

Fork cannot responsibly design the client-native sidecar bridge until the client evidence boundary has been mapped.

This packet exists to make that mapping explicit.