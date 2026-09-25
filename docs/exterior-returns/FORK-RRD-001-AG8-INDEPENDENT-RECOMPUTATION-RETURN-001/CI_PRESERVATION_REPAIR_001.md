# CI PRESERVATION REPAIR 001

Status: `BOUNDED_CI_PRESERVATION_REPAIR_COMPLETE`

PR: `#183`

Trigger: `Fork Evidence CI` run `36108966674` failed the governed-text line-ending check on two paths after the closed research lineage and exterior return were presented for main admission.

Observed paths:

1. `docs/exterior-returns/FORK-RRD-001-AG8-INDEPENDENT-RECOMPUTATION-RETURN-001/SOURCE_RETURN_SHA256SUMS.txt`
2. `research/fork-relational-resolution-demonstration-001/AG5_LOCAL_RECOMPUTATION_RECEIPT_ATTEMPT_002.json`

Disposition:

- `SOURCE_RETURN_SHA256SUMS.txt` is repository-native inspection metadata. Its three manifest lines are preserved while its line endings are normalized from CRLF to LF.
- `AG5_LOCAL_RECOMPUTATION_RECEIPT_ATTEMPT_002.json` is a frozen historical source-return object. Its bytes are not normalized or rewritten.
- `tools/check_line_endings.py` is amended with a single path-specific, SHA-256-locked preservation exception for that historical receipt.
- The exception is valid only while the exact file SHA-256 remains `884fcfacc980e91127ed8e67eba99eb84fc78043ce1c32bbd70cdcae9f96cfcc`. A byte change removes the exception and causes the checker to fail closed.

Boundaries:

```text
FOREIGN_HISTORICAL_BYTES
!= GOVERNED_NATIVE_TEXT

PRESERVATION_EXCEPTION
!= UNBOUNDED_EXEMPTION

PATH_MATCH + SHA256_MATCH
= ALLOW_EXACT_HISTORICAL_BYTES_ONLY

CI_REPAIR
!= RESEARCH_RESULT_CHANGE

CI_REPAIR
!= EDGE_STANDING_CHANGE

CI_REPAIR
!= AUTHORITY_CHANGE

CI_REPAIR
!= CLOSED_OBJECT_REOPENED
```

The CI failure is preserved in the GitHub Actions history. This repair does not alter the closed AG8 object, the historical AG5 receipt bytes, the 55/55 independent recomputation result, or the exterior-return standing.
