# Pilot Data-Handling Schedule v0.1.4

## Purpose

This schedule defines the data-handling posture for a controlled Fork pilot.

It supports out-of-band evidence-boundary preservation while minimizing data movement, limiting access, preserving institutional control, and avoiding production runtime coupling.

## Data-handling posture

Fork should be configured for minimum-necessary observation.

The preferred pilot mode is to preserve structured references, hashes, timestamps, artifact identifiers, claim boundaries, non-claim boundaries, verification receipts, graph-preservation results, and packet metadata rather than exporting full source content.

## Deployment and capture mode

The pilot separates deployment location from capture mode.

Capture mode means the class of data Fork is permitted to receive or store during pilot ingestion.

Hash/reference-only mode may operate inside an institution-controlled deployment.

## PHI and regulated-data posture

For healthcare payor workflows, the pilot should assume source artifacts may contain PHI or other regulated data.

Fork's preferred pilot configuration is hash/reference-only or institution-controlled processing. If the institution determines that Fork will create, receive, maintain, or transmit PHI on behalf of a covered entity, the pilot should proceed only under the institution's required HIPAA, BAA, security, privacy, access-control, and retention process.

## Named pilot artifacts

This schedule creates three named pilot artifacts whose completion is required before live ingestion begins:

1. Redaction Scope Artifact — identifies what Fork may receive in redacted-content mode.
2. Pilot Canonicalization Record — identifies the approved hashing and canonicalization or byte-preservation procedure.
3. Dry-Run Approval Artifact — records institutional approval of the dry run before live ingestion is authorized.

## Approved source systems

Fork should not ingest from unapproved sources. Unknown, unexpected, or unregistered sources should be logged and excluded by default.

## Hashing and reference preservation

The artifact hash is the preferred structural anchor for later recomputation or integrity checking. Hashing should be performed under a documented canonicalization or byte-preservation procedure approved for the pilot.

The institution-approved Pilot Canonicalization Record controls the pilot implementation.

## Dry-run gate

Live ingestion should not begin until dry-run output is reviewed and approved by the institution's designated technical sponsor and privacy or security sponsor.

The dry run is the pilot gate. First live ingestion should not be treated as the dry run.

## Schedule non-claims

This schedule does not claim HIPAA compliance certification, BAA sufficiency, legal admissibility, regulatory compliance, medical correctness, factual completeness, source truth, clinical safety, model quality, institutional approval, production readiness, or replacement of existing audit trails, legal holds, discovery processes, regulator-facing documentation, utilization-management review, or appeal processes.

Fork preserves structural evidence boundaries. The institution remains responsible for legal, privacy, security, clinical, compliance, operational, and records-governance determinations.
