# Exterior return package

Object: `FORK-RRD-001-AG8-INDEPENDENT-RECOMPUTATION-RETURN-001`

This directory preserves the independent recomputation return as a separate exterior object adjacent to, but not inside, the closed `FORK-RELATIONAL-RESOLUTION-DEMONSTRATION-001` object.

Files:

- `SOURCE_RETURN_ARCHIVE.zip` — exact uploaded source archive bytes. This is the primary source-return object and contains the empty failed-return directory plus the successful receipt, console transcript, and return manifest.
- `SOURCE_RETURN_SHA256SUMS.txt` — LF-normalized inspection copy of the successful return manifest. The original manifest bytes remain preserved inside `SOURCE_RETURN_ARCHIVE.zip` and are hash-bound in `ADMISSION.json`.
- `ADMISSION.json` — repository admission and reconciliation record.
- `RECONCILIATION.md` — human-readable disposition and boundaries.
- `CI_PRESERVATION_REPAIR_001.md` — bounded repair record for PR #183 line-ending enforcement.
- `SHA256SUMS.txt` — SHA-256 identities for the preserved files in this exterior-return object.

The raw source archive is primary. The admission, reconciliation, inspection copy, and CI repair records do not rewrite its contents.
