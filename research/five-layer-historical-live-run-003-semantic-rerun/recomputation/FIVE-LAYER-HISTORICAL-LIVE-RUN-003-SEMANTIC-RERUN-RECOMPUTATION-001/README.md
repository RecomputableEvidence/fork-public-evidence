# Run 003 Semantic Rerun — Recomputation 001

**Object:** `FIVE-LAYER-HISTORICAL-LIVE-RUN-003-SEMANTIC-RERUN-RECOMPUTATION-001`

**Disposition:** `SEMANTIC_RERUN_RECOMPUTATION_PASS_WITH_RANGE_SERIALIZATION_UNDERSPECIFICATION_PRESERVED`

## Subject

- Run 003 subject commit: `1cd66122b9de9dec589f9f59ea7feb233db6083f`
- Preceding packaging-recomputation freeze: `f8ba8c41aee2c95012a859d1ac12a0a9a6e8e910`

## Recomputed

- 8/8 declared Run 003 package-artifact SHA-256 values matched.
- 3/3 repository subject bindings matched at `243ece21674dd58602787edc88eed43cda6eb59c`.
- Raw `git cat-file blob` exports reproduced the declared Git blob IDs.
- `HISTORICAL-LIVE-TARGET-001.txt`: 262,318 bytes, 4,026 lines, SHA-256 `a35124bb73fb3ac81bc01e66c60a68fe875f912f377f9aa02ef617d066f33583`.
- `RECURSIVE_LENS_SHIFT_SYNTHESIS.md`: 8,812 bytes, SHA-256 `1a19e2290e4ca53c14479da9b0ee0c483ab02fbd92536ca4d999663b6f9e49bc`.

## Preserved negative evidence

The first evidence-range recomputation omitted a terminal LF. All 17 declared range hashes failed and the guard threw. A subsequent unconditional string printed `PASS`; that string is preserved as false-positive shell output and does not alter the failed result.

A later diagnostic found one uniform reproducing convention for all 17 ranges without offset adjustment:

`DECLARED | LF_FINAL_UTF8_NO_BOM`

The final guarded recomputation using one-based inclusive bounds, LF interline separators, a final LF, UTF-8 and no BOM reproduced **17/17** declared hashes.

A separately entered PowerShell `else` also failed before the corrected combined conditional was entered. That shell error is preserved.

## Standing

The semantic detector results are not changed. The evidence ranges are not changed. Stage 3 remains untouched.

The newly established issue is narrower: the frozen Run 003 mapping did not state the terminal-LF range serialization contract explicitly enough for direct recomputation.

The exact 666-line recomputation transcript is preserved inside the separately bound generated package; the package ZIP bytes are not claimed repository-resident.

## Next object

`FIVE-LAYER-HISTORICAL-LIVE-RUN-004-RANGE-SERIALIZATION-CLARIFICATION-001`
