# Longitudinal Day-0 Schema Presence vs Schema Enforcement v0.1

Status: Checker-scope clarification.
Scope: Longitudinal Reconstruction Day-0 packet.

## 1. Purpose

This note clarifies a Day-0 checker-scope distinction surfaced in Public Review Round 005:

- the Day-0 packet manifest schema is present in the repository;
- the schema is routed through the public proof surface;
- the schema file is included in public verifier path coverage;
- the Day-0 checker v0.1 does not mechanically enforce the schema.

This is a scope clarification, not a schema-enforcement upgrade.

## 2. Current schema presence

The Day-0 schema artifact is present at:

- `schemas/longitudinal_reconstruction_day0_packet_manifest_v0_1.schema.json`

The Day-0 packet manifest is present at:

- `docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/packet_manifest.json`

The public verifier requires the schema path to exist.

## 3. Current Day-0 checker behavior

The Day-0 checker currently verifies:

- required packet paths are present;
- `packet_manifest.json` parses as JSON;
- `packet_manifest_outer_receipt.json` parses as JSON;
- required manifest fields are present;
- artifact byte hashes match the manifest;
- expected reconstruction hash matches;
- environment manifest hash matches;
- non-authority boundary statement hash matches;
- manifest sidecar hash matches;
- outer receipt manifest hash binding matches;
- non-authority terms are present in selected text fields.

## 4. What is not currently enforced

The Day-0 checker v0.1 does not currently:

- import `jsonschema`;
- load the Day-0 manifest schema file as a validation schema;
- validate `packet_manifest.json` against the schema;
- validate nested evidence records against schema files;
- validate receipt records against schema files;
- convert schema presence into schema enforcement.

Therefore, reviewer language should avoid saying:

- "the Day-0 manifest is schema-validated";
- "the Day-0 packet is schema-enforced";
- "the Day-0 checker validates the manifest against its JSON Schema";
- "schema presence proves schema conformance."

Permitted language:

- "the schema file is present";
- "the public verifier requires the schema path";
- "the Day-0 checker verifies manifest structure through its own required-field and hash checks";
- "schema enforcement is not implemented in v0.1."

## 5. Future upgrade path

A future schema-enforcement upgrade would require at least:

- explicit schema-validation implementation;
- recorded validator behavior;
- invalid manifest fixture coverage;
- valid manifest fixture coverage;
- public verifier integration;
- updated reviewer-facing language;
- a separate response receipt.

## 6. Boundary statement

This note clarifies checker scope only. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, schema conformance, production readiness, procurement approval, or institutional authority.

<!-- FORK_DAY0_SCHEMA_SCOPE_EXPLICIT_SENTENCE:START -->

## Explicit v0.1 schema-scope sentence

For checker-scope purposes: schema presence is recorded; schema enforcement is not implemented; the schema file is present; the Day-0 checker does not mechanically enforce the schema.

This sentence is intentionally explicit so reviewers and automated scope checks do not confuse schema path coverage with schema validation.

<!-- FORK_DAY0_SCHEMA_SCOPE_EXPLICIT_SENTENCE:END -->

<!-- BEGIN FORK_DAY0_SCHEMA_INTEGRATION_UPGRADE_V0_1 -->
## Subsequent mechanical schema-enforcement integration

The original Day-0 checker remains a custom required-field, hash, manifest-binding, and boundary-language checker.

A separate integration validator now mechanically exercises:

- `schemas/longitudinal_reconstruction_day0_packet_manifest_v0_1.schema.json` against the Day-0 packet manifest;
- `schemas/longitudinal_day0_temporal_replay_receipt_v0_1.schema.json` against the Day-0 replay receipt.

Run:

```bash
python tools/validate_json_schema_bundle_v0_1.py --json
```

Correct bounded language:

- the Day-0 manifest is JSON-Schema validated when the integration validator passes;
- the original Day-0 checker itself is not thereby converted into a general JSON-Schema engine;
- schema conformance does not establish truth, sufficiency, compliance, legal adequacy, authorization, approval, production readiness, or authority.
<!-- END FORK_DAY0_SCHEMA_INTEGRATION_UPGRADE_V0_1 -->
