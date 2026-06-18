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
