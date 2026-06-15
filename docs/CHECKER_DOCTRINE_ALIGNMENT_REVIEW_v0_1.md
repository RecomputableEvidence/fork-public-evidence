# Checker Doctrine Alignment Review v0.1

Status: Review Artifact  
Version: v0.1  
Scope: Semantic alignment review of `check_ai_governance_mapping_record_v0_1.py` against Fork AI governance mapping doctrine  
Review target: `bd9d006` / AI Governance Mapping Record Schema and Checker v0.1

## Purpose

This review answers a different question than the checker reproducibility run.

The reproducibility run asks:

> Does the checker classify the committed fixtures the same way across environments?

This semantic alignment review asks:

> Do the checker rules correspond to the doctrine they are supposed to enforce, and where are the boundaries of that correspondence?

This review is intentionally bounded. It does not convert Fork into a legal authority, compliance engine, audit substitute, policy engine, runtime controller, or decision validator.

Boundary phrase anchors:

- This review is not a policy engine.
- This review is not a full semantic verifier.

## Reviewed artifacts

Primary artifacts:

- `docs/AI_GOVERNANCE_MAPPING_RECORD_SCHEMA_AND_CHECKER_v0_1.md`
- `schemas/ai_governance_system_mapping_record_v0_1.schema.json`
- `tools/check_ai_governance_mapping_record_v0_1.py`
- `tests/test_ai_governance_mapping_record_v0_1.py`
- `examples/ai_governance_system_mapping/records/VALID_FORK_MAPPING_RECORD_v0_1.json`
- `examples/ai_governance_system_mapping/records/INVALID_MISSING_NON_CLAIMS_v0_1.json`
- `examples/ai_governance_system_mapping/records/INVALID_CLAIM_LEAKAGE_v0_1.json`
- `examples/ai_governance_system_mapping/records/INDETERMINATE_UNRESOLVED_DEPENDENCY_v0_1.json`
- `output/ai_governance_mapping_record_checks/*.json`

Related doctrine artifacts:

- `docs/AI_GOVERNANCE_MAPPING_SYSTEM_v0_1.md`
- `docs/AI_GOVERNANCE_BOUNDARY_MAPPING_PROTOCOL_v0_1.md`
- `docs/AI_GOVERNANCE_SYSTEM_MAPPING_RECORD_TEMPLATE_v0_1.md`
- `examples/ai_governance_system_mapping/*.md`

## Review method

This review maps each checker behavior to the governance doctrine it is supposed to preserve.

The review classifies each rule as:

- `ALIGNED`: the checker rule directly supports the doctrine.
- `PARTIALLY_ALIGNED`: the checker rule supports the doctrine but only through a limited v0.1 approximation.
- `GAP`: the doctrine implies a stronger or more precise rule than the checker currently implements.
- `NOT_CLAIMED`: the checker correctly refuses to evaluate a domain outside Fork's boundary.

## Overall alignment finding

Overall status:

```text
ALIGNED_WITH_LIMITED_V0_1_SCOPE
```

The checker is semantically aligned with Fork's v0.1 doctrine as a bounded claim-boundary checker.

It correctly enforces the minimum doctrine that a mapping record must:

- declare supported claims,
- declare explicit non-claims,
- keep supported claims and non-claims disjoint,
- preserve prohibited claim inheritance,
- surface unknowns and unresolved dependencies,
- declare an authority boundary,
- guard restricted authority/correctness/compliance claims,
- require safe handoff constraints,
- preserve Fork-specific canonical non-claims.

However, the checker is not yet a full semantic verifier. It remains a v0.1 bounded checker that relies on explicit declarations, string matching, required-field presence, and fixture-backed behavior.

## Alignment matrix

