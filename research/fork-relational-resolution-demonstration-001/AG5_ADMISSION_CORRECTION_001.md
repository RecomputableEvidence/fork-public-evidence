# AG5 Admission Correction 001

Initial AG5 branch commit: `553e6e52c3315611e1884f9909b3db1b114615c0`

After that commit was created, an additional byte-identity check showed that the repository blob written at `AG5_LOCAL_RECOMPUTATION_CONSOLE_ATTEMPT_002.txt` did not reproduce the exact uploaded console-file Git blob identity, even though the source console SHA-256 had already been independently verified.

No PR had been opened and no merge had occurred.

The current AG5 head corrects the repository representation by rebuilding the AG5 tree from the exact AG4 tree and preserving the exact source transcript, console, and implementation bytes as deterministic gzip objects with independently bound raw-source SHA-256 identities. The exact Attempt 002 receipt remains embedded directly.

The initial AG5 commit remains in branch history as a procedural admission-construction error; it is not treated as the operative AG5 tree.

```text
INITIAL_AG5_BRANCH_COMMIT
!= CURRENT_AG5_ADMISSION_HEAD

REPRESENTATION_ERROR_IDENTIFIED
!= SOURCE_RECOMPUTATION_INVALIDATED

CORRECTED_CURRENT_TREE
!= PRIOR_COMMIT_ERASED
```
