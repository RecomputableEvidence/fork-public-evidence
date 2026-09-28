# FORK-SEMANTIC-STANDING-PROMOTION-CHECKER-001

Status: `CANDIDATE_REPAIR_SUCCESSOR__PRESSURE_FINDINGS_ADDRESSED_IN_CODE__INTERNAL_EXECUTION_PENDING`

Version: `v0.1.1-repair`

Predecessor head: `db8b02280ef88e002db6c8ffc3e9e139e4c5925b`

Predecessor pressure disposition: `MATERIAL_REPAIR_REQUIRED_BEFORE_FROZEN_SPEC_OR_EMPIRICAL_QUALIFICATION`

## Purpose

Explore a bounded, non-destructive checker for unsupported semantic-standing promotions in AI-generated text while preserving the source text byte-for-byte and keeping detection separate from adjudication.

The checker is not a policy oracle, semantic adjudicator, governance authority, production control, or general claim about LLM behavior.

## v0.1.1 repair boundary

The predecessor negative result remains preserved. This successor addresses only the frozen PR-001 through PR-011 pressure findings.

Load-bearing repairs:

- `STANDING_ENVELOPE_ENTRY != STANDING_PROOF`: envelope support now requires verified evidence bindings.
- `REGISTRY_FIELD_ASSERTED != FIELD_VERIFIED`: authorization, occurrence, and effectivity separate asserted status from verified status and evidence.
- `EVIDENCE_HASH_MATCH != EVIDENCE_ROLE_SUBJECT_STATUS_MATCH`: evidence identity now includes evidence ID, role, artifact, exact subject, PRESENT status, digest, and bytes.
- `BASIS_REFERENCE_PRESENT != BASIS_VERIFIED`: transition bases require evidence-backed basis roles.
- `SUPERSEDING_TRANSITION_DECLARED != SUPERSEDING_TRANSITION_VERIFIED`: temporal supersession requires the full verified transition gate.
- Runtime strict-contract validation rejects undeclared/missing input fields before semantic evaluation.
- Normalization is explicitly `DESCRIPTIVE_MAPPING_ONLY`; source assurance is limited to `SUPPLIED_ASSERTIONS_ONLY`.
- Temporal anchors carry provenance class and verification state.
- Scope is represented as typed coordinates over subject, dimension, surface, and claim.
- Per-assertion semantic outcomes use typed dispositions; PASS/WITHHOLD/INDETERMINATE remain execution actions only.

## Candidate execution surface

```text
python tools/check_semantic_standing_promotions.py \
  --source ai_output.md \
  --standing-envelope standing.json \
  --evidence-registry evidence.json \
  --transition-registry authorized_transitions.json \
  --assertions normalized_assertions.json \
  --json
```

The checker does not infer semantic standing from arbitrary prose. The source-bound normalized assertion sidecar supplies the claim vector. Omission of that sidecar remains `INDETERMINATE`.

## Candidate evidence gate

A transition can support an assertion only when the checker verifies:

1. exact subject identity,
2. exact standing dimension,
3. state alignment,
4. evidence-backed authorization,
5. evidence-backed occurrence,
6. evidence-backed effectivity,
7. verified temporal alignment,
8. transition evidence identity and bytes,
9. typed scope coverage,
10. no explicit non-effect collision,
11. evidence-backed transition basis.

Standing-envelope support is permitted only as an evidence-backed current-state index; the envelope cannot create standing merely by declaring a state.

## Regression surface

The predecessor contained six tests. The repair successor expands the population to 22 tests, including the frozen oracle-reintroduction paths for unverified statuses, wrong-role/wrong-subject/superseded evidence, basis verification, supersession poisoning, temporal provenance, conflicting transitions, version/dimension leakage, source preservation, and strict input-contract rejection.

`22 tests present != 22 tests passed` until an execution surface reports that result.

## Preservation structure

With `--output-dir`, the checker creates:

```text
source/original_ai_output.<ext>
analysis/promotion_findings.json
analysis/promotion_receipt.json
disposition/reviewer_decision.json
```

The reviewer record remains `PENDING_AUTHORIZED_DISPOSITION`.

## Nonclaims

- `REPAIR_IMPLEMENTED != REPAIR_QUALIFIED`
- `REGRESSION_PASS != INDEPENDENT_PRESSURE_PASS`
- `SUCCESSOR_BRANCH != REPOSITORY_ADMISSION`
- `CHECKER_FINDING != FINAL_SEMANTIC_ADJUDICATION`
- `SOURCE_BOUND_NORMALIZATION != COMPLETE_SOURCE_SEMANTIC_COVERAGE`
- `PREDECESSOR_NEGATIVE_RESULT_REMAINS_PRESERVED`
