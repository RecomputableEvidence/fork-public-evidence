# Longitudinal Reconstruction Trial Day-0 Packet v0.1

Status: Day-0 fixture packet.
Trial: fork_longitudinal_reconstruction_trial_v0_1
Packet: LRT_DAY0_PACKET_v0_1

## Purpose

This packet creates the first sealed Day-0 object for Fork's longitudinal reconstruction trial.

The trial question is:

Can a future reviewer reconstruct today's evidence state later without inheriting today's authority?

## Packet Contents

- packet_manifest.json
- packet_manifest.sha256
- packet_manifest_outer_receipt.json
- boundary/day0_non_authority_boundary_statement.txt
- evidence/day0_request_record.json
- evidence/day0_ai_output_record.json
- evidence/day0_human_review_record.json
- evidence/day0_boundary_state_record.json
- evidence/day0_non_claims_record.json
- expected/day0_expected_reconstruction.json
- environment/day0_environment_manifest.json
- receipts/day0_generation_receipt.json
- receipts/day0_expected_reconstruction_provenance_receipt.json
- receipts/day0_packet_scope_receipt.json

## Verification

Run from repository root:

- python tools/check_longitudinal_reconstruction_day0_packet_v0_1.py --json

The checker verifies:

- required packet files exist;
- artifact hashes match the manifest;
- packet_manifest.sha256 matches packet_manifest.json;
- packet_manifest_outer_receipt.json binds the manifest hash;
- expected reconstruction hash matches the expected reconstruction file;
- environment manifest hash matches the environment file;
- non-authority boundary statement hash matches the boundary file;
- non-authority language remains explicit.

## Boundary

This packet is a reconstruction fixture. It is not an endorsement, validation, certification, compliance opinion, legal opinion, safety assessment, production-readiness assessment, procurement approval, or authority transfer.