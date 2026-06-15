# Evidence Artifact Boundary

## Purpose

This file defines what evidence Fork may capture, hash, reference, exclude, or treat as unavailable.

## Evidence categories

Use these categories:

- `CAPTURED`
- `HASHED_REFERENCE`
- `EXTERNAL_POINTER`
- `SOURCE_UNAVAILABLE`
- `EXPLICIT_NON_CLAIM`
- `UNKNOWN`

## Artifact boundary table

| Artifact | Source system | Category | Format | Sensitivity | Retention risk | Boundary notes |
|---|---|---|---|---|---|---|
| `[FORK_TO_COMPLETE]` | `[FORK_TO_COMPLETE]` | `[CAPTURED / HASHED_REFERENCE / EXTERNAL_POINTER / SOURCE_UNAVAILABLE / EXPLICIT_NON_CLAIM / UNKNOWN]` | `[FORK_TO_COMPLETE]` | `[LOW / MEDIUM / HIGH / RESTRICTED / UNKNOWN]` | `[LOW / MEDIUM / HIGH / UNKNOWN]` | `[FORK_TO_COMPLETE]` |

## Captured evidence

Artifacts Fork may copy into an evidence packet:

`[FORK_TO_COMPLETE / NONE / UNKNOWN]`

## Hashed references

Artifacts Fork may hash but not store:

`[FORK_TO_COMPLETE / NONE / UNKNOWN]`

## External pointers

Artifacts Fork may reference only by identifier, path, ticket, URL, case number, or other pointer:

`[FORK_TO_COMPLETE / NONE / UNKNOWN]`

## Source unavailable

Relevant artifacts or sources that are unavailable:

`[FORK_TO_COMPLETE / NONE / UNKNOWN]`

## Explicit non-claims

Matters Fork must not imply from the evidence boundary:

`[FORK_TO_COMPLETE / NONE / UNKNOWN]`

## Boundary decision

Select one:

- `[ ] EVIDENCE_ARTIFACT_BOUNDARY_DRAFTED`
- `[ ] EVIDENCE_ARTIFACT_BOUNDARY_REQUIRES_REVIEW`
- `[ ] EVIDENCE_ARTIFACT_BOUNDARY_BLOCKED`
- `[ ] EVIDENCE_ARTIFACTS_UNKNOWN`

Reason:

`[FORK_TO_COMPLETE]`