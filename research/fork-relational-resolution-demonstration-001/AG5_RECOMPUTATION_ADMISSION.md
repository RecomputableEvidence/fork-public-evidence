# FORK-RELATIONAL-RESOLUTION-DEMONSTRATION-001

## AG5 — RECOMPUTATION ADMISSION

Status: `AG5_COMPLETE`

Parent AG4 commit: `9a28abf10539175e19a5eaa58e049ab7a46d4f50`

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

## 2. Verified return identity

The exact uploaded Attempt 002 return objects were independently hashed before admission:

- `AG5_LOCAL_RECOMPUTATION_CONSOLE_ATTEMPT_002.txt`
  - SHA-256 `cf02c937ac80e0c2bcc4669ce47879179f0cfcbf45c1cac87235c659422d9eec`
- `AG5_LOCAL_RECOMPUTATION_RECEIPT_ATTEMPT_002.json`
  - SHA-256 `884fcfacc980e91127ed8e67eba99eb84fc78043ce1c32bbd70cdcae9f96cfcc`
- `recompute_ag4_v0_2.py`
  - SHA-256 `a8d395a5dafc87230469bf956eed89d38dddf5202a48ac23fd231a8c209468ad`

The console and receipt bytes are embedded in this AG5 repository record. The implementation source was independently received and hash-verified before admission; its exact source-byte identity is admitted by the SHA-256 above, but the `.py` bytes are not embedded in this commit.

```text
IMPLEMENTATION_IDENTITY_ADMITTED
!= IMPLEMENTATION_BYTES_EMBEDDED
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

- Attempt 001 as preserved procedural failure evidence;
- Attempt 002 return identity;
- Attempt 002 implementation identity;
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
