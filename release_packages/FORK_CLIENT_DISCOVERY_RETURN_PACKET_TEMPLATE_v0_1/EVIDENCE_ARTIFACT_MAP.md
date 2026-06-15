# Evidence Artifact Map

## Purpose

This file classifies evidence artifacts for the candidate workflow.

Each artifact should be classified as:

- `CAPTURED`
- `HASHED_REFERENCE`
- `EXTERNAL_POINTER`
- `SOURCE_UNAVAILABLE`
- `EXPLICIT_NON_CLAIM`
- `UNKNOWN`

## Artifact table

| Artifact | Description | Source system | Category | Format | Sensitivity | Retention risk | Notes |
|---|---|---|---|---|---|---|---|
| `[CLIENT_TO_COMPLETE]` | `[CLIENT_TO_COMPLETE]` | `[CLIENT_TO_COMPLETE]` | `[CAPTURED / HASHED_REFERENCE / EXTERNAL_POINTER / SOURCE_UNAVAILABLE / EXPLICIT_NON_CLAIM / UNKNOWN]` | `[CLIENT_TO_COMPLETE]` | `[LOW / MEDIUM / HIGH / RESTRICTED / UNKNOWN]` | `[LOW / MEDIUM / HIGH / UNKNOWN]` | `[CLIENT_TO_COMPLETE]` |

## Captured evidence

List artifacts that may be copied into a Fork evidence packet.

`[CLIENT_TO_COMPLETE / NONE / UNKNOWN]`

## Hashed references

List artifacts that may be hashed but not copied.

`[CLIENT_TO_COMPLETE / NONE / UNKNOWN]`

## External pointers

List artifacts that may only be referenced by identifier, path, URL, ticket, case number, or system pointer.

`[CLIENT_TO_COMPLETE / NONE / UNKNOWN]`

## Source unavailable

List relevant artifacts or sources that are unavailable.

`[CLIENT_TO_COMPLETE / NONE / UNKNOWN]`

## Explicit non-claims

List matters Fork must not imply from this evidence boundary.

`[CLIENT_TO_COMPLETE / NONE / UNKNOWN]`

## Evidence sufficiency concern

Does the available evidence appear sufficient for a bounded pilot discovery review?

Select one:

- `[ ] YES`
- `[ ] PARTIAL`
- `[ ] NO`
- `[ ] UNKNOWN`

Reason:

`[CLIENT_TO_COMPLETE]`