| Doctrine requirement | Checker mechanism | Alignment | Finding |
|---|---|---:|---|
| Mapping records must not allow silent claim transfer across system boundaries. | `CLAIM_NONCLAIM_DISJOINT`, `PROHIBITED_CLAIM_INHERITANCE_PRESENT`, safe handoff checks. | `PARTIALLY_ALIGNED` | The checker catches exact claim/non-claim overlap and requires prohibited inheritance declarations, but does not yet detect all paraphrased or implied claim inheritance. |
| Non-claims must be explicit and travel with downstream handoffs. | `EXPLICIT_NON_CLAIMS_PRESENT`, `SAFE_HANDOFF_CONSTRAINTS`, Fork canonical non-claim guard. | `ALIGNED` | The checker requires explicit non-claims and requires handoffs to carry non-claims. |
| Fork must not claim AI output correctness, decision correctness, source completeness, legal admissibility, compliance satisfaction, audit sufficiency, institutional authority, runtime control, execution permissioning, or policy authority. | `FORK_REQUIRED_NON_CLAIMS`. | `ALIGNED` | Fork-specific records must preserve the canonical non-claims. |
| Unresolved dependencies, unknowns, unavailable evidence, and review-required states must not collapse into PASS. | `INDETERMINATE_SIGNALS`, overall status finalization. | `ALIGNED` | The checker emits `INDETERMINATE` when unresolved or review-required statuses are present. |
| Authority boundaries must be declared separately from verification results. | `AUTHORITY_NON_AUTHORITIES_PRESENT`, `RESTRICTED_AUTHORITY_CLAIM_GUARD`. | `PARTIALLY_ALIGNED` | The checker requires a boundary and guards restricted terms, but authority logic is still enumerative and string-based. |
| Safe handoffs must carry allowed claims, non-transfer claims, non-claims, unknowns, and re-verification requirements. | `SAFE_HANDOFFS_PRESENT`, `SAFE_HANDOFF_CONSTRAINTS`. | `PARTIALLY_ALIGNED` | The checker verifies required safe-handoff arrays are present and non-empty, but does not yet validate that they reference the exact upstream IDs they should carry. |
| Verification and evaluation must remain separate. | `verification_model.does_not_evaluate`, `evaluation_boundary`, non-authority statements. | `PARTIALLY_ALIGNED` | The schema captures the distinction, but the checker mostly validates presence and top-level types rather than full semantic consistency. |
| The checker must not become a policy engine. | Explicit checker non-claims and bounded status meanings. | `ALIGNED` | The checker evaluates record boundary structure, not whether policies are correct or decisions should be approved. |
| The checker must not assert legal, compliance, audit, safety, or market conclusions. | Documentation and non-claim requirements. | `NOT_CLAIMED` | This is correctly outside scope. |
| Machine-readable records should be strictly structured. | JSON Schema file and required-field/type checks. | `PARTIALLY_ALIGNED` | The schema is strict, but the checker does not yet run full JSON Schema validation through a schema engine. |

## Important semantic distinction: declared unknowns vs unresolved unknowns

The valid Fork fixture contains an `unknowns` section because Fork doctrine requires declared unknowns to travel with the record.

That is different from a runtime unresolved unknown.

For v0.1:

- `unknowns` entries with status `DECLARED` can appear in a valid record.
- `unknowns` entries with status `UNKNOWN`, `UNRESOLVED`, `NOT_CHECKED`, `UNAVAILABLE`, or `REVIEW_REQUIRED` produce `INDETERMINATE`.

This distinction is acceptable for v0.1 but should remain explicit. Otherwise, a reviewer could incorrectly assume that the mere presence of an unknowns section must always force `INDETERMINATE`.

## Strongest alignments

### 1. Canonical Fork non-claims are enforced

The checker requires Fork records to preserve canonical non-claims covering correctness, completeness, legal admissibility, compliance, audit sufficiency, institutional authority, runtime control, execution permissioning, and policy authority.

This directly supports Fork's core doctrine: Fork preserves evidence and boundaries; it does not inherit upstream correctness or downstream authority.

### 2. INDETERMINATE is a first-class outcome

The checker does not treat unresolved dependencies as PASS.

This is semantically important because many governance failures arise when missing information is silently normalized into completion.

### 3. Safe handoff constraints are required

Every safe handoff must carry non-transfer claims, non-claims, unknowns, and re-verification requirements.

This supports the doctrine that evidence handoff must preserve boundary conditions, not just artifact content.

### 4. Verification remains distinct from evaluation

