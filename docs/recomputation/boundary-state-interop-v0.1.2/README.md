# Fork Human Recomputation Sandbox v0.1.2

Status: implemented access-path integrity and retrieval-distortion test surface  
Supersedes for this scope: `boundary-state-interop-v0.1.1`  
Scope: Reviewer Access Path Integrity / Retrieval Distortion / Interpreter Compatibility

## Purpose

This surface tests whether reviewer-access limitations remain distinguishable from content findings.

It preserves the following rule:

> A failed retrieval, partial retrieval, transformed retrieval, interpreter incompatibility, or unavailable execution environment is an access or execution condition. It must not be upgraded into a negative content review, positive validation, or authority conclusion.

## Access classes

- `full_repository`
- `packet_only`
- `partial_artifact`
- `transformed_or_excerpted`
- `retrieval_failed`
- `interpreter_incompatible`
- `execution_unavailable`
- `execution_successful`

## Verification

```bash
python tools/check_reviewer_access_path_integrity_v0_1.py --json
python -m pytest tests/test_reviewer_access_path_integrity_v0_1.py -q
```

## Interpretation

A pass demonstrates only that the shipped fixtures preserve the declared access-path boundary under the current deterministic checker.

It does not establish that an artifact is true, sufficient, compliant, safe, authorized, approved, production ready, or institutionally valid. It does not convert a reviewer into authority.
