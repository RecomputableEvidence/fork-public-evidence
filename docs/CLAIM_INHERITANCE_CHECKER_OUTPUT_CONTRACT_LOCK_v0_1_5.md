Claim Inheritance Checker Output Contract Lock v0.1.5

Artifact ID: CLAIM_INHERITANCE_CHECKER_OUTPUT_CONTRACT_LOCK_v0_1_5
Status: FINAL_OUTPUT_CONTRACT_LOCK_BEFORE_GITHUB_RELEASE
Related tag: claim-inheritance-simulation-checker-output-contract-lock-v0.1.5

1. Purpose
v0.1.5 is an additive output-contract lock. It preserves the v0.1.4 CLI execution path and wraps public output with a stricter output-contract boundary.

2. Contract description and enforcement
v0.1.5 uses:
- a published checker-output JSON Schema at schemas/claim_inheritance_checker_output_v0_1_5.schema.json
- runtime output-contract validation before stdout emission
- fail-closed output when the public output boundary violates the contract.

3. Field-name lock
v0.1.5 intentionally removes positive or ambiguous legacy public fields:
- top-level ok
- runner_succeeded
- structurally_conformant
- checker_structurally_conformant
- all_invalid_fixtures_rejected

Consumers must use:
- structural_result.structural_protocol_passed
- checker_structural_protocol_passed
- all_invalid_fixtures_produced_expected_structural_failures

4. Structural protocol pass is not approval
structural_result.structural_protocol_passed=true means only that the submitted synthetic bundle passed the structural protocol checks implemented by the checker. It does not mean truth, safety, legal sufficiency, admissibility, compliance, authority validity, evidence sufficiency, medical correctness, operational authorization, production readiness, verified non-use, or actual downstream execution.

5. Output contract failure
If output validation fails, the checker must fail closed using:
- result_kind=OUTPUT_CONTRACT_VIOLATION
- safe_to_automate=false
- automation_interpretation_required=true
- structural_result=null
- harness_result=null

6. Non-claim preservation
The limitations object is mandatory at root and result-specific levels. Harness root limitations additionally carry does_not_indicate_structural_conformance=true. It includes explicit non-claims for approval, truth, safety, compliance, policy compliance, regulatory compliance, legal sufficiency, legal chain of custody, legal reliance, authority, evidence sufficiency, medical correctness, operational authorization, production readiness, actual non-use, downstream execution, and actual downstream execution.

7. Forbidden mappings
The do_not_map_to list prohibits mapping structural protocol pass to approval, truth, compliance, legal sufficiency, legal chain of custody, legal reliance, authority validity, evidence sufficiency, safety, medical correctness, operational authorization, production readiness, verified non-use, or actual downstream execution.

8. Scope
This release does not expand Fork's claim. It remains a structural synthetic protocol checker only.
