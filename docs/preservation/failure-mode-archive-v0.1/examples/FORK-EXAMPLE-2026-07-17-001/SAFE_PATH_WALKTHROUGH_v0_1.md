# VDF-001 safe-path walkthrough

Example: `FORK-EXAMPLE-2026-07-17-001`

Failure class: `VDF-001_VERIFICATION_DEPENDENCY_SCOPE_ASSUMPTION`

Status: preserved and resolved in the proposed PR #64 lineage. No admission or experiment authority.

## Failure signature

A verification module passes in the authoritative control environment but fails when the wider proof surface runs the full repository suite without the control-specific parser dependency. The same commit may therefore produce both a successful control result and failures in adjacent CI jobs.

This signature must not be collapsed into either “the contribution passed” or “the contribution is invalid.” The contribution result, dependency contract, and CI integration result are distinct observations.

## Safe path

1. Stop promotion while retaining the candidate branch and every original CI observation.
2. Record the exact failing commit, tree, run IDs, job IDs, conclusions, and affected file bytes.
3. Compare the installed lock files for successful and failing jobs.
4. Determine whether the missing package belongs to the failing environment’s declared contract.
5. If the dependency is not part of that contract, do not broaden the environment merely to silence CI. Make the test’s dependency boundary explicit.
6. Retain authoritative execution in the environment that declares the dependency. An explicit skip elsewhere may describe scope; it may not fabricate a pass for an authoritative check.
7. Run both environments again. Preserve executed-test counts and dependency-boundary skips separately.
8. Admit only a new repair commit. Do not alter or erase the failing commit, first-run observations, or specimens.

## Applied result

Fork Evidence CI installed both the proof-surface and claim-admission locks and executed all ten Independent Verification Surface tests successfully. Proof-Surface Integration intentionally installed only the proof lock; after the repair, its full suite completed with the YAML-dependent verification module explicitly skipped. The remaining proof-surface tests and all five matrix jobs completed successfully.

This establishes a bounded clean bill for the dependency integration only. It does not provide independent human review, merge approval, security certification, repository standing, or experiment execution authority.
