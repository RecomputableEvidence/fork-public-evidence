# Independent Reviewer Worksheet — PR #64 IVS v0.1.1

This worksheet records an independent human recomputation. Completing it does not constitute endorsement, merge approval, security certification, repository standing, or experiment authority.

## 1. Reviewer attribution

- Reviewer name or pseudonym:
- Affiliation, if voluntarily disclosed:
- Contact or durable public identifier:
- Relationship to the contribution author:
- Conflicts or prior involvement:
- Review date and time in UTC:

## 2. Exact package identity

- Repository: `RecomputableEvidence/fork-public-evidence`
- Pull request: `#64`
- Exact package commit:
- Exact package tree:
- Verifier release commit expected: `e366e44cb2059f5cb7243757b95fa8d44859b811`
- Exact plan Git blob observed:
- Exact committed receipt Git blob observed:

Confirm:

- [ ] I used the exact full commit SHA supplied in the review request.
- [ ] I did not substitute a mutable branch, tag, or test merge commit.
- [ ] I began from an empty disposable repository for the fresh recomputation.

## 3. Environment

- Operating system and version:
- Architecture:
- Python version:
- Git version:
- `jsonschema` version:
- `PyYAML` version:
- Network constraints or mirrors:
- Other relevant environmental facts:

## 4. Commands executed

Record the exact commands in order, including any deviations from the published procedure:

```text

```

## 5. Fresh-repository result

- Runner exit code:
- Runner result:
- Candidate checkout observed: `NONE` / other:
- Candidate-code execution observed: `NONE` / other:
- Receipt byte equality: `TRUE` / `FALSE` / `UNRESOLVED`
- Temporary repository retained after run: `NO` / `YES` / `UNKNOWN`

## 6. Contract inspection

For each item, record `SUPPORTED`, `CONTRADICTED`, or `INCONCLUSIVE`, with evidence coordinates.

| Review item | Finding | Evidence coordinates or explanation |
|---|---|---|
| Schema-valid supported receipt |  |  |
| Schema-valid contradicted receipt |  |  |
| Schema-valid inconclusive receipt |  |  |
| Verifier commit and component bindings |  |  |
| Running checker matches declared checker blob |  |  |
| v0.1 plan and receipt lineage preserved |  |  |
| v0.1 receipt recomputes byte-exactly |  |  |
| Verdict precedence is explicit and deterministic |  |  |
| Mixed contradiction/gap counts remain visible |  |  |
| External observations are temporally attributable |  |  |
| Duplicate JSON keys are rejected |  |  |
| Non-finite JSON values are rejected |  |  |
| Assertion identifiers are unique |  |  |
| Git object type and mode are recorded |  |  |
| Symlink or non-regular substitution is rejected |  |  |
| Candidate checkout and execution remain absent |  |  |

## 7. Contradictions and evidence gaps

Record every contradiction or unresolved condition. Do not omit a finding because the overall package reproduced.

| ID | Type | Affected artifact | Observation | Reproduction coordinates |
|---|---|---|---|---|
|  |  |  |  |  |

## 8. Final independent disposition

Select exactly one:

- [ ] `REPRODUCED_WITHIN_DECLARED_SCOPE`
- [ ] `INVALIDATED_BY_INDEPENDENT_RECOMPUTATION`
- [ ] `INCONCLUSIVE_EVIDENCE_GAP`

### Scope statement

Describe exactly what this disposition supports and what it does not support:


### Reviewer attestation

I attest only that this worksheet accurately records my review activity and observations. I do not, by completing it, approve a merge, certify security, endorse Fork, grant repository standing, authorize an experiment, or determine truth beyond the evidence inspected.

- Reviewer signature or durable acknowledgment:
- Date and time in UTC:
