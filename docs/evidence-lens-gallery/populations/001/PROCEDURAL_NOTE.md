# Population 001 procedural note

This note records tool-side construction events during `FORK-EVIDENCE-LENS-GALLERY-001-POPULATION-001`.

The population branch was created from exact `main@5ee76df67f25ff6be03f025cf6795088b9c4aef2`.

An unintended contents-API call then created branch commit:

`b9ad3c54517cda7047b9d2533d904820865b2350`

That commit added an empty root file named `__dummy__` with an empty commit message. It was not a research action, Gallery population event, source observation, standing transition, or semantic disposition.

Two correctly constructed low-level commit objects were also created during recovery but were never made branch-reachable:

- `a0ea097ee91be88fa93700af1a026f1c06b6e4a9` — intended population tree from the original branch base;
- `c010f3ae7ef2eb6a9e7678817c6079938767b695` — intended population tree plus this procedural note, parented to the accidental commit.

Because neither commit was ever referenced by the branch, neither carries branch standing.

Recovery then proceeded additively on the actual branch history:

- `daa1c06465b67942d091cced0322f41e749b8a6f` — preserved the procedural note;
- `c30698d02f93c5219d84790314d30793e0dfa308` — added the Population 001 README;
- `3bfabc340f93f435acd819dad0dc9488f8554f1a` — added the machine-readable population package;
- `19a5b8fab3921b28923dac737fe383bec2186643` — added package checksums;
- `709928a21286fbcb27ad7c9f32fb7e4afa944ca1` — removed the unintended `__dummy__` file.

No force-update or history erasure was used. The final branch diff contains the authorized population artifacts plus this procedural note and does not contain `__dummy__`.

`SHA256SUMS.txt` binds the Population 001 README and machine-readable package; this procedural note is intentionally outside that two-file population-package checksum set.

```text
UNINTENDED_BRANCH_WRITE
!= GALLERY_POPULATION_EVENT

UNREFERENCED_COMMIT_OBJECT
!= BRANCH_HISTORY

BRANCH_HISTORY_PRESERVED
!= PROCEDURAL_ERROR_PROMOTED

CORRECTION
!= HISTORY_ERASURE

PROCEDURAL_NOTE
!= POPULATION_ENTRY
```
