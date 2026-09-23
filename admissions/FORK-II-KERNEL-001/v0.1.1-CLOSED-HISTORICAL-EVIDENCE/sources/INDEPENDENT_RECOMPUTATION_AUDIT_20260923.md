# Independent recomputation audit — 2026-09-23

Input archive SHA-256: `0b7b86c1e709234ed1c1b9f304bccdcc6db62960dae45b33c94772bacb9ab764`

## Result

**Re-derived disposition: `CROSS_ENVIRONMENT_REPRODUCTION_OBSERVED`.** No contradiction was found in the preserved evidence.

This is an evidence-level recomputation of the cross-environment comparison, not a fresh third execution of the frozen subject. The subject executable ZIP is not included in the comparison archive.

## Independently verified from bytes present

- Outer comparison manifest: 11/11 entries match declared byte length and SHA-256.
- Preserved ChatGPT record SHA256SUMS: 91/91 listed files match. `SHA256SUMS.txt` itself is the only unlisted file.
- Outer ZIP and inner ChatGPT ZIP both pass ZIP CRC testing.
- ChatGPT raw outputs directly show baseline 22/22 PASS, seven unit tests OK, and all 12 mutants exiting 1.
- The exact failed-fixture pattern parsed from the ChatGPT stdout files matches the comparison record.
- For every one of the 12 mutant structured JSON files, `SHA256(recomputed_bytes + b"\n")` equals the previously logged packaged-receipt SHA-256; the baseline matches without adding LF.

## Independently re-derived from preserved raw execution evidence

- Claude raw transcript directly records Ubuntu 24.04.4 LTS, CPython 3.12.3, GCC 13.3.0, glibc 2.39, x86_64.
- Claude raw transcript directly records manifest check 63/63 with 0 mismatches, baseline 22/22 PASS, 7 tests OK, and 12/12 mutant detection.
- Claude raw mutant failure lines reproduce the same failed-fixture pattern as the ChatGPT record.
- Claude raw transcript records baseline PASS under `-W error` with empty stderr and records all 13 receipts as JSON-equivalent, with the same terminal-LF asymmetry on mutants.

## Boundary

Because the frozen 70,171-byte subject executable archive is not present in this package, this audit cannot independently recompute its SHA-256 from subject bytes, independently re-hash the 63 subject-manifest entries, directly inspect the packaged subject receipts, or perform a third execution. Those points are supported here by two preserved prior execution records plus the detached hash receipt, not by fresh access to the subject bytes.

## Mutant concordance

- `authority_infects_evidence` → FII-17
- `automatic_license` → FII-05, FII-13
- `eligibility_authorization` → FII-01
- `false_negation` → FII-04
- `force_total_order` → FII-18
- `historical_disposition_promoted_to_correctness` → FII-20
- `historical_rewrite` → FII-14, FII-16
- `mutable_profile_reference` → FII-19
- `null_effective_until_promoted_to_indefinite_validity` → FII-22
- `scope_globality` → FII-03
- `stale_reuse` → FII-14, FII-15
- `unbound_dependency_snapshot` → FII-21
