# Access and Export Model

## Purpose

This file describes how relevant workflow evidence can be accessed or exported without turning Fork into a runtime dependency.

Fork is read-only and out-of-band.

Fork should not block, route, approve, deny, or modify live workflow execution.

## Access posture

Select all that may apply:

- `[ ] Manual export`
- `[ ] File drop`
- `[ ] Watch folder`
- `[ ] Read-only API pull`
- `[ ] Report export`
- `[ ] Hash-only reference`
- `[ ] External pointer only`
- `[ ] No access available`
- `[ ] Unknown`

## Export formats

Select all available formats:

- `[ ] JSON`
- `[ ] JSONL`
- `[ ] CSV`
- `[ ] PDF`
- `[ ] XML`
- `[ ] TXT`
- `[ ] API response`
- `[ ] Screenshot`
- `[ ] System report`
- `[ ] Audit export`
- `[ ] GRC export`
- `[ ] Ticket export`
- `[ ] Other: [CLIENT_TO_COMPLETE]`
- `[ ] Unknown`

## Export cadence

- Export cadence: `[One-time / Daily / Weekly / Monthly / Event-driven / Manual / Unknown]`
- Timezone: `[CLIENT_TO_COMPLETE / UNKNOWN]`
- Retention period: `[CLIENT_TO_COMPLETE / UNKNOWN]`
- Are records overwritten? `[YES / NO / UNKNOWN]`
- Are records deleted or expired? `[YES / NO / UNKNOWN]`
- Are records mutable after creation? `[YES / NO / PARTIAL / UNKNOWN]`

## Access restrictions

- Is read-only access permitted? `[YES / NO / UNKNOWN]`
- Are service accounts permitted? `[YES / NO / UNKNOWN]`
- Are production credentials prohibited? `[YES / NO / UNKNOWN]`
- Is API access permitted? `[YES / NO / UNKNOWN]`
- Is manual export preferred? `[YES / NO / UNKNOWN]`
- Is data allowed to leave client environment? `[YES / NO / PARTIAL / UNKNOWN]`
- Are hashes allowed if files cannot be copied? `[YES / NO / UNKNOWN]`
- Are external references allowed? `[YES / NO / UNKNOWN]`

## Bridge feasibility signal

Select one:

- `[ ] MANUAL_EXPORT_FEASIBLE`
- `[ ] FILE_DROP_FEASIBLE`
- `[ ] WATCH_FOLDER_FEASIBLE`
- `[ ] API_PULL_FEASIBLE`
- `[ ] HYBRID_REFERENCE_FEASIBLE`
- `[ ] ACCESS_MODEL_UNKNOWN`
- `[ ] ACCESS_MODEL_BLOCKED`

Reason:

`[CLIENT_TO_COMPLETE]`

## Open access questions

`[CLIENT_TO_COMPLETE / NONE]`