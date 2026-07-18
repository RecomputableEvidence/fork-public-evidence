## Claim

<!-- State the specific change this PR introduces. Do not claim more than the diff and evidence support. -->

## Change classification

- Primary class: <!-- C0, C1, C2, C3, C4, C5, C6, or C7 -->
- Secondary classes: <!-- NONE or list -->
- Governing artifact or ruleset: <!-- path and version -->
- Classification rationale:

See [`docs/governance/CHANGE_CLASSIFICATION_v0_1.md`](../docs/governance/CHANGE_CLASSIFICATION_v0_1.md).

## Scope

### Changed surfaces

<!-- Identify files and artifact classes affected. -->

### Explicit exclusions

<!-- Identify related surfaces intentionally left unchanged. -->

## Verification

- Candidate commit: <!-- full SHA; update after final push -->
- Governing verification guide: <!-- path and version -->
- Environment: <!-- OS, shell/version, interpreter/version, material dependencies -->

### Commands executed

```text
<exact command>
```

### Expected result

<!-- Exit status, test count, finding/classification token, receipt path, or other predetermined result. -->

### Observed result

<!-- Report the actual result, including failures, skips, warnings, or evidence gaps. -->

### Generated changes

<!-- NONE or identify generated/modified files and regeneration procedure. -->

### Untested or unresolved conditions

<!-- NONE or explicit conditions. -->

## Boundary impact

For each field, state `UNCHANGED` or describe the exact change.

- Claims:
- Non-claims:
- Exclusions:
- Authority limitations:
- Unresolved or unobserved conditions:
- Evidence references:
- Schema meaning:
- Classification or finding behavior:
- Verification scope:

## Historical and admission impact

- Historical artifact modified, corrected, superseded, or projected from: <!-- NONE or identify -->
- Admission, publication, release, or canonical-state transition claimed: <!-- NONE or identify governing procedure -->
- Original bytes or sealed representation preserved where required: <!-- N/A, YES, or explain -->
- Exact originating commit or record: <!-- N/A or identifier -->

Submission, verification, review, merge, admission, publication, release, experiment readiness, and experiment execution are separate events unless the governing procedure explicitly binds them.

## Review requirements

- [ ] The PR is tightly scoped or necessary atomicity is explained.
- [ ] Formatting or mechanical changes are separated from semantic changes where practical.
- [ ] Commands were executed against the candidate identified above.
- [ ] The observed result is reported without converting evidence gaps or failures into a pass.
- [ ] No passing checker is represented as truth, compliance, legality, safety, endorsement, production readiness, or authority transfer.
- [ ] Historical and current-state records remain distinguishable.
- [ ] Experiment instrumentation and execution are separated where the change could affect results.
- [ ] Required independent review or admission procedure is identified where applicable.

## Reviewer notes

<!-- Optional: focus areas, expected difficult questions, or known residuals. -->