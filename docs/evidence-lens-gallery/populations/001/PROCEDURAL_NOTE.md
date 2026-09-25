# Population 001 procedural note

This note records a tool-side branch-write error during construction of `FORK-EVIDENCE-LENS-GALLERY-001-POPULATION-001`.

After the population branch was created from `main@5ee76df67f25ff6be03f025cf6795088b9c4aef2`, an unintended contents-API call created branch commit:

`b9ad3c54517cda7047b9d2533d904820865b2350`

That commit contains an empty root file named `__dummy__` and an empty commit message. It was not a research action, Gallery population event, source observation, standing transition, or semantic disposition.

Before that accidental branch write, the intended population tree had been constructed and commit object:

`a0ea097ee91be88fa93700af1a026f1c06b6e4a9`

was created from the original branch base. Because the branch reference was never advanced to that commit, it was never branch-reachable and carries no repository standing by itself.

The successor correction preserves the accidental commit in branch history, removes `__dummy__` by replacing the tree with the intended population tree, and adds this note. No force-update or history erasure is used.

```text
UNINTENDED_BRANCH_WRITE
!= GALLERY_POPULATION_EVENT

UNREFERENCED_COMMIT_OBJECT
!= BRANCH_HISTORY

BRANCH_HISTORY_PRESERVED
!= PROCEDURAL_ERROR_PROMOTED

CORRECTION
!= HISTORY_ERASURE
```
