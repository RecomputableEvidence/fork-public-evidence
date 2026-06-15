# Access and Export Model

## Purpose

This file describes how relevant workflow evidence can be accessed or exported without turning Fork into a runtime dependency.

## Access posture

- [x] Manual export
- [x] File drop
- [ ] Watch folder
- [ ] Read-only API pull
- [x] Report export
- [x] Hash-only reference
- [x] External pointer only
- [ ] No access available
- [ ] Unknown

## Export formats

- [x] JSON
- [ ] JSONL
- [x] CSV
- [ ] PDF
- [ ] XML
- [ ] TXT
- [ ] API response
- [ ] Screenshot
- [x] System report
- [ ] Audit export
- [x] GRC export
- [x] Ticket export
- [ ] Other: Not used
- [ ] Unknown

## Export cadence

- Export cadence: Weekly during pilot discovery
- Timezone: America/Los_Angeles
- Retention period: 18 months in GRC system
- Are records overwritten? NO
- Are records deleted or expired? NO during pilot period
- Are records mutable after creation? PARTIAL

## Access restrictions

- Is read-only access permitted? YES
- Are service accounts permitted? NO during discovery
- Are production credentials prohibited? YES
- Is API access permitted? NO during discovery
- Is manual export preferred? YES
- Is data allowed to leave client environment? PARTIAL
- Are hashes allowed if files cannot be copied? YES
- Are external references allowed? YES

## Bridge feasibility signal

- [x] MANUAL_EXPORT_FEASIBLE
- [x] FILE_DROP_FEASIBLE
- [ ] WATCH_FOLDER_FEASIBLE
- [ ] API_PULL_FEASIBLE
- [x] HYBRID_REFERENCE_FEASIBLE
- [ ] ACCESS_MODEL_UNKNOWN
- [ ] ACCESS_MODEL_BLOCKED

Reason:

A first pilot can use manual exports and controlled file-drop delivery without production credentials or runtime dependency.

## Open access questions

None