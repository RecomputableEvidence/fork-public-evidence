# FORK-RELATIONAL-RESOLUTION-DEMONSTRATION-001

## AG5 — RECOMPUTATION ADMISSION

Status: `AG5_COMPLETE`

Current AG5 parent-chain root: AG4 commit `9a28abf10539175e19a5eaa58e049ab7a46d4f50`

Authorization received: `AUTHORIZED_ADMISSION_VERIFIED`

AG5 admits the verified local recomputation return for `CAPTURE_001` without expanding AG4 standing.

## 1. Attempt sequence preserved

`AG5_LOCAL_RECOMPUTATION_ATTEMPT_001` is preserved as `PROCEDURAL_FAILURE_BEFORE_EDGE_RECOMPUTATION`. Its full-worktree method failed on Windows pathname-length constraints before the packet could be materialized. That failure is procedural evidence only and is not an AG4 status mismatch.

`AG5_LOCAL_RECOMPUTATION_ATTEMPT_002` is admitted as the successful repaired recomputation path.

```text
ATTEMPT_001_PROCEDURAL_FAILURE
!= AG4_STATUS_MISMATCH

ATTEMPT_002_COMPLETE_MATCH
!= GLOBAL_VERIFICATION
```

## 2. Verified return identities

The received source objects were independently hashed before admission:

- Attempt 001 source transcript raw bytes:
  - SHA-256 `bbe430a05d65697f90c9ca14b7b458cc8923bd4ada1b26a2f087331d965abd0f`
  - preserved recoverably as deterministic gzip bytes `AG5_LOCAL_RECOMPUTATION_ATTEMPT_001_SOURCE_TRANSCRIPT.txt.gz`
  - gzip SHA-256 `89887793e8d456bc20da4e705a1c586be26ec666726953588c7d359c400771c6`
- Attempt 002 console raw bytes:
  - SHA-256 `cf02c937ac80e0c2bcc4669ce47879179f0cfcbf45c1cac87235c659422d9eec`
  - preserved recoverably as deterministic gzip bytes `AG5_LOCAL_RECOMPUTATION_CONSOLE_ATTEMPT_002.txt.gz`
  - gzip SHA-256 `58f9b7dca217a2ad6e44c39e5b398f2ff9661431269b55c15836fbbb4e1fa5aa`
- Attempt 002 receipt bytes:
  - SHA-256 `884fcfacc980e91127ed8e67eba99eb84fc78043ce1c32bbd70cdcae9f96cfcc`
  - embedded directly as `AG5_LOCAL_RECOMPUTATION_RECEIPT_ATTEMPT_002.json`
- Attempt 002 implementation source raw bytes:
  - SHA-256 `a8d395a5dafc87230469bf956eed89d38dddf5202a48ac23fd231a8c209468ad`
  - preserved recoverably as deterministic gzip bytes `recompute_ag4_v0_2.py.gz`
  - gzip SHA-256 `cc3ebe8e49a230a093c1151f1d43c5cbaf097dbd9c4ce7a72995de914f7f773c`

For the gzip-preserved objects:

```text
RAW_SOURCE_BYTES
!= STORED_GZIP_BYTES

DECOMPRESS(STORED_GZIP_BYTES)
= ADMITTED_RAW_SOURCE_BYTES
```

## 3. Recomputed coordinate and packet identity

Attempt 002 independently reproduced:

- AG4 commit `9a28abf10539175e19a5eaa58e049ab7a46d4f50`;
- AG3 parent `874947205b9cd1dac5f3268d9d6f25e1a97be7c1`;
- exact Git-blob identities for the selectively materialized AG0–AG4 packet inputs/results;
- exact target artifact identity;
- all nine AG4 edge statuses; and
- the AG4 summary distribution.

The admitted result distribution remains:

```text
SUPPORTED                3
CONTRADICTED              0
UNRESOLVED                 0
INSUFFICIENT_EVIDENCE      6
NOT_EVALUATED              0
OUT_OF_SCOPE               0
```

The nine recomputed statuses matched the nine recorded AG4 statuses exactly.

## 4. Standing admitted by AG5

Admitted:

- Attempt 001 as preserved negative procedural evidence;
- Attempt 002 console, receipt, and implementation identities;
- recoverable preservation of the exact Attempt 001 transcript, Attempt 002 console, and Attempt 002 implementation source;
- repository-coordinate recomputation match;
- selectively materialized packet-byte identity match to Git;
- target artifact identity recomputation match;
- 9/9 edge-status reproduction;
- summary-count reproduction; and
- `OVERALL MATCH = True` for the bounded Attempt 002 recomputation.

Not admitted:

- any new source observation;
- any change to the nine AG4 edge statuses;
- any global `VERIFIED` result;
- artifact safety or correctness;
- attestation validity;
- issuer authority;
- deployment authorization;
- runtime permission;
- new provenance standing;
- a derived view;
- a selected view; or
- any external action.

```text
AG4_RESULT_REPRODUCED_LOCALLY
!= AG4_RESULT_STRENGTHENED

RECOMPUTATION_MATCH
!= GLOBAL_VERIFICATION

AG5_COMPLETE
!= AG6_AUTHORIZED
```

## 5. Next gate

`AG6 — DERIVATION_ADMISSION` remains `UNOPENED`.
