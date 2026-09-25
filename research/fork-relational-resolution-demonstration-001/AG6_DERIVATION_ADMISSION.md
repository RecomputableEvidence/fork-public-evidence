# FORK-RELATIONAL-RESOLUTION-DEMONSTRATION-001

## AG6 — DERIVATION ADMISSION

Status: `AG6_COMPLETE`

Parent authorized coordinate: `fc29b11dbe2a339f0ef81507e387d4c2f7877c41`

Derivation ruleset: `FORK-RRD-001-AG6-DERIVE-v0.1`

AG7 view selection: `UNOPENED`

This gate admits bounded derivations over the already admitted `CAPTURE_001` and `CAPTURE_002` records. It performs no new external observation, does not re-evaluate any edge, does not strengthen any edge standing, and does not select a preferred demonstration view.

## Lens shift

The surface reading is that the two captures produced the same per-edge result classes.

The deeper object is different: AG6 asks what may be derived from **two coordinate-bound graph states** without converting recurrence into persistence.

```text
REPEATED_RESULT_CLASS
!= CONTINUOUS_RELATION_PERSISTENCE

DERIVATION
!= INHERITANCE
```

The derivation layer therefore operates on the relation between `G0` and `G1`, not by collapsing them into one timeless graph.

## Admitted inputs

AG6 is bounded to the already admitted objects:

- `AG0_QUESTION_FREEZE.md`;
- `CAPTURE_001_AG2_SOURCE_OBSERVATION_SET.json`;
- `CAPTURE_001_AG4_DIMENSIONAL_EVALUATION.json`;
- `AG5_RECOMPUTATION_ADMISSION.md`;
- `CAPTURE_002_SOURCE_OBSERVATION_SET.json`;
- `CAPTURE_002_DIMENSIONAL_EVALUATION.json`; and
- `CAPTURE_002_RECOMPUTATION_ADMISSION.json`.

No new source query is introduced by AG6.

## Derivation rules

The admitted derivation rules prohibit temporal interpolation, retroactive import of CAPTURE_002-only surfaces, promotion of repeated missingness into external absence, strengthening of lower-layer edge standing, view selection, and external action.

CAPTURE_002's artifact identity remains a carried-forward reference to the identity admitted at CAPTURE_001; it is not represented as a second byte acquisition or rehash.

```text
IDENTITY_REFERENCE_CARRIED_FORWARD
!= ARTIFACT_BYTES_REACQUIRED_AT_CAPTURE_002
```

## Derived representation

### AG6-D01 — Artifact identity reference across captures

CAPTURE_002 carries the same identity tuple admitted for CAPTURE_001:

```text
google-workspace-cli-x86_64-pc-windows-msvc.zip
6275652 bytes
sha256:5e33f26556df86411959e0f07cd51caa87b4eaa413b14a385c9efd828b5b1739
```

This is identity-reference continuity in the record, not a second byte-level acquisition event.

### AG6-D02 — Primary source-field projection delta

Across the ten source surfaces made comparable by the CAPTURE_001-preserved projection:

```text
COMPARABLE_SURFACES       10
MATCHED                   10
CHANGED                    0
```

```text
SOURCE_FIELD_PROJECTION_STABILITY
!= EXTERNAL_WORLD_STATE_IDENTITY
```

### AG6-D03 — Edge result-class delta

The same nine edge classes were evaluated under `FORK-RRD-001-AG4-EVAL-v0.1` at both coordinates.

Both coordinates produced:

```text
SUPPORTED                3
CONTRADICTED             0
UNRESOLVED               0
INSUFFICIENT_EVIDENCE    6
NOT_EVALUATED            0
OUT_OF_SCOPE             0
```

Homologous edge-class status changes:

```text
0
```

This is a two-coordinate equality result, not an interval claim.

### AG6-D04 — Repeated capture missingness

Both records preserve the same material missingness conditions relevant to several edges:

- checksum assertion content was not captured; and
- no attestation bundle or decoded predicate was captured.

