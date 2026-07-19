# Fork Failure-Mode Preservation Archive v0.1

This archive preserves classified repository and system failure modes as inert, attributable evidence. Each incident folder records exact specimens, provenance coordinates, classification, continuance basis, residual conditions, and a step-by-step safe-path walkthrough.

Archived specimens are data. They must not be executed, imported, restored to live paths, or used as admission logic.

## Current corpus

- `FORK-INC-2026-07-13-001`: malformed evidence-bearing GitHub Actions workflow and the associated claim-consumption failure `CCF-001_AI_CHANGE_READINESS_PROMOTION`.
- `FORK-EXAMPLE-2026-07-17-001`: resolved Independent Verification Surface CI dependency-scope example classified as `VDF-001_VERIFICATION_DEPENDENCY_SCOPE_ASSUMPTION`.

## Current standing

- Archive status: `PROPOSED_FOR_ADMISSION`.
- Incident status: `PRESERVED_OPEN`.
- Classified-example status: `PRESERVED_RESOLVED`.
- Experiment effect: `NONE`.
- Consumer-owned admission control: planned in a separately scoped change.

## Verification

```powershell
python tools/check_preservation_integrity_v0_1.py
python -m pytest tests/test_preservation_integrity_v0_1.py -q
```

A pass establishes only the structural and integrity conditions implemented by the checker. The bounded baseline receipt is at `receipts/preservation-integrity/FORK_INC_2026_07_13_001_BASELINE_RECEIPT_v0_1.json`.
