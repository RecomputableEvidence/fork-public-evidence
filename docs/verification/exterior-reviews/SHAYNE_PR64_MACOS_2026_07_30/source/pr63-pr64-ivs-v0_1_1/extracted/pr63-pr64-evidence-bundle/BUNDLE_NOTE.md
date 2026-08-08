# Evidence Bundle — PR #63 / PR #64 Independent Recomputation (Shayne Beavan, 2026-07-30)

Contents are the ORIGINAL bytes as generated during the review run (timestamps preserved via cp -p), not reconstructions.

- FINDINGS-MEMO-PR63-PR64-IVS-v0_1_1.md — the memo, exact file as written.
- raw/PR_63_receipt_mine.json — receipt from my direct checker run (the one cmp'd byte-identical to the committed receipt).
- raw/r_1.json, raw/r_2.json, raw/r_42.json — receipts from the PYTHONHASHSEED determinism runs.
- raw/checker_out.txt — direct checker stdout capture.
- raw/plan_tampered.json — the single-byte-altered plan copy used for the fail-closed probe.
- raw/tamper_out.txt — checker output from the tamper probe (exit 2).
- raw/diff_real.txt — independently computed `git diff --name-only <merge-base> <head>` (20 paths).
- ENVIRONMENT_RECORD.txt — generated at bundle-assembly time (same host/session), labeled as such.

## Coverage disclosure (preserved, not repaired)
The fresh-runner step's JSON stdout (`FRESH_RECOMPUTATION_PASS`, `receipt_byte_exact: true`) was NOT redirected to a file at run time; its original bytes are not preserved here. The memo's transcription of it is a transcription. Rerunning would produce a fresh artifact, not the original, so per your instruction nothing was rerun to fill this gap. All other listed artifacts are original run bytes.

SHA256SUMS.txt covers every file in this bundle; digests computed at assembly.
