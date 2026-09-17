# Independent Assessment of UEM Epoch 010 Reproduction Binding

Assessment date: 2026-09-16 (America/Los_Angeles)

## Disposition

**PASS — binding-package integrity and internal consistency, with bounded evidentiary scope.**

The uploaded `UEM-v0.1-EPOCH-010-INDEPENDENT-REPRODUCTION-BINDING.zip` is internally hash-consistent. Its nested assessment archive also verifies internally, and the duplicated assessment and reproduced receipt are byte-identical between the outer package and nested archive.

This assessment does **not** independently establish the underlying fresh verifier replay or executor reproduction, because the uploaded binding package does not contain the frozen verifier source/tests, `EXECUTOR_RESULTS.json`, or the original 16-fixture executor handoff needed to rerun those operations from this upload alone.

## Independently verified from this upload

- Uploaded archive SHA-256: `c1ce9b5655fae0907efb467f081125f800cdd2df3434439bb8eb292ab45370ac`
- Outer `SHA256SUMS`: **5/5 match**
- Nested `AUDIT_SHA256SUMS`: **2/2 match**
- Outer and nested assessment markdown: **byte-identical**
- Outer and nested reproduced verification receipt: **byte-identical**
- Binding JSON's assessment hash matches the included assessment: **yes**
- Binding JSON's nested assessment ZIP hash matches the included ZIP: **yes**
- Binding JSON's reproduced receipt hash matches the included receipt: **yes**
- Reproduced receipt parses as JSON and reports status: **PASS**
- Receipt fixture population: **16 unique fixtures**
- Validation distribution: **4 ACCEPT / 12 REJECT**
- Additional registered-rule entries in the receipt: **2**
  - UEM-E10-FX-007: CRII-010
  - UEM-E10-FX-014: CRII-013

## Claims carried by the package but not independently rerunnable from this upload alone

The binding JSON states that:

- verifier tests replayed `13/13 PASS`;
- the published receipt equals a fresh replay;
- the published receipt equals the uploaded reproduced receipt;
- the published closeout archive has SHA-256 `f93be72a7b6223633a88257435260f54d67c140f83505d9a16a3166473c3d8f5`.

Those statements are internally bound into this package, but this upload omits the underlying published closeout archive and frozen replay inputs. Therefore this assessment treats them as **documented claims with consistent hashes**, not as operations independently re-executed in this assessment.

## Scope conclusion

The strongest conclusion supported directly by the uploaded binding package is:

**The independent-reproduction binding artifact is internally coherent, manifest-valid, and self-consistent. It faithfully carries a reproduced PASS receipt and an independent assessment whose bytes and hashes agree across the package.**

The stronger underlying conclusion — that a frozen verifier was freshly replayed against the exact executor results and regenerated the receipt byte-for-byte — remains supported by the embedded assessment, but cannot be independently re-performed from this binding upload alone.

No broader external-world validity, universal correctness, or independent executor-from-fixtures reproduction is established here.
