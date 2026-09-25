# FORK-RELATIONAL-RESOLUTION-DEMONSTRATION-001

## CAPTURE_002 — RELATION EDGE INSTANTIATION

Status: `CAPTURE_002_RELATION_EDGE_SET_INSTANTIATED_UNEVALUATED`

Parent source-observation commit: `d5cd35cdd0c3ca39c7a103701735e60e5eeeafa0`

This step instantiates the same nine relation-edge classes frozen at AG0 and first instantiated for `CAPTURE_001`, now against the `CAPTURE_002` observation coordinate.

No substantive relation result is assigned here.

```text
EDGE_OBJECT_EXISTS
!= EDGE_STANDING_EXISTS

CAPTURE_002_EDGE_OBJECT
!= CAPTURE_001_EDGE_OBJECT

SAME_EDGE_CLASS
!= SAME_EDGE_STANDING
```

## Instantiated edge set

1. `C2-E01` — `ARTIFACT_TO_RELEASE_OBJECT`
2. `C2-E02` — `ARTIFACT_TO_PUBLISHED_DIGEST`
3. `C2-E03` — `ARTIFACT_TO_ATTESTATION_SUBJECT`
4. `C2-E04` — `ATTESTATION_TO_SOURCE_REPOSITORY`
5. `C2-E05` — `ATTESTATION_TO_SOURCE_COMMIT`
6. `C2-E06` — `SOURCE_COMMIT_TO_WORKFLOW_REFERENCE`
7. `C2-E07` — `CLAIMED_ISSUER_TO_ISSUER_AUTHORITY`
8. `C2-E08` — `RELATION_TO_TEMPORAL_APPLICABILITY`
9. `C2-E09` — `RELATION_TO_SUPERSESSION_STATE`

Each object carries a pointer to its corresponding `CAPTURE_001` predeclared edge (`AG3-E01` through `AG3-E09`) and binds only candidate evidence already admitted in `CAPTURE_002_SOURCE_OBSERVATION_SET.json` plus the carried-forward artifact identity.

## Missingness preserved

The checksum assertion content remains uncaptured, so `C2-E02` retains a candidate target object without a proposition-level checksum assertion body.

The attestation bundle remains uncaptured, so `C2-E03`, `C2-E04`, `C2-E05`, and `C2-E07` retain unbound attestation/issuer endpoints rather than inferred bindings.

```text
UNBOUND_ENDPOINT
!= NEGATIVE_EDGE_RESULT

MISSING_SOURCE_SURFACE
!= EDGE_CONTRADICTED
```

## Supersession edge

`C2-E09` may reference the separately preserved supplemental observation that a later release exists, but that observation remains non-comparable to `CAPTURE_001`'s primary source projection and does not establish supersession by itself.

```text
LATER_RELEASE_EXISTS
!= PRIOR_RELATION_SUPERSEDED
```

## Evaluation state

For all nine edges:

```text
evaluation_state = NOT_EVALUATED
result_status = null
standing = UNASSIGNED
evaluation_gate = CAPTURE_002_DIMENSIONAL_EVALUATION
```

This lifecycle state is not a substantive edge result.

No `SUPPORTED`, `CONTRADICTED`, `UNRESOLVED`, `INSUFFICIENT_EVIDENCE`, or `OUT_OF_SCOPE` result has been assigned to any CAPTURE_002 edge.

## Boundaries

```text
FIELD_EQUALITY
!= STANDING_EQUALITY

CANDIDATE_EVIDENCE_BOUND
!= EVIDENCE_SUFFICIENT

CAPTURE_002_EDGE_SET_INSTANTIATED
!= CAPTURE_002_EVALUATION_AUTHORIZED

CAPTURE_002_EDGE_SET_INSTANTIATED
!= AG6_AUTHORIZED

G1
DOES_NOT_REWRITE
G0
```

## Next transition

`CAPTURE_002_DIMENSIONAL_EVALUATION` remains `UNOPENED`.

`AG6 — DERIVATION_ADMISSION` remains `UNOPENED`.