The schema and documentation preserve a separation between structural verification and human/institutional evaluation.

This protects Fork from being mistaken for a legal, compliance, audit, or policy authority.

## Current semantic gaps

### GAP_001: Full JSON Schema validation is not yet performed by the checker

The schema is strict and useful, but the checker currently performs its own built-in top-level field and type checks rather than full draft 2020-12 JSON Schema validation.

Risk:

A record may satisfy the checker while violating nested schema constraints.

v0.2 recommendation:

Add optional or required JSON Schema validation using a pinned dependency or a dependency-free validation strategy explicitly documented in the repo.

### GAP_002: Claim inheritance detection is still mostly literal

The checker detects exact supported-claim/non-claim overlap and restricted authority terms. It does not yet detect paraphrased claim inheritance, synonym drift, or implied authority claims.

Risk:

A record could avoid exact restricted terms while still implying prohibited authority.

v0.2 recommendation:

Add adversarial fixtures for paraphrased inheritance, including phrases such as:

- "validated the decision"
- "approved the outcome"
- "sufficient for compliance"
- "ready for legal reliance"
- "complete source record"
- "institutionally accepted"

### GAP_003: Safe handoff fields are not yet ID-referential

Safe handoff arrays are required, but the checker does not yet verify that values correspond to specific IDs in `supported_claims`, `explicit_non_claims`, `unknowns`, or `re_verification_requirements`.

Risk:

A handoff may contain generic text while failing to carry the precise upstream boundary items.

v0.2 recommendation:

Add ID-based traceability across handoff fields.

### GAP_004: Authority basis is not deeply evaluated

The checker can detect unsupported restricted terms, but it does not determine whether an asserted authority basis is substantively valid.

Risk:

A record could declare an authority basis that is facially present but institutionally weak or unsupported.

v0.2 recommendation:

Keep this as a non-claim unless external authority evidence is separately modeled and verified.

### GAP_005: Valid fixture uses declared unknowns carefully, but this distinction needs documentation

The v0.1 model permits declared classes of unknowns in a PASS record while using unresolved statuses to trigger INDETERMINATE.

Risk:

Reviewers may confuse "unknowns are declared" with "the record contains unresolved unknown facts."

v0.2 recommendation:

Rename or further distinguish:

- `declared_unknown_classes`
- `active_unresolved_unknowns`

or require status-level explanatory language.

## Non-claims of this review

This review does not claim:

- the checker proves legal admissibility,
- the checker proves compliance satisfaction,
- the checker proves audit sufficiency,
- the checker proves AI output correctness,
- the checker proves decision correctness,
- the checker proves source completeness,
- the checker proves institutional acceptance,
- the checker proves market need,
- the checker is production-complete,
- the checker performs full semantic natural-language understanding.

## v0.2 recommended additions

The next semantic hardening layer should add:

1. Full schema validation or an explicit equivalent.
2. ID-reference integrity across safe handoff fields.
3. A canonical restricted-claim registry.
4. Paraphrased claim inheritance adversarial fixtures.
5. Distinction between declared unknown classes and active unresolved unknowns.
6. Normalized result mode for cross-environment reproducibility.
7. Additional fixtures for:
   - missing safe-handoff non-claim propagation,
   - overbroad authority basis,
   - hidden compliance claim,
   - hidden legal admissibility claim,
   - source completeness leakage,
   - runtime-control leakage,
   - policy-authority leakage.
8. A machine-readable semantic alignment receipt.

## Review conclusion

The v0.1 checker is semantically aligned with Fork's doctrine as a bounded, declaration-based claim-boundary checker.

It should be described as:

```text
A v0.1 machine-checkable boundary record validator that verifies declared claim boundaries, non-claims, authority boundaries, safe handoff constraints, and indeterminate states.
```

It should not yet be described as:

```text
A full semantic verifier, legal sufficiency checker, compliance checker, audit checker, policy engine, or production governance authority.
```

Final review status:

```text
CHECKER_DOCTRINE_ALIGNMENT_REVIEW_v0_1_ALIGNED_WITH_LIMITED_SCOPE
```