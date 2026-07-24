# Predecessor package-scope recomputation v0.1

The v0.3 construction exposed a transitive dependency defect in the original
v0.2 package manifest. That manifest froze the repository-wide
claim-admission self-check receipt and the shared state README as package
members. Both files legitimately change when a successor is added.

Observed result before correction:

> A truthful successor changed shared dependency bytes and therefore made the
> predecessor package appear corrupted when recomputed against the successor
> worktree.

Disposition:

- `PACKAGE_MANIFEST_v0_2.json` remains unchanged as historical PR #91 bytes;
- `PACKAGE_DEPENDENCY_SCOPE_CORRECTION_v0_2_1.md` records the defect;
- `PACKAGE_MANIFEST_v0_2_1.json` contains only versioned v0.2 package members;
- the shared README and global self-check receipt remain validated by their
  owning checks but are not represented as immutable v0.2.1 package members.

This correction changes package dependency scope only. It does not change the
v0.2 state vector, event registry, replay interval, review standing, or
non-effects. It does not admit v0.2 or v0.3.
