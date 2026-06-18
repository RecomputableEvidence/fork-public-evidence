# Claim Inheritance Checker Output Boundary Lock v0.1.4

Artifact ID: `CLAIM_INHERITANCE_CHECKER_OUTPUT_BOUNDARY_LOCK_v0_1_4`

Status: `PUBLICATION_BOUNDARY_LOCK`

Related tags:

- `claim-inheritance-simulation-checker-hardening-v0.1.2`
- `claim-inheritance-simulation-checker-publication-support-v0.1.2`
- `claim-inheritance-simulation-checker-output-semantics-v0.1.3`

Proposed tag: `claim-inheritance-simulation-checker-output-boundary-lock-v0.1.4`

## 1. Purpose

v0.1.4 is an additive output-boundary lock.

It preserves v0.1.2 as the hardened structural checker milestone and v0.1.3 as the output-semantics correction layer.

v0.1.4 closes remaining automation-misuse risks by making the output harder to consume as a single approval-like signal.

## 2. Boundary-lock changes

v0.1.4 adds the following public-output safeguards:

- legacy output is disabled;
- machine-readable limitations are expanded;
- limitations are duplicated inside `structural_result` and `harness_result`;
- `safe_to_automate=false` is emitted;
- `automation_interpretation_required=true` is emitted;
- `do_not_map_to` lists forbidden interpretations;
- invalid-manifest mode includes `all_invalid_fixtures_produced_expected_structural_failures`;
- CI asserts the output shape directly.

## 3. Legacy output

`--legacy-output` is disabled in v0.1.4.

The checker returns `result_kind: LEGACY_OUTPUT_DISABLED` and exit code `2`.

This prevents pre-v0.1.3 top-level `ok` semantics from re-entering the public automation surface.

## 4. Machine-readable non-claims

The `limitations` object includes machine-readable non-claims including:

- `does_not_validate_approval`
- `does_not_validate_truth`
- `does_not_validate_compliance`
- `does_not_validate_policy_compliance`
- `does_not_validate_regulatory_compliance`
- `does_not_validate_legal_sufficiency`
- `does_not_validate_legal_chain_of_custody`
- `does_not_validate_legal_reliance`
- `does_not_validate_authority`
- `does_not_validate_evidence_sufficiency`
- `does_not_validate_actual_non_use`
- `does_not_validate_downstream_execution`
- `does_not_authorize_production_use`
- `safe_to_automate=false`
- `automation_interpretation_required=true`

## 5. Forbidden mappings

The checker emits a `do_not_map_to` list.

Structural conformance must not be mapped to:

- approval;
- truth;
- compliance;
- legal sufficiency;
- legal chain of custody;
- legal reliance;
- authority validity;
- evidence sufficiency;
- safety;
- medical correctness;
- operational authorization;
- production readiness;
- verified non-use;
- actual downstream execution.

## 6. Exit-code disclaimer

An exit code of `0` indicates only one of the following:

- in single-bundle mode, the submitted synthetic bundle passed structural protocol checks;
- in invalid-manifest mode, the negative-test harness produced expected structural failures.

Exit code `0` does not indicate approval, truth, compliance, authority validity, evidence sufficiency, legal sufficiency, safety, production authorization, or actual downstream behavior.

Relying only on exit code without reading the output-boundary fields is outside the checker contract.

## 7. Result object limitations

In v0.1.4, limitations are carried at the top level and inside result-specific objects.

For bundle checks:

- `limitations`
- `structural_result.limitations`

For invalid-manifest harness checks:

- `limitations`
- `harness_result.limitations`
- each fixture result also carries result-scoped limitations.

This protects against single-object parsers that inspect only `structural_result` or only `harness_result`.

## 8. Publication posture

v0.1.4 does not expand Fork's claim.

Fork still records structural claim-boundary behavior only.

Fork does not decide truth, safety, legal sufficiency, admissibility, compliance, authority validity, evidence sufficiency, medical correctness, operational authorization, production readiness, legal chain of custody, legal reliance, legal representation, verified non-use, or actual undisclosed downstream behavior.

## 9. Removed compatibility aliases

Ambiguous compatibility aliases are not emitted.

v0.1.4 does not emit:

- `runner.runner_succeeded`
- `harness_result.all_invalid_fixtures_rejected`

Consumers must use:

- `runner.command_completed`
- `runner.runner_outcome`
- `harness_result.all_invalid_fixtures_produced_expected_structural_failures`

This avoids reintroducing the ambiguity that v0.1.4 is designed to close.

## 9. Removed ambiguous aliases

v0.1.4 removes ambiguous compatibility aliases from public JSON output.

The checker does not emit:

- `runner.runner_succeeded`
- `harness_result.all_invalid_fixtures_rejected`

Consumers must use:

- `runner.command_completed`
- `runner.runner_outcome`
- `harness_result.all_invalid_fixtures_produced_expected_structural_failures`

This is an intentional backward-incompatible output-boundary lock. Wrappers relying on generic success-like fields must migrate.

Extracting `structural_result.structurally_conformant` without also validating the adjacent `limitations`, `safe_to_automate=false`, and `do_not_map_to` fields is outside the checker contract.
