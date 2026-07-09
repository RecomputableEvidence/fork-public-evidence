# Boundary Pressure Review / Retrieval Distortion Test Case v0.1

Status: Experimental review case.
Normative force: Maintainer guidance and reviewer test fixture, not external certification.
Scope: Boundary Pressure Review, retrieval distortion, failed access, partial access, exterior observation, and recomputation interpretation.
Access classification: Public repository review artifact.
Related posture: `docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md`.

## Non-endorsement and non-claims capsule

This artifact does not endorse Fork, certify Fork, validate production readiness, establish legal sufficiency, establish compliance, approve deployment, or convert any exterior observation into endorsement.

This artifact tests a review failure mode: a reviewer, model, downstream reader, or external observer may treat failed retrieval, partial retrieval, inferred access, or surrounding commentary as if it were direct inspection, recomputation, structural verification, approval, or validation.

## Purpose

Boundary Pressure Review evaluates whether Fork artifacts preserve declared claim, authority, evidence, non-claim, sufficiency, and truth boundaries under adverse interpretation.

This test case focuses on retrieval distortion.

Retrieval distortion occurs when a review channel silently changes what the reviewer thinks was accessed, observed, executed, or recomputed.

The important failure is not that retrieval failed. Failed retrieval is an ordinary access condition. The failure occurs when failed or partial retrieval is upgraded into a content review, structural reproduction, endorsement, validation, approval, compliance conclusion, legal conclusion, or evidence sufficiency conclusion.

## Test question

Can a Fork review artifact preserve the difference between:

1. raw artifact access;
2. partial access;
3. failed retrieval;
4. inferred commentary;
5. structural reproduction;
6. unresolved state;
7. evidentiary sufficiency;
8. authority;
9. approval;
10. endorsement?

A passing artifact keeps those states separate.

## Review standard exercised

A Fork artifact should not allow any of the following collapses:

- failed retrieval becomes review;
- partial access becomes complete access;
- commentary becomes execution;
- observation becomes endorsement;
- recomputation becomes validation;
- structural pass becomes truth;
- artifact inclusion becomes sufficiency;
- authority context becomes authority transfer;
- external receipt becomes certification.

## Fixture model

The fixtures use a small JSON case format.

Each fixture declares:

- `case_id`;
- `expected_result`;
- `source_access`;
- `claims`;
- `non_claims`;
- `boundary_pressure`;
- `interpretation`.

The checker validates whether the expected result aligns with the declared conditions.

## Valid fixture

The valid fixture records partial access and preserves it as an access limitation.

It does not claim structural reproduction, content review, approval, compliance, legal sufficiency, or truth.

Expected result:

`STRUCTURAL_PASS`

## Invalid fixture

The invalid fixture records no raw access but claims review completion and structural reproduction.

That is the retrieval distortion failure.

Expected result:

`STRUCTURAL_FAIL`

## Checker

Run from repo root:

```powershell
python .\tools\check_boundary_pressure_review_cases_v0_1.py
```

Expected output:

- valid fixture passes;
- invalid fixture fails for the expected reason;
- checker exits 0 when all fixture expectations are matched.

## Interpretation of checker pass

A checker pass means only that the included retrieval-distortion fixtures behaved as expected under the structural rules in the checker.
It does not establish truth, legal sufficiency, compliance, approval, endorsement, production readiness, audit sufficiency, or general completeness of the Boundary Pressure Review method.

## Future expansion

Future versions may add fixtures for:

- semantic paraphrase bypass;
- non-claim suppression;
- hostile endorsement injection;
- observation-volume-as-consensus;
- packet-inclusion-as-sufficiency;
- policy-reference-as-compliance;
- authority-context-as-transfer;
- commercial-language-overclaim;
- recomputation-receipt-overread.