# Claim Inheritance Checker Output Semantics v0.1.3

Artifact ID: `CLAIM_INHERITANCE_CHECKER_OUTPUT_SEMANTICS_v0_1_3`

Status: `PUBLICATION_SAFETY_CORRECTION_LAYER`

Related hardening tag: `claim-inheritance-simulation-checker-hardening-v0.1.2`

Related publication-support tag: `claim-inheritance-simulation-checker-publication-support-v0.1.2`

Proposed tag: `claim-inheritance-simulation-checker-output-semantics-v0.1.3`

## 1. Purpose

This note defines the v0.1.3 machine-readable output semantics for the Fork claim-inheritance simulation checker.

The purpose of v0.1.3 is to prevent downstream automation from confusing runner success, structural conformance, invalid-fixture harness success, truth, compliance, authority validity, evidentiary sufficiency, legal sufficiency, safety, or production authorization.

## 2. Core rule

The checker output must not use a generic top-level `ok` field as the canonical machine-readable status.

v0.1.3 separates status into:

- `runner.runner_succeeded`
- `structural_result.structurally_conformant`
- `harness_result.all_invalid_fixtures_rejected`

These fields must not be collapsed into a single approval, compliance, safety, truth, authority, evidence-sufficiency, or production-authorization signal.

## 3. Single-bundle output

For a normal bundle check, the checker emits `result_kind: STRUCTURAL_BUNDLE_CHECK`.

`structural_result.structurally_conformant=true` means only that the submitted synthetic bundle passed the current structural protocol checks.

It does not mean truth, safety, legal sufficiency, admissibility, compliance, authority validity, evidence sufficiency, production authorization, or actual downstream behavior.

## 4. Invalid-fixture harness output

For `--invalid-manifest`, the checker emits `result_kind: INVALID_FIXTURE_HARNESS`.

Harness success means the negative-test harness behaved as expected.

Harness success does not mean the invalid fixtures are structurally conformant.

`harness_result.all_invalid_fixtures_rejected=true` must not be mapped to structural conformance.

## 5. Exit code policy

For v0.1.3:

- single-bundle check returns exit code `0` only when `structural_result.structurally_conformant=true`;
- single-bundle check returns non-zero when structural errors are detected;
- invalid-manifest mode returns exit code `0` only when all invalid fixtures are rejected as expected;
- runner errors return exit code `2`.

Exit code `0` does not imply approval, truth, compliance, authority validity, evidence sufficiency, legal sufficiency, safety, or production authorization.

## 6. Machine-readable limitations

Every default CLI output includes a `limitations` object.

The limitations object carries structural-only non-claims, including:

- synthetic corpus only;
- does not validate truth;
- does not validate safety;
- does not validate compliance;
- does not validate legal sufficiency;
- does not validate admissibility;
- does not validate authority;
- does not validate evidence sufficiency;
- does not validate medical correctness;
- does not validate operational authorization;
- does not authorize production use;
- does not observe undisclosed downstream behavior.

## 7. Legacy output

The checker may retain `--legacy-output` for local compatibility.

Legacy output is not the canonical public automation interface for v0.1.3.

Downstream systems should consume the v0.1.3 output semantics, not the pre-v0.1.3 generic `ok` shape.

## 8. Publication-safety statement

v0.1.3 does not replace the v0.1.2 checker doctrine.

It adds a publication-safety correction layer so the machine-readable output carries the same boundary discipline as the human-readable limitations note.

Runner success is not structural conformance.

Structural conformance is not truth.

Structural conformance is not compliance.

Structural conformance is not authority validation.

Structural conformance is not evidence sufficiency.

Structural conformance is not production authorization.