The recurrence of those capture limitations explains repeated `INSUFFICIENT_EVIDENCE` results for the affected edges, but does not establish that the external checksum assertion or attestation is absent.

```text
REPEATED_MISSINGNESS_IN_CAPTURE_RECORD
!= EXTERNAL_ABSENCE
```

### AG6-D05 — Supplemental surface addition

CAPTURE_002 contains one separately labeled surface not preserved at CAPTURE_001: the repository `latest` endpoint reported `v0.22.5`.

It remains excluded from the primary CAPTURE_001-to-CAPTURE_002 field-projection comparison.

```text
NEW_C2_SURFACE
!= RETROACTIVE_C1_OBSERVATION
```

### AG6-D06 — Record-graph resolution delta

After CAPTURE_002, the record has greater temporal resolution because it contains:

- a second bounded observation coordinate;
- a second evaluation under the same edge grammar and ruleset; and
- one additional separately labeled supplemental surface.

That increase is representational, not authoritative.

```text
INCREASED_RECORD_RESOLUTION
!= INCREASED_EDGE_AUTHORITY
```

### AG6-D07 — Graph nonidentity without rewrite

`G1` is not identical to `G0` as a record graph because it is bound to a different capture coordinate and contains the CAPTURE_002-only supplemental surface.

At the same time, the primary comparable projections and homologous result classes remained stable.

```text
G1_DIFFERS_FROM_G0_AS_RECORD_GRAPH

AND

G1_DOES_NOT_REWRITE_G0
```

### AG6-D08 — Continuous-persistence bridge

`NOT_DERIVABLE_FROM_ADMITTED_INPUTS`.

No admitted object bridges the interval between CAPTURE_001 and CAPTURE_002 strongly enough to establish that any external relation persisted continuously throughout it.

```text
TWO_SUPPORTED_COORDINATES
!= INTERVAL_CONTINUITY
```

### AG6-D09 — Supersession bridge

`NOT_DERIVABLE_FROM_ADMITTED_INPUTS`.

The later `v0.22.5` release observation does not establish either supersession or non-supersession of the bounded relations around `v0.22.1`.

```text
LATER_RELEASE_EXISTS
!= PRIOR_RELATION_SUPERSEDED
```

### AG6-D10 — Edge-standing strength delta

No homologous edge acquired a different result class between the two admitted coordinates. Therefore the derivation layer adds comparative and temporal resolution while adding **no edge-standing strengthening**.

```text
EDGE_CLASS_STATUS_CHANGES   0
EDGE_CLASSES_STRENGTHENED   0

DERIVATION_ADMITTED
!= EDGE_STANDING_STRENGTHENED
```

## What AG6 establishes

The demonstration now has an admitted derivation layer capable of representing:

- identity-reference continuity;
- source-field projection stability;
- edge-result-class stability;
- repeated capture missingness;
- a CAPTURE_002-only supplemental surface;
- increased temporal record resolution;
- graph nonidentity without historical rewrite; and
- explicit non-derivability of interval-continuity and supersession bridges.

The central bounded result is therefore:

```text
MORE_TEMPORAL_AND_COMPARATIVE_RESOLUTION
WITHOUT
MORE_EDGE_AUTHORITY
```

That is stronger as a representation claim than merely saying that the two result tables matched, but it does not strengthen any underlying relation claim.

## Not admitted

AG6 does not admit:

- a preferred or selected demonstration view;
- continuous relation persistence;
- byte reacquisition at CAPTURE_002;
- global verification;
- artifact safety or correctness;
- attestation validity;
- issuer authority;
- supersession or non-supersession beyond the bounded evaluations;
- deployment or runtime authority;
- external action; or
- AG7 authorization.

```text
DERIVATION_ADMISSION
!= VIEW_SELECTION

AUTHORIZED_DERIVATION
!= AUTHORIZED_ACTION

AG6_COMPLETE
!= AG7_AUTHORIZED
```

## Next gate

`AG7 — DEMONSTRATION_VIEW_SELECTION` remains `UNOPENED`.
