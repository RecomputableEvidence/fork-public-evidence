# AG5 Local Recomputation Attempt 001 — Procedural Failure Preservation

Object: `FORK-RELATIONAL-RESOLUTION-DEMONSTRATION-001`

Attempt: `AG5_LOCAL_RECOMPUTATION_ATTEMPT_001`

Standing: `PROCEDURAL_FAILURE_BEFORE_EDGE_RECOMPUTATION`

The first local recomputation attempt successfully verified the AG4 branch coordinate, the AG3 parent coordinate, repository object integrity via `git fsck --full --strict`, and the exact target artifact byte length and SHA-256. It then failed while creating a full detached worktree on Windows because unrelated repository paths exceeded the local pathname limit. The subsequent Python invocation failed because the intended temporary worktree and packet files had not been materialized.

No edge recomputation completed in Attempt 001. No AG4 comparison completed. No recomputation receipt was produced.

The preserved source transcript received in the review conversation had SHA-256:

`bbe430a05d65697f90c9ca14b7b458cc8923bd4ada1b26a2f087331d965abd0f`

That transcript is not embedded byte-for-byte in this repository record; this file preserves its identity and bounded procedural disposition.

```text
WORKTREE_CHECKOUT_FAILURE
!= AG4_RECOMPUTATION_MISMATCH

PYTHON_FILENOTFOUND
!= EDGE_STATUS_MISMATCH

ATTEMPT_001_PROCEDURAL_FAILURE
!= AG4_STATUS_FAILURE
```

Attempt 001 remains historical negative procedural evidence. It is not superseded or erased by the successful Attempt 002.
