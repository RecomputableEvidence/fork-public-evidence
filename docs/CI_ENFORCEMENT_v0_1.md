# Fork CI Enforcement v0.1

Status: INTERNAL_REPOSITORY_GATE

## 1. Purpose

This layer moves Fork's local evidence-preservation and Claim Boundary invariants into automated repository checks.

Prior layers established:

- Claim Boundary Contract v0.1
- Claim Boundary Enforcement Phase 2
- Claim Boundary Binding v0.1
- Line Ending Canonicalization v0.1

CI Enforcement v0.1 makes those checks run automatically on pull requests and pushed v0 branches.

## 2. Enforced Invariants

The GitHub Actions workflow enforces:

1. Governed text artifacts must use LF line endings.
2. Valid claim boundary payloads must pass.
3. Overclaiming claim boundary payloads must fail.
4. Machine-readable artifacts missing claim_boundary must fail.
5. Machine-readable artifacts with overclaiming claim_boundary blocks must fail.
6. Bound verifier artifacts must pass.
7. Unbound verifier artifacts must fail.
8. Generated bound artifacts must pass artifact-level enforcement.
9. The full pytest suite must pass.

## 3. Workflow

The workflow is:

    .github/workflows/fork-evidence-ci.yml

It runs on:

- pull_request
- push to main
- push to v0_* branches

## 4. Boundary

This CI layer does not by itself prove enterprise readiness, legal sufficiency, compliance, admissibility, or correctness.

It proves only that the repository gates currently enforce the declared local invariants.

## 5. Invariant

Fork evidence-governance branches should not merge unless Claim Boundary enforcement, Claim Boundary Binding, line-ending preservation, and their tests pass automatically.