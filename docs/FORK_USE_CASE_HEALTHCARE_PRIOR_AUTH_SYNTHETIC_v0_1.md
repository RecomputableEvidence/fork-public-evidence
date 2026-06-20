# Fork Use Case: Healthcare Prior Authorization Synthetic v0.1

## Purpose

This use case stages Fork for a synthetic healthcare administrative workflow involving prior authorization denial review and internal appeal packet assembly.

The core boundary is:

> A clinical or policy summary is not medical necessity, clinical correctness, coverage determination, legal sufficiency, or patient safety.

## Synthetic-data notice

This use case is synthetic. It is intended for structural boundary demonstration only. It should not be interpreted as patient data, payer behavior, provider behavior, medical guidance, or legal guidance.

## Scope and non-scope

Scope: Fork records and checks the structural boundary of this use case, including supported claims, non-claims, evidence references, downstream consumption, unresolved pointers, and added downstream claims.

Non-scope: Fork does not evaluate substantive correctness, safety, compliance, legal sufficiency, approval, risk acceptance, control effectiveness, clinical appropriateness, production readiness, model safety, patient safety, vendor security, or incident closure.

## Scenario

An AI-assisted workflow summarizes a prior authorization denial, extracts synthetic policy language, references synthetic clinical notes, and helps assemble an internal appeal packet for human review.

## Supported claim

The record can support that an AI-assisted summary was generated from identified synthetic source documents, that certain synthetic policy and clinical references were cited, and that a human reviewer consumed the packet.

## Non-claims

Fork does not claim:

- `does_not_claim_medical_necessity`
- `does_not_claim_clinical_correctness`
- `does_not_claim_coverage_determination`
- `does_not_claim_legal_sufficiency`
- `does_not_claim_patient_safety`
- `does_not_claim_approval`

## Boundary-preserved consumption

A reviewer consumes the AI-assisted packet as a summary of referenced materials, not as a medical, legal, or coverage determination.

Example:

> The reviewer relied on the packet to locate cited synthetic materials and unresolved questions, not to conclude medical necessity.

Boundary result:

`BOUNDARY_PRESERVED`

## Boundary-expanding consumption

A downstream actor treats packet verification as substantive clinical or coverage correctness.

Example:

> The AI packet verified, so the denial was medically correct.

Boundary result:

`BOUNDARY_EXPANSION_DETECTED`

## Buyer-facing boundary sentence

Fork can preserve the distinction between an appeal packet being assembled and reviewed and the separate question of whether the decision was clinically, legally, or medically correct.

## Fork role

Fork may support administrative evidence-boundary review for synthetic healthcare workflows. It does not determine medical necessity, clinical correctness, coverage, legal sufficiency, patient safety, or approval.

## Example record

See:

- `examples/fork_use_cases/valid_healthcare_prior_auth_synthetic_v0_1.json`