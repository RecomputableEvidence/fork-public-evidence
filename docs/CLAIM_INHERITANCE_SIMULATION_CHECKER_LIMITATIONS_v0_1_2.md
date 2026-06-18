# Claim Inheritance Simulation Checker Limitations v0.1.2

Artifact ID: `CLAIM_INHERITANCE_SIMULATION_CHECKER_LIMITATIONS_v0_1_2`

Status: `PUBLICATION_GRADE_FOR_V0_1_2_HARDENED_CHECKER_TAG`

…(your full limitations markdown exactly as written)…

## Guardrail phrases

The checker status is `PUBLICATION_GRADE_FOR_V0_1_2_HARDENED_CHECKER_TAG`.

The checker does not evaluate whether any claim is true.

`AUTHORITY_REF_STRUCTURALLY_REACHABLE` means the reference is structurally represented as reachable. It does not mean authority validity.

`CLAIM_NON_USAGE_DECLARED` means non-use was declared. It does not mean verified non-use.

The checker is not a governance verdict engine.

The checker is not a compliance checker.

The checker is not a truth checker.

The checker is not an authority validator.

## v0.1.3 output-semantics correction

The v0.1.3 output-semantics hardening separates runner success, structural conformance, and invalid-fixture harness success.

The canonical public CLI output no longer relies on a generic top-level `ok` field.

Machine consumers should use:

- `runner.runner_succeeded` for command execution;
- `structural_result.structurally_conformant` for structural bundle conformance;
- `harness_result.all_invalid_fixtures_rejected` for invalid-manifest harness success.

Invalid-manifest harness success does not indicate structural conformance of the invalid fixtures.

Structural conformance does not indicate truth, compliance, authority validity, evidence sufficiency, legal sufficiency, safety, or production authorization.

## v0.1.4 output-boundary lock

The v0.1.4 output-boundary lock is an additive publication-safety hardening layer.

It preserves v0.1.2 as the hardened structural checker milestone and v0.1.3 as the output-semantics correction layer.

v0.1.4 adds:

- disabled legacy output;
- expanded machine-readable limitations;
- duplicated limitations inside result objects;
- `safe_to_automate=false`;
- `automation_interpretation_required=true`;
- a `do_not_map_to` list;
- an explicit invalid-manifest alias: `all_invalid_fixtures_produced_expected_structural_failures`;
- CI assertions for output shape.

Exit code `0` remains structural-only. It does not indicate approval, truth, compliance, authority validity, evidence sufficiency, legal sufficiency, safety, production authorization, or actual downstream behavior.

## v0.1.4 removed compatibility aliases

v0.1.4 removed ambiguous compatibility aliases from public output.

The checker does not emit `runner.runner_succeeded`.

The checker does not emit `harness_result.all_invalid_fixtures_rejected`.

Machine consumers must use `runner.command_completed`, `runner.runner_outcome`, and `harness_result.all_invalid_fixtures_produced_expected_structural_failures`.

## v0.1.4 alias purge

v0.1.4 removes ambiguous compatibility aliases from public output.

The checker does not emit `runner.runner_succeeded`.

The checker does not emit `harness_result.all_invalid_fixtures_rejected`.

Machine consumers must use `runner.command_completed`, `runner.runner_outcome`, and `harness_result.all_invalid_fixtures_produced_expected_structural_failures`.

The removal is intentional because generic success-like aliases can cause downstream systems to collapse structural evidence into approval, truth, compliance, authority validity, evidence sufficiency, safety, legal sufficiency, or production authorization.
