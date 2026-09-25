# FORK-RELATIONAL-RESOLUTION-DEMONSTRATION-001

## CAPTURE_002 — DIMENSIONAL EVALUATION

Status: `CAPTURE_002_DIMENSIONAL_EVALUATION_COMPLETE`

Ruleset: `FORK-RRD-001-AG4-EVAL-v0.1`

Ruleset change for CAPTURE_002: `NONE`

Parent edge-instantiation commit: `db872e663ed3a34442aa6c55376c58dea35ac6fb`

This step evaluates the nine CAPTURE_002 relation-edge objects under the same status vocabulary, status semantics, and global rules used for CAPTURE_001. No new external observation was introduced during evaluation.

```text
SAME_RULESET
!= SAME_COORDINATE

SAME_EDGE_CLASS
!= SAME_EDGE_OBJECT

SOURCE_OBSERVED
!= RELATION_ESTABLISHED
```

## Result set

| Edge | Relation | CAPTURE_002 result |
|---|---|---|
| `C2-E01` | `ARTIFACT_TO_RELEASE_OBJECT` | `SUPPORTED` |
| `C2-E02` | `ARTIFACT_TO_PUBLISHED_DIGEST` | `INSUFFICIENT_EVIDENCE` |
| `C2-E03` | `ARTIFACT_TO_ATTESTATION_SUBJECT` | `INSUFFICIENT_EVIDENCE` |
| `C2-E04` | `ATTESTATION_TO_SOURCE_REPOSITORY` | `INSUFFICIENT_EVIDENCE` |
| `C2-E05` | `ATTESTATION_TO_SOURCE_COMMIT` | `INSUFFICIENT_EVIDENCE` |
| `C2-E06` | `SOURCE_COMMIT_TO_WORKFLOW_REFERENCE` | `SUPPORTED` |
| `C2-E07` | `CLAIMED_ISSUER_TO_ISSUER_AUTHORITY` | `INSUFFICIENT_EVIDENCE` |
| `C2-E08` | `RELATION_TO_TEMPORAL_APPLICABILITY` | `SUPPORTED` |
| `C2-E09` | `RELATION_TO_SUPERSESSION_STATE` | `INSUFFICIENT_EVIDENCE` |

Distribution:

```text
SUPPORTED                3
CONTRADICTED              0
UNRESOLVED                 0
INSUFFICIENT_EVIDENCE      6
NOT_EVALUATED              0
OUT_OF_SCOPE               0
```

## Edge-specific boundaries

`C2-E01` is supported only for the bounded association between the already admitted artifact identity and the freshly observed `v0.22.1` release object/asset metadata at CAPTURE_002. The artifact was not reacquired or rehashed during this capture.

`C2-E02` remains insufficient because the 115-byte checksum assertion content remains uncaptured. The checksum-file object's own GitHub-reported digest is not substituted for the assertion contained in that file.

`C2-E03`, `C2-E04`, `C2-E05`, and `C2-E07` remain insufficient because no attestation bundle or decoded predicate was captured and no independent issuer-authority instrument was admitted.

`C2-E06` is supported only for the named workflow reference at source commit `45ca45bfd418db07b02995e8510dd18ac45cb3a6`. It does not establish that the workflow produced the exact public ZIP.

`C2-E08` is supported only for CAPTURE_002 record-coordinate applicability. It does not establish persistence across the interval between CAPTURE_001 and CAPTURE_002.

`C2-E09` remains insufficient even though CAPTURE_002 separately observed a later repository release. The existence of `v0.22.5` does not itself establish supersession of any relation around the historical `v0.22.1` artifact.

```text
LATER_RELEASE_EXISTS
!= PRIOR_RELATION_SUPERSEDED
```

## Cross-capture result

CAPTURE_001 and CAPTURE_002 have the same per-edge result classes under the same ruleset:

```text
CAPTURE_001: 3 SUPPORTED / 6 INSUFFICIENT_EVIDENCE
CAPTURE_002: 3 SUPPORTED / 6 INSUFFICIENT_EVIDENCE
EDGE_CLASS_STATUS_CHANGES: 0
```

That observation is itself bounded:

```text
SAME_STATUS
!= SAME_EVIDENCE_COORDINATE

SAME_STATUS
!= CONTINUOUS_RELATION_PERSISTENCE

SAME_STATUS
!= NON_SUPERSESSION_ESTABLISHED

CAPTURE_002
DOES_NOT_REWRITE
CAPTURE_001
```

The longitudinal demonstration has therefore produced two temporally distinct evaluations over an identity-stable artifact with the same edge grammar and same evaluation ruleset. The observed result classes are stable across the two captured coordinates, but no bridge is inferred across the unobserved interval.

## Standing

Admitted here:

- nine CAPTURE_002 edge evaluations;
- three bounded `SUPPORTED` results;
- six bounded `INSUFFICIENT_EVIDENCE` results;
- unchanged reuse of `FORK-RRD-001-AG4-EVAL-v0.1`;
- CAPTURE_002 coordinate binding;
- observed equality of the corresponding CAPTURE_001/CAPTURE_002 result classes.

Not admitted here:

- continuous relation persistence;
- global verification;
- artifact safety or correctness;
- attestation validity;
- issuer authority;
- deployment or runtime authority;
- supersession or non-supersession beyond the admitted evidence;
- a derived longitudinal representation;
- view selection; or
- external action.

```text
CAPTURE_002_DIMENSIONAL_EVALUATION_COMPLETE
!= CAPTURE_002_RECOMPUTATION_ADMITTED

CAPTURE_002_DIMENSIONAL_EVALUATION_COMPLETE
!= AG6_AUTHORIZED
```

## Next transition

`CAPTURE_002_RECOMPUTATION` remains `UNOPENED`.

`AG6 — DERIVATION_ADMISSION` remains `UNOPENED`.
