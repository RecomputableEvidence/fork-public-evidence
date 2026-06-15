# Access and Export Boundary

## Purpose

This file defines the approved or candidate access/export boundary for Fork.

Fork remains read-only and out-of-band.

Fork should not become a runtime dependency.

## Candidate access model

Select one or more:

- `[ ] Manual export`
- `[ ] File drop`
- `[ ] Watch folder`
- `[ ] Read-only API pull`
- `[ ] Report export`
- `[ ] Hash-only reference`
- `[ ] External pointer only`
- `[ ] No access available`
- `[ ] Unknown`

## Approved or candidate export formats

- `[ ] JSON`
- `[ ] JSONL`
- `[ ] CSV`
- `[ ] PDF`
- `[ ] XML`
- `[ ] TXT`
- `[ ] API response`
- `[ ] System report`
- `[ ] Audit export`
- `[ ] GRC export`
- `[ ] Ticket export`
- `[ ] Other: [FORK_TO_COMPLETE]`
- `[ ] Unknown`

## Access restrictions

- Read-only access permitted: `[YES / NO / UNKNOWN]`
- Service accounts permitted: `[YES / NO / UNKNOWN]`
- Production credentials prohibited: `[YES / NO / UNKNOWN]`
- API access permitted: `[YES / NO / UNKNOWN]`
- Manual export preferred: `[YES / NO / UNKNOWN]`
- Data allowed to leave client environment: `[YES / NO / PARTIAL / UNKNOWN]`
- Hashes allowed if files cannot be copied: `[YES / NO / UNKNOWN]`
- External references allowed: `[YES / NO / UNKNOWN]`

## Candidate bridge pattern

Select if appropriate:

- `[ ] MANUAL_EXPORT_BRIDGE`
- `[ ] FILE_DROP_BRIDGE`
- `[ ] WATCH_FOLDER_BRIDGE`
- `[ ] API_PULL_BRIDGE`
- `[ ] HYBRID_REFERENCE_BRIDGE`
- `[ ] NO_BRIDGE_SELECTED`

Reason:

`[FORK_TO_COMPLETE]`

## Boundary decision

Select one:

- `[ ] ACCESS_EXPORT_BOUNDARY_DRAFTED`
- `[ ] ACCESS_EXPORT_BOUNDARY_REQUIRES_REVIEW`
- `[ ] ACCESS_EXPORT_BOUNDARY_BLOCKED`
- `[ ] ACCESS_EXPORT_MODEL_UNKNOWN`

Reason:

`[FORK_TO_COMPLETE]`