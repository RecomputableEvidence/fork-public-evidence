# PR #183 CI PRESERVATION REPAIR 001

Status: `CHANGE_ACCOUNTED_WITHOUT_STANDING_PROMOTION`

PR #183 exposed a line-ending enforcement conflict between repository-native text normalization and preservation of an exact historical source-return receipt.

The bounded repair changes `tools/check_line_endings.py` from Git blob `dad8906f4977c939823bc70ebec0132e00f15ff7` to `3ad15c048511bb4c53387746023f9625d09afb08`.

The change adds one path-specific preservation exception for:

`research/fork-relational-resolution-demonstration-001/AG5_LOCAL_RECOMPUTATION_RECEIPT_ATTEMPT_002.json`

The exception is valid only when that file's SHA-256 is exactly:

`884fcfacc980e91127ed8e67eba99eb84fc78043ce1c32bbd70cdcae9f96cfcc`

A byte change fails the checker rather than broadening the exception.

Separately, the repository-native inspection copy `SOURCE_RETURN_SHA256SUMS.txt` is normalized to LF. The original successful return manifest bytes remain preserved inside the exact source-return archive.

A subsequent Windows proof-surface run exposed Git's own text-normalization warning for the same historical receipt. The exact path is therefore also marked `-text` in `.gitattributes`, matching the existing repository pattern for exact supplied historical evidence bytes. This prevents Git from attempting line-ending canonicalization on that preserved object; the SHA-256 lock in `tools/check_line_endings.py` remains the fail-closed identity guard.

This record accounts for the recognized tool transition required by `PROGRAM_CHANGE_ACCOUNTING_v0_2.json`. It does not change the closed demonstration or its admitted results.

```text
TOOL_TRANSITION_ACCOUNTED
!= RESEARCH_RESULT_CHANGE

PRESERVATION_EXCEPTION
!= UNBOUNDED_EXEMPTION

GIT_TEXT_CANONICALIZATION
!= HISTORICAL_BYTE_PRESERVATION

CI_REPAIR
!= EDGE_STANDING_CHANGE

CI_REPAIR
!= AUTHORITY_CHANGE

CI_REPAIR
!= CLOSED_OBJECT_REOPENED
```
