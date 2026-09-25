# FORK-RELATIONAL-RESOLUTION-DEMONSTRATION-001

## AG3 — RELATION-EDGE INSTANTIATION

Status: `AG3_COMPLETE_UNEVALUATED`

Capture: `CAPTURE_001_RELATION_EDGE_SET_INSTANTIATED`

Parent AG2 commit: `ec44b448679c71cfd2b00fc58d3e90445b4ffd16`

AG3 was explicitly authorized after AG2 completed. This gate instantiates the nine relation-edge classes frozen at AG0 against the artifact and source-observation objects admitted through AG2.

AG3 does **not** determine whether any edge is supported, contradicted, unresolved, insufficiently evidenced, or out of scope. That remains AG4.

```text
EDGE_OBJECT_EXISTS
!= EDGE_STANDING_EXISTS
```

---

## 1. Instantiated edge set

The following edge objects now exist for `CAPTURE_001`:

1. `AG3-E01 — ARTIFACT_TO_RELEASE_OBJECT`
2. `AG3-E02 — ARTIFACT_TO_PUBLISHED_DIGEST`
3. `AG3-E03 — ARTIFACT_TO_ATTESTATION_SUBJECT`
4. `AG3-E04 — ATTESTATION_TO_SOURCE_REPOSITORY`
5. `AG3-E05 — ATTESTATION_TO_SOURCE_COMMIT`
6. `AG3-E06 — SOURCE_COMMIT_TO_WORKFLOW_REFERENCE`
7. `AG3-E07 — CLAIMED_ISSUER_TO_ISSUER_AUTHORITY`
8. `AG3-E08 — RELATION_TO_TEMPORAL_APPLICABILITY`
9. `AG3-E09 — RELATION_TO_SUPERSESSION_STATE`

The machine-readable definitions are preserved in `CAPTURE_001_AG3_RELATION_EDGE_OBJECTS.json`.

---

## 2. Endpoint binding

Where AG1/AG2 supplied bound objects, AG3 points to those objects directly. Examples include:

- the exact captured artifact bound by SHA-256;
- GitHub release object `301345178` / tag `v0.22.1`;
- source commit `45ca45bfd418db07b02995e8510dd18ac45cb3a6`; and
- `.github/workflows/release.yml` at the observed source coordinate.

Where AG2 preserved explicit missingness, AG3 preserves an unbound endpoint rather than manufacturing one. This applies especially to:

- the attestation object;
- the attestation subject;
- a claimed issuer derived from a captured attestation; and
- an issuer-authority relation.

```text
EDGE_CLASS_PREDECLARED
!= ENDPOINT_EVIDENCE_AVAILABLE

UNBOUND_ENDPOINT
!= NEGATIVE_EDGE_RESULT
```

---

## 3. Candidate evidence binding

Each edge object lists the AG1/AG2 observations that may be relevant when AG4 evaluates that edge.

This is only candidate-evidence routing.

```text
CANDIDATE_EVIDENCE_BOUND
!= EVIDENCE_SUFFICIENT

OBSERVATION_REFERENCED_BY_EDGE
!= OBSERVATION_SUPPORTS_EDGE
```

No result vocabulary has been applied to any edge at AG3.

---

## 4. Missing surfaces remain first-class

AG2 did not capture the content of the 115-byte checksum assertion file and did not capture an attestation bundle or decoded predicate.

AG3 therefore keeps those absences attached to the affected edges rather than deleting the edges or treating them as contradicted.

```text
MISSING_SOURCE_SURFACE
!= EDGE_CONTRADICTED

MISSING_EVIDENCE
!= EVIDENCE_OF_ABSENCE
```

The absence of a captured attestation bundle currently affects `AG3-E03`, `AG3-E04`, `AG3-E05`, and `AG3-E07`. The absent checksum-file content currently affects `AG3-E02`.

These statements are routing/missingness observations only, not AG4 dispositions.

---

## 5. Higher-order temporal edges

`AG3-E08` and `AG3-E09` are intentionally higher-order relation objects.

`AG3-E08` asks whether any standing eventually assigned to the lower-order relations is bound to a specific temporal coordinate or applicability interval.

`AG3-E09` asks whether the bounded record establishes any supersession relation affecting those relations at the capture coordinate.

Neither permits a later state to rewrite an earlier state.

```text
LATER_STATE
!= EARLIER_STATE

SUPERSESSION_IF_ESTABLISHED
!= HISTORICAL_ERASURE
```

---

## 6. AG3 disposition

Admitted:

- nine relation-edge objects for `CAPTURE_001`;
- explicit source and target object references where available;
- explicit unbound endpoints where AG2 evidence is absent;
- candidate-evidence routing from AG1/AG2 into each edge object; and
- the requirement that every edge remain unevaluated until AG4.

Not admitted:

- any edge as `SUPPORTED`;
- any edge as `CONTRADICTED`;
- any edge as `UNRESOLVED`;
- any edge as `INSUFFICIENT_EVIDENCE`;
- any relation authority;
- checksum assertion validity;
- attestation validity;
- provenance standing;
- temporal applicability standing;
- supersession standing;
- a derived view;
- a selected view; or
- any downstream action.

AG4 remains `UNOPENED`.

```text
EDGE_PREDECLARED
!= EDGE_SUPPORTED

EDGE_OBJECT_INSTANTIATED
!= EDGE_STANDING_ASSIGNED

AG3_COMPLETE
!= AG4_AUTHORIZED
```
