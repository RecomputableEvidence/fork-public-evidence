# FPCF-002 public publication readback — v0.1

Status: **PUBLIC_BYTES_READBACK_MATCHED_WITH_REPAIR**; not forecast or method admission.

The ten published base64 parts were fetched by exact GitHub commit and compared to the staged inputs after whitespace removal. Parts 1–9 matched. Initial part 10 had a 44-character duplicated final line arising from an overlapping end-of-file read in the publishing transport. This was observed before final pull-request creation and repaired in successor commit `8851ff521717916f9e912ac48242e76ea42342a2`. Original erroneous publication remains in Git commit history.

Re-read the ten parts at the corrected commit: each of parts 01–09 contains 80,000 base64 characters; part 10 contains 51,948; total **771,948**, the expected length for the **578,960-byte** preserved ZIP. Each part matches staged source content after whitespace normalization (the repaired tenth segment was read directly from the complete EOF-bounded source).

The complete source ZIP was independently built and locally decoded from the original ten split parts with byte equality. Its SHA-256 is `b4956497d4c146c2825b593064a64d2c3a362e51ba5048617f4d8f1d8e09a486`.

**Nonclaims:** The connector readback matched published text and lengths, but does not establish third-party execution of a ZIP-level digest calculation on a GitHub checkout. GitHub publication time does not independently timestamp the contained predecision sequence. No forecast outcome, Lens effect, source truth, or institutional authorization has been admitted. Reviewer should run the offline reconstruction in the release README to verify the full hash and inspect each source object.
